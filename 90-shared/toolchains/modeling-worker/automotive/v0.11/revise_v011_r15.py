#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 R15 — Integrated Shoulder/Fender Feature Topology.

R14 Visual QA = REVISE.
Fixes:
- remove detached eyebrow-style outer fender crown;
- shoulder line becomes the local fender crown over each wheel;
- two explicit blend loops connect shoulder/crown to inner wheel-arch boundary;
- all lower side bands inside wheel zones are replaced by the fender patch;
- front/rear termination sections receive a local taper correction only.

Locked:
R09 cabin package + wheel hard points, R11 transverse body tension outside local wheel zones,
R12 PCHIP interpolation.
M6/M7/M8 remains blocked.
"""
from __future__ import annotations
import importlib.util,bpy,bmesh,json,math,hashlib
from pathlib import Path

BASE="/tmp/revise_v011_r14.py"
spec=importlib.util.spec_from_file_location("r14",BASE)
r14=importlib.util.module_from_spec(spec);spec.loader.exec_module(r14)
b=r14.b

MODEL="OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R15"
r14.MODEL=MODEL;r14.r12.MODEL=MODEL;r14.r11.MODEL=MODEL;r14.r10.MODEL=MODEL
r14.r09.MODEL=MODEL;r14.r08.MODEL=MODEL;r14.r08.r.MODEL=MODEL;b.MODEL=MODEL

ARCH_R=.405
ARCH_ZONE_R=.465
ANGLES=[math.radians(v) for v in (12,24,36,48,60,72,84,96,108,120,132,144,156,168)]

def taper_terminals():
    out=[]
    for s in b.SECTIONS:
        x,tz,te,bz,bw,sz,sw,mz,mw,rz,rw,uz,uw=s
        if x>2.16:
            k=max(0.45,1-(x-2.16)/.30*.35)
            te*=k;bw*=k;sw*=k;mw*=k;rw*=k;uw*=k
            tz-=.015;sz-=.010
        elif x<-2.16:
            k=max(0.48,1-(-2.16-x)/.30*.32)
            te*=k;bw*=k;sw*=k;mw*=k;rw*=k;uw*=k
            tz-=.010;sz-=.008
        out.append((x,tz,te,bz,bw,sz,sw,mz,mw,rz,rw,uz,uw))
    b.SECTIONS=out

taper_terminals()

def union_xs(rows):
    xs={round(p[0],9) for p in rows[0]}
    for wx in (b.FX,b.RX):
        for a in ANGLES:xs.add(round(wx+ARCH_ZONE_R*math.cos(a),9))
    return sorted(xs,reverse=True)

def shoulder_point(rows,x):
    p=r14.interp_row(rows[4],x);y,z=p[1],p[2]
    for wx in (b.FX,b.RX):
        dx=x-wx
        if abs(dx)<ARCH_ZONE_R:
            crown_z=b.WZ+math.sqrt(max(ARCH_ZONE_R**2-dx**2,0.0));lift=max(0.0,crown_z-z)
            if lift>0:
                z+=lift*.78;y+=min(.022,lift*.12)
    return (x,y,z)

def build_source(rows,M,glass):
    xs=union_xs(rows);sampled=[[r14.interp_row(row,x) for x in xs] for row in rows];shoulder=[shoulder_point(rows,x) for x in xs];mb=r14.MB()
    def K(i,row,side):return f"X{i}:{row}:S{side:+d}"
    def V(i,row,side):
        p=shoulder[i] if row==4 else sampled[row][i]
        if row==0:return mb.v(K(i,row,0),(p[0],0,p[2]))
        return mb.v(K(i,row,side),(p[0],side*p[1],p[2]))
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        for side in (1,-1):
            for arow,brow in ((0,1),(1,2),(2,3),(3,4)):
                a0=V(i,arow,side if arow else 0);a1=V(i+1,arow,side if arow else 0);b1=V(i+1,brow,side);b0=V(i,brow,side)
                ids=(a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1);glass_band=(arow,brow) in ((1,2),(2,3)) and -1.22<=cx<=.72;mb.f(ids,1 if glass_band else 0)
    def in_zone(x):return any(abs(x-wx)<ARCH_ZONE_R*.995 for wx in (b.FX,b.RX))
    for i in range(len(xs)-1):
        cx=(xs[i]+xs[i+1])/2
        if in_zone(cx):continue
        for side in (1,-1):
            for arow,brow in ((4,5),(5,6),(6,7)):
                a0=V(i,arow,side);a1=V(i+1,arow,side);b1=V(i+1,brow,side);b0=V(i,brow,side);mb.f((a0,a1,b1,b0) if side>0 else (a0,b0,b1,a1),0)
        rp0=V(i,7,1);rp1=V(i+1,7,1);lp1=V(i+1,7,-1);lp0=V(i,7,-1);mb.f((rp0,rp1,lp1,lp0),0)
    arch_meta=[]
    for wx,wname in ((b.FX,"F"),(b.RX,"R")):
        for side in (1,-1):
            sname="L" if side>0 else "R";crown_ids=[];blend1_ids=[];blend2_ids=[];inner_ids=[]
            for ai,a in enumerate(ANGLES):
                x=wx+ARCH_ZONE_R*math.cos(a);gi=min(range(len(xs)),key=lambda j:abs(xs[j]-x));sp=shoulder[gi]
                crown=mb.v(f"ARCH:{wname}:{sname}:CROWN:{ai}",(sp[0],side*sp[1],sp[2]));xi=wx+ARCH_R*math.cos(a);base=r14.interp_row(rows[4],xi)
                inner=(xi,side*(base[1]+.0035*math.sin(a)),b.WZ+ARCH_R*math.sin(a));ii=mb.v(f"ARCH:{wname}:{sname}:INNER:{ai}",inner)
                c=mb.verts[crown];inn=mb.verts[ii];s=math.sin(a)
                b1=(c[0]*.70+inn[0]*.30,c[1]*.70+inn[1]*.30+side*.010*s,c[2]*.70+inn[2]*.30);b2=(c[0]*.34+inn[0]*.66,c[1]*.34+inn[1]*.66+side*.006*s,c[2]*.34+inn[2]*.66)
                crown_ids.append(crown);blend1_ids.append(mb.v(f"ARCH:{wname}:{sname}:B1:{ai}",b1));blend2_ids.append(mb.v(f"ARCH:{wname}:{sname}:B2:{ai}",b2));inner_ids.append(ii)
            for ai in range(len(ANGLES)-1):
                for A,B in ((crown_ids,blend1_ids),(blend1_ids,blend2_ids),(blend2_ids,inner_ids)):
                    ids=(A[ai],A[ai+1],B[ai+1],B[ai]);mb.f(ids if side>0 else tuple(reversed(ids)),0)
            arch_meta.append((wname,sname,crown_ids,inner_ids))
    for i,label,reverse in ((0,"FRONT",False),(len(xs)-1,"REAR",True)):
        outline=[V(i,7,1),V(i,6,1),V(i,5,1),V(i,4,1),V(i,3,1),V(i,2,1),V(i,1,1),V(i,0,0),V(i,1,-1),V(i,2,-1),V(i,3,-1),V(i,4,-1),V(i,5,-1),V(i,6,-1),V(i,7,-1)]
        co=[mb.verts[k] for k in outline];ci=mb.v(f"TERM:{label}:CENTER",(xs[i],0,sum(p[2] for p in co)/len(co)))
        for j in range(len(outline)-1):
            tri=(ci,outline[j],outline[j+1]);mb.f(tuple(reversed(tri)) if reverse else tri,0)
        lc=mb.v(f"TERM:{label}:LOWER_CENTER",(xs[i],0,sampled[7][i][2]));mb.f((ci,outline[-1],lc) if not reverse else (ci,lc,outline[-1]),0);mb.f((ci,lc,outline[0]) if not reverse else (ci,outline[0],lc),0)
    me=bpy.data.meshes.new("PRIMARY_INTEGRATED_FENDER_SOURCE_MESH");me.from_pydata(mb.verts,[],mb.faces);me.update();o=bpy.data.objects.new("PRIMARY_INTEGRATED_FENDER_SOURCE",me);bpy.context.collection.objects.link(o);o.data.materials.append(M["CLAY"]);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mb.face_mat):p.use_smooth=True;p.material_index=mi
    o["OLEANDER_AUTHORITY"]="WORKING_SOURCE";o["OLEANDER_TOPOLOGY"]="R15_INTEGRATED_SHOULDER_FENDER";return o,xs,sampled,shoulder,arch_meta

def feature_guides(source,sampled,shoulder,arch_meta,M):
    FM={"hood":r14.feature_mat("MAT_FEATURE_HOOD_R15",(.92,.24,.02,1)),"shoulder":r14.feature_mat("MAT_FEATURE_SHOULDER_R15",(.04,.36,1,1)),"rocker":r14.feature_mat("MAT_FEATURE_ROCKER_R15",(.12,.75,.20,1)),"crown":r14.feature_mat("MAT_FEATURE_CROWN_R15",(1,.06,.32,1)),"arch":r14.feature_mat("MAT_FEATURE_ARCH_R15",(1,.55,.02,1))};objs=[]
    for side in (1,-1):
        objs.append(r14.curve(f"FEATURE_HOOD_TOPEDGE_{side:+}",[(p[0],side*p[1],p[2]) for p in sampled[1] if p[0]>=.72],FM["hood"],.006));objs.append(r14.curve(f"FEATURE_SHOULDER_{side:+}",[(p[0],side*p[1],p[2]) for p in shoulder],FM["shoulder"],.005));objs.append(r14.curve(f"FEATURE_ROCKER_{side:+}",[(p[0],side*p[1],p[2]) for p in sampled[6]],FM["rocker"],.005))
    for wname,sname,cids,iids in arch_meta:
        objs.append(r14.curve(f"FEATURE_FENDER_CROWN_{wname}{sname}",[source.data.vertices[i].co[:] for i in cids],FM["crown"],.007));objs.append(r14.curve(f"FEATURE_WHEEL_ARCH_{wname}{sname}",[source.data.vertices[i].co[:] for i in iids],FM["arch"],.006))
    return objs

def main():
    a=b.parse();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);b.clear();M=b.materials();glass=r14.diagnostic_glass();rows=b.controls_resampled();source,xs,sampled,shoulder,arch_meta=build_source(rows,M,glass);h0=r14.source_hash(source)
    features=feature_guides(source,sampled,shoulder,arch_meta,M);sections=b.guides(b.controls_resampled(),M);b.wheels(M);b.ground(M);L=b.rigs();b.world((.012,.012,.012),.16);wire=r14.wire_overlay(source,M);h1=r14.source_hash(source);stats=r14.topology_stats(source)
    scene=bpy.context.scene;scene["OLEANDER_MODEL"]=MODEL;scene["OLEANDER_STAGE"]="M5";scene["OLEANDER_UPSTREAM"]="R09/R11/R12 + R15 local termination/fender integration"
    r14.write_contract(out,source,stats,len(features));cp=out/"MODELING_CONTRACT.json";c=json.loads(cp.read_text());c["job_id"]="SYS-MODELING-WORKER-AUTO-M3M5-v0.11-R15";c["decision_question"]="Does integrating the wheel crown directly into the shoulder feature line, with two blend loops to the inner wheel-arch boundary, remove the detached R14 eyebrow failure while preserving the accepted cabin/body package?";c["source_authority"]["editable_source"]=f"{MODEL}.blend";c["primary_geometry"][0]["id"]="PG-INTEGRATED-FENDER-SOURCE";c["primary_geometry"][0]["role"]="primary source with integrated shoulder/fender/arch topology";c["semantic_components"][1]["id"]="COMP-INTEGRATED-FENDER-SOURCE";c["semantic_components"][1]["role"]="R15 editable primary source";c["semantic_components"][1]["source_ref"]="PG-INTEGRATED-FENDER-SOURCE";c["revision"]={"revision_id":"R15-INTEGRATED-FENDER","semantic_targets":["PG-INTEGRATED-FENDER-SOURCE"],"parameters":{"R14_detached_crown":"removed","shoulder_local_crown":"enabled","blend_loops":2,"inner_arch_radius_m":ARCH_R,"wheel_zone_radius_m":ARCH_ZONE_R,"terminal_taper":"local only"},"expected_affected_components":["COMP-INTEGRATED-FENDER-SOURCE"],"affected_view_policy":"HYBRID"};c["qa"]["project"]=["R14 eyebrow/cap reading must be closed","wheel arch must read as body-side topology, not applied trim","front/rear local taper must not alter cabin/wheel hard points","M6/M7/M8 remains blocked"];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n")
    blend=out/f"{MODEL}.blend";bpy.ops.wm.save_as_mainfile(filepath=str(blend));R=r14.render_matrix(out,a.samples,a.resolution,M,L,source,features,sections,wire);mn,mx=b.bbox(source);mods=[m.type for m in source.modifiers];names=[o.name for o in features]
    checks={"source_hash_stable_during_diagnostics":h0==h1,"length":4.60<=mx.x-mn.x<=4.70,"width":1.78<=mx.y-mn.y<=1.95,"height":1.42<=mx.z<=1.47,"wheelbase":abs(b.FX-b.RX-2.82)<1e-8,"track":abs(2*b.WY-1.59)<1e-8,"source_ngon_zero":stats["ngon"]==0,"controlled_triangles_only":stats["tri"]>0 and stats["tri"]<=80,"source_no_boolean":"BOOLEAN" not in mods,"source_no_subd":"SUBSURF" not in mods,"four_arch_boundaries":len([n for n in names if "FEATURE_WHEEL_ARCH_" in n])==4,"four_fender_crowns":len([n for n in names if "FEATURE_FENDER_CROWN_" in n])==4,"shoulder_feature_lines":len([n for n in names if "FEATURE_SHOULDER_" in n])==2,"premature_detail_absent":not any(any(k in o.name for k in ["HANDLE","LAMP","MIRROR","SEAT","SCREEN","WIPER","CALIPER","SPOKE"]) for o in bpy.context.scene.objects),"render_matrix":len(R)==12}
    q={"schema":"oleander.auto.v0.11.r15.qa","model":MODEL,"status":"MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL","source_hash_before_diagnostics":h0,"source_hash_after_diagnostics":h1,"bounds":{"min":list(mn),"max":list(mx),"dimensions":[mx.x-mn.x,mx.y-mn.y,mx.z-mn.z]},"topology":stats,"source_modifiers":mods,"feature_names":names,"checks":checks,"renders":R,"boundary":"R15 integrates fender crown into shoulder Source topology. M5 Visual QA is required; no promotion or M6/M7/M8 authority exists."};(out/"AUTOMOTIVE_V011_QA.json").write_text(json.dumps(q,ensure_ascii=False,indent=2)+"\n");rec={"schema":"oleander.auto.v0.11.r15.receipt","model":MODEL,"blender_version":bpy.app.version_string,"build_hash":bpy.app.build_hash.decode() if isinstance(bpy.app.build_hash,bytes) else str(bpy.app.build_hash),"renderer":"Cycles CPU","samples":a.samples,"resolution":[a.resolution,a.resolution],"status":"EXECUTED_"+q["status"],"blend":str(blend),"qa":str(out/"AUTOMOTIVE_V011_QA.json"),"renders":R};(out/"AUTOMOTIVE_V011_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n");print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if all(checks.values()) else 5)
if __name__=="__main__":main()
