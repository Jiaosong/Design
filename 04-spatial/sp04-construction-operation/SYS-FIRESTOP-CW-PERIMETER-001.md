# SYS-FIRESTOP-CW-PERIMETER-001｜Curtain-Wall Perimeter Fire Containment

- Status: SYSTEM HYPOTHESIS / SIMULATION-READY / NOT PROJECT APPROVED
- Layer: Spatial / SP04 Construction & Operation
- Canonical source: Notion `SYS-FIRESTOP-CW-PERIMETER-001`
- Verified: 2026-08-07

> This file stores stable system logic only. Project geometry, order batches, test reports, installed conditions and actual inspection results remain in Notion / project evidence.

## System boundary

`concrete slab edge → curtain-wall backpan/spandrel → Curtainrock (spandrel/insulation role) → perimeter void → ROCKWOOL RockSafe (fire-blocking fill role) → Hilti CFS-SP WB #430815 (surface firestop coating) → continuity / movement / curing / inspection → concealed acceptance → G9 maintenance`

Curtainrock and RockSafe are not treated as interchangeable. Curtainrock is retained for curtain-wall/spandrel insulation roles; RockSafe is the first China-official product-family candidate for the slab-edge / curtain-wall fire-blocking fill.

## Locked facts

### Hilti CFS-SP WB #430815
- China product identity: red, 19,000 ml, item #430815.
- Current public China price snapshot on 2026-08-07: CNY 10,069.39 per unit before final order tax/freight/enterprise discount.
- Application temperature: 4–40 °C.
- Approximate cure rate: 3 mm/day under the manufacturer's stated reference conditions.
- Product-level movement claim: up to 50%; this is not automatically a complete curtain-wall assembly movement approval.
- Hilti China identifies floor-slab/exterior-wall perimeter gaps as an application.

### ROCKWOOL
- Curtainrock: China product family for curtain-wall and perimeter-fire-containment applications; any “up to 2 hours” statement belongs to tested assemblies, not the board alone.
- RockSafe: China product family explicitly intended for curtain-wall fire blocking between floor slabs, curtain-wall units, or curtain wall and wall.

### Governance source
`GB/T 51410-2020` is treated as a complete-system boundary: firestopping is documented and accepted as an assembly, not as isolated material brands.

## Simulation mode

When real mock-up/project data is unavailable, three data states are kept separate:

- `F / FACT`: current standards, manufacturer pages, formal reports and current product/price identity.
- `H / SIMULATED`: exercise geometry, tolerances, process variation, movement cycles and cost proxies.
- `U / UNKNOWN`: real project geometry, actual producer/batch, installed quality, measured fire/movement performance.

Simulated values never overwrite unknown project facts.

## Simulation baseline S0.1

Exercise assumptions only, not project data or code requirements:

- slab thickness: 150 mm;
- perimeter gap: 75 mm;
- curtain-wall backpan: 1.2 mm galvanized steel;
- RockSafe fill compression scenario: 30% / 40% / 50%;
- CFS-SP WB proxy wet-film target: 3.0 mm;
- proxy overlap: at least 12.5 mm to each side;
- movement scenarios from the 75 mm initial gap: ±7.5 mm nominal, ±18.75 mm adverse, ±37.5 mm failure-seeking.

The 3.0 mm / 12.5 mm values are retained as a simulation QC proxy from Hilti curtain-wall guidance and must be reconfirmed against the current project-specific system document before construction use.

## Simulated 12-point QC set

| Point | Gap mm | Wet film mm | Left overlap mm | Right overlap mm | Simulation result |
|---|---:|---:|---:|---:|---|
| P01 | 74.4 | 3.06 | 13.6 | 13.2 | SIM-PASS |
| P02 | 76.9 | 3.14 | 13.4 | 13.5 | SIM-PASS |
| P03 | 73.4 | 3.27 | 13.3 | 13.2 | SIM-PASS |
| P04 | 76.1 | 2.78 | 13.9 | 13.3 | SIM-REWORK — wet film |
| P05 | 76.3 | 3.31 | 12.6 | 13.2 | SIM-PASS |
| P06 | 76.2 | 3.20 | 14.0 | 13.7 | SIM-PASS |
| P07 | 76.1 | 3.23 | 11.9 | 13.2 | SIM-REWORK — left overlap |
| P08 | 72.6 | 3.39 | 13.7 | 13.5 | SIM-PASS |
| P09 | 74.8 | 3.19 | 13.9 | 13.1 | SIM-PASS |
| P10 | 77.4 | 3.25 | 13.6 | 13.2 | SIM-PASS |
| P11 | 78.7 | 3.14 | 12.8 | 12.1 | SIM-REWORK — right overlap |
| P12 | 73.6 | 3.04 | 13.1 | 13.4 | SIM-PASS |

Interpretation: the training objective is not a “75% pass rate”. It is to demonstrate that average measurements can look acceptable while local thin-film and overlap defects still break the continuity of the fire/smoke path.

## Material-use proxy

For the simulation geometry `75 mm gap + 12.5 mm overlap each side + 3 mm wet film`:

- coated width = 100 mm;
- theoretical wet volume ≈ 0.30 L per linear metre;
- with a 10% exercise waste factor ≈ 0.33 L/m;
- 19 L theoretical coverage ≈ 57.6 m;
- using the current public retail snapshot, CFS-SP WB proxy material cost ≈ CNY 174.8/m.

This excludes mineral wool, Curtainrock, backpan, labour, equipment, access, tax/freight, testing, contractor overhead and project-specific waste.

## Failure-seeking checks

- mineral-wool voids / sagging;
- local under-thickness of firestop coating;
- broken coating overlap at geometry transitions;
- coating cracking or debonding under movement;
- curtain-wall backpan local failure;
- later maintenance cutting or displacing the firestop path.

## Hold points

1. Real curtain-wall geometry and movement criteria not frozen → no system approval.
2. Exact RockSafe / Curtainrock China SKU, factory/batch and complete assembly evidence not returned → OPEN.
3. CFS-SP WB batch/SDS/current system installation document not checked → no construction release.
4. Concealed closure must not occur before continuity, fill, coating, overlap, corners/transitions and labels are inspected.
5. Any repair must generate a new traceable record at the same location.

## Status ceiling

Without real assembly testing and project evidence, the highest permitted status is:

`SIMULATED / DESIGN-READY FOR FUTURE TEST`

Never upgrade simulated outcomes to `TESTED`, `VERIFIED`, `PASSED`, fire-rating approval or project acceptance.

## References

- Hilti China — CFS-SP WB #430815
- Hilti China — curtain-wall and facade firestopping
- ROCKWOOL China — Curtainrock
- ROCKWOOL China — RockSafe
- GB/T 51410-2020 system evidence page in Notion
