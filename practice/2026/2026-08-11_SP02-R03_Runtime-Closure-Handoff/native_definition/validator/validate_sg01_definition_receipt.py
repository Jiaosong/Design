from pathlib import Path
import hashlib, json, sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("native_definition_evidence")
receipt_path = root / "definition_receipt.json"
ghx_files = sorted(root.glob("*.ghx"))
errors=[]

if not receipt_path.exists():
    errors.append("MISSING definition_receipt.json")
    receipt={}
else:
    try:
        receipt=json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        errors.append("INVALID definition_receipt.json: %s" % exc)
        receipt={}

if len(ghx_files) != 1:
    errors.append("Expected exactly one native GHX in evidence directory; got %d" % len(ghx_files))

if receipt:
    if receipt.get("runtime_state") != "REAL_GRASSHOPPER_SERIALIZE_AND_RELOAD":
        errors.append("runtime_state does not prove real native serialize+reload")
    if receipt.get("extension") != ".ghx":
        errors.append("extension not .ghx")
    if receipt.get("save_mechanism") != "GH_DocumentIO.SaveQuiet":
        errors.append("unexpected save mechanism")
    if receipt.get("load_mechanism") != "GH_DocumentIO.Open":
        errors.append("unexpected load mechanism")
    if receipt.get("save_success") is not True or receipt.get("load_success") is not True:
        errors.append("save/load not both true")

    inv=receipt.get("nickname_inventory", {})
    required=[
        "SP02_BASE","SP02_GRAFT","SP02_FLATTEN","SP02_TRANSPOSE","SP02_ADVERSE_TRANSPOSE",
        "PV_BASE","PV_GRAFT","PV_FLATTEN","PV_TRANSPOSE","PV_ADVERSE"
    ]
    for name in required:
        if inv.get(name) != 1:
            errors.append("nickname inventory invalid: %s" % name)

if len(ghx_files) == 1:
    actual=hashlib.sha256(ghx_files[0].read_bytes()).hexdigest()
    if receipt.get("sha256") != actual:
        errors.append("GHX SHA256 does not match definition_receipt")
else:
    actual=None

result={
    "ND02_NATIVE_SERIALIZE":"PASS" if not any("save" in e.lower() or "GHX" in e for e in errors) and receipt.get("save_success") is True else "OPEN",
    "ND03_NATIVE_RELOAD":"PASS" if receipt.get("runtime_state")=="REAL_GRASSHOPPER_SERIALIZE_AND_RELOAD" and receipt.get("load_success") is True else "OPEN",
    "ND04_IDENTITY_AUDIT":"PASS" if not errors and actual else "OPEN",
    "SG01":"PASS" if not errors and actual else "OPEN",
    "errors":errors,
    "ghx_sha256":actual,
    "truth":"Only real GH_DocumentIO serialize+reload evidence can close SG01."
}
(root/"SG01_VALIDATION_RESULT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if result["SG01"]=="PASS" else 2)
