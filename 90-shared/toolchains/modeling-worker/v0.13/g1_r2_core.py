#!/usr/bin/env python3
from __future__ import annotations
import copy,math
import g1_geometry_core as base

def wrap(a): return (a+math.pi)%(2*math.pi)-math.pi

def apply(src,fix):
    out=copy.deepcopy(src)
    for fam,ov in fix['source_overrides'].items():
        item={'role':out['ownership'][fam]['role'],'editable':out['ownership'][fam]['editable']}
        item.update(copy.deepcopy(ov));out['ownership'][fam]=item
    out['revision']='G1-R2';return out

def center(d): return 0.0 if d.get('theta_center')=='TOP_MERIDIAN' else float(d.get('theta_center_rad',0.0))
def rho(s,u,t):
    d=base.own(s,'INTERFACE_DECK_BOUNDARY')
    return math.hypot((u-float(d['u_center']))/float(d['u_halfspan']),wrap(t-center(d))/float(d['theta_halfspan_rad']))
def point(s,u,t,revision=False,deck=True):
    g=base.bezier(base.own(s,'GRIP_AXIS')['control_points'],u)
    top=float(base.bezier(base.own(s,'PALM_PROFILE')['control_values'],u));th=float(base.bezier(base.own(s,'THUMB_SIDE_PLAN')['control_values'],u));op=float(base.bezier(base.own(s,'OPPOSITE_SIDE_PLAN')['control_values'],u));lo=float(base.bezier(base.own(s,'LOWER_RETURN_PROFILE')['control_values'],u))
    if revision: th*=1+.12*math.sin(math.pi*u)**2
    exp=float(base.own(s,'LOWER_RETURN_PROFILE').get('termination_envelope_exponent',.55));env=math.sin(math.pi*u)**exp if 0<u<1 else 0.0
    top*=env;th*=env;op*=env;lo*=env;sn=math.sin(t);cs=math.cos(t)
    lat=.5*(th+op)+.5*(th-op)*sn;vert=.5*(top+lo)+.5*(top-lo)*cs
    x=float(g[0]);y=float(g[1])+lat*sn;z=float(g[2])+vert*cs
    if deck:
        d=base.own(s,'INTERFACE_DECK_BOUNDARY');r=rho(s,u,t)
        if r<1:
            c=float(d['core_fraction']);mask=1.0 if r<=c else base.smootherstep((1-r)/(1-c));z-=float(d['depth_m'])*mask
    return (x,y,z)
def mesh(s,revision=False):
    nu=int(s['derived_execution']['u_rings']);nv=int(s['derived_execution']['circumferential_samples']);v=[point(s,0,0,revision)];faces=[];labels=[]
    for i in range(1,nu+1):
        u=i/(nu+1)
        for j in range(nv):v.append(point(s,u,2*math.pi*j/nv,revision))
    back=len(v);v.append(point(s,1,0,revision))
    for j in range(nv):faces.append((0,1+j,1+(j+1)%nv));labels.append('BODY')
    for i in range(nu-1):
        a=1+i*nv;b=a+nv;um=(i+1.5)/(nu+1)
        for j in range(nv):
            n=(j+1)%nv;tm=2*math.pi*(j+.5)/nv;faces.append((a+j,b+j,b+n,a+n));labels.append('DECK' if rho(s,um,tm)<1 else 'BODY')
    last=1+(nu-1)*nv
    for j in range(nv):faces.append((last+j,back,last+(j+1)%nv));labels.append('BODY')
    return v,faces,labels
