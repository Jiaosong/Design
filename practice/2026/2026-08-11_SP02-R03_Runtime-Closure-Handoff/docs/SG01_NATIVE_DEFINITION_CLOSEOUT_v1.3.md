# SP02-R03 v1.3｜SG01 Native Definition Closure

## Current truth
- **Handoff Artifact：POST-REVIEW PASS**
- **ND00 SDK Metadata：PASS**
- **ND01 Builder Compile：PASS**
- **ND02 Native Serialize：OPEN**
- **ND03 Native Reload：BLOCKED BY ND02**
- **ND04 Identity Audit：BLOCKED BY ND03**
- **SG01 Native Definition：OPEN**
- **CP2：OPEN**
- **CP4：OPEN**

## ND00｜real SDK metadata
Final PE/IL metadata probe:
- run `31462994131`
- job `93690114301`
- head `e195ab0d0b463f3968bd98334a57031af26c7c35`
- artifact `9090484158`
- digest `sha256:cb85b1fc030ed186f6b36963d3fc8f147cbc7eac82cd731a2942bd6d04fe3ec6`

Confirmed from official McNeel Grasshopper `8.32.26160.13001` assembly metadata:
- `Grasshopper.Kernel.Parameters.Param_Number`
- `Grasshopper.Kernel.Special.GH_ParamViewer`
- `Grasshopper.Kernel.Special.GH_PathMapper`
- `GH_PathMapper.Lexers`
- `Grasshopper.Kernel.Data.GH_LexerCombo`
- public `GH_LexerCombo(string,string)` constructor
- `IGH_Param.DataMapping`
- `GH_DocumentIO.SaveQuiet / Open`

This corrected the earlier false assumption that Path Mapper should be treated as an ordinary `IGH_Component`. The current builder uses the actual `GH_PathMapper` parameter object and `Lexers.Add(new GH_LexerCombo("{A;B}", "{B}"))`.

## ND01｜builder compile
Final complete static handoff compile:
- run `31463559829`
- job `93691740664`
- head `a0c3c4518f8bc47b6609f9d4638375d1fd452dd5`
- artifact `9090687106`
- digest `sha256:90faa650c416be27a0bb5a9f0c66dd28b3c6b708249e8537bb3eb7364d69c28c`
- builder DLL SHA256 `4adc6b62632e9cdde8272f2b33fdda3c744d086928bfdc0c7dd06e46ba312925`

ND01 first compile failed because `GH_DocumentIO` is not `IDisposable`; `using var` was removed and the compiler then passed with the SDK-typed builder.

ND01 is explicitly `STATIC_COMPILE_ONLY_NOT_GRASSHOPPER_RUNTIME`.

## Hosted Windows native-runtime experiment
Run `31463649333` compiled the Builder and harness and hydrated the managed McNeel SDK assemblies. Actual execution reached `new GH_Document()` and then failed with:

`System.DllNotFoundException: rhcommon_c`

This is accepted as **boundary evidence**. It proves that managed NuGet assembly hydration cannot substitute for Rhino's native runtime. We do not continue adding DLLs to imitate Rhino.

## Exact remaining SG01 closure chain
One real Rhino 8 native runtime must execute:

`Builder DLL → GH_Document → GH_DocumentIO.SaveQuiet(SP02_R03_native.ghx) → GH_DocumentIO.Open(same GHX) → SHA256 + nickname inventory → SG01 validator`

Required nickname inventory after reload:
- SP02_BASE
- SP02_GRAFT
- SP02_FLATTEN
- SP02_TRANSPOSE
- SP02_ADVERSE_TRANSPOSE
- PV_BASE
- PV_GRAFT
- PV_FLATTEN
- PV_TRANSPOSE
- PV_ADVERSE

A dedicated workflow already exists at `.github/workflows/sp02-r03-native-definition-real-rhino.yml` and intentionally requires `[self-hosted, Windows, X64, rhino8]` for the real-runtime job.

## Review
The v1.3 handoff package passes AR-G01—G10 + AR-S01/S03/S04/S07/S09. This does not change SG01/CP2/CP4 runtime state.
