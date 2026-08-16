# C04｜Qingjiang Thirteen Imprints App Architecture v1.4

State: `APP ARCHITECTURE DEEPENING / NO COMPRESSION / FIELD OPEN / NO_PROMOTION`

This document deepens the App architecture without changing the project-level 12-layer Web architecture and without turning the App into a scenic-area super-app.

## 0. Product thesis

The App is an **invisible travel companion**. It appears when the visitor needs orientation, optional interpretation, a short scene interaction, recovery/return information, or memory capture; it retreats when landscape, movement, body, safety, or direct human service should dominate.

Core rule:
`SERVICE / RETURN > ROUTE > OBSERVATION > EXPLANATION > MEMORY > SHARE`

## 1. Global Shell｜always available, never content-gated

### G1 Reality State
- NORMAL
- DEGRADED
- CLOSED
- UNKNOWN

The App never converts UNKNOWN into normal-open presentation.

### G2 Delivery State
- FULL
- LIGHT
- OFF

This controls digital density, not route authority.

### G3 Persistent actions
- RETURN / 服务
- Digital Silence / 手机退场
- Offline / No-phone handoff
- Current journey orientation

### G4 Context strip
Always shows only what matters now:
`WHERE / MOVE / RETURN / DIGITAL`

No points, streaks, completion percentage, or 13/13 progress.

---

## 2. TODAY｜What matters now

TODAY is not a dashboard. It is the **current travel decision page**.

### T1 Situation
- current reality state
- current delivery state
- route/return availability
- offline state

### T2 Next Move
- ARRIVAL
- BOAT
- CABLE
- WALK
- RETURN

Only one dominant next action is shown.

### T3 Journey Scale
- BOAT / continuous landscape viewing
- CABLE / moving cross-river viewpoint
- WALK / branching close observation

### T4 Nearby Meaningful Scene
Shows at most 1–3 scene suggestions based on current stage, not all 13 Imprints.
Each suggestion must expose:
- WHY HERE
- WHAT YOU SEE FIRST
- PHONE LEVEL: FULL / LIGHT / OFF
- EXIT

### T5 Rest / Return Readiness
- nearest conceptual rest/recovery option
- direct Return action
- low-stamina mode

### T6 Continue Without Phone
One action hands off to paper map / signs / human service.

TODAY exit paths:
`ROUTE / SCENE / REST / RETURN / DIGITAL OFF`

---

## 3. ROUTE｜How to move through Qingjiang

ROUTE is the spatial backbone, not a game board.

### R1 Journey Overview
- ARRIVAL
- BOAT
- CABLE
- WALK network
- RETURN

### R2 Movement Mode
- BOAT
- CABLE
- WALK

### R3 Branch Decision
For WALK only:
- continue main relation
- choose branch
- skip content
- return

No route choice is unlocked by content completion.

### R4 Scene Density Overlay
Optional layer showing where meaningful scene content may occur.
It does not redefine route geometry.

### R5 Rest / Recovery Overlay
Shows rest/recovery logic separately from culture/game content.

### R6 Reality Overlay
NORMAL / DEGRADED / CLOSED / UNKNOWN changes presentation and allowed recommendations.

### R7 Return Overlay
Return remains reachable from every route state.

### R8 No-phone Handoff
- paper map
- physical wayfinding
- human service
- return recognition

ROUTE exits:
`CONTINUE / OPEN SCENE / REST / RETURN / PHONE OFF`

---

## 4. READ｜Thirteen Imprints as an optional content world

READ is no longer a flat 13-card library only. It has four internal ways to enter.

### D1 Nearby
Only Imprints relevant to the current journey stage.

### D2 By Question
- What am I looking at?
- What story belongs here?
- What can I compare?
- What should I simply feel?

### D3 By Mode
- CULTURE
- WISDOM
- PLAY
- WELLBEING

### D4 Full 13 Imprints Index
All R01–R13 remain visible and searchable, but equal listing does not imply equal spatial importance.

Each Imprint opens a **Scene Object** rather than a generic content card.

---

## 5. Scene Object｜the core unit of the App

Every meaningful scene follows the same object architecture.

### S0 Scene Identity
- Rxx ID
- canonical scene name
- current disposition: SCENE / READ / OBSERVE-BODY / HOLD
- truth/evidence state

### S1 FIRST READ｜look before screen
Answers: `游客看到什么？`
- one landscape/spatial cue
- no long text
- may explicitly instruct `先看，不用手机`

### S2 ORIENT｜where am I in the journey
Answers: `怎么走？`
- relation to BOAT/CABLE/WALK
- continue / branch / return
- no precise GPS claim required

### S3 OPTIONAL ACTION｜what can I do here
Answers: `怎么玩？`
Possible verbs:
`LOOK / FIND / COMPARE / LISTEN / REST / WRITE / REMEMBER`

No mandatory completion.

