# OpenAI Secure MCP Tunnel route — legacy note

The implemented and verified route is now documented in `OPENAI_SECURE_TUNNEL.md`.

The current workstation has a verified `tunnel-client` v0.0.15 binary at:

`D:\Desgin\.mcp-runtime\openai-tunnel-client\bin\tunnel-client.exe`

Its release archive SHA-256 was checked against the upstream `SHA256SUMS.txt` before extraction.

This binary is runtime infrastructure and is **not vendored into the OLEANDER candidate package**.

## Current implementation

Secure MCP Tunnel uses two OpenAI Platform objects:

- `CONTROL_PLANE_TUNNEL_ID` — a tunnel created/available to the user's Platform organization;
- `CONTROL_PLANE_API_KEY` — a runtime API key whose principal has the required tunnel read/use permissions.

ChatGPT Developer Mode access is a separate workspace permission.

Do not place either secret/key in Git.

The current scripts are:

- `configure_openai_tunnel.ps1` — one-time interactive setup; stores the runtime key with Windows DPAPI and writes the `oleander-baidu-storage` profile.
- `run_openai_tunnel_secure.ps1` — starts/checks the local MCP at `127.0.0.1:9823`, runs tunnel doctor, then keeps `tunnel-client` running.

The verified profile target is `http://127.0.0.1:9823/mcp`.

## ChatGPT connection

In a ChatGPT workspace that supports custom MCP apps and Secure MCP Tunnel, create a developer-mode app and choose the tunnel connection. The ChatGPT app is still a session/storage surface; its availability does not promote this candidate into OLEANDER Current.
