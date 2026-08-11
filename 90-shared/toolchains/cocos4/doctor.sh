#!/usr/bin/env bash
set -u

TOOL_ROOT="${OLEANDER_COCOS_HOME:-${OLEANDER_COCOS_TOOL_ROOT:-/opt/oleander/cocos4}}"
[[ -f "$TOOL_ROOT/toolchain.env" ]] && source "$TOOL_ROOT/toolchain.env"
TOOL_ROOT="${OLEANDER_COCOS_HOME:-$TOOL_ROOT}"
CLI_DIR="$TOOL_ROOT/cli"
ENGINE_DIR="$CLI_DIR/packages/engine"
EXTERNAL_DIR="$ENGINE_DIR/native/external"
fail=0

printf '%-28s %s\n' 'OLEANDER COCOS home' "$TOOL_ROOT"
printf '%-28s %s\n' 'OS' "$(. /etc/os-release 2>/dev/null; echo ${PRETTY_NAME:-unknown})"
printf '%-28s %s\n' 'Node' "$(node -v 2>/dev/null || echo MISSING)"
printf '%-28s %s\n' 'npm' "$(npm -v 2>/dev/null || echo MISSING)"
printf '%-28s %s\n' 'Git' "$(git --version 2>/dev/null || echo MISSING)"
printf '%-28s %s\n' 'Engine label' "${OLEANDER_COCOS_ENGINE_TAG:-UNKNOWN}"
printf '%-28s %s\n' 'Engine pin' "${OLEANDER_COCOS_ENGINE_SHA:-UNKNOWN}"
printf '%-28s %s\n' 'External label' "${OLEANDER_COCOS_EXTERNAL_TAG:-UNKNOWN}"
printf '%-28s %s\n' 'External pin' "${OLEANDER_COCOS_EXTERNAL_SHA:-UNKNOWN}"
printf '%-28s %s\n' 'CLI pin' "${OLEANDER_COCOS_CLI_SHA:-UNKNOWN}"

node_ver="$(node -p 'process.versions.node' 2>/dev/null || echo 0.0.0)"
required="${OLEANDER_COCOS_NODE_VERSION:-22.17.0}"
node -e "const a='$node_ver'.split('.').map(Number),b='$required'.split('.').map(Number);process.exit(a[0]>b[0]||a[0]===b[0]&&(a[1]>b[1]||a[1]===b[1]&&a[2]>=b[2])?0:1)" || { echo "FAIL: Node $node_ver < required $required"; fail=1; }

if [[ -d "$CLI_DIR/.git" ]]; then
  cli_sha="$(git -C "$CLI_DIR" rev-parse HEAD 2>/dev/null || echo ERROR)"
  printf '%-28s %s\n' 'CLI checkout' "$cli_sha"
  [[ "$cli_sha" == "${OLEANDER_COCOS_CLI_SHA:-}" ]] || fail=1
else
  printf '%-28s %s\n' 'CLI checkout' 'NOT_INSTALLED'
  fail=1
fi

if [[ -d "$ENGINE_DIR/.git" ]]; then
  engine_sha="$(git -C "$ENGINE_DIR" rev-parse HEAD 2>/dev/null || echo ERROR)"
  printf '%-28s %s\n' 'Pinned engine checkout' "$engine_sha"
  [[ "$engine_sha" == "${OLEANDER_COCOS_ENGINE_SHA:-}" ]] || fail=1
else
  printf '%-28s %s\n' 'Pinned engine checkout' 'NOT_INSTALLED'
  fail=1
fi

if [[ -d "$EXTERNAL_DIR/.git" ]]; then
  external_sha="$(git -C "$EXTERNAL_DIR" rev-parse HEAD 2>/dev/null || echo ERROR)"
  printf '%-28s %s\n' 'Pinned external checkout' "$external_sha"
  [[ "$external_sha" == "${OLEANDER_COCOS_EXTERNAL_SHA:-}" ]] || fail=1
else
  printf '%-28s %s\n' 'Pinned external checkout' 'NOT_INSTALLED'
  fail=1
fi

if [[ -f "$CLI_DIR/dist/cli.js" ]]; then
  cli_version="$(node "$CLI_DIR/dist/cli.js" --version 2>/dev/null || echo ERROR)"
  printf '%-28s %s\n' 'COCOS CLI runtime' "$cli_version"
  [[ "$cli_version" != "ERROR" ]] || fail=1
else
  printf '%-28s %s\n' 'COCOS CLI runtime' 'NOT_BUILT'
  fail=1
fi

if getent hosts github.com >/dev/null 2>&1; then printf '%-28s %s\n' 'Network github.com' 'OK'; else printf '%-28s %s\n' 'Network github.com' 'UNAVAILABLE'; fi
if getent hosts registry.npmjs.org >/dev/null 2>&1; then printf '%-28s %s\n' 'Network npm registry' 'OK'; else printf '%-28s %s\n' 'Network npm registry' 'UNAVAILABLE'; fi

exit "$fail"
