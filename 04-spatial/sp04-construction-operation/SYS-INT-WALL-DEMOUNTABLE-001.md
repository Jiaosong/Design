# SYS-INT-WALL-DEMOUNTABLE-001｜Demountable Compact Interior Wall System

- Status: SYSTEM RFQ READY / mock-up blocked by subframe + substrate fastening
- Layer: Spatial / SP04 Construction & Operation
- Canonical source: Notion `SYS-INT-WALL-DEMOUNTABLE-001`
- Verified: 2026-08-07

> This file stores the stable system boundary and validation logic only. Product status, supplier evidence, project dimensions, prices and test results remain in Notion / project records.

## Locked product inputs
- Fundermax Max Compact Interior / Black core F-Quality / 0755 Warm Grey Dark / AP / 2800×1300×12 mm.
- Button-fix Type 2 / Häfele 262.94.024 identity reference.

## System boundary
`building substrate → verified subframe → substrate fastener → Button-fix Type 2 → Fundermax 12 mm panel → joints/corners/termination → Button-fix Safety Cord for Type 2 + additional Button (candidate secondary retention) → demounting/maintenance/G9`

The following remain intentionally `UNKNOWN` until current evidence is returned:
- compliant exact subframe manufacturer/profile/thickness/factory;
- substrate fastener / anchor SKU and embedment;
- complete Chinese fire-performance evidence;
- installed system price.

Secondary retention is no longer an undefined concept: Button-fix Safety Cord for Type 2 is the first-choice **candidate**. It remains unvalidated at system level until the actual panel, additional Button fixing, substrate, screws and failure scenario are physically tested.

## Procurement closure｜2026-08-07
### Fundermax panel
The current Fundermax Delivery Programme identifies 0755 Warm Grey Dark / AP in Max Compact Interior Black core F-Quality and includes 2800×1300×12 mm in the product programme. Manufacturer documentation also exposes Max Compact Interior EPD, EN 438-7 performance documentation, F-Quality Type CGF CE DoP, EN 438-4 conformity and fire-classification files.

Factory status remains **PARTIAL**: manufacturer-level origin is Austria, but the exact Chinese order's production site/batch must be returned on quotation/order/label documentation. Fire classifications tied to riveted/screwed/adhesive assemblies are not automatically transferable to the Button-fix assembly.

### Button-fix Type 2
Button-fix confirms Type 2 is Made in the UK, 90° surface-mounted, minimum 10 mm panel thickness, and subject to screw/substrate matching and project testing for critical applications. Official downloads include instructions, Declaration of Performance, independent load tests and safety warnings.

Button-fix's official Where to Buy page lists **Sugatsune** as a China stockist, with China-wide sales/delivery, stockholding and no minimum order quantity. This closes the procurement route, not the project price.

### Secondary retention candidate
Button-fix officially specifies **Safety Cord for Type 2** where extra safety is required. For a vertical panel, install two Safety Cords, one to each top-corner Fix, and use an additional Button to capture each Safety Cord loop.

This closes the accessory identity only. It does **not** close project safety. The mock-up must verify the additional Button fixing, substrate/screw compatibility, panel swing/drop path, impact risk, retention after primary-fix release, repeated demounting wear and reinstatement.

### Subframe blocker
`GB/T 11981-2024 建筑用轻钢龙骨` was published 2024-10-26, became effective 2025-05-01 and fully replaced `GB/T 11981-2008`.

BNBM / Dragon partition light-gauge steel framing remains a candidate only because the manufacturer's current public product page still cites the 2008 edition. Saint-Gobain Gyproc's current China page confirms a continuing horizontal/vertical partition stud family and customizable length/thickness, but does not by itself close a specific project SKU, 2024-edition conformity evidence, production batch or written price.

Do not lock any subframe until the vendor returns exact profile/section/thickness, actual factory, current GB/T 11981-2024 test/conformity evidence, compatible fasteners and a written quotation.

### Substrate anchorage
This remains a system-safety blocker. Do not automatically use HST3 for every substrate. The actual wall base material and system load must determine the fastener, embedment, edge distance, spacing, installation method and inspection route.

## Written quotation boundary
Use one comparable functional unit: **completed wall m² + representative removable-panel detail**. The RFQ must separately return:
1. Fundermax board, fabrication/openings/edges, yield loss, packaging, freight/tax, batch and spare boards;
2. Button-fix Fix/Button, Safety Cords, additional Buttons, positioning tools, screw boundary, China lead time and spares;
3. subframe, leveling, substrate anchorage, corners/terminations and any additional safety hardware;
4. mock-up, first article, installation, demounting rehearsal, tests and protection;
5. warranty, maintenance, spare retention, quotation validity and substitution rules.

Board price + connector price + generic stud price is not a system quotation.

## Required mock-ups before status can advance
1. Visual/tolerance mock-up — real corner, demountable panel, fixed boundary and actual lighting.
2. Demounting/safety mock-up — actual panel weight, subframe, screws and Safety Cord arrangement. Deliberately release the primary connection and record retained position, swing/impact envelope, hardware deformation and reinstatement.
3. Maintenance scenario — panel removal, temporary storage, service work, reinstatement, cleaning and re-inspection.

## Handover / G9
Transfer panel IDs/locations, approved sample, exact panel batch, spare boards, Button-fix identity/batch, Safety Cord and additional Button records, spare Fix/Button stock, positioning tools, screw record, concealed subframe/anchor evidence and secondary-retention inspection instructions.

Track panel damage/contamination/warping/joint drift, connector looseness/noise/damage, Safety Cord/extra-Button condition, demounting cycles, service labour, subframe/anchor anomalies, spare use, replenishment lead time, repair cost, installed settlement cost and replacement cost.

## Gate status
- Fundermax product identity: CLOSED
- Fundermax order factory: OPEN
- Fundermax official documentation entry: CLOSED; China complete-system applicability OPEN
- Button-fix product/origin: CLOSED
- Button-fix China procurement route: CLOSED; written price OPEN
- Secondary-retention product identity: CANDIDATE LOCKED / system safety test OPEN
- Current light-gauge-steel standard source: CLOSED (`GB/T 11981-2024`)
- Exact compliant subframe: BLOCKED
- Substrate anchorage: OPEN
- Complete system written quotation: OPEN
- Mock-up: BLOCKED until subframe + substrate fastening are locked
- G9 structure: READY / actual evidence OPEN

## Sources
- https://www.fundermax.com/en/
- Fundermax Delivery Programme / Documentation
- https://button-fix.com/products/button-fix-type-2
- https://button-fix.com/where-to-buy
- https://www.bnbm.com.cn/category/product.html
- https://www.saint-gobain.com.cn/node/18846
- https://std.samr.gov.cn/gb/search/gbDetailed?id=25940C3CEF728A9AE06397BE0A0A525A

## Next engineering action
Obtain current GB/T 11981-2024 evidence and a written quote for an exact subframe profile, then lock substrate fastening and execute the physical mock-up including deliberate primary-fix release with Safety Cord retention.