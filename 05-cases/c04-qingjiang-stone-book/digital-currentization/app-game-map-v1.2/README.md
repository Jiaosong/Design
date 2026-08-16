# C04｜Qingjiang Thirteen Imprints App / Game Map v1.2

Status: `DESIGN CURRENTIZATION / MAIN CANDIDATE / FIELD OPEN / NO_PROMOTION`

## Material delta from v1.1
- single coherent visitor-facing SPA instead of duplicated static pages;
- fixed route-layer JS binding bug;
- ROUTE now has two independent controls: map purpose (journey/culture/rest/return) + travel focus (all/boat/cable/walk);
- R01–R13 retain complete optional library and can be filtered by content mode + audience depth;
- imprint dialog now carries action / audience value / carrier / digital-off fallback and can save directly into My Book;
- MY BOOK now supports real local-device writing via localStorage; no login, cloud or GPS claim;
- SERVICE adds actual print fallback and Digital FULL/LIGHT/OFF explanation;
- all final UI text, labels and map geometry remain HTML/SVG editable; no AI-generated UI/text.

## Truth boundary
- map is relationship/NTS, not measured geometry;
- no live operation claim;
- UNKNOWN stays fail-closed;
- route/safety/return do not depend on app completion;
- FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION.
