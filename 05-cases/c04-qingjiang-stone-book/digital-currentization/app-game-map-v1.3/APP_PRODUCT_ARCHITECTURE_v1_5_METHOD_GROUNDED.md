# C04｜Qingjiang Thirteen Imprints App Product Architecture v1.5

State: `METHOD-GROUNDED ARCHITECTURE / COMPARISON CANDIDATE / FIELD OPEN / NO_PROMOTION`

This supersedes `APP_ARCHITECTURE_v1_4` as the active App-architecture study. v1.4 is retained as `REVISE / PROVENANCE` because it expanded functions before sufficiently reframing the user relation and comparison question.

## 0｜Method authority consumed

This App architecture applies existing OLEANDER design method rather than inventing a standalone UX system:

- `READ → LOCATE → TRANSLATE → FORM → TEST → REVISE`
- `Reading Unit / Hierarchy / Rhythm / Relation / Geometry`
- one screen = one central judgment
- visual responsibility: `L0 Identity / L1 Central Judgment / L2 Relation-Body / L3 Evidence-Meta / L4 Continuation`
- mobile 4-column digital grid; Reading / Evidence / Field zones have separate responsibilities
- valid participation changes visible content, judgment, later record, role or next system state; click/view/collect alone is not sufficient
- user may skip, leave UNKNOWN, revise later; no completion penalty
- `SERVICE / RETURN > ROUTE > OBSERVATION > EXPLANATION > MEMORY > SHARE`
- `NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`

---

# 1｜READ — user relationship, not feature list

## 1.1 Product role

The App is not the Qingjiang experience and not the owner of the route.

Its role is:

> **a context-sensitive travel companion that appears only when a visitor needs to make a decision, understand one meaningful relation, recover/return, or preserve a chosen memory.**

The App must be able to disappear without breaking the journey.

## 1.2 Actors

- Visitor
- Real Qingjiang landscape
- Route / transport / return system
- Thirteen Imprints content
- Physical / sensory design
- Human service / official update
- Paper map / Qingjiang Journal
- Digital App

## 1.3 Original relation

The visitor moves through a real river / cable / walking journey. Landscape, route, body and service already exist before the App.

## 1.4 Relationship break in v1.2–v1.4

The prototype is functionally complete but still reads too much like an App product:

1. four equal bottom tabs imply that all four domains deserve equal attention at all times;
2. card grids and filters make Thirteen Imprints feel like a content catalogue;
3. reality/delivery states exist as controls, but do not fully restructure the first read of each screen;
4. no-phone is described as fallback rather than designed as a parallel path for every critical user job;
5. My Book can be opened as a feature before memory has been earned by an actual user action or recognition;
6. scene detail explains too much before the user has looked, moved or acted;
7. route, content and memory are feature areas instead of consequences of one continuous visitor journey;
8. visual hierarchy is too card-heavy and equal-weight, risking dashboard / scenic-app first read.

## 1.5 Intended relation

`real scene / route / body state`
→ `visitor notices a need or question`
→ `App appears at the minimum useful depth`
→ `visitor makes one decision or one meaningful action`
→ `App reveals only the next necessary layer`
→ `visitor continues / rests / returns / closes phone`
→ `only selected changes or memories may enter My Book`

The App therefore behaves as an **attention regulator**, not a content broadcaster.

---

# 2｜LOCATE — seven real user jobs

The architecture is organized by user jobs first. Existing features are mapped into them later.

## J01｜ORIENT
**Question:** 我现在处在这趟游程的什么位置？

Need:
- current journey phase
- movement mode
- route / return relation
- reality state

Must not require:
- GPS precision
- reading Thirteen Imprints
- task completion

## J02｜DECIDE NEXT MOVE
**Question:** 我下一步应该继续、分支、休息还是回来？

Possible outputs:
- CONTINUE
- CHOOSE BRANCH
- REST
- RETURN
- PHONE OFF

One screen must not present all possibilities with equal weight; one dominant next decision is required.

## J03｜NOTICE
**Question:** 这里有什么值得我真正看一眼？

The first answer must come from landscape / spatial / body evidence, not a paragraph.

Output:
- one visible relation / one question
- optional deeper entry

