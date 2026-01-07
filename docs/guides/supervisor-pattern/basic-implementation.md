# Basic Supervisor Implementation

Build a supervisor agent with keyword-based routing logic.

## Overview

Simple supervisor that analyzes user messages and routes to specialized agents using keyword matching.

## Prerequisites

```bash
pip install arc-sdk
```

## Architecture

```
User Query: "I need help with invoice INV-123"
     │
     ▼
Supervisor (keyword analysis)
     │
     ▼ (contains "invoice")
Finance Agent
```

## Step 1: Deploy Sub-Agents

### finance_agent.py

```python
from arc import Server

server = Server(server_id="finance-server")

@server.agent_handler("finance-agent", "chat.start")
async def handle_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": f"Finance agent: {message}"}]
            }
        }
    }

@server.agent_handler("finance-agent", "chat.message")
async def handle_message(params, context):
    message = params["message"]["parts"][0]["content"]
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": f"Processing: {message}"}]
            }
        }
    }

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8001)
```

### hr_agent.py

```python
from arc import Server

server = Server(server_id="hr-server")

@server.agent_handler("hr-agent", "chat.start")
async def handle_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": f"HR agent: {message}"}]
            }
        }
    }

@server.agent_handler("hr-agent", "chat.message")
async def handle_message(params, context):
    message = params["message"]["parts"][0]["content"]
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": f"Processing: {message}"}]
            }
        }
    }

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8002)
```

### support_agent.py

```python
from arc import Server

server = Server(server_id="support-server")

@server.agent_handler("support-agent", "chat.start")
async def handle_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": f"Support agent: {message}"}]
            }
        }
    }

@server.agent_handler("support-agent", "chat.message")
async def handle_message(params, context):
    message = params["message"]["parts"][0]["content"]
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": f"Processing: {message}"}]
            }
        }
    }

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8003)
```

## Step 2: Implement Supervisor

### supervisor.py

```python
from arc import Server, Client
import re

server = Server(server_id="supervisor-server")

# Sub-agent clients
finance_client = Client("http://localhost:8001/arc")
hr_client = Client("http://localhost:8002/arc")
support_client = Client("http://localhost:8003/arc")

# Routing rules
ROUTING_RULES = {
    "finance": {
        "keywords": ["invoice", "payment", "budget", "expense", "finance"],
        "client": finance_client,
        "agent": "finance-agent"
    },
    "hr": {
        "keywords": ["salary", "benefits", "leave", "vacation", "hr", "employee"],
        "client": hr_client,
        "agent": "hr-agent"
    },
    "support": {
        "keywords": ["help", "support", "question", "issue"],
        "client": support_client,
        "agent": "support-agent"
    }
}

def route_message(message: str) -> tuple:
    """Analyze message and return (client, agent_id)"""
    message_lower = message.lower()
    
    # Check each routing rule
    for domain, config in ROUTING_RULES.items():
        for keyword in config["keywords"]:
            if keyword in message_lower:
                return config["client"], config["agent"]
    
    # Default to support
    return support_client, "support-agent"

@server.agent_handler("supervisor", "chat.start")
async def supervisor_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    # Route to appropriate agent
    client, agent_id = route_message(message)
    
    # Forward to sub-agent
    response = await client.chat.start(
        target_agent=agent_id,
        initial_message=params["initialMessage"],
        trace_id=context.trace_id
    )
    
    return response.result

@server.agent_handler("supervisor", "chat.message")
async def supervisor_message(params, context):
    message = params["message"]["parts"][0]["content"]
    
    # Route based on current message
    client, agent_id = route_message(message)
    
    # Forward to sub-agent
    response = await client.chat.message(
        target_agent=agent_id,
        chat_id=params["chatId"],
        message=params["message"],
        trace_id=context.trace_id
    )
    
    return response.result

if __name__ == "__main__":
    print("Starting supervisor on port 8000...")
    print("Sub-agents: finance (8001), hr (8002), support (8003)")
    server.run(host="0.0.0.0", port=8000)
```

## Step 3: Run System

```bash
# Terminal 1: Finance agent
python finance_agent.py

# Terminal 2: HR agent
python hr_agent.py

# Terminal 3: Support agent
python support_agent.py

# Terminal 4: Supervisor
python supervisor.py
```

## Step 4: Test Routing

```python
# test_supervisor.py
from arc import Client
import asyncio

async def test_supervisor():
    client = Client("http://localhost:8000/arc")
    
    # Test 1: Finance routing
    response = await client.chat.start(
        target_agent="supervisor",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "I need help with invoice INV-123"}]
        }
    )
    print(f"Finance: {response.result['chat']['message']['parts'][0]['content']}")
    
    # Test 2: HR routing
    response = await client.chat.start(
        target_agent="supervisor",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "Question about my salary"}]
        }
    )
    print(f"HR: {response.result['chat']['message']['parts'][0]['content']}")
    
    # Test 3: Support routing (default)
    response = await client.chat.start(
        target_agent="supervisor",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "General question"}]
        }
    )
    print(f"Support: {response.result['chat']['message']['parts'][0]['content']}")

asyncio.run(test_supervisor())
```

