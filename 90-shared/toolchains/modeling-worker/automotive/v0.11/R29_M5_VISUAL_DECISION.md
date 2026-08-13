# Automotive v0.11｜R29 Human M5 Visual Decision

Status: `MACHINE PASS / HUMAN M5 REVISE WITH DIRECTION RETAINED / NOT FOR PROMOTION`

## Machine facts

Canonical run: `31618784504`

Artifact: `9150398943` / `oleander-automotive-v0-11-r29-31618784504`

Digest: `sha256:9821152df2e9a229c48c00a4e900f666e81092b44c195a3e6791871955495962`

R29 machine gate passed:
- one connected Source island;
- 2369 vertices / 2269 faces;
- 4 termination triangles / 2265 quads / 0 n-gons;
- no Source Boolean or SubD;
- 24 shared endpoint reuses;
- canonical `wheel_hp_contract.py` active and exact at 0.700 m OD;
- four apex records present;
- R29 programmed z/y monotonic checks passed;
- 9-view M5 matrix completed.

## Human M5 evidence

Compared against the HP-correct R25 baseline under the same 0.700 m wheel package:

### Retain
- R29 materially reduces the large cap-like local bulge visible in R25 arch detail.
- Hero / Strip / Grazing broad surfaces remain materially cleaner than the R28A-C patch family.
- The R25 topology family remains the preferred Source architecture.
- The shared wheel hard-point contract remains canonical and must not be reimplemented inside later revisions.

### Revise
- Front and rear arch detail still show a planar/shelf-like band above the wheel opening.
- The shelf is especially visible on the front wheel and remains readable in Hero/Grazing.
- This is a Source geometry relation, not a wheel-package artifact and not a normal/render failure.

## Root-cause refinement

R29 correctly removed B1/B2 overshoot, but its chosen vertical monotonic direction is wrong for the desired fender section.

Apex z records:
- Front: `CROWN 0.702 → B1 0.721 → B2 0.738 → INNER 0.755 m`
- Rear: `CROWN 0.722 → B1 0.734 → B2 0.744 → INNER 0.755 m`

Thus the outer shoulder-fed crown sits below the inner wheel-opening lip and the surface climbs inward. Human evidence reads this as a projecting shelf rather than a crown flowing down toward the opening.

## R30 gate

Next revision: `R30｜HP-Correct Shoulder-Fed Descending Crown`

Locked:
- R25 Source topology family;
- R25 rounded x-z opening target;
- canonical 0.700 m wheel HP contract;
- R29 y ordering;
- 24 endpoint reuse;
- R09/R11/R12/R18/R20 and all non-wheel Source geometry.

Reopen only:
- wheel-zone crown z-envelope and B1/B2 vertical interpolation.

R30 hypothesis:
- at wheel apex, crown should sit modestly above the inner opening lip;
- B1/B2 should descend monotonically from crown to inner lip;
- the crown rise is a designer-estimate validation parameter, not an engineering requirement;
- no topology expansion, Boolean, global SubD or n-gon is allowed.

M6/M7/M8 remain blocked until Human M5 PASS.
