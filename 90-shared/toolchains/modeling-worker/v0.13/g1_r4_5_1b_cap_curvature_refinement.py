#!/usr/bin/env python3
from __future__ import annotations

import argparse,json,sys
from pathlib import Path
from typing import Any
import bpy

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))

import g1_r2_core as r2
import g1_r2_blender_roundtrip as rt
import g1_r2_topology_isolation as iso
import g1_r4_5_termination_cap_relation as r45
import g1_r4_5_1_cap_curvature_scale as r451


def args():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True); p.add_argument('--r2-correction',required=True)
    p.add_argument('--confirmed-interface',required=True); p.add_argument('--execution-contract',required=True)
    p.add_argument('--binding',required=True); p.add_argument('--contract',required=True)
    p.add_argument('--out',required=True); p.add_argument('--resolution',type=int,default=640)
    return p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def main()->int:
    a=args(); seed=load(a.source); fix=load(a.r2_correction); confirmed=load(a.confirmed_interface)
    execution=load(a.execution_contract); binding=load(a.binding); contract=load(a.contract)
    out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    receipt=(HERE/contract['authorization_receipt']).read_text(encoding='utf-8')
    if contract['authorization_phrase'] not in receipt: raise RuntimeError('R4.5.1B authorization receipt mismatch')

    template=r2.apply(seed,fix); native_before=rt.extract_native_source(template); digest_before=iso.source_digest(native_before)
    deck=bpy.data.objects.get(rt.NAMES['INTERFACE_DECK_BOUNDARY']); lower=bpy.data.objects.get(rt.NAMES['LOWER_RETURN_PROFILE'])
    if deck is None or lower is None: raise RuntimeError('Blender-native Source objects missing')
    original_deck={k:deck[k] for k in ('u_center','u_halfspan','theta_halfspan_rad','core_fraction','depth_m','theta_center_rad','theta_center_semantics','blend')}
    original_extra={k:lower[k] for k in lower.keys() if k.startswith('termination_cap_')}
    r45.set_confirmed_interface(deck,confirmed['source_overrides']); r451.clear_relation(lower)
    confirmed_reference=rt.extract_native_source(template)
    onset=float(contract['relation_vocabulary']['locked_onset_value'])

    control_scale=float(contract['visual_reference']['termination_cap_pole_curvature_scale'])
    r451.bind_relation(lower,onset,control_scale); control_source=rt.extract_native_source(template)
    control_result,control_source=r451.evaluate(confirmed_reference,control_source,contract,fix)
    if not control_result['machine_pass']: raise RuntimeError('The .90 visual control no longer passes the unchanged Machine gate')

    variants={}
    for vid,spec in contract['variants'].items():
        scale=float(spec['termination_cap_pole_curvature_scale']); r451.bind_relation(lower,onset,scale)
        source=rt.extract_native_source(template); result,source=r451.evaluate(confirmed_reference,source,contract,fix)
        result['source_digest']=iso.source_digest(source); variants[vid]={'result':result,'source':source}
    pass_ids=[k for k,v in variants.items() if v['result']['machine_pass']]
    if pass_ids:
        probe=min(pass_ids,key=lambda k:variants[k]['result']['cap_turn_probe']['cap_region_max_normal_turn_deg'])
        r451.bind_relation(lower,onset,variants[probe]['result']['termination_cap_pole_curvature_scale'])
        roundtrip=rt.controlled_native_cap_pole_scale_edit_test(template,delta_scale=0.005)
    else:
        probe=None; roundtrip={'pass':False,'checks':{'machine_pass_variant_required':False}}

    surface_runtime,runtime=iso.load_surface_runtime(binding); scene=bpy.context.scene
    surface_runtime.render_setup(scene,execution['runtime'],a.resolution); scene.view_settings.exposure=-1.20
    dc=bpy.data.collections.get(binding['surface_evaluation']['derived_collection']); qc=bpy.data.collections.get(binding['surface_evaluation']['qa_collection'])
    if dc is None or qc is None: raise RuntimeError('Derived/QA collections missing')
    control_obj,vc,fc=r451.replace_object('OL_DERIVED_G1_R4_5_1B_SCALE_0_90_CONTROL',control_source,dc)
    local=contract['local_view']; target=r45.axis_point(control_source,float(local['target_u'])); off=tuple(float(v) for v in local['offset_from_target_m']); loc=tuple(target[i]+off[i] for i in range(3))
    old=bpy.data.objects.get(local['name'])
    if old is not None: bpy.data.objects.remove(old,do_unlink=True)
    cam=surface_runtime.camera(local['name'],float(local['lens_mm']),loc,target,qc); cam['OLEANDER_R4_5_1B_ROLE']='SAME_DOF_REFINEMENT_CAMERA'
    iso.set_only_rendered(dc,control_obj)
    reference_id=contract['visual_reference']['id']; renders={reference_id:r451.render_set(surface_runtime,binding,out,qc,control_obj,cam,'R4_5_1B_SCALE_0_90_CONTROL')}
    geometry={reference_id:{'vertices':vc,'faces':fc,'authority':control_obj.get('OLEANDER_AUTHORITY'),'source_digest':iso.source_digest(control_source)}}
    for vid in pass_ids:
        obj,vn,fn=r451.replace_object(f'OL_DERIVED_G1_R4_5_1B_{vid}',variants[vid]['source'],dc); iso.set_only_rendered(dc,obj)
        renders[vid]=r451.render_set(surface_runtime,binding,out,qc,obj,cam,f'R4_5_1B_{vid}')
        geometry[vid]={'vertices':vn,'faces':fn,'authority':obj.get('OLEANDER_AUTHORITY'),'source_digest':obj.get('OLEANDER_SOURCE_DIGEST')}
    diffs={vid:{rig:iso.image_difference(out/renders[reference_id][rig],out/renders[vid][rig]) for rig in ('BROAD','STRIP','GRAZING','ZEBRA')} for vid in pass_ids}
    ranked=sorted(pass_ids,key=lambda k:(variants[k]['result']['cap_turn_probe']['cap_region_max_normal_turn_deg'],variants[k]['result']['reflection_flow_concentration_ratio'],variants[k]['result']['cap_turn_probe']['near_pole_max_normal_turn_deg']))

    for k,v in original_deck.items(): deck[k]=v
    r451.clear_relation(lower)
    for k,v in original_extra.items(): lower[k]=v
    restored=rt.extract_native_source(template); restore_err=rt.source_difference(native_before,restored); restore_digest=iso.source_digest(restored)
    checks={
      'authorization_bound':True,
      'same_two_dof_relation_only':int(contract['relation_vocabulary']['numeric_dof_count'])==2 and contract['policy']['third_numeric_cap_dof_forbidden'] is True,
      'onset_locked_at_0_88':abs(onset-.88)<=1e-12,
      'control_0_90_machine_pass':control_result['machine_pass'],
      'native_scale_roundtrip_pass':bool(roundtrip.get('pass')),
      'shared_surface_runtime_pass':runtime['status']=='PASS' and all(runtime['checks'].values()),
      'at_least_one_refinement_machine_pass':len(pass_ids)>0,
      'only_machine_pass_candidates_rendered':set(renders)-{reference_id}==set(pass_ids),
      'derived_not_authority':all(x['authority']=='DERIVED_EXECUTION_NOT_AUTHORITY' for x in geometry.values()),
      'native_source_restored_exactly':digest_before==restore_digest and max(restore_err.values())<=1e-12,
      'candidate_promotion_not_run':contract['policy']['candidate_promotion']=='NOT_RUN'
    }
    status='R4_5_1B_REFINEMENT_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'R4_5_1B_REFINEMENT_MACHINE_FAIL_REVISE'
    report={'schema':'oleander.modeling-worker.v0.13.g1.r4.5.1b.refinement-report.v1','status':status,'job_state':'R4_5_1B_REFINEMENT_EXECUTED','design_state':'REVISE','authority_state':'WORKING_SOURCE','candidate_review':'REOPENED','candidate_promotion':'NOT_RUN','global_checks':checks,'control':control_result,'variants':{k:v['result'] for k,v in variants.items()},'machine_pass_variants':pass_ids,'machine_ranked_variants':ranked,'roundtrip':roundtrip,'renders':renders,'geometry':geometry,'image_difference_metrics_vs_0_90_control':diffs,'surface_system_runtime':runtime,'visual_gate':contract['visual_gate'],'next_legal_action':'Review Machine-PASS .86/.88 against .90 control. Confirm only if terminal island/hook is materially reduced without near-pole pinch or onset/interface regression.','boundary':contract['boundary']}
    (out/'G1_R4_5_1B_CAP_CURVATURE_REFINEMENT_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8'); print(json.dumps(report,indent=2))
    return 0 if status.endswith('REQUIRED') else 15

if __name__=='__main__': raise SystemExit(main())
