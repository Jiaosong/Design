# OLEANDER｜SP02-R03 v1.3｜Multi-Provider Runtime Closure

**Handoff Artifact：POST-REVIEW PASS**  
**SP02 Runtime：ACTIVE / RUNTIME GATE OPEN**

## Solve Gate Decomposition
`SG00 Authority → SG01 Native Definition → SG02 Solve Request → SG03 Solve Completion → SG04 Tree Extraction → SG05 Contract Match → SG06 Adverse Visibility → SG07 Repeatability`

- `CP2-CORE = SG00—SG03`
- `CP2-DATA = SG04—SG06`
- `CP2-REPRO = SG07`
- `CP2 = SG00—SG07`
- `CP4` remains a separate real GUI provenance gate.

## v1.3｜SG01 Native Definition Closure
SG01 is further decomposed:

- `ND00｜SDK Metadata` → **PASS**
- `ND01｜Builder Compile` → **PASS**
- `ND02｜Native Serialize` → **OPEN**
- `ND03｜Native Reload` → **BLOCKED BY ND02**
- `ND04｜Identity Audit` → **BLOCKED BY ND03**
- `SG01` → **OPEN**

### ND00
Official McNeel Grasshopper `8.32.26160.13001` PE/IL metadata was inspected without pretending to load Rhino runtime. It confirmed:

- `Param_Number`
- `GH_ParamViewer`
- `GH_PathMapper`
- `GH_PathMapper.Lexers`
- `GH_LexerCombo(string,string)`
- `IGH_Param.DataMapping`
- `GH_DocumentIO.SaveQuiet / Open`

This rejected the earlier assumption that Path Mapper should be treated as an ordinary `IGH_Component`.

### ND01
The SDK-typed native builder now compiles successfully. It builds the intended Base/Graft/Flatten/Path Mapper/Adverse structure and five Param Viewers. Final static handoff compile:

- run `31463559829`
- artifact `9090687106`
- artifact digest `sha256:90faa650c416be27a0bb5a9f0c66dd28b3c6b708249e8537bb3eb7364d69c28c`
- builder DLL SHA256 `4adc6b62632e9cdde8272f2b33fdda3c744d086928bfdc0c7dd06e46ba312925`

ND01 means **STATIC_COMPILE_ONLY_NOT_GRASSHOPPER_RUNTIME**.

## Hosted SDK runtime boundary
A GitHub-hosted Windows experiment compiled the Builder and harness and hydrated the managed McNeel SDK assemblies. Actual execution reached `new GH_Document()` and then failed on Rhino native `rhcommon_c`.

Decision: this is accepted as boundary evidence. We stop trying to hydrate managed DLLs because that would imitate Rhino rather than execute Rhino. The historical hosted workflow is now manual-only and is not a supported SG01 closure route.

## Exact remaining SG01 operation
Run once on a real Rhino 8 native runtime:

`Builder DLL → GH_Document → GH_DocumentIO.SaveQuiet(SP02_R03_native.ghx) → GH_DocumentIO.Open(same GHX) → SHA256 + five sinks + five Param Viewers identity audit`

Prepared paths:
- `native_definition/runner/run_native_definition_windows.ps1`
- `native_definition/runner/run_builder_in_rhino.py`
- `native_definition/validator/validate_sg01_definition_receipt.py`
- `.github/workflows/sp02-r03-native-definition-real-rhino.yml`

The real-Rhino workflow intentionally requires `[self-hosted, Windows, X64, rhino8]` for ND02—ND04.

## Current truth
`ND00 PASS / ND01 PASS / ND02 OPEN / ND03 BLOCKED / ND04 BLOCKED / SG00 OPEN / SG01 OPEN / CP2 OPEN / CP4 OPEN`

See `docs/SG01_NATIVE_DEFINITION_CLOSEOUT_v1.3.md` for evidence IDs, rejected shortcuts and review state.
