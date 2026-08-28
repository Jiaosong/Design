# OLEANDER Motion Art Direction & Choreography Extension

Status: `CANDIDATE EXTENSION`

Use when motion must carry a repeatable project/brand character or coordinate multiple elements, layers or narrative beats beyond a single state transition.

## Authority order

OLEANDER Motion Role remains first:

`STATE / INFORMATION CHANGE → MOTION ROLE → NO-MOTION BASELINE → TEMPORAL CHARACTER → CHOREOGRAPHY → TIMING / EASING → REDUCED MOTION → RUNTIME REVIEW`.

Do not start from a personality preset, easing curve or showcase effect and search for somewhere to use it.

## Temporal character

Before assigning detailed parameters, describe the intended temporal character in project-specific language. Examples may include restrained, decisive, elastic, ceremonial, mechanical, soft, abrupt, suspended or weighty.

The description must connect to at least one real carrier:

- interaction frequency and urgency;
- object/material behavior;
- brand/visual identity;
- narrative beat;
- spatial relationship;
- user-control expectation;
- data/state semantics.

`TEMPORAL CHARACTER ≠ CLAIMED USER EMOTION`.

An intended emotional tone is a design hypothesis unless tested. Do not present generic emotion/color tables as psychological fact.

## Project-level motion grammar

For systems that use motion repeatedly, define a compact grammar instead of tuning every animation independently:

1. **Timing palette** — a small set of quick / standard / deliberate durations or physics bands, calibrated in the actual runtime.
2. **Easing / velocity family** — one dominant family plus explicitly justified exceptions.
3. **Entrance / exit logic** — where objects come from, how they settle and how departures differ.
4. **Continuity rule** — how shared objects, camera or spatial context preserve origin/destination understanding.
5. **Emphasis rule** — which state changes may earn stronger displacement, scale, contrast or temporal delay.
6. **Ambient rule** — whether continuous motion exists at all, and its stop/pause/reduced-motion behavior.

Reuse the grammar for similar interactions. Same semantic action should not receive arbitrarily different timing merely for novelty.

## Choreography hierarchy

When several objects respond to one event, assign roles before keyframes:

- **Primary** — the object/state change that must be understood first.
- **Supporting** — motion that clarifies attachment, cause, hierarchy or continuity.
- **Ambient** — optional background motion that carries atmosphere without stealing task attention.

Supporting or ambient layers are not mandatory. Remove any layer without an identifiable role.

Use this sequence:

`TRIGGER → PRIMARY CHANGE → SUPPORT RESPONSE → SETTLE / READ WINDOW → NEXT EVENT`.

A short still/read window may be more useful than continuously filling the scene with motion.

## Coordination rules

- Lead with the semantic focal object, not automatically the largest graphic object.
- Use spatial origin/direction consistently when the objects belong to one causal event.
- Stagger according to reading/causal order rather than decorative cascade.
- Limit simultaneous high-salience motion; concurrency is an attention budget, not a fixed percentage rule.
- Counter-motion is optional and must explain depth, inertia, camera/object relation or balance; decorative opposite-direction drift is not automatically useful.
- Children/following parts may settle after the parent when that delay communicates attachment or mass.
- If a sequence feels busy, reduce concurrent motion, displacement, frequency or layers before adding longer duration.

## Material / weight translation

Physical metaphors can inform motion, but they are not universal presets. When using weight, elasticity, fluidity or inertia:

- identify the source analogy or real object behavior;
- translate it into velocity, damping, overshoot, path, secondary lag or deformation;
- test whether the metaphor improves comprehension/identity in context;
- avoid fake physics that conflicts with the represented product/material.

## Responsive / platform adaptation

Do not scale desktop choreography proportionally onto smaller or lower-performance contexts.

For each target environment decide:

- number of simultaneous moving objects;
- maximum displacement and camera motion;
- hover-dependent behaviors versus touch equivalents;
- parallax/3D necessity;
- runtime/GPU/bundle cost;
- user-control and interruption behavior;
- reduced-motion equivalent.

Mobile or constrained contexts usually require fewer motion carriers and shorter spatial travel, but actual parameters must be verified in the target runtime rather than copied from a universal table.

## Motion-density review

At real playback speed, inspect:

- what the eye follows first;
- whether two high-salience motions compete;
- whether the primary state can be understood before the next event begins;
- whether stagger reflects reading/causal order;
- whether ambient motion remains peripheral;
- whether repeated use becomes tiring or delays expert users;
- whether rapid repeat/interruption/reversal preserves the same hierarchy;
- whether Reduced Motion keeps equivalent state and information.

## Output

When this extension is active, record:

- motion role;
- temporal-character statement and evidence basis;
- timing/easing/physics grammar;
- primary/supporting/ambient ownership;
- choreography/event order;
- target platform adaptations;
- no-motion and reduced-motion path;
- runtime evidence and observed attention conflicts;
- Keep / Reduce / Remove decision.

## Candidate boundary

This extension governs temporal art direction and coordination. It does not prove user emotion, brand perception or usability improvement without appropriate testing. Fixed duration/easing examples from external references remain heuristics, not OLEANDER truth.