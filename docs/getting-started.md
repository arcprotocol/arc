---
id: getting-started
title: Getting Started
sidebar_position: 2
---

# Getting Started

## Protocol Overview

**Core Features:**
- Single endpoint serves multiple agents via `targetAgent` routing
- Stateless RPC design with JSON serialization
- Workflow tracing via `traceId` propagation
- Quantum-safe hybrid TLS (X25519 + Kyber-768)
- Server-Sent Events (SSE) for real-time streaming

**Transport:** HTTPS  
**Content-Type:** `application/arc+json`  
**Authentication:** OAuth2 Bearer Token

## Protocol Structure

### Request Format

```json
{
  "arc": "1.0",
  "id": "unique-request-id",
  "method": "task.create",
  "requestAgent": "client-id",
  "targetAgent": "destination-agent",
  "params": { /* method-specific parameters */ },
  "traceId": "workflow-trace-id"
}
```

### Response Format

```json
{
  "arc": "1.0",
  "id": "unique-request-id",
  "responseAgent": "destination-agent",
  "targetAgent": "client-id",
  "result": { /* method-specific result */ },
  "error": null,
  "traceId": "workflow-trace-id"
}
```

### Error Format

```json
{
  "arc": "1.0",
  "id": "unique-request-id",
  "responseAgent": "server",
  "targetAgent": "client-id",
  "result": null,
  "error": {
    "code": -41001,
    "message": "Agent not found",
    "details": { /* error-specific details */ }
  }
}
```

## Available Methods

### Task Methods
Asynchronous operations for long-running work:

| Method | Purpose |
|--------|---------|
| `task.create` | Create new task with initial message |
| `task.send` | Send additional message to existing task |
| `task.info` | Query task status and history |
| `task.cancel` | Cancel running task |
| `task.subscribe` | Subscribe to task status notifications |
| `task.notification` | Server-initiated notification (server-to-client) |

### Chat Methods
Real-time streaming for interactive conversations:

| Method | Purpose |
|--------|---------|
| `chat.start` | Begin new chat session with initial message |
| `chat.message` | Send message in active chat session |
| `chat.end` | Terminate active chat session |

## Quick Start with Python SDK

### Installation

```bash
pip install arc-sdk

# With quantum-safe TLS support
pip install arc-sdk[pqc]
```

### Client Example

```python
from arc import ARCClient

client = ARCClient(
    endpoint="https://api.example.com/arc",
    token="your-oauth2-token"
)

# Create a task
response = await client.task_create(
    target_agent="booking-agent",
    initial_message={
        "role": "user",
        "parts": [{"type": "text", "content": "Book flight to Paris"}]
    }
)

task_id = response["result"]["task"]["taskId"]
```

### Server Example

```python
from arc import ARCServer

server = ARCServer(server_id="booking-server")

@server.task_handler("booking-agent")
async def handle_booking(params, context):
    message = params["initialMessage"]
    
    # Process booking logic
    task_id = create_booking_task(message)
    
    return {
        "type": "task",
        "task": {
            "taskId": task_id,
            "status": "SUBMITTED",
            "createdAt": datetime.utcnow().isoformat() + "Z"
        }
    }

server.run(host="0.0.0.0", port=8000)
```

## Next Steps

**Implementation Guides:**
- [Multi-Agent System](guides/multi-agent-system/index.md) - Deploy multiple agents on single or distributed servers
- [Supervisor Pattern](guides/supervisor-pattern/index.md) - Intelligent routing with ARC Compass and Ledger

**Core Concepts:**
- [Protocol Design](concepts/protocol-design/index.md) - Stateless RPC, single-endpoint architecture, error handling
- [Architecture](concepts/architecture/index.md) - Multi-agent patterns, supervisor/router, workflow composition
- [Security](concepts/security/index.md) - OAuth2 authentication, quantum-safe TLS, authorization

**SDK Documentation:**
- [Python SDK](sdk/python/index.md) - Complete client/server implementation
- [Client Methods](sdk/python/client/index.md) - Task and chat operations
- [Server Implementation](sdk/python/server/index.md) - Handler registration and routing

**Specification:**
- [ARC Specification](spec/overview.md) - Complete technical specification
- [OpenRPC Schema](https://github.com/arcprotocol/arcprotocol/tree/main/spec/versions/v1.0) - Machine-readable protocol definition