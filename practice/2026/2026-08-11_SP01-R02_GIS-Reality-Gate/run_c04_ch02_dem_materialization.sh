#!/usr/bin/env bash
set -euo pipefail

# TEMP EXECUTION ADAPTER / DO NOT MERGE.
# Reuses the already validated SP01 QGIS/GDAL runtime only to materialize
# C04 CH02 real terrain bytes. It does not change SP01 method authority.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$ROOT/outputs/c04_ch02"
WORK="$OUT/work"
rm -rf "$OUT"
mkdir -p "$WORK"

WEST=109.7500
SOUTH=30.2900
EAST=109.8100
NORTH=30.3150
TILE=N30E109
GLO_ID=Copernicus_DSM_COG_10_N30_00_E109_00_DEM
GLO_URL="https://copernicus-dem-30m.s3.amazonaws.com/${GLO_ID}/${GLO_ID}.tif"
ESA_URL="https://step.esa.int/auxdata/dem/SRTMGL1/${TILE}.SRTMGL1.hgt.zip"
MAPZEN_URL="https://s3.amazonaws.com/elevation-tiles-prod/skadi/N30/${TILE}.hgt.gz"

SOURCE_TYPE=""
SOURCE_URL=""
SOURCE="$WORK/source_dem"

try_raster() {
  local url="$1" dest="$2"
  if curl -L --fail --retry 2 --retry-delay 2 --connect-timeout 20 --max-time 180 -o "$dest" "$url"; then
    if gdalinfo "$dest" >/dev/null 2>&1; then return 0; fi
  fi
  return 1
}

if try_raster "$GLO_URL" "$WORK/glo30.tif"; then
  SOURCE_TYPE="COPERNICUS_GLO30_DSM"
  SOURCE_URL="$GLO_URL"
  SOURCE="$WORK/glo30.tif"
elif curl -L --fail --retry 2 --connect-timeout 20 --max-time 180 -o "$WORK/srtm.zip" "$ESA_URL" && unzip -q "$WORK/srtm.zip" -d "$WORK/srtm" && test -s "$WORK/srtm/${TILE}.hgt"; then
  SOURCE_TYPE="ESA_SRTMGL1_HGT"
  SOURCE_URL="$ESA_URL"
  SOURCE="$WORK/srtm/${TILE}.hgt"
elif curl -L --fail --retry 2 --connect-timeout 20 --max-time 180 -o "$WORK/mapzen.hgt.gz" "$MAPZEN_URL"; then
  gzip -dc "$WORK/mapzen.hgt.gz" > "$WORK/${TILE}.hgt"
  gdalinfo "$WORK/${TILE}.hgt" >/dev/null
  SOURCE_TYPE="MAPZEN_SKADI_HGT_FALLBACK"
  SOURCE_URL="$MAPZEN_URL"
  SOURCE="$WORK/${TILE}.hgt"
else
  echo "C04 CH02 DEM MATERIALIZATION FAILED" >&2
  exit 41
fi

printf '%s\n' "$SOURCE_TYPE" > "$OUT/source_type.txt"
printf '%s\n' "$SOURCE_URL" > "$OUT/source_url.txt"
sha256sum "$SOURCE" > "$OUT/source_sha256.txt"
wc -c "$SOURCE" > "$OUT/source_bytes.txt"
gdalinfo -json -stats "$SOURCE" > "$OUT/source_gdalinfo.json"

# Current CH02 ANALYSIS EXTENT only. This is not a surveyed site polygon.
gdal_translate \
  -projwin "$WEST" "$NORTH" "$EAST" "$SOUTH" \
  -projwin_srs EPSG:4326 \
  -of GTiff -co COMPRESS=DEFLATE \
  "$SOURCE" "$OUT/C04_CH02_SOURCE_CROP_WGS84.tif"

gdalinfo -json -stats "$OUT/C04_CH02_SOURCE_CROP_WGS84.tif" > "$OUT/crop_wgs84_gdalinfo.json"

