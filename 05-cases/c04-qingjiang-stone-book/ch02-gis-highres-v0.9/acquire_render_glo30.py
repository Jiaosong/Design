#!/usr/bin/env python3
from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import math
import os
import pathlib
import tempfile
import urllib.parse
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import rasterio
from rasterio.windows import from_bounds
import requests

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "generated"
OUT.mkdir(parents=True, exist_ok=True)

# Current CH02 remote-analysis extent. This is an analytical corridor extent,
# NOT a surveyed site polygon / cadastral boundary.
WEST, SOUTH, EAST, NORTH = 109.7500, 30.2900, 109.8100, 30.3150
TILE_ID = "Copernicus_DSM_COG_10_N30_00_E109_00_DEM"
BUCKET = "https://copernicus-dem-30m.s3.amazonaws.com"
DIRECT = f"{BUCKET}/{TILE_ID}/{TILE_ID}.tif"

PAPER = "#F1EDE4"       # CH14 Bone Mist
INK = "#111918"         # CH14 River Black
DEEP = "#133B3C"        # CH14 Deep Water
JADE = "#2E7571"        # CH14 Jade Current
WET = "#65706A"         # CH14 Wet Stone
SAND = "#D8C9B1"        # CH14 Sediment Sand
RED = "#B8543E"         # CH14 Cinnabar
WHITE = "#FAF8F2"


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_tile() -> pathlib.Path:
    tmp = pathlib.Path(tempfile.gettempdir()) / f"{TILE_ID}.tif"
    urls = [DIRECT]
    # Robust fallback: public bucket listing by prefix.
    try:
        q = requests.get(BUCKET + "/", params={"list-type": "2", "prefix": TILE_ID}, timeout=30)
        if q.ok:
            root = ET.fromstring(q.text)
            ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
            keys = [e.text for e in root.findall("s3:Contents/s3:Key", ns) if e.text and e.text.endswith("_DEM.tif")]
            urls.extend([BUCKET + "/" + urllib.parse.quote(k, safe="/") for k in keys])
    except Exception:
        pass
    seen = set()
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        try:
            with requests.get(url, stream=True, timeout=60) as r:
                if not r.ok:
                    continue
                with tmp.open("wb") as f:
                    for chunk in r.iter_content(1024 * 1024):
                        if chunk:
                            f.write(chunk)
            if tmp.stat().st_size > 1_000_000:
                return tmp
        except Exception:
            continue
    raise RuntimeError("Copernicus GLO-30 tile could not be materialized from public S3")


def crop_tile(src_path: pathlib.Path):
    crop_path = OUT / "C04_CH02_GLO30_AOI_CROP.tif"
    with rasterio.open(src_path) as src:
        if not src.crs:
            raise RuntimeError("DEM CRS missing")
        window = from_bounds(WEST, SOUTH, EAST, NORTH, transform=src.transform)
        window = window.round_offsets().round_lengths()
        arr = src.read(1, window=window, boundless=False).astype(np.float32)
        transform = src.window_transform(window)
        nodata = src.nodata
        profile = src.profile.copy()
        profile.update(
            driver="GTiff",
            height=arr.shape[0],
            width=arr.shape[1],
            transform=transform,
            count=1,
            dtype="float32",
            compress="DEFLATE",
            predictor=3,
        )
        with rasterio.open(crop_path, "w", **profile) as dst:
            dst.write(arr, 1)
        meta = {
            "dataset": "Copernicus DEM GLO-30 Public",
            "surface_model": "DSM / not bare-earth DTM",
            "source_tile": TILE_ID,
            "source_tile_url": DIRECT,
            "source_tile_sha256": sha256(src_path),
            "crop_sha256": sha256(crop_path),
            "crs": str(src.crs),
            "source_resolution": [float(src.transform.a), float(abs(src.transform.e))],
            "crop_shape": [int(arr.shape[0]), int(arr.shape[1])],
            "crop_bounds_requested_wgs84": [WEST, SOUTH, EAST, NORTH],
            "crop_transform": list(transform)[:6],
            "nodata": nodata,
            "does_not_prove": [
                "surveyed site boundary",
                "field-measured elevation",
                "bare-earth terrain under vegetation/buildings",
                "construction or safety suitability",
            ],
        }
    return crop_path, arr, transform, meta


