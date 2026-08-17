# OLEANDER Training — Material Identity Gate

Training ID: `OLEANDER-TRN-2026-08-17-MATERIAL-IDENTITY`

## Why this round

Recent OLEANDER spatial/model reviews repeatedly exposed `gray-model feel`, weak material separation, and surfaces whose identity depended more on labels/color than on credible response. Existing `oleander-3d-pipeline` governed material naming, paths, exchange and manifests, but did not contain an independent visual Material Identity Gate.

This round reuses the existing 3D pipeline and the glTF 2.0 metallic-roughness parameter categories. It does not create a parallel CMF framework.

## Practice

Three calibration passes were made under one representational lighting assumption:

- `v1 REJECT`: three named materials differ mostly by hue; highlight width, texture scale and edge behavior are almost identical.
- `v2 REVISE`: response channels are differentiated, but limestone becomes a regular decorative pattern, weathering steel uses obvious repeated spots, and timber grain repeats too mechanically.
- `v3 KEEP FOR TRAINING`: reduce patterning into lower-amplitude surface variation, separate broad/tight response, preserve material-specific texture direction/scale, and distinguish edge behavior.

A grayscale derivative was also generated locally to check whether the three material families remain visually distinct after hue is removed.

## Design Crit

### First visual gate

`PASS v3` — stone, steel and timber no longer read as the same gray-model surface with different labels.

### Composition / proportion / typography

`PASS` — equal specimen framing keeps material behavior as the controlled variable; labels are secondary to the visual sample.

### Material realism

`KEEP within training boundary` — v3 establishes a more credible material hierarchy, but it is a deterministic SVG calibration diagram, not a PBR render or measured sample.

### Scale / node / interaction

`N/A` for this calibration. Texture-scale plausibility is tested conceptually, not against a field-measured object.

### Professional finish

`KEEP FOR TRAINING`, not MAIN project evidence.

## Failure knowledge

1. Material names and texture slots do not prove material identity.
2. Hue cannot carry the whole distinction; orange alone is not weathering steel and brown alone is not timber.
3. A procedural texture can be technically valid yet visually wrong when its repeat/pattern becomes stronger than the material itself.
4. Microtexture must be judged at intended camera distance; a close-up detail cannot rescue a distant hero material.
5. Edge response is part of material reading and must agree with fabrication/weathering logic.
6. Render success and material realism remain independent gates.

## Transfer

Applicable to spatial renders, product CMF, Blender/KeyShot/D5/Unreal material libraries, exploded/axon renders, hero images, and reusable PBR assets.

Not a substitute for real sample approval, measured reflectance, slip/fire/UV/corrosion performance, structural suitability, fabrication quality, or field installation evidence.
