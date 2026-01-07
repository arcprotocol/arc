# ThreadManager

Client-side thread management for WebSocket sessions.

## Overview

ThreadManager automatically manages chat threads for WebSocket connections, handling chat.start vs chat.message routing and cleanup.

**Features:**
- Per-session in-memory storage
- Automatic chat.start vs chat.message selection
- Automatic cleanup on disconnect
- Thread reuse across multiple messages

## Initialization

```python
from arc import Client
from arc.client import ThreadManager

# Create per-WebSocket connection
arc_client = Client(endpoint="...", token="...")
thread_manager = ThreadManager(arc_client)
```

## Methods

### send_to_agent()

Send message to agent (automatically routes to chat.start or chat.message).

```python
# First message - calls chat.start
response = await thread_manager.send_to_agent(
    agent_id="support-agent",
    message={
        "role": "user",
        "parts": [{"type": "text", "content": "Help needed"}]
    },
    trace_id="trace-123"
)

# Second message - calls chat.message (reuses chat_id)
response = await thread_manager.send_to_agent(
    agent_id="support-agent",
    message={
        "role": "user",
        "parts": [{"type": "text", "content": "More info"}]
    }
)
```

**Parameters:**
- `agent_id` (str): Target agent ID
- `message` (dict): Message object
- `trace_id` (Optional[str]): Workflow trace ID
- `stream` (bool): Enable SSE streaming (default: False)

**Returns:** ARCResponse or SSE stream

### get_thread_id()

Get stored chat_id for agent.

```python
chat_id = thread_manager.get_thread_id("support-agent")
if chat_id:
    print(f"Active chat: {chat_id}")
```

### has_thread()

Check if thread exists for agent.

```python
if thread_manager.has_thread("support-agent"):
    print("Thread exists")
```

### end_chat()

End specific chat.

```python
await thread_manager.end_chat(
    agent_id="support-agent",
    reason="Issue resolved"
)
```

### end_all_chats()

End all active chats (call on disconnect).

```python
await thread_manager.end_all_chats()
```

### cleanup_all()

Alias for `end_all_chats()`.

```python
await thread_manager.cleanup_all()
```

### get_all_agents()

Get list of agents with active threads.

```python
agents = thread_manager.get_all_agents()
print(f"Active agents: {agents}")
```

## WebSocket Integration

### FastAPI WebSocket

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
            # Receive message
            data = await websocket.receive_json()
            
            # Route to agent (automatic chat.start vs chat.message)
            response = await thread_manager.send_to_agent(
                agent_id=data["agent_id"],
                message=data["message"],
                trace_id=data.get("trace_id")
            )
            
            # Send response
            await websocket.send_json(response.to_dict())
            
    except WebSocketDisconnect:
        # Cleanup on disconnect
        await thread_manager.end_all_chats()
    finally:
        await arc_client.close()
```

### Starlette WebSocket

```python
from starlette.applications import Starlette
from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.routing import WebSocketRoute
from arc import Client
from arc.client import ThreadManager

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    arc_client = Client(endpoint="https://api.example.com/arc", token="token")
    thread_manager = ThreadManager(arc_client)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            response = await thread_manager.send_to_agent(
                agent_id=data["agent_id"],
                message=data["message"]
            )
            
            await websocket.send_json(response.to_dict())
            
    except WebSocketDisconnect:
        await thread_manager.end_all_chats()
    finally:
        await arc_client.close()

app = Starlette(routes=[
    WebSocketRoute("/ws", websocket_endpoint)
])
```

## Streaming Integration

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    arc_client = Client(endpoint="...", token="...")
    thread_manager = ThreadManager(arc_client)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Stream response
            async for event in await thread_manager.send_to_agent(
                agent_id=data["agent_id"],
                message=data["message"],
                stream=True
            ):
                if event.event == "content":
                    await websocket.send_json({
                        "type": "content",
                        "data": event.data
                    })
                elif event.event == "done":
                    await websocket.send_json({
                        "type": "done",
                        "data": event.data
                    })
                    break
                elif event.event == "error":
                    await websocket.send_json({
                        "type": "error",
                        "data": event.data
                    })
                    break
                    
    except WebSocketDisconnect:
        await thread_manager.end_all_chats()
```

## Multi-Agent Example

Handle multiple agents in single WebSocket:

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    arc_client = Client(endpoint="...", token="...")
    thread_manager = ThreadManager(arc_client)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Route to different agents
            agent_id = data["agent_id"]  # "support", "finance", "hr", etc.
            
            response = await thread_manager.send_to_agent(
                agent_id=agent_id,
                message=data["message"]
            )
            
            await websocket.send_json({
                "agent_id": agent_id,
                "response": response.to_dict()
            })
            
    except WebSocketDisconnect:
        # End all chats with all agents
        await thread_manager.end_all_chats()
```

## Best Practices

### DO

1. **Create per WebSocket connection**
   ```python
   @app.websocket("/ws")
   async def handler(websocket):
       thread_manager = ThreadManager(arc_client)  # Per connection
   ```

2. **Always cleanup on disconnect**
   ```python
   except WebSocketDisconnect:
       await thread_manager.end_all_chats()
   ```

3. **Use trace IDs for debugging**
   ```python
   await thread_manager.send_to_agent(
       agent_id="...",
       message=...,
       trace_id=workflow_id
   )
   ```

### DON'T

1. **Don't share across users**
   ```python
   # Bad: Global ThreadManager
   global_thread_manager = ThreadManager(...)  # ❌
   ```

2. **Don't forget cleanup**
   ```python
   # Bad: No cleanup
   except WebSocketDisconnect:
       pass  # ❌ Leaves open chats
   ```

## Architecture

```
User → WebSocket → ThreadManager → ARCClient → Agent Server
                        ↓
                   {agent_id: chat_id}
```

ThreadManager maintains in-memory mapping of agent_id to chat_id for the duration of the WebSocket connection.

## Examples

- [ThreadManager Example](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/thread_manager_example.py)
- [Complete Client Test](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/arc_client_test.py)

