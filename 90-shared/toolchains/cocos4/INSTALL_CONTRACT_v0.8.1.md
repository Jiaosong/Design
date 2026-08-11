# OLEANDER COCOS 4 Install Contract v0.8.2

## Purpose

This contract makes the COCOS 4 + COCOS CLI runtime a repo-wide OLEANDER dependency rather than a C04-local install.

## Authority

- Stable OLEANDER entry point: `oleander-cocos`.
- Upstream CLI source is pinned by commit.
- Upstream engine is managed by the pinned CLI `npm run init` flow and MUST resolve to the pinned COCOS 4 engine commit.
- Projects keep only source/data/art/audio/config; they do not vendor private engine forks.
- The command surface is defined by the **actual source at the pinned CLI commit**, not by drifting upstream documentation.

## Required environment

- Node.js `>=22.17.0`.
- Git.
- npm.
- Network access to GitHub and the npm registry during bootstrap.

## Optional authenticated GitHub fetch

Set `GITHUB_TOKEN` when anonymous GitHub clone/submodule traffic is rate-limited. The bootstrap passes the credential through process-local Git configuration and does not write the token into repository files.

## Install locations

Defaults:

- runtime home: `/opt/oleander/cocos4`
- gateway bin: `/usr/local/bin`

Both are overridable:

```bash
OLEANDER_COCOS_HOME="$HOME/.local/share/oleander/cocos4" \
OLEANDER_COCOS_BIN_DIR="$HOME/.local/bin" \
./90-shared/toolchains/cocos4/bootstrap-linux.sh
```

This allows non-root CI and workstation installs.

## Pinned command boundary

At `OLEANDER_COCOS_CLI_SHA=6f810d60d89f100b5a5d6f1b0cd3518b67b15e5c`, the CLI registers `create`, `build`, `start-mcp-server`, `make`, `run`, `upload` and `preview`. It does not register standalone `import` or `info` commands. OLEANDER therefore MUST NOT expose or require synthetic `import` / `info` gates for this pin.

## Verification gates

Bootstrap is successful only if all of these pass:

1. CLI checkout equals `OLEANDER_COCOS_CLI_SHA`.
2. CLI-managed `packages/engine` checkout equals `OLEANDER_COCOS_ENGINE_SHA`.
3. `dist/cli.js` exists.
4. `oleander-cocos doctor` passes.
5. For a promoted project, official `create --project ... --type 2d` must succeed against a non-existing destination.
6. The materializer must verify the generated project metadata and required governed source overlay.
7. The target `build` must execute and pass for the declared platform.

Do not label a source pack or wrapper-only install as `TOOLCHAIN_INSTALLED`. Do not label a materialized source overlay as `WEB_BUILD_SMOKE_PASS` until the target build has actually completed successfully.
