---
id: errors
title: Error Codes
sidebar_label: Errors
sidebar_position: 4
---

# Error Codes

ARC Protocol error codes and handling.

## Standard RPC Errors

Borrowed from JSON-RPC convention:

| Code | Message | Description |
|------|---------|-------------|
| -32600 | Invalid Request | Malformed request |
| -32601 | Method not found | Unknown method |
| -32602 | Invalid params | Invalid parameters |
| -32603 | Internal error | Server error |

## ARC-Specific Errors

| Code | Message | Description |
|------|---------|-------------|
| -42001 | Agent not found | Target agent unavailable |
| -42002 | Authentication failed | Invalid credentials |
| -42003 | Task not found | Task ID not found |
| -42004 | Task processing error | Task execution failed |
| -42005 | Chat not found | Chat ID not found |
| -42006 | Invalid agent state | Agent in invalid state |
| -42007 | Rate limit exceeded | Too many requests |
| -42008 | Insufficient scope | Missing required OAuth scope |

## Error Response

```json
{
  "error": {
    "code": -42001,
    "message": "Agent not found",
    "data": {
      "targetAgent": "nonexistent-agent",
      "availableAgents": ["agent-1", "agent-2"]
    }
  }
}
```

## Error Handling

### Client-Side

```python
from arc import Client
from arc.exceptions import ARCException

client = Client("https://api.example.com/arc")

try:
    response = await client.chat.start(...)
except ARCException as e:
    if e.code == -42001:
        print("Agent not found")
    elif e.code == -42002:
        print("Authentication failed")
    else:
        print(f"Error: {e.message}")
```

### Server-Side

```python
from arc import Server
from arc.exceptions import ARCException

server = Server(server_id="my-server")

@server.agent_handler("my-agent", "chat.start")
async def handle_start(params, context):
    if not is_valid_request(params):
        raise ARCException(code=-32602, message="Invalid params")
    
    # Process request
    return {...}
```

## Full Specification

See complete error handling:
[ARC Specification Document](https://github.com/arcprotocol/arcprotocol/blob/main/spec/arc-specification.md)

