# OLEANDER Blender Surface System｜v1.18.0｜Evidence Adapter × Archetype Retirement × Project Binding

**Status:** `REVIEW / STACKED / NOT MERGED`

Base: `agent/blender-surface-system-v1-17-0`.

## Scope

v1.18.0 adds no new procedural source or Node Group. It changes how projects are allowed to call the existing Surface System.

`Evidence Source → Evidence Adapter → Claim Lane → Project Binding Resolver → Representation / Claim Permission`

## Claim lanes

- `EVIDENCE_BOUND` — source directly supports a project-specific claim.
- `VISUALIZATION_LOCKED` — existing digital implementation/profile may be reproduced for visual continuity only.
- `REFERENCE_ONLY` — generic learning archetype; never auto-bound.
- `BLOCKED` — project evidence/gate forbids or does not support activation.
- `UNKNOWN` — identity/process/parameter unresolved.

## Material Archetype Retirement

The legacy `material_process_archetypes.json` already declares itself `VISUALIZATION_STARTING_POINTS_NOT_MEASURED_FACTS`. v1.18.0 therefore retires all six generic archetypes from automatic project binding.

Key corrections:

- `PP_INJECTION_FINE_MATTE` → reference only globally; XJ01 can retain it only as `VISUALIZATION_LOCKED` implementation continuity.
- `TPE_OVERMOLD_SOFT_MATTE` → retired and split because legacy `TPE_PU` merges materially distinct families.
- `STEEL_POWDERCOAT_FINE_MATTE` → blocked for XJ01 while process remains unknown.
- `AL_BRUSHED_ANODIZED` → generic numeric values retired; project-specific Timer visualization profile has priority.
- `PC_FROSTED_TRANSLUCENT` → retired and split because legacy `PC_PMMA` merges distinct polymers.
- `ABS_PAINT_CLEARCOAT_HIGHGLOSS` → reference only until coating stack/process/sample evidence exists.

All eight legacy texture recipes are downgraded to `TECHNIQUE_REFERENCE_ONLY`.

## Real project binding results

### Baojiajie XJ01 / R02

- `PP_PRIMARY_FIELD` → `VISUALIZATION_LOCKED / ALLOW_REPRESENTATION_ONLY`.
- `IRON_VISIBLE` powder-coat archetype → `BLOCKED / DENY` because process remains unknown.
- `PU_CONTACT` TPE/PU merged archetype → `BLOCKED / DENY` because exact family/process is unresolved.

This preserves the existing controlled render implementation without opening Finish/Texture as evidence-backed design variables.

### Timer Light Basin / Hero-CMF

Housing, Knob and Diffuser may reuse their **project-specific** locked visualization profiles. Generic material archetype numeric values are not inherited.

## CI scope

The v1.18.0 workflow validates governance/binding behavior only. Blender 5.2 Node Group runtime and asset persistence remain inherited from the already verified v1.17.0 layer; no new Blender binary/API behavior is introduced here.

## Governance boundary

Render implementation ≠ evidence claim. Representation continuity does not establish measured CMF, process, durability, optical, thermal, manufacturing or user truth.
