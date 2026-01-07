# Python SDK

Official Python implementation of the ARC Protocol.

## Installation

```bash
pip install arc-sdk              # Core
pip install arc-sdk[pqc]         # + Post-Quantum Cryptography
pip install arc-sdk[fastapi]     # + FastAPI integration
pip install arc-sdk[starlette]   # + Starlette integration
pip install arc-sdk[all]         # All integrations (excludes PQC)
pip install arc-sdk[all,pqc]     # Complete installation
```

## Quick Links

- [Getting Started](./getting-started.md) - Quick start guide
- [Client Documentation](./client/) - ARCClient and ThreadManager
- [Server Documentation](./server/) - ARCServer and agent handlers
- [State Management](./state-management/) - ChatManager and storage
- [Integrations](./integrations/) - FastAPI and Starlette
- [Quantum-Safe TLS](./quantum/) - Post-quantum cryptography
- [Streaming](./streaming/) - Server-Sent Events patterns

## Documentation Structure

### [Client](./client/index.md)

Client-side ARC Protocol communication.

- [Task Methods](./client/task-methods.md) - Asynchronous task operations
- [Chat Methods](./client/chat-methods.md) - Real-time chat operations
- [ThreadManager](./client/thread-manager.md) - WebSocket session management
- [Responses & Errors](./client/responses-errors.md) - Response handling and error management

### [Server](./server/index.md)

Server-side ARC Protocol handling.

- [Agent Handlers](./server/agent-handlers.md) - Agent registration and routing
- [Authentication](./server/authentication.md) - OAuth2 and JWT validation
- [Middleware](./server/middleware.md) - Custom middleware and health checks

### [State Management](./state-management/index.md)

Server-side state and session management.

- [ChatManager](./state-management/chat-manager.md) - Chat session mapping
- [Storage Backends](./state-management/storage.md) - Redis, PostgreSQL, MongoDB
- [Framework Integration](./state-management/frameworks.md) - LangChain, LlamaIndex

### [Integrations](./integrations/)

Framework integrations for ARC servers.

- [FastAPI](./integrations/fastapi.md) - FastAPI integration
- [Starlette](./integrations/starlette.md) - Starlette integration

### [Quantum-Safe TLS](./quantum/)

Post-quantum cryptography with hybrid TLS.

- [Hybrid TLS](./quantum/hybrid-tls.md) - X25519 + Kyber-768 implementation
- [Installation](./quantum/installation.md) - Build requirements and setup

### [Streaming](./streaming/)

Server-Sent Events patterns.

- [SSE Streaming](./streaming/sse.md) - Real-time streaming implementation
- [Client Streaming](./streaming/client.md) - Client-side streaming consumption
- [Server Streaming](./streaming/server.md) - Server-side streaming generation

## Core Components

### ARCClient

HTTP client for ARC Protocol requests.

```python
from arc import Client

client = Client("https://api.example.com/arc", token="your-token")
task = await client.task.create(target_agent="analyzer", initial_message={...})
```

### ARCServer

FastAPI-based server for handling ARC requests.

```python
from arc import Server

server = Server(server_id="my-server")

@server.agent_handler("my-agent", "chat.start")
async def handle_chat(params, context):
    return {"type": "chat", "chat": {...}}
```

### ChatManager

Maps ARC `chat_id` to framework `thread_id`.

```python
from arc.core.chat import ChatManager

chat_manager = ChatManager(agent_id="my-agent", storage=storage)
await chat_manager.create_chat(chat_id="chat-123", metadata={...})
```

### ThreadManager

Client-side thread management for WebSocket sessions.

```python
from arc.client import ThreadManager

thread_manager = ThreadManager(arc_client)
response = await thread_manager.send_to_agent("agent-id", message)
```

## Features

- Full ARC Protocol implementation
- Quantum-safe hybrid TLS (X25519 + Kyber-768)
- FastAPI and Starlette integration
- OAuth2 authentication with scope validation
- SSE streaming support
- Multi-agent routing
- Workflow tracing
- Persistent session storage (Redis, PostgreSQL, MongoDB)

## Examples

- [Python SDK Examples](https://github.com/arcprotocol/python-sdk/tree/main/examples)
- [Protocol Examples](../../../examples/python)

## Links

- **GitHub**: [arcprotocol/python-sdk](https://github.com/arcprotocol/python-sdk)
- **PyPI**: [arc-sdk](https://pypi.org/project/arc-sdk/)
- **Specification**: [ARC Protocol](../../../spec/arc-specification.md)
