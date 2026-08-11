# 2026-08-11｜XJ01 R02｜CMF Digital Direction × Surface v1.18 Evidence Binding

**Project:** 宝家洁 XJ01  
**Record status:** `PROJECT DECISION MIGRATED / SURFACE v1.18 BOUND / DIGITAL CMF ONLY`  
**Surface authority:** `OLEANDER Blender Surface System v1.18.0`  
**Legacy source:** PR #43 / Surface v1.15 integration — retained as historical calibration provenance, **not** current toolchain authority.

## 1｜Migration decision

PR #43 contains useful XJ01 R02 designer decisions, but its old shared-toolchain layer cannot be merged after v1.18.0 because it would reactivate generic material archetypes and set an obsolete v1.15 `ACTIVE.json` authority.

This record therefore migrates only the **project-specific decisions** and reclassifies every material/process/finish parameter under v1.18 claim lanes.

No v1.15 generic archetype or texture recipe is restored to automatic project binding.

## 2｜R02 decision chain retained

- `R02-00` — controlled digital baseline PASS in the historical calibration line.
- `R02-01` — Anchor lightness: **A_MID `#888C8F` selected**.
  - A_LIGHT `#B8BCC0`: structural spine collapsed too far into the PP field.
  - A_DEEP `#5B5F62`: rod/PP joint became too hard and tool-like.
- `R02-02A` — Field lightness: **F_MID `#AAA59D` selected** as the digital lightness corridor baseline.
- `R02-02B` — Hue: warm-neutral rejected; **Cool Blue** and **Teal** retained.
- `R02-02C` — Chroma: C05 under-signals the field; C20 begins to dominate first reading; **C12 retained**.

Current digital directions:

### Primary｜Mineral Cool Blue
- PP Primary Field `#92A9BA`
- PP Secondary `#E4E1D9`
- PP UI `#31516A`
- PU Contact `#65737A`
- Iron Visible / Anchor `#888C8F`
- Metal Hardware `#777A78`

### Alternate｜Clean Teal
- PP Primary Field `#8BACAA`
- PP UI `#245E60`
- PU Contact `#617270`

These are **designer digital calibration decisions**, not measured master colors, supplier approvals or user-preference findings.

## 3｜v1.18 evidence reinterpretation

### PP roles
`MAT_PP_PRIMARY_FIELD / MAT_PP_SECONDARY / MAT_PP_UI`

- project material fact: `PP`
- digital color direction: `VISUALIZATION_LOCKED`
- representation permission: `ALLOW_REPRESENTATION_ONLY`
- generic `PP_INJECTION_FINE_MATTE` autobind: **DENIED / REFERENCE_ONLY**
- generic Noise/Bump activation: **BLOCKED** without project finish/texture evidence
- old render-response signature `44a462645344c996872c5d3cf80b73e2d9a448d26d34356e8918fb60951642ac` is retained only as **legacy calibration provenance**, not as v1.18 physical-material evidence.

### PU contact
`MAT_PU_CONTACT`

- project material fact: `PU`
- digital color direction: `VISUALIZATION_LOCKED`
- legacy merged `TPE_PU` / overmold archetype: **BLOCKED / DENY**
- exact PU family, process, physical roughness and microtexture: **UNKNOWN / PENDING EVIDENCE**

### Iron visible
`MAT_IRON_VISIBLE`

- project material fact: iron tube
- digital Anchor color `#888C8F`: `VISUALIZATION_LOCKED`
- generic powder-coat activation: **BLOCKED / DENY**
- actual coating/process/texture: **UNKNOWN** until supplier/sample/process evidence exists

### Metal hardware
`MAT_METAL_HARDWARE`

- exact finish/process: **UNKNOWN**
- current `#777A78` appearance is representation-only and cannot establish plating/coating or physical roughness.

## 4｜Local-detail findings retained

- `D02_ROD_PP_JOINT`: digital hierarchy review PASS; supports A_MID selection only.
- `D03C_PP_SURFACE_GRAZE_LOW`: Beauty Macro readability HOLD; do not increase procedural amplitude merely to make grain visible.
- `D05B_PU_SURFACE_GRAZE`: Beauty Macro readability HOLD; improve reflection-design imaging before changing surface parameters.
- `D04_LOWER_UI_HARDWARE`: assembly hierarchy readable; hardware finish remains unknown.

A local/detail view may reveal rendering response but cannot silently change geometry, A/B lighting, texture amplitude or material/process claims.

## 5｜Physical sample closure path

The old lightweight sampling plan remains useful as a **future verification plan**, not as completed evidence:

- PP color plaques around retained Cool Blue / Teal corridors;
- restrained PP surface comparison without assigning supplier texture standard numbers before samples exist;
- real iron-tube coating coupon;
- real PU strip/reference;
- existing production hardware first, with separate finish development only if hierarchy requires it.

First physical review should test whole-product color hierarchy, PP–PU separation, iron visual weight, dirt/fingerprint visibility and UI surface intentionality.

## 6｜Hard boundary

This migration does **not** validate:

- physical colorimetry / gloss / roughness;
- powder coat, overmold, injection-finish or plating process;
- wet / dirty / aged behavior;
- manufacturing tolerance or supplier capability;
- user preference;
- mass-production approval.

`Render implementation ≠ evidence claim.`

## 7｜PR lineage

After this record is merged, PR #43 should be closed as:

`SUPERSEDED / PROJECT DECISIONS MIGRATED / LEGACY v1.15 TOOLCHAIN NOT MERGED`.
