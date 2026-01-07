---
id: overview
title: ARC Protocol Specification
sidebar_label: Overview
sidebar_position: 1
---

# ARC Protocol Specification

ARC (Agent Remote Communication) is a stateless, lightweight remote procedure call (RPC) protocol for agent communications in multi-agent systems (MAS) with workflow tracing capabilities, quantum-safe hybrid TLS encryption, and single-endpoint multi-agent routing.

## Specification Files

### Primary Specification

**[arc-openrpc.json](https://github.com/arcprotocol/arcprotocol/blob/main/spec/versions/v1.0/arc-openrpc.json)** - OpenRPC format
- Primary RPC specification
- Method definitions
- Type schemas
- Error codes

### Tooling Compatibility

**[arc-openapi.yaml](https://github.com/arcprotocol/arcprotocol/blob/main/spec/versions/v1.0/arc-openapi.yaml)** - OpenAPI 3.0 format
- Source for generating OpenRPC
- Used for tooling compatibility
- TypeScript type generation

## Full Specification

View the complete specification:

**[ARC Specification Document](https://github.com/arcprotocol/arcprotocol/blob/main/spec/arc-specification.md)**

## Core Protocol Features

### Stateless RPC Design
- No session state on server
- Each request is independent
- Client manages `chatId` and `taskId`

### Single Endpoint Architecture
- All agents accessible via `/arc`
- Routing via `targetAgent` field
- Simplified deployment and discovery

### Workflow Tracing
- `traceId` propagates across agent calls
- End-to-end observability
- Integration with tracing systems

### Quantum-Safe Security
- Hybrid TLS: X25519 + Kyber-768
- FIPS 203 ML-KEM compliant
- Future-proof encryption

## Method Categories

### Task Methods
Asynchronous operations:
- `task.create`
- `task.send`
- `task.info`
- `task.cancel`
- `task.subscribe`
- `task.notification`

### Chat Methods
Real-time communication:
- `chat.start`
- `chat.message`
- `chat.end`

## Request Structure

```json
{
  "method": "chat.start",
  "params": {
    "requestAgent": "client-123",
    "targetAgent": "finance-agent",
    "traceId": "trace-abc",
    "initialMessage": {
      "role": "user",
      "parts": [{"type": "text", "content": "Help with invoice"}]
    }
  }
}
```

## Response Structure

```json
{
  "result": {
    "type": "chat",
    "chat": {
      "chatId": "chat-xyz",
      "status": "ACTIVE",
      "message": {
        "role": "agent",
        "parts": [{"type": "text", "content": "I can help with that"}]
      }
    }
  }
}
```

## Error Handling

ARC uses standard RPC error codes (borrowed from JSON-RPC convention):

- `-32600` - Invalid Request
- `-32601` - Method not found
- `-32602` - Invalid params
- `-32603` - Internal error
- `-42001` - Agent not found
- `-42002` - Authentication failed
- `-42003` - Task not found
- `-42004` - Task processing error

## Schema Usage

### Generate TypeScript Types

```bash
npm run generate:types
```

### Generate OpenRPC from OpenAPI

```bash
npm run generate:openrpc
```

### Validate Schema

```bash
npm run validate
```

## Links

- [Website](https://arc-protocol.org)
- [GitHub](https://github.com/arcprotocol)
- [Full Specification](https://github.com/arcprotocol/arcprotocol/blob/main/spec/arc-specification.md)
- [OpenRPC Spec](https://github.com/arcprotocol/arcprotocol/blob/main/spec/versions/v1.0/arc-openrpc.json)
- [OpenAPI Spec](https://github.com/arcprotocol/arcprotocol/blob/main/spec/versions/v1.0/arc-openapi.yaml)

