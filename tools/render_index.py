#!/usr/bin/env python3
"""Render docs/INDEX.md: a browsable Markdown view of every record so the library can be read on
GitHub without opening YAML. Deterministic output; CI fails if the committed copy is stale.

Usage: python3 -I tools/render_index.py [repo_root]
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]


def load_all() -> list[tuple[Path, dict]]:
    out: list[tuple[Path, dict]] = []
    for d in ("vocabulary", "standards"):
        for p in sorted((ROOT / d).rglob("*.yaml")):
            with p.open() as fh:
                docs = list(yaml.safe_load_all(fh))
            for doc in docs:
                if isinstance(doc, dict):
                    out.append((p, doc))
    return out


def q(v: dict | None) -> str:
    """Render a Quantity dict compactly."""
    if not v:
        return ""
    if v.get("text") and v.get("value") is None and v.get("min_value") is None:
        return v["text"]
    if v.get("min_value") is not None or v.get("max_value") is not None:
        core = f"{v.get('min_value', '')} to {v.get('max_value', '')}".strip()
    else:
        core = "" if v.get("value") is None else f"{v['value']:g}"
    unit = v.get("unit")
    if unit == "factor":
        core += " x"
    elif unit and unit != "text":
        core += f" {unit}"
    if v.get("relative_to") and v["relative_to"] != "none":
        core += f" re {v['relative_to'].replace('_', ' ')}"
    if v.get("per"):
        core += f" per {v['per']}"
    return core.strip()


def cite(c: dict) -> str:
    bits = []
    if c.get("table"):
        bits.append(c["table"])
    if c.get("clause"):
        bits.append(f"§{c['clause']}")
    if c.get("page"):
        bits.append(f"p. {c['page']}")
    if c.get("pdf_page"):
        bits.append(f"pdf {c['pdf_page']}")
    return ", ".join(bits)


def render_matrix(doc: dict, rel: str) -> list[str]:
    out = [f"#### {doc['title']}", ""]
    out.append(f"`{doc['id']}` · {cite(doc['citation'])} · regime: {doc.get('regime', 'all')} · confidence: {doc.get('confidence', 'verified')} · [{rel}]({rel})")
    out.append("")
    cols = doc["columns"]
    out.append("| Test | Clause | " + " | ".join(c["label"] for c in cols) + " |")
    out.append("|---|---|" + "|".join("---" for _ in cols) + "|")
    for r in doc["rows"]:
        label = r["label"] + (f" ({r['variant']})" if r.get("variant") else "")
        cells = []
        for c in cols:
            cell = r["cells"].get(c["id"])
            if cell is None:
                cells.append("")
            else:
                s = f"`{cell['code']}`"
                if cell.get("footnotes"):
                    s += " " + ",".join(cell["footnotes"])
                cells.append(s)
        out.append(f"| {label} | {r.get('clause') or ''} | " + " | ".join(cells) + " |")
    if doc.get("legend"):
        out.append("")
        out.append("Legend: " + "; ".join(f"`{k}` = {v}" for k, v in doc["legend"].items()))
    if doc.get("footnotes"):
        out.append("")
        for k, v in doc["footnotes"].items():
            out.append(f"- {k}: {v}")
    out.append("")
    return out


def render_params(doc: dict, rel: str) -> list[str]:
    out = [f"#### {doc['title']}", ""]
    out.append(f"`{doc['id']}` · test: `{doc['test_type']}`" + (f" / {doc['variant']}" if doc.get("variant") else "") + f" · {cite(doc['citation'])} · confidence: {doc.get('confidence', 'verified')} · [{rel}]({rel})")
    if doc.get("level_of_assembly"):
        out.append("")
        out.append("Levels: " + ", ".join(doc["level_of_assembly"]))
    out.append("")
    regimes = list(doc["by_regime"].keys())
    fields = ["level", "duration", "cycles", "margin", "temperature_range", "sweep_rate", "actuations", "axes", "dwell", "rate"]
    used = [f for f in fields if any(doc["by_regime"][r].get(f) for r in regimes)]
    extras = sorted({k for r in regimes for k in (doc["by_regime"][r].get("extra") or {})})
    out.append("| Regime | " + " | ".join(used + [f"extra: {e}" for e in extras]) + " | footnotes |")
    out.append("|---|" + "|".join("---" for _ in used + extras) + "|---|")
    for r in regimes:
        ps = doc["by_regime"][r]
        vals = [q(ps.get(f)) for f in used] + [q((ps.get("extra") or {}).get(e)) for e in extras]
        out.append(f"| {r} | " + " | ".join(vals) + " | " + ",".join(ps.get("footnotes", [])) + " |")
    if doc.get("footnotes"):
        out.append("")
        for k, v in doc["footnotes"].items():
            out.append(f"- {k}: {v}")
    if doc.get("notes"):
        out.append("")
        out.append(doc["notes"].strip())
    out.append("")
    return out


def render_provision(doc: dict, rel: str) -> list[str]:
    out = [f"#### {doc['title']}", ""]
    out.append(f"`{doc['id']}` · {cite(doc['citation'])} · confidence: {doc.get('confidence', 'verified')} · [{rel}]({rel})")
    out.append("")
    out.append(doc["summary"].strip())
    out.append("")
    for p in doc["permits"]:
        line = f"- **{p['action']}**: {p['description'].strip()}"
        if p.get("constraints"):
            line += f" Constraints: {p['constraints'].strip()}"
        out.append(line)
    if doc.get("approval"):
        out.append(f"- Approval: {doc['approval']}")
    if doc.get("documentation"):
        out.append(f"- Recorded in: {doc['documentation']}")
    out.append("")
    return out


def render_rule(doc: dict, rel: str) -> list[str]:
    out = [f"#### {doc['title']}", ""]
    out.append(f"`{doc['id']}` · {doc['category']} · {cite(doc['citation'])} · confidence: {doc.get('confidence', 'verified')} · [{rel}]({rel})")
    out.append("")
    out.append(doc["statement"].strip())
    if doc.get("values"):
        out.append("")
        out.append("| Value | |")
        out.append("|---|---|")
        for k, v in doc["values"].items():
            out.append(f"| {k} | {q(v)} |")
    if doc.get("before") or doc.get("after"):
        out.append("")
        out.append(f"Sequence: after {doc.get('before') or []}; before {doc.get('after') or []}")
    out.append("")
    return out


def main() -> int:
    records = load_all()
    lines = ["# Library index", "", "Generated by `tools/render_index.py`; do not edit by hand.", ""]

    vocab = [(p, d) for p, d in records if d.get("kind") == "vocabulary"]
    lines += ["## Vocabularies", ""]
    for p, d in vocab:
        rel = p.relative_to(ROOT).as_posix()
        lines.append(f"- **{d['vocabulary']}** ({len(d['entries'])} entries) · [{rel}]({rel}): " + ", ".join(f"`{e['id']}`" for e in d["entries"]))
    lines.append("")

    stds = {d["id"]: (p, d) for p, d in records if d.get("kind") == "standard"}
    lines += ["## Standards", ""]
    lines.append("| id | designation | edition | status | access |")
    lines.append("|---|---|---|---|---|")
    for sid, (p, d) in sorted(stds.items()):
        lines.append(f"| `{sid}` | {d['designation']} | {d['date']} | {d.get('status', '')} | {d.get('access', '')} |")
    lines.append("")

    for sid, (sp, sd) in sorted(stds.items()):
        lines += [f"## {sd['designation']}: {sd['title']}", ""]
        lines.append(sd["scope"].strip())
        lines.append("")
        mine = [(p, d) for p, d in records if d.get("standard") == sid and d.get("kind") != "standard"]
        for kind, title, fn in (
            ("applicability_matrix", "Applicability matrices", render_matrix),
            ("test_parameters", "Test levels and durations", render_params),
            ("tailoring_provision", "Tailoring provisions", render_provision),
            ("rule", "Rules", render_rule),
        ):
            group = [(p, d) for p, d in mine if d.get("kind") == kind]
            if not group:
                continue
            lines += [f"### {title}", ""]
            for p, d in group:
                lines += fn(d, p.relative_to(ROOT).as_posix())

    out = ROOT / "docs" / "INDEX.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines).rstrip() + "\n")
    print(f"wrote {out.relative_to(ROOT)} ({len(records)} records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
