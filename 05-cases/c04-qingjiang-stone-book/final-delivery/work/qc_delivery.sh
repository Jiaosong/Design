#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
QC="$ROOT/qc/repro_20260815"
rm -rf "$QC/render_a1" "$QC/render_20screen" "$QC/render_weasy_a1" "$QC/render_weasy_20screen"
mkdir -p "$QC/render_a1" "$QC/render_20screen" "$QC/render_weasy_a1" "$QC/render_weasy_20screen"
LOG="$ROOT/logs/C04_F_QC_REPRO_$(date -u +%Y%m%dT%H%M%SZ).log"
exec > >(tee -a "$LOG") 2>&1

PDF_RENDER="/home/oai/skills/pdfs/scripts/render_pdf.py"
PYTHON="${PYTHON:-$(command -v python)}"
FFMPEG="${FFMPEG:-$(command -v ffmpeg)}"
FFPROBE="${FFPROBE:-$(command -v ffprobe)}"
GS="${GS:-$(command -v gs)}"
PDFINFO="${PDFINFO:-$(command -v pdfinfo)}"

echo "[QC] start $(date -u +%FT%TZ)"
A1="$ROOT/boards/C04_F_A1_BOARDS_v0.1.pdf"
P20="$ROOT/C04_F_Landscape_Atlas_20screen_v0.1.pdf"
VID="$ROOT/video/C04_F_FILM_86s_REPRO.mp4"
[[ -s "$VID" ]] || VID="$ROOT/video/C04_F_FILM_86s_v0.2.mp4"

"$PDFINFO" "$A1" | tee "$QC/A1_pdfinfo.txt"
"$PDFINFO" "$P20" | tee "$QC/P20_pdfinfo.txt"
"$GS" -q -dNOPAUSE -dBATCH -sDEVICE=nullpage "$A1" 2>"$QC/A1_gs_errors.txt"
"$GS" -q -dNOPAUSE -dBATCH -sDEVICE=nullpage "$P20" 2>"$QC/P20_gs_errors.txt"
"$PYTHON" "$PDF_RENDER" "$A1" --out_dir "$QC/render_a1" --dpi 48
"$PYTHON" "$PDF_RENDER" "$P20" --out_dir "$QC/render_20screen" --dpi 36

for f in "C04_F_A1_WEASYPRINT_FALLBACK.pdf" "C04_F_20screen_WEASYPRINT_FALLBACK.pdf"; do
  if [[ -s "$QC/$f" ]]; then
    "$PDFINFO" "$QC/$f" > "$QC/${f%.pdf}_pdfinfo.txt"
    "$GS" -q -dNOPAUSE -dBATCH -sDEVICE=nullpage "$QC/$f" 2> "$QC/${f%.pdf}_gs_errors.txt"
  fi
done
if [[ -s "$QC/C04_F_A1_WEASYPRINT_FALLBACK.pdf" ]]; then
  pdftoppm -png -r 36 -f 1 -singlefile "$QC/C04_F_A1_WEASYPRINT_FALLBACK.pdf" "$QC/weasy_a1_first" >/dev/null 2>&1
  pdftoppm -png -r 36 -f 3 -singlefile "$QC/C04_F_A1_WEASYPRINT_FALLBACK.pdf" "$QC/weasy_a1_last" >/dev/null 2>&1
fi
if [[ -s "$QC/C04_F_20screen_WEASYPRINT_FALLBACK.pdf" ]]; then
  pdftoppm -png -r 36 -f 1 -singlefile "$QC/C04_F_20screen_WEASYPRINT_FALLBACK.pdf" "$QC/weasy20_first" >/dev/null 2>&1
  pdftoppm -png -r 36 -f 20 -singlefile "$QC/C04_F_20screen_WEASYPRINT_FALLBACK.pdf" "$QC/weasy20_last" >/dev/null 2>&1
fi

"$FFPROBE" -v error -show_entries format=duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,sample_rate,channels -of json "$VID" | tee "$QC/C04_F_FILM_86s_REPRO_probe.json"
: > "$QC/C04_F_FILM_86s_REPRO_decode_errors.txt"
"$FFMPEG" -v error -i "$VID" -f null - 2> "$QC/C04_F_FILM_86s_REPRO_decode_errors.txt"

