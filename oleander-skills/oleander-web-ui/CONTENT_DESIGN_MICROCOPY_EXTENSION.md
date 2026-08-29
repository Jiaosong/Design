# OLEANDER Content Design + Microcopy Extension

Status: `CANDIDATE EXTENSION / WEB-UI`

Use when interface words materially affect task comprehension, action consequence, state recognition, trust, recovery, accessibility or localization. This is not a copywriting house style and does not replace `oleander-ui-interaction`, `ACCESSIBLE_INTERACTION_EXTENSION.md`, brand voice authority, legal/compliance review or backend truth.

## Core contract

`USER TASK / PRODUCT PURPOSE → CURRENT STATE → CONTENT ROLE → ACTION / CONSEQUENCE → SYSTEM RESPONSE → RECOVERY / INVERSE ACTION → IMPLEMENTATION / LOCALIZATION → ACTUAL STATE READBACK`.

Words are interaction material when they change what the user understands, chooses, expects or can recover from. A polished sentence that misstates system state or available recovery is a design defect.

## Conversation-flow gate

For a material flow, inspect the sequence rather than isolated strings:

- entry point and what the user already knows;
- instruction or context actually required;
- action label and the consequence it promises;
- loading/progress state when delay matters;
- success confirmation and any visibility/reversibility consequence;
- validation/system failure state;
- realistic recovery, retry, alternative path, cancel, undo or Return behavior;
- inverse/destructive action when relevant.

Use the appropriate content carrier for the state: title, label, helper text, CTA, inline error, banner, dialog, empty state, toast, notification or help surface. Do not use a more prominent component merely to compensate for unclear wording or broken interaction design.

## Action-consequence gate

For material buttons and links:

1. Resolve the actual system consequence first.
2. Name the action/outcome at the specificity required by the stakes.
3. Distinguish reversible, cancelable, destructive, paid, publishing/sharing and permission-granting actions.
4. If the backend does not support undo/retry/cancel, copy must not imply that it does.
5. Generic labels may be acceptable when surrounding context makes the consequence unambiguous; there is no universal word-count rule.

`GOOD LABEL ≠ VERIFIED SYSTEM CONSEQUENCE`.

## Error and recovery gate

Treat errors as interaction states, not tone exercises.

Record:
- what failed in user terms;
- whether the failure can be prevented earlier;
- which entered values/state must be preserved;
- the specific recovery or escape path actually available;
- programmatic association/announcement required by the implementation;
- whether the error is field-level, page-level, permission, offline, service or blocking.

Prefer `AVOID → EXPLAIN → RESOLVE`, but do not force a fixed sentence formula. Never invent causes, availability, deadlines, support channels or remediation steps.

## Empty / loading / success state gate

- Empty state: distinguish first use, user-cleared content, no results, permission state and load/error absence before writing the message.
- Loading/progress: state only what the system can support; unknown duration stays unknown.
- Success: confirm only what actually completed, and surface important next-step, visibility, delivery or reversibility consequences when material.

A visually empty state is not automatically an onboarding opportunity; if no meaningful action exists, do not manufacture one.

## Voice, tone and trust

Voice is a persistent product/brand property; tone adapts to task, stakes and user context. Do not import external personality adjectives as OLEANDER defaults.

For sensitive or high-stakes moments:
- disclose why sensitive data is required when that reason is material to trust;
- avoid playful language that obscures cost, data use, surveillance, deletion, consent or irreversible effects;
- route regulated/legal/medical/financial wording to the proper authority instead of rewriting truth for friendliness.

## Localization and implementation

When copy becomes a real UI string, check:
- expansion/contraction and longest-string behavior;
- script/language coverage and fallback through `TYPOGRAPHY_SYSTEM_EXTENSION.md` when needed;
- variable/place-holder ambiguity;
- programmatic label/description/error association;
- dynamic announcement when a state changes without focus movement;
- component/state identity so the same concept is not named differently across screens.

A string catalog, token file or translation-ready key does not prove the rendered state remains usable.

## Readback attacks

At minimum inspect applicable states in the actual interface or prototype:
- normal task path;
- validation error;
- offline/service failure;
- empty/no-results;
- destructive or irreversible action;
- success/confirmation;
- narrow/translated stress state when localization is material.

Delete surrounding explanatory prose and ask whether the label/message still identifies the task/state/consequence. Then test the opposite: if the copy were removed, is the interaction structure still coherent? Copy should clarify a sound model, not hide a broken one.

## Cross-owner routing

- state machine / interruption / re-entry → `oleander-ui-interaction`;
- semantic HTML, focus, programmatic names and dynamic announcements → `ACCESSIBLE_INTERACTION_EXTENSION.md`;
- IA naming/canonical homes → `INFORMATION_ARCHITECTURE_WAYFINDING_EXTENSION.md`;
- brand voice authority → Current brand/visual communication knowledge + `oleander-visual-design` as needed;
- typography/script/longest-string stress → `oleander-visual-design/TYPOGRAPHY_SYSTEM_EXTENSION.md`;
- legal/compliance/security/backend truth → proper domain authority / VALIDATION.

## Rejected external defaults

Do **not** promote as universal OLEANDER rules:
- fixed character counts or line lengths;
- fixed school-grade reading levels;
- fixed active-voice percentages;
- fixed CTA word counts;
- one mandatory error-message sentence template;
- one default emotional tone for all products;
- conversion uplift claims without project evidence.

These may be contextual diagnostics only when a Current source or project test justifies them.

## Required output

Return the user-task/state map, content-role inventory, action/consequence labels, stress-state copy, recovery/inverse-action contract, localization/accessibility implementation notes, actual state readback, rejected assumptions and unresolved truth/compliance holds.

## Candidate boundary

This extension is independently reformulated from MIT-licensed study of `content-designer/ux-writing-skill` and `hueyexe/frontend-agent-skills/ux-writing-content-design`, cross-checked against public GOV.UK error-message guidance. External templates, fixed benchmarks, examples and house voice are not OLEANDER defaults. Real project use and independent review are required before stronger maturity claims.