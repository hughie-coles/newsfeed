#!/usr/bin/env python3
import json
import urllib.request
import urllib.error

MCP_URL = (
    "https://api.anthropic.com/v2/ccr-sessions/cse_01VTtM7W4TwFFJ9oZWvLhaKK/mcp"
    "?mcp_url=https%3A%2F%2Fgmail.mcp.claude.com%2Fmcp"
    "&mcp_server_id=f0a9f4e6-3f2c-5e43-9026-b0a3dc5ed85f"
    "&toolbox_mcp_server_id=e2f17b0e-febf-4335-ae94-f828550e92e5"
)
TOKEN = open("/home/claude/.claude/remote/.session_ingress_token").read().strip()

with open("/home/user/newsfeed/digest.html") as f:
    html_body = f.read()

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "create_draft",
        "arguments": {
            "to": ["hughie.coles@gmail.com"],
            "subject": "Feed Digest: 2026-05-13",
            "htmlBody": html_body,
        },
    },
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    MCP_URL,
    data=data,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
        "X-MCP-Server-ID": "e2f17b0e-febf-4335-ae94-f828550e92e5",
        "X-Session-UUID": "cse_01VTtM7W4TwFFJ9oZWvLhaKK",
        "anthropic-version": "2023-06-01",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode()
        print("HTTP", resp.status)
        print(body[:2000])
except urllib.error.HTTPError as e:
    print("HTTP Error", e.code)
    print(e.read().decode()[:2000])
