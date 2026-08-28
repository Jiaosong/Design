# OLEANDER Live-editable HTML Presentation Extension

Status: `CANDIDATE EXTENSION / STORY-AND-BOARD + WEB-UI + DELIVERY-QC`

## Purpose

Use when the required deliverable is a browser-based presentation, portfolio deck, roadshow, review deck or PPT-like HTML artifact that must remain directly editable after delivery.

This extension preserves a real editable browser artifact rather than turning slides into screenshots. It is independent OLEANDER implementation guidance; it does not import third-party template/code/prompt assets.

## Mode boundary

`RESPONSIVE WEBSITE ≠ FIXED-STAGE PRESENTATION`.

For presentation delivery:

- author a fixed 16:9 logical stage, normally `1920×1080` unless Current authority says otherwise;
- scale the stage uniformly to the viewport rather than reflowing slide composition through responsive breakpoints;
- show one live slide at a time;
- keep navigation/edit controls as viewport chrome, not authored slide content;
- maintain editable/vector/live text as DOM text, not rasterized text.

## Live-editing contract

A live-editable HTML deck should provide these capabilities when the user requests direct browser editing:

1. **Explicit edit mode** — editing is opt-in and visibly indicated; normal presentation remains clean.
2. **Stable semantic editable IDs** — every editable text object uses a stable semantic identity such as `slide-intro-title` or `slide-r06-caption`, never DOM-order persistence.
3. **Selective editability** — make authored visible copy editable; do not make navigation, filters or state-control labels editable when changing them would break runtime behavior.
4. **Local persistence** — save edits as a key/value object by semantic ID in browser storage or equivalent local state. Namespace storage by artifact identity and edit version.
5. **Save shortcut isolation** — `Cmd/Ctrl+S` may persist deck edits, but must not corrupt browser/page behavior.
6. **Editing/navigation isolation** — while focus is inside editable text, arrow keys, Space, Home/End and other slide shortcuts must edit text or behave natively rather than change slides.
7. **Re-render safety** — if dynamic filtering/re-rendering exists, save current edits before DOM replacement and restore by semantic ID afterward.
8. **Layout protection** — edited text must be rechecked for overflow, line wrapping, clipping, title collisions and bottom-safe-area violations. Live editing does not waive Design Quality.

## Standalone HTML export contract

When `Export HTML` is part of the deliverable, the exported file must embed the current edited state and remain usable without the original browser profile.

The export process must:

- serialize the current authored DOM with the latest edits embedded;
- retain required CSS and JavaScript for presentation, editing and re-export;
- remove transient editing UI state such as active contenteditable outlines or temporary runtime chrome that should not become authored slide content;
- set editable nodes back to a safe normal state on first open while preserving their semantic IDs;
- assign a new edit-version namespace so stale browser storage from the source file cannot overwrite the exported markup;
- preserve page/slide metadata, navigation behavior and live page counting;
- produce a portable `.html` artifact or self-contained folder according to Current delivery requirements.

`LOCAL STORAGE SAVE ≠ PORTABLE EXPORT`.

A saved edit that exists only in one browser profile is not a successful standalone delivery.

## Stable slide identity

Each slide should expose stable semantic metadata independent of current order, for example:

- `data-slide-id` — semantic stable identity;
- `data-original-number` — provenance/order reference if needed;
- `data-slide-title` — current title for QA/readback.

Current page number and total count must derive from the live slide collection so deletion/reordering does not create stale numbering.

Editable node IDs should derive from `slide-id + semantic role`, not current page index.

## Interaction contract

Presentation controls should support the Current project's required input methods. For ordinary browser decks, keyboard navigation should include next/previous and direct bounds access. Fullscreen is optional when runtime permits.

Hard requirements when live editing is enabled:

- slide shortcuts are suppressed inside `input`, `textarea`, `select` and editable text;
- entering/exiting edit mode does not alter the current slide unexpectedly;
- saving does not navigate;
- rapid next/previous remains deterministic outside editing;
- exactly one slide remains interactable at a time;
- reduced-motion mode retains full information and navigation.

## Media editing boundary

Text editability is the baseline. Media replacement is optional and must not silently rewrite Source Authority.

If image/video replacement is supported:

- preserve source/derivative provenance;
- do not replace authoritative project evidence with a browser-local image without an explicit new source record;
- maintain aspect/crop rules and rerun image/layout review;
- external blob/object URLs are not considered durable delivery unless packaged or resolved according to Current requirements.

## Round-trip verification

Before claiming the editable-deck capability works, perform this sequence in a real browser/runtime:

`OPEN SOURCE DECK → ENTER EDIT MODE → MODIFY A KNOWN EDITABLE OBJECT → SAVE → EXPORT HTML → OPEN EXPORTED FILE IN CLEAN CONTEXT → VERIFY EDIT IS EMBEDDED → VERIFY NAVIGATION → RE-ENTER EDIT MODE → MODIFY AGAIN → RE-EXPORT → REOPEN`

Record pass/fail for:

- edited text embedded in exported source;
- unique/stable edit namespace;
- slide navigation still works;
- editing still works after export;
- second export succeeds;
- no stale local state overwrites exported copy;
- edited content remains inside visual/layout limits.

If the exported file cannot be edited and exported again, the round trip is incomplete.

## Proof classes

Keep these separate:

`EDIT MODE EXISTS ≠ PERSISTENCE WORKS ≠ PORTABLE EXPORT WORKS ≠ NAVIGATION WORKS ≠ VISUAL QUALITY PASS`.

Automated browser checks can prove runtime mechanics. They cannot independently grant aesthetic KEEP.

## Ownership

- `oleander-story-and-board` — narrative, slide sequence, fixed-stage composition, target-scale visual review.
- `oleander-web-ui` — browser state, semantic IDs, edit-mode behavior, persistence, navigation isolation, export interaction.
- `oleander-motion` — transition semantics and reduced-motion equivalence when motion exists.
- `oleander-delivery-qc` — standalone portability, dependency integrity, round-trip reopen/edit/re-export proof.

## Candidate boundary

This extension is Candidate. A working editable HTML deck proves only the tested runtime and delivery behavior. It does not prove PowerPoint-native editability, production backend persistence, multi-user collaboration or aesthetic approval.