def terrain_derivatives(z: np.ndarray, transform):
    lat_mid = (SOUTH + NORTH) / 2
    dx = abs(transform.a) * 111320.0 * math.cos(math.radians(lat_mid))
    dy = abs(transform.e) * 111320.0
    valid = np.isfinite(z)
    if not valid.all():
        med = float(np.nanmedian(z))
        z = np.where(valid, z, med)
    gy, gx = np.gradient(z, dy, dx)
    slope = np.degrees(np.arctan(np.hypot(gx, gy))).astype(np.float32)
    aspect = (np.degrees(np.arctan2(gx, -gy)) + 360.0) % 360.0

    # Multi-directional-style relief: combine four hillshades, source geometry unchanged.
    slope_r = np.arctan(np.hypot(gx, gy))
    aspect_r = np.arctan2(gx, -gy)
    shades = []
    alt = math.radians(42)
    for az_d in (315, 45, 135, 225):
        az = math.radians(az_d)
        hs = np.sin(alt) * np.cos(slope_r) + np.cos(alt) * np.sin(slope_r) * np.cos(az - aspect_r)
        shades.append(np.clip(hs, 0, 1))
    hill = np.mean(shades, axis=0).astype(np.float32)

    # D8 receiver + contributing-cell accumulation. This is potential convergence
    # on the DSM surface, not an observed drainage network.
    h, w = z.shape
    receiver = np.full(h * w, -1, dtype=np.int32)
    for r in range(h):
        for c in range(w):
            i = r * w + c
            best = z[r, c]
            best_i = -1
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < h and 0 <= cc < w and z[rr, cc] < best:
                        best = z[rr, cc]
                        best_i = rr * w + cc
            receiver[i] = best_i
    acc = np.ones(h * w, dtype=np.float64)
    order = np.argsort(z.reshape(-1))[::-1]
    for i in order:
        j = receiver[i]
        if j >= 0:
            acc[j] += acc[i]
    acc = acc.reshape(h, w).astype(np.float32)

    # Relative solar exposure scenarios, geometry-based only.
    def solar(az_deg, alt_deg):
        az = math.radians(az_deg)
        altv = math.radians(alt_deg)
        cosi = np.sin(altv) * np.cos(slope_r) + np.cos(altv) * np.sin(slope_r) * np.cos(az - aspect_r)
        return np.clip(cosi, 0, 1).astype(np.float32)
    sol_summer = solar(180, 83)
    sol_equinox = solar(180, 60)
    sol_winter = solar(180, 36)
    return z, slope, aspect.astype(np.float32), hill, receiver, acc, sol_summer, sol_equinox, sol_winter, dx, dy


