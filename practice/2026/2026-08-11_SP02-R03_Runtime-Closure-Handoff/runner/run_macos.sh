#!/bin/bash
set -euo pipefail
GH_FILE="${1:?Usage: run_macos.sh /path/to/definition.gh[x] [evidence_dir]}"
EVIDENCE_DIR="${2:-$(cd "$(dirname "$0")/.." && pwd)/runtime_evidence}"
RHINO="/Applications/Rhino 8.app"
CAPTURE="$(cd "$(dirname "$0")/../rhino" && pwd)/SP02_R03_capture_runtime.py"

mkdir -p "$EVIDENCE_DIR"
if [ ! -d "$RHINO" ]; then
  printf '{"runtime_state":"HOST_BLOCKED","reason":"RHINO_8_NOT_FOUND","rhino_path":"%s"}\n' "$RHINO" > "$EVIDENCE_DIR/HOST_PREFLIGHT.json"
  exit 2
fi
if [ ! -f "$GH_FILE" ]; then
  echo "Grasshopper definition not found: $GH_FILE" >&2
  exit 2
fi

export SP02_GH_FILE="$(cd "$(dirname "$GH_FILE")" && pwd)/$(basename "$GH_FILE")"
export SP02_EVIDENCE_DIR="$(cd "$EVIDENCE_DIR" && pwd)"
export SP02_EXIT_AFTER_CAPTURE=1
open -W "$RHINO" --args -nosplash -notemplate -runscript "-_RunPythonScript ($CAPTURE)"
python3 "$(cd "$(dirname "$0")/../validator" && pwd)/validate_runtime_evidence.py" "$SP02_EVIDENCE_DIR"