"$PYTHON" - "$ROOT" "$QC" "$VID" <<'PY'
from pathlib import Path
from PIL import Image, ImageStat
import json, subprocess, sys, hashlib
root=Path(sys.argv[1]); qc=Path(sys.argv[2]); vid=Path(sys.argv[3])
results={"schema":"oleander.c04.f-qc/1.0","status":"PASS","checks":{},"does_not_prove":[
 "PDF/video technical integrity does not prove field truth, spatial accuracy, safety, compliance, accessibility, structural adequacy, or implementation readiness.",
 "Browser/renderer parity does not promote any upstream source or replace design/field review."
]}
def check(name, cond, detail):
    results["checks"][name]={"pass":bool(cond),"detail":detail}
    if not cond: results["status"]="FAIL"
for label,file,expected in [("a1",root/'boards/C04_F_A1_BOARDS_v0.1.pdf',3),("p20",root/'C04_F_Landscape_Atlas_20screen_v0.1.pdf',20)]:
    text=subprocess.check_output(['pdfinfo',str(file)],text=True,errors='replace')
    pages=int(next(x.split(':',1)[1].strip() for x in text.splitlines() if x.startswith('Pages:')))
    check(f'{label}_page_count',pages==expected,f'{pages} pages / expected {expected}')
for label,folder,expected in [('a1',qc/'render_a1',3),('p20',qc/'render_20screen',20)]:
    imgs=sorted(folder.glob('*.png'))
    check(f'{label}_render_count',len(imgs)==expected,f'{len(imgs)} rendered pages')
    vars=[]; dims=[]
    for p in imgs:
        im=Image.open(p).convert('L'); st=ImageStat.Stat(im); vars.append(st.var[0]); dims.append(im.size)
    check(f'{label}_nonblank',bool(vars) and min(vars)>20,f'min variance={min(vars) if vars else None:.2f}')
    results['checks'][f'{label}_render_dimensions']={"pass":True,"detail":sorted(set(map(str,dims)))}
for tag in ['A1','P20']:
    p=qc/f'{tag}_gs_errors.txt'; txt=p.read_text(errors='replace') if p.exists() else 'missing'
    check(f'{tag.lower()}_ghostscript_zero_error',txt.strip()=='',f'{len(txt.strip())} stderr chars')
dec=(qc/'C04_F_FILM_86s_REPRO_decode_errors.txt').read_text(errors='replace')
check('video_full_decode_zero_error',dec.strip()=='',f'{len(dec.strip())} stderr chars')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels','-of','json',str(vid)],text=True))
dur=float(probe['format']['duration']); streams=probe['streams']; v=next(s for s in streams if s['codec_type']=='video'); a=next((s for s in streams if s['codec_type']=='audio'),None)
check('video_duration',abs(dur-86.0)<0.05,f'{dur:.3f}s')
check('video_resolution',v.get('width')==1920 and v.get('height')==1080,f"{v.get('width')}x{v.get('height')}")
check('video_fps',v.get('r_frame_rate')=='24/1',v.get('r_frame_rate'))
check('video_codec',v.get('codec_name')=='h264',v.get('codec_name'))
check('audio_present_aac',a is not None and a.get('codec_name')=='aac',a.get('codec_name') if a else 'NONE')
for p in [root/'boards/C04_F_A1_BOARDS_v0.1.pdf',root/'C04_F_Landscape_Atlas_20screen_v0.1.pdf',vid,root/'video/C04_F_FILM_86s_audio_master.m4a']:
    results.setdefault('sha256',{})[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
(qc/'C04_F_QC_RESULT.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
if results['status']!='PASS': sys.exit(2)
PY

sha256sum "$A1" "$P20" "$VID" "$ROOT/video/C04_F_FILM_86s_audio_master.m4a" | tee "$QC/SHA256_AFTER.txt"
echo "[QC] complete $(date -u +%FT%TZ)"
echo "LOG=$LOG"
