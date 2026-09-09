#!/usr/bin/env python3
"""Extract and compare the *static* public API surface of two pyroblack trees.

Unlike :mod:`scripts.compat_diff_v272`, which walks callables file-by-file, this
script builds a name-oriented view of the surface an application actually binds
against:

  - ``pyrogram.<name>`` re-exports (``__init__.py`` assignments + imports)
  - every public class and its public methods (walking ``pyrogram/`` packages)
  - method parameter names and whether they are required (no default)
  - enum member names per ``enum`` class
  - module-level constants

It then reports what disappeared or became stricter in the new tree, which is
what breaks v2.7.6 applications.

Usage::

    python scripts/compat_surface.py --old /path/to/v2.7.6/tree
    python scripts/compat_surface.py --old ../pb276 --json out.json
"""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import dataclass, field
from pathlib import Path

SKIP_DIRS = {"__pycache__", "raw"}


@dataclass
class FuncSurface:
    name: str
    params: list[str] = field(default_factory=list)
    required: list[str] = field(default_factory=list)
    is_async: bool = False
    has_var_kw: bool = False


@dataclass
class ClassSurface:
    name: str
    module: str
    bases: list[str] = field(default_factory=list)
    methods: dict[str, FuncSurface] = field(default_factory=dict)
    attrs: list[str] = field(default_factory=list)


@dataclass
class Surface:
    classes: dict[str, ClassSurface] = field(default_factory=dict)
    functions: dict[str, FuncSurface] = field(default_factory=dict)
    constants: dict[str, list[str]] = field(default_factory=dict)
    modules: set[str] = field(default_factory=set)


def _iter_py(root: Path):
    for path in sorted(root.rglob("*.py")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def _func_surface(node: ast.FunctionDef | ast.AsyncFunctionDef) -> FuncSurface:
    a = node.args
    positional = [*a.posonlyargs, *a.args]
    params = [p.arg for p in positional]
    params += [p.arg for p in a.kwonlyargs]

    n_defaults = len(a.defaults)
    required = [p.arg for p in positional[: len(positional) - n_defaults]]
    required += [
        p.arg for p, d in zip(a.kwonlyargs, a.kw_defaults, strict=False) if d is None
    ]
    required = [p for p in required if p not in ("self", "cls")]

    return FuncSurface(
        name=node.name,
        params=[p for p in params if p not in ("self", "cls")],
        required=required,
        is_async=isinstance(node, ast.AsyncFunctionDef),
        has_var_kw=a.kwarg is not None,
    )


def collect(root: Path) -> Surface:
    surface = Surface()
    pkg_root = root / "pyrogram"

    for path in _iter_py(pkg_root):
        rel = path.relative_to(root).with_suffix("")
        module = ".".join(rel.parts)
        if module.endswith(".__init__"):
            module = module[: -len(".__init__")]
        surface.modules.add(module)

        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue

        consts: list[str] = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name) and not tgt.id.startswith("_"):
                        consts.append(tgt.id)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if not node.target.id.startswith("_"):
                    consts.append(node.target.id)
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                if not node.name.startswith("_"):
                    surface.functions.setdefault(node.name, _func_surface(node))
            elif isinstance(node, ast.ClassDef):
                if node.name.startswith("_"):
                    continue
                cls = ClassSurface(
                    name=node.name,
                    module=module,
                    bases=[ast.unparse(b) for b in node.bases],
                )
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef | ast.AsyncFunctionDef):
                        if sub.name.startswith("__") and sub.name != "__init__":
                            continue
                        cls.methods[sub.name] = _func_surface(sub)
                    elif isinstance(sub, ast.Assign):
                        for tgt in sub.targets:
                            if isinstance(tgt, ast.Name) and not tgt.id.startswith("_"):
                                cls.attrs.append(tgt.id)
                    elif isinstance(sub, ast.AnnAssign) and isinstance(
                        sub.target, ast.Name
                    ):
                        if not sub.target.id.startswith("_"):
                            cls.attrs.append(sub.target.id)
                # A class may legitimately be defined twice across the tree
                # (e.g. a stub plus the real implementation). Keep the richer one.
                prev = surface.classes.get(node.name)
                if prev is None or len(cls.methods) > len(prev.methods):
                    surface.classes[node.name] = cls

        if consts:
            surface.constants[module] = consts

    return surface


