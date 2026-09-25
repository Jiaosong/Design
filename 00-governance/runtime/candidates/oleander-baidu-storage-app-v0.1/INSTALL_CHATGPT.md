# Install / test in ChatGPT

This candidate is an MCP-powered ChatGPT app server. ChatGPT connects to a **remote Streamable HTTP MCP endpoint**, not directly to this local Python process.

## 1. Configure Baidu access

Obtain a Baidu Netdisk Open Platform access token using the current official Baidu Netdisk MCP instructions.

On this Windows workstation the candidate includes `configure_baidu_token.ps1`, which opens the current official personal-test authorization URL and stores the pasted token using Windows DPAPI under the current user. This avoids pasting the token into ChatGPT or committing it to Git. The Baidu repository explicitly describes the personal-user credential as limited-time testing, so re-authorize if that official test client changes.

Set it only as server-side secret material:

```text
BAIDU_NETDISK_ACCESS_TOKEN=<token>
```

Do not place the token in Git, plugin ZIP files, chat messages, screenshots or the HOME index.

## 2. Test locally

```powershell
$env:BAIDU_NETDISK_ACCESS_TOKEN="..."
$env:PORT="9817"
py -3.13 -m app.server
```

Endpoint:

`http://127.0.0.1:9817/mcp`

Before any external exposure, run the test suite and validator.

## 3. Expose securely

Preferred for workstation testing: use OpenAI Secure MCP Tunnel or another authenticated/private transport supported by your deployment environment.

Do **not** expose this server as an unauthenticated public endpoint because the server holds a Baidu access token capable of acting on the user's storage account.

The server now fails closed when Baidu credentials are configured but neither an app bearer token nor an explicitly trusted private transport is active. `OLEANDER_TRUST_PRIVATE_TRANSPORT=true` must be used only behind a verified authenticated/private transport such as a working Secure MCP Tunnel or an equivalent private gateway. It is not a shortcut for a public deployment.

For a durable deployment, run the Docker image behind an authenticated reverse proxy / private gateway and inject the Baidu token through a secret store. The candidate also supports an optional `OLEANDER_APP_BEARER_TOKEN` guard for generic MCP clients that can send a static Authorization header; this is not a substitute for a proper OAuth/private-tunnel deployment when ChatGPT cannot supply that header.

## 4. ChatGPT app connection

When the account/workspace supports custom MCP apps:

1. enable Developer Mode;
2. create a custom app/connector;
3. provide the remote `https://.../mcp` endpoint;
4. inspect the tool list before enabling write tools;
5. test `oleander_storage_status`, then read/list/search, then bounded folder creation;
6. enable destructive capabilities only after policy review.

The app should appear conceptually as `OLEANDER 百度网盘`.

## 5. Plan boundary

ChatGPT account/workspace support for custom MCP read/write actions is a product capability outside this repository. A valid server package does not prove that the current account can install every write action.

If full write MCP is unavailable on the current account, keep this candidate deployable and use the same Baidu storage policy from COS/local tooling until the account/workspace supports the required connector mode.
