---
name: oleander-ui-interaction
description: OLEANDER interaction design skill for UI state machines, focus, interruption, re-entry, recovery, progressive disclosure, input routing, route/object continuity, feedback, keyboard/touch parity, and motion-state coordination.
status: candidate
version: 0.1.0
---

# OLEANDER UI Interaction

## Purpose
Design and review interaction as a stateful, interruptible system rather than a collection of click handlers and transitions.

Use this skill for screen flows, world/map interactions, focus/selection, reveal, Return, back behavior, touch/keyboard parity, re-entry, recovery, and coordination with `oleander-motion`.

## Authority discipline
- Product logic and state authority come from Current Authority, not from the current pixels.
- Interaction refinement may currentize behavior but may not invent new missions, rewards, route facts, services, safety claims, or completion requirements.
- Producer may report state-machine/runtimes facts, but final Design verdict remains independent.

## Core principles
### 1. Interaction is a conversation
Every action should have:
- recognizable affordance;
- immediate acknowledgement;
- visible/programmatic state change;
- clear next possibility;
- recovery path.

### 2. Preserve orientation
At every state, users should understand:
- where they are;
- what object is active;
- what changed;
- where they can go next;
- how to go back/Return.

### 3. Define state before animation
For every interactive object, define states before timing/easing:

```text
default
available/discoverable
focus/hover
pressed
selected/locked
entering
active
revealed
withdrawn
returning
unavailable/unknown/closed
disabled
reduced-motion equivalent
```

Only then assign motion.

### 4. Interruption is normal
Users change their mind. Long transitions must be cancelable or redirectable unless they represent an irreversible operation.

Test:
- choose A then B quickly;
- press Return during focus/enter;
- press Back during reveal;
- tap outside/cancel where applicable;
- repeat the same action;
- switch route/mode while another state is active.

### 5. Return / escape uses priority routing
If a project declares Return/safety/escape as high priority, it must bypass decorative locks and cancel lower-priority transitions.

Recommended priority model:

```text
SAFETY / RETURN / CLOSE
> RECOVERY / BACK
> CURRENT PRIMARY ACTION
> OPTIONAL REVEAL / READING
> FLAVOR / DECORATION
```

### 6. Progressive disclosure
Expose only what the user needs for the current decision. Optional explanation should appear after focus/interest, not occupy default first read.

### 7. Focus is a system state
Focus must be visible, stable, and semantic. Keyboard focus, gamepad/cardinal navigation, pointer focus, and touch selection should converge on the same interaction intent where possible.

Do not use invisible focusable hit areas.

### 8. Input routing
UI events dispatch intents. They should not mutate unrelated product state directly.

Recommended model:

```text
input → intent → state transition → UI update → motion/feedback
```

Avoid:

```text
click → arbitrary DOM/CSS mutation → second handler guesses what happened
```

### 9. Re-entry and memory
When users return from a detail/scene, preserve useful context where safe:
- route mode;
- focused node;
- scroll/pan position;
- journal context;
- accessibility settings.

Do not reset the world unnecessarily.

### 10. Motion is subordinate to state
Invoke `oleander-motion` after state transitions are defined. Motion explains cause, continuity, depth, or state change. Motion must not block critical tasks.

## Workflow
1. Read Current Authority and identify immutable product rules.
2. List screens/objects and their user intents.
3. Write a state table for each key object.
4. Draw transition graph including Back/Return/Cancel/Unknown paths.
5. Assign input methods: pointer/touch, keyboard, optional gamepad/cardinal if in scope.
6. Define focus and selection semantics.
7. Define interruption/priority routing.
8. Define progressive disclosure and optional layers.
9. Define re-entry/context preservation.
10. Hand transition roles to `oleander-motion` for timing/easing/spatial continuity.
11. Run attack tests in target runtime.
12. Report observed behavior and defects; do not self-score design quality.

## Minimum state table
For each P0 interaction record:

| Field | Required |
|---|---|
| object_id | yes |
| default_state | yes |
| intents | yes |
| transitions | yes |
| interruptible_by | yes |
| return_behavior | yes |
| keyboard_behavior | if web/keyboard in scope |
| touch_behavior | if mobile in scope |
| reduced_motion_behavior | if motion exists |
| unavailable/error behavior | yes |
| re_entry_behavior | yes |

## Runtime attack tests
At minimum:
- rapid target switch;
- Return during enter transition;
- repeated activation;
- keyboard-only traversal;
- focus visibility;
- touch target activation/cancel;
- Reduced Motion state equivalence;
- route/pan re-entry;
- unavailable/unknown state;
- no console/page errors after interaction sequence.

## Hard failure conditions
- critical action blocked by animation lock;
- Back/Return changes only appearance but not actual state;
- state can become impossible to exit;
- selection and focus disagree;
- pointer path works but keyboard/touch equivalent fails where required;
- invisible element remains focusable/clickable;
- reduced-motion mode removes feedback or leaves delay locks;
- re-entry unexpectedly resets high-value context;
- same intent mutates different rules across screens;
- UI state is duplicated in multiple unsynchronized variables without reason.

## Review output
```text
OBJECTS / INTENTS:
STATE TABLE:
TRANSITION GRAPH:
INPUT ROUTING:
FOCUS / SELECTION:
INTERRUPTION PRIORITY:
RETURN / BACK / RECOVERY:
PROGRESSIVE DISCLOSURE:
RE-ENTRY:
REDUCED MOTION:
RUNTIME ATTACK RESULTS:
OPEN DEFECTS:
INDEPENDENT DESIGN VERDICT REQUIRED: YES
```

## Source lineage
Adapted for OLEANDER from external interaction-pattern skills, game UI input/focus practices, accessibility-first state design, and OLEANDER's existing motion interruption/Return/reduced-motion rules.