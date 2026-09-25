# Vercel deployment boundary

`api/index.py` is a thin Vercel ASGI carrier around the same OLEANDER Baidu Storage MCP app.

Public routes on a Vercel deployment are:

- `/api/mcp` — Streamable HTTP MCP;
- `/api/healthz` — deployment/runtime health only;
- `/api/policy` — non-secret storage policy projection.

## Secrets

Never deploy the Baidu access token as source code or a committed deployment file.

The live project requires the server-side environment variable:

`BAIDU_NETDISK_ACCESS_TOKEN`

Optional hardening variable:

`OLEANDER_APP_BEARER_TOKEN`

The second variable is only useful for MCP clients that can send the static bearer header. ChatGPT personal-plugin authentication should instead use a supported private connection/OAuth design; do not paste a bearer token into a chat or plugin package.

## Safe no-token deployment

A deployment without `BAIDU_NETDISK_ACCESS_TOKEN` is intentionally useful for transport testing. It exposes only:

- `oleander_storage_status`;
- `oleander_storage_probe` (returns configuration error until a token exists);
- `oleander_storage_bootstrap` (cannot reach Baidu until a token exists).

No provider file/search/write tools are advertised until the upstream Baidu MCP connection can be authenticated.

Do not add `BAIDU_NETDISK_ACCESS_TOKEN` to a public Vercel deployment until inbound user/client authentication is in place. When Baidu credentials are present, the app itself returns `mcp_auth_required` unless either `OLEANDER_APP_BEARER_TOKEN` is configured or `OLEANDER_TRUST_PRIVATE_TRANSPORT=true` is explicitly set behind a verified private transport.

`DEPLOYMENT READY != BAIDU AUTH != CHATGPT INSTALL != CURRENT PROMOTION`.
