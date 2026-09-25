# OpenAI Secure MCP Tunnel route

For a private workstation-hosted app, prefer OpenAI Secure MCP Tunnel instead of a public ad-hoc tunnel.

The current workstation has a verified `tunnel-client` v0.0.15 binary at:

`D:\Desgin\.mcp-runtime\openai-tunnel-client\bin\tunnel-client.exe`

Its release archive SHA-256 was checked against the upstream `SHA256SUMS.txt` before extraction.

This binary is runtime infrastructure and is **not vendored into the OLEANDER candidate package**.

## Required external inputs

Secure MCP Tunnel requires two OpenAI Platform objects that this repository cannot truthfully invent:

- `CONTROL_PLANE_TUNNEL_ID` — a tunnel created/available to the user's Platform organization;
- `CONTROL_PLANE_API_KEY` — a runtime API key whose principal has the required tunnel read/use permissions.

ChatGPT Developer Mode access is a separate workspace permission.

Do not place either secret/key in Git.

## Prepare a profile

Start the OLEANDER Baidu MCP app locally on port 8000, then:

```powershell
$env:CONTROL_PLANE_TUNNEL_ID="tunnel_..."
.\setup_openai_tunnel.ps1
```

The generated profile points to:

`http://127.0.0.1:8000/mcp`

Before running the tunnel:

```powershell
$env:CONTROL_PLANE_API_KEY="<runtime key>"
& 'D:\Desgin\.mcp-runtime\openai-tunnel-client\bin\tunnel-client.exe' doctor --profile oleander-baidu --explain
& 'D:\Desgin\.mcp-runtime\openai-tunnel-client\bin\tunnel-client.exe' run --profile oleander-baidu
```

Only report the tunnel usable after `doctor` and runtime readiness pass.

## ChatGPT connection

In a ChatGPT workspace that supports custom MCP apps and Secure MCP Tunnel, create a developer-mode app and choose the tunnel connection. The ChatGPT app is still a session/storage surface; its availability does not promote this candidate into OLEANDER Current.
