#!/usr/bin/env bash
set -euo pipefail

MAGICK_BIN="${OLEANDER_MAGICK_BIN:-$(command -v magick || true)}"
ICC="${1:-/usr/share/color/icc/ghostscript/srgb.icc}"
OUT="${2:-./icc-profile-smoke}"

if [[ -z "$MAGICK_BIN" || ! -x "$MAGICK_BIN" ]]; then
  echo 'RESULT=HOLD REASON=IMAGEMAGICK_NOT_AVAILABLE'
  exit 78
fi
if [[ ! -f "$ICC" ]]; then
  echo 'RESULT=HOLD REASON=ICC_PROFILE_NOT_AVAILABLE'
  exit 78
fi

VERSION="$($MAGICK_BIN -version)"
if ! grep -qiE 'Delegates.*\blcms\b' <<<"$VERSION"; then
  echo 'RESULT=HOLD REASON=LCMS_DELEGATE_NOT_AVAILABLE'
  echo "$VERSION" | grep '^Delegates' || true
  exit 78
fi

mkdir -p "$OUT"
$MAGICK_BIN -size 320x180 gradient:'#202020-#e8e8e8' -profile "$ICC" "$OUT/source.png"
$MAGICK_BIN "$OUT/source.png" -resize 160x90 "$OUT/roundtrip.png"
$MAGICK_BIN "$OUT/source.png" "$OUT/source.icc"
$MAGICK_BIN "$OUT/roundtrip.png" "$OUT/roundtrip.icc"

SRC_HASH=$(sha256sum "$OUT/source.icc" | awk '{print $1}')
RT_HASH=$(sha256sum "$OUT/roundtrip.icc" | awk '{print $1}')
SRC_PROFILES=$($MAGICK_BIN identify -format '%[profiles]' "$OUT/source.png")
RT_PROFILES=$($MAGICK_BIN identify -format '%[profiles]' "$OUT/roundtrip.png")
RT_DIMS=$($MAGICK_BIN identify -format '%wx%h' "$OUT/roundtrip.png")

if [[ "$SRC_PROFILES" == *icc* && "$RT_PROFILES" == *icc* && "$SRC_HASH" == "$RT_HASH" && "$RT_DIMS" == '160x90' ]]; then
  echo "RESULT=PASS PROFILE_HASH=$RT_HASH DIMS=$RT_DIMS"
  exit 0
fi

echo "RESULT=REVISE SRC_PROFILES=$SRC_PROFILES RT_PROFILES=$RT_PROFILES SRC_HASH=$SRC_HASH RT_HASH=$RT_HASH DIMS=$RT_DIMS"
exit 1
