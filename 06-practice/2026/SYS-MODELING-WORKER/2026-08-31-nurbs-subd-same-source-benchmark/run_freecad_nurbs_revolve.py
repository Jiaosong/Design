#!/usr/bin/env python3
import hashlib, json, os
from pathlib import Path
import FreeCAD as App
import Part

DOC='OLEANDER_NURBS_SAME_SOURCE'
OBJ='NURBS_REVOLVE'

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()

def load_source(path):
    d=json.loads(Path(path).read_text())
    assert d['schema']=='oleander.3d.same-source-control-rings.v1'
    assert d['axis']=='X' and d['units']=='mm'
    return d

def bbox(shape):
    b=shape.BoundBox
    return {'min':[float(b.XMin),float(b.YMin),float(b.ZMin)],'max':[float(b.XMax),float(b.YMax),float(b.ZMax)],'size':[float(b.XLength),float(b.YLength),float(b.ZLength)]}

def write_obj(shape,path,deflection=0.45):
    verts,faces=shape.tessellate(deflection)
    with open(path,'w',encoding='utf-8') as f:
        f.write('# OLEANDER FreeCAD/OpenCASCADE B-spline revolve tessellation\n')
        for v in verts: f.write(f'v {v.x:.9f} {v.y:.9f} {v.z:.9f}\n')
        for face in faces:
            ids=[int(i)+1 for i in face]
            if len(ids)==3:
                f.write('f %d %d %d\n'%tuple(ids))
            elif len(ids)>3:
                for i in range(1,len(ids)-1): f.write(f'f {ids[0]} {ids[i]} {ids[i+1]}\n')
    return {'vertices':len(verts),'faces_raw':len(faces),'bytes':Path(path).stat().st_size,'sha256':sha256(path),'deflection_mm':deflection}

def curve_meta(curve):
    out={}
    for key,attr in [('degree','Degree'),('is_periodic','isPeriodic'),('is_rational','isRational')]:
        try:
            v=getattr(curve,attr)
            out[key]=bool(v()) if callable(v) and key.startswith('is_') else (v() if callable(v) else v)
        except Exception as e: out[key]=f'UNAVAILABLE:{type(e).__name__}'
    for key,method in [('knots','getKnots'),('multiplicities','getMultiplicities'),('weights','getWeights')]:
        try: out[key]=list(getattr(curve,method)())
        except Exception as e: out[key]=f'UNAVAILABLE:{type(e).__name__}'
    return out

def build(out,source_path):
    src=load_source(source_path); rings=src['rings']
    poles=[App.Vector(float(r['x']),0.0,float(r['radius'])) for r in rings]
    curve=Part.BSplineCurve(); curve.buildFromPoles(poles)
    edge=curve.toShape()
    shape=edge.revolve(App.Vector(0,0,0),App.Vector(1,0,0),360.0)
    if shape.isNull() or not shape.isValid(): raise RuntimeError('invalid revolved B-spline shape')
    doc=App.newDocument(DOC); obj=doc.addObject('Part::Feature',OBJ); obj.Label='Same-source B-spline revolve'; obj.Shape=shape; doc.recompute()
    native=out/'FREECAD_NURBS_SAME_SOURCE.FCStd'; step=out/'FREECAD_NURBS_SAME_SOURCE.step'; mesh=out/'FREECAD_NURBS_EVALUATED.obj'
    doc.saveAs(str(native)); Part.export([obj],str(step)); mesh_stats=write_obj(shape,mesh)
    receipt={
      'schema':'oleander.3d.nurbs-subd.same-source.freecad.v1','mode':'build','freecad_version':App.Version(),
      'source_controls':Path(source_path).name,'source_controls_sha256':sha256(source_path),
      'representation':'Part.BSplineCurve control poles -> OpenCASCADE B-spline edge -> 360deg revolve B-Rep',
      'control_role':'poles/control architecture, not interpolation constraints','control_count':len(poles),'curve':curve_meta(curve),
      'shape':{'is_valid':bool(shape.isValid()),'shape_type':shape.ShapeType,'faces':len(shape.Faces),'edges':len(shape.Edges),'vertices':len(shape.Vertexes),'area_mm2':float(shape.Area),'bbox_mm':bbox(shape)},
      'native':{'file':native.name,'bytes':native.stat().st_size,'sha256':sha256(native)},
      'step':{'file':step.name,'bytes':step.stat().st_size,'sha256':sha256(step)},'evaluated_mesh':{'file':mesh.name,**mesh_stats},
      'promotion_scope':['same control-pole source executed in FreeCAD/OpenCASCADE','native FCStd B-Rep save','STEP derivative','explicit evaluated tessellation for cross-representation comparison'],
      'holds':['Rhino native runtime/Class-A analysis','manufacturing approval','SubD parity','physical/aerodynamic performance','Design KEEP']
    }
    (out/'FREECAD_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    App.closeDocument(doc.Name); print(json.dumps(receipt,indent=2))

def reopen(out):
    native=out/'FREECAD_NURBS_SAME_SOURCE.FCStd'; before=json.loads((out/'FREECAD_BUILD_RECEIPT.json').read_text())
    doc=App.openDocument(str(native)); obj=doc.getObject(OBJ); doc.recompute()
    if obj is None or obj.Shape.isNull() or not obj.Shape.isValid(): raise RuntimeError('native reopen invalid')
    after={'schema':'oleander.3d.nurbs-subd.same-source.freecad-reopen.v1','freecad_version':App.Version(),'native_reopen_valid':True,'shape_type':obj.Shape.ShapeType,'area_mm2':float(obj.Shape.Area),'bbox_mm':bbox(obj.Shape)}
    area_rel=abs(after['area_mm2']-before['shape']['area_mm2'])/max(before['shape']['area_mm2'],1.0)
    after['area_relative_error']=area_rel; after['bbox_size_delta_mm']=[abs(a-b) for a,b in zip(after['bbox_mm']['size'],before['shape']['bbox_mm']['size'])]
    after['overall_pass']=area_rel<1e-10 and max(after['bbox_size_delta_mm'])<1e-8
    (out/'FREECAD_REOPEN_RECEIPT.json').write_text(json.dumps(after,indent=2)+'\n'); print(json.dumps(after,indent=2))
    App.closeDocument(doc.Name)
    if not after['overall_pass']: raise SystemExit(7)

def main():
    out=Path(os.environ['OLEANDER_OUT']).resolve(); out.mkdir(parents=True,exist_ok=True); mode=os.environ.get('OLEANDER_MODE','build')
    if mode=='build': build(out,Path(os.environ['OLEANDER_SOURCE']).resolve())
    elif mode=='reopen': reopen(out)
    else: raise SystemExit('OLEANDER_MODE must be build or reopen')

if __name__=='__main__': main()
