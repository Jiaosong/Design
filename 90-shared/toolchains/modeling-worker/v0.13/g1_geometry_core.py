#!/usr/bin/env python3
from __future__ import annotations
import math
from typing import Any


def bezier(values: list[Any], u: float) -> Any:
    n = len(values) - 1
    if isinstance(values[0], list):
        out = [0.0] * len(values[0])
        for i, point in enumerate(values):
            b = math.comb(n, i) * (u ** i) * ((1.0 - u) ** (n - i))
            for j, value in enumerate(point):
                out[j] += b * float(value)
        return out
    return sum(math.comb(n, i) * (u ** i) * ((1.0 - u) ** (n - i)) * float(v) for i, v in enumerate(values))


def smootherstep(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x*x*x*(x*(x*6.0-15.0)+10.0)


def own(source: dict[str, Any], family: str) -> dict[str, Any]:
    return source['ownership'][family]


def point(source: dict[str, Any], u: float, theta: float, revision: bool=False, deck: bool=True) -> tuple[float,float,float]:
    grip = bezier(own(source,'GRIP_AXIS')['control_points'], u)
    top = float(bezier(own(source,'PALM_PROFILE')['control_values'], u))
    thumb = float(bezier(own(source,'THUMB_SIDE_PLAN')['control_values'], u))
    opposite = float(bezier(own(source,'OPPOSITE_SIDE_PLAN')['control_values'], u))
    lower = float(bezier(own(source,'LOWER_RETURN_PROFILE')['control_values'], u))
    if revision:
        thumb *= 1.0 + 0.12 * math.sin(math.pi*u)**2
    env = math.sin(math.pi*u)**0.55 if 0.0 < u < 1.0 else 0.0
    top*=env; thumb*=env; opposite*=env; lower*=env
    s=math.sin(theta); c=math.cos(theta)
    lateral=0.5*(thumb+opposite)+0.5*(thumb-opposite)*s
    vertical=0.5*(top+lower)+0.5*(top-lower)*c
    x=float(grip[0]); y=float(grip[1])+lateral*s; z=float(grip[2])+vertical*c
    if deck:
        d=own(source,'INTERFACE_DECK_BOUNDARY')
        du=abs(u-float(d['u_center']))/float(d['u_halfspan'])
        lm=smootherstep(1.0-du) if du<1.0 else 0.0
        threshold=float(d['angular_threshold_cos'])
        am=smootherstep((c-threshold)/(1.0-threshold)) if c>threshold else 0.0
        z-=float(d['depth_m'])*lm*am*(1.0+float(d['thumb_bias'])*max(0.0,s))
    return x,y,z


def mesh(source: dict[str, Any], revision: bool=False):
    nu=int(source['derived_execution']['u_rings']); nv=int(source['derived_execution']['circumferential_samples'])
    verts=[point(source,0.0,0.0,revision)]
    for i in range(1,nu+1):
        u=i/(nu+1)
        for j in range(nv):
            verts.append(point(source,u,2.0*math.pi*j/nv,revision))
    back=len(verts); verts.append(point(source,1.0,0.0,revision))
    faces=[]; first=1
    for j in range(nv): faces.append((0,first+j,first+(j+1)%nv))
    for i in range(nu-1):
        a=1+i*nv; b=a+nv
        for j in range(nv):
            jn=(j+1)%nv; faces.append((a+j,b+j,b+jn,a+jn))
    last=1+(nu-1)*nv
    for j in range(nv): faces.append((last+j,back,last+(j+1)%nv))
    return verts,faces
