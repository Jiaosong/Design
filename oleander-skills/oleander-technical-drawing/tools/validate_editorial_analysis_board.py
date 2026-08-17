#!/usr/bin/env python3
import json, sys
from pathlib import Path

ROLES={
'BACKGROUND_EVIDENCE','CITY_SYSTEM_CONTEXT','SITE_SYNTHESIS','GROUND_PHOTO_AUDIT',
'PROBLEM_LAYER','TARGET_STRATEGY','THEORY_FRAME','DESIGN_PROPOSITION','VISION_CLOSE'
}
REQ={'panel_id','panel_role','question_answered','claim','source_refs','carrier_family','why_this_carrier','pixel_state','semantic_state'}

def fail(msg):
    print('FAIL:',msg); raise SystemExit(1)

def main():
    if len(sys.argv)!=2: fail('usage: validate_editorial_analysis_board.py REGISTER.json')
    d=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    if d.get('promotion') not in {'NO','NO_PROMOTION','CANDIDATE_NOT_PROMOTED'}: fail('register must remain non-promoted')
    if not d.get('reading_chain'): fail('reading_chain required')
    panels=d.get('panels')
    if not isinstance(panels,list) or not panels: fail('panels required')
    ids=set(); dom=[]
    for p in panels:
        miss=REQ-set(p)
        if miss: fail(f"panel missing {sorted(miss)}")
        if p['panel_id'] in ids: fail('duplicate panel_id '+p['panel_id'])
        ids.add(p['panel_id'])
        if p['panel_role'] not in ROLES: fail(f"{p['panel_id']}: invalid panel_role")
        if not p['source_refs']: fail(f"{p['panel_id']}: source_refs required")
        if not p['why_this_carrier']: fail(f"{p['panel_id']}: why_this_carrier required")
        if p.get('dominant'): dom.append(p['panel_id'])
        if p.get('text_state')=='UNRECOVERABLE' and p.get('invented_text'):
            fail(f"{p['panel_id']}: unreadable source text cannot be invented")
        if p.get('pixel_state')=='SOURCE_RASTER_VISIBLE' and p.get('semantic_state')=='COMPLETE':
            fail(f"{p['panel_id']}: source raster visibility cannot prove semantic completion")
        if p['panel_role']=='THEORY_FRAME' and not p.get('diagnosis_link'):
            fail(f"{p['panel_id']}: theory frame must link to diagnosis")
        if p['panel_role']=='GROUND_PHOTO_AUDIT' and not p.get('ground_evidence'):
            fail(f"{p['panel_id']}: photo audit must state ground evidence role")
    if len(dom)!=1: fail('exactly one dominant panel required for this fixture contract')
    if d.get('dominant_panel_id')!=dom[0]: fail('dominant_panel_id mismatch')
    if d.get('source_tile_control') and d.get('rf_claim')=='RF-C3':
        fail('source tile control cannot claim RF-C3')
    print(f"PASS: {len(panels)} editorial-board panels structurally valid")

if __name__=='__main__': main()
