# Projected Profile → Section Inversion Protocol v1

Status: CURRENT CANDIDATE / reference-reproduction causal modeling method.

## INPUT
- external/calibrated projected width profile by normalized height;
- locked orthogonal silhouettes and hard points;
- last-known-good regression baselines;
- semantic Source family to be edited;
- confidence / perspective limitations of the reference image.

## MUST CHECK
1. Convert the profile only into the failed causal family; do not globally warp unrelated geometry.
2. Keep target provenance external to candidate measurement provenance.
3. If the same profile is used to generate geometry, its post-build RMSE is **constraint compliance**, not independent fidelity evidence.
4. Preserve independent orthogonal locks: SIDE silhouette, wheel/axle/hard points, aperture anchors, or other views not used by the inversion.
5. Clamp/noise-smooth perspective-derived profiles only with a persisted rule; never silently rewrite the target.
6. A profile is a projected envelope, not a manufacturer cross-section. Do not infer hidden local curvature or Class-A patch layout from it.
7. Use multi-view/3Q visual review after the inverse fit. A candidate can fit FRONT/REAR projected profiles and still have wrong longitudinal mass, reflection flow, or part topology.
8. If two reference constraints conflict because of perspective/studio bias, retain both with confidence labels and route to HOLD rather than forcing a false exact fit.

## ALLOWED
- derive transverse roof/cabin/shoulder envelope from projected width-vs-height samples;
- interpolate front↔rear section constraints longitudinally;
- preserve exact hard/aperture anchors while fitting the remaining section;
- treat the resulting metric as `MACHINE_CONSTRAINT_COMPLIANCE_PASS/FAIL`;
- keep a visually stronger LKG even when the inverse-fit experiment has lower profile RMSE.

## FORBIDDEN
- `generated from target + low RMSE = reference fidelity PASS`;
- using a studio perspective profile as engineering section dimensions;
- moving passing wheelbase / SIDE / lower-envelope families to satisfy one profile;
- replacing independent design review with inverse-fit math;
- claiming Class-A, manufacturer CAD, or production section geometry.

## EVIDENCE
Persist:
- reference profile file + source image hash/revision;
- inversion algorithm/version;
- edited Source family IDs;
- protected regression locks;
- raw and smoothed/inverted samples;
- final evaluated profile receipt;
- independent multi-view visual state.

## FAIL / HOLD
- `FAIL_PROFILE_INVERSION_SCOPE_POLLUTION`
- `FAIL_PROTECTED_GATE_REGRESSION`
- `HOLD_CONFLICTING_REFERENCE_PROJECTIONS`
- `HOLD_PROFILE_COMPLIANCE_NOT_FIDELITY`
- `REJECT_PROFILE_FIT_VISUAL_IDENTITY_FAIL`

## 992.2 benchmark
V27 proved connected topology but FRONT/REAR profile RMSE regressed because the transverse cabin envelope was still guessed. V28 uses the same-revision front/rear projected width profiles to derive the cabin Y/Z section while preserving V27 connected topology, SIDE/lower locks and calibrated aperture anchors. The resulting FRONT/REAR RMSE remains a generated-constraint compliance signal only; actual 3/4 reference fidelity stays HOLD pending visual review.
