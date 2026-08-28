# OLEANDER Live-editable HTML Presentation QC

Status: `CANDIDATE QC EXTENSION`

Use when a browser-based presentation/deck claims direct editing, local persistence, standalone HTML export or portable handoff.

## Proof contract

Keep these proof classes separate:

`EDIT UI VISIBLE ≠ EDIT PERSISTENCE ≠ PORTABLE EXPORT ≠ CLEAN-CONTEXT REOPEN ≠ RE-EDIT ≠ RE-EXPORT ≠ DESIGN PASS`.

A demo that edits text in one browser tab but cannot embed the current state into a portable exported file is not a complete live-editable delivery.

## Required round-trip

Run in a real browser/runtime:

1. Open the Current editable deck.
2. Enter edit mode.
3. Modify one known editable text node with a stable semantic edit ID.
4. Save/persist.
5. Export standalone HTML.
6. Open the exported file in a clean browser context or isolated profile/file context.
7. Verify the edited content is embedded in the exported artifact without relying on the source browser's prior storage.
8. Verify slide navigation and current/total numbering.
9. Re-enter edit mode in the exported file.
10. Modify a second editable node.
11. Re-export.
12. Reopen the second export and confirm the second edit persists.

Return `HOLD` if any required round-trip step cannot be executed in the claimed delivery environment.

## Identity and storage checks

- Editable text nodes use stable semantic IDs, not DOM-order indexes.
- Storage is namespaced by artifact/file identity and edit version.
- Export creates a fresh edit-version namespace or equivalent stale-state protection.
- Reordering/deleting slides does not attach prior edits to the wrong content object.
- Current page number and total derive from the live slide collection.
- Browser-local storage is treated as working state, not as the portable master.

## Interaction checks

- Slide navigation shortcuts do not fire while focus is in `input`, `textarea`, `select` or editable text.
- Editing arrow-key behavior remains native inside text.
- Save commands do not navigate or invoke unintended browser save-page behavior when the deck intentionally overrides them.
- Entering/exiting edit mode does not change the active slide unexpectedly.
- Rapid next/previous outside edit mode leaves exactly one slide interactable.
- Reduced-motion mode preserves the same information and navigation.

## Export integrity checks

The exported standalone artifact must:

- contain the current edited text/state required for portability;
- preserve required CSS/JS/navigation/edit logic;
- not depend on inaccessible absolute local paths;
- not preserve transient editing chrome as authored slide content;
- reopen without the source build environment when standalone delivery is claimed;
- remain capable of a second edit and second export when re-editability is part of the claim.

## Visual regression after edit

Live editing can create new layout defects. After the round-trip edit, inspect at least the edited slides at target playback size for:

- title/body overflow;
- unintended reflow or clipping;
- image/text collision;
- bottom-safe-area violation;
- broken hierarchy from line-count change;
- CJK/Latin fallback changes;
- control chrome obscuring authored content.

Runtime success does not grant aesthetic KEEP. Return visual defects to `oleander-story-and-board` / `oleander-visual-design`.

## Source boundary

- The HTML/HTML+asset package remains the Current editable browser master only when Current authority defines it so.
- A downloaded/exported copy is a derivative/new portable generation unless promoted by the project Current pointer.
- Browser editing does not authorize replacing authoritative project images, maps, geometry or evidence without a new source/authority record.
- This capability does not prove PowerPoint-native editability, cloud sync, collaboration, conflict resolution or backend persistence.

## QC record

Return:

- source deck identity/hash or commit;
- browser/runtime used;
- edited semantic IDs;
- persistence namespace/version;
- first export identity/hash;
- clean-context reopen result;
- navigation result;
- re-edit result;
- second export/reopen result;
- visual regression result;
- blocker/warning list;
- final `PASS / REVISE / HOLD` for the claimed live-editable delivery behavior.