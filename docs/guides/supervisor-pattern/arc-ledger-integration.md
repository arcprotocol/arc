# ARC Ledger Integration

Implement dynamic agent discovery and routing using ARC Ledger.

## Overview

ARC Ledger provides a discovery service for agents. Supervisors query Ledger to find agents based on capabilities and route requests dynamically.

## Prerequisites

```bash
pip install arc-sdk
# ARC Ledger access credentials
```

## Architecture

```
┌──────────┐
│   User   │
└─────┬────┘
      │ "Find document processing agents"
      ▼
┌────────────────┐
│   Supervisor   │
└────┬───────────┘
     │
     │ 1. Query Ledger: capabilities={fileUpload: true}
     ▼
┌────────────────┐         ┌─────────────────┐
│   ARC Ledger   │ ──────► │ [Agent A, B, C] │
└────────────────┘         └─────────────────┘
     │
     │ 2. Return matching agents
     ▼
┌────────────────┐
│   Supervisor   │ ──────► Select Agent B
└────┬───────────┘
     │
     │ 3. Route request
     ▼
┌────────────────┐
│    Agent B     │
└────────────────┘
```

## Step 1: Register Agents

Register agents with ARC Ledger including their capabilities and endpoints.

### Register Finance Agent

```python
# Note: This is TypeScript example as Python SDK doesn't have Ledger client yet
# Use HTTP requests directly or wait for Python Ledger SDK

import aiohttp

async def register_finance_agent():
    async with aiohttp.ClientSession() as session:
        agent_card = {
            "name": "Finance Agent",
            "visibility": "public",
            "description": "Handles invoices, payments, and budgets",
            "version": "1.0.0",
            "url": "http://localhost:8001/arc",
            "provider": {
                "organization": "YourCompany",
                "contact": "finance@company.com"
            },
            "capabilities": {
                "streaming": True,
                "fileUpload": False
            },
            "skills": [
                {
                    "name": "Invoice Processing",
                    "description": "Process and track invoices"
                },
                {
                    "name": "Payment Management",
                    "description": "Handle payment transactions"
                }
            ],
            "tags": ["finance", "invoices", "payments"]
        }
        
        async with session.post(
            "https://ledger.arcprotocol.ai/agents",
            json=agent_card,
            headers={"Authorization": f"Bearer {LEDGER_API_KEY}"}
        ) as response:
            result = await response.json()
            return result["agentId"]
```

### Register HR Agent

```python
async def register_hr_agent():
    async with aiohttp.ClientSession() as session:
        agent_card = {
            "name": "HR Agent",
            "visibility": "public",
            "description": "Manages employee queries and benefits",
            "version": "1.0.0",
            "url": "http://localhost:8002/arc",
            "provider": {
                "organization": "YourCompany",
                "contact": "hr@company.com"
            },
            "capabilities": {
                "streaming": True,
                "fileUpload": False
            },
            "skills": [
                {
                    "name": "Salary Inquiries",
                    "description": "Answer salary questions"
                },
                {
                    "name": "Benefits Information",
                    "description": "Explain benefits packages"
                }
            ],
            "tags": ["hr", "salary", "benefits"]
        }
        
        async with session.post(
            "https://ledger.arcprotocol.ai/agents",
            json=agent_card,
            headers={"Authorization": f"Bearer {LEDGER_API_KEY}"}
        ) as response:
            result = await response.json()
            return result["agentId"]
```

## Step 2: Implement Dynamic Supervisor

### Supervisor with Ledger Query

