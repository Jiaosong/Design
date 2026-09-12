# OLEANDER 3D Pipeline — Front / Rear Projected Profile Calibration Protocol v1

SIDE silhouette can screen longitudinal proportion while still allowing a generic or incorrect FRONT/REAR identity. Existing-object reproduction therefore needs an independent cross-view projected-width profile when the target's body/cabin taper is identity-bearing.

## Reference representation
For a front or rear reference image:
1. isolate the main vehicle silhouette;
2. define detected silhouette bottom = 0 and top = 1;
3. sample full visible width at fixed normalized height fractions;
4. normalize each width by the detected maximum main-body width;
5. store source, file hash, revision, measurement method and transfer limitations.

Studio or near-perspective images may be used only as `SOURCE_GROUNDED_PROFILE_ESTIMATE`, never as manufacturer section dimensions.

## Candidate measurement
Measure the **final evaluated visible geometry union**, after modifiers/transforms, in locked world projection:
- FRONT / REAR: world `Y/Z` projection;
- SIDE: world `X/Z` projection.

Use projected triangle intersections rather than Source control values or sparse vertices alone.

## MUST CHECK
- reference and candidate provenance are independent;
- candidate members correspond to the visible body/roof/interface patch network, not hidden construction geometry;
- overall width and height normalization is derived from the final candidate projection;
- front and rear profiles are evaluated separately;
- SIDE gates that already passed remain locked unless the new cross-view correction proves a causal conflict.

## Failure routing
- upper profile too wide → greenhouse / roof / pillar cross-section;
- mid-height too narrow/wide → shoulder / haunch / upper-door cross-section;
- lower profile wrong → bumper / sill / wheel-aperture / diffuser family;
- SIDE remains correct but FRONT/REAR fails → reopen cross-section representation, not longitudinal envelope.

## Gate states
- `FRONT_PROFILE_SCREENING_PASS / FAIL`
- `REAR_PROFILE_SCREENING_PASS / FAIL`
- independent `REFERENCE_FIDELITY_REVIEW` remains required.

## 992.2 transfer
V20 passed SIDE upper/lower projection screens while actual FRONT/REAR/3Q still looked generic. V22 adds calibrated full-height front/rear projected-width profiles and freezes V20 SIDE envelope as the baseline.
