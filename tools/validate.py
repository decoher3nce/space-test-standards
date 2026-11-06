#!/usr/bin/env python3
"""Validate every YAML record in the library against the vendored JSON Schema and check
cross-record references. Exit code 1 on any problem.

Usage: python3 -I tools/validate.py [repo_root]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
RECORD_DIRS = ["vocabulary", "standards"]


def load_schemas() -> dict[str, Draft202012Validator]:
    out: dict[str, Draft202012Validator] = {}
    for p in sorted((ROOT / "schema").glob("*.schema.json")):
        kind = p.name.removesuffix(".schema.json")
        out[kind] = Draft202012Validator(json.loads(p.read_text()))
    return out


def iter_records(errors: list[str]) -> list[tuple[Path, dict]]:
    recs: list[tuple[Path, dict]] = []
    for d in RECORD_DIRS:
        for p in sorted((ROOT / d).rglob("*.yaml")):
            with p.open() as fh:
                try:
                    docs = list(yaml.safe_load_all(fh))
                except yaml.YAMLError as e:
                    errors.append(f"{p.relative_to(ROOT)}: YAML parse error: {str(e).splitlines()[0]}")
                    continue
            for doc in docs:
                if doc is None:
                    continue
                recs.append((p, doc if isinstance(doc, dict) else {"kind": "<invalid>"}))
    return recs


def main() -> int:
    schemas = load_schemas()
    errors: list[str] = []
    records = iter_records(errors)

    # 1. schema validation
    for path, doc in records:
        kind = doc.get("kind")
        rel = path.relative_to(ROOT)
        if kind not in schemas:
            errors.append(f"{rel}: unknown or missing kind {kind!r}")
            continue
        for err in sorted(schemas[kind].iter_errors(doc), key=lambda e: list(e.path)):
            loc = "/".join(str(x) for x in err.path) or "<root>"
            errors.append(f"{rel}: {loc}: {err.message}")

    # 2. collect vocabularies and ids
    vocab: dict[str, set[str]] = {}
    ids: dict[str, Path] = {}
    standards: set[str] = set()
    param_ids: set[str] = set()
    for path, doc in records:
        kind = doc.get("kind")
        if kind == "vocabulary":
            vocab.setdefault(doc["vocabulary"], set()).update(e["id"] for e in doc.get("entries", []))
        elif kind == "standard":
            standards.add(doc["id"])
        if kind in {"standard", "applicability_matrix", "test_parameters", "tailoring_provision", "rule"}:
            rid = doc.get("id")
            if rid in ids:
                errors.append(f"{path.relative_to(ROOT)}: duplicate id {rid!r} (also in {ids[rid].relative_to(ROOT)})")
            elif rid:
                ids[rid] = path
            if kind == "test_parameters" and rid:
                param_ids.add(rid)

    test_types = vocab.get("test_type", set())
    levels = vocab.get("level_of_assembly", set())
    hw = vocab.get("hardware_type", set())
    flags = vocab.get("flag", set())

    # 3. referential checks
    for path, doc in records:
        rel = path.relative_to(ROOT)
        kind = doc.get("kind")
        if kind in {"applicability_matrix", "test_parameters", "tailoring_provision", "rule"}:
            if doc.get("standard") not in standards:
                errors.append(f"{rel}: standard {doc.get('standard')!r} has no standard.yaml record")
            cit = doc.get("citation") or {}
            if cit.get("standard") not in standards:
                errors.append(f"{rel}: citation.standard {cit.get('standard')!r} unknown")
            if not (cit.get("clause") or cit.get("table")):
                errors.append(f"{rel}: citation needs a clause or a table")
        if kind == "applicability_matrix":
            dim = doc.get("column_dimension")
            allowed = levels if dim == "level_of_assembly" else hw if dim == "hardware_type" else None
            for col in doc.get("columns", []):
                if allowed is not None and col["id"] not in allowed:
                    errors.append(f"{rel}: column id {col['id']!r} not in {dim} vocabulary")
            for row in doc.get("rows", []):
                if row.get("test_type") not in test_types:
                    errors.append(f"{rel}: row {row.get('label')!r} test_type {row.get('test_type')!r} not in vocabulary")
                pref = row.get("parameters_ref")
                if pref and pref not in param_ids:
                    errors.append(f"{rel}: row {row.get('label')!r} parameters_ref {pref!r} not found")
                colset = {c["id"] for c in doc.get("columns", [])}
                for cid, cell in (row.get("cells") or {}).items():
                    if cid not in colset:
                        errors.append(f"{rel}: row {row.get('label')!r} cell column {cid!r} undefined")
                    for f in cell.get("footnotes", []):
                        if f not in (doc.get("footnotes") or {}):
                            errors.append(f"{rel}: row {row.get('label')!r} footnote {f!r} undefined")
        if kind == "test_parameters":
            if doc.get("test_type") not in test_types:
                errors.append(f"{rel}: test_type {doc.get('test_type')!r} not in vocabulary")
            for hwid in doc.get("hardware_type") or []:
                if hwid not in hw:
                    errors.append(f"{rel}: hardware_type {hwid!r} not in vocabulary")
            for regime, ps in (doc.get("by_regime") or {}).items():
                for f in ps.get("footnotes", []):
                    if f not in (doc.get("footnotes") or {}):
                        errors.append(f"{rel}: {regime} footnote {f!r} undefined")
        if kind in {"tailoring_provision", "rule"}:
            scope = doc.get("applies_to") or {}
            for tt in scope.get("test_types", []):
                if tt not in test_types:
                    errors.append(f"{rel}: applies_to.test_types {tt!r} not in vocabulary")
            for h in scope.get("hardware_types", []):
                if h not in hw:
                    errors.append(f"{rel}: applies_to.hardware_types {h!r} not in vocabulary")
            for fl in scope.get("flags", []):
                if fl not in flags:
                    errors.append(f"{rel}: applies_to.flags {fl!r} not in vocabulary")
            for tt in list(doc.get("before", [])) + list(doc.get("after", [])):
                if tt not in test_types:
                    errors.append(f"{rel}: sequence test_type {tt!r} not in vocabulary")

    counts: dict[str, int] = {}
    for _, doc in records:
        counts[doc.get("kind", "?")] = counts.get(doc.get("kind", "?"), 0) + 1
    print("records:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print(" -", e)
        return 1
    print("OK: all records valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
