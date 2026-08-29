# Cross-context Practice — Editorial Publication System — Multi-document Technical Manual

Status: `CROSS_CONTEXT_EVIDENCE / CONTROLLED PRACTICE / NO_PROJECT_USAGE / NO_PROMOTION`

## Why this context is materially different

Batch-4 `SK-STORY-006` attacks a 64-page image-led catalog. This practice uses a fictional 120-page maintenance and operation manual whose primary requirements are non-linear retrieval, versioned chapters, repeated technical objects, section numbering, appendices and shared styles. Pacing is subordinate to findability and change control.

## Second-source cross-check

Current Adobe InDesign Book documentation was used as a bounded production cross-check. Adobe's Book model keeps individual documents separate while coordinating document order, numbering and shared style sources across a long-form project.

Sources:
- `https://helpx.adobe.com/indesign/desktop/create-and-organize-pages/create-and-manage-book-files/create-save-book-files.html`
- `https://helpx.adobe.com/indesign/desktop/create-and-organize-pages/create-and-manage-book-files/add-documents-to-book-files.html`

Rights boundary: no Adobe UI screenshot, template, style set, proprietary example or branded publication design is copied. InDesign is treated as one possible runtime carrier, not the conceptual authority for OLEANDER publication design.

## Synthetic publication purpose

Manual purpose: let a technician locate an operation, warning, replacement sequence or specification quickly and verify which revision they are reading.

Synthetic content modules:
- D00 Front matter + revision record
- D01 System overview
- D02 Safety boundaries
- D03 Routine operation
- D04 Maintenance procedures
- D05 Replaceable components
- D06 Troubleshooting
- D07 Technical specifications
- D08 Appendices / glossary / index

No real product claims are made.

## Multi-document authority model

`BOOK MANIFEST → DOCUMENT ORDER → STYLE SOURCE → NUMBERING / SECTION RULE → DOCUMENT CONTENT → CROSS-REFERENCE / INDEX → EXPORT DERIVATIVE`.

The book/manifest coordinates the publication but does not replace the individual editable documents. A PDF export is a derivative, not the publication source master.

## Flat-plan excerpt

| Pages | Document | Page role | Primary use | Density | Cross-link requirement |
|---|---|---|---|---|---|
| 1–6 | D00 | front matter | identify manual/revision/navigation | low–medium | TOC + revision record |
| 7–18 | D01 | overview | understand system components | medium | component IDs → D04/D05 |
| 19–30 | D02 | safety | recover warnings before procedures | medium | warning IDs reused at point of action |
| 31–52 | D03 | operation | step-by-step normal use | medium | operation IDs → troubleshooting |
| 53–82 | D04 | maintenance | procedures + inspection | high | tools/parts/spec links |
| 83–96 | D05 | replacement | component-specific replacement | high | part IDs + return to maintenance |
| 97–108 | D06 | troubleshooting | symptom → check → action | high | links back to exact procedure IDs |
| 109–116 | D07 | specifications | exact lookup | high | units/source authority |
| 117–120 | D08 | appendix/index | non-linear retrieval | medium | index/glossary/cross-reference |

This is a planning artifact, not a real pagination guarantee.

## Page-role / master family

A limited role family is sufficient:
- `M-OPEN` — chapter opener with revision/section identity;
- `M-PROC` — procedure page with step, tool/part and warning ownership;
- `M-SPEC` — specification/table page;
- `M-TROUBLE` — symptom/check/action relation;
- `M-REF` — glossary/index/appendix.

No hero/image-led spread master is required merely because the catalog practice had one.

## Shared-style / local-exception contract

For a multi-document carrier:
- one declared style source owns shared paragraph/character/object/table style identities;
- document-local overrides require a reason and cannot silently redefine the same semantic role;
- chapter-specific exceptions use explicit new semantic IDs rather than visually similar anonymous overrides;
- synchronization is a controlled action with readback; it is not proof that the resulting pages remain visually or semantically correct.

`SYNC SUCCESS ≠ DESIGN QUALITY PASS ≠ CONTENT/TRUTH PASS`.

## Numbering / cross-reference gate

Required synthetic identities:
- chapter IDs D00–D08;
- procedure IDs `PROC-*`;
- warning IDs `WARN-*`;
- component IDs `CMP-*`;
- figure/table IDs;
- revision ID.

Page numbers may shift when documents change; cross-references should resolve through stable semantic IDs where the production tool supports them rather than hard-coded page-number prose.

## Non-linear reading attack

Unlike a catalog, the manual cannot depend on the reader having seen the previous spread. Every procedure page must recover enough local context to identify:
- current system/component;
- procedure identity;
- prerequisite/safety state;
- continuation/return path;
- relevant revision/source boundary.

This strengthens the existing extension's single-page integrity rule.

## Full-sequence readback attack

Review set for this context:
- TOC → chapter entry correctness;
- one procedure that crosses a page boundary;
- one warning repeated at multiple points without wording drift;
- one specification table with unit/source integrity;
- one troubleshooting route that links back to a procedure;
- one chapter inserted late to test numbering/cross-reference stability;
- index/glossary entry after pagination change;
- PDF export/reopen with bookmarks/links only if the delivery route requires them.

## Readback verdict

**KEEP as cross-context evidence:** flat-plan, page-role, caption/folio/navigation and sequence concepts transfer, but the dominant design value changes from visual pacing to retrieval/change resilience.

**Material delta:** add an explicit `MULTI-DOCUMENT / STYLE-SOURCE / NUMBERING / CROSS-REFERENCE AUTHORITY` gate when the publication is assembled from multiple editable files or is expected to change over time.

**REJECT:** treating InDesign's Book feature, one shared style source, or successful synchronization as universal software requirement or proof of publication quality.

**HOLD:** no actual INDB/INDD runtime, technical content authority, PDF accessibility validation, print proof or real manual user test. Therefore no Project Usage Evidence or Independent KEEP.