# Automotive v0.11｜M9 Material Binding Gate

Status: `M9 OPEN / M5-M8 LOCKED / M10 BLOCKED`

## Purpose

M9 validates semantic material binding across passed Source, routing, secondary and linked-detail authorities without changing geometry.

M9 is **not** final CMF approval. Materials are neutral benchmark materials used to verify binding, hierarchy, selective rebinding and physically plausible diagnostic response.

## Locked authority

Primary Source hash:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

M6 routing assignments, M7 secondary mesh signatures and M8 linked prototype/instance structure remain locked.

M9 must not change:
- R29A Source coordinates/topology;
- M6 region IDs;
- M7 wheelhouse/glazing geometry;
- M8 prototype meshes or instance transforms;
- canonical 0.700 m wheel HP package.

## Neutral material registry

Required material IDs:
- `MAT-BODY-NEUTRAL-COAT`
- `MAT-GLASSHOUSE-BACKER`
- `MAT-GLAZING-NEUTRAL`
- `MAT-WHEELHOUSE-DARK-POLYMER`
- `MAT-TIRE-RUBBER`
- `MAT-WHEEL-DETAIL-METAL`

All values are `BENCHMARK_MATERIAL / NOT_FINAL_CMF`.

### Binding targets

`MAT-BODY-NEUTRAL-COAT`
- all R29A Source routing faces except `REG-GLASSHOUSE`.

`MAT-GLASSHOUSE-BACKER`
- R29A Source faces in `REG-GLASSHOUSE` only.
- exists as a visual backer below the separated M7 glazing shell; not production interior trim.

`MAT-GLAZING-NEUTRAL`
- `SEC-GLAZING-SHELL`.

`MAT-WHEELHOUSE-DARK-POLYMER`
- `SEC-WHEELHOUSE-FL / FR / RL / RR`.

`MAT-TIRE-RUBBER`
- canonical HP tire objects `WHEEL_FL_TIRE / FR / RL / RR_TIRE`.

`MAT-WHEEL-DETAIL-METAL`
- `PROTO-WHEEL-SPOKE` mesh datablock;
- `PROTO-WHEEL-RIM-RING` mesh datablock;
- linked instances inherit through the shared prototype mesh datablocks.

Objects without a registered semantic authority are not forcibly rebound in M9.

## Material intent

Material values should be physically plausible enough for Blender/Cycles diagnosis but remain generic:
- body: non-metallic coated neutral surface;
- glasshouse backer: dark neutral opaque substrate;
- glazing: transparent dielectric benchmark;
- wheelhouse: dark rough polymer-like benchmark;
- tire: high-roughness dark rubber-like benchmark;
- linked wheel detail: neutral metallic benchmark.

No supplier, resin grade, paint system, coating stack, glazing certification or production process is asserted.

## Machine gate

M9 machine PASS requires:
- Source hash before/after binding unchanged;
- Source topology unchanged;
- M7 secondary mesh signatures unchanged;
- M8 prototype mesh geometry signatures unchanged;
- M8 detail instance transforms and linked mesh relationships unchanged;
- M6 region assignments unchanged;
- canonical wheel HP package exact;
- exactly six required material IDs exist;
- every required semantic target resolves;
- Source face material coverage is exact with no unbound face;
- exactly 220 glasshouse Source faces receive the backer material;
- four wheelhouses receive the wheelhouse material;
- four canonical tire objects receive tire material;
- glazing shell receives glazing material;
- spoke/ring prototype mesh datablocks receive detail-metal material and all 44 linked instances inherit it;
- no primary or secondary object authority is altered by binding;
- material binding manifest includes affected-view policy;
- lightweight material diagnostic render matrix completes.

## Human M9 review

- no missing/pink material;
- body/glazing/wheelhouse/tire/detail hierarchy is readable;
- glazing shell remains subordinate and does not create severe double-surface artifacts;
- glasshouse backer does not leak onto body routing faces;
- wheelhouse material stays inside the exterior opening;
- tire material remains on exact HP tires only;
- linked spoke/ring materials are consistent across all wheels;
- Hero views do not imply final CMF approval;
- check occlusion, scale/proportion, framing/cropping and lighting sufficiency.

## Gate transition

If M9 PASS:
`M9 PASS → M10 MULTI-SCALE QA MAY OPEN`

No Notion/Drive canonical promotion and no PR merge are implied by M9 PASS.
