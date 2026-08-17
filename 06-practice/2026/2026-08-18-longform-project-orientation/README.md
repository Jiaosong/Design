# OLEANDER Training｜Long-form Project Orientation

Training ID: `OLEANDER-TRN-2026-08-18-LONGFORM-ORIENTATION`

## Project trigger

C04 current architecture keeps **20 chapter containers** while protecting **52 existing page identities** and allowing materially new N-series pages. The project explicitly requires rebuilding reading rhythm with pages inside chapters rather than compressing chapters into pages.

The design risk is therefore no longer only content compression. A complete long-form case can still fail when its navigation exposes the whole project structure on every page and competes with the current design claim.

## Existing-first

Reused `oleander-story-and-board`; no new framework was created.

External calibration:
- W3C WAI Breadcrumb Pattern: breadcrumb trails communicate hierarchical location; current page can be marked with `aria-current="page"`.
- W3C WAI Landmark Regions: multiple navigation landmarks should have distinct labels; landmark value falls as unnecessary regions multiply.
- W3C G65: breadcrumb trails should reflect the actual navigational path/location.

## Practice

Real editable outputs:
- `index.html` — responsive semantic HTML/CSS prototype.
- `orientation_specimen.svg` — editable mobile closed/open global-index proof.

Practice identity `CH09-P02` is **training-only**, not a final C04 Web PAGE-ID.

### v1 — REVISE

Desktop hierarchy improved, but the mobile rule hid the persistent chapter rail without preserving a global jump mechanism. Local continuity survived; global access disappeared.

### v2 — REVISE

Added an on-demand Project index, but the first static open-state proof visually replaced too much page context.

### v3 — KEEP FOR TRAINING

Global index opens as a contextual overlay; the current page remains perceptible behind it. Three navigation jobs are now visibly and semantically distinct:

1. `Breadcrumb` = orientation / where am I?
2. `Adjacent pages` = local continuity / what comes before or next?
3. `Project index` = global access / jump elsewhere on demand.

Static semantic checks confirm distinct navigation labels, current-page state and presence of all three navigation roles.

## Design Crit

- First visual gate: **KEEP** — the page claim remains dominant over navigation.
- Composition: **KEEP** — navigation forms a thin orientation frame around the page, not a dashboard.
- Proportion: **KEEP** — current page > local navigation > global index trigger.
- Hierarchy: **KEEP** — project/chapter/page hierarchy remains explicit without equating chapter count with page count.
- Typography: **KEEP** for calibration — neutral type; semantic roles are carried by scale/position before decoration.
- Spatial/material realism: N/A — this is an editorial/web navigation exercise.
- Scale: **KEEP within UI boundary** — desktop/mobile roles are separately considered; browser runtime screenshot remains environment-dependent.
- Interaction: **KEEP for prototype logic** — Project index is native `<details>`; actual assistive-technology/browser validation is not claimed.
- Narrative: **KEEP** — adjacent-page titles preserve reading continuity without exposing the whole directory.
- Professional finish: **KEEP FOR TRAINING**, not C04 Web MAIN promotion.

## Failure knowledge

- `CHAPTER ≠ PAGE`, and navigation must not silently re-collapse them.
- `all pages reachable ≠ all pages permanently visible`.
- `responsive rail hidden ≠ mobile navigation solved`.
- `no overflow ≠ orientation PASS`.
- A long-form interface can be technically complete and still cognitively flat when orientation, local continuity and global access are forced into one mega-navigation surface.

## Reusable rule

`PAGE IDENTITY → CURRENT LOCATION → LOCAL CONTINUITY → GLOBAL ACCESS → DESKTOP READ → MOBILE READ → OPEN/CLOSED INDEX STATE → DESIGN CRIT`

## Truth boundary

This training does not create the exact C04 52-row PAGE REGISTER, assign final N-series IDs, merge pages, prove final browser/accessibility conformance, or promote the current C04 Web. It modifies presentation/navigation logic only.