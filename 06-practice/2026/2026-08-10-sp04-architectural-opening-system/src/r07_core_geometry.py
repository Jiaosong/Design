# -*- coding: utf-8 -*-
"""SP04-R07 core geometry generator.
Requires numpy, shapely, trimesh.
No AI image generation. All dimensions are training-only hypothetical parameters.
"""
from pathlib import Path
import math, json
import numpy as np
import trimesh
from shapely.geometry import Polygon, box
from shapely.ops import triangulate, unary_union

OUT = Path("R07_generated")
OUT.mkdir(parents=True, exist_ok=True)


def rect_poly(cx, sill, width, height):
    return box(cx-width/2, sill, cx+width/2, sill+height)


def arch_poly(cx, sill, width, rect_height, rise, segments=72):
    x0, x1 = cx-width/2, cx+width/2
    spring = sill + rect_height
    pts=[(x0,sill),(x1,sill),(x1,spring)]
    for i in range(segments+1):
        th=i*math.pi/segments
        pts.append((cx+(width/2)*math.cos(th), spring+rise*math.sin(th)))
    pts.append((x0,spring))
    return Polygon(pts)


def poly_to_mesh(poly, depth, y0=0.0):
    verts=[]; faces=[]; vmap={}
    def addv(p):
        key=tuple(round(float(x),8) for x in p)
        if key not in vmap:
            vmap[key]=len(verts); verts.append(key)
        return vmap[key]
    def quad(a,b,c,d):
        q=[addv(p) for p in (a,b,c,d)]
        faces.extend([[q[0],q[1],q[2]],[q[0],q[2],q[3]]])
    for tr in triangulate(poly):
        inter=tr.intersection(poly)
        if abs(inter.area-tr.area) <= max(1e-7,tr.area*1e-9):
            c=list(tr.exterior.coords)[:3]
            b=[addv((x,y0,z)) for x,z in c]
            t=[addv((x,y0+depth,z)) for x,z in c]
            faces.extend([[b[0],b[2],b[1]],[t[0],t[1],t[2]]])
    for ring in [poly.exterior]+list(poly.interiors):
        c=list(ring.coords)
        for (x0,z0),(x1,z1) in zip(c[:-1],c[1:]):
            quad((x0,y0,z0),(x1,y0,z1),(x1,y0+depth,z1),(x0,y0+depth,z0))
    m=trimesh.Trimesh(vertices=np.asarray(verts,float),faces=np.asarray(faces,int),process=True)
    trimesh.repair.fix_normals(m,multibody=True)
    if m.volume < 0:
        m.invert()
    return m


def wall_mesh(length,height,depth,openings,y0=0.0):
    solid=box(0,0,length,height).difference(unary_union(openings))
    return poly_to_mesh(solid,depth,y0)


def ring_rect(cx,sill,outer_w,outer_h,profile):
    outer=rect_poly(cx,sill,outer_w,outer_h)
    inner=rect_poly(cx,sill+profile,outer_w-2*profile,outer_h-2*profile)
    return outer.difference(inner)


def box_mesh(x0,x1,y0,y1,z0,z1):
    m=trimesh.creation.box(extents=[x1-x0,y1-y0,z1-z0])
    m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2])
    return m


def save_scene(name, components):
    folder=OUT/name
    folder.mkdir(parents=True,exist_ok=True)
    scene=trimesh.Scene()
    qa={}
    for cname,m in components.items():
        scene.add_geometry(m,node_name=cname,geom_name=cname)
        m.export(folder/f"{cname}.obj")
        qa[cname]={
            "watertight":bool(m.is_watertight),
            "winding_consistent":bool(m.is_winding_consistent),
            "body_count":int(m.body_count)
        }
    (folder/"scene.glb").write_bytes(scene.export(file_type="glb"))
    return qa


# A — Deep Reveal
opA=rect_poly(3000,450,1800,2100)
wallA=wall_mesh(6000,3300,600,[opA])
frameA=poly_to_mesh(ring_rect(3000,490,1720,2020,70),60,500)
seatA=box_mesh(2140,3860,0,520,370,450)
qaA=save_scene("A_DEEP_REVEAL",{"wall":wallA,"frame":frameA,"seat":seatA})

# B — Soft Arch
opB=arch_poly(3000,0,1600,1300,800)
wallB=wall_mesh(6000,3300,500,[opB])
thresholdB=box_mesh(2260,3740,0,500,0,60)
qaB=save_scene("B_SOFT_ARCH",{"wall":wallB,"threshold":thresholdB})

# C — Offset Frame: smaller interior aperture + larger exterior aperture
opCi=rect_poly(3000,900,1800,1500)
opCo=rect_poly(3000,750,2100,1800)
inner=wall_mesh(6000,3300,90,[opCi],0)
outer=wall_mesh(6000,3300,270,[opCo],90)
frameC=poly_to_mesh(ring_rect(3000,900,1800,1500,65),55,90)
qaC=save_scene("C_OFFSET_FRAME",{"wall_inner_slice":inner,"wall_outer_slice":outer,"frame":frameC})

# D — Opening Field
count=5; w=720; h=1900; gap=420; sill=500
total=count*w+(count-1)*gap
edge=(6000-total)/2
ops=[]
for i in range(count):
    cx=edge+w/2+i*(w+gap)
    ops.append(rect_poly(cx,sill,w,h))
wallD=wall_mesh(6000,3300,420,ops)
qaD=save_scene("D_OPENING_FIELD",{"wall":wallD})

result={"A":qaA,"B":qaB,"C":qaC,"D":qaD}
(OUT/"qa_core.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
assert all(v["watertight"] and v["winding_consistent"] for group in result.values() for v in group.values())
print("R07 core geometry generated and QA passed")