# UTM 49N is used only as the metric analytical CRS for this longitude/latitude extent.
# TAP introduces a small rotated-edge envelope; explicit dst NoData prevents those cells
# from becoming false zero elevations or contaminating derivatives.
gdalwarp -overwrite \
  -t_srs EPSG:32649 -tr 30 30 -tap -r bilinear -dstnodata -9999 \
  -co COMPRESS=DEFLATE \
  "$OUT/C04_CH02_SOURCE_CROP_WGS84.tif" "$OUT/C04_CH02_TERRAIN_UTM49N_30M.tif"

gdalinfo -json -stats "$OUT/C04_CH02_TERRAIN_UTM49N_30M.tif" > "$OUT/terrain_utm49n_gdalinfo.json"

gdaldem slope "$OUT/C04_CH02_TERRAIN_UTM49N_30M.tif" "$OUT/C04_CH02_SLOPE_DEG.tif" -compute_edges -of GTiff -co COMPRESS=DEFLATE
gdaldem aspect "$OUT/C04_CH02_TERRAIN_UTM49N_30M.tif" "$OUT/C04_CH02_ASPECT_DEG.tif" -compute_edges -zero_for_flat -of GTiff -co COMPRESS=DEFLATE
gdaldem hillshade "$OUT/C04_CH02_TERRAIN_UTM49N_30M.tif" "$OUT/C04_CH02_HILLSHADE_MULTI.tif" -multidirectional -compute_edges -of GTiff -co COMPRESS=DEFLATE
gdal_contour -i 20 -a elev -f GeoJSON "$OUT/C04_CH02_TERRAIN_UTM49N_30M.tif" "$OUT/C04_CH02_CONTOUR_20M.geojson"

# D8 accumulation + relative solar are derived from the actual metric raster.
/usr/bin/python3 - <<'PY'
from osgeo import gdal
import numpy as np, json, math
from pathlib import Path
out=Path('outputs/c04_ch02')

def read(path):
    ds=gdal.Open(str(path)); a=ds.GetRasterBand(1).ReadAsArray().astype(float); nd=ds.GetRasterBand(1).GetNoDataValue()
    if nd is not None: a[a==nd]=np.nan
    return ds,a

ds,z=read(out/'C04_CH02_TERRAIN_UTM49N_30M.tif')
valid=np.isfinite(z)
fill=float(np.nanmedian(z)); zz=np.where(valid,z,fill)
h,w=zz.shape
receiver=np.full(h*w,-1,dtype=np.int32)
for r in range(h):
  for c in range(w):
    i=r*w+c
    if not valid[r,c]: continue
    best=zz[r,c]; bj=-1
    for dr in (-1,0,1):
      for dc in (-1,0,1):
        if dr==0 and dc==0: continue
        rr,cc=r+dr,c+dc
        if 0<=rr<h and 0<=cc<w and valid[rr,cc] and zz[rr,cc] < best:
          best=zz[rr,cc]; bj=rr*w+cc
    receiver[i]=bj
acc=np.zeros(h*w,dtype=np.float64)
acc[valid.reshape(-1)]=1.0
for i in np.argsort(zz.reshape(-1))[::-1]:
  if not valid.reshape(-1)[i]: continue
  j=receiver[i]
  if j>=0: acc[j]+=acc[i]
acc=acc.reshape(h,w); acc[~valid]=np.nan

def write(name,a,nodata=-9999.0):
  drv=gdal.GetDriverByName('GTiff'); o=drv.Create(str(out/name),w,h,1,gdal.GDT_Float32,options=['COMPRESS=DEFLATE'])
  o.SetGeoTransform(ds.GetGeoTransform()); o.SetProjection(ds.GetProjection()); b=o.GetRasterBand(1); b.SetNoDataValue(nodata); b.WriteArray(np.where(np.isfinite(a),a,nodata).astype('float32')); b.FlushCache(); o=None
write('C04_CH02_D8_ACCUMULATION_CELLS.tif',acc)

