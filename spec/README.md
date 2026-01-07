# ARC Protocol Specifications

This directory contains the official ARC Protocol specifications, schemas, and technical documentation.

**ARC (Agent Remote Communication)** is a stateless, lightweight remote procedure call (RPC) protocol for agent communications in multi-agent systems (MAS) with workflow tracing capabilities, quantum-safe hybrid TLS encryption, and single-endpoint multi-agent routing.

- Website: https://arc-protocol.org
- GitHub: https://github.com/arcprotocol

## Current Version: 1.0

### Specification Files

- **[arc-specification.md](arc-specification.md)** - Complete protocol specification
- **[arc-openrpc.json](versions/v1.0/arc-openrpc.json)** - OpenRPC schema (primary specification for RPC protocols)
- **[arc-openapi.yaml](versions/v1.0/arc-openapi.yaml)** - OpenAPI 3.0 schema (for tooling compatibility)

### Version Information

- **Status**: Stable
- **Release**: August 7, 2025
- **Breaking Changes**: None (initial release)

## Protocol Definition

ARC is a communication standard between agents for multi-agent systems. The protocol enables:

- **Multi-agent architecture**: Single endpoint supports multiple agents
- **Agent-level routing**: `requestAgent` and `targetAgent` identification at protocol level
- **Workflow tracing**: End-to-end traceability via `traceId` for monitoring integration
- **Stateless design**: Each request is independent and self-contained
- **Method-based invocation**: Clean RPC-style method calls
- **SSE streaming**: Real-time streaming via Server-Sent Events

### Message Structure

ARC uses a stateless RPC pattern with JSON serialization:

```json
{
  "arc": "1.0",
  "id": "request-id",
  "method": "task.create",
  "requestAgent": "client-agent-id",
  "targetAgent": "server-agent-id",
  "params": { ... },
  "traceId": "optional-trace-id"
}
```

### Method Definitions

**Task Methods** (Asynchronous Operations):
- `task.create` - Initialize task with initial message
- `task.send` - Append additional messages to existing task
- `task.info` - Retrieve task state and artifacts
- `task.cancel` - Terminate task execution
- `task.subscribe` - Register webhook for task events
- `task.notification` - Server-initiated event notification

**Chat Methods** (Real-time Interactions):
- `chat.start` - Initialize chat session
- `chat.message` - Send message within active session
- `chat.end` - Terminate chat session

### Transport and Authentication

- **Protocol**: HTTPS
- **Method**: POST only
- **Endpoint**: `/arc` (recommended)
- **Content-Type**: `application/arc+json` or `text/event-stream` (for SSE)
- **Authentication**: OAuth 2.0 Bearer tokens (recommended)

### Data Types

The specification defines schemas for:

- **Message Parts**: TextPart, DataPart, ErrorPart, ImagePart, AudioPart, VideoPart
- **Task States**: SUBMITTED, WORKING, COMPLETED, FAILED, CANCELED
- **Chat States**: ACTIVE, CLOSED
- **Error Codes**: -32xxx (borrowed from JSON-RPC), -41xxx (Agent), -42xxx (Method), -43xxx (Session), -44xxx (Auth), -45xxx (Protocol)

### Agent Routing

Multi-agent communication is handled through the `targetAgent` field, enabling:

- Single endpoint serving multiple agents
- Agent-to-agent delegation patterns
- Cross-agent workflow orchestration
- Per-agent method implementations

### Error Handling

Comprehensive error taxonomy with hierarchical error codes:

- Standard RPC errors (-32xxx, borrowed from JSON-RPC conventions)
- Protocol errors (-45xxx)
- Authentication errors (-44xxx)
- Session errors (-43xxx)
- Task errors (-42xxx)
- Agent errors (-41xxx)

### Streaming Protocol

Server-Sent Events (SSE) support for real-time streaming:

- Content-Type: `text/event-stream`
- Event types: `content`, `metadata`, `error`, `done`
- Incremental content delivery
- Graceful error handling

## Schema Usage

### Validation

The OpenRPC schema enables:

- Runtime request/response validation
- Contract testing
- Mock server generation
- Documentation generation

### Code Generation

Generate language-specific bindings from the OpenAPI source:

```bash
npm run generate:types     # TypeScript type definitions
npm run generate:openrpc   # Convert OpenAPI to OpenRPC schema
```

### Tooling

See [../tools/](../tools/) for:

- `schema-to-types.ts` - TypeScript type generator (from OpenAPI)
- `schema-to-openrpc.ts` - OpenRPC converter (OpenAPI → OpenRPC)
- Schema validation utilities

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Related Documentation

- [Protocol Specification](arc-specification.md) - Detailed technical specification
- [Getting Started](../docs/getting-started.md) - Implementation guide
- [Examples](../examples/) - Reference implementations

## License

Apache License 2.0 - See [LICENSE](../LICENSE)