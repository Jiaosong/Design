# OLEANDER Continuity / HOME Management Protocol v0.1

**Status:** `CANDIDATE / NON-AUTHORITY CONTINUITY LAYER`

This directory implements the user-facing management and cross-surface continuity layer for OLEANDER. It is deliberately **not** a second Project State, Project Registry, Control Card database, artifact registry, execution checkpoint, Current Authority, Design KEEP authority or Promotion authority.

## 1. Purpose

OLEANDER may be entered from several surfaces:

- Chat On Steroids (COS) on the main workstation;
- ChatGPT Web;
- ChatGPT Desktop;
- the separate Knowledge administration surface.

Those surfaces are sessions, not separate systems. They must converge on the same owner-native project/runtime state instead of each keeping its own project truth.

The continuity layer therefore provides only four things:

1. a thin `HOME` index of where authoritative carriers live;
2. an operator-attention projection (`ACTIVE / PARKED / ARCHIVED`) that does not rewrite project state;
3. session receipts describing what happened in one Human–AI session;
4. execution intents that can carry explicit Human instructions between remote and local execution surfaces.

## 2. Authority boundary

The following remain authoritative in their existing owners:

- OLEANDER Current Authority and runtime contracts;
- Project / Case identity and the existing Project Registry;
- Project State / Current Task owner-native carriers;
- Project Control Cards;
- `OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json` for automated project production priority;
- source / artifact / native-master identity;
- execution receipts and checkpoints;
- Design KEEP / professional verdicts / independent review;
- persistence, Promotion and cross-system synchronization;
- Knowledge Architecture, KI/OE state and Knowledge Registry.

`HOME` stores pointers to those carriers. It must not copy their mutable facts and then become a competing source of truth.

Hard rule:

`HOME POINTER != PROJECT STATE`

`ATTENTION_STATE != PROJECT STATE`

`SESSION RECEIPT != CURRENT TASK RECEIPT`

`EXECUTION INTENT != MUTATION PERMISSION`

`CHAT MEMORY != AUTHORITY`

## 3. Session entry sequence

Any COS / Web / Desktop conversation that is asked to "continue OLEANDER", "show OLEANDER status", or continue a named project should resolve in this order:

1. read `00-governance/runtime/OLEANDER_RUNTIME_LATEST.md`;
2. read `OLEANDER_HOME_INDEX_v0.1.json` only as a locator/attention projection;
3. for a formal project, reopen the exact `authority_refs` and `control_card_ref`/project-native Current carrier before consequential reasoning;
4. if automated production priority matters, reread `00-governance/OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json` rather than copying its order into HOME;
5. resolve the minimum task-scoped Knowledge through the existing Knowledge owners;
6. before any material project write, rerun the existing owner-native mutation/authority guards and checkpoint freshness checks.

## 4. Surface roles

### COS

Primary local execution surface. It may operate local files, Git, CAD, 3D, renderers and other approved native tools. Local execution still requires the exact project owner-native authority/readback chain.

### ChatGPT Web / Desktop

Remote co-design and management surfaces. They may inspect synchronized state, discuss, compare, record explicit Human feedback/steer/decisions and create a bounded execution intent. They must not claim that workstation-only native execution occurred when it did not.

### Knowledge administration surface

Administrative maintenance surface for importing, deduplicating, provenance, classification and Knowledge lifecycle work. It is not the place where project Current state is stored.

## 5. ACTIVE / PARKED / ARCHIVED

`attention_state` is an operator-attention projection only.

- `ACTIVE` — should be surfaced routinely for continuation and Human Stops.
- `PARKED` — preserved but not loaded into routine context unless requested or a dependency reopens it.
- `ARCHIVED` — historical/closed for attention purposes; authority/history remains with the original owner.

This classification does **not** change a project's own `STATE`, professional stage, Control Card, Priority Queue entry or archive authority.

The automated Project Priority Queue remains governed by `OLEANDER_WORK_COORDINATION_CONTRACT_v1.0.md` and retains its existing maximum of three ACTIVE production slots. HOME does not create a second queue.

## 6. Remote → local execution handoff

Use `execution-intents/*.json` only to carry explicit Human intent across surfaces.

Canonical sequence:

`REMOTE HUMAN INPUT → EXECUTION INTENT → LOCAL OWNER-NATIVE REREAD → AUTHORITY / CHECKPOINT / CONSTRAINT GUARD → EXECUTION → ACTUAL READBACK → OWNER-NATIVE PROJECT RECEIPT / STATE UPDATE → SESSION RECEIPT`

Rules:

- an execution intent cannot itself change Project State;
- the intent must preserve the user's exact wording;
- project mutation requires a fresh local reread of the actual owner-native authority/state carrier;
- drift between capture and execution is fail-closed;
- a consumed intent points to the session receipt that consumed it;
- project writeback is recorded only by the existing project-state/current-task mechanism, never by editing the intent into a fake completion record.

## 7. Session receipts

`sessions/*.json` record session continuity:

- which surface was used;
- the Human's explicit intent;
- which owner-native carriers were actually read;
- what candidate/local artifacts were produced;
- any execution intents created or consumed;
- unresolved boundaries and Human Stops;
- what the receipt does not prove.

A session receipt is deliberately insufficient to claim a changed project decision, Current Task, Design KEEP, professional PASS or Promotion unless it references the corresponding owner-native receipt that actually made that change.

## 8. HOME update rule

HOME may update pointers, attention state, surface availability and receipt/intent indexes.

It must not copy dynamic fields such as:

- `CURRENT_NATIVE_MASTER`;
- current professional stage/verdict;
- locked/open design variables;
- project decision status;
- checkpoint sequence;
- Design KEEP;
- Promotion status;
- artifact-registry contents.

Those values are read from the owner at use time.

## 9. Validation

Run:

```powershell
py -3.13 00-governance/runtime/continuity/validate_continuity.py
py -3.13 00-governance/runtime/continuity/show_home.py
```

The validator checks schema validity, local reference resolution, authority-boundary invariants, attention-state limits and session/intent linkage. It cannot validate professional/design quality and does not grant Current adoption.