## J04｜ENGAGE
**Question:** 如果我愿意参与，我具体做什么？

Valid verbs:
- LOOK
- FIND
- COMPARE
- LISTEN
- REST
- WRITE
- REMEMBER

A valid action must change at least one later state:
- next reveal
- comparison
- personal judgment
- memory record
- route/rest decision

## J05｜RECOVER
**Question:** 我累了、想停、想减少信息时怎么办？

Need:
- rest / lean / stop / sit / quiet viewing
- low-stamina default
- information reduction
- return readiness

## J06｜RETURN
**Question:** 我怎样安全、清楚地结束探索并回来？

Return owns priority over new content.

Need:
- main return relation
- CLOSED / UNKNOWN fail-closed behavior
- paper / sign / human path
- no completion gate

## J07｜REMEMBER
**Question:** 哪一部分真的值得我带走？

Memory must be caused by recognition / action / changed judgment, not by automatic collection.

Possible outputs:
- one chosen scene
- one observation
- one changed judgment
- one revisit intention
- paper journal correspondence

---

# 3｜TRANSLATE — product principles

## P01｜CONTEXT BEFORE NAVIGATION
Bottom navigation is access infrastructure, not the product architecture.
The dominant screen changes according to journey state.

## P02｜ONE READING UNIT / ONE DECISION
Every screen owns one central question or judgment.
No screen should simultaneously be route dashboard + culture catalogue + service panel + memory prompt.

## P03｜FIELD FIRST
When the visitor is at a scene, the first read is landscape / route / body.
UI cannot visually out-rank Qingjiang.

## P04｜PROGRESSIVE REVEAL
Do not explain first.
Default sequence:
`LOOK → ACT/COMPARE → REVEAL → DECIDE → EXIT`.

## P05｜PARTICIPATION MUST HAVE CONSEQUENCE
A tap is not participation.
If an action does not change what is revealed, recorded, compared or decided, it remains passive content.

## P06｜UNKNOWN IS VALID
Visitors can choose:
- 不确定
- 先跳过
- 以后再看
- 只看景观

No penalty and no completion debt.

## P07｜RETURN ALWAYS WINS
When reality state, stamina or context requires it, Return replaces content as L1 Central Judgment.

## P08｜EVERY DIGITAL JOB HAS A NO-PHONE SHADOW
Critical user jobs must remain possible through physical / paper / human means.

## P09｜MEMORY IS AN OUTCOME, NOT A TAB FEATURE
My Book is visible as a destination but only becomes meaningful after a user-selected observation, recognition or note.

## P10｜EVIDENCE DOES NOT OWN FIRST READ
Evidence/status/version live in L3 and can be expanded; they never compete with L1 scene or route judgment.

---

# 4｜FORM — compare three architecture candidates

Locked variables across all candidates:
- R01–R13 canonical identities
- BOAT / CABLE / WALK real journey logic
- Service / Return priority
- NORMAL / DEGRADED / CLOSED / UNKNOWN
- FULL / LIGHT / OFF
- offline / no-GPS / no-phone principles
- existing content modes and audience-depth content
- My Book local memory concept
- project visual tokens

Changed variable:
**primary information architecture and reading order only**.

## Candidate A｜TABS-FIRST / current family

Primary access:
`TODAY / ROUTE / READ / MY BOOK`

Strength:
- easy to understand as a conventional app
- all existing capabilities remain visible

Failure risk:
- product reads as four feature departments
- phone remains mentally present throughout journey
- READ becomes catalogue
- MY BOOK appears before memory consequence

Status: `CONTROL / NOT RECOMMENDED AS FINAL ARCHITECTURE`

## Candidate B｜JOURNEY-STATE-FIRST / recommended

Primary state spine:
`ENTER → MOVE → NOTICE → ENGAGE / SKIP → RECOVER → RETURN → RECOGNIZE → REMEMBER`

The App shell exposes only the current phase plus global Return / Service.
TODAY / ROUTE / THIRTEEN IMPRINTS / MY BOOK become **capability drawers / destinations**, not equal cognitive departments.

Strength:
- directly matches real visitor journey
- phone can appear and retreat naturally
- route/body/return can dominate when needed
- Scene Interaction and Memory become consequences of context

