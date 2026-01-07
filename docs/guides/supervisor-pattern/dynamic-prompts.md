# Dynamic Prompts

Enhance agent prompts with capability information from ARC Ledger.

## Overview

Dynamic prompts adjust agent instructions based on capabilities fetched from ARC Ledger, enabling context-aware routing and better agent utilization.

## Why Dynamic Prompts

**Static Prompt:**
```
"You are a finance assistant."
```

**Dynamic Prompt:**
```
"You are a finance assistant with invoice processing and payment management capabilities.
Available skills: Invoice Processing, Payment Management, Budget Analysis."
```

Dynamic prompts provide agents with self-awareness and enable better decision-making.

## Basic Implementation

### Fetch Agent Capabilities

```python
# supervisor_dynamic.py
from arc import Server, Client
import aiohttp
import os

server = Server(server_id="supervisor-dynamic")

LEDGER_ENDPOINT = "https://ledger.arcprotocol.ai"
LEDGER_API_KEY = os.getenv("LEDGER_API_KEY")

async def get_agent_details(agent_id: str) -> dict:
    """Fetch agent details from Ledger"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{LEDGER_ENDPOINT}/agents/{agent_id}",
            headers={"Authorization": f"Bearer {LEDGER_API_KEY}"}
        ) as response:
            return await response.json()

async def build_enhanced_prompt(agent_id: str, user_message: str) -> str:
    """Build prompt with agent capabilities"""
    agent_details = await get_agent_details(agent_id)
    
    skills_list = ", ".join([skill["name"] for skill in agent_details.get("skills", [])])
    
    capabilities = agent_details.get("capabilities", {})
    capabilities_text = ", ".join([k for k, v in capabilities.items() if v])
    
    prompt = f"""You are {agent_details['name']}.

Description: {agent_details['description']}

Your skills: {skills_list}

Your capabilities: {capabilities_text}

User request: {user_message}

Provide assistance based on your skills and capabilities."""
    
    return prompt
```

### Supervisor with Dynamic Prompts

```python
@server.agent_handler("supervisor", "chat.start")
async def supervisor_start(params, context):
    user_message = params["initialMessage"]["parts"][0]["content"]
    
    # Find agent via Ledger
    agent_info = await find_agent_by_keywords(extract_keywords(user_message))
    
    if not agent_info:
        return error_response()
    
    # Build enhanced prompt
    enhanced_prompt = await build_enhanced_prompt(agent_info["agentId"], user_message)
    
    # Send enhanced message to agent
    enhanced_message = {
        "role": "system",
        "parts": [{"type": "text", "content": enhanced_prompt}]
    }
    
    agent_client = Client(agent_info["url"])
    
    # Send system message followed by user message
    response = await agent_client.chat.start(
        target_agent=agent_info["agentId"],
        initial_message=enhanced_message,
        trace_id=context.trace_id
    )
    
    return response.result

async def find_agent_by_keywords(keywords: list) -> dict:
    """Query ARC Ledger for agents"""
    async with aiohttp.ClientSession() as session:
        params = {"tags": ",".join(keywords), "limit": 1}
        
        async with session.get(
            f"{LEDGER_ENDPOINT}/agents/search",
            params=params,
            headers={"Authorization": f"Bearer {LEDGER_API_KEY}"}
        ) as response:
            result = await response.json()
            return result["agents"][0] if result.get("agents") else None

def extract_keywords(text: str) -> list:
    text_lower = text.lower()
    
    if any(kw in text_lower for kw in ["invoice", "payment"]):
        return ["finance"]
    elif any(kw in text_lower for kw in ["salary", "benefits"]):
        return ["hr"]
    else:
        return ["support"]

def error_response():
    return {
        "type": "chat",
        "chat": {
            "chatId": generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "No suitable agent found"}]
            }
        }
    }

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8000)
```

## Advanced: Capability-Aware Routing

### Route Based on Required Capabilities

