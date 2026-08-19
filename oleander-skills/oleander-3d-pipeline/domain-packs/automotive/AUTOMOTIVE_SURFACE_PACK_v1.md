# Automotive Surface Pack v1

Status: CURRENT CANDIDATE / domain pack. This file does not replace the generic OLEANDER 3D Skill.

Purpose: provide automotive-specific Source families and stage gates only after the generic Representation Router selects `REFERENCE_RECONSTRUCTION + FEATURE_CURVE_STRUCTURED_SUBD` or an equivalent CAD/NURBS route.

## Automotive stage graph
`A0 Vehicle Identity Lock → A1 Package / Hard Points → A2 Identity Curve Stack → A3 Critical Sections → A4 Primary Patch Surface → A5 Greenhouse / Aperture Architecture → A6 End Forms / Fascia Integration → A7 Secondary Identity → A8 CMF / Presentation → Independent Multi-view Review`

## A0 Vehicle Identity Lock
Resolve maker/model/generation/body style/variant/revision before modeling. Styling cues from another trim/body shell may transfer only when explicitly allowed.

## A1 Package / Hard Points
Lock as evidence allows:
- overall length/width/height;
- wheelbase;
- track;
- axle centers;
- wheel/tire envelope;
- overhangs;
- ground/rocker datum;
- cabin/occupant/package anchors when available.

Hard-point compliance is not vehicle identity.

## A2 Identity Curve Stack
Typical Tier A automotive families:
- `SIDE_GESTURE`;
- `CENTER_SPINE` / hood-roof-deck crown;
- `FRONT_FENDER_CROWN_L/R`;
- `HOOD_VALLEY_L/R` when present;
- `SHOULDER_RAIL_L/R`;
- `BELT_RAIL_L/R`;
- `ROCKER_RAIL_L/R`;
- `GREENHOUSE_OUTER_BOUNDARY_L/R`;
- `A_PILLAR_RAIL` / `C_PILLAR_OR_SAIL_RAIL`;
- `REAR_HAUNCH_CROWN_L/R`;
- `NOSE_TERMINATION` / `TAIL_TERMINATION`.

Do not infer that every vehicle uses every family. The target determines the vocabulary.

## A3 Critical Sections
Prefer sections at real form transitions instead of uniformly spaced body rings. Candidate stations typically include:
- front extreme;
- lamp/fender center;
- front axle;
- cowl;
- A-pillar transition;
- roof apex;
- B/C or sail transition;
- rear axle;
- maximum rear haunch;
- rear deck/lamp relation;
- rear extreme.

Sections should explicitly encode hood-to-fender, shoulder-to-door, greenhouse-to-quarter and deck-to-haunch relationships.

## A4 Primary Patch Surface
Generate a structured quad cage or CAD/NURBS equivalent from the curve/section network. Fender crowns and rear haunches are primary surface conditions, not detachable blobs when the reference reads as one continuous body.

### MUST CHECK
- body wrap in front/rear 3/4;
- hood/fender cross-section;
- shoulder velocity;
- wheel-to-body stance;
- rear-engine/front-engine mass distribution as applicable;
- terminal plan curvature;
- Broad/Strip/Grazing/Zebra.

## A5 Greenhouse / Aperture Architecture
Windshield, side glazing and rear glass must be represented as owned boundaries/openings when they materially define identity.

Do not rely on:
- dark overlays over opaque body;
- polygon-center deletion;
- oversized overlapping pillar/glass patches;
- late Boolean cuts unsupported by frame/rail topology.

Required semantic capability IDs may include:
- `APERTURE_WINDSHIELD_BOUNDARY`;
- `APERTURE_SIDE_GLASS_BOUNDARY`;
- `APERTURE_REAR_GLASS_BOUNDARY`;
- `PILLAR_A_SURFACE`;
- `PILLAR_C_OR_SAIL_SURFACE`;
- `ROOF_RAIL_BOUNDARY`.

Diagnostics must request capability IDs rather than legacy object names.

## A6 End Forms / Fascia Integration
Nose and tail are not constant-X caps hidden by bumper meshes. Primary terminal curvature must exist in the body surface before intakes, lightbars, diffuser or garnish detail.

## A7 Secondary Identity
Lamps, intakes, fascia openings, mirrors, spoilers, handles, panel seams and wheel detail enter only after Tier A identity is visually coherent.

A lamp must be integrated as:
`host surface → recess/opening/interface → housing/lens → internal detail`, not a floating sphere/ellipsoid placed on the body.

## A8 CMF / Presentation
CMF cannot compensate for wrong mass, greenhouse or surface architecture. Clay and diagnostic rigs remain authoritative for surface criticism.

## Multi-view fitting and held-out review
Fit/calibration views and held-out review views must be declared separately. A suggested pattern:
- fit: SIDE + FRONT + REAR;
- held-out: FRONT_3Q + REAR_3Q + TOP_3Q.

A candidate generated from calibrated contours may pass target-compliance metrics while failing held-out vehicle identity.

## Automotive Representation Escalation
Trigger `STOP_PARAMETER_TUNING_REOPEN_REPRESENTATION` when:
- the car remains generic after repeated identity-curve edits;
- correcting side silhouette repeatedly breaks front/rear mass;
- greenhouse can only be approximated with overlays or destructive cuts;
- fender/haunch requires detached visible volumes to achieve shape;
- final 3/4 identity remains REJECT despite orthographic metric PASS.

## 992.2 benchmark application
For the current 911 Carrera 992.2 benchmark, V47 and earlier history remain provenance. A future candidate should start from locked hard points/reference evidence and the best comparable machine baselines, but the new Source should be a feature-aligned curve/section/patch representation. Do not create another wrapper runtime merely to tune V47 geometry. The current high-value rebuild priorities are hood valley + twin front fender crowns, greenhouse/A-C-pillar/backlight architecture, and rear haunch/deck/tail continuous mass.

## Does not prove
This pack does not prove Porsche/manufacturer CAD, Class-A surfacing, crash/aero/package engineering, homologation, tooling or manufacturing feasibility.
