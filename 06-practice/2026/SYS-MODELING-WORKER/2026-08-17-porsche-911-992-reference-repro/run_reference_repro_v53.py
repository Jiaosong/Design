#!/usr/bin/env python3
"""V53 — surface fold localization diagnostic only.

Geometry delta: NONE. Uses V51 geometry + V52 semantic evidence unchanged.
Purpose: localize every adjacent-face normal reversal on the pre-aperture primary skin so the next
Source edit targets the owning section/rail rather than using smoothing, SubD or visual guesswork.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V52=HERE/'run_reference_repro_v52.py'
text=V52.read_text();marker='\nrun52()\n'
if marker not in text: raise SystemExit('V52 run marker missing')
ctx={'__file__':str(V52),'__name__':'oleander_v53_fold_diagnostic'}
exec(compile(text.split(marker,1)[0],str(V52),'exec'),ctx)

v=ctx['v'];runtime=ctx['runtime'];patch51=ctx['patch51']
CAND='V51_FRONT_TRANSVERSE_IDENTITY_REPAIR';EVID='V53_SURFACE_FOLD_LOCALIZATION'

def nearest_station(x, xs):
    i=min(range(len(xs)),key=lambda j:abs(xs[j]-x));return i,float(xs[i])

def emit_fold_diag(out):
    body=bpy.data.objects.get('DERIVED_911_9922_BODY')
    if body is None: raise SystemExit('FAIL_SURFACE_FOLD_DIAGNOSTIC_BODY_MISSING')
    me=body.data;mw=body.matrix_world
    edge_faces={}
    for p in me.polygons:
        vs=list(p.vertices)
        for a,b in zip(vs,vs[1:]+vs[:1]): edge_faces.setdefault(tuple(sorted((a,b))),[]).append(p.index)
    # derive station X values from ring blocks where available; fallback to unique rounded X of vertices.
    xs=sorted(set(round(float((mw@vv.co).x),6) for vv in me.vertices))
    folds=[]
    for (a,b),faces in edge_faces.items():
        if len(faces)!=2: continue
        pa,pb=me.polygons[faces[0]],me.polygons[faces[1]]
        dot=float(pa.normal.dot(pb.normal))
        if dot>=-.15: continue
        va=mw@me.vertices[a].co;vb=mw@me.vertices[b].co;cx=(float(va.x)+float(vb.x))*.5;cy=(float(va.y)+float(vb.y))*.5;cz=(float(va.z)+float(vb.z))*.5
        si,sx=nearest_station(cx,xs)
        folds.append({'edge_vertices':[int(a),int(b)],'face_indices':[int(faces[0]),int(faces[1])],'normal_dot':dot,'center_m':[cx,cy,cz],'nearest_longitudinal_station_index':si,'nearest_longitudinal_station_x_m':sx,'side':'CENTER' if abs(cy)<.03 else ('LEFT_POS_Y' if cy>0 else 'RIGHT_NEG_Y'),'region':'FRONT' if cx>.55 else ('REAR' if cx<-.55 else 'MID')})
    # cluster by nearest x station + mirrored absolute-y band.
    clusters={}
    for f in folds:
        key=(f['nearest_longitudinal_station_index'],round(abs(f['center_m'][1]),2),f['region'])
        c=clusters.setdefault(key,{'station_index':key[0],'station_x_m':f['nearest_longitudinal_station_x_m'],'abs_y_band_m':key[1],'region':key[2],'fold_count':0,'sides':set(),'z_min':999.0,'z_max':-999.0})
        c['fold_count']+=1;c['sides'].add(f['side']);c['z_min']=min(c['z_min'],f['center_m'][2]);c['z_max']=max(c['z_max'],f['center_m'][2])
    cl=[]
    for c in clusters.values():
        c['sides']=sorted(c['sides']);cl.append(c)
    cl.sort(key=lambda x:(-x['fold_count'],x['station_x_m'],x['abs_y_band_m']))
    d={'schema':'oleander.3d.surface-fold-diagnostic.v1','candidate_revision':CAND,'evidence_revision':EVID,'geometry_revision_unchanged':CAND,'fold_count':len(folds),'folds':folds,'clusters':cl,'cluster_count':len(cl),'front_fold_count':sum(1 for f in folds if f['region']=='FRONT'),'mid_fold_count':sum(1 for f in folds if f['region']=='MID'),'rear_fold_count':sum(1 for f in folds if f['region']=='REAR'),'authority':'DIAGNOSTIC_NOT_REFERENCE_AUTHORITY','does_not_prove':['reference fidelity','Class-A continuity','root cause until cluster relation is reviewed']}
    Path(out,'SURFACE_FOLD_DIAGNOSTIC.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'fold_count':d['fold_count'],'front':d['front_fold_count'],'mid':d['mid_fold_count'],'rear':d['rear_fold_count'],'top_clusters':cl[:12]},indent=2))

def run53():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:
        runtime['run30']()
    except SystemExit as e:
        patch51(out);emit_fold_diag(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:
        patch51(out);emit_fold_diag(out)
run53()
