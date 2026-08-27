#!/usr/bin/env bash
set -euo pipefail
if [[ -n "${OLEANDER_FFMPEG_BIN:-}" && -x "${OLEANDER_FFMPEG_BIN}" ]]; then
  ffmpeg_bin="${OLEANDER_FFMPEG_BIN}"
elif command -v ffmpeg >/dev/null 2>&1; then
  ffmpeg_bin="$(command -v ffmpeg)"
else
  echo "OLEANDER motion runtime not found: FFmpeg is required for this wrapper." >&2
  exit 127
fi
exec "$ffmpeg_bin" "$@"