```python
# supervisor_ledger.py
from arc import Server, Client
import aiohttp
import os

server = Server(server_id="supervisor-ledger")

LEDGER_ENDPOINT = "https://ledger.arcprotocol.ai"
LEDGER_API_KEY = os.getenv("LEDGER_API_KEY")

async def find_agent_by_keywords(keywords: list) -> dict:
    """Query ARC Ledger for agents matching keywords"""
    async with aiohttp.ClientSession() as session:
        # Search by tags
        params = {
            "tags": ",".join(keywords),
            "limit": 1
        }
        
        async with session.get(
            f"{LEDGER_ENDPOINT}/agents/search",
            params=params,
            headers={"Authorization": f"Bearer {LEDGER_API_KEY}"}
        ) as response:
            result = await response.json()
            
            if result.get("agents"):
                return result["agents"][0]  # Return best match
            
            return None

async def find_agent_by_text(query: str) -> dict:
    """Query ARC Ledger with text search"""
    async with aiohttp.ClientSession() as session:
        params = {"q": query, "limit": 1}
        
        async with session.get(
            f"{LEDGER_ENDPOINT}/agents/search",
            params=params,
            headers={"Authorization": f"Bearer {LEDGER_API_KEY}"}
        ) as response:
            result = await response.json()
            
            if result.get("agents"):
                return result["agents"][0]
            
            return None

@server.agent_handler("supervisor", "chat.start")
async def supervisor_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    # Extract keywords
    keywords = extract_keywords(message)
    
    # Query Ledger
    agent_info = await find_agent_by_keywords(keywords)
    
    if not agent_info:
        # Fallback: text search
        agent_info = await find_agent_by_text(message)
    
    if not agent_info:
        return {
            "type": "chat",
            "chat": {
                "chatId": params.get("chatId") or generate_id(),
                "status": "ACTIVE",
                "message": {
                    "role": "agent",
                    "parts": [{"type": "text", "content": "No suitable agent found"}]
                }
            }
        }
    
    # Create client for discovered agent
    agent_client = Client(agent_info["url"])
    
    # Extract agent ID from agent_info (if multiple agents on same server)
    # For simplicity, assume agent_info["name"] can be used as agent ID
    target_agent_id = agent_info.get("agentId", "default-agent")
    
    # Forward request
    response = await agent_client.chat.start(
        target_agent=target_agent_id,
        initial_message=params["initialMessage"],
        trace_id=context.trace_id
    )
    
    return response.result

@server.agent_handler("supervisor", "chat.message")
async def supervisor_message(params, context):
    # Retrieve session to maintain agent routing
    # For simplicity, re-route based on message
    message = params["message"]["parts"][0]["content"]
    
    keywords = extract_keywords(message)
    agent_info = await find_agent_by_keywords(keywords)
    
    if not agent_info:
        agent_info = await find_agent_by_text(message)
    
    if not agent_info:
        return {
            "type": "chat",
            "chat": {
                "chatId": params["chatId"],
                "status": "ACTIVE",
                "message": {
                    "role": "agent",
                    "parts": [{"type": "text", "content": "No suitable agent found"}]
                }
            }
        }
    
    agent_client = Client(agent_info["url"])
    target_agent_id = agent_info.get("agentId", "default-agent")
    
    response = await agent_client.chat.message(
        target_agent=target_agent_id,
        chat_id=params["chatId"],
        message=params["message"],
        trace_id=context.trace_id
    )
    
    return response.result

def extract_keywords(text: str) -> list:
    """Extract keywords from text"""
    text_lower = text.lower()
    
    keyword_map = {
        "finance": ["invoice", "payment", "budget", "expense"],
        "hr": ["salary", "benefits", "leave", "employee"],
        "support": ["help", "question", "issue"]
    }
    
    keywords = []
    for category, terms in keyword_map.items():
        if any(term in text_lower for term in terms):
            keywords.append(category)
    
    return keywords or ["support"]

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    print("Starting supervisor with ARC Ledger integration...")
    server.run(host="0.0.0.0", port=8000)
```

## Step 3: Test Dynamic Routing

```python
# test_ledger_supervisor.py
from arc import Client
import asyncio

async def test_ledger_supervisor():
    client = Client("http://localhost:8000/arc")
    
    # Test 1: Finance routing
    response = await client.chat.start(
        target_agent="supervisor",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "Help with invoice processing"}]
        }
    )
    print(f"Routed to Finance: {response.result['chat']['message']['parts'][0]['content']}")
    
    # Test 2: HR routing
    response = await client.chat.start(
        target_agent="supervisor",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "Question about salary"}]
        }
    )
    print(f"Routed to HR: {response.result['chat']['message']['parts'][0]['content']}")

asyncio.run(test_ledger_supervisor())
```

## Advanced: Capability-Based Routing

### Query by Capabilities

