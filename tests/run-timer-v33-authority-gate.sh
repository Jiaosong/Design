#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 /path/to/OLEANDER_Zhizuo_TimerLightBasin_v3.3_AUDITED_2026-08-10.zip" >&2
  exit 64
fi

ZIP_PATH=$1
MANIFEST=${TIMER_V33_MANIFEST:-website/practice/timer-light-basin-v3/DEPLOYMENT_ARTIFACT_MANIFEST_v3.3.json}
QA_DIR=${TIMER_V33_QA_OUT:-test-results/timer-v33-authority}
STAGE_DIR=${TIMER_V33_STAGE_DIR:-test-results/timer-v33-authority-stage}
VERIFY_ONLY=${TIMER_V33_VERIFY_ONLY:-false}
BASE_URL=${TIMER_V33_BASE_URL:-http://127.0.0.1:4173/index.html}

mkdir -p "$QA_DIR" "$STAGE_DIR"

python3 tests/timer-v33-stage-package.py \
  --zip "$ZIP_PATH" \
  --manifest "$MANIFEST" \
  --dest "$STAGE_DIR/site" \
  --result "$QA_DIR/package-verification.json"

cp "$MANIFEST" "$QA_DIR/deployment-artifact-manifest.json"

if [[ "$VERIFY_ONLY" == "true" ]]; then
  printf '%s\n' 'Timer v3.3 authority package verification: PASS (browser skipped by explicit VERIFY_ONLY)'
  exit 0
fi

server_pid=''
cleanup() {
  if [[ -n "$server_pid" ]]; then
    kill "$server_pid" 2>/dev/null || true
    wait "$server_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT

STATIC_ROOT="$STAGE_DIR/site" node tests/serve-static-root.mjs > "$QA_DIR/server.log" 2>&1 &
server_pid=$!

for _ in {1..45}; do
  if curl -fsS "$BASE_URL" >/dev/null; then
    break
  fi
  sleep 1
done

if ! curl -fsS "$BASE_URL" >/dev/null; then
  cat "$QA_DIR/server.log" >&2 || true
  echo "Timer v3.3 staged authority server did not become ready: $BASE_URL" >&2
  exit 65
fi

TIMER_V33_BASE_URL="$BASE_URL" \
TIMER_V33_QA_OUT="$QA_DIR" \
node tests/timer-v33-integrated.mjs
