#!/usr/bin/env python3
import copy, json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
VALIDATOR=ROOT/'tools'/'validate_analysis_contract.py'
FIXTURE=Path(__file__).with_name('ANALYSIS-CONTRACT-01_REGISTER.json')

def run(data,should_pass,label):
    with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False,encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2); p=Path(f.name)
    cp=subprocess.run([sys.executable,str(VALIDATOR),str(p)],capture_output=True,text=True)
    p.unlink(missing_ok=True)
    if (cp.returncode==0)!=should_pass:
        print(cp.stdout,cp.stderr); raise SystemExit('regression failed: '+label)
    print('PASS regression:',label)

def main():
    base=json.loads(FIXTURE.read_text(encoding='utf-8'))
    run(base,True,'positive analysis contract')
    bad=copy.deepcopy(base); bad['decision_question']=''
    run(bad,False,'decision question required')
    bad=copy.deepcopy(base); bad['representation_contract']['supports']=[]
    run(bad,False,'representation must declare supported relations')
    bad=copy.deepcopy(base); bad['alternative_explanations']=[]
    run(bad,False,'documented alternative-explanation state requires content')
    bad=copy.deepcopy(base); bad['abstraction_budget']['removed_or_relaxed_variables'].append('TOPOLOGY')
    run(bad,False,'task-critical variable cannot disappear without external support')
    good=copy.deepcopy(base); good['abstraction_budget']['removed_or_relaxed_variables'].append('TOPOLOGY'); good['abstraction_budget']['external_support_layers']['TOPOLOGY']='TOPOLOGY-SCHEMATIC-LAYER'
    run(good,True,'removed task-critical variable may be carried by named external layer')

if __name__=='__main__': main()
