#!/usr/bin/env python3
import copy, json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
VALIDATOR=ROOT/'tools'/'validate_node_semantics.py'
DIR=Path(__file__).parent
SPATIAL_SVG=DIR/'NODE-01_SEMANTICS.svg'
SPATIAL_REG=DIR/'NODE-01_REGISTER.json'
INTERFACE_SVG=DIR/'NODE-02_INTERFACE.svg'
INTERFACE_REG=DIR/'NODE-02_INTERFACE_REGISTER.json'

def run(svg,data,should_pass,label):
    with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False,encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2); p=Path(f.name)
    cp=subprocess.run([sys.executable,str(VALIDATOR),str(svg),str(p)],capture_output=True,text=True)
    p.unlink(missing_ok=True)
    if (cp.returncode==0)!=should_pass:
        print(cp.stdout,cp.stderr); raise SystemExit('regression failed: '+label)
    print('PASS regression:',label)

def main():
    spatial=json.loads(SPATIAL_REG.read_text(encoding='utf-8'))
    interface=json.loads(INTERFACE_REG.read_text(encoding='utf-8'))
    run(SPATIAL_SVG,spatial,True,'spatial-event fixture')
    run(INTERFACE_SVG,interface,True,'construction-interface fixture')

    bad=copy.deepcopy(spatial); bad['nodes'][1]['node_mode']='CONSTRUCTION_INTERFACE'
    run(SPATIAL_SVG,bad,False,'route junction cannot silently become construction interface')

    bad=copy.deepcopy(interface); bad['nodes'][0]['component_ids']=['COMP_PRIMARY']
    run(INTERFACE_SVG,bad,False,'construction interface requires at least two components')

    bad=copy.deepcopy(interface); bad['nodes'][0]['component_ids'][1]='MISSING_COMPONENT'
    bad['nodes'][0]['attached_component_ids']=['MISSING_COMPONENT']
    run(INTERFACE_SVG,bad,False,'construction component ids must exist in SVG')

    bad=copy.deepcopy(interface); bad['nodes'][0]['connected_edge_ids']=['E01']
    run(INTERFACE_SVG,bad,False,'construction interface cannot contaminate route topology')

if __name__=='__main__': main()
