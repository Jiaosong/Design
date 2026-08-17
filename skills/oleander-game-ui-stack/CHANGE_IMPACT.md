# OLEANDER Game UI Stack — Change Impact

Status: `CANDIDATE / REVIEW REQUIRED`

## Scope
Adds five UI-specialist candidate skills:
- `oleander-game-ui`
- `oleander-mobile-game-ui`
- `oleander-ui-visual-composition`
- `oleander-route-wayfinding-ui`
- `oleander-ui-interaction`

No existing skill is deleted, renamed, superseded, or promoted by this change.

## Problem addressed
Existing OLEANDER skills covered motion, story, delivery, research, data visualization, and 3D well, but game-facing UI review repeatedly fell back to generic frontend/app heuristics. This stack adds explicit gates for:
- game interface vs dashboard distinction;
- world/HUD hierarchy;
- mobile game touch ergonomics;
- route/wayfinding source translation;
- first-visual UI composition;
- state-machine / focus / interruption / Return behavior.

## Authority impact
None. These skills consume Current Authority; they do not create project facts or project-state authority.

External GitHub/UI sources are treated as reference evidence and distilled practice, not as OLEANDER Current Authority.

## Existing systems affected
### Extended, not replaced
- Existing Mature Design First
- First Visual Gate
- `oleander-motion`
- `oleander-story-and-board`
- `oleander-delivery-qc`
- independent review / no-self-evaluation
- no-loss / no-compression

### Explicit non-impact
- project taxonomy and L0–L7 semantics;
- FIELD / G1F / NO_PROMOTION boundaries;
- 3D/data/research workflows;
- C04 product authority;
- route source facts;
- rights policy.

## Regression risks
1. **Method inflation** — adding too many mandatory steps could slow production.
   - Mitigation: use routing; invoke only relevant skills, not all five by default.
2. **Game-style overreach** — generic game conventions could overwrite project identity.
   - Mitigation: Existing Mature Design and project specificity precede game patterns.
3. **Gamification pollution** — game UI could be misread as permission for XP/rewards/tasks.
   - Mitigation: `oleander-game-ui` explicitly forbids unauthorized reward/completion systems.
4. **Mobile simplification loss** — responsive work could delete information.
   - Mitigation: no-loss rule; recompose/progressively disclose rather than delete.
5. **Route authority pollution** — designed route could be mistaken for factual geometry.
   - Mitigation: route skill separates source topology from relational translation and truth boundaries.
6. **Self-review leakage** — producer could use skill checklist to declare MAIN.
   - Mitigation: every skill requires independent final verdict and forbids producer numeric scoring.

## Promotion requirements
- schema/frontmatter validation;
- execute `GOLDEN_CASES.md`;
- compare against prior OLEANDER review output on a real UI object;
- verify no contradiction with current governance;
- independent review of findings quality;
- explicit promotion transition after review.

Merge, file existence, or CI green do not equal promotion.