#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
import g1_r2_core as r2
import g1_r2_qa as qa
import g1_r2_blender_scene as bs
MODEL='OLEANDER_G1_R2_HandheldShell__BLENDER_EXECUTION__v0_13'

def args():
    p=argparse.ArgumentParser(); p.add_argument('--source',required=True); p.add_argument('--correction',required=True); p.add_argument('--contract',required=True); p.add_argument('--out',required=True); p.add_argument('--resolution',type=int,default=512); return p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    a=args(); source=load(a.source); fix=load(a.correction); contract=load(a.contract); s=r2.apply(source,fix)
    base_report,bv=qa.evaluate(s,fix,False); rev_report,rv=qa.evaluate(s,fix,True); _,bf,_=r2.mesh(s,False); _,rf,_=r2.mesh(s,True)
    out=Path(a.out).resolve(); diag=out/contract['outputs']['diagnostic_root']; diag.mkdir(parents=True,exist_ok=True)
    bs.clean(); sc=bs.col(bs.SRC); dc=bs.col(bs.DER); qc=bs.col(bs.QA); src=bs.sources(s,sc)
    base=bs.mesh_obj('OL_DERIVED_G1_R2_BASELINE',bv,bf,dc,'R2 baseline derived execution mesh'); rev=bs.mesh_obj('OL_DERIVED_G1_R2_THUMB_REVISION',rv,rf,dc,'R2 controlled THUMB_SIDE_PLAN revision derived mesh'); rev.hide_render=True; rev.hide_viewport=True
    clay=bs.material('OLEANDER_MAT_DIAG_CLAY_v1',(.34,.35,.37),.42,0); refl=bs.material('OLEANDER_MAT_DIAG_REFLECTION_v1',(.055,.06,.07),.14,.65); zebra=bs.zebra(); bs.assign(base,clay); bs.assign(rev,clay)
    scene=bpy.context.scene; bs.render_setup(scene,contract,a.resolution); target=(.095,0,.052)
    hero=bs.camera('HERO_CAM',85,(.34,-.34,.25),target,qc); cmf=bs.camera('CMF_CAM',110,(.10,0,.46),target,qc); inspect=bs.camera('INSPECTION_CAM',135,(.42,0,.075),target,qc); rigmap=bs.rigs(qc,target)
    rendered=[]
    for stem,cam,mat,rig in [('BASELINE_BROAD_PERSPECTIVE',hero,clay,'BROAD'),('BASELINE_BROAD_TOP',cmf,clay,'BROAD'),('BASELINE_BROAD_SIDE',inspect,clay,'BROAD'),('BASELINE_STRIP_PERSPECTIVE',hero,refl,'STRIP'),('BASELINE_GRAZING_PERSPECTIVE',hero,refl,'GRAZING'),('BASELINE_ZEBRA_PERSPECTIVE',hero,zebra,'ZEBRA')]: rendered.append(bs.render(scene,diag,stem,cam,base,mat,rig,qc))
    base.hide_render=True; base.hide_viewport=True; rev.hide_render=False; rev.hide_viewport=False
    for stem,mat,rig in [('REVISION_BROAD_PERSPECTIVE',clay,'BROAD'),('REVISION_STRIP_PERSPECTIVE',refl,'STRIP')]: rendered.append(bs.render(scene,diag,stem,hero,rev,mat,rig,qc))
    base.hide_render=False; base.hide_viewport=False; rev.hide_render=True; rev.hide_viewport=True; master=bs.master_exr(scene,diag,hero,base,refl,qc)
    native={'schema':'oleander.modeling-worker.v0.13.g1.r2.blender-native-source-snapshot','authority_state':'WORKING_SOURCE','source_mode':'BLENDER_NATIVE_EDITABLE_MIRROR_WITH_JSON_INPUT_AUTHORITY','objects':{o.name:{'type':o.type,'role':o.get('OLEANDER_ROLE'),'editable':bool(o.get('OLEANDER_EDITABLE',False))} for o in src},'derived_objects':[base.name,rev.name],'round_trip_writeback_to_json':'NOT_IMPLEMENTED_IN_THIS_GATE'}
    (diag/contract['outputs']['source_snapshot']).write_text(json.dumps(native,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    scene['OLEANDER_MODEL']=MODEL; scene['OLEANDER_STAGE']='G1_R2_BLENDER_EXECUTION_DIAGNOSTIC'; scene['OLEANDER_AUTHORITY_STATE']='WORKING_SOURCE'; scene['OLEANDER_DESIGN_STATE']='EXPLORE'; scene['OLEANDER_CANDIDATE_PROMOTION']='NOT_RUN'; scene['OLEANDER_SOURCE_SHA256']=sha(a.source); scene['OLEANDER_CORRECTION_SHA256']=sha(a.correction); scene['OLEANDER_EXECUTION_CONTRACT_SHA256']=sha(a.contract)
    blend=out/contract['outputs']['blend']; bpy.ops.wm.save_as_mainfile(filepath=str(blend)); required=set(contract['required_diagnostics']); produced={Path(x).stem for x in rendered}
    checks={'source_authority_objects_present':len(src)==6 and all(bpy.data.objects.get(contract['native_source_objects'][k]) for k in contract['native_source_objects']),'source_objects_editable':all(bool(o.get('OLEANDER_EDITABLE',False)) for o in src),'derived_mesh_not_authority':base.get('OLEANDER_AUTHORITY')=='DERIVED_EXECUTION_NOT_AUTHORITY' and rev.get('OLEANDER_AUTHORITY')=='DERIVED_EXECUTION_NOT_AUTHORITY','baseline_machine_pass_retained':all(base_report['checks'].values()),'revision_machine_pass_retained':all(rev_report['checks'].values()),'required_diagnostics_written':required.issubset(produced) and all((diag/f'{x}.png').exists() for x in required),'master_exr_written':(diag/master).exists(),'native_blend_written':blend.exists(),'explicit_materials_present':all(bpy.data.materials.get(x) for x in ('OLEANDER_MAT_DIAG_CLAY_v1','OLEANDER_MAT_DIAG_REFLECTION_v1','OLEANDER_MAT_QA_ZEBRA_NORMAL_v1')),'explicit_cameras_present':all(bpy.data.objects.get(x) for x in ('HERO_CAM','CMF_CAM','INSPECTION_CAM')),'candidate_promotion_not_executed':contract['candidate_promotion']=='NOT_RUN'}
    status='BLENDER_EXECUTION_PASS_HUMAN_REFLECTION_REVIEW_REQUIRED' if all(checks.values()) else 'BLENDER_EXECUTION_FAIL_REVISE'
    report={'schema':'oleander.modeling-worker.v0.13.g1.r2.blender-report','model':MODEL,'status':status,'job_state':'EXECUTED','design_state':'EXPLORE','authority_state':'WORKING_SOURCE','candidate_promotion':'NOT_RUN','blender_version':bpy.app.version_string,'render_engine':scene.render.engine,'checks':checks,'machine_baseline':base_report,'machine_revision':rev_report,'source_objects':[o.name for o in src],'derived_objects':[base.name,rev.name],'camera_jobs':[hero.name,cmf.name,inspect.name],'rigs':rigmap,'diagnostics':rendered,'master_exr':master,'blend':blend.name,'source_sha256':sha(a.source),'correction_sha256':sha(a.correction),'contract_sha256':sha(a.contract),'boundary':contract['boundary']}
    (diag/contract['outputs']['report']).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if status.startswith('BLENDER_EXECUTION_PASS') else 5
if __name__=='__main__': raise SystemExit(main())
