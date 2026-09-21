# Technical Drawing Execution Core v0.3

## 1. Authority classes

Every controlling value is one of:

- `AUTHORITY_VERIFIED`
- `LOCKED_DESIGN_VALUE`
- `DESIGN_RECOMMENDATION`
- `RECOMMENDED_RANGE`
- `REFERENCE_ONLY`
- `DERIVED_NOT_FIELD_MEASURED`
- `FIELD_VERIFY`
- `TBD`

A range is not a point estimate. A derived value is not a field measurement.

## 2. Native-output classes

- `PROJECT_NATIVE_CAD_BIM` — project authority remains outside this Skill when applicable.
- `ASCII_DXF_EDITABLE` — bounded 2D technical carrier.
- `SVG_EDITABLE` — bounded vector technical carrier.
- `PDF_DERIVATIVE` — presentation/review derivative only unless another owner grants authority.
- `NTS_TECHNICAL_EXPLANATION` — relation/detail carrier without formal plotted-scale closure.

## 3. Minimum round-trip

For generated DXF/SVG:

`SOURCE VALUES → WRITE NATIVE FILE → REOPEN PARSER → MEASURE REGISTERED GEOMETRY → COMPARE TO SOURCE → RECORD DIFFERENCE → REVIEW`.

For project-native external CAD/BIM:

`PROJECT AUTHORITY REF → PROJECT READBACK REF → DERIVED DRAWING REF → CROSS-VIEW CHECK → INDEPENDENT REVIEW`.

## 4. Dimension truth

A drawing may show:

- exact controlling values only when source authority supports them;
- min/max envelopes when the source provides ranges;
- `FIELD VERIFY` when remote closure is impossible;
- `NTS` when scale closure is absent.

Do not select a midpoint merely to make the graphic easier.

## 5. Closure

Machine readback may verify file structure, entity geometry, declared dimensions and cross-view consistency. It cannot self-award professional adequacy, engineering validity, statutory acceptance or field truth.
