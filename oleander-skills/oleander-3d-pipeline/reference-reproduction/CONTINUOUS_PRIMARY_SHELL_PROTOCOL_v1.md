# OLEANDER 3D Pipeline — Continuous Primary Shell Protocol v1

Use this gate when the target's identity depends on one continuous body/form envelope.

## Rule
A semantic `PRIMARY_VOLUME` family does **not** imply a separate visible object. When the reference reads as one continuous shell, fender crowns, haunches, roof masses, shoulders and terminal volumes must be expressed as Source section/guide/continuity conditions of the same primary shell unless the real reference proves a separate part boundary.

`Semantic family ≠ separate mesh object`

## MUST CHECK
- Does the reference show a continuous highlight/silhouette across the proposed family boundary?
- Does a separate visible mesh create intersections, double highlights, floating shells or local bulges?
- Can the family be represented as a sparse section/guide/crown relation inside the current Source shell?
- Do SIDE / FRONT / REAR / 3Q remain consistent after the family is integrated?

## FORBIDDEN
- overlapping ellipsoids used as visible fender/haunch bodies;
- floating roof shells used to repair a wrong underlying greenhouse;
- a separate fascia slab used to hide a flat terminal cap;
- boolean or material seams that do not exist in the reference;
- calling additional object count "more detail" or "higher fidelity".

## Failure codes
- `FAIL_PRIMARY_VOLUME_FRAGMENTED`
- `FAIL_VISIBLE_SHELL_INTERSECTION`
- `REVISE_PRIMARY_VOLUME_INTEGRATION`
- `HOLD_SOURCE_REPRESENTATION_INSUFFICIENT`

## Evidence
- Source family table showing each semantic volume and its owning continuous Source shell;
- final evaluated projection receipt;
- controlled FRONT / REAR / SIDE / 3Q views;
- Source digest before/after;
- no hidden intermediate shell substituted for the final visible candidate.

## Transfer rule from the 992.2 benchmark
V12 proved that adding separate `FRONT_FENDER_CROWN`, `REAR_HAUNCH`, `ROOF_SHELL` and `REAR_FASCIA_VOLUME` objects can worsen fidelity even when the semantic decomposition is correct. V13 therefore keeps those semantic families but moves them into the cross-section and longitudinal guide logic of one visible primary shell.