_,slope=read(out/'C04_CH02_SLOPE_DEG.tif'); _,aspect=read(out/'C04_CH02_ASPECT_DEG.tif')
sr=np.radians(np.where(np.isfinite(slope),slope,0)); ar=np.radians(np.where(np.isfinite(aspect),aspect,0))
def solar(alt_deg,az_deg=180):
  alt=math.radians(alt_deg); az=math.radians(az_deg)
  v=np.sin(alt)*np.cos(sr)+np.cos(alt)*np.sin(sr)*np.cos(az-ar)
  v=np.clip(v,0,1); v[~valid]=np.nan; return v
summer=solar(83); equinox=solar(60); winter=solar(36)
write('C04_CH02_SOLAR_SUMMER_REL.tif',summer); write('C04_CH02_SOLAR_EQUINOX_REL.tif',equinox); write('C04_CH02_SOLAR_WINTER_REL.tif',winter)

stats={
 'terrain_shape_rows_cols':[int(h),int(w)],
 'cell_count_total':int(h*w),
 'cell_count_valid':int(valid.sum()),
 'cell_count_nodata':int((~valid).sum()),
 'elevation_m':{'min':float(np.nanmin(z)),'median':float(np.nanmedian(z)),'max':float(np.nanmax(z))},
 'slope_deg':{'median':float(np.nanmedian(slope)),'p90':float(np.nanpercentile(slope,90)),'max':float(np.nanmax(slope))},
 'd8_accumulation_cells':{'p90':float(np.nanpercentile(acc,90)),'p99':float(np.nanpercentile(acc,99)),'max':float(np.nanmax(acc))},
 'solar_relative_mean':{'summer':float(np.nanmean(summer)),'equinox':float(np.nanmean(equinox)),'winter':float(np.nanmean(winter))}
}
(out/'derived_stats.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
PY

# Lightweight review derivatives; final CH14 boards are rebuilt after artifact retrieval.
gdal_translate -of PNG -scale "$OUT/C04_CH02_HILLSHADE_MULTI.tif" "$OUT/PREVIEW_HILLSHADE.png"
gdal_translate -of PNG -scale 0 60 0 255 -ot Byte "$OUT/C04_CH02_SLOPE_DEG.tif" "$OUT/PREVIEW_SLOPE.png"
gdal_translate -of PNG -scale "$OUT/C04_CH02_D8_ACCUMULATION_CELLS.tif" "$OUT/PREVIEW_D8.png"

/usr/bin/python3 - <<'PY'
from pathlib import Path
import json, hashlib
out=Path('outputs/c04_ch02')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
source=(out/'source_type.txt').read_text().strip(); url=(out/'source_url.txt').read_text().strip()
stats=json.loads((out/'derived_stats.json').read_text())
files={}
for p in sorted(out.iterdir()):
  if p.is_file(): files[p.name]={'bytes':p.stat().st_size,'sha256':sha(p)}
receipt={
 'project_id':'PRJ-C04-QINGJIANG-SHISHU','chapter':'CH02','run':'REAL DEM MATERIALIZATION / TEMP SP01 RUNTIME ADAPTER',
 'analysis_extent_wgs84':[109.75,30.29,109.81,30.315],
 'analysis_extent_semantics':'CURRENT CH02 ANALYSIS EXTENT / NOT SURVEYED SITE POLYGON',
 'source_type':source,'source_url':url,
 'metric_analysis_crs':'EPSG:32649','target_cell_size_m':[30,30],
 'nodata_policy':'metric warp outside valid rotated footprint = -9999; excluded from all stats and D8 routing',
 'derived':stats,'files':files,
 'truth':'REMOTE SOURCE-GROUNDED / FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS',
 'does_not_prove':['surveyed site boundary','field-measured elevation','observed drainage network','hydraulic capacity','geohazard safety','construction suitability','independent Design PASS']
}
(out/'C04_CH02_REAL_DEM_SOURCE_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
PY

find "$OUT" -maxdepth 1 -type f -printf '%f\t%s bytes\n' | sort > "$OUT/C04_CH02_FILE_LIST.txt"
echo "C04 CH02 real DEM materialization complete: $SOURCE_TYPE"