```python
async def find_agent_with_capabilities(required_caps: dict) -> dict:
    """Find agent with specific capabilities"""
    async with aiohttp.ClientSession() as session:
        payload = {"capabilities": required_caps, "limit": 5}
        
        async with session.post(
            f"{LEDGER_ENDPOINT}/agents/search",
            json=payload,
            headers={"Authorization": f"Bearer {LEDGER_API_KEY}"}
        ) as response:
            result = await response.json()
            
            if result.get("agents"):
                return result["agents"][0]
            
            return None

@server.agent_handler("supervisor", "chat.start")
async def supervisor_start(params, context):
    user_message = params["initialMessage"]["parts"][0]["content"]
    
    # Determine required capabilities from message
    required_caps = analyze_required_capabilities(user_message)
    
    # Find agent with required capabilities
    agent_info = await find_agent_with_capabilities(required_caps)
    
    if not agent_info:
        return error_response()
    
    # Build capability-aware prompt
    prompt = await build_capability_prompt(agent_info, user_message, required_caps)
    
    # Forward with enhanced prompt
    agent_client = Client(agent_info["url"])
    response = await agent_client.chat.start(
        target_agent=agent_info["agentId"],
        initial_message={
            "role": "system",
            "parts": [{"type": "text", "content": prompt}]
        },
        trace_id=context.trace_id
    )
    
    return response.result

def analyze_required_capabilities(message: str) -> dict:
    """Analyze message to determine required capabilities"""
    message_lower = message.lower()
    
    caps = {}
    
    if "upload" in message_lower or "file" in message_lower:
        caps["fileUpload"] = True
    
    if "stream" in message_lower or "real-time" in message_lower:
        caps["streaming"] = True
    
    return caps

async def build_capability_prompt(agent_info: dict, user_message: str, required_caps: dict) -> str:
    """Build prompt highlighting required capabilities"""
    skills_list = ", ".join([skill["name"] for skill in agent_info.get("skills", [])])
    
    # Highlight matching capabilities
    matching_caps = [cap for cap in required_caps.keys() if agent_info.get("capabilities", {}).get(cap)]
    
    prompt = f"""You are {agent_info['name']}.

Your skills: {skills_list}

Required capabilities for this request: {', '.join(matching_caps)}

User request: {user_message}

Use your {', '.join(matching_caps)} capabilities to fulfill this request."""
    
    return prompt
```

## Multi-Agent Prompt Coordination

### Supervisor Coordinates Multiple Agents

```python
@server.agent_handler("supervisor", "chat.start")
async def supervisor_start(params, context):
    user_message = params["initialMessage"]["parts"][0]["content"]
    
    # Find multiple agents
    agents = await find_multiple_agents(user_message)
    
    if not agents:
        return error_response()
    
    # Build prompts for each agent
    prompts = []
    for agent in agents:
        prompt = await build_collaborative_prompt(agent, agents, user_message)
        prompts.append((agent, prompt))
    
    # Parallel agent calls
    import asyncio
    
    tasks = []
    for agent, prompt in prompts:
        client = Client(agent["url"])
        task = client.chat.start(
            target_agent=agent["agentId"],
            initial_message={
                "role": "system",
                "parts": [{"type": "text", "content": prompt}]
            },
            trace_id=context.trace_id
        )
        tasks.append(task)
    
    responses = await asyncio.gather(*tasks)
    
    # Aggregate responses
    aggregated = aggregate_responses(responses)
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": aggregated}]
            }
        }
    }

async def find_multiple_agents(message: str) -> list:
    """Find multiple relevant agents"""
    keywords = extract_keywords(message)
    
    async with aiohttp.ClientSession() as session:
        params = {"tags": ",".join(keywords), "limit": 3}
        
        async with session.get(
            f"{LEDGER_ENDPOINT}/agents/search",
            params=params,
            headers={"Authorization": f"Bearer {LEDGER_API_KEY}"}
        ) as response:
            result = await response.json()
            return result.get("agents", [])

async def build_collaborative_prompt(agent: dict, all_agents: list, user_message: str) -> str:
    """Build prompt for collaborative agent execution"""
    other_agents = [a["name"] for a in all_agents if a["agentId"] != agent["agentId"]]
    
    prompt = f"""You are {agent['name']}.

You are working with: {', '.join(other_agents)}

Your role: {agent['description']}

Your skills: {', '.join([s['name'] for s in agent.get('skills', [])])}

User request: {user_message}

Provide your specialized contribution to answer this request. Your response will be combined with others."""
    
    return prompt

def aggregate_responses(responses: list) -> str:
    """Aggregate multiple agent responses"""
    parts = []
    
    for i, response in enumerate(responses, 1):
        content = response.result['chat']['message']['parts'][0]['content']
        parts.append(f"Agent {i}: {content}")
    
    return "\n\n".join(parts)
```

