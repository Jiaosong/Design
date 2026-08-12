#!/usr/bin/env python3
"""OLEANDER Automotive Primary Surface v0.8 — R03 integrated-shell revision.

R02 visual review proved that BODY_PRIMARY + CABIN_PRIMARY as two closed solids causes
an unavoidable hat/pillbox reading. R03 triggers the Modeling Contract v0.2.1
CONDITIONALLY_UNLOCKABLE rule for the body-cabin interface.

Locked: wheelbase, track, wheel centers, wheel/tire guide size, lower-body section values.
Rebuilt: upper body + cabin as one continuous primary shell; glazing becomes material zones
on that same shell rather than a second large closed volume.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import bpy, bmesh

ap=argparse.ArgumentParser();ap.add_argument('--base-source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--samples',type=int,default=8);ap.add_argument('--resolution',type=int,default=640)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];a=ap.parse_args(av)
src=Path(a.base_source).read_text(encoding='utf-8');defs=src.split('if __name__=="__main__":')[0];exec(compile(defs,a.base_source,'exec'),globals(),globals())
MODEL='OLEANDER_Automotive_Primary_Surface_v0.8';REV='R03'
TOP_PROFILE={-2.21:(.65,.20,.63,.38,.61),-2.10:(.74,.25,.72,.48,.69),-1.92:(.81,.28,.79,.55,.76),-1.72:(.92,.32,.90,.46,.86),-1.52:(1.10,.34,1.08,.50,1.00),-1.36:(1.25,.42,1.24,.56,1.15),-1.12:(1.34,.48,1.33,.60,1.25),-.75:(1.415,.55,1.405,.635,1.35),-.30:(1.430,.575,1.420,.640,1.375),.15:(1.415,.56,1.405,.635,1.35),.55:(1.340,.49,1.330,.60,1.25),.88:(1.135,.35,1.120,.51,1.045),1.15:(.90,.31,.885,.58,.865),1.36:(.87,.29,.855,.60,.84),1.62:(.84,.27,.825,.58,.80),1.88:(.78,.25,.765,.54,.73),2.08:(.74,.23,.725,.46,.67),2.21:(.65,.19,.635,.36,.60)}

def shell_ring(sec):
    x,wr,wl,ws,wb,zr,zl,zs,zb,zt=sec;rc,rw,rz,uw,uz=TOP_PROFILE[round(x,2)]
    pts=[(0.0,rc),(rw,rz),(uw,uz),(wb,zb),(ws,zs),(wl,zl),(wr,zr),(.58,.158),(0.0,.145),(-.58,.158),(-wr,zr),(-wl,zl),(-ws,zs),(-wb,zb),(-uw,uz),(-rw,rz)]
    return [(x,y,z) for y,z in pts]

def integrated_loft(name,sections,body_mat,glass_mat,subdiv=2):
    rings=[shell_ring(s) for s in sections];verts=[];faces=[];midx=[];rows=[];n=len(rings[0])
    for ring in rings:
        row=[]
        for p in ring:row.append(len(verts));verts.append(p)
        rows.append(row)
    for i,(ra,rb) in enumerate(zip(rows[:-1],rows[1:])):
        xa=sections[i][0];xb=sections[i+1][0];xm=(xa+xb)/2
        for j in range(n):
            k=(j+1)%n;faces.append((ra[j],ra[k],rb[k],rb[j]));mi=0
            if -1.52 <= xm <= .88 and j in (2,13):mi=1
            if .88 < xm < 1.15 and j in (0,1,2,13,14,15):mi=1
            if -1.72 < xm < -1.52 and j in (0,1,2,13,14,15):mi=1
            midx.append(mi)
    for row,rev in [(rows[0],True),(rows[-1],False)]:
        c=[sum(verts[ii][d] for ii in row)/n for d in range(3)];ci=len(verts);verts.append(tuple(c))
        for j in range(n):
            k=(j+1)%n;faces.append((ci,row[k],row[j]) if rev else (ci,row[j],row[k]));midx.append(0)
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();cage=bpy.data.objects.new(name+'_CAGE',me);bpy.context.collection.objects.link(cage);cage.data.materials.append(body_mat);cage.data.materials.append(glass_mat)
    for p,mi in zip(cage.data.polygons,midx):p.material_index=mi;p.use_smooth=True
    final=cage.copy();final.data=cage.data.copy();final.name=name;bpy.context.collection.objects.link(final);cage.hide_render=True;cage.hide_viewport=True
    md=final.modifiers.new('PRIMARY_SUBD','SUBSURF');md.levels=subdiv;md.render_levels=subdiv;bpy.context.view_layer.objects.active=final;bpy.ops.object.modifier_apply(modifier=md.name);return final,cage

def nm(o):
    bm=bmesh.new();bm.from_mesh(o.data);n=sum(1 for e in bm.edges if not e.is_manifold);bm.free();return n

def fs(o):
    q={'tri':0,'quad':0,'ngon':0}
    for p in o.data.polygons:
        n=len(p.vertices);q['tri' if n==3 else 'quad' if n==4 else 'ngon']+=1
    return q

def overlay(mats):
    out=[]
    for i,s in enumerate(BODY_SECTIONS):
        o=curve_poly(f'SEC_SHELL_{i:02d}',shell_ring(s),mats['SECTION'],.0045,True);o.hide_render=True;out.append(o)
    guides={'ROOF_CENTER':[(s[0],0,TOP_PROFILE[round(s[0],2)][0]) for s in BODY_SECTIONS],'ROOF_EDGE_POS':[(s[0],TOP_PROFILE[round(s[0],2)][1],TOP_PROFILE[round(s[0],2)][2]) for s in BODY_SECTIONS],'ROOF_EDGE_NEG':[(s[0],-TOP_PROFILE[round(s[0],2)][1],TOP_PROFILE[round(s[0],2)][2]) for s in BODY_SECTIONS],'BELT_POS':[(s[0],s[4],s[8]) for s in BODY_SECTIONS],'BELT_NEG':[(s[0],-s[4],s[8]) for s in BODY_SECTIONS],'SHOULDER_POS':[(s[0],s[3],s[7]) for s in BODY_SECTIONS],'SHOULDER_NEG':[(s[0],-s[3],s[7]) for s in BODY_SECTIONS]}
    for n,pts in guides.items():
        o=curve_poly('GUIDE_'+n,pts,mats['GUIDE'],.005,False);o.hide_render=True;out.append(o)
    return out

for o in list(bpy.data.objects):
    n=o.name
    if n.startswith(('BODY_PRIMARY','CABIN_PRIMARY','SIDE_GLASS_','B_PILLAR_','SEC_BODY_','SEC_CABIN_','SEC_SHELL_','GUIDE_')) or n in {'WINDSHIELD','REAR_GLASS','BODY_CONTROL_WIRE','CABIN_CONTROL_WIRE'}:bpy.data.objects.remove(o,do_unlink=True)
mats={'BODY':bpy.data.materials['MAT_PRIMARY_CLAY'],'GLASS':bpy.data.materials['MAT_GUIDE_GLASS'],'TIRE':bpy.data.materials['MAT_TIRE_GUIDE'],'RIM':bpy.data.materials['MAT_RIM_GUIDE'],'GROUND':bpy.data.materials['MAT_GROUND'],'SECTION':bpy.data.materials['MAT_SECTION'],'GUIDE':bpy.data.materials['MAT_GUIDE'],'CAGE':bpy.data.materials['MAT_CONTROL_CAGE'],'BLACK':bpy.data.materials.get('MAT_SILHOUETTE') or make_mat('MAT_SILHOUETTE',(0.002,0.002,0.002,1),.55,0)}
shell,cage=integrated_loft('BODY_PRIMARY',BODY_SECTIONS,mats['BODY'],mats['GLASS'],2);arch_cut(shell,FX);arch_cut(shell,RX);wire_objs=[make_wire_overlay(cage,'BODY_CONTROL_WIRE',mats['CAGE'])];section_objs=overlay(mats)
lights={'BROAD':[bpy.data.objects['BROAD_KEY'],bpy.data.objects['BROAD_FILL']],'STRIP':[bpy.data.objects['STRIP_KEY'],bpy.data.objects['STRIP_FILL']],'GRAZING':[bpy.data.objects['GRAZING_KEY'],bpy.data.objects['GRAZING_FILL']]}
out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);build_contract(out);cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-VAL-03-AUTO-PRIMARY-v0.8-R03';c['decision_question']='Can one continuous integrated primary shell establish coherent wheel/body/greenhouse/roof relationships before secondary details are introduced?';c['design_state']='REVISE';c['modeling_stage']='M6';c['sections']={'applicable':True,'not_applicable_reason':None,'items':[{'id':f'SEC-SHELL-{i:02d}','role':'integrated transverse body/roof control','station':s[0],'plane':'YZ','continuity_target':'continuous lower-body / belt / glazing / roof progression','depends_on':['HP-WHEELBASE','HP-TRACK','HP-COWL','HP-ROOF-PEAK','HP-BELT'],'status':'OPEN'} for i,s in enumerate(BODY_SECTIONS)]};c['primary_geometry']=[{'id':'PG-INTEGRATED-SHELL','role':'single continuous exterior primary shell','representation':'SubD integrated section-loft with material zoning','source_sections':[f'SEC-SHELL-{i:02d}' for i in range(len(BODY_SECTIONS))],'status':'OPEN'}];c['semantic_components']=[{'id':'ASY-VEHICLE','role':'automotive benchmark assembly','parent':None,'source_type':'EDITABLE_SOURCE','source_ref':MODEL,'parameters':{},'instance_rule':None,'authority_state':'WORKING_SOURCE'},{'id':'COMP-INTEGRATED-SHELL','role':'continuous body/greenhouse/roof primary shell','parent':'ASY-VEHICLE','source_type':'EDITABLE_SOURCE','source_ref':'PG-INTEGRATED-SHELL','parameters':{'body_cabin_interface':'continuous'},'instance_rule':'bilateral symmetry encoded in sections','authority_state':'WORKING_SOURCE'},{'id':'ASY-WHEEL-GUIDE','role':'hard-point wheel guide','parent':'ASY-VEHICLE','source_type':'GENERATOR','source_ref':'wheel_placeholder','parameters':{'outer_diameter_m':HARD['wheel_outer_radius_m']*2},'instance_rule':'4 locked positions','authority_state':'WORKING_SOURCE'},{'id':'COMP-GLAZING-ZONES','role':'glazing zones on integrated shell','parent':'COMP-INTEGRATED-SHELL','source_type':'DERIVED_MODEL','source_ref':'integrated-shell material indices','parameters':{},'instance_rule':'symmetric side zones + front/rear transition','authority_state':'NONE'}];c['dependencies']=[{'from':'HP-WHEELBASE','to':'SEC-SHELL-05','type':'DESIGN'},{'from':'HP-COWL','to':'PG-INTEGRATED-SHELL','type':'DESIGN'},{'from':'HP-ROOF-PEAK','to':'PG-INTEGRATED-SHELL','type':'DESIGN'},{'from':'PG-INTEGRATED-SHELL','to':'COMP-INTEGRATED-SHELL','type':'GEOMETRY'},{'from':'COMP-INTEGRATED-SHELL','to':'COMP-GLAZING-ZONES','type':'GEOMETRY'}];c['locks']=[{'target':'wheelbase / track / wheel centers / wheel OD','state':'LOCKED','reason':'stance hard points retained from R01/R02','unlock_trigger':None},{'target':'lower-body section values below belt','state':'DEPENDENCY_LOCKED','reason':'R02 visual failure was at body-cabin architecture, not lower stance','unlock_trigger':'future M5 review demonstrates lower-body highlight/stance failure'},{'target':'body-cabin interface','state':'OPEN','reason':'R02 triggered conditional unlock because split closed volumes caused hat/pillbox reading','unlock_trigger':None},{'target':'secondary details','state':'LOCKED','reason':'M7/M8 blocked until integrated primary shell passes M5','unlock_trigger':None}];c['qa']['construction']=['integrated control cage has zero n-gons','single primary shell is manifold after wheel openings','no split cabin closed volume remains','section network controls lower body through roof','no behavior-sensitive pinching visible in Broad/Strip/Grazing'];c['qa']['design_geometry']=['side silhouette','wheel/body stance','continuous hood/windshield/roof/rear trajectory','greenhouse/body ratio','belt/shoulder/roof relation','front/rear width taper','Broad/Strip/Grazing highlight continuity'];c['material_bindings']=[{'target_component':'COMP-INTEGRATED-SHELL','material_or_preset':'MAT_PRIMARY_CLAY','binding_scope':'REFERENCE_ONLY','coordinate_dependency':None,'directionality':None,'scale_semantics':'surface diagnostic','status':'BOUND'},{'target_component':'COMP-GLAZING-ZONES','material_or_preset':'MAT_GUIDE_GLASS','binding_scope':'REFERENCE_ONLY','coordinate_dependency':'integrated shell face zones','directionality':None,'scale_semantics':'component readability only','status':'BOUND'}];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
scene=bpy.context.scene;scene['OLEANDER_MODEL']=MODEL;scene['OLEANDER_REVISION']=REV;scene['OLEANDER_REVISION_SCOPE']='integrated primary shell; body-cabin interface conditionally unlocked; stance hard points retained';blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));renders=render_matrix(out,a.samples,a.resolution,mats,lights,section_objs,wire_objs)
mn,mx=bbox([shell]);stats=fs(cage);premature=[o.name for o in bpy.context.scene.objects if any(k in o.name for k in ['HANDLE','HEADLAMP','TAILLAMP','SEAT_','SCREEN','CALIPER','MIRROR'])];checks={'length_corridor':4.35 <= (mx.x-mn.x) <= 4.50,'width_corridor':1.80 <= (mx.y-mn.y) <= 1.90,'height_corridor':1.38 <= mx.z <= 1.46,'wheelbase':abs((FX-RX)-HARD['wheelbase_m'])<1e-8,'track':abs(2*WY-HARD['track_m'])<1e-8,'integrated_shell_manifold':nm(shell)==0,'control_ngon_zero':stats['ngon']==0,'single_primary_shell':bpy.data.objects.get('CABIN_PRIMARY') is None,'section_count':len(BODY_SECTIONS)==18,'wheel_guides':len([o for o in bpy.context.scene.objects if o.name.endswith('_TIRE')])==4,'premature_detail_absent':len(premature)==0,'render_matrix':len(renders)==8};q={'schema':'oleander.automotive-primary-surface.qa.v0.8-r03','model':MODEL,'revision':REV,'status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL','hard_points':HARD,'primary_bounds_m':{'min':list(mn),'max':list(mx),'dimensions':[mx.x-mn.x,mx.y-mn.y,mx.z-mn.z]},'control_face_stats':stats,'nonmanifold':nm(shell),'premature_detail_objects':premature,'checks':checks,'renders':renders,'revision_scope':'Integrated primary shell. Body-cabin interface unlocked by R02 impact analysis; wheel stance and lower-body values retained.','evidence_boundary':'Machine/Construction pre-gate only. Visual M5 review required.'};(out/'AUTOMOTIVE_PRIMARY_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');rec={'schema':'oleander.automotive-primary-surface.receipt.v0.8-r03','model':MODEL,'revision':REV,'blender_version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),'renderer':'Cycles CPU','samples':a.samples,'resolution':[a.resolution,a.resolution],'status':'EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if q['status'].startswith('MACHINE_PASS') else 'EXECUTED_MACHINE_FAIL','blend':str(blend),'contract':str(cp),'qa':str(out/'AUTOMOTIVE_PRIMARY_QA.json'),'renders':renders};(out/'AUTOMOTIVE_PRIMARY_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if q['status'].startswith('MACHINE_PASS') else 5)
