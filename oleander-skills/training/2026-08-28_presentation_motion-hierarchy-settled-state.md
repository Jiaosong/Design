# OLEANDER PRESENTATION Training Evidence — Motion Hierarchy × Settled State

Status: `PRACTICE_EVIDENCE / MOTION-SETTLED-STATE / NO PROJECT WRITE / NOT ACTIVE`
Mode: `TRAINING_MODE`
Owner context: PRESENTATION / existing installed `oleander-motion`

## GAP
Motion hierarchy / settled state: state changes either animate every layer equally, or use long stagger/bounce that delays a stable final frame. Reduced Motion can also remove visuals while retaining artificial wait time.

## SOURCE
Apple Human Interface Guidelines — Motion + Accessibility / Reduced Motion. Motion should have a clear purpose, feedback should be brief and precise, frequent operations should avoid unnecessary motion, animations should be interruptible, and Reduce Motion should preserve meaning with lower-motion alternatives.

## ARTIFACT
Editable HTML/CSS/JS state transition prototype; no generated imagery; real Chromium normal/reduced-motion runtime; keyframes at 80/180/280/520 ms; rapid-repeat interruption attack; desktop + 390px mobile; grayscale settled-state readback.

## A/B
A simultaneous movement + ongoing marker drift → B1 hierarchy via excessive stagger/bounce → B2 primary-first fast settle → B3 repair synchronizes Reduced Motion with immediate state settlement and guards against stale transition timers.

## READBACK
A keeps moving after the information state is already understandable. B1 establishes sequence but delays final legibility beyond a second. B2 settles quickly in normal mode but Reduced Motion still leaves a 260 ms semantic wait. B3 reaches a stable state rapidly, survives rapid repeat to the latest selected state, and Reduced Motion reports SETTLED immediately while preserving the same content/state.

## FAILURE / ROOT CAUSE
Motion quality was conflated first with amount of movement, then with choreography complexity. The B2 accessibility failure came from treating motion removal as CSS-only while leaving timing semantics unchanged.

## REPAIR / RETEST
Primary heading receives the only positional transition; support layers fade within the same short window; no element loops after settle. State timers use a transition token so interrupted transitions cannot overwrite the latest state. Reduced Motion collapses both visual animation and artificial wait time. Reopened normal/reduced desktop, rapid-repeat attack, mobile and grayscale.

## TRANSFER RULE
`DECLARE STATE + MOTION ROLE → MOVE PRIMARY RELATION FIRST → RESOLVE SUPPORT INSIDE THE SAME SHORT WINDOW → STOP ALL NONESSENTIAL MOTION AT SETTLE → MAKE REDUCED MOTION SEMANTICALLY IMMEDIATE → ATTACK RAPID REPEAT / INTERRUPT`

`MOTION HIERARCHY ≠ STAGGER QUANTITY`

## BOUNDARY
Training interface is not project UX evidence. No claim is made about comprehension, comfort or accessibility beyond runtime behavior. Project motion still requires project-specific trigger, frequency, interaction and browser/device validation.

## STATUS
`PRACTICE_EVIDENCE / MOTION-SETTLED-STATE / NO PROJECT WRITE / NOT ACTIVE`
