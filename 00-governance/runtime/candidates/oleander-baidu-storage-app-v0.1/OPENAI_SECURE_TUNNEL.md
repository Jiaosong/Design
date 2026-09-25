# OpenAI Secure MCP Tunnel route

This is the preferred remote route for the personal OLEANDER Baidu Storage candidate.

It replaces the temporary public Railway deployment for normal use:

`ChatGPT / supported OpenAI surface -> OpenAI Secure MCP Tunnel -> workstation tunnel-client -> 127.0.0.1:9823/mcp -> OLEANDER Baidu Storage -> Baidu Netdisk`

The workstation must remain online for remote calls. The Baidu access token remains in the current Windows user's DPAPI store and does not need to be copied to a cloud host.

## One-time setup

1. In OpenAI Platform Tunnels settings, create a tunnel associated with the intended personal Platform organization / ChatGPT workspace.
2. Create a runtime API key whose principal has Tunnels Read + Use.
3. Run `configure_openai_tunnel.ps1` and paste the `tunnel_...` ID plus runtime key locally. The key is stored with Windows DPAPI.
4. Run `run_openai_tunnel_secure.ps1`.
5. Only after `tunnel-client doctor` passes and the daemon is ready, select that tunnel when creating/testing the ChatGPT developer-mode app.

## Security boundary

- No inbound router/firewall port is opened.
- The local MCP stays on `127.0.0.1:9823`.
- `OLEANDER_TRUST_PRIVATE_TRANSPORT=true` is used only on the loopback-local MCP process behind the OpenAI tunnel.
- The OpenAI runtime API key and Baidu access token are stored separately with Windows DPAPI.
- The tunnel is transport only. It does not own Project State, Current, Design KEEP or Promotion.

## Availability

When the workstation or `tunnel-client` is offline, remote ChatGPT storage calls are unavailable. OLEANDER must report `LOCAL_GATEWAY_OFFLINE` rather than pretending cloud execution occurred.

