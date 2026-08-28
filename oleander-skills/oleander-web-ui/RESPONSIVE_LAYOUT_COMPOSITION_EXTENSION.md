# OLEANDER Responsive Layout Composition Extension

Status: `CANDIDATE EXTENSION / WEB-UI`

Use when a content hierarchy must survive multiple viewport/container sizes, loading states and content lengths without collapsing into proportional shrinkage or generic device templates.

## Core principle

`PRIORITY HIERARCHY → CONTENT / MEDIA CONSTRAINTS → SCAN PATTERN → SPATIAL SKELETON → CONTENT-BREAK POINTS → REFLOW RULES → STATE FOOTPRINT → ACTUAL MULTI-VIEWPORT READBACK`.

Layout is the spatial expression of task and content priority. It should be derived from what must remain visible and usable, not from a favourite grid or marketed device width.

## Hierarchy handoff

Before composition, resolve:

- primary task/claim/object;
- secondary support;
- tertiary/deep detail;
- required actions and recovery path;
- fixed-format objects such as maps, charts, models, tables, media or technical drawings;
- protected claim-bearing regions in media;
- high-risk long strings, localization or bilingual content;
- loading/empty/error/unknown/closed states when relevant.

If hierarchy is unresolved, return upstream. Layout cannot repair an undefined priority model.

## Scan-pattern decision

Choose the spatial reading model from the content relation, not by aesthetic habit. Possible structures include:

- linear reading / single-column;
- master-detail;
- persistent context + main content;
- table/data-first;
- peer grid/gallery;
- comparison matrix;
- sequenced step/flow;
- sticky media + evolving explanation;
- asymmetric editorial composition;
- spatial/map-led composition.

These are relation types, not templates. A project may use a hybrid when the content requires it.

## Content-driven breakpoints

Breakpoints should occur when a real relationship stops working, for example:

- a readable measure collapses;
- a technical drawing annotation becomes illegible;
- a table can no longer preserve essential columns;
- two evidence objects lose their intended comparison relation;
- an image crop starts removing protected evidence;
- a navigation/action row wraps or changes priority;
- a model/map becomes too small for the required interaction.

Named device widths are useful test targets, not design authority.

## Reflow contract

For each material breakpoint/container condition, explicitly decide what:

- stacks;
- collapses;
- pins/stays reachable;
- moves earlier/later;
- becomes scrollable;
- moves behind disclosure;
- changes crop/aspect;
- changes type tier;
- remains fixed because its relation is authoritative.

Preserve semantic/interaction order. A visually attractive mobile rearrangement that makes keyboard/focus order or Return/recovery confusing is not acceptable.

## Spatial stability

Reserve stable geometry where unexpected movement would damage comprehension or control:

- images/video with known aspect ratios;
- chart/map/model regions;
- tables and comparison rows;
- toolbars/action bars;
- loading skeletons;
- expandable regions where the displacement is intentional and legible.

Do not treat all layout shift as identical. Intentional content reveal may move content; accidental reflow caused by missing dimensions, font swaps or late-loading media is a defect.

## State-footprint gate

Review loaded, loading, empty, error, partial and unavailable states in the same structural region. The hierarchy should remain understandable even when the primary content is absent.

Empty/error states are part of composition: they must preserve orientation, next action and recovery rather than collapsing the page into an unrelated centered message.

## Responsive media

Media should respond by role rather than by generic `width:100%` alone.

Resolve:

- crop versus contain;
- protected evidence region;
- minimum useful size;
- focal-point shift;
- alternate mobile derivative when justified;
- overflow/zoom/pan when information density cannot be safely reduced;
- captions/legends/source notes and their reading order.

Do not distort authoritative maps, drawings, charts, logos or product geometry to fit a grid.

## Actual readback

At minimum test the project-required desktop and narrow/mobile conditions, plus intermediate widths around actual break points. Attack:

- longest labels/headlines;
- language expansion;
- loading → loaded transition;
- empty/error state;
- hover/focus/active changes;
- image/model/map aspect changes;
- browser zoom or text enlargement when relevant;
- keyboard focus order after reflow.

Record the breakpoint reason and the rendered defect it prevents.

## Failure modes

Reject or revise when:

- mobile is only a scaled desktop;
- breakpoints exist only because a framework names `sm/md/lg`;
- primary content moves below decorative support on narrow screens;
- authoritative geometry is stretched to satisfy the grid;
- loaded and loading states cause avoidable large layout jumps;
- a desktop two-column relation stacks on mobile in an order that reverses meaning;
- a media object becomes too small to perform its evidence/interaction role;
- a layout passes at three canonical screenshots but fails around the actual content break point;
- responsive correctness is inferred from CSS source without rendered verification.

## Boundary

This extension does not impose universal breakpoint widths, grid column counts, character measures or device classes. Those are project-derived and must be tested against real content.

External study provenance: `jacob-balslev/skill-graph` layout-composition (repository license Apache-2.0; independently reformulated here).