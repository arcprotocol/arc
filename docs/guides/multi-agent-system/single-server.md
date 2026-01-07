# Single Server Deployment

Deploy multiple agents on one server.

## Overview

Single server deployment runs all agents in one process, sharing resources and dependencies.

## Architecture

```
┌─────────────────────────────────────────┐
│        Server (port 8000)               │
│                                         │
│  ┌────────────┐  ┌────────────┐        │
│  │  Finance   │  │     HR     │        │
│  │   Agent    │  │   Agent    │        │
│  └────────────┘  └────────────┘        │
│                                         │
│  ┌────────────┐                         │
│  │  Support   │                         │
│  │   Agent    │                         │
│  └────────────┘                         │
│                                         │
│  Single Endpoint: /arc                  │
└─────────────────────────────────────────┘
```

## Prerequisites

```bash
pip install arc-sdk
```

## Implementation

### Step 1: Create Server

```python
# server.py
from arc import Server

server = Server(server_id="multi-agent-server")
```

### Step 2: Implement Agents

```python
# Finance Agent
@server.agent_handler("finance-agent", "chat.start")
async def finance_chat_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    # Process finance query
    if "invoice" in message.lower():
        response = "I can help with invoice inquiries. Please provide invoice number."
    elif "payment" in message.lower():
        response = "I can assist with payment processing. What's your payment ID?"
    else:
        response = "I handle invoices, payments, and budgets. How can I help?"
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_chat_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": response}]
            }
        }
    }

@server.agent_handler("finance-agent", "chat.message")
async def finance_chat_message(params, context):
    message = params["message"]["parts"][0]["content"]
    
    # Process follow-up
    response = f"Processing your request: {message}"
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": response}]
            }
        }
    }

# HR Agent
@server.agent_handler("hr-agent", "chat.start")
async def hr_chat_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    if "salary" in message.lower():
        response = "I can help with salary inquiries. Please provide your employee ID."
    elif "benefits" in message.lower():
        response = "I can explain our benefits package. What would you like to know?"
    else:
        response = "I handle HR matters: salary, benefits, leave. How can I assist?"
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_chat_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": response}]
            }
        }
    }

@server.agent_handler("hr-agent", "chat.message")
async def hr_chat_message(params, context):
    message = params["message"]["parts"][0]["content"]
    response = f"Let me check that for you: {message}"
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": response}]
            }
        }
    }

# Support Agent
@server.agent_handler("support-agent", "chat.start")
async def support_chat_start(params, context):
    response = "Hi! I'm here to help with general support. What do you need?"
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_chat_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": response}]
            }
        }
    }

@server.agent_handler("support-agent", "chat.message")
async def support_chat_message(params, context):
    message = params["message"]["parts"][0]["content"]
    response = f"I understand your concern: {message}. Let me help you."
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": response}]
            }
        }
    }

# Helper
def generate_chat_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"
```

### Step 3: Run Server

```python
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8000)
```

## Testing

### Test Finance Agent

```python
# test_client.py
from arc import Client
import asyncio

async def test_finance():
    client = Client("http://localhost:8000/arc")
    
    # Start chat
    response = await client.chat.start(
        target_agent="finance-agent",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "I need help with an invoice"}]
        }
    )
    
    print(f"Finance Agent: {response.result['chat']['message']['parts'][0]['content']}")
    
    # Follow-up
    chat_id = response.result['chat']['chatId']
    response = await client.chat.message(
        target_agent="finance-agent",
        chat_id=chat_id,
        message={
            "role": "user",
            "parts": [{"type": "text", "content": "Invoice number INV-12345"}]
        }
    )
    
    print(f"Finance Agent: {response.result['chat']['message']['parts'][0]['content']}")

asyncio.run(test_finance())
```

### Test All Agents

