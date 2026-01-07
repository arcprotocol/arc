# Supervisor/Router Pattern

Central supervisor pattern for multi-agent orchestration.

## Pattern Overview

Supervisor agent routes requests to specialized sub-agents based on capabilities and task requirements.

```
┌─────────────────────────────────────────────────────┐
│              Supervisor Agent                       │
│         (Routing + Orchestration)                   │
└───────────────┬─────────────────────────────────────┘
    ┌───────────┼───────────┬───────────┐
    ▼           ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Agent A │ │ Agent B │ │ Agent C │ │ Agent D │
│Finance  │ │  HR     │ │ Legal   │ │Support  │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
```

## Components

### Supervisor Agent

**Responsibilities:**
- Request analysis
- Agent selection
- Request routing
- Response aggregation (if needed)
- Error handling

### Sub-Agents

**Responsibilities:**
- Domain-specific processing
- Task execution
- Response generation

## Implementation

### Basic Supervisor

```python
from arc import Server, Client

supervisor = Server(server_id="supervisor")

# Sub-agent endpoints
SUB_AGENTS = {
    "finance": "https://finance-server.com/arc",
    "hr": "https://hr-server.com/arc",
    "support": "https://support-server.com/arc"
}

@supervisor.agent_handler("supervisor", "chat.start")
async def route_request(params, context):
    # Analyze request
    message = params["initialMessage"]["parts"][0]["content"]
    
    # Select agent
    target = select_agent(message)
    
    # Route to sub-agent
    client = Client(SUB_AGENTS[target])
    response = await client.chat.start(
        target_agent=target,
        initial_message=params["initialMessage"],
        trace_id=context.get("trace_id")
    )
    
    return response.result

def select_agent(message: str) -> str:
    """Agent selection logic"""
    if "salary" in message or "benefits" in message:
        return "hr"
    elif "invoice" in message or "payment" in message:
        return "finance"
    else:
        return "support"
```

## Dynamic Prompt Adjustment

Enhance prompts with agent capability context from ARC Ledger.

### Flow

```
┌─────────────────────────────────────────────────────┐
│                 Supervisor Agent                    │
│                                                     │
│  1. Receive request                                 │
│  2. Select sub-agent                                │
│  3. Query ARC Ledger for capabilities               │
│  4. Enhance prompt with capabilities                │
│  5. Route enhanced request to sub-agent             │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                   ARC Ledger                        │
│                                                     │
│  Agent metadata:                                    │
│  - Capabilities                                     │
│  - Description                                      │
│  - Endpoints                                        │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                   Sub-Agent                         │
│                                                     │
│  Receives enhanced prompt with:                     │
│  - Original request                                 │
│  - Capability context                               │
│  - Role instructions                                │
└─────────────────────────────────────────────────────┘
```

### Implementation

```python
@supervisor.agent_handler("supervisor", "chat.start")
async def route_with_context(params, context):
    # Select agent
    target = select_agent(params["initialMessage"])
    
    # Get agent capabilities from ARC Ledger
    capabilities = await ledger.get_agent_capabilities(target)
    
    # Enhance prompt
    enhanced_message = {
        "role": "user",
        "parts": [
            {
                "type": "text",
                "content": f"""You are {target} with these capabilities:
{capabilities['description']}

Capabilities: {', '.join(capabilities['capabilities'])}

User request: {params['initialMessage']['parts'][0]['content']}"""
            }
        ]
    }
    
    # Route with enhanced prompt
    client = Client(SUB_AGENTS[target])
    response = await client.chat.start(
        target_agent=target,
        initial_message=enhanced_message,
        trace_id=context.get("trace_id")
    )
    
    return response.result
```

## Runtime Agent Addition

Add sub-agents dynamically without supervisor modification.

```python
# Register new agent at runtime
def register_agent(name: str, endpoint: str):
    SUB_AGENTS[name] = endpoint
    
    # Update ARC Ledger
    await ledger.register_agent({
        "name": name,
        "endpoint": endpoint,
        "capabilities": [...],
        "description": "..."
    })

# Add agent
await register_agent("legal", "https://legal-server.com/arc")
```

## Agent Selection Strategies

### Keyword-Based

```python
def select_agent(message: str) -> str:
    keywords = {
        "finance": ["invoice", "payment", "budget"],
        "hr": ["salary", "benefits", "leave"],
        "legal": ["contract", "compliance"]
    }
    
    for agent, words in keywords.items():
        if any(word in message.lower() for word in words):
            return agent
    
    return "support"  # Default
```

### LLM-Based

```python
async def select_agent_llm(message: str) -> str:
    # Use LLM to determine routing
    prompt = f"""Determine which agent should handle this request:
Available agents: finance, hr, legal, support

Request: {message}

Respond with only the agent name."""
    
    agent = await llm.generate(prompt)
    return agent.strip().lower()
```

### Capability-Based

```python
async def select_agent_by_capability(message: str) -> str:
    # Query ARC Compass for ranked agents
    ranked_agents = await compass.search({
        "query": message,
        "limit": 1
    })
    
    return ranked_agents[0]["name"]
```

## Error Handling

```python
@supervisor.agent_handler("supervisor", "chat.start")
async def route_with_fallback(params, context):
    target = select_agent(params["initialMessage"])
    
    try:
        # Try primary agent
        client = Client(SUB_AGENTS[target])
        return await client.chat.start(
            target_agent=target,
            initial_message=params["initialMessage"],
            trace_id=context.get("trace_id")
        )
    except AgentNotAvailableError:
        # Fallback to support agent
        fallback_client = Client(SUB_AGENTS["support"])
        return await fallback_client.chat.start(
            target_agent="support",
            initial_message=params["initialMessage"],
            trace_id=context.get("trace_id")
        )
```

## Workflow Tracing

Preserve trace ID across agent hops:

```python
@supervisor.agent_handler("supervisor", "chat.start")
async def route_with_trace(params, context):
    # Extract or generate trace ID
    trace_id = context.get("trace_id") or generate_trace_id()
    
    # Route with trace ID
    response = await client.chat.start(
        target_agent=target,
        initial_message=params["initialMessage"],
        trace_id=trace_id  # Propagate trace
    )
    
    return response.result
```

## Benefits

1. **Centralized Routing** - Single point for routing logic
2. **Easy Expansion** - Add agents without client changes
3. **Capability Discovery** - Dynamic agent selection
4. **Context Enhancement** - Prompt adjustment with capabilities
5. **Fault Tolerance** - Fallback and retry logic

## Trade-offs

**Pros:**
- Clean separation of concerns
- Flexible agent addition
- Centralized monitoring

**Cons:**
- Additional network hop
- Single point of failure (mitigate with supervisor redundancy)
- Supervisor must handle all agent selection logic

## Links

- [Multi-Agent Patterns](./multi-agent.md)
- [Agent Discovery](../agent-discovery/)
- [Workflow Tracing](../observability/workflow-tracing.md)

