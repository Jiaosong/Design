"""Temporary diagnostic for FreeCAD face-tilt kernel/persistence failure. Remove after diagnosis."""
import math
import os
import traceback
from pathlib import Path

import FreeCAD as App
import Part

ROOT = Path("/tmp/oleander-face-tilt-diagnostic")
ROOT.mkdir(parents=True, exist_ok=True)


def trace(label, **data):
    print("OLE_TILT_DIAG=" + label + (" " + repr(data) if data else ""), flush=True)


def normal(face):
    u0, u1, v0, v1 = face.ParameterRange
    n = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    n.normalize()
    return n


def same(a, b):
    return (a - b).Length <= 1e-6


def build(width, angle_deg):
    tag = f"w{int(width)}_a{angle_deg:+g}"
    shape = Part.makeBox(width, 50.0, 10.0)
    trace("case_base", case=tag, valid=shape.isValid(), solids=len(shape.Solids))
    top = [f for f in shape.Faces if f.BoundBox.ZLength <= 1e-6 and abs(f.BoundBox.ZMax-10.0)<=1e-6 and normal(f).z>0.999999][0]
    bottom = [f for f in shape.Faces if f.BoundBox.ZLength <= 1e-6 and abs(f.BoundBox.ZMin)<=1e-6 and normal(f).z<-0.999999][0]
    pts = [v.Point for v in top.OuterWire.OrderedVertexes]
    area2 = sum(p.x*pts[(i+1)%4].y-pts[(i+1)%4].x*p.y for i,p in enumerate(pts))
    if area2 < 0:
        pts.reverse()
    c = top.CenterOfMass
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    q = [App.Vector(c.x + ca*(p.x-c.x), p.y, c.z - sa*(p.x-c.x)) for p in pts]
    expected = App.Vector(math.sin(a),0,math.cos(a))
    new_top = Part.Face(Part.makePolygon(q+[q[0]]))
    if normal(new_top).dot(expected) < 0:
        new_top = new_top.reversed()
    actual = math.degrees(math.atan2(normal(new_top).x, normal(new_top).z))
    trace("new_top", case=tag, valid=new_top.isValid(), angle=actual, area=new_top.Area, min_z=min(p.z for p in q))
    reps=[(top,new_top)]
    zmin=shape.BoundBox.ZMin
    b=[App.Vector(p.x,p.y,zmin) for p in pts]
    for i,p0 in enumerate(pts):
        p1=pts[(i+1)%4]
        old=[]
        for f in shape.Faces:
            if f.isSame(top) or f.isSame(bottom):
                continue
            vs=[v.Point for v in f.Vertexes]
            if any(same(v,p0) for v in vs) and any(same(v,p1) for v in vs):
                old.append(f)
        assert len(old)==1, ("old_side",tag,i,len(old))
        poly=[b[i],b[(i+1)%4],q[(i+1)%4],q[i]]
        nf=Part.Face(Part.makePolygon(poly+[poly[0]]))
        if normal(nf).dot(normal(old[0])) < 0:
            nf=nf.reversed()
        trace("side", case=tag, i=i, valid=nf.isValid(), area=nf.Area)
        reps.append((old[0],nf))
    trace("before_replace", case=tag, count=len(reps))
    reshaped=shape.replaceShape(reps)
    trace("after_replace", case=tag, null=reshaped.isNull(), valid=reshaped.isValid(), faces=len(reshaped.Faces), solids=len(reshaped.Solids), type=reshaped.ShapeType)
    candidate=reshaped.copy()
    candidate.sewShape(1e-7)
    trace("after_sew", case=tag, valid=candidate.isValid(), faces=len(candidate.Faces), solids=len(candidate.Solids), type=candidate.ShapeType)
    candidate.fix(1e-7,1e-7,1e-7)
    candidate=candidate.removeSplitter()
    trace("after_fix_cleanup", case=tag, valid=candidate.isValid(), faces=len(candidate.Faces), solids=len(candidate.Solids), type=candidate.ShapeType)
    if candidate.isValid() and len(candidate.Solids)==1:
        solid=candidate.Solids[0]
    else:
        shell=Part.makeShell(candidate.Faces)
        shell.sewShape(1e-7)
        shell.fix(1e-7,1e-7,1e-7)
        solid=Part.makeSolid(shell).removeSplitter()
    trace("final_solid", case=tag, valid=solid.isValid(), faces=len(solid.Faces), solids=len(solid.Solids), type=solid.ShapeType, bbox=[solid.BoundBox.XLength,solid.BoundBox.YLength,solid.BoundBox.ZLength], volume=solid.Volume)
    assert solid.isValid() and len(solid.Solids)==1
    return solid, actual


def main():
    cases=[]
    for width in (80.0,100.0):
        for angle in (5.0,-5.0):
            solid, actual=build(width,angle)
            cases.append((width,angle,solid,actual))

    trace("all_kernel_cases_pass", cases=[(w,a,ang,s.Volume) for w,a,s,ang in cases])
    doc=App.newDocument("OLE_TILT_DIAGNOSTIC")
    for width,angle,solid,actual in cases:
        name=f"CASE_W{int(width)}_{'POS' if angle>0 else 'NEG'}"
        obj=doc.addObject("PartDesign::Feature",name)
        obj.Shape=solid
        obj.addProperty("App::PropertyFloat","AngleDeg","Diag")
        obj.AngleDeg=angle
        obj.addProperty("App::PropertyString","Units","Diag")
        obj.Units="deg"
        trace("doc_add", name=name, angle=obj.AngleDeg, valid=obj.Shape.isValid())
    doc.recompute()
    fcstd=ROOT/"tilt_diag.FCStd"
    trace("before_save", path=str(fcstd))
    doc.saveAs(str(fcstd))
    trace("after_save", exists=fcstd.exists(), size=fcstd.stat().st_size if fcstd.exists() else 0)
    for obj in doc.Objects:
        step=ROOT/(obj.Name+".step")
        trace("before_step", name=obj.Name)
        obj.Shape.exportStep(str(step))
        trace("after_step", name=obj.Name, exists=step.exists(), size=step.stat().st_size if step.exists() else 0)
    App.closeDocument(doc.Name)
    trace("before_reopen")
    reopened=App.openDocument(str(fcstd))
    trace("after_reopen", objects=[o.Name for o in reopened.Objects])
    for obj in reopened.Objects:
        trace("reopen_obj", name=obj.Name, angle=float(obj.AngleDeg), valid=obj.Shape.isValid(), solids=len(obj.Shape.Solids))
        assert obj.Shape.isValid() and len(obj.Shape.Solids)==1
    App.closeDocument(reopened.Name)
    trace("done")


try:
    main()
except Exception as exc:
    trace("python_exception", error=repr(exc))
    traceback.print_exc()
    raise
