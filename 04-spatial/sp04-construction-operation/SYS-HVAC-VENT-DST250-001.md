# SYS-HVAC-VENT-DST250-001｜DST15-250P Balanced Ventilation Distribution System

- Status: SYSTEM HYPOTHESIS / SIMULATION-READY / NOT COMMISSIONED
- Layer: Spatial / SP04 Construction & Operation
- Canonical source: Notion `SYS-HVAC-VENT-DST250-001`
- Verified: 2026-08-07

> This file stores stable system logic only. Real project geometry, branch routes, installed products, measured airflow/noise and commissioning records remain in Notion / project evidence.

## Equipment fact boundary

Green Island Wind / Nedfon `DST15-250P`:

- high mode: supply 300 m³/h @ 225 Pa, exhaust 250 m³/h @ 100 Pa, 64 W, published noise 43 dB(A);
- low mode: supply 200 m³/h @ 190 Pa, exhaust 180 m³/h @ 70 Pa, 50 W, published noise 38 dB(A).

These are equipment parameters, not installed working points.

## System chain

`outdoor intake → weather/insect interface → DST15-250P → flexible connection/service → supply silencer → supply main → branches/balancing dampers → terminals → rooms → exhaust terminals → branches/dampers → exhaust main → exhaust silencer → DST15-250P → outdoor exhaust`

Parallel requirements: duct insulation/condensation control, supports, access, electrical/control, penetrations/firestopping, cleaning and G9 maintenance.

## Simulation mode

All duct dimensions, room allocations, pressure losses and balancing results below are exercise assumptions. They must never be written as measured commissioning evidence.

### Simulated airflow allocation

Supply 300 m³/h:
- A 90
- B 80
- C 70
- D 60

Exhaust 250 m³/h:
- A 80
- B 70
- C 60
- D 40

Example duct geometry:
- supply main 200×150 mm → ~2.78 m/s at 300 m³/h;
- exhaust main 250×150 mm → ~1.85 m/s at 250 m³/h;
- typical branches 150×100 mm.

These are not construction-document sizes.

## Supply pressure-budget exercise

| Component | Nominal Pa | Adverse Pa |
|---|---:|---:|
| Outdoor intake | 18 | 25 |
| Flexible connection | 8 | 12 |
| Silencer | 22 | 32 |
| Main duct | 32 | 40 |
| Fittings | 26 | 36 |
| Balancing damper | 18 | 24 |
| Terminal | 15 | 20 |
| **Total** | **139** | **189** |

Against the published 225 Pa high-mode supply static-pressure value:
- nominal proxy reserve = 86 Pa;
- adverse proxy reserve = 36 Pa.

If crushed flexible duct, excessive throttling or higher-than-assumed silencer/terminal loss pushes the external network beyond the fan capability, total airflow should be expected to fall.

## Exhaust-side constraint

The published high-mode exhaust static pressure is only 100 Pa.

Initial simulation:

`terminal 10 + branches 18 + main 22 + fittings 18 + damper 10 + silencer 15 + outlet 15 = 108 Pa`

Result: **SIM-FAIL**.

Revised simulation uses a larger/lower-loss exhaust route and targets:

`12 + 14 + 16 + 12 + 8 + 8 + 5 = 75 Pa`

Proxy reserve ≈ 25 Pa.

Design rule: do not mirror the supply network onto the exhaust network. The lower-static exhaust side should drive low-resistance routing, terminal selection and fitting count.

## Simulated balancing set

Internal training proxy only: ±10% per terminal is used to flag SIM-PASS / SIM-REWORK. It is not a project specification or code limit.

### Supply
| Space | Design | Simulated | Deviation |
|---|---:|---:|---:|
| A | 90 | 86 | -4.4% |
| B | 80 | 83 | +3.8% |
| C | 70 | 68 | -2.9% |
| D | 60 | 58 | -3.3% |

Total simulated supply = 295 m³/h (-1.7%).

### Exhaust
| Space | Design | Simulated | Deviation |
|---|---:|---:|---:|
| A | 80 | 78 | -2.5% |
| B | 70 | 68 | -2.9% |
| C | 60 | 62 | +3.3% |
| D | 40 | 39 | -2.5% |

Total simulated exhaust = 247 m³/h (-1.2%).

The resulting 48 m³/h supply-exhaust difference does **not** prove room positive pressure; infiltration, doors, other exhaust systems and envelope leakage are not modeled.

## Noise boundary

The manufacturer's 43 dB(A) high-mode value is not arithmetically added to terminal noise.

An internal exercise target of ≤35 dB(A) may be used only to compare alternative duct velocity / silencer / damper strategies. Any such number is simulated until measured in the real room.

## Failure-seeking checks

- external pressure loss exceeds available fan static;
- exhaust path runs out of pressure margin before supply;
- near branches over-supply and remote branches under-supply;
- throttling noise from balancing dampers;
- condensation at insulation discontinuities;
- filter/duct fouling causes long-term airflow drift;
- maintenance changes damper positions and destroys the commissioning baseline.

## Product-selection gate

Before specific duct/terminal products are locked, require:

- duct material/thickness/flange/insulation system;
- silencer size, airflow, pressure drop and insertion-loss data;
- balancing-damper size, pressure drop and lockable setting;
- terminal effective area, pressure drop, throw/spread and noise data;
- intake/exhaust weather and insect protection with pressure-drop data;
- cleaning access, serviceability and spare-part route.

## Status ceiling

- DST15-250P identity/high-low parameters: FACT / CLOSED.
- external duct network: SIMULATED / NOT COMMISSIONED.
- first exhaust design: SIM-FAIL; revised low-loss target: 75 Pa.
- duct/damper/silencer/terminal specific products: OPEN.
- real pressure/airflow/noise: UNKNOWN.
- highest permitted status without field work: `DESIGN-READY FOR PRODUCT SELECTION / FUTURE COMMISSIONING`.
