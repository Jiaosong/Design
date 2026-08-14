# OLEANDER MOT-02 State Transition Lab — 2026-08-14

## Knowledge position
- Domain: General Design Knowledge / Motion & Interaction Design
- Level: L5 Practice Method Candidate
- Canonical Path: `06-practice/2026/2026-08-14-mot02-state-transition/`
- Role: PRACTICE / TOOL METHOD
- Decision question: 状态变化时，怎样把“任务变化”置于装饰变化之前？
- Application Mapping: IP03 PRIMARY; B04 SUPPORTING.

## Project relation
- P2 Project ID: `PRAC-IP-2026`
- P3 Workstream ID: `PRAC-IP-2026-WS-03`
- P3 name: `Motion Hierarchy｜State × Attention × Reduced Motion`
- Current P3 state: `EXPLORE / G4`
- This Practice adds runtime evidence to the existing P3; it does not create P4 validation.

## Authority split
- Stable Motion Theory: Notion `KN-THEORY-MOTION-DESIGN-001`.
- Current/datable runtime-library routing: Notion `TOOL-MOTION-RUNTIME-ROUTING-001` + GitHub `oleander-skills/oleander-motion/`.
- GitHub skill merge/CI snapshot: Notion `EVD-MOTION-SKILL-V03-MERGE-20260811`.
- This artifact: executed MOT-02 runtime evidence only; it does not promote the Theory or every tool/library route.

## Variants
- No-motion Baseline: idle state.
- Candidate A / Simultaneous: card translation + dot scale/opacity + progress expansion share the same 320 ms transition.
- Candidate B / Task-led staged: progress leads (420 ms), secondary dot follows after 220 ms; container does not translate.
- Reduced Motion: all transition durations collapse to 1 ms; state remains explicit through progress fill, tone, and readout.

All durations, offsets, scale factors and timing values are **EXERCISE ASSUMPTIONS** and do not represent user-performance or project data.

## Executed runtime evidence
Runtime: system Chromium, headless, loaded via Playwright `page.set_content` because navigation to file:// / localhost is blocked by container administrator policy.

Observed states:
- baseline: `state=idle | reduce-motion=false`.
- 100 ms after active: Candidate A card already translates (~-7.73 px) and dot scales (~1.676) while its progress changes; Candidate B progress changes while secondary dot remains scale 1.0. This confirms the intended staged relation.
- 550 ms: both candidates reach active state; B secondary dot completes to scale 1.45.
- reduced-motion: computed transition duration for A card and B progress is `0.001s`.
- reset click returns to `state=idle | reduce-motion=false`.

## Design decision
- KEEP: Candidate B’s task-led sequencing and explicit reduced-motion state.
- REDUCE: progress easing should stay restrained; do not add additional secondary motion unless it encodes state priority.
- REMOVE: Candidate A’s container translation as a default status-change cue; it competes with progress without adding state information.
- Candidate rule: **Task-bearing state change should lead; secondary motion may follow only when it encodes a subordinate state relationship.** This remains an L5 Practice Method Candidate until tested in a real product task/user context.

## QA
- Machine QA: PASS — HTML/CSS/JS parsed and executed in Chromium; buttons and scripted state controls worked.
- Visual QA: PASS for this exercise — no clipping/occlusion; hierarchy, boundary, clearance and cross-state composition reviewed in generated screenshots.
- Project QA: PASS — directly answers the single decision question without reopening unrelated variables.
- Motion specialist review: PASS for runtime execution and reduced-motion behavior; no claim of user-experience improvement.
- Evidence boundary: EXECUTED digitally; NOT HUMAN TESTED; NOT PRODUCT VALIDATED.

## Internal score
- Technical correctness: 24/25
- File structure: 14/15
- Parameter/timing logic: 14/15
- Visual/time expression: 14/15
- Review/revision: 9/10
- Reproducibility: 9/10
- Project application value: 8/10
- Total: 92/100. Score does not override gates.

## Persistence gate
GitHub and Drive statuses must be reported independently. `SYNCED` requires target-platform readback.
