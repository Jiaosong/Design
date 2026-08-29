#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$ROOT/logs/C04_F_EXPORT_REPRODUCIBLE_$(date -u +%Y%m%dT%H%M%SZ).log"
exec > >(tee -a "$LOG") 2>&1

echo "[C04 F] reproducible export start $(date -u +%FT%TZ)"
echo "ROOT=$ROOT"

PYTHON="${PYTHON:-$(command -v python)}"
FFMPEG="${FFMPEG:-$(command -v ffmpeg)}"
CHROMIUM="${CHROMIUM:-$(command -v chromium || true)}"

# 1) Primary raster/PDF/HTML export: pure Python + Pillow + ReportLab.
"$PYTHON" "$ROOT/work/generate_f_delivery.py"

# 2) Preserve/use accepted F narration/audio master. No paid dependency.
AUDIO="$ROOT/video/C04_F_FILM_86s_audio_master.m4a"
ACCEPTED="$ROOT/video/C04_F_FILM_86s_v0.2.mp4"
if [[ ! -s "$AUDIO" && -s "$ACCEPTED" ]]; then
  "$FFMPEG" -y -v error -i "$ACCEPTED" -vn -c:a copy "$AUDIO"
fi

# 3) Reproducible 86 s delivery export.
# Default = stream-copy repackage of the already accepted F v0.2 master (fast, no quality loss).
# Optional full layer rebuild = D v1.1 motion + F ASS + accepted F audio master.
D_BASE="$ROOT/inputs/d_v11/QJD_v1.1_PUBLIC_DISPLAY/02_VIDEO/QJD_V11_PUBLIC_MOTION_86s_1920x1080.mp4"
ASS="$ROOT/video/C04_F_FILM_86s_v0.1.ass"
OUT="$ROOT/video/C04_F_FILM_86s_REPRO.mp4"
if [[ "${C04_REENCODE_VIDEO:-0}" == "1" ]]; then
  if [[ -s "$AUDIO" ]]; then
    "$FFMPEG" -y -v warning \
      -i "$D_BASE" -i "$AUDIO" \
      -vf "ass=$ASS:fontsdir=/usr/share/fonts/opentype/noto" \
      -map 0:v:0 -map 1:a:0 \
      -c:v libx264 -preset ultrafast -crf 20 -profile:v high -level:v 4.1 \
      -pix_fmt yuv420p -r 24 -c:a copy -t 86 -movflags +faststart "$OUT"
  else
    echo "[DEGRADED] audio master missing; producing explicit silent technical fallback, not submission master"
    OUT="$ROOT/video/C04_F_FILM_86s_REPRO_SILENT_FALLBACK.mp4"
    "$FFMPEG" -y -v warning \
      -i "$D_BASE" -f lavfi -i anullsrc=r=48000:cl=mono \
      -vf "ass=$ASS:fontsdir=/usr/share/fonts/opentype/noto" \
      -map 0:v:0 -map 1:a:0 -shortest \
      -c:v libx264 -preset ultrafast -crf 20 -profile:v high -level:v 4.1 \
      -pix_fmt yuv420p -r 24 -c:a aac -b:a 128k -t 86 -movflags +faststart "$OUT"
  fi
else
  echo "[VIDEO] fast reproducible delivery = accepted F v0.2 stream-copy remux"
  "$FFMPEG" -y -v error -i "$ACCEPTED" -map 0 -c copy -movflags +faststart "$OUT"
fi

# 4) HTML/CSS paged-media fallback.
# Chromium binary exists but current headless print smoke times out in this container;
# WeasyPrint is the tested, non-blocking fallback. Chromium can be diagnostically retried only when explicitly requested.
WEASYPRINT="${WEASYPRINT:-$(command -v weasyprint || true)}"
if [[ -n "$WEASYPRINT" ]]; then
  "$WEASYPRINT" "$ROOT/web/print_20screen.html" "$ROOT/qc/repro_20260815/C04_F_20screen_WEASYPRINT_FALLBACK.pdf"
  "$WEASYPRINT" "$ROOT/boards/print_a1_fallback.html" "$ROOT/qc/repro_20260815/C04_F_A1_WEASYPRINT_FALLBACK.pdf"
else
  echo "[FALLBACK] WeasyPrint unavailable; primary ReportLab PDFs remain the export path."
fi
if [[ "${C04_TRY_CHROMIUM:-0}" == "1" && -n "$CHROMIUM" ]]; then
  timeout 15s "$CHROMIUM" --headless --no-sandbox --disable-gpu --disable-dev-shm-usage --allow-file-access-from-files \
    --print-to-pdf="$ROOT/qc/repro_20260815/C04_F_20screen_CHROMIUM_DIAGNOSTIC.pdf" \
    --no-pdf-header-footer "file://$ROOT/web/print_20screen.html" || echo "[EXPECTED CURRENT LIMIT] Chromium diagnostic print did not complete."
fi

sha256sum \
  "$ROOT/boards/C04_F_A1_BOARDS_v0.1.pdf" \
  "$ROOT/C04_F_Landscape_Atlas_20screen_v0.1.pdf" \
  "$OUT" \
  "$AUDIO" | tee "$ROOT/logs/C04_F_EXPORT_SHA256_LATEST.txt"

echo "[C04 F] reproducible export complete $(date -u +%FT%TZ)"
echo "LOG=$LOG"
