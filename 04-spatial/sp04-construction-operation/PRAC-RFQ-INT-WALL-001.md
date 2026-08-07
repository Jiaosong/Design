# PRAC-RFQ-INT-WALL-001｜Demountable Wall Integrated RFQ + Safety Mock-up Gate

- Status: RFQ PACKAGE READY / B0 NOT RUN / B1 BLOCKED
- Layer: Spatial / SP04 Construction & Operation; Business / B03 Operation & Partnership
- Canonical source: Notion `PRAC-RFQ-INT-WALL-001`
- Verified: 2026-08-07

> This file stores the stable execution boundary only. Supplier quotations, project substrate facts, order batches, actual measurements and test results remain in Notion / project evidence. **Mock-up conditions are not project approval.**

## 1. Evidence boundary
No current project-level evidence establishes the real OLEANDER site substrate type, strength, thickness or reinforcement position. Therefore:

- **Project substrate:** `UNKNOWN / HOLD`.
- **Mock-up substrate:** a separately procured, traceable normal-weight structural concrete specimen.
- A successful mock-up may not be transferred to masonry, AAC, lightweight walls, unknown existing walls, different concrete, different panel geometry or a different order batch without renewed verification.

## 2. Locked mock-up route

```text
traceable normal-weight concrete specimen >=150 mm
→ Hilti HUS4-H 8×65 25/5/- | item #2293136
→ mock-up design input candidate hnom2 = 60 mm
→ Shengda Q100 track 100×35×0.6 mm
→ Shengda Q100 stud 100×45×0.6 mm
→ tested 90° metal adapter/backing + M5 mechanical clamping path
→ Button-fix Type 2
→ Fundermax F-Quality 12 mm mock-up panel
→ Safety Cord ×2 + additional Button ×2
```

`>=150 mm` is an OLEANDER mock-up procurement control, not a universal code minimum. Hilti technical data for the Ø8 / 60 mm nominal embedment condition lists a 100 mm minimum base-material thickness; the larger specimen condition is used only to provide practical mock-up margin. Actual concrete strength, cracking state, spacing, edge distances, hole depth, fixture thickness, loads and reinforcement conflicts still require the applicable current approval / IFU / PROFIS / engineer check before installation.

## 3. Exact anchor candidate

Mock-up-only anchor SKU:

- Hilti `HUS4-H 8×65 25/5/-`
- item `#2293136`
- drill diameter `8 mm`
- nominal embedment options in the referenced Hilti technical table: `40 mm / 60 mm`
- mock-up input candidate: `60 mm`

Status: **MOCK-UP SKU LOCKED / PROJECT NOT LOCKED**.

## 4. Shengda Q100 boundary

RFQ basis:

- Q100 vertical stud: `100×45×0.6 mm` nominal product-family basis;
- Q100 track: `100×35×0.6 mm`;
- bridging / through member: `38×12×1.0 mm` only when required by the returned mock-up engineering.

The existing `W02510311482` report supports the tested Q100 items against `GB/T 11981-2024`, but does not close the actual order producer, production date or batch. The RFQ must return exact SKU / length, actual producer/site, batch traceability, current evidence, packaging, MOQ, tax/freight, lead time and written price. No silent "equivalent" substitution.

## 5. Button-fix × 0.6 mm Q100 interface

Button-fix Type 2's Blue Button may be fixed with an M5 machine screw, but this does **not** prove that a 0.6 mm Q100 web can safely act as a direct M5 threaded substrate.

Required mock-up interface:

- fabricator-designed 90° metal adapter / backing;
- explicit M5 mechanical clamping path;
- returned material, thickness, dimensions, hole positions, screw length, washer / locking arrangement and drawing;
- separate B0 interface coupon before the full panel.

A generic self-tapping screw note is not acceptable evidence closure.

## 6. Panel-side Type 2 Fix

Mock-up panel basis:

- Fundermax `0755 / AP / F-Quality / 12 mm`;
- internal screening geometry: `600×1200×12 mm`;
- actual panel must be weighed and its processed hole pattern recorded before the full test.

The fabricator must return the concealed Type 2 Fix-to-compact-HPL method. Do not assume a timber screw is suitable for compact HPL. Make and inspect a separate panel-side coupon first.

## 7. Secondary retention

For the vertical mock-up panel:

- `Safety Cord for Type 2 ×2`;
- one at each top-corner Fix;
- `additional Button ×2` to capture the two cord loops.

