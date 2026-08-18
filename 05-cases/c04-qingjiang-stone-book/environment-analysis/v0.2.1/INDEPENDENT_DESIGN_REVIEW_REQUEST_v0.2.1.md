# C04｜Independent OLEANDER Design Review Request｜GIS v0.2.1

Status: `REVIEW REQUESTED / VERDICT PENDING`  
Producer verdict: **NONE**  
Machine QC: `PASS`  
Persistence: `PASS`  
Professional Design: `PENDING`

## Artifact under review

`C04_GIS_REDO_SPLIT_v0.2.1.zip`  
Drive ID: `1n_Qyz_BN4VFP45nUHKrmRW4FrhF60s9_`  
SHA-256: `1c01ab71486183348e96fc27f738e200592e6a88f3a46fc8b77cc86913c3d075`

## Applicable review gates

Use current `OLEANDER Artifact Review System v1.1`:

- Common Review / Evidence & Truth / Cross-file consistency / Final Artifact Review;
- `AR-S03 Data`;
- `AR-S05 GIS`;
- actual-preview Professional Design Gate.

Current owner map explicitly states `oleander-delivery-qc ≠ Design Review`; release QC may support evidence but may not issue the design-quality verdict.

## Required questions

### ENV-01｜DEM slope/aspect
- Does the first read clearly say `regional 21×21 sample grid`, rather than site survey?
- Are slope classes and sparse aspect arrows professionally legible?
- Is the Qingjiang context line subordinate to the analytical claim?

### ENV-02｜potential drainage
- Does the sampled-cell graphic avoid implying a calibrated stream/drainage network?
- Is `D8 potential convergence` visibly distinct from hydraulic design?
- Does the visual genuinely inform later R06/R13/Physical verification priorities?

### ENV-03｜land-cover HOLD
- Does HOLD read immediately?
- Does the page explain why no analytical land-cover figure is shown without feeling like a broken placeholder?
- Is the source/next-action evidence useful enough to keep in Process/Technical reading?

### ENV-04｜water-history HOLD
- Same HOLD test as ENV-03.
- Does the page prevent the viewer from reading OSM river geometry as historical water extent?

### ENV-05｜solar scenarios
- Do three small multiples communicate scenario comparison more clearly than the former averaged heatmap?
- Is `relative terrain incidence` visually prior to any false microclimate certainty?

### ENV-06｜operations conflict
- Verify `ROUTE-03` topology is preserved without presentation-driven re-authoring.
- Does the current-operation layer distinguish `reported role` from `exact anchor open`?
- Does the graphic lead to actionable Return/service design consequences rather than a generic operations list?

## Whole-set design gate

Evaluate:
1. first-read claim;
2. professional cartographic completeness at the stated evidence level;
3. C04 specificity;
4. `Evidence → Interpretation → Design Impact`;
5. information hierarchy and text legibility;
6. consistency of truth-state wording;
7. cross-media consistency with `ROUTE-03`, CH02 and current C04 route/service logic;
8. portfolio value;
9. deletion test;
10. whether any map should be `KEEP / REVISE / REJECT / HOLD`.

Every verdict must name one primary root cause. Machine/persistence success may not override visual or evidence defects.