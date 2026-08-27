#!/usr/bin/env bash
set -euo pipefail
runtime_home="${OLEANDER_PRO_RUNTIME_HOME:-/mnt/data/runtime/oleander-pro-design}"
if [[ -n "${OLEANDER_PRO_PYTHON:-}" && -x "${OLEANDER_PRO_PYTHON}" ]]; then
  py="${OLEANDER_PRO_PYTHON}"
elif [[ -x "$runtime_home/venv/bin/python" ]]; then
  py="$runtime_home/venv/bin/python"
else
  echo "OLEANDER professional Python runtime not materialized." >&2
  echo "Run tools/oleander-runtime/pro-design/materialize.sh on an execution surface with network access." >&2
  exit 127
fi
exec "$py" "$@"
