#!/usr/bin/env python3
import copy,json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
VALIDATOR=ROOT/'tools'/'validate_editorial_analysis_board.py'
FIXTURE=Path(__file__).with_name('BOARD-01_REGISTER.json')

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
    run(base,True,'positive fixture')
    bad=copy.deepcopy(base); bad['rf_claim']='RF-C3'
    run(bad,False,'source-tile control cannot claim RF-C3')
    bad=copy.deepcopy(base); bad['panels'][0]['invented_text']=True
    run(bad,False,'unrecoverable microtext cannot be invented')
    bad=copy.deepcopy(base); bad['panels'][2]['semantic_state']='COMPLETE'
    run(bad,False,'visible source raster cannot prove semantic completion')
    bad=copy.deepcopy(base); bad['panels'][6]['diagnosis_link']=''
    run(bad,False,'theory frame must link back to diagnosis')
    bad=copy.deepcopy(base); bad['panels'][3]['ground_evidence']=''
    run(bad,False,'photo audit must state evidence role')
    bad=copy.deepcopy(base); bad['one_sentence_finding']=''
    run(bad,False,'board requires one-sentence finding')
    bad=copy.deepcopy(base); bad['first_read_object_id']='P05'
    run(bad,False,'first-read object must bind to dominant synthesis panel')
    bad=copy.deepcopy(base); bad['first_read_labels']=['1','2','3','4','5','6']
    run(bad,False,'first-read label budget cannot exceed five')
    bad=copy.deepcopy(base)
    for p in bad['panels']: p['reading_tempo']='SLOW'
    run(bad,False,'multi-role board cannot collapse all panels to one reading tempo')
    bad=copy.deepcopy(base); bad['actual_preview_review_ref']=''
    run(bad,False,'board structure must hand off to actual-preview review receipt')

if __name__=='__main__': main()
