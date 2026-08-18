# C04 Qingjiang Stone Seal v0.6 — Current Receipt

## Selected route
`B / STONE SEAL → Topology A / Strata Cut → Material Identity Stack v0.6`

## Current status
`PRODUCER CANDIDATE / MATERIAL-SKILL RERUN / PIXEL READBACK + REPAIRS COMPLETE / INDEPENDENT DESIGN REVIEW PENDING / NO_PROMOTION`

## Skill dependency
- Notion Brand System Candidate: `Material Identity Extension｜2026-08-18`
- GitHub reusable-skill Draft PR: `#242`
- Skill branch: `skills/story-board-material-identity-v0-1`
- Executable owner: `oleander-story-and-board`
- Production/readback owner: `oleander-delivery-qc`

## Material Identity Stack
1. Geometry Authority
2. Chromatic Field
3. Gradient / Tonal Modulation
4. Texture Scale
5. Finish / Edge Behaviour
6. Medium / Optical Decay

## Current source hierarchy
- Geometry authority: `QJ_STONE_SEAL_FLAT_MASTER_v0_6.svg`
- Gradient field: recoverable package `QJ_STONE_SEAL_GRADIENT_FIELD_v0_6.svg`
- Texture field: recoverable package `QJ_STONE_SEAL_TEXTURE_FIELD_v0_6.svg`
- Material master: recoverable package `QJ_STONE_SEAL_MATERIAL_MASTER_v0_6.svg`
- Small optical: `QJ_STONE_SEAL_OPTICAL_SMALL_v0_6.svg`
- Tokens: `STONE_SEAL_TOKENS_v0_6.json`

## Material rules
- Gradient: neighboring green/teal/value corridor; controlled axis and low-to-moderate contrast; `Gradient OFF` must preserve identity.
- Macro texture: low-frequency tonal fields + irregular mineral veins.
- Meso texture: directional abrasion in asymmetric density zones.
- Micro texture: top-dense → middle-medium → lower-sparse grain distribution.
- Edge: sparse local abrasion / sheen only; no full outline and no faux-antique dirt.
- River cut and strata apertures remain clean.
- Display >=96 px: full material stack.
- Standard 48–95 px: gradient or flat; texture reduced/removed.
- Small <=32 px: optical-flat; gradient/texture off.
- Print / emboss / 1-color: Flat Master; simulated digital stone texture does not prove or replace real process texture.

## Readback repairs
Producer readback rejected two rendering implementations before the current source was accepted as executable evidence:
1. compound `clipPath` caused slivers through strata/river apertures in CairoSVG;
2. SVG mask containment leaked material outside the symbol.

CURRENT implementation uses no clipPath and no SVG mask for material detail. Macro fields, mineral/abrasion lines, micro grain and edge wear are geometrically intersected with the authoritative Stone Seal polygon before SVG serialization. Embedded material assets use unique gradient namespaces.

## Recoverable package
- Google Drive file ID: `1rEYpE3PDWu-nZSXTACV35jwZYXkmJDAi`
- File: `C04_QINGJIANG_STONE_SEAL_v0_6.zip`
- Bytes: `17,588,583`
- Local ZIP SHA-256: `bdf1e6c2826c46dc2ecc648ce717b95188ab01adf4a6aadee06e505a34bfeedf`
- Drive raw readback reports the same byte count.
- Local ZIP integrity: no errors.

## Key source hashes
- Flat Master SHA-256: `6d218325b5983929a8abe7fe62692f444b5c186da79072140545788869098181`
- Gradient Field SHA-256: `9a86c1cda8dacf2061c3e10e6318f569a038e9551ae1bbeda0c64b47055be543`
- Texture Field SHA-256: `28cd1879f5485604f93e0de15561276843ea928751fc70a59cc28033fb8b7a0b`
- Material Master SHA-256: `1d8c28124cdd81e9ec75784193a57ca37bb45afff134b1ac3d325a6709501252`
- Optical Small SHA-256: `35f471ff8b1919ce0b762dde53ac85effa1ae828e6eb3f42ac9df4e5b7c04090`
- Contact Sheet SHA-256: `42e0ca1ce4780664ad1cc19a4eb9b34e26c6b32ba823ce69f7faef7b6dc38f37`

## Supersession
Stone Seal v0.5 is `SUPERSEDED PROVENANCE`. Its geometry/readback history is retained, but it no longer declares CURRENT.

## Does not prove
Independent Design PASS, operator approval, trademark clearance, physical stone/print/emboss performance, Field validation, production material specification, manufacturing approval or commercial release.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`.