The Safety Cord is a secondary retention path, not a substitute for the primary fixing. The additional Buttons require the same explicit Q100 adapter / M5 fastening logic.

## 8. One-system RFQ return set

The RFQ must be returned as one coordinated package:

1. **Concrete specimen:** producer, dimensions, thickness, strength evidence, production/batch traceability, reinforcement/embedded-item condition and delivery photos.
2. **Hilti:** item #2293136, quantity, current China availability, written price, pack, batch, current IFU/ETA reference, drill/installation tool and technical contact.
3. **Shengda Q100:** exact stud/track/bridging identity and lengths, actual producer/site, batch, current `GB/T 11981-2024` evidence, price, MOQ, tax/freight and lead time.
4. **Button-fix:** Type 2 identity / 262.94.024 reference, Fix/Button pack quantities, Safety Cords, additional Buttons, Fix Marker, China stock, price, lead time and spares.
5. **Interface fabrication:** Q100-to-Button adapter/backing, M5 mechanical route, panel-side concealed Fix route, drawings, material/finish, fabrication responsibility and price.
6. **Fundermax:** exact panel identity, source batch, mock-up cutting/drilling, actual weight, edge condition, price and spare panel.
7. **Mock-up/test service:** installation, first demount, repeated demounting, controlled primary-release scenario, Safety Cord retention, measurement/photos/video, rework and report.

## 9. Purchase hold points

Do not release the full mock-up order if any of these remains unresolved:

- concrete specimen lacks traceable strength/batch evidence;
- current item #2293136 supply / installation document cannot be confirmed;
- Q100 actual producer/batch is still blank;
- the Q100-to-Button interface is described only as a generic self-tapper;
- Fundermax-to-Fix concealed attachment has no coupon method;
- Safety Cords lack their additional Button fastening path;
- quotation excludes system fabrication, mock-up or test work.

## 10. Physical test sequence

### B0-A — substrate anchorage coupon

Real concrete specimen + Q100 track + HUS4 #2293136.

Record hole location, drill, nominal embedment, installation method/tool, anchor identity, local Q100 deformation and any slip/loosening. B0-A is not a substitute for project structural design.

### B0-B — connection coupons

Two interfaces are tested before a full panel:

1. Q100 + adapter/backing + M5 mechanical path + Type 2 Button.
2. Fundermax 12 mm + concealed Type 2 Fix attachment.

If either coupon fails or remains untraceable, **B1 stays blocked**.

### B1 — full safety panel

Internal screening basis only; these are **exercise/mock-up assumptions, not standard requirements or project acceptance limits**:

- one real `600×1200×12 mm` panel, weighed before installation;
- four Type 2 Fix/Button connections;
- two top Safety Cords + two additional Buttons;
- 20 normal demount/reinstall cycles with position, feel, noise, wear and loosening recorded;
- then a controlled primary-connection release using an independent backup safety tether and an exclusion zone;
- record displacement/swing, cord/extra-Button/adapter deformation, panel impact risk, edge damage and reinstatement.

Immediate FAIL conditions include uncontrolled panel drop, Safety Cord escape, additional Button or adapter detachment, panel fracture, or an uncontrolled personnel/equipment impact hazard.

A PASS applies only to the exact tested assembly and conditions.

## 11. Required evidence package

- integrated RFQ and supplier quote;
- product/order/batch photos;
- concrete strength/batch evidence;
- HUS4 installation record;
- Q100 label / actual producer / batch record;
- interface fabrication drawing;
- actual panel weight and machining record;
- repeated-demount log;
- controlled-release photos/video;
- deformation/damage record;
- PASS / FAIL / rework decision;
- G9 spare-parts and maintenance baseline.

## 12. Status transitions

- Current: `RFQ PACKAGE READY / MOCK-UP NOT RUN`.
- After evidenced B0 success: `INTERFACE COUPON PASSED / B1 READY`.
- After evidenced B1 execution: `PHYSICAL MOCK-UP EXECUTED`.
- Project approval remains separate and requires the real project substrate, panel dimensions, installation height, structural/fire/use conditions and order batches to be closed.

## References

- Canonical system: Notion `SYS-INT-WALL-DEMOUNTABLE-001`
- Canonical execution package: Notion `PRAC-RFQ-INT-WALL-001`
- Hilti China HUS4-H product family
- Hilti HUS4 technical data / item #2293136
- Shengda Q100 / report `W02510311482`
- Button-fix Type 2 / Safety Cord official documentation
- Fundermax Max Compact Interior documentation
