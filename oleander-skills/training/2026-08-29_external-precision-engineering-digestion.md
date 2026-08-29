# External Skill Digestion — Precision Engineering Specialist — 2026-08-29

Status: `SOURCE DIGESTION / CANDIDATE MATERIAL DELTA / NO INSTALL / NO PROMOTION`

## Source

- Repository: `K-Dense-AI/scientific-agents`
- Source file: `scientific-agents/precision-engineering-specialist/AGENTS.md`
- License: repository root `LICENSE.md` = MIT, verified 2026-08-29.

## Current-first comparison

Compared against:

1. `oleander-3d-pipeline/PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md`
   - already owns source geometry, units, datums/joints, assembly placement and deterministic dimensional checks;
   - does not yet define the full function→variation-control→inspection-feature handoff.
2. `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md`
   - already owns measurand, method, calibration, traceability, uncertainty, propagation and decision impact;
   - intentionally remains general and does not map GD&T/GPS feature controls to measurement plans.
3. Technical Drawing PR #172 Candidate
   - owns drawing-carrier structure, spatial/technical translation and editable annotation;
   - does not become Current merely because this source provides GD&T/metrology content.
4. `oleander-design-process/DFM_DFA_PROCESS_CAPABILITY_EXTENSION.md`
   - owns manufacturability/process-capability/design-return reasoning;
   - does not own the semantic definition of a controlled geometric characteristic.

## Material Delta accepted

- GD&T/GPS is treated as a functional geometric contract, not decorative drawing notation;
- size, form, orientation, location, profile and runout remain distinct control families;
- datum reference strategy derives from real assembly/use relations, while datum simulation/alignment is part of the measurement contract;
- tolerance stack/variation modeling must identify contributors and correlation/assembly assumptions before choosing a calculation method;
- ASME Y14.5 and ISO GPS semantics must not be mixed without governing-authority/translation state;
- an inspection method must map to the actual controlled feature/relation rather than to “a dimension” generically;
- sampling, alignment, fitting, filtering and inaccessible geometry can materially change profile/form/location evidence;
- MBD/PMI presence in CAD/exchange is not enough: semantic associations/modifiers/revision must survive readback;
- CAD/PMI/drawing/inspection-program/report revision identity must be bound before a PASS can propagate;
- dimensional nonconformance should preserve design/process/measurement rival causes until evidence resolves them.

## Rejected / bounded transfer

Do not install as universal OLEANDER truth:

- fixed uncertainty-to-tolerance guard-band percentages;
- fixed temperature values, thermal coefficients, soak times or clean-room assumptions;
- fixed CMM stylus choice, scan density, point spacing, filter cutoff or probing strategy;
- one ASME Y14.5 edition or ISO GPS edition as global authority;
- blanket conversion of deprecated callouts to a preferred newer symbol without customer/project authority;
- fixed MMC/LMC/virtual-condition examples or dimensions;
- fixed Cpk/GR&R/SPC thresholds;
- fixed software stack (PC-DMIS, Calypso, PolyWorks, CETOL, 3DCS, etc.);
- AS9102/PPAP/FAI report structure as a universal OLEANDER release process;
- micrometer-class precision as the default scale for all products;
- “CMM report = truth” without method/traceability/uncertainty.

## Resulting OLEANDER extension

`oleander-skills/oleander-3d-pipeline/FUNCTIONAL_TOLERANCE_GDNT_METROLOGY_HANDOFF_EXTENSION.md`

Core bounded transfer:

`FUNCTION / FAILURE MODE → ASSEMBLY RELATION → FUNCTIONAL DATUM STRATEGY → CONTROLLED FEATURE → VARIATION / TOLERANCE MODEL → GD&T-GPS / PMI EXPRESSION → INSPECTION FEATURE MAP → METHOD / DATUM SIMULATION → UNCERTAINTY / DECISION-RULE HANDOFF → RESULT / NONCONFORMANCE → DESIGN OR PROCESS RETURN`

## Adversarial regression required

The Golden case must reject:
- datum labels chosen by CAD convenience;
- diameter pass used as location/assembly proof;
- automatic RSS or worst-case stack choice;
- mixed ASME/ISO semantics without authority;
- PMI icon/export presence used as semantic proof;
- best-fit CMM frame replacing the design datum frame silently;
- hand-gage spot check replacing a profile/location requirement;
- inspection PASS with stale design revision or unresolved uncertainty/method state.

## Maturity

`EXTERNAL-SOURCE-DIGESTED / DOCUMENTED CANDIDATE EXTENSION / PRACTICE NOT YET RUN / CROSS-CONTEXT NOT ESTABLISHED / PROJECT USAGE NOT ESTABLISHED / NO PROMOTION`.