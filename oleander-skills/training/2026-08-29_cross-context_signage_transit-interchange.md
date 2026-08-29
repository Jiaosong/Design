# Cross-context Practice — Physical Signage / Environmental Graphics — Transit Interchange

Status: `CROSS_CONTEXT_EVIDENCE / CONTROLLED PRACTICE / NO_PROJECT_USAGE / NO_PROMOTION`

## Why this context is materially different

Batch-4 `SK-VIS-009` attacks a museum/park family. This practice uses a fictional rail/bus interchange with fast-moving transfer decisions, multiple approach directions, service information and reverse/Return routes. The wayfinding problem is operational and time-sensitive rather than interpretive.

## Second-source cross-check

Transport for London Streetscape Guidance and Legible London material were used as bounded professional cross-checks. TfL explicitly treats pedestrian wayfinding as a connected system and places signs at pedestrian journey starts, key decision points and landmark destinations while minimizing unnecessary street clutter.

Sources:
- `https://content.tfl.gov.uk/streetscape-guidance-2022-revision-2.pdf`
- `https://content.tfl.gov.uk/ll-yellow-book.pdf`

Rights boundary: no TfL map graphics, roundel, color palette, typeface, sign dimensions, proprietary artwork or sign manual specification is copied. This practice transfers sequencing/placement logic only.

## Synthetic interchange

A fictional interchange contains:
- concourse C0;
- rail platforms P1/P2;
- bus exit B;
- street exit S;
- accessible lift route L;
- ticket/help point H.

Approach A enters C0 from rail platform P1. Approach B enters C0 from street exit S. Both must reach B without using the same initial sightline. There is one ambiguous junction J1 before the bus corridor and one confirmation point K1 after the turn.

## Approach-direction map

`A: P1 → C0 → J1 → K1 → B`

`B: S → C0 → J1 → K1 → B`

`RETURN A: B → K1 → J1 → C0 → P1`

`RETURN B: B → K1 → J1 → C0 → S`

The reverse paths are explicitly retained because a one-way outbound sign family does not prove recovery.

## Decision-point ledger

| Node | Approach | Decision required | Information must appear | Carrier role | Failure attack |
|---|---|---|---|---|---|
| C0-A | from P1 | establish bus vs street/help directions | before passenger commits to wrong concourse edge | orientation + directional | crowd occludes low carrier |
| C0-B | from S | find bus transfer without assuming rail knowledge | immediately after entry | orientation + directional | map orientation conflicts with body heading |
| J1-A | from rail side | choose bus corridor vs lift/help branch | before physical split | directional | sign placed after split |
| J1-B | from street side | choose same destination from reverse visual field | before split | directional | one-sided sign face invisible |
| K1 | both | confirm bus corridor choice | after turn, before next ambiguity | confirmation | no confirmation creates uncertainty/backtracking |
| B | arrival | identify bus interchange and local bay information | at destination | identification + local information | arrival sign competes with service data |

## Progressive disclosure

- **C0:** only major destination families + immediate accessible alternative; no platform-level bus detail yet.
- **J1:** current choice only; low-priority narrative/branding removed from decision surface.
- **K1:** short confirmation plus remaining path cue.
- **B:** detailed bus/local information appears after destination recognition.

This preserves `RIGHT INFORMATION / RIGHT PLACE / RIGHT STAGE` without importing TfL's visual identity.

## Redundant cue contract

Bus destination is not encoded by color alone. Candidate redundancy:
- stable destination name `Bus interchange`;
- directional arrow at J1;
- repeated destination naming at K1;
- optional pictogram only if incumbent symbol authority exists;
- spatial landmark/architectural cue may support but not replace the sign.

## Situated-map attack

At C0-B, a north-up map could be technically correct but cognitively reversed relative to the viewer. The map gate therefore records:
- map orientation convention;
- actual viewer facing direction;
- `YOU ARE HERE` location;
- visible landmark/path correspondence;
- label parity with physical signs.

If a rotated heads-up map is chosen, the rotation is a presentation transform only; base route geometry remains authoritative.

## Operational-state boundary

Static signage must not imply live platform/bus status. Any dynamic disruption/service state is owned by the current operational-information system. Physical direction carriers may route to an alternate path only when that state source is authoritative and the sign implementation actually supports change.

## Readback verdict

**KEEP as cross-context evidence:** decision-before-commitment, confirmation after turn, reverse-path recovery and situated-map checks remain valid under faster transit conditions.

**Material delta:** explicitly distinguish `JOURNEY START / DECISION / CONFIRMATION / DESTINATION` as sequencing states when the environment involves repeated transfers. These are functional stages, not a mandatory four-sign visual taxonomy.

**REJECT:** TfL colors/type/roundel/map appearance or any fixed spacing/dimension as OLEANDER default.

**HOLD:** no real station plan, passenger-flow observation, field sightline, jurisdiction/accessibility code or fabrication readback. Therefore no Field PASS or operational performance claim.