# Cross-context Practice — Content Design / Microcopy — Desktop Sync Recovery

Status: `CROSS_CONTEXT_EVIDENCE / CONTROLLED PRACTICE / NO_PROJECT_USAGE / NO_PROMOTION`

## Why this context is materially different

Batch-4 Golden `SK-WEB-009` attacks signup/payment/account wording. This practice uses a desktop sync conflict with offline state, local-only work, destructive reset and delayed cloud confirmation. The content problem is therefore not conversion/onboarding; it is preservation, consequence, uncertainty and recovery.

## Second-source cross-check

Microsoft Windows writing guidance was used only as a bounded professional cross-check: actions should be understandable from button text, dialogs should form a coherent call-and-response, and errors should help the user recover. Microsoft voice adjectives, fixed button-length advice and source examples are not adopted as OLEANDER defaults.

Source: `https://learn.microsoft.com/en-us/windows/apps/design/style/writing-style`

Rights boundary: no Microsoft examples, screenshots, branded strings or house voice copied into this practice.

## Synthetic system truth

Assume a fictional desktop design app with these verified behavior constraints:

- unsynced local edits exist;
- cloud version is older than local version;
- network is currently offline;
- `Keep local version` preserves local edits and queues sync later;
- `Replace local with cloud` permanently discards unsynced local edits after confirmation;
- there is no server-side undo after replacement;
- reopening the dialog does not change the underlying versions;
- app cannot truthfully predict when connectivity will return.

These are scenario inputs, not claims about a real product.

## State / content-role map

| State | User question | Carrier | Accepted content role | Rejected failure |
|---|---|---|---|---|
| Conflict detected | What happened? | dialog title + body | name the version conflict and local-unsynced condition | `Something went wrong` |
| Offline | Can this sync now? | inline status | say sync cannot complete while offline; avoid time promise | `We'll sync in a few minutes` |
| Preserve local | What will this do? | primary/secondary action | `Keep local version` + consequence note that sync will retry later | generic `Continue` |
| Destructive replace | What will be lost? | destructive action + confirmation | `Replace local with cloud` and explicitly state unsynced local edits will be deleted | `Use cloud` without loss statement |
| Replacement complete | Did it finish? | confirmation | confirm local file now matches cloud version; do not claim cloud changed | `Everything is synced` |
| Retry after connectivity | What happens next? | status | identify queued retry without invented ETA | spinner with no state text |

## Dialog contract

**Title:** `Choose which version to keep`

**Body:** `This device has changes that have not been synced. The cloud copy is older, and you're currently offline.`

**Safe action:** `Keep local version`

Supporting consequence: `Your local edits stay on this device. Sync will retry when a connection is available.`

**Destructive action:** `Replace local with cloud`

Destructive confirmation title: `Delete unsynced local edits?`

Destructive confirmation body: `Replacing this file will remove the unsynced edits on this device. This cannot be undone from the cloud.`

Buttons: `Cancel` / `Replace local with cloud`

## Recovery / inverse-action contract

- `Cancel` returns to the unchanged local document.
- `Keep local version` is not described as an undo; it is a preservation decision.
- Destructive replace exposes no false undo path.
- Offline state provides no invented retry time.
- After connectivity returns, queued sync may proceed; the confirmation copy must reflect actual result rather than optimistic intent.

## Localization / accessibility stress

Attack strings that are most likely to expand:
- `Replace local with cloud`
- `Your local edits stay on this device. Sync will retry when a connection is available.`
- `Replacing this file will remove the unsynced edits on this device.`

Implementation handoff:
- destructive dialog title must be programmatically associated with the dialog;
- offline/conflict status changes need an announced state when they update without focus movement;
- button semantic identity must remain stable across translations;
- no positive-tabindex or custom click-only replacement is introduced by copy work.

## Readback verdict

**KEEP as cross-context evidence:** action/consequence and error/recovery contract transfers cleanly from web signup/payment context to offline desktop sync.

**REVISE boundary:** Microsoft guidance that buttons should be only a couple of short words is not portable enough for this destructive action; consequence clarity takes priority over a fixed length heuristic.

**HOLD:** no real desktop runtime, localization render, assistive-technology test or backend implementation was executed. Therefore this is `CROSS_CONTEXT_EVIDENCE`, not `PROJECT_USAGE_EVIDENCE`, browser/runtime PASS or Independent KEEP.

## Material delta to retain

The practice strengthens one rule in the extension without creating a new owner:

`CONCISE ACTION LABEL < CONSEQUENCE-LEGIBLE ACTION LABEL` when shortening would hide irreversible or material system effects.

This remains contextual, not a license for verbose labels.