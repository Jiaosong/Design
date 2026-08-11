from pathlib import Path
import json, sys, hashlib

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("runtime_evidence")
CONTRACT = Path(__file__).resolve().parents[1] / "contracts" / "expected_tree_contract.json"
RUNTIME_CONTRACT = Path(__file__).resolve().parents[1] / "contracts" / "runtime_evidence_contract.json"

expected = json.loads(CONTRACT.read_text(encoding="utf-8"))
runtime_contract = json.loads(RUNTIME_CONTRACT.read_text(encoding="utf-8"))
errors=[]
warnings=[]

def load(name):
    p=ROOT/name
    if not p.exists():
        errors.append("MISSING: "+name)
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append("INVALID_JSON %s: %s"%(name,e))
        return None

receipt=load("runtime_receipt.json")
runtime=load("tree_runtime.json")
inventory=load("component_inventory.json")

for name in runtime_contract["required_files"]:
    if not (ROOT/name).exists():
        errors.append("MISSING REQUIRED ARTIFACT: "+name)

native=list(ROOT.glob("*.gh"))+list(ROOT.glob("*.ghx"))+list((ROOT/"solved_definition").glob("*.gh"))+list((ROOT/"solved_definition").glob("*.ghx"))
if not native:
    errors.append("NO NATIVE .gh/.ghx RUNTIME ARTIFACT")

if receipt:
    if receipt.get("runtime_state") != "RHINO_GRASSHOPPER_EXECUTED":
        errors.append("RUNTIME STATE IS NOT REAL RHINO+GRASSHOPPER EXECUTED")
    if receipt.get("rhino_license_validated") is not True:
        errors.append("RHINO LICENSE NOT VALIDATED IN RECEIPT")

def compare_state(label, observed, target):
    if observed is None:
        errors.append("STATE MISSING: "+label); return
    for key in ("branch_count","data_count","branch_lengths"):
        if observed.get(key) != target.get(key):
            errors.append("%s %s mismatch observed=%r expected=%r"%(label,key,observed.get(key),target.get(key)))
    if "paths" in target and observed.get("paths") != target["paths"]:
        errors.append("%s paths mismatch observed=%r expected=%r"%(label,observed.get("paths"),target["paths"]))
    if "path_dimension" in target:
        dims=[]
        for p in observed.get("paths",[]):
            content=p.strip("{}")
            dims.append(0 if not content else len(content.split(";")))
        if not dims or any(d != target["path_dimension"] for d in dims):
            errors.append("%s path dimension mismatch: %r"%(label,dims))

if runtime:
    states=runtime.get("states",{})
    for label,target in expected["nominal"].items():
        compare_state(label, states.get(label), target)
    for label,target in expected["adverse"].items():
        compare_state(label, states.get(label), target)

if inventory:
    nicknames=[o.get("nickname") for o in inventory.get("objects",[])]
    for n in expected["required_sink_nicknames"]+expected["required_viewer_nicknames"]:
        if nicknames.count(n) != 1:
            errors.append("COMPONENT INVENTORY requires exactly one %s; got %d"%(n,nicknames.count(n)))

for name in ("grasshopper_canvas_four_state.png","rhino_viewport_four_state.png","adverse_case_canvas.png"):
    p=ROOT/name
    if p.exists() and p.stat().st_size < 10_000:
        errors.append("SCREENSHOT TOO SMALL / LIKELY INVALID: %s (%d bytes)"%(name,p.stat().st_size))

result={
    "exercise":"SP02-R03｜Runtime Closure",
    "evidence_root":str(ROOT),
    "CP2":"PASS" if not any(("RUNTIME" in e or "STATE" in e or "mismatch" in e or "NATIVE" in e or "LICENSE" in e) for e in errors) else "OPEN",
    "CP4":"PASS" if not any(("VIEWER" in e or "COMPONENT INVENTORY" in e or "SCREENSHOT" in e or "MISSING REQUIRED ARTIFACT" in e) for e in errors) else "OPEN",
    "errors":errors,
    "warnings":warnings,
}
result["runtime_gate"]="PASS" if result["CP2"]=="PASS" and result["CP4"]=="PASS" and not errors else "OPEN"
result["promotion_allowed"]=result["runtime_gate"]=="PASS"
result["final_artifact_review"]="PENDING"
print(json.dumps(result, ensure_ascii=False, indent=2))
(Path(ROOT)/"VALIDATION_RESULT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
sys.exit(0 if result["runtime_gate"]=="PASS" else 2)
