#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from collections import defaultdict
from pathlib import Path
import g1_geometry_core as base
import g1_r2_core as r2

def sub(a,b):return tuple(a[i]-b[i] for i in range(3))
def dot(a,b):return sum(a[i]*b[i] for i in range(3))
def norm(a):return math.sqrt(dot(a,a))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):
 n=norm(a);return tuple(v/n for v in a)
def normal(s,u,t,rev=False):
 q=1e-4;return unit(cross(sub(r2.point(s,min(.99999,u+q),t,rev),r2.point(s,max(.00001,u-q),t,rev)),sub(r2.point(s,u,t+q,rev),r2.point(s,u,t-q,rev))))
def ang(a,b):return math.degrees(math.acos(max(-1,min(1,dot(a,b)))))
def fair(s,rev=False):
 ml=mc=0.;n=0
 for i in range(45):
  u=.03+.94*i/44
  for j in range(72):
   t=2*math.pi*j/72;u1=min(.97,u+.01);t1=t+.05
   if min(r2.rho(s,u,t),r2.rho(s,u1,t),r2.rho(s,u,t1))<1.08:continue
   z=normal(s,u,t,rev);ml=max(ml,ang(z,normal(s,u1,t,rev)));mc=max(mc,ang(z,normal(s,u,t1,rev)));n+=1
 return ml,mc,n
def continuity(s,r0,eps):
 d=base.own(s,'INTERFACE_DECK_BOUNDARY');mx=0.
 for k in range(72):
  p=2*math.pi*k/72
  def uv(r):return float(d['u_center'])+float(d['u_halfspan'])*r*math.cos(p),r2.center(d)+float(d['theta_halfspan_rad'])*r*math.sin(p)
  mx=max(mx,ang(normal(s,*uv(r0-eps)),normal(s,*uv(r0+eps))))
 return mx
def loops(faces,labels):
 e=defaultdict(list)
 for f,l in zip(faces,labels):
  for i in range(len(f)):e[tuple(sorted((f[i],f[(i+1)%len(f)])))].append(l)
 x=[k for k,v in e.items() if len(v)==2 and v[0]!=v[1]];a=defaultdict(set)
 for u,v in x:a[u].add(v);a[v].add(u)
 seen=set();c=0
 for v in a:
  if v in seen:continue
  c+=1;q=[v];seen.add(v)
  while q:
   w=q.pop()
   for z in a[w]:
    if z not in seen:seen.add(z);q.append(z)
 return c,len(x),all(len(a[v])==2 for v in a)
def scalars(v):
 if isinstance(v,bool):return 0
 if isinstance(v,(int,float)):return 1
 if isinstance(v,list):return sum(scalars(x) for x in v)
 if isinstance(v,dict):return sum(scalars(x) for k,x in v.items() if k!='editable')
 return 0
def evaluate(s,fix,rev=False):
 v,f,l=r2.mesh(s,rev);lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];dim=[hi[i]-lo[i] for i in range(3)];th=s['machine_thresholds'];ml,mc,n=fair(s,rev);d=base.own(s,'INTERFACE_DECK_BOUNDARY');eps=float(fix['machine_zoning']['interface_transition_validation']['boundary_probe_epsilon_rho']);o=continuity(s,1,eps);c=continuity(s,float(d['core_fraction']),eps);lp,edges,closed=loops(f,l);u=.55;g=base.bezier(base.own(s,'GRIP_AXIS')['control_points'],u);asy=(r2.point(s,u,math.pi/2,rev)[1]-g[1])-(g[1]-r2.point(s,u,3*math.pi/2,rev)[1]);depth=r2.point(s,float(d['u_center']),0,rev,False)[2]-r2.point(s,float(d['u_center']),0,rev,True)[2];m=fix['machine_zoning']['interface_transition_validation'];checks={'sparse':scalars(s['ownership'])<=int(th['max_sparse_authority_scalar_count']),'length':abs(dim[0]-float(th['overall_length_target_m']))<=float(th['overall_length_tolerance_m']),'width':abs(dim[1]-float(th['overall_width_target_m']))<=float(th['overall_width_tolerance_m']),'height':abs(dim[2]-float(th['overall_height_target_m']))<=float(th['overall_height_tolerance_m']),'asymmetry':asy>=float(th['min_thumb_opposite_asymmetry_m']),'interface_region':l.count('DECK')>0,'interface_loop':lp==int(m['required_region_boundary_loops']) and closed,'depth':float(th['min_interface_inset_depth_m'])<=depth<=float(th['max_interface_inset_depth_m']),'broad_long':ml<=float(th['max_longitudinal_normal_delta_deg_per_0_01u']),'broad_circ':mc<=float(th['max_circumferential_normal_delta_deg_per_0_05rad']),'outer_continuity':o<=float(m['outer_boundary_normal_continuity_max_deg']),'core_continuity':c<=float(m['core_boundary_normal_continuity_max_deg']),'execution_not_authority':s['derived_execution']['editable_authority'] is False};return {'checks':checks,'dimensions_m':dim,'sparse_scalar_count':scalars(s['ownership']),'asymmetry_m':asy,'interface_depth_m':depth,'interface_faces':l.count('DECK'),'interface_boundary_edges':edges,'interface_boundary_loops':lp,'broad_fairness':{'long_deg':ml,'circ_deg':mc,'samples':n},'outer_continuity_deg':o,'core_continuity_deg':c},v
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--correction',required=True);p.add_argument('--out',required=True);a=p.parse_args();src=json.load(open(a.source));fix=json.load(open(a.correction));s=r2.apply(src,fix);b,bv=evaluate(s,fix);q,qv=evaluate(s,fix,True);mx=max(norm(sub(x,y)) for x,y in zip(bv,qv));u=.55;gain=r2.point(s,u,math.pi/2,True)[1]-r2.point(s,u,math.pi/2,False)[1];opp=abs(r2.point(s,u,3*math.pi/2,True)[1]-r2.point(s,u,3*math.pi/2,False)[1]);rel={'checks':{'upstream_only':True,'no_mesh_patch':True,'displacement':.002<=mx<=.010,'thumb_gain':gain>=.002,'opposite_unchanged':opp<=1e-6},'max_displacement_m':mx,'thumb_gain_m':gain,'opposite_change_m':opp};checks={'baseline':all(b['checks'].values()),'revised':all(q['checks'].values()),'relation_revision':all(rel['checks'].values())};status='MACHINE_PASS_RELATION_REVISION_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL_REVISE_R2';report={'status':status,'job_state':'EXECUTED','design_state':'EXPLORE' if status.startswith('MACHINE_PASS') else 'REVISE','authority_state':'WORKING_SOURCE','checks':checks,'baseline':b,'revised':q,'relation_revision':rel,'boundary':'Machine PASS opens Visual QA only.'};o=Path(a.out);o.mkdir(parents=True,exist_ok=True);(o/'G1_R2_MACHINE_REPORT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0 if status.startswith('MACHINE_PASS') else 5
if __name__=='__main__':raise SystemExit(main())