Risk:
- requires stronger state design and transition clarity
- must avoid fake “automatic context awareness” without GPS/field data

Mitigation:
- phase can be selected manually from visible journey anchors
- no precise location inference is claimed

Status: `PRIMARY CANDIDATE`

## Candidate C｜MAP-FIRST

Primary access:
`Journey Map → Branch / Scene / Rest / Return → Detail`

Strength:
- spatial relation is always clear
- strong fit with BOAT / CABLE / WALK and multi-branch route

Failure risk:
- turns all content into map POIs
- risks 13 Imprints becoming 13 markers
- memory and body states become secondary
- map may visually replace landscape

Status: `SUPPORTING REFERENCE / NOT PRIMARY`

### Decision
Proceed with Candidate B as the **working product architecture**, while preserving Candidate C map logic inside MOVE/ORIENT and preserving Candidate A four anchors as secondary access if testing proves useful.

This is a design decision, not a locked final state.

---

# 5｜Working product architecture — Journey-State-First

## Global Shell
Persistent but visually quiet:
- project identity / current journey phase
- Reality State only when relevant
- Return / Service
- Digital level FULL / LIGHT / OFF
- explicit `手机退场`

The shell must never become a dashboard.

## PHASE 01｜ENTER / 出发与进入

### User goal
知道这趟清江怎么开始，以及怎么回来。

### L1 Central Judgment
`今天先怎么进入清江？`

### Primary content
- BOAT / CABLE / WALK relationship
- return readiness
- reality state

### Primary actions
- `看游程`
- `无手机继续`

### Exit
`MOVE`

No 13-Imprint cards on first read.

---

## PHASE 02｜MOVE / 移动与判断

### User goal
知道现在应该继续、分支、休息还是返回。

### L1 Central Judgment
One of:
- `继续向前`
- `这里需要选择分支`
- `先休息`
- `建议返回`

### Field Zone
- relation map / movement mode
- no fake GPS cursor

### L2 actions
At most:
- one primary movement action
- one secondary option
- Return escape

### Scene markers
Subordinate; show only meaningful nearby/next scenes, not all R01–R13 at equal weight.

---

## PHASE 03｜NOTICE / 先看

### User goal
在拿手机之前先看真实场景。

### L1 Central Judgment
One scene-specific question only.

Examples:
- R05: `整片峰林里，你最先认出的是什么？`
- R06: `江、两岸、坡面和步道，彼此在哪里？`
- R13: no play question before passage; `先通过 / 看光 / 确认返回`.

### UI behavior
- Field Zone dominates
- most controls hidden
- `先看` can explicitly switch to OFF/LIGHT

### Exit
- `继续看`
- `跳过内容`
- `RETURN`

---

## PHASE 04｜ENGAGE / 选择参与

Only appears if the scene has a valid interaction and the visitor opts in.

### L1 Central Judgment
One action verb.

Examples:
- FIND one relation
- COMPARE two visible cues
- LISTEN
- REST

### Rule
User input must alter the next reveal or record.

Bad pattern:
`点一下 → 播放固定说明`

Valid pattern:
`先选择/描述/比较 → 系统只展示与该选择有关的最小解释 → 用户可修订/保持未知`.

### Exit
- `我改变了判断`
- `没有改变`
- `仍不确定`
- `不继续`

---

## PHASE 05｜REVEAL / 最小解释

Not every scene requires this phase.

### L1 Central Judgment
`什么信息真正改变了刚才的判断？`

### Reading Zone
minimal explanation only.

### Evidence Zone
- source / status / uncertainty
- expandable, secondary

### Interaction
visitor can mark:
- changed
- unchanged
- unknown

This determines whether a memory/judgment record is offered.

---

## PHASE 06｜RECOVER / 身体与休息

This phase is not a content screen.

### Trigger
- visitor chooses rest
- low-stamina profile
- R06 / rest-related scene
- context recommends reduced information

### L1 Central Judgment
`先停下来，还是继续？`

### Body relation
- stand / lean / sit / stop / listen / look
- duration is not gamified

### Digital behavior
OFF or LIGHT by default.

### Exit
- continue
- remain
- return

---

## PHASE 07｜RETURN / 回来

