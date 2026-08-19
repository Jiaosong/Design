# C04 CH13 Delivery QC v2

## Scope
Visual-carrier revision for `CH13 / PHYSICAL · BODY · SENSORY`, preserving `CH13-P01..P07` authoring content while rebuilding presentation rhythm against current CH14 Web grammar.

## Material delta from v1
- Removed P01 four-grid dashboard; rebuilt as oversized editorial hero + abstract body/trace field.
- P02/P03 changed from explanation-first cards to object-first / boundary-first composition.
- P04 changed from mechanism-demo layout to a large `STEP → RESPONSE → FADE` spatial field; mechanism proof moved to near-read layer.
- P05 changed from four comparison cards to one competition ladder and a dominant Fluid Rest source field.
- P06 changed to large editorial reality-attack rows rather than cards.
- P07 changed from resource/table logic to a full dark sensory field and `NONE → TRACE → FRAME` progression.
- No fifth physical family added. No raw source board was redrawn or AI-substituted.

## CH14 alignment target
`CONTEMPORARY EDITORIAL + LANDSCAPE SPACE`

Applied as: primary object first, composition over boxes, large serif hierarchy, mineral-paper field, full-width dark bands, restrained mono metadata, continuous carrier, no local nav/footer/page break.

## Static integrity
- `CH13-P01..P07`: present.
- Duplicate element IDs: none.
- CSS braces: 197 / 197.
- Derived vector assets: present.
- Responsive CSS: desktop + mobile rules present.

**STATIC INTEGRITY = PASS**

## Actual Chromium runtime
Normal `file://` / localhost URL navigation is blocked by runtime administrator policy. To test the exact self-contained carrier, Playwright launched system `/usr/bin/chromium` under Xvfb and loaded the complete self-contained HTML with `page.set_content()`.

Results:
- Desktop viewport: `1920 × 1080`; document scroll size `1905 × 10085`; no horizontal overflow.
- Mobile viewport: `390 × 844`; document scroll size `375 × 13767`; no horizontal overflow.
- Embedded derived SVGs: both decoded and rendered (`240 × 150` intrinsic source viewBox).
- Step Light: after pointer activation, pulse count `1`; after ~1.7 s, pulse count `0`, matching transient `STEP → RESPONSE → FADE` behavior.

Evidence files:
- `review_v2b/desktop_full.png`
- `review_v2b/mobile_full.png`
- `review_v2b/step_click.png`

**TARGET-BROWSER RENDER / REFLOW = PASS**  
**STEP-LIGHT RUNTIME BEHAVIOR = PASS**

These runtime checks prove rendering and interaction behavior only. They do not prove finished-pixel design quality.

## Source hierarchy / source bind
ODB-02, ODB-03A/B and ODB-04B are verified as project source boards but their raw pixels are still not materialized in this runtime. Their dominant Web fields therefore remain explicit source-bind HOLDs rather than invented substitutes.

**SOURCE HIERARCHY = PASS**  
**PRIMARY SOURCE PIXEL BIND = HOLD**

## Independent design gate
Producer-side visual revision and runtime evidence are complete for this iteration. OLEANDER independent finished-pixel review is still required against CH14 at target size.

**INDEPENDENT FINISHED-PIXEL DESIGN VERDICT = PENDING**

## Promotion boundary
This v2 supersedes v1 only inside Draft PR #301 as the current producer candidate. It does not replace project Current Authority and must not be promoted while source pixel bind and independent finished-pixel review remain open.

`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`