```python
async def find_agent_by_capabilities(capabilities: dict) -> dict:
    """Find agents with specific capabilities"""
    async with aiohttp.ClientSession() as session:
        payload = {
            "capabilities": capabilities,
            "limit": 1
        }
        
        async with session.post(
            f"{LEDGER_ENDPOINT}/agents/search",
            json=payload,
            headers={"Authorization": f"Bearer {LEDGER_API_KEY}"}
        ) as response:
            result = await response.json()
            
            if result.get("agents"):
                return result["agents"][0]
            
            return None

# Usage
@server.agent_handler("supervisor", "chat.start")
async def supervisor_start(params, context):
    # User requests file upload capability
    agent_info = await find_agent_by_capabilities({
        "fileUpload": True,
        "streaming": True
    })
    
    if agent_info:
        # Route to agent with file upload capability
        agent_client = Client(agent_info["url"])
        response = await agent_client.chat.start(...)
        return response.result
```

## Session Persistence

Store Ledger-discovered agent info in session:

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)

@server.agent_handler("supervisor", "chat.start")
async def supervisor_start(params, context):
    message = params["initialMessage"]["parts"][0]["content"]
    
    # Query Ledger
    agent_info = await find_agent_by_keywords(extract_keywords(message))
    
    # Store in session
    chat_id = params.get("chatId") or generate_id()
    redis_client.setex(
        f"session:{chat_id}",
        3600,
        json.dumps({
            "agent_url": agent_info["url"],
            "agent_id": agent_info["agentId"]
        })
    )
    
    # Forward request
    agent_client = Client(agent_info["url"])
    response = await agent_client.chat.start(...)
    
    # Return with supervisor's chat ID
    result = response.result
    result['chat']['chatId'] = chat_id
    return result

@server.agent_handler("supervisor", "chat.message")
async def supervisor_message(params, context):
    chat_id = params["chatId"]
    
    # Retrieve session
    session_data = redis_client.get(f"session:{chat_id}")
    if not session_data:
        raise Exception("Session not found")
    
    session = json.loads(session_data)
    
    # Forward to same agent
    agent_client = Client(session["agent_url"])
    response = await agent_client.chat.message(
        target_agent=session["agent_id"],
        chat_id=chat_id,
        message=params["message"],
        trace_id=context.trace_id
    )
    
    return response.result
```

## Benefits

1. **Dynamic Discovery** - No hardcoded agent URLs
2. **Runtime Flexibility** - Add/remove agents without code changes
3. **Capability Matching** - Route based on actual agent capabilities
4. **Centralized Registry** - Single source of truth for agents
5. **Version Management** - Ledger tracks agent versions

## Production Considerations

### 1. Cache Ledger Queries

```python
from functools import lru_cache
from datetime import datetime, timedelta

cache = {}
CACHE_TTL = 300  # 5 minutes

async def find_agent_cached(keywords: list) -> dict:
    cache_key = ",".join(sorted(keywords))
    
    if cache_key in cache:
        entry = cache[cache_key]
        if datetime.now() - entry["time"] < timedelta(seconds=CACHE_TTL):
            return entry["data"]
    
    # Query Ledger
    agent_info = await find_agent_by_keywords(keywords)
    
    # Cache result
    cache[cache_key] = {
        "data": agent_info,
        "time": datetime.now()
    }
    
    return agent_info
```

### 2. Handle Ledger Failures

```python
async def find_agent_with_fallback(keywords: list) -> dict:
    try:
        return await find_agent_by_keywords(keywords)
    except Exception as e:
        logger.error(f"Ledger query failed: {e}")
        
        # Fallback to hardcoded agents
        return get_default_agent(keywords)

def get_default_agent(keywords: list) -> dict:
    defaults = {
        "finance": {"url": "http://localhost:8001/arc", "agentId": "finance-agent"},
        "hr": {"url": "http://localhost:8002/arc", "agentId": "hr-agent"},
        "support": {"url": "http://localhost:8003/arc", "agentId": "support-agent"}
    }
    
    for keyword in keywords:
        if keyword in defaults:
            return defaults[keyword]
    
    return defaults["support"]
```

### 3. Monitor Ledger Latency

```python
import time

async def find_agent_with_metrics(keywords: list) -> dict:
    start = time.time()
    
    try:
        agent_info = await find_agent_by_keywords(keywords)
        duration = time.time() - start
        
        logger.info(f"Ledger query completed in {duration:.2f}s")
        
        return agent_info
    except Exception as e:
        duration = time.time() - start
        logger.error(f"Ledger query failed after {duration:.2f}s: {e}")
        raise
```

## Next Steps

- [Dynamic Prompts](./dynamic-prompts.md) - Capability-aware prompts
- [ARC Ledger Concepts](../../concepts/agent-discovery/arc-ledger.md) - Discovery details

