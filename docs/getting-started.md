# Getting Started with ARC Protocol

Welcome to the **Agent Remote Communication (ARC) Protocol**! This guide will help you understand and implement ARC in your multi-agent system.

---

## 📋 Table of Contents

1. [What is ARC Protocol?](#what-is-arc-protocol)
2. [Core Concepts](#core-concepts)
3. [Quick Example](#quick-example)
4. [Protocol Structure](#protocol-structure)
5. [Implementing a Client](#implementing-a-client)
6. [Implementing a Server](#implementing-a-server)
7. [Next Steps](#next-steps)

---

## What is ARC Protocol?

**ARC (Agent Remote Communication)** is a communication protocol designed for multi-agent systems. It enables:

- **🎯 Single Endpoint Architecture** - Deploy multiple agents behind one URL
- **🔀 Agent-Level Routing** - Route requests to specific agents using `targetAgent`
- **📊 Workflow Tracing** - Track multi-agent workflows with `traceId`
- **⚡ Real-time Streaming** - SSE support for chat responses
- **🔒 Quantum-Safe Security** - Hybrid TLS with post-quantum cryptography

---

## Core Concepts

### 1. **Request/Response Structure**

Every ARC request follows this format:

```json
{
  "arc": "1.0",
  "id": "req_123",
  "method": "chat.start",
  "requestAgent": "agent-a",
  "targetAgent": "agent-b",
  "params": { ... },
  "traceId": "workflow_abc"
}
```

Every ARC response:

```json
{
  "arc": "1.0",
  "id": "req_123",
  "responseAgent": "agent-b",
  "targetAgent": "agent-a",
  "result": { ... },
  "error": null,
  "traceId": "workflow_abc"
}
```

### 2. **Methods**

ARC has two main method categories:

#### **Task Methods** (Asynchronous)
For long-running operations:
- `task.create` - Create a new task
- `task.send` - Send additional data
- `task.info` - Get task status
- `task.cancel` - Cancel task

#### **Chat Methods** (Real-time)
For interactive conversations:
- `chat.start` - Begin a chat
- `chat.message` - Send message
- `chat.end` - End chat

### 3. **Agent Routing**

Route to specific agents using the `targetAgent` field:

```json
{
  "targetAgent": "finance-agent",  // Route to finance agent
  "method": "task.create",
  ...
}
```

Multiple agents can run on the same server endpoint!

---

## Quick Example

### Creating a Task

**Request:**
```json
POST /arc HTTP/1.1
Host: api.company.com
Content-Type: application/arc+json

{
  "arc": "1.0",
  "id": "req_001",
  "method": "task.create",
  "requestAgent": "user-interface",
  "targetAgent": "document-analyzer",
  "params": {
    "initialMessage": {
      "role": "user",
      "parts": [
        {
          "type": "TextPart",
          "content": "Analyze this quarterly report"
        }
      ]
    },
    "priority": "HIGH"
  }
}
```

**Response:**
```json
{
  "arc": "1.0",
  "id": "req_001",
  "responseAgent": "document-analyzer",
  "targetAgent": "user-interface",
  "result": {
    "type": "task",
    "task": {
      "taskId": "task-12345",
      "status": "SUBMITTED",
      "createdAt": "2024-01-15T10:30:00Z"
    }
  },
  "error": null
}
```

---

## Protocol Structure

### Message Parts

ARC supports multiple content types in messages:

```json
{
  "role": "user",
  "parts": [
    {
      "type": "TextPart",
      "content": "Hello world"
    },
    {
      "type": "FilePart",
      "content": "base64...",
      "mimeType": "application/pdf",
      "filename": "report.pdf"
    },
    {
      "type": "ImagePart",
      "content": "base64...",
      "mimeType": "image/jpeg",
      "width": 1920,
      "height": 1080
    }
  ]
}
```

### Error Handling

Errors follow a structured format:

```json
{
  "arc": "1.0",
  "id": "req_001",
  "responseAgent": "server",
  "targetAgent": "client",
  "result": null,
  "error": {
    "code": -41001,
    "message": "Agent not found: unknown-agent",
    "details": {
      "agentId": "unknown-agent",
      "availableAgents": ["agent-a", "agent-b"]
    }
  }
}
```

**Common Error Codes:**
- `-32600` - Invalid request
- `-32601` - Method not found
- `-41001` - Agent not found
- `-42001` - Task not found
- `-43001` - Chat not found
- `-44001` - Authentication failed

---

## Implementing a Client

### Python SDK Example

```python
from arc import Client

# Initialize client
client = Client(
    "https://api.company.com/arc",
    token="your-oauth2-token"
)

# Create a task
task = await client.task.create(
    target_agent="document-analyzer",
    initial_message={
        "role": "user",
        "parts": [{"type": "TextPart", "content": "Analyze report"}]
    },
    priority="HIGH"
)

print(f"Task created: {task['result']['task']['taskId']}")

# Start a chat
chat = await client.chat.start(
    target_agent="support-agent",
    initial_message={
        "role": "user",
        "parts": [{"type": "TextPart", "content": "Help me"}]
    }
)

print(f"Chat started: {chat['result']['chat']['chatId']}")
```

### Raw HTTP Example

```python
import requests

url = "https://api.company.com/arc"
headers = {
    "Content-Type": "application/arc+json",
    "Authorization": "Bearer your-token"
}

request = {
    "arc": "1.0",
    "id": "req_001",
    "method": "task.create",
    "requestAgent": "my-client",
    "targetAgent": "document-analyzer",
    "params": {
        "initialMessage": {
            "role": "user",
            "parts": [{"type": "TextPart", "content": "Analyze report"}]
        }
    }
}

response = requests.post(url, json=request, headers=headers)
print(response.json())
```

---

## Implementing a Server

### Python SDK Example

```python
from arc import Server

# Create server
server = Server(server_id="my-server")

# Register agent handler
@server.agent_handler("finance-agent", "task.create")
async def handle_finance_task(params, context):
    initial_msg = params["initialMessage"]
    
    # Your agent logic here
    task_id = "task-123"
    
    return {
        "type": "task",
        "task": {
            "taskId": task_id,
            "status": "SUBMITTED",
            "createdAt": "2024-01-15T10:30:00Z"
        }
    }

# Register chat handler
@server.agent_handler("support-agent", "chat.start")
async def handle_support_chat(params, context):
    initial_msg = params["initialMessage"]
    
    # Your chat logic here
    response_msg = {
        "role": "agent",
        "parts": [{"type": "TextPart", "content": "How can I help?"}]
    }
    
    return {
        "type": "chat",
        "chat": {
            "chatId": "chat-456",
            "status": "ACTIVE",
            "message": response_msg
        }
    }

# Run server
server.run(host="0.0.0.0", port=8000)
```

---

## Next Steps

### 📚 Learn More

1. **[Complete Specification](../spec/arc-specification.md)** - Full protocol details
2. **[Best Practices](concepts/best-practices.md)** - Implementation guidelines
3. **[SDK Documentation](sdk/)** - Language-specific guides

### 🔧 Explore Features

1. **Workflow Tracing** - Track multi-agent workflows with `traceId`
2. **Streaming Responses** - Use SSE for real-time chat
3. **Quantum-Safe Security** - Enable hybrid TLS encryption

### 🤝 Get Involved

1. **[GitHub Repository](https://github.com/arcprotocol/arcprotocol)** - View source code
2. **[Contributing Guidelines](../CONTRIBUTING.md)** - Contribute to the project
3. **[Issue Tracker](https://github.com/arcprotocol/arcprotocol/issues)** - Report bugs or request features

---

## 📖 Additional Resources

- [Python SDK](https://github.com/arcprotocol/python-sdk) - Python implementation
- [ARC Compass](https://github.com/arcprotocol/arccompass) - Agent discovery
- [ARC Ledger](https://github.com/arcprotocol/arcledger) - Agent registry

---

**Need Help?** 
- Check the [full documentation](index.md)
- Open an [issue](https://github.com/arcprotocol/arcprotocol/issues)
- Review [examples](../examples/)

---

**Ready to build?** Start implementing your first ARC agent! 🚀

