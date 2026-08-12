#!/usr/bin/env python3
"""M6 diagnostic coverage fix.

No Source geometry, topology, region assignment, dependency graph or selective-rebuild
rule changes. Adds one derived-only underside view so REG-UNDERBODY-CENTER can receive
Human M6 review without ground-plane occlusion.
"""
from __future__ import annotations
import importlib.util
import bpy


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

m6=load('/tmp/revise_v011_r29a_m6.py','m6')

m6.VIEW_POLICY['REG-UNDERBODY-CENTER']=[
    'M6_COMPONENT_SIDE',
    'M6_COMPONENT_FRONT_3Q',
    'M6_COMPONENT_REAR_3Q',
    'M6_COMPONENT_UNDERSIDE_3Q',
]


def render_component_views(out,samples,res,M,source,diag):
    m6.b.wheels(M)
    before_ground={o.name for o in bpy.context.scene.objects}
    m6.b.ground(M)
    ground_objs=[o for o in bpy.context.scene.objects if o.name not in before_ground]
    L=m6.b.rigs()
    m6.b.world((.018,.018,.018),.18)
    source.hide_render=True
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True)
    views=[
        ('M6_COMPONENT_SIDE',(0,-8.8,1.14),(0,0,.64),85,True,5.25,'BROAD',False),
        ('M6_COMPONENT_FRONT_3Q',(6.2,-7.0,2.75),(.05,0,.66),78,False,5.0,'BROAD',False),
        ('M6_COMPONENT_REAR_3Q',(-6.0,6.8,2.65),(-.10,0,.66),78,False,5.0,'BROAD',False),
        # Diagnostic-only view: ground hidden and world raised so the cross-center
        # underbody routing strip is visible. This camera has no design authority.
        ('M6_COMPONENT_UNDERSIDE_3Q',(4.2,-5.2,-2.65),(0,0,.28),72,False,5.0,'BROAD',True),
    ]
    records=[]
    for label,loc,target,lens,ortho,scale,rig,underside in views:
        m6.b.setrig(L,rig)
        for g in ground_objs:
            g.hide_render=underside
        if underside:
            m6.b.world((.08,.08,.08),.55)
        else:
            m6.b.world((.018,.018,.018),.18)
        cam=m6.b.camera('CAM_'+label,loc,target,lens,ortho,scale)
        bpy.context.scene.camera=cam
        p=rd/f'{m6.MODEL}__{label}.png'
        m6.b.setup(p,samples,res)
        bpy.ops.render.render(write_still=True)
        records.append({'view':label,'file':str(p),'authority':'DIAGNOSTIC_ONLY','ground_hidden':underside})
        bpy.data.objects.remove(cam,do_unlink=True)
    for g in ground_objs:
        g.hide_render=False
    source.hide_render=False
    return records

m6.render_component_views=render_component_views

if __name__=='__main__':
    m6.main()
