#!/usr/bin/env python3
"""Compare public callables between an old pyroblack tag (default: v2.7.2) and the
current working tree.

For every Python file under ``pyrogram/`` in the old tag, extract:
  - function / method name
  - class (if any)
  - file path + line number
  - parameter names
  - return type annotation (as source text)

Then look for the same callable in the current tree (same relative path preferred,
with fallback search by class+name / name only) and report mismatches.

Usage:
  python scripts/compat_diff_v272.py
  python scripts/compat_diff_v272.py --old-tag v2.7.2 --root pyrogram
  python scripts/compat_diff_v272.py --json report.json
  python scripts/compat_diff_v272.py --skip-raw   # ignore pyrogram/raw (huge TL gen)
  python scripts/compat_diff_v272.py --params     # also report param-name diffs

Exit code:
  0 = no missing callables (return-type-only diffs still print, exit 0)
  1 = at least one missing file or missing callable
  2 = tool error (git / parse)
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------


@dataclass
class CallableInfo:
    """One function or method definition."""

    file: str
    line: int
    name: str
    class_name: str | None
    qualname: str  # Class.name or name
    params: list[str]
    return_type: str | None  # annotation as unparsed source, or None
    is_async: bool
    is_method: bool  # defined inside a class

    def key(self) -> str:
        return f"{self.file}::{self.qualname}"


@dataclass
class Report:
    old_tag: str
    root: str
    old_files: int = 0
    new_files: int = 0
    old_callables: int = 0
    new_callables: int = 0
    missing_files: list[str] = field(default_factory=list)
    missing_callables: list[dict] = field(default_factory=list)
    return_type_mismatches: list[dict] = field(default_factory=list)
    param_mismatches: list[dict] = field(default_factory=list)
    moved_callables: list[dict] = field(default_factory=list)  # found elsewhere
    parse_errors_old: list[str] = field(default_factory=list)
    parse_errors_new: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Git / filesystem helpers
# ---------------------------------------------------------------------------


def run_git(args: list[str], cwd: Path) -> str:
    r = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        msg = f"git {' '.join(args)} failed:\n{r.stderr or r.stdout}"
        raise RuntimeError(
            msg,
        )
    return r.stdout


def list_py_files(tag: str, root: str, cwd: Path) -> list[str]:
    out = run_git(["ls-tree", "-r", "--name-only", tag, root], cwd)
    return sorted(
        line.replace("\\", "/") for line in out.splitlines() if line.endswith(".py")
    )


def git_show(tag: str, path: str, cwd: Path) -> str:
    return run_git(["show", f"{tag}:{path}"], cwd)


def read_workspace(path: str, cwd: Path) -> str | None:
    p = cwd / path
    if not p.is_file():
        return None
    return p.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# AST extraction
# ---------------------------------------------------------------------------


def _ann_to_str(node: ast.expr | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return getattr(node, "id", None) or type(node).__name__


def _params(fn: ast.AST) -> list[str]:
    assert isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef))
    names: list[str] = []
    for a in fn.args.posonlyargs:
        names.append(a.arg)
    for a in fn.args.args:
        names.append(a.arg)
    if fn.args.vararg:
        names.append("*" + fn.args.vararg.arg)
    for a in fn.args.kwonlyargs:
        names.append(a.arg)
    if fn.args.kwarg:
        names.append("**" + fn.args.kwarg.arg)
    return names


def extract_callables(src: str, file: str) -> list[CallableInfo]:
    """Extract top-level functions and class methods (one level of class nesting)."""
    try:
        tree = ast.parse(src, filename=file)
    except SyntaxError as e:
        msg = f"{file}: {e}"
        raise SyntaxError(msg) from e

    found: list[CallableInfo] = []

    def add_fn(
        fn: ast.AST,
        class_name: str | None,
    ) -> None:
        assert isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef))
        # skip nested defs inside methods
        name = fn.name
        # optionally skip dunders except __init__/__call__
        qual = f"{class_name}.{name}" if class_name else name
        found.append(
            CallableInfo(
                file=file,
                line=fn.lineno,
                name=name,
                class_name=class_name,
                qualname=qual,
                params=_params(fn),
                return_type=_ann_to_str(fn.returns),
                is_async=isinstance(fn, ast.AsyncFunctionDef),
                is_method=class_name is not None,
            ),
        )

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add_fn(node, None)
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add_fn(item, node.name)
                # nested class one level deeper (rare but exists)
                elif isinstance(item, ast.ClassDef):
                    nested = f"{node.name}.{item.name}"
                    for sub in item.body:
                        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            add_fn(sub, nested)

    return found


def index_by_qualname(
    items: Iterable[CallableInfo],
) -> dict[str, list[CallableInfo]]:
    """Map Class.name or name -> list of definitions (may appear in many files)."""
    idx: dict[str, list[CallableInfo]] = defaultdict(list)
    for c in items:
        idx[c.qualname].append(c)
        # also bare name for fallback
        idx.setdefault(c.name, []).append(c)
    return idx


# ---------------------------------------------------------------------------
# Compare
# ---------------------------------------------------------------------------


def normalize_return(rt: str | None) -> str | None:
    if rt is None:
        return None
    s = rt.strip()
    # strip wrapping quotes from string annotations: 'None' / "Message"
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        s = s[1:-1]
    s = s.replace(" ", "")
    # common equivalent annotations
    if s in ("None", "NoneType"):
        return "None"
    aliases = {
        "types.Message": "Message",
        "types.User": "User",
        "types.Chat": "Chat",
        "Optional[str]": "str|None",
        "Optional[int]": "int|None",
        "Optional[bool]": "bool|None",
        "List[": "list[",
        "Dict[": "dict[",
        "Tuple[": "tuple[",
        "Optional[": "Optional[",
    }
    for a, b in aliases.items():
        s = s.replace(a, b)
    return s


def params_significant(params: list[str]) -> list[str]:
    """Drop self/cls for comparison."""
    return [p for p in params if p not in ("self", "cls")]


def compare(
    old_tag: str,
    root: str,
    cwd: Path,
    skip_raw: bool,
    check_params: bool,
    include_private: bool,
) -> Report:
    report = Report(old_tag=old_tag, root=root)

    old_files = list_py_files(old_tag, root, cwd)
    if skip_raw:
        old_files = [
            f
            for f in old_files
            if "/raw/" not in f and not f.startswith("pyrogram/raw/")
        ]

    new_files_set = (
        {str(p.relative_to(cwd)).replace("\\", "/") for p in (cwd / root).rglob("*.py")}
        if (cwd / root).exists()
        else set()
    )
    if skip_raw:
        new_files_set = {
            f
            for f in new_files_set
            if "/raw/" not in f and not f.startswith("pyrogram/raw/")
        }

    report.old_files = len(old_files)
    report.new_files = len(new_files_set)

    # Build full new index (all callables in workspace under root)
    all_new: list[CallableInfo] = []
    for nf in sorted(new_files_set):
        src = read_workspace(nf, cwd)
        if src is None:
            continue
        try:
            all_new.extend(extract_callables(src, nf))
        except SyntaxError as e:
            report.parse_errors_new.append(str(e))

    if not include_private:
        all_new = [
            c
            for c in all_new
            if not c.name.startswith("_")
            or c.name in ("__init__", "__call__", "__aenter__", "__aexit__")
        ]

    report.new_callables = len(all_new)
    new_by_file_qual: dict[tuple[str, str], CallableInfo] = {}
    for c in all_new:
        new_by_file_qual[(c.file, c.qualname)] = c
    new_by_qual = index_by_qualname(all_new)

    # Walk old files
    for of in old_files:
        if of not in new_files_set:
            report.missing_files.append(of)

        try:
            old_src = git_show(old_tag, of, cwd)
        except RuntimeError as e:
            report.parse_errors_old.append(str(e))
            continue

        try:
            old_callables = extract_callables(old_src, of)
        except SyntaxError as e:
            report.parse_errors_old.append(str(e))
            continue

        if not include_private:
            old_callables = [
                c
                for c in old_callables
                if not c.name.startswith("_")
                or c.name in ("__init__", "__call__", "__aenter__", "__aexit__")
            ]

        report.old_callables += len(old_callables)

        new_src = read_workspace(of, cwd)
        new_in_same_file: dict[str, CallableInfo] = {}
        if new_src is not None:
            try:
                for c in extract_callables(new_src, of):
                    new_in_same_file[c.qualname] = c
            except SyntaxError as e:
                report.parse_errors_new.append(str(e))

        for oc in old_callables:
            # 1) same file + qualname
            nc = new_in_same_file.get(oc.qualname)
            location = "same_file"

            # 2) same qualname elsewhere
            if nc is None:
                candidates = [
                    x
                    for x in new_by_qual.get(oc.qualname, [])
                    if x.qualname == oc.qualname
                ]
                if candidates:
                    nc = candidates[0]
                    location = "moved"
                    report.moved_callables.append(
                        {
                            "old": {
                                "file": oc.file,
                                "line": oc.line,
                                "qualname": oc.qualname,
                            },
                            "new": {
                                "file": nc.file,
                                "line": nc.line,
                                "qualname": nc.qualname,
                            },
                        },
                    )

            # 3) bare name + same class name anywhere
            if nc is None and oc.class_name:
                for x in new_by_qual.get(oc.qualname, []):
                    if x.class_name == oc.class_name and x.name == oc.name:
                        nc = x
                        location = "moved"
                        break

            if nc is None:
                report.missing_callables.append(
                    {
                        "file": oc.file,
                        "line": oc.line,
                        "qualname": oc.qualname,
                        "params": params_significant(oc.params),
                        "return_type": oc.return_type,
                        "is_async": oc.is_async,
                    },
                )
                continue

            # Return type (compare normalized; skip pure annotation-style noise)
            ort = normalize_return(oc.return_type)
            nrt = normalize_return(nc.return_type)
            if ort != nrt and not (ort in (None, "None") and nrt in (None, "None")):
                # only report if at least one side had a meaningful annotation
                if oc.return_type is not None or nc.return_type is not None:
                    report.return_type_mismatches.append(
                        {
                            "qualname": oc.qualname,
                            "old_file": oc.file,
                            "old_line": oc.line,
                            "new_file": nc.file,
                            "new_line": nc.line,
                            "old_return": oc.return_type,
                            "new_return": nc.return_type,
                            "old_return_norm": ort,
                            "new_return_norm": nrt,
                            "location": location,
                        },
                    )

            if check_params:
                op = params_significant(oc.params)
                np = params_significant(nc.params)
                # **kwargs accepts any legacy keyword — not a hard API break
                if any(p.startswith("**") for p in np):
                    missing_params = []
                else:
                    missing_params = [
                        p for p in op if p not in np and not p.startswith("*")
                    ]
                if missing_params:
                    report.param_mismatches.append(
                        {
                            "qualname": oc.qualname,
                            "old_file": oc.file,
                            "old_line": oc.line,
                            "new_file": nc.file,
                            "new_line": nc.line,
                            "missing_params": missing_params,
                            "old_params": op,
                            "new_params": np,
                            "location": location,
                        },
                    )

    return report


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def print_report(report: Report, verbose: bool) -> None:
    w = sys.stdout.write
    w("=" * 72 + "\n")
    w(f"  pyroblack callable compatibility: {report.old_tag}  →  HEAD\n")
    w(f"  root: {report.root}\n")
    w("=" * 72 + "\n\n")

    w(f"Old files:        {report.old_files}\n")
    w(f"New files:        {report.new_files}\n")
    w(f"Old callables:    {report.old_callables}\n")
    w(f"New callables:    {report.new_callables}\n")
    w(f"Missing files:    {len(report.missing_files)}\n")
    w(f"Missing funcs:    {len(report.missing_callables)}\n")
    w(f"Moved funcs:      {len(report.moved_callables)}\n")
    w(f"Return mismatches:{len(report.return_type_mismatches)}\n")
    w(f"Param mismatches: {len(report.param_mismatches)}\n")
    w(f"Parse errors old: {len(report.parse_errors_old)}\n")
    w(f"Parse errors new: {len(report.parse_errors_new)}\n")
    w("\n")

    if report.missing_files:
        w("-" * 72 + "\n")
        w(f"MISSING FILES ({len(report.missing_files)})\n")
        w("-" * 72 + "\n")
        for f in report.missing_files:
            w(f"  {f}\n")
        w("\n")

    if report.missing_callables:
        w("-" * 72 + "\n")
        w(f"MISSING CALLABLES ({len(report.missing_callables)})\n")
        w("-" * 72 + "\n")
        # group by file
        by_file: dict[str, list[dict]] = defaultdict(list)
        for c in report.missing_callables:
            by_file[c["file"]].append(c)
        for fpath in sorted(by_file):
            w(f"\n  [{fpath}]\n")
            for c in by_file[fpath]:
                ret = c["return_type"] or "<none>"
                async_s = "async " if c["is_async"] else ""
                w(
                    f"    L{c['line']:>5}  {async_s}{c['qualname']}(...) -> {ret}\n",
                )
                if verbose:
                    w(f"             params: {c['params']}\n")
        w("\n")

    if report.moved_callables and verbose:
        w("-" * 72 + "\n")
        w(
            f"MOVED CALLABLES ({len(report.moved_callables)}) — still present elsewhere\n"
        )
        w("-" * 72 + "\n")
        for m in report.moved_callables[:200]:
            o, n = m["old"], m["new"]
            w(
                f"  {o['qualname']}\n"
                f"    old: {o['file']}:{o['line']}\n"
                f"    new: {n['file']}:{n['line']}\n",
            )
        if len(report.moved_callables) > 200:
            w(f"  ... +{len(report.moved_callables) - 200} more\n")
        w("\n")

    if report.return_type_mismatches:
        w("-" * 72 + "\n")
        w(f"RETURN TYPE MISMATCHES ({len(report.return_type_mismatches)})\n")
        w("-" * 72 + "\n")
        for m in report.return_type_mismatches[:300]:
            w(
                f"  {m['qualname']}  ({m['location']})\n"
                f"    old: {m['old_file']}:{m['old_line']}  -> {m['old_return']!r}\n"
                f"    new: {m['new_file']}:{m['new_line']}  -> {m['new_return']!r}\n",
            )
        if len(report.return_type_mismatches) > 300:
            w(f"  ... +{len(report.return_type_mismatches) - 300} more\n")
        w("\n")

    if report.param_mismatches:
        w("-" * 72 + "\n")
        w(f"PARAM MISMATCHES — names missing in new ({len(report.param_mismatches)})\n")
        w("-" * 72 + "\n")
        for m in report.param_mismatches[:300]:
            w(
                f"  {m['qualname']}\n"
                f"    old: {m['old_file']}:{m['old_line']}\n"
                f"    new: {m['new_file']}:{m['new_line']}\n"
                f"    missing params: {m['missing_params']}\n",
            )
        if len(report.param_mismatches) > 300:
            w(f"  ... +{len(report.param_mismatches) - 300} more\n")
        w("\n")

    if report.parse_errors_old or report.parse_errors_new:
        w("-" * 72 + "\n")
        w("PARSE ERRORS\n")
        w("-" * 72 + "\n")
        for e in report.parse_errors_old:
            w(f"  [old] {e}\n")
        for e in report.parse_errors_new:
            w(f"  [new] {e}\n")
        w("\n")

    w("=" * 72 + "\n")
    if report.missing_callables or report.missing_files:
        w("RESULT: FAIL — missing files and/or callables vs old tag\n")
    else:
        w("RESULT: OK — all old callables found (check return/param sections above)\n")
    w("=" * 72 + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Diff callables (name, location, return type) between an old "
        "pyroblack tag and the current tree.",
    )
    ap.add_argument(
        "--old-tag",
        default="v2.7.2",
        help="Git tag/commit for the old version (default: v2.7.2)",
    )
    ap.add_argument(
        "--root",
        default="pyrogram",
        help="Subtree to compare (default: pyrogram)",
    )
    ap.add_argument(
        "--cwd",
        default=".",
        help="Repo root (default: .)",
    )
    ap.add_argument(
        "--skip-raw",
        action="store_true",
        help="Skip pyrogram/raw (generated TL bindings, huge & noisy)",
    )
    ap.add_argument(
        "--params",
        action="store_true",
        help="Also report parameter names present in old but missing in new",
    )
    ap.add_argument(
        "--private",
        action="store_true",
        help="Include private (_foo) callables (except always-included dunders)",
    )
    ap.add_argument(
        "--json",
        metavar="PATH",
        help="Write full JSON report to PATH",
    )
    ap.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show moved callables and param lists",
    )
    args = ap.parse_args(argv)

    cwd = Path(args.cwd).resolve()
    if not (cwd / ".git").exists():
        return 2

    try:
        # ensure tag exists
        run_git(["rev-parse", "--verify", args.old_tag], cwd)
    except RuntimeError:
        return 2

    try:
        report = compare(
            old_tag=args.old_tag,
            root=args.root,
            cwd=cwd,
            skip_raw=args.skip_raw,
            check_params=args.params,
            include_private=args.private,
        )
    except Exception:
        return 2

    print_report(report, verbose=args.verbose)

    if args.json:
        out = {
            **{k: getattr(report, k) for k in report.__dataclass_fields__},
        }
        Path(args.json).write_text(
            json.dumps(out, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    if report.missing_callables or report.missing_files:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
