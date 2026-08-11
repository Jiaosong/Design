#!/usr/bin/env bash
set -u
TOOL_ROOT="${OLEANDER_COCOS_TOOL_ROOT:-/opt/oleander/cocos4}"
[[ -f "$TOOL_ROOT/toolchain.env" ]] && source "$TOOL_ROOT/toolchain.env"
fail=0
printf '%-24s %s\n' 'OLEANDER COCOS home' "${OLEANDER_COCOS_HOME:-$TOOL_ROOT}"
printf '%-24s %s\n' 'OS' "$(. /etc/os-release 2>/dev/null; echo ${PRETTY_NAME:-unknown})"
printf '%-24s %s\n' 'Node' "$(node -v 2>/dev/null || echo MISSING)"
printf '%-24s %s\n' 'npm' "$(npm -v 2>/dev/null || echo MISSING)"
printf '%-24s %s\n' 'Git' "$(git --version 2>/dev/null || echo MISSING)"
printf '%-24s %s\n' 'Cocos CLI' "$(command -v cocos 2>/dev/null || echo NOT_INSTALLED)"
printf '%-24s %s\n' 'Engine pin' "${OLEANDER_COCOS_ENGINE_TAG:-UNKNOWN}"
printf '%-24s %s\n' 'CLI pin' "${OLEANDER_COCOS_CLI_SHA:-UNKNOWN}"
if getent hosts github.com >/dev/null 2>&1; then printf '%-24s %s\n' 'Network github.com' 'OK'; else printf '%-24s %s\n' 'Network github.com' 'UNAVAILABLE'; fail=1; fi
if getent hosts registry.npmjs.org >/dev/null 2>&1; then printf '%-24s %s\n' 'Network npm registry' 'OK'; else printf '%-24s %s\n' 'Network npm registry' 'UNAVAILABLE'; fail=1; fi
node_ver="$(node -p 'process.versions.node' 2>/dev/null || echo 0.0.0)"
required="${OLEANDER_COCOS_NODE_VERSION:-22.17.0}"
node -e "const a='$node_ver'.split('.').map(Number),b='$required'.split('.').map(Number);process.exit(a[0]>b[0]||a[0]===b[0]&&(a[1]>b[1]||a[1]===b[1]&&a[2]>=b[2])?0:1)" || { echo "WARN: Node $node_ver < required $required"; fail=1; }
if command -v cocos >/dev/null 2>&1; then cocos --version || fail=1; else fail=1; fi
exit "$fail"
