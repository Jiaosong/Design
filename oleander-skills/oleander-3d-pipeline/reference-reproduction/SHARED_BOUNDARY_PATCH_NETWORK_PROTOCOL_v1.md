# OLEANDER 3D Pipeline — Shared-Boundary Patch Network Protocol v1

The V12→V15 benchmark exposed an important correction:

`Visual continuity ≠ one application object`

and

`Semantic family ≠ floating overlapping volume`.

A professional continuous exterior may be represented by multiple Source/Derived patches when their boundaries and transitions are intentional. The review object is the **visible patch network**, not the Blender object count.

## Allowed patch-network architecture
Examples for automotive/product reference reconstruction:
- lower body / hood / quarter primary shell;
- roof outer panel;
- windshield / side glass / backlight aperture infill;
- A/B/C pillar and roof-rail interface patches;
- bumper/fascia patches when the real reference contains an interface.

## MUST CHECK
1. Every visible patch has an explicit semantic owner and boundary.
2. Adjacent patches either:
   - share the same geometric boundary, or
   - overlap only in a hidden construction zone with no double highlight.
3. A visible gap/crease/seam must exist in the reference or be explicitly provisional.
4. No body surface may remain behind an aperture where the reference is open/glazed.
5. FRONT / REAR / SIDE / 3Q must be reviewed on the assembled visible patch network.
6. Surface diagnostics must detect boundary kinks/double highlights after macro projection passes.

## FORBIDDEN
- overlapping ellipsoid/floating roof objects used as visible body mass;
- treating one monolithic mesh as automatically more correct;
- destructive Boolean apertures on a relation model that has no supporting frame/pillar topology;
- body polygons left behind windows and hidden only by dark glass;
- object count used as fidelity evidence.

## Failure codes
- `FAIL_PATCH_BOUNDARY_UNOWNED`
- `FAIL_PATCH_VISIBLE_OVERLAP`
- `FAIL_APERTURE_BACKFACE_EXPOSED`
- `FAIL_PATCH_NETWORK_DISCONTINUITY`
- `HOLD_PATCH_NETWORK_REPRESENTATION_INSUFFICIENT`

## 992.2 transfer
V12 failed because semantic primary volumes were separate overlapping visible objects. V13/V14 corrected this toward one shell. V15 then proved the opposite extreme can also fail: large Boolean window cuts on a monolithic ring-based shell fragmented the greenhouse and exposed the weakness of the underlying representation. V16 therefore uses a lower-body primary shell + roof/interface patches with shared semantic boundaries and genuine glass apertures.
