# Multi-Agent Patterns

Multi-agent deployment strategies for ARC Protocol.

## Co-located Deployment

Deploy related agents on same server to reduce network overhead.

```
┌─────────────────────────────────────────┐
│        Single Server Deployment         │
│                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Agent A │  │ Agent B │  │ Agent C │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│                                         │
│  Common Domain (e.g., Finance Suite)   │
└─────────────────────────────────────────┘
```

**Benefits:**
- Reduced network latency
- Shared dependencies
- Simplified deployment
- Lower operational overhead

**When to Use:**
- Agents share similar dependencies
- Related business domains
- Performance-critical inter-agent communication

## Distributed Deployment

Deploy agents across multiple servers for isolation and scaling.

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Server 1   │  │   Server 2   │  │   Server 3   │
│              │  │              │  │              │
│  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │
│  │Agent A │  │  │  │Agent B │  │  │  │Agent C │  │
│  │Agent D │  │  │  └────────┘  │  │  └────────┘  │
│  └────────┘  │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

**Benefits:**
- Independent scaling per agent
- Fault isolation
- Resource isolation
- Technology stack flexibility

**When to Use:**
- Different scaling requirements
- Isolation requirements
- Different technology stacks
- High availability needs

## Hybrid Deployment

Combine co-location and distribution based on requirements.

```
┌───────────────────────┐  ┌──────────────┐
│      Server 1         │  │   Server 2   │
│                       │  │              │
│  ┌────────┐┌────────┐ │  │  ┌────────┐  │
│  │Agent A ││Agent B │ │  │  │Agent C │  │
│  └────────┘└────────┘ │  │  └────────┘  │
│                       │  │              │
│  Co-located Group     │  │  Isolated    │
└───────────────────────┘  └──────────────┘
```

**Strategy:**
1. Co-locate tightly coupled agents
2. Isolate independent agents
3. Scale groups independently

## Implementation

### Single Server (Python SDK)

```python
from arc import Server

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

server.run(host="0.0.0.0", port=8000)
```

### Multiple Servers

```python
# Server 1: Finance agents
server1 = Server(server_id="finance-server")

@server1.agent_handler("finance-agent", "chat.start")
async def finance_chat(params, context):
    return {...}

server1.run(host="0.0.0.0", port=8001)
```

```python
# Server 2: Support agents
server2 = Server(server_id="support-server")

@server2.agent_handler("support-agent", "chat.start")
async def support_chat(params, context):
    return {...}

server2.run(host="0.0.0.0", port=8002)
```

## Agent Communication

### Same Server

Direct handler invocation (internal routing):

```python
# Agent A calls Agent B on same server
@server.agent_handler("agent-a", "task.create")
async def agent_a_handler(params, context):
    # Call Agent B
    result = await internal_call("agent-b", "task.create", params)
    return result
```

### Different Servers

ARC Protocol communication:

```python
# Agent A calls Agent B on different server
@server.agent_handler("agent-a", "task.create")
async def agent_a_handler(params, context):
    # Use ARC client
    client = Client("https://server2.example.com/arc")
    result = await client.task.create(
        target_agent="agent-b",
        initial_message=params["initialMessage"]
    )
    return result
```

## Scaling Strategies

### Vertical Scaling

Increase server resources for co-located agents:
- More CPU cores
- More memory
- Faster storage

### Horizontal Scaling

Add more server instances:

```
Load Balancer
      ↓
┌─────┴─────┬─────────┬─────────┐
│           │         │         │
Server 1    Server 2  Server 3  Server 4
(Agents)    (Agents)  (Agents)  (Agents)
```

Use load balancer with session affinity or stateless routing.

### Per-Agent Scaling

Scale specific agents independently:

```
┌──────────────┐
│ Load Balancer│
└┬────────┬────┘
 │        │
 │        └───────┐
 ▼                ▼
Finance Agents   Support Agents
(4 instances)    (2 instances)
```

Scale based on agent-specific load.

## Best Practices

1. **Group by Domain** - Co-locate agents in same business domain
2. **Isolate Critical Paths** - Separate high-priority agents
3. **Monitor Per-Agent** - Track metrics per agent for scaling decisions
4. **Use Trace IDs** - Enable cross-agent workflow tracing
5. **Plan for Failure** - Design for agent unavailability

## Trade-offs

| Pattern | Pros | Cons |
|---------|------|------|
| Co-located | Low latency, simple | Limited scaling, coupled deployment |
| Distributed | Independent scaling, isolation | Network overhead, complex |
| Hybrid | Balanced approach | Requires careful planning |

## Links

- [Supervisor/Router Pattern](./supervisor-router.md)
- [Workflow Composition](./workflow-composition.md)
- [Single Endpoint Design](../protocol-design/single-endpoint.md)

