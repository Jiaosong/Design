#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
runtime_home="${OLEANDER_PRO_RUNTIME_HOME:-/mnt/data/runtime/oleander-pro-design}"
python_bin="${OLEANDER_PRO_PYTHON:-python3}"
requirements="$repo_root/90-shared/toolchains/pro-design/requirements.lock.txt"
venv="$runtime_home/venv"

mkdir -p "$runtime_home"

if [[ ! -x "$venv/bin/python" ]]; then
  "$python_bin" -m venv "$venv"
fi

"$venv/bin/python" -m pip install --upgrade pip
"$venv/bin/pip" install --no-cache-dir -r "$requirements"

if [[ "${OLEANDER_PRO_MATERIALIZE_FREECAD:-0}" == "1" ]]; then
  freecad_dir="$runtime_home/freecad-1.1.3"
  freecad_app="$freecad_dir/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"
  mkdir -p "$freecad_dir"
  if [[ ! -f "$freecad_app" ]]; then
    curl -L --fail --retry 3 \
      "https://github.com/FreeCAD/FreeCAD/releases/download/1.1.3/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage" \
      -o "$freecad_app"
  fi
  echo "3a853eb69ee595f779f2255dbf80a765926981d8ff68903cefee4dfb03a8f5ef  $freecad_app" | sha256sum -c -
  chmod +x "$freecad_app"
fi

printf 'OLEANDER_PRO_RUNTIME_HOME=%s\n' "$runtime_home"
printf 'OLEANDER_PRO_PYTHON=%s\n' "$venv/bin/python"
