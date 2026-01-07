# Stateless RPC

Why ARC uses stateless RPC pattern instead of JSON-RPC 2.0.

## ARC is Not JSON-RPC

ARC is a **pure RPC-style protocol**, not JSON-RPC 2.0. Key differences:

### JSON-RPC 2.0
- Rigid specification with strict requirements
- Fixed request/response structure
- Limited to JSON-RPC 2.0 specification rules

### ARC Protocol
- Own RPC design with JSON serialization
- Flexible agent-centric routing
- Protocol-level agent identification
- Built-in workflow tracing
- Borrows error code conventions from JSON-RPC (-32xxx range)

## Stateless Design

### Request Independence

Each request contains all necessary information:

```json
{
  "arc": "1.0",
  "id": "request-123",
  "method": "task.create",
  "requestAgent": "client-agent",
  "targetAgent": "server-agent",
  "params": {...},
  "traceId": "trace-456"
}
```

No server-side session required.

### Response Correlation

Responses match requests via `id` field:

```json
{
  "arc": "1.0",
  "id": "request-123",
  "responseAgent": "server-agent",
  "targetAgent": "client-agent",
  "result": {...}
}
```

### Benefits

**Horizontal Scaling:**
- Any server instance can handle any request
- No session affinity required
- Load balancing simplified

**Reliability:**
- No session state to lose
- Failures isolated to single request
- Automatic retry possible

**Simplicity:**
- No session management overhead
- No session storage required
- Clear request/response boundaries

## Agent-Level Routing

Routing determined by protocol fields, not URLs:

```
POST /arc

{
  "targetAgent": "finance-agent",
  "method": "chat.start"
}
```

Single endpoint serves multiple agents.

## Error Code Conventions

ARC borrows error code ranges from JSON-RPC conventions but defines its own meanings:

**Standard RPC Errors (-32xxx):**
- `-32700` Parse error
- `-32600` Invalid request
- `-32601` Method not found
- `-32602` Invalid params
- `-32603` Internal error

**ARC-Specific Errors:**
- `-41xxx` Agent errors
- `-42xxx` Task errors
- `-43xxx` Chat errors
- `-44xxx` Security errors
- `-45xxx` Protocol errors

See [Error Codes](./error-codes.md) for complete taxonomy.

## Comparison

| Feature | ARC Protocol | JSON-RPC 2.0 |
|---------|-------------|--------------|
| Type | Pure RPC | JSON-RPC Standard |
| Routing | Agent-level | Not specified |
| Tracing | Built-in `traceId` | Not specified |
| Session | Stateless | Not specified |
| Errors | Extended taxonomy | Standard codes |
| Streaming | SSE support | Not specified |

## Design Rationale

**Why Not JSON-RPC 2.0:**
1. No agent routing concept
2. No workflow tracing
3. Rigid specification
4. Limited error taxonomy
5. No streaming support

**Why Stateless RPC:**
1. Scalability requirements
2. Multi-agent routing needs
3. Workflow tracing integration
4. Flexible error handling
5. SSE streaming compatibility

## Links

- [Single Endpoint Design](./single-endpoint.md)
- [Error Codes](./error-codes.md)
- [Specification](../../spec/arc-specification.md)

