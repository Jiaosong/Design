"""Temporary diagnostic for FreeCAD face-tilt kernel failure. Remove after diagnosis."""
import math
import traceback
import FreeCAD as App
import Part


def trace(label, **data):
    print("OLE_TILT_DIAG=" + label + (" " + repr(data) if data else ""), flush=True)


def normal(face):
    u0, u1, v0, v1 = face.ParameterRange
    n = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    n.normalize()
    return n


def same(a, b):
    return (a - b).Length <= 1e-6


def main():
    shape = Part.makeBox(80.0, 50.0, 10.0)
    trace("base", valid=shape.isValid(), solids=len(shape.Solids))
    top = [f for f in shape.Faces if f.BoundBox.ZLength <= 1e-6 and abs(f.BoundBox.ZMax-10.0)<=1e-6 and normal(f).z>0.999999][0]
    bottom = [f for f in shape.Faces if f.BoundBox.ZLength <= 1e-6 and abs(f.BoundBox.ZMin)<=1e-6 and normal(f).z<-0.999999][0]
    trace("selectors", top=normal(top), bottom=normal(bottom))
    pts = [v.Point for v in top.OuterWire.OrderedVertexes]
    area2 = sum(p.x*pts[(i+1)%4].y-pts[(i+1)%4].x*p.y for i,p in enumerate(pts))
    if area2 < 0:
        pts.reverse()
    c = top.CenterOfMass
    a = math.radians(5.0)
    ca, sa = math.cos(a), math.sin(a)
    q = [App.Vector(c.x + ca*(p.x-c.x), p.y, c.z - sa*(p.x-c.x)) for p in pts]
    expected = App.Vector(math.sin(a),0,math.cos(a))
    wire = Part.makePolygon(q+[q[0]])
    new_top = Part.Face(wire)
    if normal(new_top).dot(expected) < 0:
        new_top = new_top.reversed()
    trace("new_top", valid=new_top.isValid(), n=normal(new_top), area=new_top.Area)
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
        assert len(old)==1, ("old_side",i,len(old))
        poly=[b[i],b[(i+1)%4],q[(i+1)%4],q[i]]
        nf=Part.Face(Part.makePolygon(poly+[poly[0]]))
        if normal(nf).dot(normal(old[0])) < 0:
            nf=nf.reversed()
        trace("side", i=i, valid=nf.isValid(), n=normal(nf), area=nf.Area)
        reps.append((old[0],nf))
    trace("before_replace", count=len(reps))
    reshaped=shape.replaceShape(reps)
    trace("after_replace", null=reshaped.isNull(), valid=reshaped.isValid(), faces=len(reshaped.Faces), solids=len(reshaped.Solids), type=reshaped.ShapeType)
    candidate=reshaped.copy()
    trace("before_sew")
    candidate.sewShape(1e-7)
    trace("after_sew", valid=candidate.isValid(), faces=len(candidate.Faces), solids=len(candidate.Solids), type=candidate.ShapeType)
    candidate.fix(1e-7,1e-7,1e-7)
    trace("after_fix", valid=candidate.isValid(), faces=len(candidate.Faces), solids=len(candidate.Solids), type=candidate.ShapeType)
    candidate=candidate.removeSplitter()
    trace("after_remove_splitter", valid=candidate.isValid(), faces=len(candidate.Faces), solids=len(candidate.Solids), type=candidate.ShapeType)
    if not (candidate.isValid() and len(candidate.Solids)==1):
        trace("before_shell_rebuild")
        shell=Part.makeShell(candidate.Faces)
        trace("made_shell", valid=shell.isValid(), type=shell.ShapeType)
        shell.sewShape(1e-7)
        shell.fix(1e-7,1e-7,1e-7)
        solid=Part.makeSolid(shell).removeSplitter()
        trace("rebuilt_solid", valid=solid.isValid(), faces=len(solid.Faces), solids=len(solid.Solids), type=solid.ShapeType)
    trace("done")


try:
    main()
except Exception as exc:
    trace("python_exception", error=repr(exc))
    traceback.print_exc()
    raise
