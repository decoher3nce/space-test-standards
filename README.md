# space-test-standards

Public aerospace environmental test standards, encoded as data.

Every applicability matrix, test level, duration, cycle count, margin and tailoring provision in
the standards below is stored as a YAML record with a clause or table citation, in one shared
vocabulary, so a program can look a requirement up, compare standards cell by cell, and trace a
tailored test plan back to the paragraph it came from. The repository is the data layer behind
[Bespoke](https://github.com/decoher3nce/bespoke), a tailoring compiler for payload test plans,
and is usable on its own from any language that reads YAML.

| Standard | What is encoded |
|---|---|
| GSFC-STD-7000B (GEVS, 2021) | Test factors and durations, factors of safety, structural/mechanical, EMC, thermal, cryogenic and contamination matrices, functional-test rules, permitted tailoring |
| ECSS-E-ST-10-03C Rev.1 (2022) | Equipment and element qualification, acceptance and protoflight baselines and their levels and durations; tolerances; Annex D tailoring |
| SSC-S-016 (2014 content; 2026 revision deltas) | Unit test matrices by hardware type, thermal ranges and cycle counts, tailoring exemptions |
| 320-MAR-1001 Rev. D | Per-class (A to D) applicability of the verification section and its DIDs |

Browse the whole library as tables in [docs/INDEX.md](docs/INDEX.md).

## Layout

```
vocabulary/        shared ids: test types, levels of assembly, hardware types, regimes, codes, flags
standards/<id>/    standard.yaml (metadata and terminology), then
  matrices/        applicability_matrix records: who must do which test (raw code kept, unified reading added)
  parameters/      test_parameters records: levels, durations, cycles, margins per regime
  tailoring/       tailoring_provision records: relaxations the standard itself allows
  rules/           rule records: sequence constraints, operating hours, factors of safety, probability levels
schema/            JSON Schema for every record kind (exported from Bespoke's Pydantic models)
tools/             validate.py (schema + cross-reference checks), render_index.py (docs/INDEX.md)
```

A file may hold several records separated by `---` when they come from one table.

## Record kinds in one minute

- **applicability_matrix**: rows are unified `test_type`s, columns are levels of assembly or hardware
  types. Each cell keeps the `code` exactly as printed (`T2`, `X`, `ER`, `R(8)`) and adds a unified
  `requirement` (`required`, `required_unless_justified`, `evaluate`, `customer_decision`, …), an
  optional `method`, footnote ids and a paraphrased `condition`.
- **test_parameters**: one test, with a `ParameterSet` per regime (`qualification`, `protoflight`,
  `acceptance`, or `all`). Every value is a `Quantity` with an explicit `unit` and `relative_to`
  (for example `3 dB re limit_level`, `1 min per axis`, `10 degC re max_predicted`).
- **tailoring_provision**: what the standard itself lets a program relax, with the approval and
  documentation it demands. A tailoring tool classifies a relaxation as *permitted tailoring* only
  when it can cite one of these; otherwise it is a *deviation*.
- **rule**: everything else with structure (12 cycles before flight, 1000 operating hours,
  factors of safety, 95/50 probability levels, "magnetics after vibration").
- **vocabulary**: the unified ids, each with the words every standard uses for it.

Regime names are mapped (`protoflight` ≈ SSC protoqualification ≈ ECSS PFM) for intent only; the
factors are never copied across standards.

## Using it

```bash
pip install -r tools/requirements.txt
python3 -I tools/validate.py        # schema + cross-reference checks
python3 -I tools/render_index.py    # regenerate docs/INDEX.md
```

From Python, `yaml.safe_load_all` any file and validate against `schema/<kind>.schema.json`.

## Confidence

`confidence: verified` means the value was read from the named edition of the document. `deck_only`
or `secondary` means it came from a briefing or summary and names what to check it against. See
[NOTICE.md](NOTICE.md) for provenance and posture, [LICENSE](LICENSE) (tools, MIT) and
[LICENSE-DATA](LICENSE-DATA) (records, CC BY 4.0).

## Contributing a record

1. Read the table in the standard itself. Cite clause, table and printed page; add `pdf_page` for
   the public PDF named in `standard.yaml`.
2. Keep the raw code. Add the unified reading. Paraphrase footnotes; never paste the standard's text.
3. Run the validator and the index renderer; commit both the record and the regenerated index.
4. Nothing proprietary, customer-specific or export-controlled.
