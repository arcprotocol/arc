# Client

ARCClient for ARC Protocol communication.

## Overview

ARCClient provides HTTP client functionality for ARC Protocol requests.

**Features:**
- Task and chat method operations
- OAuth2 Bearer token authentication
- Quantum-safe hybrid TLS (optional)
- SSE streaming support
- Workflow tracing via `trace_id`
- Automatic error handling

## Initialization

```python
from arc import Client

# Standard configuration
client = Client(
    endpoint="https://api.example.com/arc",
    token="your-oauth2-token",
    request_agent="my-client-id"
)

# Quantum-safe TLS (default)
client = Client(
    endpoint="https://api.example.com/arc",
    token="your-oauth2-token",
    use_quantum_safe=True
)

# Disable quantum-safe TLS
client = Client(
    endpoint="https://api.example.com/arc",
    token="your-oauth2-token",
    use_quantum_safe=False
)
```

### Parameters

- `endpoint` (str): ARC endpoint URL
- `token` (Optional[str]): OAuth2 Bearer token
- `request_agent` (Optional[str]): Client agent ID (auto-generated if not provided)
- `timeout` (float): Request timeout in seconds (default: 60.0)
- `verify_ssl` (bool): Verify SSL certificates (default: True)
- `ssl_context` (Optional[ssl.SSLContext]): Custom SSL context
- `use_quantum_safe` (bool): Enable quantum-safe hybrid TLS (default: True)
- `hybrid_tls_config` (Optional[HybridTLSConfig]): Quantum-safe TLS configuration

## Documentation

- [Task Methods](./task-methods.md) - Asynchronous task operations
- [Chat Methods](./chat-methods.md) - Real-time chat operations
- [ThreadManager](./thread-manager.md) - WebSocket session management
- [Responses & Errors](./responses-errors.md) - Response handling and error management

## Quick Examples

### Task Operations

```python
# Create task
response = await client.task.create(
    target_agent="document-analyzer",
    initial_message={
        "role": "user",
        "parts": [{"type": "text", "content": "Analyze report"}]
    }
)

task_id = response.result["task"]["taskId"]
```

### Chat Operations

```python
# Start chat
response = await client.chat.start(
    target_agent="support-agent",
    initial_message={
        "role": "user",
        "parts": [{"type": "text", "content": "Need help"}]
    }
)

chat_id = response.result["chat"]["chatId"]
```

### Streaming

```python
# Stream chat response
async for event in await client.chat.start(
    target_agent="support-agent",
    initial_message=message,
    stream=True
):
    if event.event == "content":
        print(event.data, end="", flush=True)
    elif event.event == "done":
        break
```

## Client Lifecycle

### Close Connection

```python
await client.close()
```

### Context Manager

```python
async with Client(endpoint="...", token="...") as client:
    response = await client.task.create(...)
```

## Examples

- [Client Examples](https://github.com/arcprotocol/python-sdk/tree/main/examples/client)
- [WebSocket Integration](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/thread_manager_example.py)

