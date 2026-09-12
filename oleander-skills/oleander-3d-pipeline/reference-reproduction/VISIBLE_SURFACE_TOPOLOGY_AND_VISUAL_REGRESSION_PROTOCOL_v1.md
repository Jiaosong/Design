# Visible Surface Topology + Visual Regression Protocol v1

Status: CURRENT CANDIDATE / extracted from the 992.2 V23–V26 benchmark.

Purpose: prevent a 3D reference-reproduction workflow from mistaking better scalar/profile metrics for a better visible object when the surface topology, aperture architecture, or multi-view read has regressed.

## INPUT
- last-known-good or best-known per-gate baseline;
- current candidate;
- final evaluated geometry;
- reference imagery / measured targets;
- candidate edit scope;
- independent visual review requirement.

## MUST CHECK
1. **Numeric improvement does not override topology collapse.** A lower silhouette/profile RMSE is only a machine-screening result.
2. **Opaque exterior ownership must be explicit.** Semantic Source families may remain separate, but one visible continuous region must not be approximated by intersecting/floating meshes unless the reference proves a real seam.
3. **Apertures must terminate the opaque host.** Windshield / side glass / rear glass cannot be dark overlays on an opaque exterior shell.
4. **Shared boundary means one geometric boundary, not two nearby edges.** Adjacent visible regions must either share vertices/edge controls or have a documented physical seam/gap.
5. **Best-known baseline is per gate.** Do not revert from a stronger front gate to a weaker whole-revision baseline merely because another rear metric is better.
6. **Regression locks include topology-sensitive gates.** Preserve already-passing side silhouette, lower envelope, wheelbase, aperture ratios, and any validated surface/boundary state not in the edit scope.
7. **Promotion requires independent visual KEEP.** `PROMOTE_OVER_LKG` is invalid when visual review is `NOT_RUN`, `HOLD`, `REVISE`, or `REJECT`, or when the producer/owner is the sole reviewer.
8. **3/4 views are mandatory after orthographic screening.** Orthographic profile success cannot prove roof-to-quarter continuity, body wrap, section transition, or reflection coherence.
9. **Representation ceiling triggers source-vocabulary change.** If repeated parameter edits leave the object reading as assembled patches / generic form, stop tuning and change the causal representation.

## ALLOWED
- keep a numerically stronger experiment as SUPPORT while retaining a visually stronger LKG;
- use multiple semantic Source families feeding one evaluated visible shell;
- use a shared-boundary patch network when boundaries are actually shared and reflection continuity is separately reviewed;
- preserve derived interior/backing geometry to prevent exterior bleed through apertures;
- rebuild one causal layer while locking previously passing families.

## FORBIDDEN
- `RMSE improved → promote`;
- floating roof/sail/fender/quarter surfaces used to fake a continuous production shell;
- opaque body polygons behind glazing unless reference proves an opaque panel there;
- owner/self-review as the sole visual promotion authority;
- relaxing passing-gate baselines to make a new representation pass;
- adding trim/CMF/detail to hide broken primary topology.

## EVIDENCE
Minimum execution evidence:
- `REFERENCE_PROJECTION_RECEIPT.json` from final evaluated geometry;
- `REFERENCE_REGRESSION_PROMOTION_RECEIPT.json` using best-known per-gate baselines;
- `VISIBLE_SURFACE_TOPOLOGY_RECEIPT.json` listing opaque visible owners, forbidden floating visible families, aperture infill, and boundary method;
- six-view candidate including front/rear 3/4 and SIDE/FRONT/REAR orthographic;
- independent visual review receipt before any promotion.

## FAIL / HOLD
- `FAIL_VISIBLE_PATCH_TOPOLOGY_OVERLAP`
- `FAIL_OPAQUE_HOST_BEHIND_APERTURE`
- `FAIL_SHARED_BOUNDARY_NOT_SHARED`
- `REJECT_NUMERIC_IMPROVEMENT_VISUAL_REGRESSION`
- `HOLD_INDEPENDENT_VISUAL_KEEP_REQUIRED`
- `HOLD_RELATION_MODEL_INSUFFICIENT`

## 992.2 benchmark finding
V23 improved FRONT/REAR projected profiles without fixing the visual roof/C-pillar/quarter interface. V24 improved the front numeric profile further while rear topology visibly collapsed and rear RMSE regressed. V25 recovered the rear metric to the best-known range but still read as assembled pieces. Therefore V26 changes the representation: the opaque roof exists only between windshield and rear-glass headers, A/C pillars and rear-deck surround belong to one visible cabin surface object, and glazing occupies real open regions. This is still machine/evidence work; reference fidelity remains HOLD until independent multi-view visual review.