### Trigger
- user chooses Return
- CLOSED / UNKNOWN requires fail-closed response
- low stamina
- journey ending

### L1 Central Judgment
`现在先回来。`

### Field / route
- main return relation
- service/paper/human fallback

### Content behavior
- Thirteen Imprints disappear from first read
- no new game/content recommendation

### Exit
`RECOGNIZE` or real-world exit.

---

## PHASE 08｜RECOGNIZE / 回程再看一次

### User goal
把刚刚经过的空间关系重新认出来。

### L1 Central Judgment
`回来时，你现在认出了什么？`

Possible outputs:
- river / two banks
- cable direction
- one scene / peak
- one route relation
- `没有特别记住`

This is a valid user input, not a quiz.

### Consequence
Only selected recognition may be offered to My Book.

---

## PHASE 09｜REMEMBER / 带走

### L1 Central Judgment
`哪一部分值得留下？`

### Inputs
- recognition from Return
- one changed judgment
- one chosen scene
- one short note
- revisit intention

### Outputs
- My Book page
- Qingjiang Journal correspondence

No auto-collection, score, completion percentage or medal.

---

# 6｜Secondary capability architecture

These capabilities remain complete but no longer dictate the main journey reading order.

## CAP-ROUTE
- journey overview
- BOAT / CABLE / WALK
- branch relation
- rest overlay
- reality state
- return overlay
- paper/no-phone handoff

## CAP-IMPRINTS
- nearby meaningful Imprints
- by question
- by content mode
- complete R01–R13 index
- canonical scene detail

The full index is an archive/library view, not the default field experience.

## CAP-BOOK
- today trace
- saved scenes
- changed/unknown judgments
- recognition
- journal notes
- revisit

## CAP-SERVICE
- Return now
- human service
- paper map
- offline/no-phone
- current operator/field status placeholder with explicit evidence boundary

---

# 7｜Object model — product structure, not page inventory

## JourneySession
- phase
- movement mode
- reality state
- digital state
- user depth profile
- return state

## TravelLeg
- ARRIVAL / BOAT / CABLE / WALK / RETURN
- relation to next decision point
- no measured distance claim unless authority exists

## DecisionPoint
- one central decision
- primary action
- secondary action
- escape / return

## Scene
- canonical Rxx identity
- disposition: SCENE / READ / OBSERVE-BODY / HOLD
- first-read question
- valid actions
- reveal contract
- digital retreat contract
- no-phone counterpart
- exit contract

## Observation
- user's own selection / wording / comparison
- may remain UNKNOWN
- may be revised

## RecoveryState
- body need
- reduce-information state
- continue / remain / return

## MemoryPage
- selected recognition / observation / changed judgment
- note
- revisit
- paper correspondence

This object model is more important than a long list of screens.

---

# 8｜Visual hierarchy contract

## L0 Identity
Quiet persistent anchor only.
Must not compete with Qingjiang or route decision.

## L1 Central Judgment
Exactly one per screen/state.
Largest semantic weight.

## L2 Relation / Body
Map relation, landscape cue, body action, comparison, scene relation.
This is the main operational layer.

## L3 Evidence / Meta
Reality state, source, version, evidence boundary, explanatory status.
Always secondary and expandable.

## L4 Continuation
`继续 / 跳过 / 休息 / 返回 / 手机退场 / 记下来`
One clear continuation line, not a second headline.

### Mobile grid
- 390 reference
- 4 columns
- 12 gutter
- 20 side margin

### Reading zones
- **Field Zone:** landscape / map / relation; may span full width
- **Reading Zone:** one question + minimal text
- **Evidence Zone:** source/status; visually quieter

### Anti-patterns to remove
- equal-weight card walls
- four or more pills competing at first read
- dense filter bars before scene context
- decorative lines with no semantic responsibility
- Signal red used as generic accent
- persistent progress/collection indicators

---

# 9｜Interaction grammar

Every interaction must declare:

`USER INTENT → ACTION → SYSTEM RESPONSE → USER CONSEQUENCE → EXIT`

## Pattern A｜Observe → Reveal
`look / choose one cue → minimal relation reveal → changed / unchanged / unknown → exit`

## Pattern B｜Compare
`select A/B visible relation → compare → optional explanation → revise or keep judgment`

