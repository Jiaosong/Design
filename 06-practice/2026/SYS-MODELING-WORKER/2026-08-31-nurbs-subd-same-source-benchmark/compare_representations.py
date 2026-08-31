#!/usr/bin/env python3
import argparse, csv, json, math
from pathlib import Path

def cli():
    p=argparse.ArgumentParser(); p.add_argument('--source',required=True); p.add_argument('--freecad',required=True); p.add_argument('--subd-l2',required=True); p.add_argument('--subd-l4',required=True); p.add_argument('--freecad-receipt',required=True); p.add_argument('--blender-receipt',required=True); p.add_argument('--out',required=True); return p.parse_args()

def parse_obj(path):
    v=[]; f=[]
    for line in Path(path).read_text(errors='ignore').splitlines():
        if line.startswith('v '):
            _,x,y,z=line.split()[:4]; v.append((float(x),float(y),float(z)))
        elif line.startswith('f '):
            ids=[int(s.split('/')[0])-1 for s in line.split()[1:]]
            if len(ids)==3: f.append(tuple(ids))
            elif len(ids)>3:
                for i in range(1,len(ids)-1): f.append((ids[0],ids[i],ids[i+1]))
    if not v or not f: raise RuntimeError(f'empty OBJ {path}')
    return v,f

def plane_profile(mesh,x0):
    verts,faces=mesh; pts={}; eps=1e-8
    for tri in faces:
        q=[verts[i] for i in tri]
        for a,b in ((q[0],q[1]),(q[1],q[2]),(q[2],q[0])):
            da=a[0]-x0; db=b[0]-x0
            if abs(da)<eps and abs(db)<eps:
                for p in (a,b): pts[(round(p[0],6),round(p[1],6),round(p[2],6))]=p
            elif da*db<=0 and abs(a[0]-b[0])>eps:
                t=(x0-a[0])/(b[0]-a[0])
                if -1e-7<=t<=1+1e-7:
                    p=(x0,a[1]+t*(b[1]-a[1]),a[2]+t*(b[2]-a[2])); pts[(round(p[0],6),round(p[1],6),round(p[2],6))]=p
    rr=[math.hypot(p[1],p[2]) for p in pts.values()]
    if len(rr)<6: raise RuntimeError(f'plane x={x0} has only {len(rr)} intersections')
    mean=sum(rr)/len(rr); std=math.sqrt(sum((r-mean)**2 for r in rr)/len(rr))
    return {'x':float(x0),'mean_radius':mean,'std_radius':std,'noncircularity':std/max(mean,1e-9),'samples':len(rr),'min_radius':min(rr),'max_radius':max(rr)}

def profile(mesh,xs): return [plane_profile(mesh,x) for x in xs]

def rmse(a,b,key='mean_radius'):
    return math.sqrt(sum((x[key]-y[key])**2 for x,y in zip(a,b))/len(a))

def curvature(p):
    out=[]
    for i in range(1,len(p)-1):
        x0,x1,x2=p[i-1]['x'],p[i]['x'],p[i+1]['x']; r0,r1,r2=p[i-1]['mean_radius'],p[i]['mean_radius'],p[i+1]['mean_radius']
        h1=x1-x0; h2=x2-x1
        if abs(h1-h2)>1e-6: continue
        h=(h1+h2)/2; rp=(r2-r0)/(2*h); rpp=(r2-2*r1+r0)/(h*h); k=abs(rpp)/((1+rp*rp)**1.5); out.append({'x':x1,'curvature':k})
    return out

def rmse_series(a,b):
    return math.sqrt(sum((x['curvature']-y['curvature'])**2 for x,y in zip(a,b))/max(len(a),1))

def bbox(mesh):
    v=mesh[0]; xs=[p[0] for p in v]; ys=[p[1] for p in v]; zs=[p[2] for p in v]; return [max(xs)-min(xs),max(ys)-min(ys),max(zs)-min(zs)]

def control_deviation(mesh,rings):
    vals=[]
    for r in rings[1:-1]:
        p=plane_profile(mesh,float(r['x'])); vals.append({'x':r['x'],'control_radius':r['radius'],'evaluated_radius':p['mean_radius'],'delta':p['mean_radius']-float(r['radius'])})
    rms=math.sqrt(sum(v['delta']**2 for v in vals)/len(vals)); return vals,rms