### S4 FEEDBACK｜what responds
Possible carriers:
- short UI reveal
- light
- sound
- graphic relation
- physical/sensory response
- no response when landscape itself is enough

### S5 DEPTH｜how far do I want to go
Audience and interest depth:
- family
- youth
- adult
- older / low-stamina

Depth changes explanation and action burden, never route access.

### S6 BODY / REST
Answers: `怎么休息？` and `实体设计怎么被身体使用？`
- stand / walk / lean / sit / touch / listen / stop
- use duration
- support relation
- exit posture

Only shown where relevant.

### S7 DIGITAL RETREAT
Answers: `手机什么时候退场？`
- FULL
- LIGHT
- OFF
- AUTO RETREAT after reveal

Examples:
- R01 CABLE moving view: LIGHT/OFF, no forced UI
- R05: LIGHT, short optional observation
- R06: OFF during viewing/rest → SHORT REVEAL → OFF/LIGHT
- R13: PLAY OFF / Digital OFF / Body + Return first

### S8 NO-PHONE
Answers: `没手机怎么成立？`
- what remains physically visible
- route/return fallback
- paper/sign/human support

### S9 EXIT
Every Scene must end explicitly:
- CONTINUE
- RETURN
- REST MORE
- SAVE TO MY BOOK
- PHONE OFF

A Scene without EXIT cannot enter MAIN.

---

## 6. MY BOOK｜personal journey, not completion system

MY BOOK has four internal layers.

### M1 Journey Trace
Relationship trace only:
- BOAT
- CABLE
- WALK
- selected stops
No GPS precision claim.

### M2 Saved Scenes
Only scenes the visitor deliberately saved.
No auto-collection of all R01–R13.

### M3 Recognition
Return-stage prompts:
- I recognize the river / two banks
- I recognize the cable direction
- I recognize a peak/scene I passed

### M4 Journal Page
- LOOK / LISTEN / REST / WRITE / REMEMBER
- one short note
- optional revisit
- paper/digital correspondence

### M5 Take Away
- digital personal Stone Book
- paper Qingjiang Journal
- selected memory artifact

No score, badge, medal, 13/13 completion, ranking, streak, or unlock tree.

---

## 7. SERVICE / RETURN｜parallel priority layer

Not a fifth bottom tab; it is globally reachable.

### SR1 Return Now
Dominant action when CLOSED / UNKNOWN / low stamina / late journey.

### SR2 Service
- official/onsite update placeholder
- human help
- weather / operation boundary

### SR3 No-phone minimum complete path
`paper map → physical direction → human service → return recognition`

### SR4 Digital OFF
The App may be fully closed without breaking the basic journey.

---

## 8. Cross-system state machine

### Journey state
`ARRIVAL → BOAT → CABLE → WALK → SCENE → REST → RETURN → EXIT`

### Reality state
`NORMAL / DEGRADED / CLOSED / UNKNOWN`

### Digital state
`FULL / LIGHT / OFF`

### Attention state
`ROUTE / LANDSCAPE / BODY / CONTENT / RETURN`

Recommended rule examples:
- ARRIVAL + UNKNOWN → ROUTE/RETURN first, FULL information allowed
- CABLE → LANDSCAPE first, LIGHT/OFF
- R05 → LANDSCAPE → optional PLAY LIGHT → EXIT
- R06 → LANDSCAPE/BODY → OFF → optional short WISDOM → OFF/LIGHT
- R13 → BODY/RETURN → OFF
- RETURN → ROUTE/RECOGNITION, LIGHT/FULL only when useful

---

## 9. Screen architecture

Persistent shell
├── TODAY
│   ├── Situation
│   ├── Next Move
│   ├── Journey Scale
│   ├── Nearby Scene
│   ├── Rest / Return
│   └── No-phone handoff
├── ROUTE
│   ├── Journey Overview
│   ├── Movement Mode
│   ├── Branch Decision
│   ├── Scene Density
│   ├── Rest Overlay
│   ├── Reality Overlay
│   ├── Return Overlay
│   └── No-phone Handoff
├── READ
│   ├── Nearby
│   ├── By Question
│   ├── By Mode
│   ├── Full 13 Index
│   └── Scene Object
│       ├── First Read
│       ├── Orient
│       ├── Optional Action
│       ├── Feedback
│       ├── Depth
│       ├── Body / Rest
│       ├── Digital Retreat
│       ├── No-phone
│       └── Exit
└── MY BOOK
    ├── Journey Trace
    ├── Saved Scenes
    ├── Recognition
    ├── Journal Page
    └── Take Away

Parallel priority layer:
`SERVICE / RETURN / DIGITAL SILENCE`

---

## 10. No-loss statement

This architecture does not delete the v1.2/v1.3 capabilities. It expands their internal product logic. Existing TODAY / ROUTE / READ / MY BOOK remain as the four public anchors because they already map to the visitor journey; the architecture deepening occurs below and across them.

`NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`

Truth boundary remains:
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.