Expected output:
```
Finance: Finance agent: I need help with invoice INV-123
HR: HR agent: Question about my salary
Support: Support agent: General question
```

## Enhanced Routing

### Multi-Keyword Scoring

```python
def route_message(message: str) -> tuple:
    """Score-based routing"""
    message_lower = message.lower()
    scores = {}
    
    for domain, config in ROUTING_RULES.items():
        score = sum(1 for kw in config["keywords"] if kw in message_lower)
        scores[domain] = score
    
    # Select highest scoring domain
    best_domain = max(scores.items(), key=lambda x: x[1])[0]
    
    if scores[best_domain] == 0:
        # No match, use support
        return support_client, "support-agent"
    
    config = ROUTING_RULES[best_domain]
    return config["client"], config["agent"]
```

### Regex-Based Routing

```python
ROUTING_PATTERNS = {
    "finance": [
        r"invoice\s+\w+",
        r"payment\s+\d+",
        r"\$\d+",
    ],
    "hr": [
        r"employee\s+id",
        r"salary\s+review",
        r"pto|vacation",
    ]
}

def route_message(message: str) -> tuple:
    for domain, patterns in ROUTING_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                config = ROUTING_RULES[domain]
                return config["client"], config["agent"]
    
    # Default
    return support_client, "support-agent"
```

## Session Management

### Track Sub-Agent Chat IDs

```python
# Store mapping: supervisor_chat_id → (sub_agent_client, sub_agent_id, sub_chat_id)
session_store = {}

@server.agent_handler("supervisor", "chat.start")
async def supervisor_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    client, agent_id = route_message(message)
    
    # Call sub-agent
    response = await client.chat.start(
        target_agent=agent_id,
        initial_message=params["initialMessage"],
        trace_id=context.trace_id
    )
    
    # Store session
    supervisor_chat_id = params.get("chatId") or generate_id()
    sub_chat_id = response.result['chat']['chatId']
    
    session_store[supervisor_chat_id] = {
        "client": client,
        "agent_id": agent_id,
        "sub_chat_id": sub_chat_id
    }
    
    # Return with supervisor's chat ID
    result = response.result
    result['chat']['chatId'] = supervisor_chat_id
    return result

@server.agent_handler("supervisor", "chat.message")
async def supervisor_message(params, context):
    supervisor_chat_id = params["chatId"]
    
    # Retrieve session
    session = session_store.get(supervisor_chat_id)
    
    if not session:
        raise Exception("Session not found")
    
    # Forward to same sub-agent
    response = await session["client"].chat.message(
        target_agent=session["agent_id"],
        chat_id=session["sub_chat_id"],
        message=params["message"],
        trace_id=context.trace_id
    )
    
    # Return with supervisor's chat ID
    result = response.result
    result['chat']['chatId'] = supervisor_chat_id
    return result

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"
```

## Production Considerations

### 1. Persistent Session Storage

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)

def store_session(chat_id, session_data):
    redis_client.setex(
        f"session:{chat_id}",
        3600,  # 1 hour TTL
        json.dumps(session_data)
    )

def get_session(chat_id):
    data = redis_client.get(f"session:{chat_id}")
    return json.loads(data) if data else None
```

### 2. Circuit Breaker for Sub-Agents

```python
from datetime import datetime, timedelta

class AgentCircuitBreaker:
    def __init__(self):
        self.failures = {}
    
    async def call(self, client, agent_id, method, **kwargs):
        if self.is_open(agent_id):
            raise Exception(f"{agent_id} is unavailable")
        
        try:
            response = await getattr(client.chat, method)(**kwargs)
            self.record_success(agent_id)
            return response
        except Exception as e:
            self.record_failure(agent_id)
            raise e
    
    def is_open(self, agent_id):
        if agent_id not in self.failures:
            return False
        return self.failures[agent_id]["count"] >= 5
    
    def record_failure(self, agent_id):
        if agent_id not in self.failures:
            self.failures[agent_id] = {"count": 0, "time": datetime.now()}
        self.failures[agent_id]["count"] += 1
    
    def record_success(self, agent_id):
        if agent_id in self.failures:
            del self.failures[agent_id]

breaker = AgentCircuitBreaker()

# Usage
response = await breaker.call(
    client, agent_id, "start",
    target_agent=agent_id,
    initial_message={...}
)
```

### 3. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@server.agent_handler("supervisor", "chat.start")
async def supervisor_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    client, agent_id = route_message(message)
    
    logger.info(f"[{context.trace_id}] Routing to {agent_id}: {message[:50]}...")
    
    response = await client.chat.start(...)
    
    logger.info(f"[{context.trace_id}] {agent_id} responded")
    
    return response.result
```

## Limitations

1. **Static Rules** - Cannot adapt to new agent types
2. **Manual Updates** - Adding agents requires code changes
3. **No Capability Discovery** - Cannot query agent capabilities

For dynamic routing, see [ARC Ledger Integration](./arc-ledger-integration.md).

## Next Steps

- [ARC Ledger Integration](./arc-ledger-integration.md) - Dynamic discovery
- [Dynamic Prompts](./dynamic-prompts.md) - Capability-aware prompts