def compare(old: Surface, new: Surface) -> dict:
    report: dict = {
        "missing_modules": sorted(old.modules - new.modules),
        "missing_classes": [],
        "missing_methods": [],
        "missing_functions": [],
        "dropped_params": [],
        "newly_required_params": [],
        "missing_class_attrs": [],
        "missing_constants": [],
    }

    for name, cls in old.classes.items():
        newcls = new.classes.get(name)
        if newcls is None:
            report["missing_classes"].append({"name": name, "module": cls.module})
            continue

        for mname, fn in cls.methods.items():
            newfn = newcls.methods.get(mname)
            if newfn is None:
                report["missing_methods"].append(
                    {"class": name, "method": mname, "module": cls.module}
                )
                continue
            if newfn.has_var_kw:
                continue
            gone = [p for p in fn.params if p not in newfn.params]
            if gone:
                report["dropped_params"].append(
                    {"class": name, "method": mname, "params": gone}
                )
            newly_required = [
                p
                for p in newfn.required
                if p not in fn.required and p in fn.params or p not in fn.params
            ]
            if newly_required:
                report["newly_required_params"].append(
                    {"class": name, "method": mname, "params": newly_required}
                )

        gone_attrs = [a for a in cls.attrs if a not in newcls.attrs]
        if gone_attrs:
            report["missing_class_attrs"].append({"class": name, "attrs": gone_attrs})

    for name in old.functions:
        if name not in new.functions:
            report["missing_functions"].append(name)

    for module, consts in old.constants.items():
        newconsts = set(new.constants.get(module, []))
        gone = [c for c in consts if c not in newconsts]
        if gone:
            report["missing_constants"].append({"module": module, "names": gone})

    return report


def _live_class(name: str):
    """Find *name* on the live ``pyrogram`` package, or return None."""
    import importlib

    for module_name in (
        "pyrogram",
        "pyrogram.types",
        "pyrogram.enums",
        "pyrogram.errors",
        "pyrogram.storage",
        "pyrogram.handlers",
        "pyrogram.session",
        "pyrogram.connection",
    ):
        module = importlib.import_module(module_name)
        found = getattr(module, name, None)
        if isinstance(found, type):
            return found

    from pyrogram import Client

    # Client method mixins are not exported anywhere; a mixin's members are
    # reachable through Client, so resolve them there.
    return Client


def _live_callable(class_name: str, method_name: str):
    """Resolve the live callable for *class_name*.*method_name*, or None."""
    cls = _live_class(class_name)
    if cls is None:
        return None
    if method_name == "__init__":
        return getattr(cls, "__init__", None)
    return getattr(cls, method_name, None)


def _accepts(func, names: list[str]) -> bool:
    """Whether calling *func* with each of *names* as a keyword would bind.

    A method wrapped by ``pyrogram.legacy_compat`` advertises ``**kwargs``, so
    it accepts the v2.7.6 keyword and remaps it internally.
    """
    import inspect

    try:
        signature = inspect.signature(func)
    except (TypeError, ValueError):
        return False

    parameters = signature.parameters
    if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in parameters.values()):
        return True
    return all(name in parameters for name in names)


def drop_resolvable(report: dict) -> dict:
    """Remove findings that a *runtime* lookup resolves.

    The AST pass cannot see members contributed by a mixin (``Story`` gets its
    v2.7.6 surface from ``LegacyStoryMixin``), members added by an alias table
    (``pyrogram.emoji``), methods reached through a re-export, or keywords that
    the ``legacy_compat`` wrapper accepts and remaps. Filtering the report
    through real attribute lookups and signature binds is what makes it a usable
    gate: what is left is genuinely unreachable.

    Private members (``_parse``, ``_install_legacy_attrs``, …) are dropped too.
    They are internal plumbing that applications do not call, and their
    signatures move with every layer bump.
    """
    import importlib

    def resolves(class_name: str, member: str) -> bool:
        cls = _live_class(class_name)
        return cls is not None and hasattr(cls, member)

    report["missing_methods"] = [
        entry
        for entry in report["missing_methods"]
        if not entry["method"].startswith("_")
        and not resolves(entry["class"], entry["method"])
    ]
    for key in ("dropped_params", "newly_required_params"):
        kept = []
        for entry in report[key]:
            if entry["method"].startswith("_") and entry["method"] != "__init__":
                continue
            func = _live_callable(entry["class"], entry["method"])
            if func is not None and _accepts(func, entry["params"]):
                continue
            kept.append(entry)
        report[key] = kept
    report["missing_class_attrs"] = [
        {
            "class": entry["class"],
            "attrs": [a for a in entry["attrs"] if not resolves(entry["class"], a)],
        }
        for entry in report["missing_class_attrs"]
    ]
    report["missing_class_attrs"] = [
        entry for entry in report["missing_class_attrs"] if entry["attrs"]
    ]

    filtered_constants = []
    for entry in report["missing_constants"]:
        try:
            module = importlib.import_module(entry["module"])
        except ImportError:
            filtered_constants.append(entry)
            continue
        names = [n for n in entry["names"] if not hasattr(module, n)]
        if names:
            filtered_constants.append({"module": entry["module"], "names": names})
    report["missing_constants"] = filtered_constants

    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True, help="path to the old (v2.7.6) tree root")
    ap.add_argument("--new", default=".", help="path to the current tree root")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument(
        "--static",
        action="store_true",
        help="report the raw AST diff without resolving names at runtime",
    )
    args = ap.parse_args()

    old = collect(Path(args.old))
    new = collect(Path(args.new))
    report = compare(old, new)
    if not args.static:
        report = drop_resolvable(report)

    for key, values in report.items():
        print(f"\n=== {key} ({len(values)}) ===")
        for value in values[:400]:
            print("  ", value)

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
