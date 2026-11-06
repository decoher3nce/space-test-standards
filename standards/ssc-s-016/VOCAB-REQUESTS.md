# Vocabulary requests from the SSC-S-016 encoding

Ids that would let SSC-S-016 records be encoded more faithfully. Until they exist the records
use the closest existing id as described.

| Requested id | Vocabulary | Why | Workaround used |
|---|---|---|---|
| `bus` | hardware_type | NESC deck slide 56 (pdf 57) gives subsystem-level thermal vacuum applicability by Structure / Bus / Payload; a matrix needs a column id for "Bus" | Encoded as `rule` `ssc-s-016.rule.subsystem_payload_thermal_vacuum_applicability` with text values instead of an `applicability_matrix` |
| `hot_fire` | test_type | Unit table footnote 9: thruster thermal vacuum may be satisfied by hot-fire testing (a substitute test needs a target id) | Provision `ssc-s-016.provision.thruster_tv_hot_fire` names it in `constraints` only |
| alias `Climatic` on `humidity` for `ssc-s-016-2014` | test_type | Already present; no change needed, listed for completeness | - |
| alias `Pressure` on `proof_pressure` for `ssc-s-016-2014` | test_type | Deck overview slide 5 (pdf 6) prints the unit pressure test as "Pressure" and the subsystem/vehicle entry as "Leakage / Pressure" | Mapped to `proof_pressure` with a cell note |
