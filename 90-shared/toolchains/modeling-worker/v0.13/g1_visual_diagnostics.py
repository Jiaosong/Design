#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,struct,zlib
from pathlib import Path
import g1_geometry_core as core

def chunk(k,d): return struct.pack('>I',len(d))+k+d+struct.pack('>I',zlib.crc32(k+d)&0xffffffff)
def save_png(path,w,h,rgb):
    raw=bytearray(); stride=w*3
    for y in range(h): raw.append(0); raw.extend(rgb[y*stride:(y+1)*stride])
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(bytes(raw),9))+chunk(b'IEND',b''))
def line(img,w,h,x0,y0,x1,y1,shade):
    dx=abs(x1-x0); sx=1 if x0<x1 else -1; dy=-abs(y1-y0); sy=1 if y0<y1 else -1; err=dx+dy
    while True:
        if 0<=x0<w and 0<=y0<h:
            q=(y0*w+x0)*3; img[q:q+3]=bytes((shade,shade,shade))
        if x0==x1 and y0==y1: break
        e2=2*err
        if e2>=dy: err+=dy; x0+=sx
        if e2<=dx: err+=dx; y0+=sy

def rotate(p,yaw,pitch):
    x,y,z=p; cy=math.cos(yaw); sy=math.sin(yaw); x,y=cy*x-sy*y,sy*x+cy*y
    cp=math.cos(pitch); sp=math.sin(pitch); y,z=cp*y-sp*z,sp*y+cp*z; return x,y,z

def render(path,source,revision,view,w=900,h=620):
    img=bytearray([246]*(w*h*3)); nu=29; nv=36
    grid=[[core.point(source,i/(nu-1),2*math.pi*j/nv,revision) for j in range(nv)] for i in range(nu)]
    proj=[]
    for row in grid:
        rr=[]
        for p in row:
            if view=='side': q=(p[0],p[2])
            elif view=='top': q=(p[0],p[1])
            elif view=='front': q=(p[1],p[2])
            else:
                r=rotate(p,-.55,.42); q=(r[0],r[2])
            rr.append(q)
        proj.append(rr)
    xs=[p[0] for r in proj for p in r]; ys=[p[1] for r in proj for p in r]
    cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; span=max(max(xs)-min(xs),max(ys)-min(ys),1e-9); scale=.82*min(w,h)/span
    def sc(p): return int(w/2+(p[0]-cx)*scale),int(h/2-(p[1]-cy)*scale)
    for i in range(0,nu,2):
        for j in range(nv): line(img,w,h,*sc(proj[i][j]),*sc(proj[i][(j+1)%nv]),92)
    for j in range(0,nv,3):
        for i in range(nu-1): line(img,w,h,*sc(proj[i][j]),*sc(proj[i+1][j]),54)
    save_png(path,w,h,img)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    source=json.loads(Path(a.source).read_text()); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    for v in ('perspective','side','top','front'): render(out/f'G1_BASELINE_{v.upper()}.png',source,False,v)
    render(out/'G1_R1_THUMB_RELATION_PERSPECTIVE.png',source,True,'perspective')
    manifest={'schema':'oleander.modeling-worker.v0.13.g1.visual-diagnostics','authority':'DERIVED_EXECUTION_EVIDENCE','views':['G1_BASELINE_PERSPECTIVE.png','G1_BASELINE_SIDE.png','G1_BASELINE_TOP.png','G1_BASELINE_FRONT.png','G1_R1_THUMB_RELATION_PERSPECTIVE.png'],'visual_qa':'HUMAN_REQUIRED','project_qa':'HUMAN_REQUIRED','candidate_authority':False}
    (out/'G1_VISUAL_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n'); print(json.dumps(manifest,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
