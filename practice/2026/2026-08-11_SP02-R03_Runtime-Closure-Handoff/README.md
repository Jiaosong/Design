# OLEANDER｜SP02-R03 v1.4｜One-Run CP2 Closure

**Handoff Artifact：POST-REVIEW PASS / STATIC HANDOFF VERIFIED**  
**Real Rhino Runtime：NOT EXECUTED**  
**SP02：ACTIVE / RUNTIME GATE OPEN**  
**CP2：OPEN**  
**CP4：OPEN**

## Current architecture
`SG00 Authority → SG01 Native Definition → SG02 Solve Request → SG03 Solve Completion → SG04 Tree Extraction → SG05 Contract Match → SG06 Adverse Visibility → SG07 Repeatability`

- `CP2-CORE = SG00—SG03`
- `CP2-DATA = SG04—SG06`
- `CP2-REPRO = SG07`
- `CP2 = SG00—SG07 all PASS`
- `CP4` remains a separate real GUI provenance gate.

## What v1.4 changes
v1.3 proved the native-definition boundary:
- ND00 SDK metadata PASS;
- ND01 SDK-typed Builder compile PASS;
- hosted managed SDK cannot instantiate `GH_Document` without Rhino native `rhcommon_c`.

v1.4 therefore stops trying to close SG01 separately. A single real Rhino 8 process now targets **SG00—SG07 / CP2** in one execution.

The real process will:
1. require `RhinoApp.IsLicenseValidated = true` for SG00;
2. programmatically build the native GHX;
3. `GH_DocumentIO.SaveQuiet()` + immediate `Open()` + SHA256/identity audit for SG01;
4. observe `SolutionStart` and call `GH_Document.NewSolution(true, GH_SolutionMode.Silent)` for SG02;
5. observe `SolutionEnd`, collect runtime Error messages and output fingerprint for SG03;
6. extract BASE / GRAFT / FLATTEN / TRANSPOSE / ADVERSE from real `VolatileData` for SG04;
7. compare nominal states to the frozen tree contract for SG05;
8. verify adverse `[4,4,4,4,4,3] / 23 items` remains visible for SG06;
9. solve the same native definition again and compare structural signatures for SG07.

If all eight microgates pass:
`CP2 = PASS / CP4 = OPEN`.

CP4 is intentionally not bundled into CP2. It still requires readable real Parameter Viewer / Grasshopper canvas provenance and final visual review.

## Final static handoff verification
GitHub Actions run `31464984533` / job `93695924498`:
- C# Builder + `Sp02RuntimeClosure.cs` compile：PASS
- PowerShell AST syntax review：PASS
- empty-evidence fail-closed validator：PASS
- static handoff artifact upload：PASS

Static artifact:
- ID `9091185183`
- digest `sha256:338a43f4c69f8999c179bef19baf1fdcfd860524f6ac8202fade002509265cd0`
- head `e64e3b66580dd76aa8e5c114e361d116f6c65c44`

This remains **static handoff evidence only**.

## One-click execution
A portable kit is provided in the release package:

`ONE_CLICK_CP2/RUN_CP2.cmd`

Prerequisite: a Windows machine with installed and activated Rhino 8.
No manual Grasshopper definition construction is required.

## No-Purchase Constraint
**`NO_PURCHASE = TRUE` is now a hard project constraint.**

SP02 must not trigger a new purchase of Rhino, Rhino.Compute, Cloud VM, or a third-party paid runtime service merely to close Practice gates.

Allowed order:
1. existing licensed Rhino machine;
2. Human Authority using an existing licensed machine and returning evidence;
3. official evaluation only if its current no-purchase terms are re-verified at execution time;
4. genuinely free existing runtime provider if it actually executes Grasshopper;
5. otherwise stop and preserve `CP2 OPEN / CP4 OPEN`.

The one-click kit is therefore an **execution handoff for an already available legal Rhino environment**, not a purchase recommendation.

See `providers/NO_PURCHASE_RUNTIME_POLICY.md`.

## Release-review correction
The first portable kit inherited the repository-relative expected-contract path. That revision was rejected during release review. The final portable runner explicitly passes:

`ONE_CLICK_CP2/contract/expected_tree_contract.json`

to the validator.

## Current truth
`STATIC HANDOFF PASS / REAL RHINO NOT EXECUTED / SG00—SG07 OPEN / CP2 OPEN / CP4 OPEN / NO_PURCHASE TRUE`

See `docs/SP02_R03_v1.4_ONE_RUN_CP2_CLOSEOUT.md` and `data/sp02_r03_v1.4_status.json`.
