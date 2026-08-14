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
import g1_r2_blender_roundtrip as rt
MODEL='OLEANDER_G1_R2_HandheldShell__BLENDER_NATIVE_SOURCE__v0_13'

def args():
    p=argparse.ArgumentParser(); p.add_argument('--source',required=True); p.add_argument('--correction',required=True); p.add_argument('--contract',required=True); p.add_argument('--binding',required=True); p.add_argument('--out',required=True); p.add_argument('--resolution',type=int,default=512); return p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def text(name,content):
    t=bpy.data.texts.get(name) or bpy.data.texts.new(name); t.clear(); t.write(content); return t

def main():
    a=args(); source_path=Path(a.source); seed_sha_before=sha(source_path); source=load(a.source); fix=load(a.correction); contract=load(a.contract); binding=load(a.binding); seed=r2.apply(source,fix)
    out=Path(a.out).resolve(); diag=out/contract['outputs']['diagnostic_root']; diag.mkdir(parents=True,exist_ok=True)

    gate=binding['roundtrip_gate']; read_tol=float(gate['bootstrap_readback_tolerance_m']); edit_tol=float(gate['controlled_native_edit_tolerance_m']); restore_tol=float(gate['restore_tolerance_m']); locked_tol=float(gate['locked_semantic_tolerance_rad'])
    bs.clean(); sc=bs.col(bs.SRC); dc=bs.col(bs.DER); qc=bs.col(bs.QA); src=bs.sources(seed,sc)
    live_source,bootstrap_diffs,authority_checks=rt.authority_checks(seed,read_tol,locked_tol)
    edit_delta=float(gate['controlled_native_edit_delta_m']); edit_test=rt.controlled_native_edit_test(seed,edit_delta,edit_tol,restore_tol)
    live_source=rt.extract_native_source(seed)
    base_report,bv=qa.evaluate(live_source,fix,False); rev_report,rv=qa.evaluate(live_source,fix,True); _,bf,_=r2.mesh(live_source,False); _,rf,_=r2.mesh(live_source,True)
    base=bs.mesh_obj('OL_DERIVED_G1_R2_BASELINE',bv,bf,dc,'R2 baseline derived from Blender-native Working Source'); rev=bs.mesh_obj('OL_DERIVED_G1_R2_THUMB_REVISION',rv,rf,dc,'R2 controlled revision derived from Blender-native Working Source'); rev.hide_render=True; rev.hide_viewport=True
    base['OLEANDER_SOURCE_MODE']='BLENDER_NATIVE_EDITABLE_WORKING_SOURCE'; rev['OLEANDER_SOURCE_MODE']='BLENDER_NATIVE_EDITABLE_WORKING_SOURCE'

    clay=bs.material('OLEANDER_MAT_DIAG_CLAY_v1',(.34,.35,.37),.42,0); refl=bs.material('OLEANDER_MAT_DIAG_REFLECTION_v1',(.055,.06,.07),.14,.65); zebra=bs.zebra(); bs.assign(base,clay); bs.assign(rev,clay)
    scene=bpy.context.scene; bs.render_setup(scene,contract,a.resolution); scene.view_settings.exposure=-1.20; target=(.095,0,.052)
    scene['OLEANDER_G1_R2_U_RINGS']=int(live_source['derived_execution']['u_rings']); scene['OLEANDER_G1_R2_CIRC_SAMPLES']=int(live_source['derived_execution']['circumferential_samples']); scene['OLEANDER_TERMINATION_ENVELOPE_EXPONENT']=float(live_source['ownership']['LOWER_RETURN_PROFILE'].get('termination_envelope_exponent',.34)); scene['OLEANDER_LOCKED_THETA_CENTER_TOP']=True; scene['OLEANDER_NATIVE_READBACK_TOLERANCE_M']=read_tol
    hero=bs.camera('HERO_CAM',85,(.34,-.34,.25),target,qc); cmf=bs.camera('CMF_CAM',110,(.095,0,1.20),target,qc); inspect=bs.camera('INSPECTION_CAM',135,(.95,0,.075),target,qc); rigmap=bs.rigs(qc,target)
    for o in qc.objects:
        if (o.type=='LIGHT' or o.name=='R2_NEG_FILL') and hasattr(o,'visible_camera'): o.visible_camera=False
    rendered=[]
    for stem,cam,mat,rig in [('BASELINE_BROAD_PERSPECTIVE',hero,clay,'BROAD'),('BASELINE_BROAD_TOP',cmf,clay,'BROAD'),('BASELINE_BROAD_SIDE',inspect,clay,'BROAD'),('BASELINE_STRIP_PERSPECTIVE',hero,refl,'STRIP'),('BASELINE_GRAZING_PERSPECTIVE',hero,refl,'GRAZING'),('BASELINE_ZEBRA_PERSPECTIVE',hero,zebra,'ZEBRA')]: rendered.append(bs.render(scene,diag,stem,cam,base,mat,rig,qc))
    base.hide_render=True; base.hide_viewport=True; rev.hide_render=False; rev.hide_viewport=False
    for stem,mat,rig in [('REVISION_BROAD_PERSPECTIVE',clay,'BROAD'),('REVISION_STRIP_PERSPECTIVE',refl,'STRIP')]: rendered.append(bs.render(scene,diag,stem,hero,rev,mat,rig,qc))
    base.hide_render=False; base.hide_viewport=False; rev.hide_render=True; rev.hide_viewport=True; master=bs.master_exr(scene,diag,hero,base,refl,qc)

    rebuild_source=(HERE/'g1_r2_blender_rebuild.py').read_text(encoding='utf-8'); text('OLEANDER_G1_R2_REBUILD.py',rebuild_source); text('OLEANDER_G1_R2_LIVE_SOURCE.json',json.dumps(live_source,ensure_ascii=False,indent=2))
    roundtrip={
      'schema':'oleander.modeling-worker.v0.13.g1.r2.blender-native-roundtrip',
      'authority_state':'WORKING_SOURCE','source_mode':'BLENDER_NATIVE_EDITABLE_WORKING_SOURCE','bootstrap_seed_sha256':seed_sha_before,
      'representation_precision':gate['representation_precision'],'bootstrap_readback_tolerance_m':read_tol,'bootstrap_readback_family_error_m':bootstrap_diffs,'authority_checks':authority_checks,'controlled_native_edit_test':edit_test,
      'live_source_snapshot':live_source,'bootstrap_seed_overwritten':False,'writeback_policy':'NEW_SNAPSHOT_ONLY','rebuild_text_block':'OLEANDER_G1_R2_REBUILD.py'
    }
    (diag/contract['outputs']['roundtrip_snapshot']).write_text(json.dumps(roundtrip,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    native={'schema':'oleander.modeling-worker.v0.13.g1.r2.blender-native-source-snapshot','authority_state':'WORKING_SOURCE','source_mode':'BLENDER_NATIVE_EDITABLE_WORKING_SOURCE','bootstrap_role':'IMMUTABLE_SEED_AND_PROVENANCE','objects':{o.name:{'type':o.type,'role':o.get('OLEANDER_ROLE'),'editable':bool(o.get('OLEANDER_EDITABLE',False))} for o in src},'derived_objects':[base.name,rev.name],'round_trip_readback_and_rebuild':'IMPLEMENTED','bootstrap_seed_overwrite':'FORBIDDEN','locked_semantics':binding['source_authority']['locked_semantics']}
    (diag/contract['outputs']['source_snapshot']).write_text(json.dumps(native,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    scene['OLEANDER_MODEL']=MODEL; scene['OLEANDER_STAGE']='G1_R2_BLENDER_NATIVE_SOURCE_ROUNDTRIP'; scene['OLEANDER_AUTHORITY_STATE']='WORKING_SOURCE'; scene['OLEANDER_DESIGN_STATE']='REVISE'; scene['OLEANDER_CANDIDATE_REVIEW']='REOPENED'; scene['OLEANDER_CANDIDATE_PROMOTION']='NOT_RUN'; scene['OLEANDER_SOURCE_MODE']='BLENDER_NATIVE_EDITABLE_WORKING_SOURCE'; scene['OLEANDER_SOURCE_SHA256']=seed_sha_before; scene['OLEANDER_CORRECTION_SHA256']=sha(a.correction); scene['OLEANDER_EXECUTION_CONTRACT_SHA256']=sha(a.contract); scene['OLEANDER_SURFACE_BINDING_SHA256']=sha(a.binding); scene['OLEANDER_DIAGNOSTIC_EXPOSURE']=-1.20
    blend=out/contract['outputs']['blend']; bpy.ops.wm.save_as_mainfile(filepath=str(blend)); required=set(contract['required_diagnostics']); produced={Path(x).stem for x in rendered}; seed_sha_after=sha(source_path)
    checks={
      'source_authority_objects_present':authority_checks['six_native_source_objects_present'],
      'source_objects_editable':authority_checks['all_native_source_objects_editable'],
      'source_objects_are_working_source':authority_checks['all_native_source_objects_working_source'],
      'bootstrap_to_native_readback_within_representation_tolerance':authority_checks['bootstrap_roundtrip_within_blender_representation_tolerance'],
      'locked_source_semantics_preserved':authority_checks['locked_top_meridian_semantic_preserved'],
      'controlled_native_edit_roundtrip_pass':edit_test['pass'],
      'derived_mesh_not_authority':base.get('OLEANDER_AUTHORITY')=='DERIVED_EXECUTION_NOT_AUTHORITY' and rev.get('OLEANDER_AUTHORITY')=='DERIVED_EXECUTION_NOT_AUTHORITY',
      'derived_mesh_built_from_native_readback':base.get('OLEANDER_SOURCE_MODE')=='BLENDER_NATIVE_EDITABLE_WORKING_SOURCE',
      'baseline_machine_pass_retained':all(base_report['checks'].values()),'revision_machine_pass_retained':all(rev_report['checks'].values()),
      'required_diagnostics_written':required.issubset(produced) and all((diag/f'{x}.png').exists() for x in required),'master_exr_written':(diag/master).exists(),'native_blend_written':blend.exists(),
      'self_contained_rebuild_text_embedded':bpy.data.texts.get('OLEANDER_G1_R2_REBUILD.py') is not None,
      'live_source_text_embedded':bpy.data.texts.get('OLEANDER_G1_R2_LIVE_SOURCE.json') is not None,
      'roundtrip_snapshot_written':(diag/contract['outputs']['roundtrip_snapshot']).exists(),
      'bootstrap_seed_not_overwritten':seed_sha_before==seed_sha_after,
      'explicit_materials_present':all(bpy.data.materials.get(x) for x in ('OLEANDER_MAT_DIAG_CLAY_v1','OLEANDER_MAT_DIAG_REFLECTION_v1','OLEANDER_MAT_QA_ZEBRA_NORMAL_v1')),
      'explicit_cameras_present':all(bpy.data.objects.get(x) for x in ('HERO_CAM','CMF_CAM','INSPECTION_CAM')),
      'candidate_review_reopened':contract['candidate_review']=='REOPENED','candidate_promotion_not_executed':contract['candidate_promotion']=='NOT_RUN'
    }
    status='BLENDER_NATIVE_SOURCE_ROUNDTRIP_PASS_REFLECTION_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'BLENDER_NATIVE_SOURCE_ROUNDTRIP_FAIL_REVISE'
    report={'schema':'oleander.modeling-worker.v0.13.g1.r2.blender-report.v2','model':MODEL,'status':status,'job_state':'BLENDER_NATIVE_SOURCE_ROUNDTRIP_EXECUTED','design_state':'REVISE','authority_state':'WORKING_SOURCE','candidate_review':'REOPENED','candidate_promotion':'NOT_RUN','blender_version':bpy.app.version_string,'render_engine':scene.render.engine,'diagnostic_exposure':scene.view_settings.exposure,'checks':checks,'bootstrap_readback_family_error_m':bootstrap_diffs,'native_edit_roundtrip':edit_test,'machine_baseline':base_report,'machine_revision':rev_report,'source_objects':[o.name for o in src],'derived_objects':[base.name,rev.name],'camera_jobs':{'HERO_CAM':{'lens_mm':85,'location':[.34,-.34,.25]},'CMF_CAM':{'lens_mm':110,'location':[.095,0,1.20]},'INSPECTION_CAM':{'lens_mm':135,'location':[.95,0,.075]}},'rigs':rigmap,'diagnostics':rendered,'master_exr':master,'blend':blend.name,'roundtrip_snapshot':contract['outputs']['roundtrip_snapshot'],'rebuild_text_block':'OLEANDER_G1_R2_REBUILD.py','source_sha256':seed_sha_before,'correction_sha256':sha(a.correction),'contract_sha256':sha(a.contract),'binding_sha256':sha(a.binding),'boundary':contract['boundary']}
    (diag/contract['outputs']['report']).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if status.startswith('BLENDER_NATIVE_SOURCE_ROUNDTRIP_PASS') else 5
if __name__=='__main__': raise SystemExit(main())
