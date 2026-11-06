# Provenance and posture

This repository holds **structured data derived from public aerospace test standards**: the
letter codes in their applicability matrices, the numeric test levels, durations, cycle counts
and margins in their tables, the tailoring provisions they themselves allow, and a clause or
table citation for every record. It does not reproduce the standards' prose.

| Standard | Edition encoded | Access | Posture |
|---|---|---|---|
| GSFC-STD-7000B (GEVS) | 2021-04-28 | US Government work, public domain | values and citations |
| ECSS-E-ST-10-03C Rev.1 | 2022-05-31 | free after registration at ecss.nl, copyright ECSS | values and citations only; notes paraphrased |
| SMC-S-016 / SSC-S-016 | 2014 public release; 2023 and 2026 revisions as reported in a public NESC Academy briefing | public release (DTIC, EverySpec); revision as Aerospace TR-2025-00777 | values and citations; deck-sourced values marked `confidence: deck_only` |
| 320-MAR-1001 Rev. D | Rev. D | US Government work | A/T/R codes and DID ids |

**What "verified" means.** `confidence: verified` on a record means the value was read from the
named edition of the document itself and the citation points at the table or clause. Anything
read from a secondary source (a briefing, a summary) is marked `deck_only` or `secondary` and
lists what to check it against. Treat unverified values as leads, not requirements.

**What this repository is not.** It is not a substitute for the standards. A program that
contracts to a standard must work from the controlled copy its customer cites. Check the
revision: GEVS 7000B, ECSS 10-03C Rev.1 and SSC-S-016 are all periodically revised, and the
records here name the edition they came from.

**Nothing proprietary.** Customer-specific levels, launch-vehicle user-guide data under NDA,
program environments and anything export-controlled do not belong here and will not be accepted.
