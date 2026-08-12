#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 — R25 hard-point-correct working baseline.

Source geometry is exactly R25. The only implementation correction is the reusable
wheel hard-point contract applied before rendering. R27/R28 remain audit evidence and
are not source authority after the HP-correct A/B rebaseline.
"""
from __future__ import annotations
import importlib.util,json
from pathlib import Path

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
r25=load('/tmp/revise_v011_r25.py','r25');hp=load('/tmp/wheel_hp_contract.py','wheel_hp_contract')
r24=r25.r24;r20=r25.r20;r18=r25.r18;r16=r25.r16;r14=r25.r14;b=r25.b
MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R25_HPBASE'
for m in (r25,r24,r20,r18,r16,r16.r15,r14,r14.r12,r14.r11,r14.r10,r14.r09,r14.r08,r14.r08.r,b):m.MODEL=MODEL
EXPECTED_R25_SOURCE_HASH='6ae67c33aafb6da9f64359784e0cabb4fe9fb36b5bf62b91e49a0fa5348b9adf'
hp.install(b,.700)

def patch_outputs(out:Path):
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());records=getattr(b,'_OLEANDER_WHEEL_HP_RECORDS',[]);exact=bool(getattr(b,'_OLEANDER_WHEEL_HP_EXACT',False))
    q['schema']='oleander.auto.v0.11.r25-hpbase.qa';q['model']=MODEL;q['source_hash']=q.get('source_shape_hash') or q.get('source_hash');q['checks']['wheel_hp_contract_active']=True;q['checks']['wheel_hp_package_exact']=exact;q['checks']['r25_source_hash_rebaseline_locked']=q['source_hash']==EXPECTED_R25_SOURCE_HASH;q['wheel_hp_package']=records;q['boundary']='R25 Source restored as working baseline after HP-correct A/B. Wheel rendering is deterministically corrected to OD=0.70 m and exact current runtime hard-point centers. Human M5 remains required; M6/M7/M8 blocked.';q['status']='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(q['checks'].values()) else 'MACHINE_FAIL';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r25-hpbase.receipt';r['model']=MODEL;r['status']='EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if q['status'].startswith('MACHINE_PASS') else 'EXECUTED_MACHINE_FAIL';rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-AUTO-M1M5-v0.11-R25-HPBASE';c['source_authority']['editable_source']=f'{MODEL}.blend';c['decision_question']='With the visible wheel package corrected to the locked 0.70 m OD and current R09 hard-point centers, is R25 the stronger working Source baseline than the R27/R28 topology expansions?';c['revision']={'revision_id':'R25-HP-REBASELINE','source_change':False,'source_hash_expected':EXPECTED_R25_SOURCE_HASH,'wheel_implementation_fix':'wheel_hp_contract.py / OD=0.70 m / exact runtime hard-point centers','design_variable_change':False,'ab_decision':'R25 retained over R28A'};c['locks'].append({'target':'R25 Source geometry hash','state':'LOCKED','reason':'HP-correct A/B shows R25 materially cleaner than R28A; next revision must explicitly reopen only a smaller fender-crown dependency','unlock_trigger':'R29 local crown/shoulder evidence'});c['qa']['project']=['R25 is the current working source baseline, not promotion authority','remaining Human M5 issues: cap-like fender crown, hood-fender-shoulder pinching, local arch endpoint cleanup','R27/R28 retained as audit evidence only','M6/M7/M8 remains blocked'];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    (out/'HP_REBASELINE_DECISION.json').write_text(json.dumps({'status':'R25_WORKING_BASELINE_RETAINED','source_hash':q['source_hash'],'wheel_hp_package_exact':exact,'r27_r28_status':'SUPERSEDED_AS_SOURCE / AUDIT_ONLY','human_m5':'REVISE','next_gate':'R29_LOCAL_FENDER_CROWN_INTEGRATION','blocked':['M6','M7','M8']},ensure_ascii=False,indent=2)+'\n')

def main():
    code=0
    try:r25.main()
    except SystemExit as e:code=int(e.code or 0)
    a=b.parse();out=Path(a.out).resolve();patch_outputs(out);q=json.loads((out/'AUTOMOTIVE_V011_QA.json').read_text());raise SystemExit(0 if q['status']=='MACHINE_PASS_VISUAL_REVIEW_REQUIRED' else (code or 5))
if __name__=='__main__':main()
