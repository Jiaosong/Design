# OLEANDER 3D Pipeline — Aperture Interface Surface Protocol v1

An aperture can be geometrically open and still look wrong if its interface is represented only by curves/tubes.

Core rule:

`Opening + glass ≠ complete aperture architecture`

For large identity-bearing apertures, the host transition must include surface interfaces where the reference contains real surface width/volume.

## Typical automotive greenhouse chain
`hood/cowl patch → windshield → A-pillar surface → roof panel → roof-rail surface → C-pillar/sail surface → backlight → rear-deck/quarter patch`

Side glazing additionally requires:
- belt/sill interface;
- B-pillar surface;
- door glass and quarter glass ownership;
- shared or hidden-overlap boundaries that do not create double highlights.

## FORBIDDEN
- using bevelled curves/tubes as the final visible A/C-pillar when the reference shows a broad surface;
- windshield floating between hood and roof;
- rear glass floating above the quarter/deck;
- roof panel extending beyond its actual windshield/backlight header boundaries;
- body/roof/glass interfaces judged only by orthographic width ratios.

## MUST CHECK
- 3/4 view continuity across cowl→A-pillar→roof and roof→C-pillar→quarter;
- surface width/taper, not only centerline position;
- no body behind glazing;
- no gaps visible through the interface;
- FRONT/REAR/SIDE projections remain within previously locked gates.

## Failure codes
- `FAIL_APERTURE_INTERFACE_IS_CURVE_ONLY`
- `FAIL_COWL_WINDSHIELD_GAP`
- `FAIL_ROOF_BACKLIGHT_GAP`
- `FAIL_PILLAR_SURFACE_WIDTH`
- `REVISE_GREENHOUSE_INTERFACE_SURFACE`

V20 transfer: the macro silhouette and lower envelope screened within tolerance, yet the 3/4 result remained clearly non-992 because the greenhouse was assembled from glass panels plus thin curve-like frames. V21 freezes the passing macro families and replaces those interfaces with surface patches.
