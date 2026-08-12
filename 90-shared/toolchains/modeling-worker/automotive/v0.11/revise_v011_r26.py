#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R26 — Lateral Fender Section Integration.

R25 fixed the side-view wheel-opening profile, but Human M5 review still shows the tire
standing proud of the body in 3/4 views and an isolated cap-like fender crown.
R26 retains R25 topology and x-z opening law and changes only wheel-zone Source y-coordinates,
creating a tapered local fender/shoulder bulge over the wheel package.
"""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path

BASE='/tmp/revise_v011_r25.py'
spec=importlib.util.spec_from_file_location('r25',BASE)
r25=importlib.util.module_from_spec(spec);spec.loader.exec_module(r25)
r24=r25.r24;r20=r25.r20;r18=r25.r18;r16=r25.r16;r14=r25.r14;b=r25.b

MODEL='OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R26'
r25.MODEL=MODEL;r24.MODEL=MODEL;r20.MODEL=MODEL;r18.MODEL=MODEL;r16.MODEL=MODEL;r16.r15.MODEL=MODEL
r14.MODEL=MODEL;r14.r12.MODEL=MODEL;r14.r11.MODEL=MODEL;r14.r10.MODEL=MODEL;r14.r09.MODEL=MODEL;r14.r08.MODEL=MODEL;r14.r08.r.MODEL=MODEL;b.MODEL=MODEL

LAT_MAX=.060
Z_CENTER=.62
Z_HALF=.58
_orig_build=r25.build_source_raw

def vertical_weight(z):
    return max(0.0,1.0-abs(z-Z_CENTER)/Z_HALF)

def build_source_r26(rows,M,glass):
    source,xs,cols,arch_meta,reuse=_orig_build(rows,M,glass)
    changed=0;outside=0;max_delta=0.0
    for v in source.data.vertices:
        x,y,z=v.co.x,v.co.y,v.co.z
        if abs(y)<1e-8:continue
        wx=min((b.FX,b.RX),key=lambda q:abs(x-q))
        if abs(x-wx)>r25.ZONE+1e-7:continue
        s=r25.arch_shape(x,wx);vw=vertical_weight(z);delta=LAT_MAX*s*vw
        if delta<=1e-8:continue
        v.co.y += (1.0 if y>0 else -1.0)*delta
        changed+=1;max_delta=max(max_delta,delta)
        if abs(x-wx)>r25.ZONE+1e-7:outside+=1
    source['OLEANDER_TOPOLOGY']='R26_R25_TOPOLOGY_LATERAL_FENDER_SECTION'
    source['R26_CHANGED_VERTEX_COUNT']=changed;source['R26_MAX_LATERAL_DELTA_M']=max_delta;source['R26_OUTSIDE_WHEEL_ZONE_CHANGED']=outside
    return source,xs,cols,arch_meta,reuse

r25.build_source_raw=build_source_r26

def patch_outputs(out:Path):
    cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text())
    c['job_id']='SYS-MODELING-WORKER-AUTO-M4M5-v0.11-R26'
    c['decision_question']='With R25 wheel-opening profile retained, does a tapered wheel-zone lateral section expansion integrate the tire under the fender and make the crown grow from the shoulder rather than read as an isolated cap?'
    c['source_authority']['editable_source']=f'{MODEL}.blend'
    c['primary_geometry'][0]['id']='PG-LATERAL-FENDER-SOURCE';c['primary_geometry'][0]['role']='R25 rounded local arch with R26 wheel-zone lateral fender section'
    c['semantic_components'][1]['id']='COMP-LATERAL-FENDER-SOURCE';c['semantic_components'][1]['role']='R26 editable primary source';c['semantic_components'][1]['source_ref']='PG-LATERAL-FENDER-SOURCE'
    c['locks'].append({'target':'R25 x-z wheel-opening profile + R09/R11/R12 package + topology membership','state':'LOCKED','reason':'R26 changes wheel-zone lateral section only','unlock_trigger':None})
    c['revision']={'revision_id':'R26-LATERAL-FENDER-SECTION','semantic_targets':['front/rear fender lateral section','shoulder-to-crown integration'],'parameters':{'max_lateral_delta_m':LAT_MAX,'vertical_center_m':Z_CENTER,'vertical_half_range_m':Z_HALF,'x_zone_radius_m':r25.ZONE,'topology_change':False},'expected_affected_components':['wheel-zone Source y-coordinates only'],'affected_view_policy':'HYBRID'}
    c['qa']['construction']=['R25 topology retained','one connected Source mesh','source n-gon=0','no Source Boolean/SubD','R20 terminal winding retained']
    c['qa']['project']=['wheel/tire must sit visually under the local fender in 3/4 views','fender crown must connect to shoulder without cap-like isolation','R25 rounded side opening must remain acceptable','M6/M7/M8 remains blocked']
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
    qp=out/'AUTOMOTIVE_V011_QA.json';q=json.loads(qp.read_text());q['schema']='oleander.auto.v0.11.r26.qa';q['model']=MODEL;q['checks']['lateral_fender_section_active']=True;q['boundary']='R26 changes wheel-zone Source y-coordinates only; R25 x-z arch profile and topology are retained. Human M5 Visual QA required; M6/M7/M8 blocked.';qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    rp=out/'AUTOMOTIVE_V011_RECEIPT.json';r=json.loads(rp.read_text());r['schema']='oleander.auto.v0.11.r26.receipt';r['model']=MODEL;rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def main():
    try:
        r25.main()
    except SystemExit as e:
        a=b.parse();out=Path(a.out).resolve();patch_outputs(out);raise SystemExit(e.code)

if __name__=='__main__':main()
