# Automotive v0.11｜M10 Multi-Scale QA Decision

Status: `M10 PASS / MODELING WORKER v0.11 CANDIDATE AUTHORITY / DRAFT / NOT CANONICAL PROMOTION`

## Scope

M10 PASS closes the Modeling Contract validation chain for this generic automotive Modeling Worker benchmark.

It validates an editable modeling benchmark with semantic routing, secondary geometry, linked detail instances, neutral material binding and multi-scale QA.

It does **not** validate Class-A automotive surfacing, engineering CAD, crash/aero, manufacturing feasibility, production panel splits, homologation or final CMF.

## Canonical machine evidence

Run: `31623379139`

Artifact: `9152168778` / `oleander-automotive-v0-11-m10-31623379139`

Digest: `sha256:01b39f726ff943f9db2bca2d089cd197a3b23ce35a7ca277c2740cfe0448e6ac`

Primary Source hash before complete M10 assembly:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

Primary Source hash after complete M10 rendering:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

Source topology remains:
- 2909 vertices;
- 2793 faces;
- 4 triangles;
- 2789 quads;
- 0 n-gons.

Machine gate confirms:
- M6 region counts exact;
- M7 secondary signatures stable;
- M8 prototype signatures stable;
- M8 instance transforms stable;
- M8 linked mesh relationships stable;
- M9 six-material binding complete;
- canonical 0.700 m wheel package exact;
- 40 spoke instances retained;
- 4 rim-ring instances retained;
- Macro views = 3;
- Meso views = 3;
- Micro views = 2;
- total diagnostic views = 8;
- all views explicitly carry `engineering_authority=false`.

Execution receipt:
- Blender 5.2.0 LTS;
- Cycles diagnostic render;
- 640 × 640;
- 4 samples;
- 8 views;
- script elapsed ≈ 48.62 s.

## Human M10 review

### MACRO — PASS

Views:
- `M10_MACRO_SIDE`
- `M10_MACRO_HERO_FRONT`
- `M10_MACRO_HERO_REAR`

Findings:
- overall silhouette/package remains coherent under the corrected 0.700 m wheel hard point;
- R29A wheel crowns do not reintroduce the earlier R25 cap or R29 shelf as a dominant broad-volume event;
- wheel/detail/material layers remain subordinate to body proportion;
- front/rear Hero framing exposes rather than conceals the main body and wheel relations;
- Side view retains enough margin around front/rear terminations for package judgment.

No Macro issue requires reopening M5-M9.

### MESO — PASS

Views:
- `M10_MESO_FRONT_ARCH`
- `M10_MESO_REAR_ARCH`
- `M10_MESO_GLASSHOUSE`

Findings:
- front and rear wheelhouse liners remain inside the exterior fender/quarter openings;
- wheelhouse material stays secondary and does not become an exterior design feature;
- front/rear crown-to-opening relationships remain continuous enough for the passed Modeling Worker benchmark;
- separated glazing remains aligned with the M6 glasshouse routing region;
- glazing close view shows readable dielectric reflection without a severe exploded edge, duplicate-surface tear or backer leak onto the body;
- M9 neutral material binding does not hide a M5 surface failure.

No Meso issue requires reopening M5, M7 or M9.

### MICRO — PASS

Views:
- `M10_MICRO_FRONT_WHEEL`
- `M10_MICRO_REAR_WHEEL`

Findings:
- linked spoke/ring families remain centered on the canonical wheel package;
- front/rear instance scale and rotation remain consistent;
- spoke/ring radial envelopes remain visibly inside tire OD;
- tire/detail material binding remains consistent;
- no individual linked instance drift or broken prototype relationship is visible;
- near-side framing controls occlusion sufficiently for detail judgment.

No Micro issue requires reopening M8 or M9.

## Candidate Authority

The passed benchmark may now be labeled:

`MODELING_WORKER_v0.11_CANDIDATE_AUTHORITY`

Authority includes:
- R29A editable primary Source;
- M6 semantic routing metadata;
- M7 secondary wheelhouse/glazing benchmark;
- M8 linked wheel-detail instance benchmark;
- M9 neutral material binding benchmark;
- M10 multi-scale evidence matrix.

## Re-entry triggers

Reopen the smallest responsible gate if later work changes:
- hard points / package → M1-M2;
- section logic → M3;
- primary surface → M4-M5;
- routing/dependency IDs → M6;
- secondary geometry → M7;
- linked details / transforms → M8;
- material binding → M9;
- evidence scale / final benchmark coherence → M10.

## Promotion boundary

M10 PASS permits a separate Promote decision only.

It does not automatically:
- merge PR #85;
- sync to canonical Notion/Drive;
- replace `SYS-BLENDER-SURFACE` system authority;
- claim final CMF or engineering validity.
