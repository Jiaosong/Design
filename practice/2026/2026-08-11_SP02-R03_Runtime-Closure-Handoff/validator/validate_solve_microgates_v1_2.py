from pathlib import Path
import json, sys
E=Path(sys.argv[1]) if len(sys.argv)>1 else Path("runtime_evidence")
ROOT=Path(__file__).resolve().parents[1]
EXPECTED=json.loads((ROOT/"contracts/expected_tree_contract.json").read_text(encoding="utf-8"))
def load(name):
    p=E/name
    if not p.exists(): return None
    try:return json.loads(p.read_text(encoding="utf-8"))
    except:return None
p=load("provider_receipt.json"); d=load("definition_receipt.json"); s=load("solve_receipt.json")
t=load("tree_runtime.json"); r=load("reproduction_receipt.json")
g={f"SG{i:02d}":{"status":"OPEN"} for i in range(8)}
if p and p.get("runtime_authority_verified") is True and p.get("provider_id") and p.get("execution_id") and p.get("truth_state")!="TEST_FIXTURE":
    g["SG00"]={"status":"PASS"}
if d and str(d.get("extension","")).lower() in (".gh",".ghx") and len(str(d.get("sha256","")))==64 and d.get("load_success") is True:
    g["SG01"]={"status":"PASS"}
if s and s.get("request_observed") is True and s.get("mechanism"):
    g["SG02"]={"status":"PASS"}
if s and s.get("completion_observed") is True and s.get("errors")==[] and s.get("output_fingerprint"):
    g["SG03"]={"status":"PASS"}
states=(t or {}).get("states",{})
required=["BASE","GRAFT","FLATTEN","TRANSPOSE","ADVERSE_TRANSPOSE"]
if all(k in states for k in required):
    g["SG04"]={"status":"PASS"}
def same(label,target):
    o=states.get(label)
    if not o:return False
    for key in ("branch_count","data_count","branch_lengths"):
        if o.get(key)!=target.get(key):return False
    if "paths" in target and o.get("paths")!=target.get("paths"):return False
    return True
nom=EXPECTED["nominal"]
if g["SG04"]["status"]=="PASS" and all(same(k,nom[k]) for k in ("BASE","GRAFT","FLATTEN","TRANSPOSE")):
    g["SG05"]={"status":"PASS"}
adv=EXPECTED["adverse"]["ADVERSE_TRANSPOSE"]
if g["SG04"]["status"]=="PASS" and same("ADVERSE_TRANSPOSE",adv):
    g["SG06"]={"status":"PASS"}
if r and int(r.get("run_count",0))>=2 and r.get("definition_hash_same") is True and r.get("structure_signature_match") is True:
    g["SG07"]={"status":"PASS"}
def comp(ids):return "PASS" if all(g[i]["status"]=="PASS" for i in ids) else "OPEN"
out={"microgates":g,"CP2_CORE":comp(["SG00","SG01","SG02","SG03"]),"CP2_DATA":comp(["SG04","SG05","SG06"]),"CP2_REPRO":comp(["SG07"]),"CP2":comp([f"SG{i:02d}" for i in range(8)]),"CP4":"OPEN","truth":"Partial microgate closure never equals CP2 closure."}
out["practice_close_allowed"]=out["CP2"]=="PASS" and out["CP4"]=="PASS"
(E/"SOLVE_MICROGATE_RESULT.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(out,ensure_ascii=False,indent=2))
sys.exit(0 if out["CP2"]=="PASS" else 2)
