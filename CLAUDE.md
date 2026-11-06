# space-test-standards — working notes for Claude Code

Public aerospace test standards encoded as YAML records with citations. Data only; the consumer is
the sibling repo `../bespoke`.

## Commands

```bash
python3 -I tools/validate.py          # JSON Schema + cross-reference checks (needs pyyaml, jsonschema)
python3 -I tools/render_index.py      # regenerates docs/INDEX.md; commit it with the records
```

## Rules

- Structured values, codes and clause/table/page citations only. Never paste the standards' text;
  paraphrase footnotes briefly. ECSS is copyrighted; GEVS and the MAR are US Government works;
  SSC-S-016 is a public release.
- Keep the raw printed code in every matrix cell and add the unified reading from
  `vocabulary/requirement-codes.yaml`.
- `confidence: verified` only for values read from the named edition of the document itself;
  `deck_only` / `secondary` otherwise, with a note saying what to verify against.
- Ids are lowercase and prefixed `<standard-id>.matrix.|params.|provision.|rule.`.
- Vocabulary ids are shared across standards; add aliases rather than new ids where a concept
  already exists, and never rename an id without updating every record that uses it.
- Nothing proprietary, customer-specific or export-controlled is accepted.
- The JSON Schema files under `schema/` are exported from Bespoke's Pydantic models
  (`bespoke schema export`); edit the models, not the schema files.
