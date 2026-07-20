#!/usr/bin/env python3
"""Inject missing optional keyword parameters from the v2.7.2 compat report into
current function signatures so call sites and the compat_diff script agree.

For each param mismatch in scripts/compat_report_v272.json, add
``name=None`` as keyword-only (or trailing optional) parameters when absent.

Does NOT change function bodies (legacy_compat / dual-attrs still handle values).
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


def load_mismatches(report_path: Path) -> dict[tuple[str, str], list[str]]:
    data = json.loads(report_path.read_text(encoding="utf-8"))
    out: dict[tuple[str, str], list[str]] = {}
    for m in data.get("param_mismatches", []):
        # use new_file if present else old_file
        f = m.get("new_file") or m.get("old_file")
        q = m["qualname"]
        out[(f, q)] = list(m["missing_params"])
    return out


class ParamInjector(ast.NodeTransformer):
    def __init__(self, wanted: dict[str, list[str]]) -> None:
        # qualname -> missing params for THIS file
        self.wanted = wanted
        self.class_stack: list[str] = []
        self.changed = False

    def visit_ClassDef(self, node: ast.ClassDef):
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()
        return node

    def _qual(self, name: str) -> str:
        if self.class_stack:
            return ".".join([*self.class_stack, name])
        return name

    def _inject(self, node: ast.AST) -> ast.AST:
        assert isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        q = self._qual(node.name)
        # also bare method name keys if class.method
        missing = self.wanted.get(q)
        if missing is None and self.class_stack:
            # try Class.method exact
            pass
        if not missing:
            return node

        existing: set[str] = set()
        for a in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
            existing.add(a.arg)
        if node.args.vararg:
            existing.add("*" + node.args.vararg.arg)
        if node.args.kwarg:
            existing.add("**" + node.args.kwarg.arg)

        to_add = [p for p in missing if p not in existing and not p.startswith("*")]
        if not to_add:
            return node

        # Add as keyword-only with default None
        for p in to_add:
            node.args.kwonlyargs.append(ast.arg(arg=p, annotation=None))
            node.args.kw_defaults.append(ast.Constant(value=None))
        self.changed = True
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        node = self._inject(node)
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        node = self._inject(node)
        self.generic_visit(node)
        return node


def patch_file(path: Path, qual_to_params: dict[str, list[str]]) -> bool:
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False

    inj = ParamInjector(qual_to_params)
    tree = inj.visit(tree)
    if not inj.changed:
        return False

    ast.fix_missing_locations(tree)
    try:
        new_src = ast.unparse(tree)
    except Exception:
        return False

    # preserve trailing newline
    if not new_src.endswith("\n"):
        new_src += "\n"
    path.write_text(new_src, encoding="utf-8")
    return True


def main() -> int:
    root = Path.cwd()
    report = root / "scripts" / "compat_report_v272.json"
    if not report.exists():
        return 2

    mismatches = load_mismatches(report)
    # group by file
    by_file: dict[str, dict[str, list[str]]] = {}
    for (f, q), params in mismatches.items():
        by_file.setdefault(f, {})[q] = params

    changed = 0
    for fpath, qmap in sorted(by_file.items()):
        p = root / fpath
        if not p.is_file():
            continue
        if patch_file(p, qmap):
            changed += 1
        else:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
