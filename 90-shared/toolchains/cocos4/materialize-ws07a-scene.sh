#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="${1:?materialized COCOS project path required}"
PORT="${OLEANDER_COCOS_MCP_PORT:-9527}"
LOG="${RUNNER_TEMP:-${TMPDIR:-/tmp}}/oleander-c04-ws07a-mcp.log"

command -v oleander-cocos >/dev/null 2>&1 || { echo "ERROR: oleander-cocos gateway missing" >&2; exit 69; }
[[ -f "$PROJECT/package.json" ]] || { echo "ERROR: materialized COCOS project missing: $PROJECT" >&2; exit 66; }

: > "$LOG"
oleander-cocos mcp "$PROJECT" "$PORT" >"$LOG" 2>&1 &
MCP_PID=$!
cleanup() {
  if kill -0 "$MCP_PID" >/dev/null 2>&1; then
    kill "$MCP_PID" >/dev/null 2>&1 || true
    sleep 1
    kill -9 "$MCP_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

for _ in $(seq 1 120); do
  if ! kill -0 "$MCP_PID" >/dev/null 2>&1; then
    cat "$LOG" >&2
    echo "ERROR: COCOS MCP server exited before materialization" >&2
    exit 70
  fi
  if grep -Eq 'MCP Server started|Server listening|Server is running on:' "$LOG"; then
    break
  fi
  sleep 1
done

if ! grep -Eq 'MCP Server started|Server listening|Server is running on:' "$LOG"; then
  cat "$LOG" >&2
  echo "ERROR: timed out waiting for COCOS MCP server" >&2
  exit 70
fi

if ! node "$SCRIPT_DIR/materialize-ws07a-scene.mjs" "$PROJECT" "$PORT"; then
  cat "$LOG" >&2
  exit 65
fi

[[ -f "$PROJECT/assets/scenes/VisualPrototype.scene" ]] || { cat "$LOG" >&2; echo "ERROR: VisualPrototype.scene was not persisted" >&2; exit 65; }
[[ -f "$PROJECT/temp/oleander-ws07a-scene-proof.json" ]] || { echo "ERROR: scene proof missing" >&2; exit 65; }
cat "$PROJECT/temp/oleander-ws07a-scene-proof.json"