## Pattern C｜Rest
`choose rest → UI reduces → body support / quiet field → continue or return`

## Pattern D｜Return
`return intent → all nonessential content retracts → route/service dominates → recognition after safe return stage`

## Pattern E｜Memory
`recognition / changed judgment → deliberate save → one page`

No pattern may require completion before route or Return.

---

# 10｜Audience depth — behavior, not persona decoration

Audience profiles change default depth and burden, not access rights.

## Family
- simpler shared observation
- find / compare / listen
- no score or race

## Youth
- optional comparison / photography / light inference
- more self-directed depth

## Adult
- culture / landform / evidence deep read available

## Older / Low-stamina
- Recovery / Service / Return promoted
- larger/shorter content
- interactions default optional/off

Same Scene object remains canonical; only default depth and continuation change.

---

# 11｜No-phone shadow architecture

Every critical digital job has a non-digital counterpart:

| User job | Digital | No-phone shadow |
|---|---|---|
| Orient | journey relation map | paper map / physical map / human service |
| Decide next move | route decision | signs / route geometry / staff |
| Notice | scene prompt | landscape itself / optional physical prompt |
| Engage | short optional interaction | physical/sensory action or no interaction |
| Recover | rest cue | actual rest/support condition |
| Return | return relation | physical direction / human service |
| Remember | My Book | Qingjiang Journal / personal memory |

If a row has no no-phone shadow, the digital feature cannot own a critical journey function.

---

# 12｜Prototype test contract

Do not validate by asking whether users “like the App”.

## Scenario S1｜First arrival
Success signs:
- understands how to start
- sees Return/service early
- does not interpret thirteen Imprints as mandatory checkpoints

Failure signs:
- sees a scenic-app dashboard
- first question is “which points should I collect?”

## S2｜Cable movement / R01 carrier
Success:
- screen retreats
- visitor can understand movement without opening content

Failure:
- long reading or required action appears during moving view

## S3｜R05
Success:
- landscape first
- optional action changes the reveal or record
- visitor can skip without debt

Failure:
- interaction becomes find-and-score game

## S4｜R06 / low stamina
Success:
- rest / Service / Return appears before deep explanation
- Digital OFF/LIGHT feels intentional

Failure:
- content demands attention while user is recovering

## S5｜R13
Success:
- PLAY OFF
- body / route / return dominates

Failure:
- task, timer, collection or long explanation appears in narrow passage

## S6｜UNKNOWN / CLOSED
Success:
- visually not read as normal-open
- Return/service dominates

Failure:
- same map visual hierarchy as NORMAL

## S7｜No-phone
Success:
- basic journey still makes sense after phone is closed

Failure:
- route, return or required scene information becomes unavailable

## S8｜Return → Memory
Success:
- memory is caused by recognition or changed judgment

Failure:
- app automatically rewards/collects everything visited

---

# 13｜Decision and current gaps

## KEEP
- four existing capabilities: Today / Route / Thirteen Imprints / My Book
- Service / Return permanent reachability
- R01–R13 complete optional system
- audience-depth content
- offline / local memory / print fallback
- FULL / LIGHT / OFF and reality states

## REFRAME
- four bottom tabs: from equal product architecture → secondary capability access
- TODAY: from dashboard → current journey decision
- READ: from catalogue → scene-context entry + optional full index
- MY BOOK: from feature destination → consequence of recognition/changed judgment
- state controls: from demo toolbar → hierarchy-changing context

## ADD
- journey-state spine
- DecisionPoint object
- observation/unknown/revision state
- explicit screen L0–L4 contract
- no-phone shadow mapping per user job
- test scenarios based on failure signs

## CUT / DEMOTE
- equal-weight card walls in first read
- generic filter-first interaction
- interactions with no downstream consequence
- progress metaphors / collection language
- visual controls that exist only to show system completeness

---

# 14｜Truth / promotion boundary

This architecture does not claim:
- live location
- live operations
- measured route geometry
- field validation
- safety validation
- user-test PASS
- final visual PASS

Truth boundary:
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`.

Design state:
`CANDIDATE ARCHITECTURE / NEEDS PROTOTYPE + VISUAL QA + USER-SCENARIO TEST`.