def main():
    a=cli(); src=json.loads(Path(a.source).read_text()); xs=[float(x) for x in src['comparison_planes_x']]
    meshes={'FREECAD_NURBS':parse_obj(a.freecad),'SUBD_L2':parse_obj(a.subd_l2),'SUBD_L4':parse_obj(a.subd_l4)}
    prof={k:profile(m,xs) for k,m in meshes.items()}; curv={k:curvature(v) for k,v in prof.items()}
    fc_receipt=json.loads(Path(a.freecad_receipt).read_text()); bl_receipt=json.loads(Path(a.blender_receipt).read_text())
    if fc_receipt['source_controls_sha256']!=bl_receipt['source_controls_sha256']: raise RuntimeError('source control hash mismatch between workers')
    fc_ctrl,fc_ctrl_rms=control_deviation(meshes['FREECAD_NURBS'],src['rings']); s4_ctrl,s4_ctrl_rms=control_deviation(meshes['SUBD_L4'],src['rings'])
    cross=rmse(prof['FREECAD_NURBS'],prof['SUBD_L4']); sampling=rmse(prof['SUBD_L2'],prof['SUBD_L4']); kcross=rmse_series(curv['FREECAD_NURBS'],curv['SUBD_L4'])
    b={k:bbox(v) for k,v in meshes.items()}; diameter_rel=abs(max(b['FREECAD_NURBS'][1:])-max(b['SUBD_L4'][1:]))/max(max(b['FREECAD_NURBS'][1:]),1e-9); length_rel=abs(b['FREECAD_NURBS'][0]-b['SUBD_L4'][0])/max(b['FREECAD_NURBS'][0],1e-9)
    max_non=max(max(p['noncircularity'] for p in prof[k]) for k in prof)
    contract={
      'shared_source_hash':True,
      'all_cross_sections_resolved':all(p['samples']>=6 for ps in prof.values() for p in ps),
      'subd_sampling_converges':sampling<2.5,
      'representations_are_not_numerically_identical':cross>0.05,
      'same_intent_remains_broadly_aligned':cross<12.0 and diameter_rel<0.15 and length_rel<0.08,
      'radial_symmetry_bounded':max_non<0.08,
      'control_points_are_not_assumed_surface_points':fc_ctrl_rms>0.01 and s4_ctrl_rms>0.01
    }
    receipt={'schema':'oleander.3d.nurbs-subd.same-source.comparison.v1','source_controls_sha256':fc_receipt['source_controls_sha256'],'comparison_planes_x_mm':xs,'metrics':{'freecad_vs_subd_l4_profile_rmse_mm':cross,'subd_l2_vs_l4_profile_rmse_mm':sampling,'freecad_vs_subd_curvature_rmse_per_mm':kcross,'freecad_control_station_rms_delta_mm':fc_ctrl_rms,'subd_l4_control_station_rms_delta_mm':s4_ctrl_rms,'bbox_mm':b,'length_relative_delta':length_rel,'max_diameter_relative_delta':diameter_rel,'max_cross_section_noncircularity':max_non},'control_station_readback':{'freecad_nurbs':fc_ctrl,'subd_l4':s4_ctrl},'profiles':prof,'curvature_profiles':curv,'contract':contract,'overall_pass':all(contract.values()),'practiced_propositions':['SAME CONTROL ARCHITECTURE != SAME LIMIT SURFACE','CONTROL POLES/RINGS != REQUIRED SURFACE INTERPOLATION POINTS','HIGHER SUBD EVALUATION LEVEL REDUCES SAMPLING ERROR BUT DOES NOT CONVERT THE REPRESENTATION INTO NURBS','REPRESENTATION COMPARISON REQUIRES EVALUATED GEOMETRY READBACK, NOT UI COMMAND NAME PARITY'],'holds':['Rhino native NURBS/SubD evaluation','Class-A G2 highlight/zebra qualification','Houdini procedural parity','manufacturing/aerodynamic truth','Design KEEP']}
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True); (out/'COMPARISON_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    with (out/'PROFILE_COMPARISON.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['x_mm','freecad_radius','subd_l2_radius','subd_l4_radius','freecad_noncircularity','subd_l4_noncircularity'])
        for i,x in enumerate(xs): w.writerow([x,prof['FREECAD_NURBS'][i]['mean_radius'],prof['SUBD_L2'][i]['mean_radius'],prof['SUBD_L4'][i]['mean_radius'],prof['FREECAD_NURBS'][i]['noncircularity'],prof['SUBD_L4'][i]['noncircularity']])
    print(json.dumps({'overall_pass':receipt['overall_pass'],'metrics':receipt['metrics'],'contract':contract},indent=2))
    if not receipt['overall_pass']: raise SystemExit(9)
if __name__=='__main__': main()
