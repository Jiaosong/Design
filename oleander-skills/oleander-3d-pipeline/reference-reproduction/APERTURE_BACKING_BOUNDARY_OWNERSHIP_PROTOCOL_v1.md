# OLEANDER 3D Reference Reproduction — Aperture Backing & Shared Boundary Ownership Protocol v1

Use this protocol after primary mass/silhouette work when the reproduced object contains glazing, openings, recessed lamps, vents or other apertures.

A correct outer silhouette can still look structurally false when the aperture system has no interior backing or when adjacent patches do not share the same physical boundary.

`Opening + glass ≠ complete aperture`

`Coincident-looking patches ≠ shared boundary`

`Profile RMSE improvement ≠ interface topology PASS`

## 1. Aperture layer stack

For each aperture classify and persist these layers:
1. `HOST_SURFACE` — the exterior body/skin that owns the opening;
2. `OPENING_BOUNDARY` — the actual cut/termination boundary;
3. `INTERFACE_SURFACE` — frame, reveal, pillar, seal land, roof rail, lamp pocket or equivalent transition;
4. `INFILL` — glass/lens/grille/mesh when present;
5. `BACKING_OR_VOID` — interior trim, dark cavity, cabin volume, lamp backing or explicitly empty space;
6. `SECONDARY_DETAIL` — seals, clips, hardware, trim.

### FAIL
- `FAIL_APERTURE_BACKING_MISSING` when a transparent/open aperture exposes unrelated exterior geometry behind it;
- `FAIL_APERTURE_LAYER_COLLAPSED` when interface/infill/backing are represented as one visual patch with no declared boundary semantics.

---

## 2. Shared boundary ownership

Every visible interface boundary must have exactly one canonical geometric definition.

Adjacent patches may be separate Blender objects, but the common edge must be generated from the same Source curve / section / equation / vertex set or be verified coincident after evaluation.

Examples:
- windshield ↔ A-pillar;
- A-pillar ↔ roof rail;
- roof rail ↔ roof outer panel;
- rear glass ↔ C-pillar/sail;
- sail ↔ rear quarter;
- cowl ↔ hood/body;
- lamp lens ↔ lamp pocket.

### MUST CHECK
- one boundary owner ID is persisted;
- adjacent consumers reference the same owner or emit a deterministic correspondence table;
- no independently guessed endpoints at the same visual junction;
- evaluated gap/overlap is measured where practical;
- surface normal/width changes do not create a false floating strip or spike.

### FAIL
- `FAIL_SHARED_BOUNDARY_DIVERGENCE`
- `REJECT_OVERLAPPING_INTERFACE_PATCHES`
- `REJECT_FLOATING_INTERFACE_STRIP`

---

## 3. Backing/occlusion is geometry, not a render trick

Transparent glazing must not reveal the opposite exterior skin, hood, deck or unrelated body panel through the cabin/opening.

Allowed backing evidence:
- simplified interior volume;
- dashboard / rear bulkhead proxy;
- dark cavity/pocket geometry;
- explicit void where the real system is open.

The backing may be `DERIVED_EXECUTION_NOT_AUTHORITY`, but must be spatially plausible and excluded from outer-silhouette authority unless the reference proves it is externally visible.

### FORBIDDEN
- compositor masks used to hide missing interior geometry;
- opaque glass used solely to conceal an incorrect aperture stack;
- a background card positioned to fake cabin depth;
- counting backing proxies as exterior Source Authority.

### FAIL
`REVISE_BACKING_OCCLUSION_ARCHITECTURE`.

---

## 4. Interface closure before detail

Before adding seals, trim, wipers, handles, lamps or CMF, inspect the major aperture loop in SIDE / FRONT / REAR / 3Q:

`cowl → A-pillar → roof rail → C-pillar/sail → rear deck/quarter → belt → cowl`

The loop must read as one continuous physical architecture even when composed from multiple patches.

### MUST CHECK
- no visible open roof-to-C-pillar gap;
- no sail/quarter spike caused by independently terminated patches;
- no roof rail floating above or beside the roof host edge;
- no exterior panel visible through windshield/rear glass unless the real view permits it;
- B-pillar and belt surfaces terminate into owned boundaries instead of crossing glazing arbitrarily.

### FAIL
`REJECT_APERTURE_INTERFACE_LOOP_OPEN`.

---

## 5. Measurement relationship

Projection metrics remain useful but are insufficient for interface topology.

Therefore keep separate gates:
- `PROJECTED_PROFILE_GATE` — gross mass/width distribution;
- `BOUNDARY_CLOSURE_GATE` — ownership/coincidence/loop closure;
- `BACKING_OCCLUSION_GATE` — correct behind-glass/cavity read;
- `VISUAL_REFERENCE_GATE` — actual reference comparison;
- `DESIGN_QUALITY_GATE` — independent professional review.

A candidate may report `PROJECTED_PROFILE_GATE=PASS` while `BOUNDARY_CLOSURE_GATE=REJECT`.

That is a valid verification result and must not be promoted.

---

## 6. Evidence receipt

For a mature aperture system emit `APERTURE_INTERFACE_RECEIPT.json` with:
- aperture IDs;
- boundary owner IDs;
- host/interface/infill/backing objects;
- shared-boundary method;
- evaluated gap/overlap check when available;
- backing/occlusion objects and authority state;
- projected-profile state;
- boundary-closure state;
- visual review state;
- does-not-prove.

`Boundary Closure PASS` does not prove manufacturer patch layout, Class-A continuity, seal engineering, tooling or production glazing design.
