# Single Endpoint

Single-endpoint multi-agent routing in ARC Protocol.

## Design

All ARC communication happens through one endpoint:

```
POST /arc
```

Agent routing determined by request body, not URL path.

## Request Routing

```json
{
  "arc": "1.0",
  "method": "chat.start",
  "requestAgent": "client-123",
  "targetAgent": "finance-agent",
  "params": {...}
}
```

The `targetAgent` field determines routing.

## Benefits

### Simplified Infrastructure

**Single Load Balancer:**
```
Client → Load Balancer → Server Pool
            /arc
```

No per-agent routing configuration required.

### Dynamic Agent Addition

Add agents without infrastructure changes:

```python
# Add new agent
@server.agent_handler("new-agent", "chat.start")
async def handle_chat(params, context):
    return {...}
```

No load balancer reconfiguration needed.

### Consistent Monitoring

Single endpoint simplifies:
- Logging
- Metrics
- Rate limiting
- Authentication

### Protocol Simplicity

Clients need one endpoint URL:

```python
client = Client(endpoint="https://api.example.com/arc")

# Route to any agent
await client.chat.start(target_agent="agent-a", ...)
await client.chat.start(target_agent="agent-b", ...)
await client.chat.start(target_agent="agent-c", ...)
```

## Multi-Agent Deployment

### Co-located Agents

Multiple agents on single server:

```python
server = Server(server_id="multi-agent-server")

@server.agent_handler("finance-agent", "chat.start")
async def finance_chat(params, context):
    return {...}

@server.agent_handler("hr-agent", "chat.start")
async def hr_chat(params, context):
    return {...}

@server.agent_handler("support-agent", "chat.start")
async def support_chat(params, context):
    return {...}
```

All accessible via `/arc` endpoint.

### Distributed Agents

Agents on different servers share same endpoint pattern:

```
Server 1: https://api.example.com/arc
  - finance-agent
  - hr-agent

Server 2: https://api.example.com/arc
  - support-agent
  - legal-agent
```

Clients route to appropriate server based on agent location.

## Agent Discovery

Single endpoint enables dynamic discovery:

```
Query: "Which agents are available?"
Response: ["finance-agent", "hr-agent", "support-agent"]

All accessible via: POST /arc
```

## Internal Routing

Server-side routing logic:

```python
def route_request(request):
    target_agent = request["targetAgent"]
    method = request["method"]
    
    # Find handler
    handler = agents[target_agent][method]
    
    # Execute
    return await handler(request["params"], context)
```

Clean separation between protocol and routing.

## Comparison

### Traditional REST

```
POST /finance-agent/chat
POST /hr-agent/chat
POST /support-agent/chat
```

Requires URL routing for each agent.

### ARC Single Endpoint

```
POST /arc
{targetAgent: "finance-agent"}

POST /arc
{targetAgent: "hr-agent"}

POST /arc
{targetAgent: "support-agent"}
```

Agent routing at protocol level.

## Advantages

1. **Infrastructure Simplicity** - One endpoint, one load balancer rule
2. **Dynamic Scaling** - Add agents without infrastructure changes
3. **Consistent Monitoring** - Single endpoint to monitor
4. **Clean Abstraction** - Routing logic in application, not infrastructure
5. **Discovery Support** - Easy to query available agents

## Trade-offs

**Pros:**
- Simplified infrastructure
- Dynamic agent management
- Consistent interface
- Easy discovery

**Cons:**
- All traffic through one endpoint (can be mitigated with horizontal scaling)
- Agent filtering at application layer (negligible overhead)

## Implementation

See [Python SDK Server](../../sdk/python/server/) for implementation examples.

## Links

- [Architecture Patterns](../architecture/)
- [Agent Discovery](../agent-discovery/)