## Caching Agent Capabilities

### Cache to Reduce Ledger Queries

```python
from datetime import datetime, timedelta

capability_cache = {}
CACHE_TTL = 600  # 10 minutes

async def get_agent_details_cached(agent_id: str) -> dict:
    """Fetch agent details with caching"""
    if agent_id in capability_cache:
        entry = capability_cache[agent_id]
        if datetime.now() - entry["time"] < timedelta(seconds=CACHE_TTL):
            return entry["data"]
    
    # Fetch from Ledger
    agent_details = await get_agent_details(agent_id)
    
    # Cache
    capability_cache[agent_id] = {
        "data": agent_details,
        "time": datetime.now()
    }
    
    return agent_details

async def build_enhanced_prompt(agent_id: str, user_message: str) -> str:
    """Build prompt using cached capabilities"""
    agent_details = await get_agent_details_cached(agent_id)
    
    # Build prompt as before
    skills_list = ", ".join([skill["name"] for skill in agent_details.get("skills", [])])
    
    prompt = f"""You are {agent_details['name']}.

Your skills: {skills_list}

User request: {user_message}"""
    
    return prompt
```

## Real-World Example

### Finance Supervisor with Dynamic Prompts

```python
@server.agent_handler("finance-supervisor", "chat.start")
async def finance_supervisor_start(params, context):
    user_message = params["initialMessage"]["parts"][0]["content"]
    
    # Determine task type
    if "invoice" in user_message.lower():
        required_caps = {"fileUpload": True}
        agent_info = await find_agent_with_capabilities(required_caps)
    elif "payment" in user_message.lower():
        required_caps = {"streaming": True}
        agent_info = await find_agent_with_capabilities(required_caps)
    else:
        agent_info = await find_agent_by_keywords(["finance"])
    
    if not agent_info:
        return error_response()
    
    # Build context-aware prompt
    agent_details = await get_agent_details(agent_info["agentId"])
    
    prompt = f"""You are {agent_details['name']} specializing in finance.

Available skills:
{format_skills(agent_details['skills'])}

User request: {user_message}

Provide detailed financial assistance using your specialized skills."""
    
    agent_client = Client(agent_info["url"])
    response = await agent_client.chat.start(
        target_agent=agent_info["agentId"],
        initial_message={
            "role": "system",
            "parts": [{"type": "text", "content": prompt}]
        },
        trace_id=context.trace_id
    )
    
    return response.result

def format_skills(skills: list) -> str:
    """Format skills for prompt"""
    return "\n".join([f"- {skill['name']}: {skill['description']}" for skill in skills])
```

## Benefits

1. **Context-Aware** - Agents understand their capabilities
2. **Self-Documenting** - Prompts include skill descriptions
3. **Adaptive** - Prompts adjust based on Ledger data
4. **Consistent** - Centralized capability definitions
5. **Scalable** - Add capabilities without code changes

## Best Practices

### 1. Cache Aggressively

Cache Ledger queries for 5-10 minutes to reduce latency.

### 2. Fallback Prompts

Have default prompts if Ledger is unavailable.

```python
DEFAULT_PROMPTS = {
    "finance-agent": "You are a finance assistant.",
    "hr-agent": "You are an HR assistant."
}

async def build_enhanced_prompt_with_fallback(agent_id: str, user_message: str) -> str:
    try:
        return await build_enhanced_prompt(agent_id, user_message)
    except Exception as e:
        logger.error(f"Failed to build dynamic prompt: {e}")
        return DEFAULT_PROMPTS.get(agent_id, "You are an assistant.")
```

### 3. Version Awareness

Include agent version in prompts for clarity.

```python
prompt = f"""You are {agent_details['name']} (version {agent_details['version']}).

Skills: {skills_list}

User request: {user_message}"""
```

## Next Steps

- [Agent Discovery Concepts](../../concepts/agent-discovery/) - Discovery patterns
- [ARC Ledger Integration](./arc-ledger-integration.md) - Ledger implementation

