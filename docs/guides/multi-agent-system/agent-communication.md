# Agent Communication

Enable agents to communicate with each other while preserving workflow tracing.

## Overview

Agents call other agents using ARC Protocol client. The `traceId` propagates automatically.

## Architecture

```
User → Agent A → Agent B → Agent C
       └─────────traceId────────┘
```

## Basic Agent-to-Agent Call

### Agent A Calls Agent B

```python
# agent_a_server.py
from arc import Server, Client

server = Server(server_id="agent-a")
agent_b_client = Client("http://localhost:8002/arc")

@server.agent_handler("agent-a", "chat.start")
async def handle_start(params, context):
    user_message = params["initialMessage"]["parts"][0]["content"]
    
    # Call Agent B
    agent_b_response = await agent_b_client.chat.start(
        target_agent="agent-b",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": f"Process: {user_message}"}]
        },
        trace_id=context.trace_id  # Propagate traceId
    )
    
    # Use Agent B's response
    b_result = agent_b_response.result['chat']['message']['parts'][0]['content']
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": f"Agent A processed via Agent B: {b_result}"}]
            }
        }
    }

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8001)
```

### Agent B Implementation

```python
# agent_b_server.py
from arc import Server

server = Server(server_id="agent-b")

@server.agent_handler("agent-b", "chat.start")
async def handle_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    # Process request
    result = f"Agent B processed: {message}"
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": result}]
            }
        }
    }

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8002)
```

## Test Agent Communication

```python
# test_communication.py
from arc import Client
import asyncio

async def test():
    client = Client("http://localhost:8001/arc")
    
    # Call Agent A, which calls Agent B internally
    response = await client.chat.start(
        target_agent="agent-a",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "Hello"}]
        }
    )
    
    print(response.result['chat']['message']['parts'][0]['content'])
    # Output: "Agent A processed via Agent B: Agent B processed: Process: Hello"

asyncio.run(test())
```

## Workflow Tracing

### TraceId Propagation

```python
# Automatic traceId propagation
@server.agent_handler("agent-a", "chat.start")
async def handle_start(params, context):
    # context.trace_id is automatically available
    
    # Pass to Agent B
    response = await agent_b_client.chat.start(
        target_agent="agent-b",
        initial_message={...},
        trace_id=context.trace_id  # Propagate
    )
    
    return {...}
```

### Observability Integration

```python
import logging

logger = logging.getLogger(__name__)

@server.agent_handler("agent-a", "chat.start")
async def handle_start(params, context):
    logger.info(f"[{context.trace_id}] Agent A started")
    
    # Call Agent B
    response = await agent_b_client.chat.start(
        target_agent="agent-b",
        initial_message={...},
        trace_id=context.trace_id
    )
    
    logger.info(f"[{context.trace_id}] Agent B completed")
    
    return {...}
```

## Multi-Agent Chain

### Agent A → Agent B → Agent C

```python
# Agent A calls Agent B
@server_a.agent_handler("agent-a", "chat.start")
async def a_handle(params, context):
    response_b = await client_b.chat.start(
        target_agent="agent-b",
        initial_message={...},
        trace_id=context.trace_id
    )
    
    return {...}

# Agent B calls Agent C
@server_b.agent_handler("agent-b", "chat.start")
async def b_handle(params, context):
    response_c = await client_c.chat.start(
        target_agent="agent-c",
        initial_message={...},
        trace_id=context.trace_id
    )
    
    return {...}

# Agent C processes
@server_c.agent_handler("agent-c", "chat.start")
async def c_handle(params, context):
    # Final processing
    return {...}
```

All three agents share the same `traceId`.

## Parallel Agent Calls

### Call Multiple Agents Simultaneously

```python
import asyncio

@server.agent_handler("orchestrator", "chat.start")
async def handle_start(params, context):
    # Call three agents in parallel
    results = await asyncio.gather(
        agent_a_client.chat.start(
            target_agent="agent-a",
            initial_message={...},
            trace_id=context.trace_id
        ),
        agent_b_client.chat.start(
            target_agent="agent-b",
            initial_message={...},
            trace_id=context.trace_id
        ),
        agent_c_client.chat.start(
            target_agent="agent-c",
            initial_message={...},
            trace_id=context.trace_id
        )
    )
    
    # Aggregate results
    combined = " | ".join([
        r.result['chat']['message']['parts'][0]['content']
        for r in results
    ])
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": combined}]
            }
        }
    }
```

## Error Handling

### Handle Agent Failures

```python
from arc.exceptions import ARCException

@server.agent_handler("agent-a", "chat.start")
async def handle_start(params, context):
    try:
        response = await agent_b_client.chat.start(
            target_agent="agent-b",
            initial_message={...},
            trace_id=context.trace_id
        )
        
        return {...}
    
    except ARCException as e:
        # Agent B failed
        logger.error(f"Agent B error: {e.message}")
        
        # Fallback response
        return {
            "type": "chat",
            "chat": {
                "chatId": params.get("chatId") or generate_id(),
                "status": "ACTIVE",
                "message": {
                    "role": "agent",
                    "parts": [{"type": "text", "content": "Service temporarily unavailable"}]
                }
            }
        }
```

## Real-World Example

### Finance Agent Calls Payment Agent

```python
# finance_server.py
from arc import Server, Client

server = Server(server_id="finance-server")
payment_client = Client("http://localhost:8100/arc")

@server.agent_handler("finance-agent", "chat.start")
async def handle_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    if "pay invoice" in message.lower():
        # Extract invoice number
        invoice_num = message.split()[-1]
        
        # Call payment agent
        payment_response = await payment_client.task.send(
            target_agent="payment-agent",
            method="process_payment",
            parameters={"invoice": invoice_num},
            trace_id=context.trace_id
        )
        
        result = payment_response.result
        response_text = f"Payment processed: {result['status']}"
    else:
        response_text = "Finance agent ready"
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": response_text}]
            }
        }
    }
```

```python
# payment_server.py
from arc import Server

server = Server(server_id="payment-server")

@server.task_handler("payment-agent", "process_payment")
async def process_payment(params, context):
    invoice = params["invoice"]
    
    # Process payment
    return {
        "status": "completed",
        "invoice": invoice,
        "amount": "$1000.00"
    }

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8100)
```

## Best Practices

### 1. Always Propagate TraceId

```python
# Correct
response = await other_agent.chat.start(
    target_agent="other",
    initial_message={...},
    trace_id=context.trace_id  # ✓
)

# Wrong
response = await other_agent.chat.start(
    target_agent="other",
    initial_message={...}
    # ✗ Missing trace_id
)
```

### 2. Handle Timeouts

```python
import asyncio

try:
    response = await asyncio.wait_for(
        agent_b_client.chat.start(...),
        timeout=5.0  # 5 second timeout
    )
except asyncio.TimeoutError:
    # Handle timeout
    return fallback_response
```

### 3. Implement Circuit Breaker

```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.is_open = False
    
    async def call(self, func, *args, **kwargs):
        if self.is_open:
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.is_open = False
                self.failure_count = 0
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.is_open = True
            
            raise e

# Usage
breaker = CircuitBreaker()

response = await breaker.call(
    agent_b_client.chat.start,
    target_agent="agent-b",
    initial_message={...}
)
```

## Next Steps

- [Supervisor Pattern](../supervisor-pattern/) - Intelligent routing
- [Observability Concepts](../../concepts/observability/) - Tracing details