def save_grid_csv(z, slope, aspect, acc, sw, transform):
    p = OUT / "C04_CH02_GLO30_DERIVED_GRID.csv"
    h, w = z.shape
    with p.open("w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["row", "col", "longitude", "latitude", "elevation_dsm_m", "slope_deg", "aspect_deg_0N", "d8_accumulation_cells", "winter_relative_solar"])
        for r in range(h):
            for c in range(w):
                lon, lat = rasterio.transform.xy(transform, r, c, offset="center")
                wr.writerow([r, c, f"{lon:.8f}", f"{lat:.8f}", f"{z[r,c]:.3f}", f"{slope[r,c]:.3f}", f"{aspect[r,c]:.3f}", f"{acc[r,c]:.1f}", f"{sw[r,c]:.5f}"])
    return p


def data_png(arr: np.ndarray, mode: str) -> str:
    a = np.asarray(arr, dtype=float)
    lo, hi = np.nanpercentile(a, [2, 98])
    t = np.clip((a - lo) / max(hi - lo, 1e-9), 0, 1)
    if mode == "hill":
        # Neutral relief; no decorative blur.
        c0 = np.array([241, 237, 228], float)
        c1 = np.array([92, 112, 106], float)
        rgb = c0[None,None,:] * (1-t[...,None]) + c1[None,None,:] * t[...,None]
    elif mode == "slope":
        stops = np.array([[241,237,228],[216,201,177],[126,158,151],[46,117,113],[184,84,62]], float)
        pos = np.clip(t * (len(stops)-1), 0, len(stops)-1-1e-6)
        i = pos.astype(int); u = (pos-i)[...,None]
        rgb = stops[i]*(1-u) + stops[i+1]*u
    elif mode == "solar":
        stops = np.array([[19,59,60],[46,117,113],[216,201,177],[241,237,228]], float)
        pos = np.clip(t * (len(stops)-1), 0, len(stops)-1-1e-6)
        i = pos.astype(int); u = (pos-i)[...,None]
        rgb = stops[i]*(1-u) + stops[i+1]*u
    else:
        rgb = np.repeat((t*255)[...,None], 3, axis=2)
    im = Image.fromarray(np.clip(rgb,0,255).astype(np.uint8), "RGB")
    bio = io.BytesIO(); im.save(bio, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(bio.getvalue()).decode("ascii")


def contour_segments(z, transform, interval=20.0):
    h, w = z.shape
    xmin = transform.c
    ymax = transform.f
    xmax = xmin + transform.a * w
    ymin = ymax + transform.e * h
    low = math.floor(float(np.nanmin(z))/interval)*interval
    high = math.ceil(float(np.nanmax(z))/interval)*interval
    levels = np.arange(low, high+interval, interval)
    fig, ax = plt.subplots(figsize=(6,4))
    cs = ax.contour(np.linspace(xmin,xmax,w), np.linspace(ymax,ymin,h), z, levels=levels)
    out = []
    for lvl, segs in zip(cs.levels, cs.allsegs):
        for seg in segs:
            if len(seg) > 2:
                out.append((float(lvl), seg.tolist()))
    plt.close(fig)
    return out


def svg_header(title, fig_id):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="3200" height="1800" viewBox="0 0 3200 1800">
<rect width="3200" height="1800" fill="{PAPER}"/>
<text x="110" y="82" font-family="Noto Sans Mono CJK SC,monospace" font-size="18" font-weight="700" letter-spacing="3" fill="{RED}">PRJ-C04 / CH02 / {fig_id} / GLO-30</text>
<text x="110" y="158" font-family="Noto Serif CJK SC,serif" font-size="62" font-weight="400" fill="{INK}">{title}</text>
<line x1="110" y1="196" x2="3090" y2="196" stroke="{INK}" stroke-opacity=".18"/>
'''


def map_xy(lon, lat, box):
    x,y,w,h = box
    return x + (lon-WEST)/(EAST-WEST)*w, y + (NORTH-lat)/(NORTH-SOUTH)*h


def contour_svg(segs, box, opacity=.44):
    parts=[]
    for lvl, seg in segs:
        pts = [map_xy(p[0], p[1], box) for p in seg]
        if len(pts)<2: continue
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        major = int(round(lvl)) % 100 == 0
        parts.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-opacity="{opacity if major else opacity*.55:.3f}" stroke-width="{2.0 if major else 0.85}"/>')
    return "".join(parts)


def section_profile(z, transform, p0, p1, n=220):
    xs=np.linspace(p0[0],p1[0],n); ys=np.linspace(p0[1],p1[1],n)
    inv=~transform
    vals=[]
    for lon,lat in zip(xs,ys):
        c,r=inv*(lon,lat)
        rr=int(np.clip(round(r),0,z.shape[0]-1)); cc=int(np.clip(round(c),0,z.shape[1]-1))
        vals.append(float(z[rr,cc]))
    return np.array(vals)


def add_section_svg(parts, z, transform, p0, p1, box, label):
    x,y,w,h=box
    prof=section_profile(z,transform,p0,p1)
    mn,mx=float(prof.min()),float(prof.max())
    pts=[]
    for i,v in enumerate(prof):
        xx=x+i/(len(prof)-1)*w; yy=y+h-(v-mn)/max(mx-mn,1e-6)*(h-34)
        pts.append((xx,yy))
    d="M"+" L".join(f"{a:.1f},{b:.1f}" for a,b in pts)
    parts.append(f'<line x1="{x}" y1="{y+h}" x2="{x+w}" y2="{y+h}" stroke="{INK}" stroke-opacity=".28"/>')
    parts.append(f'<path d="{d}" fill="none" stroke="{DEEP}" stroke-width="3"/>')
    parts.append(f'<text x="{x}" y="{y-14}" font-family="Noto Sans Mono CJK SC,monospace" font-size="15" font-weight="700" fill="{RED}">{label} · {mn:.0f}–{mx:.0f} m DSM</text>')


def render_env01(z,slope,aspect,hill,transform,segs,meta):
    box=(110,250,2220,1220)
    parts=[svg_header("坡度—坡向｜地形先于色块", "ENV-01")]
    x,y,w,h=box
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WHITE}"/>')
    parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" opacity=".52" href="{data_png(hill,"hill")}"/>')
    parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" opacity=".52" href="{data_png(slope,"slope")}"/>')
    parts.append(contour_svg(segs,box,.56))
    p90=float(np.percentile(slope,90)); p50=float(np.percentile(slope,50)); mx=float(np.max(slope))
    # section lines mapped to plan
    sec1=((WEST, (SOUTH+NORTH)/2),(EAST,(SOUTH+NORTH)/2))
    sec2=((WEST+.012,SOUTH+.002),(EAST-.010,NORTH-.002))
    for lab,pp,col in [("SEC-T01",sec1,RED),("SEC-T02",sec2,JADE)]:
        a=map_xy(*pp[0],box); b=map_xy(*pp[1],box)
        parts.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{col}" stroke-width="2.2" stroke-dasharray="12 8"/>')
        parts.append(f'<text x="{a[0]+10}" y="{a[1]-10}" font-family="Noto Sans Mono CJK SC,monospace" font-size="14" fill="{col}">{lab}</text>')
    # editorial rail, no dashboard cards
    rx=2390
    parts.append(f'<text x="{rx}" y="284" font-family="Noto Serif CJK SC,serif" font-size="32" fill="{DEEP}">连续地貌是第一阅读。</text>')
    parts.append(f'<text x="{rx}" y="338" font-family="Noto Sans CJK SC,sans-serif" font-size="19" fill="{WET}">坡度综合色只承担一个变量；等高线、河谷起伏与剖面保持可追溯。</text>')
    for yy,val,lab,col in [(430,p50,"MEDIAN SLOPE",INK),(530,p90,"P90 SLOPE",RED),(630,mx,"MAX CELL SLOPE",DEEP)]:
        parts.append(f'<text x="{rx}" y="{yy}" font-family="Noto Serif CJK SC,serif" font-size="48" fill="{col}">{val:.1f}°</text>')
        parts.append(f'<text x="{rx}" y="{yy+30}" font-family="Noto Sans Mono CJK SC,monospace" font-size="14" letter-spacing="2" fill="{WET}">{lab}</text>')
    # aspect octant counts
    bins=np.histogram(aspect,bins=np.arange(0,361,45))[0]; labs=["N","NE","E","SE","S","SW","W","NW"]
    parts.append(f'<text x="{rx}" y="740" font-family="Noto Sans Mono CJK SC,monospace" font-size="15" font-weight="700" fill="{RED}">ASPECT / 8 OCTANTS</text>')
    maxc=max(int(bins.max()),1)
    for i,(lab,cnt) in enumerate(zip(labs,bins)):
        yy=780+i*44; bw=260*cnt/maxc
        parts.append(f'<text x="{rx}" y="{yy}" font-family="monospace" font-size="14" fill="{WET}">{lab}</text>')
        parts.append(f'<rect x="{rx+52}" y="{yy-15}" width="{bw:.1f}" height="15" fill="{JADE}" fill-opacity=".74"/>')
        parts.append(f'<text x="{rx+330}" y="{yy}" font-family="monospace" font-size="13" fill="{INK}">{int(cnt)}</text>')
    add_section_svg(parts,z,transform,*sec1,(2390,1190,650,150),"SEC-T01")
    add_section_svg(parts,z,transform,*sec2,(2390,1445,650,150),"SEC-T02")
    parts.append(f'<text x="110" y="1565" font-family="Noto Sans CJK SC,sans-serif" font-size="18" fill="{INK}">SPATIAL FINDING → 陡坡不是一圈综合色，而是沿连续地形中出现的高坡度带与转折面。</text>')
    parts.append(f'<text x="110" y="1605" font-family="Noto Sans CJK SC,sans-serif" font-size="18" fill="{INK}">FIELD CONSEQUENCE → 优先核验高坡度带附近的雨后通过、边缘感、维护与真实微地形。</text>')
    parts.append(f'<text x="110" y="1692" font-family="Noto Sans Mono CJK SC,monospace" font-size="13" fill="{WET}">COPERNICUS GLO-30 DSM · REAL CROP {z.shape[1]}×{z.shape[0]} CELLS · DERIVED SLOPE/ASPECT · NOT SURVEY · FIELD OPEN</text>')
    parts.append('</svg>')
    (OUT/"C04_CH02_ENV01_SLOPE_ASPECT_GLO30_CH14.svg").write_text("".join(parts),encoding="utf-8")


def render_env02(z,hill,receiver,acc,transform,segs):
    box=(110,250,2220,1220); x,y,w,h=box
    parts=[svg_header("潜在汇水｜从色块改成流动层级", "ENV-02")]
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WHITE}"/>')
    parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" opacity=".48" href="{data_png(hill,"hill")}"/>')
    parts.append(contour_svg(segs,box,.30))
    hh,ww=z.shape
    vals=acc.reshape(-1); positive=vals[vals>1]
    th1=float(np.percentile(positive,82)); th2=float(np.percentile(positive,94)); th3=float(np.percentile(positive,99))
    def cell_lonlat(idx):
        r=idx//ww; c=idx%ww
        return rasterio.transform.xy(transform,r,c,offset="center")
    # Draw derived D8 links only for accumulated cells, with hierarchy.
    for i,a in enumerate(vals):
        j=int(receiver[i])
        if j<0 or a<th1: continue
        lon1,lat1=cell_lonlat(i); lon2,lat2=cell_lonlat(j)
        p1=map_xy(lon1,lat1,box); p2=map_xy(lon2,lat2,box)
        if a>=th3: sw,op=4.2,.95
        elif a>=th2: sw,op=2.5,.84
        else: sw,op=1.2,.57
        parts.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="{JADE}" stroke-width="{sw}" stroke-opacity="{op}"/>')
    # convergence nodes top 0.5%
    node_th=float(np.percentile(vals,99.5))
    for i,a in enumerate(vals):
        if a<node_th: continue
        lon,lat=cell_lonlat(i); px,py=map_xy(lon,lat,box)
        rr=5+10*math.log1p(a)/max(math.log1p(vals.max()),1)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rr:.1f}" fill="{PAPER}" stroke="{RED}" stroke-width="2.2"/>')
    rx=2390
    parts.append(f'<text x="{rx}" y="284" font-family="Noto Serif CJK SC,serif" font-size="32" fill="{DEEP}">先读低势面，再读收敛层级。</text>')
    parts.append(f'<text x="{rx}" y="338" font-family="Noto Sans CJK SC,sans-serif" font-size="19" fill="{WET}">D8 由真实 30 m DSM 派生；线宽只表示 contributing-cell hierarchy，不冒充实测沟渠。</text>')
    metrics=[("82% LINK THRESHOLD",th1,INK),("94% MAIN LINKS",th2,JADE),("99% PRIMARY LINKS",th3,DEEP),("MAX ACCUMULATION",float(vals.max()),RED)]
    for k,(lab,v,col) in enumerate(metrics):
        yy=460+k*108
        parts.append(f'<text x="{rx}" y="{yy}" font-family="Noto Serif CJK SC,serif" font-size="46" fill="{col}">{v:.0f}</text>')
        parts.append(f'<text x="{rx}" y="{yy+29}" font-family="Noto Sans Mono CJK SC,monospace" font-size="13" letter-spacing="1.8" fill="{WET}">{lab} · CELLS</text>')
    parts.append(f'<line x1="{rx}" y1="920" x2="3040" y2="920" stroke="{INK}" stroke-opacity=".18"/>')
    parts.append(f'<text x="{rx}" y="968" font-family="Noto Sans Mono CJK SC,monospace" font-size="15" font-weight="700" fill="{RED}">DOES NOT PROVE</text>')
    deny=["observed drainage network","hydraulic capacity / flood extent","culvert / engineered drainage","geohazard safety"]
    for i,s in enumerate(deny):
        parts.append(f'<text x="{rx}" y="{1010+i*38}" font-family="Noto Sans CJK SC,sans-serif" font-size="17" fill="{INK}">— {s}</text>')
    # section through strongest convergence
    imax=int(np.argmax(vals)); lonm,latm=cell_lonlat(imax)
    p0=(WEST,max(SOUTH,min(NORTH,latm))); p1=(EAST,max(SOUTH,min(NORTH,latm)))
    a=map_xy(*p0,box); b=map_xy(*p1,box)
    parts.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{RED}" stroke-width="2" stroke-dasharray="12 8"/>')
    add_section_svg(parts,z,transform,p0,p1,(2390,1325,650,160),"SEC-H01 / MAX CONVERGENCE")
    parts.append(f'<text x="110" y="1565" font-family="Noto Sans CJK SC,sans-serif" font-size="18" fill="{INK}">SPATIAL FINDING → 收敛关系应读成支线—主线—节点的层级，而不是一整幅大综合色栅格。</text>')
    parts.append(f'<text x="110" y="1605" font-family="Noto Sans CJK SC,sans-serif" font-size="18" fill="{INK}">FIELD CONSEQUENCE → 高收敛点只触发雨后湿滑 / 排水 / 维护观察优先级，不直接生成风险等级。</text>')
    parts.append(f'<text x="110" y="1692" font-family="Noto Sans Mono CJK SC,monospace" font-size="13" fill="{WET}">COPERNICUS GLO-30 DSM · D8 POTENTIAL CONVERGENCE · NOT OBSERVED WATERCOURSE · FIELD OPEN</text>')
    parts.append('</svg>')
    (OUT/"C04_CH02_ENV02_DRAINAGE_GLO30_CH14.svg").write_text("".join(parts),encoding="utf-8")


def render_syn(z,slope,acc,sw,hill,transform,segs):
    parts=[svg_header("环境综合｜同范围 small multiples，不做风险热区", "ENV-SYN-01")]
    parts.append(f'<text x="110" y="238" font-family="Noto Sans CJK SC,sans-serif" font-size="20" fill="{WET}">同一 extent / north / scale / terrain base。每个面板只回答一个问题；综合页只负责比较，不制造单一风险分数。</text>')
    panels=[
        (110,310,900,900,"A / SLOPE",slope,"slope"),
        (1150,310,900,900,"B / D8 ACCUMULATION",np.log1p(acc),"solar"),
        (2190,310,900,900,"C / WINTER SOLAR",sw,"solar"),
    ]
    for x,y,w,h,lab,arr,mode in panels:
        box=(x,y,w,h)
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WHITE}"/>')
        parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" opacity=".38" href="{data_png(hill,"hill")}"/>')
        parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" opacity=".62" href="{data_png(arr,mode)}"/>')
        parts.append(contour_svg(segs,box,.25))
        parts.append(f'<text x="{x}" y="{y-20}" font-family="Noto Sans Mono CJK SC,monospace" font-size="16" font-weight="700" fill="{RED}">{lab}</text>')
    # Bottom evidence → finding → consequence strip.
    y0=1320
    parts.append(f'<line x1="110" y1="{y0}" x2="3090" y2="{y0}" stroke="{INK}" stroke-opacity=".22"/>')
    cols=[
        (110,"EVIDENCE","GLO-30 DSM / slope + D8 + relative solar","真实栅格 / 远程分析；ENV-03 / ENV-04 仍 HOLD。"),
        (1110,"SPATIAL FINDING","Terrain / convergence / exposure remain separate","不把三个变量压成一张“综合色越深越危险”的图。"),
        (2110,"DESIGN / FIELD CONSEQUENCE","Verification priority, not site verdict","把问题送回 FIELD：通过、湿滑、维护、可见度与 Return。"),
    ]
    for x,head,en,cn in cols:
        parts.append(f'<text x="{x}" y="1380" font-family="Noto Sans Mono CJK SC,monospace" font-size="15" font-weight="700" letter-spacing="2" fill="{RED}">{head}</text>')
        parts.append(f'<text x="{x}" y="1430" font-family="Noto Serif CJK SC,serif" font-size="24" fill="{DEEP}">{en}</text>')
        parts.append(f'<text x="{x}" y="1475" font-family="Noto Sans CJK SC,sans-serif" font-size="18" fill="{INK}">{cn}</text>')
    parts.append(f'<text x="110" y="1692" font-family="Noto Sans Mono CJK SC,monospace" font-size="13" fill="{WET}">LOCKED COMPARISON EXTENT · NO IMAGE GENERATION · ENV-03 LAND COVER HOLD · ENV-04 WATER HISTORY HOLD · NO RISK SCORE</text>')
    parts.append('</svg>')
    (OUT/"C04_CH02_ENV_SYN_01_GLO30_CH14.svg").write_text("".join(parts),encoding="utf-8")


def main():
    tile=fetch_tile()
    crop,z,transform,meta=crop_tile(tile)
    z,slope,aspect,hill,receiver,acc,ss,se,sw,dx,dy=terrain_derivatives(z,transform)
    meta.update({
        "effective_cell_size_m_approx": [dx,dy],
        "elevation_stats_m": {"min":float(z.min()),"median":float(np.median(z)),"max":float(z.max())},
        "slope_stats_deg": {"median":float(np.median(slope)),"p90":float(np.percentile(slope,90)),"max":float(slope.max())},
        "d8_accumulation_cells": {"p90":float(np.percentile(acc,90)),"p99":float(np.percentile(acc,99)),"max":float(acc.max())},
        "solar_relative_mean": {"summer":float(ss.mean()),"equinox":float(se.mean()),"winter":float(sw.mean())},
        "truth_state": "REMOTE SOURCE-GROUNDED / FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS",
    })
    (OUT/"C04_CH02_GLO30_SOURCE_AUTHORITY.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
    np.savez_compressed(OUT/"C04_CH02_GLO30_DERIVED.npz", elevation=z,slope=slope,aspect=aspect,hillshade=hill,receiver=receiver,accumulation=acc,solar_summer=ss,solar_equinox=se,solar_winter=sw,transform=np.array(list(transform)[:6]))
    save_grid_csv(z,slope,aspect,acc,sw,transform)
    segs=contour_segments(z,transform,20.0)
    render_env01(z,slope,aspect,hill,transform,segs,meta)
    render_env02(z,hill,receiver,acc,transform,segs)
    render_syn(z,slope,acc,sw,hill,transform,segs)
    receipt={
        "project_id":"PRJ-C04-QINGJIANG-SHISHU",
        "chapter":"CH02",
        "version":"v0.9 GLO-30 landscape analytical drawing redo",
        "skills":["oleander-data-viz","Landscape GIS Analysis Drawing Binding","Cartographic Task Hierarchy","oleander-story-and-board","oleander-delivery-qc"],
        "style_authority":"CH14 P04/P05/P06/P07; exact palette inherited from CH09-P01 CH14 rebuild",
        "no_image_generation":True,
        "native_outputs":["ENV-01 SVG","ENV-02 SVG","ENV-SYN-01 SVG","GeoTIFF crop","CSV","NPZ","source authority JSON"],
        "review":"PRODUCER EXECUTION ONLY / INDEPENDENT PROFESSIONAL DESIGN REVIEW PENDING",
        "truth":"FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS",
    }
    (OUT/"C04_CH02_GIS_GLO30_EXECUTION_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding="utf-8")
    manifest={}
    for p in sorted(OUT.iterdir()):
        if p.is_file(): manifest[p.name]={"bytes":p.stat().st_size,"sha256":sha256(p)}
    (OUT/"MANIFEST_SHA256.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(meta,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
