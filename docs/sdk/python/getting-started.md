# Getting Started

Quick start guide for the ARC Python SDK.

## Installation

### Core Package

```bash
pip install arc-sdk
```

### With Post-Quantum Cryptography

```bash
pip install arc-sdk[pqc]
```

Requires build tools (cmake, ninja). See [Quantum-Safe Guide](./advanced/quantum-safe.md) for details.

### Complete Installation

```bash
pip install arc-sdk[all,pqc]
```

Includes all features: FastAPI, Starlette, and post-quantum cryptography.

## Client Setup

### Basic Client

```python
from arc import Client

client = Client(
    endpoint="https://api.example.com/arc",
    token="your-oauth2-token"
)

# Create task
response = await client.task.create(
    target_agent="document-analyzer",
    initial_message={
        "role": "user",
        "parts": [{"type": "text", "content": "Analyze this report"}]
    }
)

print(response.result["task"]["taskId"])
```

### WebSocket Integration

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from arc import Client
from arc.client import ThreadManager

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Create per-connection instances
    arc_client = Client(endpoint="https://api.example.com/arc", token="token")
    thread_manager = ThreadManager(arc_client)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Automatic chat.start vs chat.message routing
            response = await thread_manager.send_to_agent(
                agent_id=data["agent_id"],
                message=data["message"]
            )
            
            await websocket.send_json(response.to_dict())
            
    except WebSocketDisconnect:
        await thread_manager.end_all_chats()
    finally:
        await arc_client.close()
```

## Server Setup

### Basic Server

```python
from arc import Server

server = Server(server_id="my-server")

@server.agent_handler("support-agent", "chat.start")
async def handle_chat_start(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "How can I help?"}]
            }
        }
    }

@server.agent_handler("support-agent", "chat.message")
async def handle_chat_message(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Response"}]
            }
        }
    }

# Run server
server.run(host="0.0.0.0", port=8000)
```

### With State Management

```python
from arc import Server
from arc.core.chat import ChatManager
from arc.server.storage import RedisChatStorage
import redis
import uuid

# Setup storage
redis_client = redis.Redis(host="localhost", port=6379)
storage = RedisChatStorage(redis_client)
chat_manager = ChatManager(agent_id="support-agent", storage=storage)

# Create server
server = Server(
    server_id="support-server",
    enable_chat_manager=True,
    chat_manager_agent_id="support-agent"
)

@server.agent_handler("support-agent", "chat.start")
async def handle_chat_start(params, context):
    chat_id = params.get("chatId") or f"chat-{uuid.uuid4().hex[:8]}"
    framework_thread_id = str(uuid.uuid4())
    
    # Store mapping
    await chat_manager.create_chat(
        target_agent=context["request_agent"],
        chat_id=chat_id,
        metadata={
            "framework": "custom",
            "framework_thread_id": framework_thread_id
        }
    )
    
    # Process with your framework
    response = process_message(params["initialMessage"], framework_thread_id)
    
    return {
        "type": "chat",
        "chat": {
            "chatId": chat_id,
            "status": "ACTIVE",
            "message": response
        }
    }

@server.agent_handler("support-agent", "chat.message")
async def handle_chat_message(params, context):
    # Retrieve mapping
    chat = await chat_manager.get_chat(params["chatId"])
    framework_thread_id = chat["metadata"]["framework_thread_id"]
    
    # Process with your framework
    response = process_message(params["message"], framework_thread_id)
    
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": response
        }
    }

server.run(host="0.0.0.0", port=8000)
```

## FastAPI Integration

```python
from fastapi import FastAPI
from arc.fastapi import create_arc_router

app = FastAPI()

# Create ARC router
arc_router = create_arc_router(server_id="my-server")

@arc_router.agent_handler("my-agent", "chat.start")
async def handle_chat(params, context):
    return {"type": "chat", "chat": {...}}

# Mount router
app.include_router(arc_router, prefix="/arc")

# Run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Common Patterns

### Task Operations

```python
# Create task
task = await client.task.create(
    target_agent="analyzer",
    initial_message=message,
    priority="HIGH"
)

# Check status
status = await client.task.info(
    target_agent="analyzer",
    task_id=task.result["task"]["taskId"]
)

# Cancel task
await client.task.cancel(
    target_agent="analyzer",
    task_id=task_id,
    reason="User cancelled"
)
```

### Chat Operations

```python
# Start chat
chat = await client.chat.start(
    target_agent="support",
    initial_message=message
)

# Send message
response = await client.chat.message(
    target_agent="support",
    chat_id=chat.result["chat"]["chatId"],
    message=message
)

# End chat
await client.chat.end(
    target_agent="support",
    chat_id=chat_id,
    reason="Issue resolved"
)
```

### Error Handling

```python
from arc.exceptions import (
    ARCException,
    TaskNotFoundError,
    ChatNotFoundError,
    AgentNotFoundError
)

try:
    response = await client.task.create(...)
except TaskNotFoundError as e:
    print(f"Task not found: {e.code}")
except AgentNotFoundError as e:
    print(f"Agent not found: {e.code}")
except ARCException as e:
    print(f"ARC error: {e.code} - {e.message}")
```

## Next Steps

- [Client Documentation](./client/index.md) - Detailed client API
- [Server Documentation](./server/index.md) - Server setup and configuration
- [State Management](./state-management/index.md) - Session management patterns
- [Examples](https://github.com/arcprotocol/python-sdk/tree/main/examples) - Complete examples

## Resources

- **GitHub**: [arcprotocol/python-sdk](https://github.com/arcprotocol/python-sdk)
- **PyPI**: [arc-sdk](https://pypi.org/project/arc-sdk/)
- **Specification**: [ARC Protocol](../../../spec/arc-specification.md)

