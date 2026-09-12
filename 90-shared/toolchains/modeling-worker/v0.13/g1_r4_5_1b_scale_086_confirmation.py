#!/usr/bin/env python3
from __future__ import annotations

import argparse,hashlib,json,sys
from pathlib import Path
from typing import Any
import bpy

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))

import g1_geometry_core as base
import g1_r2_core as r2
import g1_r2_blender_roundtrip as rt
import g1_r2_topology_isolation as iso
import g1_r4_5_termination_cap_relation as r45
import g1_r4_5_1_cap_curvature_scale as r451


def args():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--r2-correction',required=True)
    p.add_argument('--confirmed-interface',required=True);p.add_argument('--execution-contract',required=True)
    p.add_argument('--binding',required=True);p.add_argument('--refinement-contract',required=True)
    p.add_argument('--confirmation',required=True);p.add_argument('--out',required=True);p.add_argument('--resolution',type=int,default=768)
    return p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def text(name,content):
    b=bpy.data.texts.get(name) or bpy.data.texts.new(name);b.clear();b.write(content);return b

def main()->int:
    a=args();seed_path=Path(a.source);seed_sha=sha(seed_path);seed=load(a.source);fix=load(a.r2_correction)
    confirmed=load(a.confirmed_interface);execution=load(a.execution_contract);binding=load(a.binding)
    machine_contract=load(a.refinement_contract);confirmation=load(a.confirmation);out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    receipt=(HERE/confirmation['authorization_receipt']).read_text(encoding='utf-8')
    if confirmation['authorization_phrase'] not in receipt:raise RuntimeError('Scale .86 confirmation authorization mismatch')
    rel=confirmation['selected_relation']
    if abs(float(rel['termination_cap_onset_u'])-.88)>1e-12 or abs(float(rel['termination_cap_pole_curvature_scale'])-.86)>1e-12:raise RuntimeError('Exact selected relation changed')
    if not confirmation['policy']['parameter_tuning_in_confirmation_forbidden']:raise RuntimeError('Confirmation must be frozen')

    template=r2.apply(seed,fix);deck=bpy.data.objects.get(rt.NAMES['INTERFACE_DECK_BOUNDARY']);lower=bpy.data.objects.get(rt.NAMES['LOWER_RETURN_PROFILE'])
    if deck is None or lower is None:raise RuntimeError('Blender-native Source objects missing')
    r45.set_confirmed_interface(deck,confirmed['source_overrides']);r451.clear_relation(lower)
    confirmed_reference=rt.extract_native_source(template)

    r451.bind_relation(lower,.88,.90);control_source=rt.extract_native_source(template);control_machine,control_source=r451.evaluate(confirmed_reference,control_source,machine_contract,fix)
    r451.bind_relation(lower,.88,.86);candidate_source=rt.extract_native_source(template);machine,candidate_source=r451.evaluate(confirmed_reference,candidate_source,machine_contract,fix)
    roundtrip=rt.controlled_native_cap_pole_scale_edit_test(template,delta_scale=.005)
    native_readback,native_diffs,authority=rt.authority_checks(candidate_source)
    candidate_digest=iso.source_digest(candidate_source);readback_digest=iso.source_digest(native_readback)
    interface=base.own(candidate_source,'INTERFACE_DECK_BOUNDARY');low=base.own(candidate_source,'LOWER_RETURN_PROFILE')
    source_checks={
      'exact_onset_0_88':abs(float(low['termination_cap_onset_u'])-.88)<=1e-12,
      'exact_scale_0_86':abs(float(low['termination_cap_pole_curvature_scale'])-.86)<=1e-12,
      'two_numeric_dofs':int(rel['numeric_dof_count'])==2,
      'cap_law_exact':low.get('termination_cap_law')==r2.CAP_LAW,
      'cap_semantics_exact':low.get('termination_cap_semantics')==r2.CAP_SEMANTICS,
      'cap_endpoint_exact':low.get('termination_cap_endpoint_section')==r2.CAP_ENDPOINT_SECTION,
      'confirmed_interface_exact':abs(float(interface['u_center'])-.62)<=1e-12 and abs(float(interface['u_halfspan'])-.26)<=1e-12 and interface.get('theta_center')=='TOP_MERIDIAN' and abs(float(interface['theta_halfspan_rad'])-1.06)<=1e-12 and abs(float(interface['core_fraction'])-.29)<=1e-12 and abs(float(interface['depth_m'])-.012)<=1e-12,
      'termination_envelope_locked':abs(float(low['termination_envelope_exponent'])-.34)<=1e-12,
      'candidate_machine_pass':machine['machine_pass'] and all(machine['checks'].values()),
      'control_0_90_machine_pass':control_machine['machine_pass'] and all(control_machine['checks'].values()),
      'sparse_authority_count_50':machine['legacy_machine_report']['sparse_scalar_count']==50,
      'native_scale_roundtrip_pass':roundtrip['pass'],
      'native_authority_checks_pass':all(authority.values()),
      'native_readback_digest_exact':candidate_digest==readback_digest and max(native_diffs.values())<=1e-8,
      'candidate_promotion_not_run':confirmation['policy']['candidate_promotion']=='NOT_RUN'
    }

    surface_runtime,runtime=iso.load_surface_runtime(binding);scene=bpy.context.scene;surface_runtime.render_setup(scene,execution['runtime'],a.resolution);scene.view_settings.exposure=-1.20
    dc=bpy.data.collections.get(binding['surface_evaluation']['derived_collection']);qc=bpy.data.collections.get(binding['surface_evaluation']['qa_collection'])
    if dc is None or qc is None:raise RuntimeError('Derived/QA collections missing')
    control_obj,_,_,_=rt.replace_derived('OL_DERIVED_G1_R4_5_1B_CONFIRM_SCALE_090_CONTROL',control_source,dc,False)
    candidate_obj,_,_,_=rt.replace_derived('OL_DERIVED_G1_R4_5_1B_CONFIRM_SCALE_086',candidate_source,dc,False)
    control_obj['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';candidate_obj['OLEANDER_AUTHORITY']='DERIVED_EXECUTION_NOT_AUTHORITY';candidate_obj['OLEANDER_SOURCE_DIGEST']=candidate_digest
    local=confirmation['local_view'];target=r45.axis_point(candidate_source,float(local['target_u']));off=tuple(float(v) for v in local['offset_from_target_m']);loc=tuple(target[i]+off[i] for i in range(3))
    old=bpy.data.objects.get(local['name'])
    if old is not None:bpy.data.objects.remove(old,do_unlink=True)
    cam=surface_runtime.camera(local['name'],float(local['lens_mm']),loc,target,qc);cam['OLEANDER_R4_5_1B_ROLE']='SCALE_086_EXACT_CONFIRMATION_CAMERA'
    iso.set_only_rendered(dc,control_obj);control_renders=r451.render_set(surface_runtime,binding,out,qc,control_obj,cam,'R4_5_1B_CONFIRM_SCALE_090_CONTROL')
    iso.set_only_rendered(dc,candidate_obj);candidate_renders=r451.render_set(surface_runtime,binding,out,qc,candidate_obj,cam,'R4_5_1B_CONFIRM_SCALE_086')
    diffs={rig:iso.image_difference(out/control_renders[rig],out/candidate_renders[rig]) for rig in ('BROAD','STRIP','GRAZING','ZEBRA')}

    text('OLEANDER_G1_R2_REBUILD.py',(HERE/'g1_r2_blender_rebuild.py').read_text(encoding='utf-8'))
    text('OLEANDER_G1_R2_LIVE_SOURCE.json',json.dumps(candidate_source,ensure_ascii=False,indent=2))
    text('OLEANDER_G1_R4_5_1B_CONFIRMED_RELATION.json',json.dumps(confirmation,ensure_ascii=False,indent=2))
    scene['OLEANDER_MODEL']='OLEANDER_G1_R4_5_1B_SCALE_086_WORKING_SOURCE__v0_13';scene['OLEANDER_STAGE']='R4_5_1B_EXACT_SCALE_086_CONFIRMATION';scene['OLEANDER_AUTHORITY_STATE']='WORKING_SOURCE';scene['OLEANDER_DESIGN_STATE']='REVISE / EXACT_CONFIRMATION_VISUAL_DECISION_PENDING';scene['OLEANDER_CANDIDATE_REVIEW']='REOPENED';scene['OLEANDER_CANDIDATE_PROMOTION']='NOT_RUN';scene['OLEANDER_TERMINATION_CAP_ONSET_U']=.88;scene['OLEANDER_TERMINATION_CAP_POLE_CURVATURE_SCALE']=.86;scene['OLEANDER_LIVE_SOURCE_DIGEST']=candidate_digest;scene['OLEANDER_SURFACE_SYSTEM_SHARED_RUNTIME_BOUND']=True
    blend=out/confirmation['outputs']['blend'];bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    snapshot={'schema':'oleander.modeling-worker.v0.13.g1.r4.5.1b.scale-086-native-source-snapshot.v1','authority_state':'WORKING_SOURCE','relation_state':'R4_5_1B_SCALE_086_EXACT_CONFIRMATION','live_source_digest':candidate_digest,'live_source':candidate_source,'blender_source_objects':list(rt.NAMES.values()),'derived_object':candidate_obj.name,'derived_is_authority':False,'embedded_live_source_text':'OLEANDER_G1_R2_LIVE_SOURCE.json','embedded_relation_text':'OLEANDER_G1_R4_5_1B_CONFIRMED_RELATION.json'}
    (out/confirmation['outputs']['native_source_snapshot']).write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    checks={**source_checks,
      'shared_surface_runtime_pass':runtime['status']=='PASS' and all(runtime['checks'].values()),
      'candidate_derived_not_authority':candidate_obj.get('OLEANDER_AUTHORITY')=='DERIVED_EXECUTION_NOT_AUTHORITY',
      'saved_blend_keeps_onset_active':abs(float(lower['termination_cap_onset_u'])-.88)<=1e-12,
      'saved_blend_keeps_scale_active':abs(float(lower['termination_cap_pole_curvature_scale'])-.86)<=1e-12,
      'live_source_embedded':bpy.data.texts.get('OLEANDER_G1_R2_LIVE_SOURCE.json') is not None,
      'relation_embedded':bpy.data.texts.get('OLEANDER_G1_R4_5_1B_CONFIRMED_RELATION.json') is not None,
      'all_exact_renders_written':all((out/x).exists() for x in list(control_renders.values())+list(candidate_renders.values())),
      'native_blend_written':blend.exists(),
      'snapshot_written':(out/confirmation['outputs']['native_source_snapshot']).exists(),
      'bootstrap_seed_not_overwritten':sha(seed_path)==seed_sha
    }
    status='R4_5_1B_SCALE_086_EXACT_CONFIRMATION_PASS_VISUAL_DECISION_REQUIRED' if all(checks.values()) else 'R4_5_1B_SCALE_086_EXACT_CONFIRMATION_FAIL_REVISE'
    report={'schema':'oleander.modeling-worker.v0.13.g1.r4.5.1b.scale-086-confirmation-report.v1','status':status,'job_state':'R4_5_1B_SCALE_086_EXACT_CONFIRMATION_EXECUTED','design_state':'REVISE / EXACT_VISUAL_DECISION_PENDING','authority_state':'WORKING_SOURCE','candidate_review':'REOPENED','candidate_promotion':'NOT_RUN','selected_relation':rel,'source_digest':candidate_digest,'candidate_machine':machine,'control_machine':control_machine,'roundtrip':roundtrip,'checks':checks,'surface_system_runtime':runtime,'renders':{'control_0_90':control_renders,'candidate_0_86':candidate_renders},'image_difference_metrics_vs_0_90':diffs,'blend':blend.name,'native_source_snapshot':confirmation['outputs']['native_source_snapshot'],'visual_decision':'NOT_RUN_REQUIRES_EXACT_CONFIRMATION_REVIEW','boundary':confirmation['boundary']}
    (out/confirmation['outputs']['report']).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2));return 0 if status.endswith('REQUIRED') else 17

if __name__=='__main__':raise SystemExit(main())