```python
async def test_all_agents():
    client = Client("http://localhost:8000/arc")
    
    agents = ["finance-agent", "hr-agent", "support-agent"]
    messages = [
        "Help with invoice",
        "Question about salary",
        "General support needed"
    ]
    
    for agent, message in zip(agents, messages):
        response = await client.chat.start(
            target_agent=agent,
            initial_message={
                "role": "user",
                "parts": [{"type": "text", "content": message}]
            }
        )
        
        print(f"{agent}: {response.result['chat']['message']['parts'][0]['content']}")

asyncio.run(test_all_agents())
```

## Production Considerations

### 1. Error Handling

```python
from arc.exceptions import ARCException

@server.agent_handler("finance-agent", "chat.start")
async def finance_chat_start(params, context):
    try:
        # Agent logic
        return {...}
    except Exception as e:
        # Log error
        print(f"Error in finance-agent: {e}")
        raise ARCException(code=-42004, message="Task processing error")
```

### 2. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@server.agent_handler("finance-agent", "chat.start")
async def finance_chat_start(params, context):
    logger.info(f"Finance agent received: {params['initialMessage']}")
    # Process
    return {...}
```

### 3. Resource Limits

```python
# Limit concurrent requests per agent
from asyncio import Semaphore

finance_semaphore = Semaphore(10)  # Max 10 concurrent

@server.agent_handler("finance-agent", "chat.start")
async def finance_chat_start(params, context):
    async with finance_semaphore:
        # Process request
        return {...}
```

### 4. Health Check

```python
# Built-in health endpoint
# GET http://localhost:8000/health

# Response:
# {
#   "status": "healthy",
#   "server_id": "multi-agent-server",
#   "version": "1.0.0"
# }
```

## Advantages

1. **Simple Deployment** - Single process, single port
2. **Low Latency** - No network overhead between agents
3. **Shared Resources** - Common dependencies, memory
4. **Easy Debugging** - All logs in one place

## Limitations

1. **Scaling** - All agents scale together
2. **Resource Contention** - Agents share CPU/memory
3. **Fault Isolation** - One agent crash affects all
4. **Deployment Coupling** - Update one, redeploy all

## When to Use

Use single server when:
- Development and testing
- Low to medium traffic
- Tight budget constraints
- Agents have similar scaling needs

For production with high traffic or independent scaling, see [Distributed Deployment](./distributed.md).

## Complete Example

```python
# complete_server.py
from arc import Server
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Server(server_id="multi-agent-server")

def generate_chat_id():
    return f"chat-{uuid.uuid4().hex[:8]}"

# Finance Agent
@server.agent_handler("finance-agent", "chat.start")
async def finance_start(params, context):
    logger.info(f"Finance agent: new chat")
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_chat_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Finance agent ready"}]
            }
        }
    }

@server.agent_handler("finance-agent", "chat.message")
async def finance_message(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Processing finance request"}]
            }
        }
    }

# HR Agent
@server.agent_handler("hr-agent", "chat.start")
async def hr_start(params, context):
    logger.info(f"HR agent: new chat")
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_chat_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "HR agent ready"}]
            }
        }
    }

@server.agent_handler("hr-agent", "chat.message")
async def hr_message(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Processing HR request"}]
            }
        }
    }

# Support Agent
@server.agent_handler("support-agent", "chat.start")
async def support_start(params, context):
    logger.info(f"Support agent: new chat")
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_chat_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Support agent ready"}]
            }
        }
    }

@server.agent_handler("support-agent", "chat.message")
async def support_message(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Processing support request"}]
            }
        }
    }

if __name__ == "__main__":
    print("Starting multi-agent server on port 8000...")
    print("Available agents: finance-agent, hr-agent, support-agent")
    server.run(host="0.0.0.0", port=8000)
```

Run: `python complete_server.py`

## Next Steps

- [Distributed Deployment](./distributed.md) - Scale agents independently
- [Agent Communication](./agent-communication.md) - Agent-to-agent calls
- [Supervisor Pattern](../supervisor-pattern/) - Add intelligent routing

