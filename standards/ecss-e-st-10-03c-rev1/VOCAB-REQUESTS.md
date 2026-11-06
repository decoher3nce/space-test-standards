# Vocabulary requests from ECSS-E-ST-10-03C Rev.1 encoding

Verified equipment-type key (printed under Tables 5-1, 5-3 and 5-5, pdf pages 47, 56, 64):

| Letter | ECSS type | Unified `hardware_type` applied |
|---|---|---|
| a | Electronic, electrical and RF equipment | `electronic` |
| b | Antenna | `antenna` |
| c | Battery | `battery` |
| d | Valve | `fluid_component` (closest; valve is listed in its name) |
| e | Fluid or propulsion equipment | `fluid_component` (collision with d, see below) |
| f | Pressure vessel | `pressure_vessel` |
| g | Thruster | `thruster` |
| h | Thermal equipment | `thermal` |
| i | Optical equipment | `optical` |
| j | Mechanism | `mechanism` |
| k | Solar array | `solar_array` |
| l | Solar panel | `solar_panel` |

## hardware_type

- **Letter e (fluid or propulsion equipment) has no distinct unified home.** Both d (valve) and
  e map to `fluid_component`, whose alias now reads `["d", "e"]`. An applicability matrix needs
  one column id per column, so the equipment matrices carry column d under `fluid_component` and
  record column e in the matrix `notes` (it equals column d in every row except Life, where d is R
  and e is X, and Burn-in, where d is X and e is "-"). Request: add an id such as
  `propulsion_equipment` (name "Fluid or propulsion equipment", parent `fluid_component`) so the
  e column can be encoded as its own column; or add `valve` (parent `fluid_component`) and give
  e the parent id.
- **`structure` has no ECSS equipment type.** The previous guess mapped it to j (which is
  Mechanism). The ECSS alias was removed; structure is tested as a subsystem or at element level
  in this standard (Table 6-x static load, sine burst, modal survey).

## test_type (closest id used, with a `variant` where two rows share an id)

- "Thermal test at mission pressure" (5.5.4.3, 6.5.4.3): temperature cycling at the mission
  (non-vacuum) pressure, for example Mars or Venus atmosphere. Encoded as `thermal_cycle`
  ("thermal cycling at ambient pressure"). The standard says explicitly that room-pressure
  thermal cycling in the US sense is not part of it, so a dedicated id
  (`thermal_mission_pressure`) would be more accurate.
- "Multipactor" (5.5.5.5) and "Corona and arc discharge" (5.5.5.6) both map to `discharge`;
  encoded as variants `multipaction` and `corona_arc`.
- "Micro-vibration generated environment" (5.5.2.7) encoded as `microvibration_emission`.
- Element-level tests with no unified id, encoded as variants of the closest id:
  - "Mission (MT)" 6.5.1.4 -> `functional_performance` variant `mission_test` (request `mission_test`)
  - "Functional (FFT/RFT)" 6.5.1.2 -> `functional_performance` variant `functional`
  - "Performances (PT)" 6.5.1.3 -> `functional_performance` variant `performance`
  - "Polarity" 6.5.1.5 -> `functional_performance` variant `polarity` (request `polarity`)
  - "Launcher interface" 6.5.1.6 (fit check, clamp-band release, electrical and data interfaces)
    -> `mechanical_function` variant `launcher_interface` (request `launcher_interface`)
  - "Transient" 6.5.2.5 (time-domain launch transient on a shaker, can replace sine with modal
    survey) -> `sine_vibration` variant `transient` (request `transient`)
  - "Electromagnetic auto-compatibility" 6.5.5.3 -> `emc` variant `auto_compatibility`
  - "Aero-thermodynamics" 6.5.6.1 (wind-tunnel tests on scaled models for atmospheric entry)
    -> `mission_specific` variant `aero_thermodynamics` (request `aero_thermodynamic`)
  - "Vibroacoustic emission" 6.5.7.1 (noise emitted by disturbance sources, crewed elements)
    -> `audible_noise` variant `vibroacoustic_emission` (request `vibroacoustic_emission`)
  - "HFE" 6.5.7.2 (human factors engineering, crewed) -> `mission_specific` variant `hfe`
    (request `human_factors`)
  - "Toxic off gassing" 6.5.7.3 (crewed cabin air) -> `bakeout` variant `toxic_offgassing`
    (request `toxic_offgassing`)

## requirement_code

- Element tables 6-1, 6-3, 6-5 define X as "to be decided on the basis of design features,
  required lifetime, sensitivity to environmental exposure, and expected usage" and R as
  "Mandatory"; the equipment tables define X as "to be decided by the customer". Both X readings
  are encoded as `customer_decision`; the distinction is kept in each matrix legend.
