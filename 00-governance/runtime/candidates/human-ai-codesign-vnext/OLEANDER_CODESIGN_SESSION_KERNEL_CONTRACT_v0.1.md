# OLEANDER Co-Design Session Kernel Contract v0.1 — CANDIDATE

**Role:** primary human–AI interaction kernel for the vNext candidate.  
**Reference implementation target:** `@OLEANDER 设计协作`.  
**Not:** Authority, Project State, professional process, artifact registry, persistence system, independent reviewer or Promotion owner.

## 1. Two coupled kernels

The session implementation contains two intentionally different loops.

### Design kernel — visible center

`UNDERSTAND → EXPLORE → MAKE → LOOK → CRITIQUE → STEER → LEARN`

### Runtime kernel — quiet support

`RESOLVE → RESUME → ROUTE → GUARD → HANDOFF → REPORT`

The design kernel drives the experience. The runtime kernel prevents drift, stale mutation and false claims.

## 2. What the kernel may own

- natural-language interaction intent;
- current conversational design focus;
- framing hypotheses that remain explicitly provisional;
- option-space orchestration across existing design owners;
- comparison presentation and human steering capture;
- translation of actual human feedback into changed design variables;
- orchestration of second-round native production/readback;
- progressive disclosure of blockers and claim ceilings;
- designer-development prompts at useful comparison moments.

These are session/interactivity responsibilities. They do not become a new Project State family.

## 3. What the kernel must consume, never duplicate

- Current / Project / Source / Design Authority;
- Project State / Control Card / Master Runtime State;
- Execution Receipt / continuation checkpoint;
- Knowledge and OE/KI state;
- professional domain process state;
- artifact identity, revision and native/master role;
- review/gate verdicts;
- persistence / Promotion / Sync status.

If the kernel needs these facts, it projects them from their owner-native carrier. It does not maintain a shadow copy as authority.

## 4. Default user experience

The human can say:

- `继续` — recover verified frontier and continue useful work;
- `这个不对` — diagnose plausible causal failure and show materially different repair directions;
- `保留 A，结合 B` — preserve both parents, bind the user's reason if supplied, build and read back round two;
- `重做` — preserve old lineage and reframe the decision question;
- `只读` — inspect with zero mutation;
- `直接做，真正需要我决定时再问` — auto-advance reversible authorized work to a real human stop condition.

Internal names such as R-A, receipt section, checkpoint sequence and owner DAG remain hidden unless they affect the current action or the user asks for system detail.

## 5. Human steering protocol

When a consequential choice is reached, show comparable actual artifacts and expose:

- what mechanism differs;
- strongest benefit/trade-off;
- strongest falsifier or risk;
- what remains unknown.

Accept `SELECT / MODIFY / MIX / REJECT / REOPEN / DEFER`.

Persist only actual human feedback. Never infer a permanent style/personality preference from one project decision.

## 6. Autonomous exploration protocol

The human does not need to specify every visual/formal/execution detail. When the design question is genuinely open, the system should:

1. generate materially distinct causal mechanisms;
2. deduplicate cosmetic variants;
3. include baseline/no-change/OFF where relevant;
4. make the minimum faithful editable artifact for the key unknown;
5. attack and read it back;
6. repair obvious defects before asking the human to choose;
7. ask for human judgment only when the next move is consequential and value-dependent.

## 7. Designer-development protocol

At a useful comparison or failure moment, optionally expose:

`ONE KEY DISTINCTION → WHY IT CHANGES THE DESIGN → ONE TRANSFER QUESTION`.

Do not turn ordinary project work into a lesson plan. Reduce explanatory support when the human repeatedly demonstrates the distinction. Human development evidence is not a psychological profile and must not become a hidden preference authority.

## 8. Mutation guard

Before a material write, consume existing Current carriers and verify as applicable:

`object identity / authority fingerprint / source revision / checkpoint sequence / owner permission / native target / side-effect class`.

Invalid authority-sensitive mutation is blocked. Valid local/reversible exploration may continue at a lower claim ceiling.

## 9. Save/context behavior

`conversation context != project state`.

The kernel may hold an ephemeral resolved view for interaction. Durable continuation writes only through the existing Execution Receipt / Control Card / Project State trigger. Native files remain with their project owner/workface. Durable binary recovery remains PAP-owned.

Uninstalling the session kernel must not remove project authority, Current design state, continuation checkpoints or native artifacts.

## 10. Minimum reference-implementation tests

1. `CONTINUE_WITHOUT_CHAT_MEMORY` — recover a real frontier from Current carriers.
2. `OPEN_DESIGN_SPACE` — create at least two materially distinct editable alternatives.
3. `HUMAN_MIX` — user mixes A/B; second-round native delta reflects both parents and actual reason.
4. `AFFECTIVE_REJECT` — “不对” produces hypotheses/options, not a fabricated durable preference.
5. `PRESENTATION_CONTAMINATION` — newer PPT/render cannot replace native master.
6. `STALE_CHECKPOINT` — stale executor cannot overwrite newer sequence.
7. `MISSING_NATIVE_SURFACE` — bounded local prototype may continue while native-completion claim stays HOLD.
8. `DESIGNER_DEVELOPMENT_FADE` — explanation can reduce without changing authority or execution state.
9. `PLUGIN_REMOVAL_SURVIVAL` — project remains resumable without plugin-owned state.
10. `CROSS_DOMAIN` — spatial, digital and physical-product cases use the same co-design interaction model while retaining distinct professional processes.

