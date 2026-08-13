#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R14 — Source Feature-Loop Topology

Accepted upstream state:
- R09 rearward cabin longitudinal package
- R11 transverse shoulder/mid/rocker tension
- R12 shape-preserving PCHIP longitudinal interpolation

R14 M3/M4 upgrade:
- wheel arch becomes explicit Source topology, not a Boolean cut;
- fender crown becomes an explicit outer feature loop;
- hood/top-edge, shoulder and rocker remain semantic longitudinal feature lines;
- front/rear terminations use controlled triangle fans (no n-gons);
- no global SubD, no Boolean, no M6/M7/M8 detail.

Designer F1 / M5 benchmark only. Not Class-A or engineering CAD.
"""
from __future__ import annotations
import importlib.util, bpy, bmesh, json, math, hashlib
from pathlib import Path

BASE="/tmp/revise_v011_r12.py"
spec=importlib.util.spec_from_file_location("r12",BASE)
r12=importlib.util.module_from_spec(spec);spec.loader.exec_module(r12)
r11=r12.r11; r10=r12.r10; r09=r11.r09; r08=r12.r08; b=r12.b

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R14"
r12.MODEL=MODEL; r11.MODEL=MODEL; r10.MODEL=MODEL; r09.MODEL=MODEL
r08.MODEL=MODEL; r08.r.MODEL=MODEL; b.MODEL=MODEL

ARCH_INNER_R=.405
ARCH_CROWN_R=.458
ARCH_ANGLES=[math.radians(v) for v in (15,27,39,51,63,75,90,105,117,129,141,153,165)]

def set_input(node,names,value):
    if isinstance(names,str): names=[names]
    for k in names:
        s=node.inputs.get(k)
        if s is not None:
            s.default_value=value
            return

def diagnostic_glass():
    m=bpy.data.materials.new("MAT_SEMANTIC_GLAZING_DIAG_R14");m.use_nodes=True
    nt=m.node_tree;nt.nodes.clear()
    out=nt.nodes.new("ShaderNodeOutputMaterial");bs=nt.nodes.new("ShaderNodeBsdfPrincipled")
    set_input(bs,"Base Color",(0.012,.025,.032,1));set_input(bs,"Roughness",.16)
    set_input(bs,["Transmission Weight","Transmission"],.08);set_input(bs,"IOR",1.45)
    nt.links.new(bs.outputs["BSDF"],out.inputs["Surface"])
    return m

def feature_mat(name,color):
    return b.mat(name,color,.24,0,(color,2.0))

def interp_row(row,x):
    if x >= row[0][0]: return row[0]
    if x <= row[-1][0]: return row[-1]
    for p1,p2 in zip(row[:-1],row[1:]):
        if p1[0] >= x >= p2[0]:
            t=(p1[0]-x)/(p1[0]-p2[0])
            return (x,p1[1]+(p2[1]-p1[1])*t,p1[2]+(p2[2]-p1[2])*t)
    raise ValueError(x)

def union_xs(rows):
    xs={round(p[0],9) for p in rows[0]}
    for wx in (b.FX,b.RX):
        for a in ARCH_ANGLES:
            xs.add(round(wx+ARCH_CROWN_R*math.cos(a),9))
    return sorted(xs,reverse=True)

class MB:
    def __init__(self):
        self.verts=[];self.faces=[];self.face_mat=[];self.keys={}
    def v(self,key,co):
        if key in self.keys:return self.keys[key]
        i=len(self.verts);self.verts.append(tuple(co));self.keys[key]=i;return i
    def f(self,ids,mat=0):
        self.faces.append(tuple(ids));self.face_mat.append(mat)

def build_source(rows,M,glass):
    xs=union_xs(rows)
    sampled=[[interp_row(row,x) for x in xs] for row in rows]
    mb=MB()
    def K(i,row,side): return f"X{i}:{row}:S{side:+d}"
    def V(i,row,side):
        p=sampled[row][i]
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))

    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0)
                b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1)
                glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22 <= cx <= .72
                mb.f(ids,1 if glass_band else 0)

    def arch_z(wx,x,r):
        dx=x-wx
        if abs(dx)>=r:return None
        return b.WZ+math.sqrt(max(r*r-dx*dx,0.0))
    def in_wheel_zone(cx):
        return any(abs(cx-wx) < ARCH_CROWN_R*.985 for wx in (b.FX,b.RX))

    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((4,5),(5,6),(6,7)):
                pts=[sampled[arow][i],sampled[arow][i+1],sampled[brow][i+1],sampled[brow][i]]
                cz=sum(p[2] for p in pts)/4
                skip=False
                if (arow,brow)==(4,5) and in_wheel_zone(cx):
                    skip=True
                else:
                    for wx in (b.FX,b.RX):
                        zlim=arch_z(wx,cx,ARCH_CROWN_R)
                        if zlim is not None and cz < zlim: skip=True
                if skip:continue
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side)
                mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)

    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        if in_wheel_zone(cx):continue
        rp0=V(i,7,1);rp1=V(i+1,7,1);lp1=V(i+1,7,-1);lp0=V(i,7,-1)
        mb.f((rp0,rp1,lp1,lp0),0)

    arch_meta=[]
    for wx,wname in ((b.FX,"F"),(b.RX,"R")):
        for side in (1,-1):
            sname="L" if side>0 else "R"
            shoulder_ids=[];crown_ids=[];inner_ids=[]
            for ai,a in enumerate(ARCH_ANGLES):
                x=wx+ARCH_CROWN_R*math.cos(a)
                gi=min(range(len(xs)),key=lambda j:abs(xs[j]-x))
                sp=sampled[4][gi]
                shoulder_ids.append(V(gi,4,side))
                bulge=.014*math.sin(a)**1.5
                crown=(x,side*(sp[1]+bulge),b.WZ+ARCH_CROWN_R*math.sin(a))
                xi=wx+ARCH_INNER_R*math.cos(a)
                spi=interp_row(rows[4],xi)
                inner=(xi,side*(spi[1]+.004*math.sin(a)),b.WZ+ARCH_INNER_R*math.sin(a))
                crown_ids.append(mb.v(f"ARCH:{wname}:{sname}:CROWN:{ai}",crown))
                inner_ids.append(mb.v(f"ARCH:{wname}:{sname}:INNER:{ai}",inner))
            for ai in range(len(ARCH_ANGLES)-1):
                ids=(shoulder_ids[ai],shoulder_ids[ai+1],crown_ids[ai+1],crown_ids[ai])
                mb.f(ids if side>0 else tuple(reversed(ids)),0)
                ids=(crown_ids[ai],crown_ids[ai+1],inner_ids[ai+1],inner_ids[ai])
                mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,crown_ids,inner_ids))

    for i,label,reverse in ((0,"FRONT",False),(len(xs)-1,"REAR",True)):
        outline=[V(i,7,1),V(i,6,1),V(i,5,1),V(i,4,1),V(i,3,1),V(i,2,1),V(i,1,1),V(i,0,0),V(i,1,-1),V(i,2,-1),V(i,3,-1),V(i,4,-1),V(i,5,-1),V(i,6,-1),V(i,7,-1)]
        co=[mb.verts[k] for k in outline]
        ci=mb.v(f"TERM:{label}:CENTER",(xs[i],0,sum(p[2] for p in co)/len(co)))
        for j in range(len(outline)-1):
            tri=(ci,outline[j],outline[j+1]);mb.f(tuple(reversed(tri)) if reverse else tri,0)
        lc=mb.v(f"TERM:{label}:LOWER_CENTER",(xs[i],0,sampled[7][i][2]))
        mb.f((ci,outline[-1],lc) if not reverse else (ci,lc,outline[-1]),0)
        mb.f((ci,lc,outline[0]) if not reverse else (ci,outline[0],lc),0)

    me=bpy.data.meshes.new("PRIMARY_FEATURE_SOURCE_MESH");me.from_pydata(mb.verts,[],mb.faces);me.update()
    o=bpy.data.objects.new("PRIMARY_FEATURE_SOURCE",me);bpy.context.collection.objects.link(o)
    o.data.materials.append(M["CLAY"]);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o["OLEANDER_AUTHORITY"]="WORKING_SOURCE";o["OLEANDER_TOPOLOGY"]="R14_FEATURE_LOOP"
    o["OLEANDER_BOOLEAN_ON_SOURCE"]=False;o["OLEANDER_SUBD_ON_SOURCE"]=False
    return o,xs,sampled,arch_meta

def curve(name,pts,ma,depth=.006):
    cu=bpy.data.curves.new(name+"_CURVE","CURVE");cu.dimensions="3D";cu.bevel_depth=depth;cu.bevel_resolution=2
    sp=cu.splines.new("POLY");sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts):p.co=(*co,1.0)
    o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.data.materials.append(ma);o.hide_render=True
    return o

def feature_guides(sampled,M):
    FM={"hood":feature_mat("MAT_FEATURE_HOOD",(.92,.24,.02,1)),"shoulder":feature_mat("MAT_FEATURE_SHOULDER",(.04,.36,1,1)),"rocker":feature_mat("MAT_FEATURE_ROCKER",(.12,.75,.20,1)),"crown":feature_mat("MAT_FEATURE_CROWN",(1,.06,.32,1)),"arch":feature_mat("MAT_FEATURE_ARCH",(1,.55,.02,1))}
    objs=[]
    for side in (1,-1):
        objs.append(curve(f"FEATURE_HOOD_TOPEDGE_{side:+}",[(p[0],side*p[1],p[2]) for p in sampled[1] if p[0]>=.72],FM["hood"],.006))
        objs.append(curve(f"FEATURE_SHOULDER_{side:+}",[(p[0],side*p[1],p[2]) for p in sampled[4]],FM["shoulder"],.005))
        objs.append(curve(f"FEATURE_ROCKER_{side:+}",[(p[0],side*p[1],p[2]) for p in sampled[6]],FM["rocker"],.005))
    return objs,FM

def append_arch_feature_curves(source,arch_meta,objs,FM):
    for wname,sname,cids,iids in arch_meta:
        objs.append(curve(f"FEATURE_FENDER_CROWN_{wname}{sname}",[source.data.vertices[i].co[:] for i in cids],FM["crown"],.007))
        objs.append(curve(f"FEATURE_WHEEL_ARCH_{wname}{sname}",[source.data.vertices[i].co[:] for i in iids],FM["arch"],.006))

def wire_overlay(source,M):
    w=source.copy();w.data=source.data.copy();w.name="SOURCE_WIREFRAME_DIAG";bpy.context.collection.objects.link(w)
    w.data.materials.clear();w.data.materials.append(M["BLACK"]);w.hide_render=True
    md=w.modifiers.new("WIREFRAME_DIAG","WIREFRAME");md.thickness=.0045;md.use_replace=True
    return w

def source_hash(o):
    h=hashlib.sha256()
    for v in o.data.vertices:h.update(f"{v.co.x:.9f},{v.co.y:.9f},{v.co.z:.9f};".encode())
    for p in o.data.polygons:h.update((",".join(map(str,p.vertices[:]))+";").encode())
    return h.hexdigest()

def topology_stats(o):
    tri=quad=ngon=0
    for p in o.data.polygons:
        n=len(p.vertices)
        if n==3:tri+=1
        elif n==4:quad+=1
        else:ngon+=1
    bm=bmesh.new();bm.from_mesh(o.data);boundary=sum(1 for e in bm.edges if len(e.link_faces)==1);nonmanifold=sum(1 for e in bm.edges if not e.is_manifold);bm.free()
    return {"vertices":len(o.data.vertices),"edges":len(o.data.edges),"faces":len(o.data.polygons),"tri":tri,"quad":quad,"ngon":ngon,"boundary_edges":boundary,"nonmanifold_edges":nonmanifold}

def render_matrix(out,samples,res,M,L,source,features,sections,wire):
    rd=out/"renders";rd.mkdir(parents=True,exist_ok=True);R=[]
    V=[("SIDE_SILHOUETTE",(0,-8.8,1.14),(0,0,.64),85,True,5.25,"BROAD","sil"),("PACKAGE_SIDE",(0,-8.8,1.14),(0,0,.64),85,True,5.25,"BROAD","normal"),("TOP_ORTHO",(0,0,8),(0,0,.56),85,True,5.35,"BROAD","normal"),("FRONT_ORTHO",(7.7,0,1.13),(0,0,.65),85,True,2.65,"BROAD","normal"),("HERO_FRONT_3Q",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"BROAD","normal"),("CLAY_STRIP",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"STRIP","normal"),("CLAY_GRAZING",(6.2,-7.0,2.75),(.05,0,.66),78,False,5,"GRAZING","normal"),("SECTION_OVERLAY",(5.8,-6.4,3.0),(0,0,.70),80,False,5,"BROAD","section"),("FEATURE_TOPOLOGY",(5.5,-6.2,2.45),(.10,0,.62),82,False,5,"BROAD","feature"),("SOURCE_WIREFRAME",(5.8,-6.4,2.8),(0,0,.66),80,False,5,"BROAD","wire"),("FRONT_ARCH_DETAIL",(2.65,-3.4,.95),(b.FX,-b.WY,.48),100,False,5,"STRIP","normal"),("REAR_ARCH_DETAIL",(-2.55,-3.4,.95),(b.RX,-b.WY,.48),100,False,5,"STRIP","normal")]
    for lab,loc,t,lens,ortho,scale,rig,mode in V:
        b.setrig(L,rig)
        for o in features:o.hide_render=(mode!="feature")
        for o in sections:o.hide_render=(mode!="section")
        wire.hide_render=(mode!="wire");source.hide_render=(mode=="wire")
        b.world((1,1,1),.75) if mode=="sil" else b.world((.012,.012,.012),.16)
        bpy.context.view_layer.material_override=M["BLACK"] if mode=="sil" else None
        c=b.camera("CAM_"+lab,loc,t,lens,ortho,scale);bpy.context.scene.camera=c
        p=rd/f"{MODEL}__{lab}.png";b.setup(p,samples,res);bpy.ops.render.render(write_still=True);R.append({"view":lab,"file":str(p),"mode":mode});bpy.data.objects.remove(c,do_unlink=True)
    bpy.context.view_layer.material_override=None;source.hide_render=False
    return R

def write_contract(out,source,stats,feature_count):
    c={"contract_version":"v0.2","spec_patch":"v0.2.1","job_id":"SYS-MODELING-WORKER-AUTO-M3M5-v0.11-R14","domain":"AUTOMOTIVE","decision_question":"Can the accepted R09/R11/R12 proportion-and-section state be rebuilt with explicit source-authority wheel-arch/fender feature loops and longitudinal feature lines, eliminating derived Boolean dependence while preserving coherent M5 surface flow?","loop":"CANONICAL_PRODUCTION","fidelity":"F1_DESIGN_VALIDATION","design_state":"REVISE","source_authority":{"state":"WORKING_SOURCE","editable_source":f"{MODEL}.blend","artifact_hash":source_hash(source),"derived_models":["SOURCE_WIREFRAME_DIAG"],"exports":[]},"modeling_stage":"M5","hard_points":{"applicable":True,"not_applicable_reason":None,"items":[{"id":"HP-WHEELBASE","role":"R09 locked axle relation","value":2.82,"unit":"m","status":"LOCKED"},{"id":"HP-TRACK","role":"R09 locked stance","value":1.59,"unit":"m","status":"LOCKED"},{"id":"HP-WHEEL-OD","role":"R09 locked wheel scale","value":.70,"unit":"m","status":"LOCKED"},{"id":"HP-COWL","role":"R09 accepted cabin placement","value":[.72,.90],"unit":"m","status":"LOCKED"},{"id":"HP-ROOF","role":"R09 accepted roof peak","value":[-.24,1.45],"unit":"m","status":"LOCKED"}]},"envelopes":{"applicable":True,"not_applicable_reason":None,"items":[{"id":"ENV-EXTERIOR","role":"feature-loop primary source envelope","geometry_type":"open source mesh with integrated wheel openings","source":"R09/R11/R12 controls + R14 feature topology","status":"OPEN"}]},"sections":{"applicable":True,"not_applicable_reason":None,"items":[{"id":f"SEC-{i:02d}","role":"R11 locked transverse section","station":s[0],"plane":"YZ","continuity_target":"R12 PCHIP + R14 local feature topology","depends_on":["HP-WHEELBASE","HP-TRACK"],"status":"DEPENDENCY_LOCKED"} for i,s in enumerate(b.SECTIONS)]},"primary_geometry":[{"id":"PG-FEATURE-SOURCE","role":"primary source with explicit feature loops","representation":"shared mesh; quads + controlled termination triangles; no n-gons/Boolean/SubD","source_sections":[f"SEC-{i:02d}" for i in range(len(b.SECTIONS))],"status":"OPEN"}],"semantic_components":[{"id":"ASY-VEHICLE","role":"automotive benchmark","parent":None,"source_type":"EDITABLE_SOURCE","source_ref":MODEL,"parameters":b.HP,"instance_rule":None,"authority_state":"WORKING_SOURCE"},{"id":"COMP-PRIMARY-FEATURE-SOURCE","role":"R14 editable primary source","parent":"ASY-VEHICLE","source_type":"EDITABLE_SOURCE","source_ref":"PG-FEATURE-SOURCE","parameters":{"topology_stats":stats,"feature_curve_count":feature_count},"instance_rule":"bilateral topology with four semantic wheel-arch loops","authority_state":"WORKING_SOURCE"}],"dependencies":[{"from":"HP-WHEELBASE","to":"PG-FEATURE-SOURCE","type":"DESIGN"},{"from":"HP-COWL","to":"PG-FEATURE-SOURCE","type":"DESIGN"},{"from":"PG-FEATURE-SOURCE","to":"COMP-PRIMARY-FEATURE-SOURCE","type":"GEOMETRY"}],"locks":[{"target":"R09 longitudinal package + R11 transverse tension + R12 PCHIP","state":"DEPENDENCY_LOCKED","reason":"R14 tests topology construction; upstream geometry may reopen only if R14 reveals genuine relation failure","unlock_trigger":"M5 Visual QA"},{"target":"M6/M7/M8 secondary/detail geometry","state":"LOCKED","reason":"M5 not promoted","unlock_trigger":"future M5 promotion"}],"revision":{"revision_id":"R14-SOURCE-FEATURE-LOOPS","semantic_targets":["PG-FEATURE-SOURCE"],"parameters":{"wheel_arch_inner_radius_m":ARCH_INNER_R,"fender_crown_radius_m":ARCH_CROWN_R,"arch_samples":len(ARCH_ANGLES),"source_boolean":False,"source_subd":False},"expected_affected_components":["COMP-PRIMARY-FEATURE-SOURCE"],"affected_view_policy":"HYBRID"},"qa":{"integrity":["Blender runtime","source exists","12 renders","wheel package locked"],"construction":["source n-gon count = 0","source has no Boolean modifier","source has no Subdivision modifier","four inner wheel-arch loops","four outer fender-crown loops","front/rear controlled termination triangles only"],"design_geometry":["wheel/body stance","front/rear fender crown relationship","hood/top-edge feature line","shoulder/rocker hierarchy","Side/Top/Front/Hero","Strip/Grazing flow"],"project":["M6/M7/M8 remains blocked","semantic glazing is diagnostic only","do not promote if feature topology creates patching/pinching"],"diagnostic_views":["SIDE_SILHOUETTE","PACKAGE_SIDE","TOP_ORTHO","FRONT_ORTHO","HERO_FRONT_3Q","CLAY_STRIP","CLAY_GRAZING","SECTION_OVERLAY","FEATURE_TOPOLOGY","SOURCE_WIREFRAME","FRONT_ARCH_DETAIL","REAR_ARCH_DETAIL"]},"resource_budget":{"max_variants":3,"max_iterations":3,"max_runtime_minutes":25,"max_render_views":12,"max_geometry_density":None,"parallelism":1},"cache":{"enabled":True,"scope":"PROJECT_LOCAL","key_inputs":["R09/R11/R12 controls","R14 feature topology","Blender version","builder commit"]},"exit_condition":"Source wheel arches and fender crowns read as part of the primary form in multi-view/Strip/Grazing diagnostics without Boolean artifacts, seam-like patching or detail assistance.","promotion":{"eligible_authority_states":["WORKING_SOURCE","CANDIDATE_AUTHORITY"],"worker_may_mutate_source_authority":False,"decision":"PENDING"},"persistence":{"policy":"PROMOTION_ONLY","artifact_registry":True,"sync_targets":["NOTION","GITHUB","GOOGLE_DRIVE"]},"material_bindings":[{"target_component":"COMP-PRIMARY-FEATURE-SOURCE","material_or_preset":"MAT_PRIMARY_CLAY + MAT_SEMANTIC_GLAZING_DIAG_R14","binding_scope":"REFERENCE_ONLY","coordinate_dependency":None,"directionality":None,"scale_semantics":"M5 diagnostic only","status":"BOUND"}]}
    (out/"MODELING_CONTRACT.json").write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();glass=diagnostic_glass();rows=b.controls_resampled()
    source,xs,sampled,arch_meta=build_source(rows,M,glass);h0=source_hash(source)
    features,FM=feature_guides(sampled,M);append_arch_feature_curves(source,arch_meta,features,FM)
    sections=b.guides(b.controls_resampled(),M);b.wheels(M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16);wire=wire_overlay(source,M);h1=source_hash(source)
    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5";scene["OLEANDER_UPSTREAM"]="R09 cabin + R11 transverse tension + R12 PCHIP";scene["OLEANDER_SOURCE_BOOLEAN"]=False;scene["OLEANDER_SOURCE_SUBD"]=False
    stats=topology_stats(source);write_contract(out,source,stats,len(features));blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));R=render_matrix(out,a.samples,a.resolution,M,L,source,features,sections,wire)
    mn,mx=b.bbox(source);modifiers=[m.type for m in source.modifiers];feature_names=[o.name for o in features]
    checks={"source_hash_stable_during_diagnostics":h0==h1,"length":4.60<=mx.x-mn.x<=4.70,"width":1.80<=mx.y-mn.y<=1.95,"height":1.42<=mx.z<=1.47,"wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.59)<1e-8,"source_ngon_zero":stats["ngon"]==0,"controlled_triangles_only":stats["tri"]>0 and stats["tri"]<=80,"source_no_boolean":"BOOLEAN" not in modifiers,"source_no_subd":"SUBSURF" not in modifiers,"four_arch_boundaries":len([n for n in feature_names if "FEATURE_WHEEL_ARCH_" in n])==4,"four_fender_crowns":len([n for n in feature_names if "FEATURE_FENDER_CROWN_" in n])==4,"hood_feature_lines":len([n for n in feature_names if "FEATURE_HOOD_TOPEDGE_" in n])==2,"shoulder_feature_lines":len([n for n in feature_names if "FEATURE_SHOULDER_" in n])==2,"premature_detail_absent":not any(any(k in o.name for k in ["HANDLE","LAMP","MIRROR","SEAT","SCREEN","WIPER","CALIPER","SPOKE"]) for o in bpy.context.scene.objects),"render_matrix":len(R)==12}
    q={"schema":"oleander.auto.v0.11.r14.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL","source_hash_before_diagnostics":h0,"source_hash_after_diagnostics":h1,"bounds":{"min":list(mn),"max":list(mx),"dimensions":[mx.x-mn.x,mx.y-mn.y,mx.z-mn.z]},"topology":stats,"source_modifiers":modifiers,"feature_names":feature_names,"checks":checks,"renders":R,"boundary":"R14 promotes wheel-arch/fender feature topology into WORKING_SOURCE only. M5 visual quality is not pre-approved; M6/M7/M8 remains blocked."}
    (out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");rec={"schema":"oleander.auto.v0.11.r14.receipt","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R};(out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)
if __name__=="__main__":main()
