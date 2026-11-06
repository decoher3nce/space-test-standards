# Vocabulary requests from the GEVS-7000B encoding

Ids that would have been used had they existed. Each record that needed one names the substitute in
its `notes`. Vocabulary files were not edited.

- `test_type: cold_vibration` - Table 2.7-1 row "Cold Vibration Testing" (vibration of critical
  cryo-thermal components at operating temperature). Encoded as `random_vibration` with
  `variant: cold_vibration` in `matrices/table-2.7-1-cryogenic-requirements.yaml`. A distinct id
  would let a tailoring tool require it only for `cryogenic` hardware launched cold without
  conflating it with the ambient random vibration row.
- `test_type: temperature_pressure_humidity` (or a `variant` convention on `humidity`) - Table 2.7-1
  row "Temperature-Pressure-Humidity (Habitable Volumes)" and the 2.6.5.1 crewed-spaces case.
  Encoded as `humidity` with `variant: temperature_pressure_humidity_habitable`.
- `hardware_type: pressure_transducer` - the 2.6.3.2.2.1 hardware-specific cycling table gives
  pressure transducers their own row (8 cycles). Encoded with `hardware_types: [fluid_component,
  electronic]` in `rules/section-2.6.3.2.2.1-hardware-specific-cycles.yaml`; neither parent alone
  carries the right cycle count.
- `hardware_type: radiator_panel` (child of `thermal`) - same table, radiator panels row (4 cycles,
  IR imaging when heat pipes are embedded). Encoded as `thermal` with flag `heat_pipe`.
- `hardware_type: propulsion_valve` or `regulator` (children of `fluid_component`) - same table
  separates dynamic non-electronic components (regulators, fill and drain valves, 1 cycle) from
  dynamic electronic ones (solenoid valves, thrusters, 8 cycles). Encoded as `fluid_component` with
  flags `mechanism` and, for the electronic row, `has_eee_parts`.
