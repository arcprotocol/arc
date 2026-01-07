# Distributed Deployment

Deploy agents across multiple servers for independent scaling.

## Architecture

```
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  Finance       │  │     HR         │  │   Support      │
│  Server        │  │   Server       │  │   Server       │
│  :8001         │  │   :8002        │  │   :8003        │
│                │  │                │  │                │
│ finance-agent  │  │  hr-agent      │  │ support-agent  │
└────────────────┘  └────────────────┘  └────────────────┘
```

## Step 1: Create Server Files

### finance_server.py

```python
from arc import Server

server = Server(server_id="finance-server")

@server.agent_handler("finance-agent", "chat.start")
async def handle_start(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Finance agent ready"}]
            }
        }
    }

@server.agent_handler("finance-agent", "chat.message")
async def handle_message(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Processing request"}]
            }
        }
    }

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8001)
```

### hr_server.py

```python
from arc import Server

server = Server(server_id="hr-server")

@server.agent_handler("hr-agent", "chat.start")
async def handle_start(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "HR agent ready"}]
            }
        }
    }

@server.agent_handler("hr-agent", "chat.message")
async def handle_message(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params["chatId"],
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Processing HR query"}]
            }
        }
    }

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8002)
```

### support_server.py

```python
from arc import Server

server = Server(server_id="support-server")

@server.agent_handler("support-agent", "chat.start")
async def handle_start(params, context):
    return {
        "type": "chat",
        "chat": {
            "chatId": params.get("chatId") or generate_id(),
            "status": "ACTIVE",
            "message": {
                "role": "agent",
                "parts": [{"type": "text", "content": "Support agent ready"}]
            }
        }
    }

@server.agent_handler("support-agent", "chat.message")
async def handle_message(params, context):
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

def generate_id():
    import uuid
    return f"chat-{uuid.uuid4().hex[:8]}"

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8003)
```

## Step 2: Run Servers

```bash
# Terminal 1
python finance_server.py

# Terminal 2
python hr_server.py

# Terminal 3
python support_server.py
```

## Step 3: Test Distributed System

```python
# test_distributed.py
from arc import Client
import asyncio

async def test_distributed():
    # Each agent on different server
    finance_client = Client("http://localhost:8001/arc")
    hr_client = Client("http://localhost:8002/arc")
    support_client = Client("http://localhost:8003/arc")
    
    # Test finance
    finance_response = await finance_client.chat.start(
        target_agent="finance-agent",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "Invoice help"}]
        }
    )
    print(f"Finance: {finance_response.result['chat']['message']['parts'][0]['content']}")
    
    # Test HR
    hr_response = await hr_client.chat.start(
        target_agent="hr-agent",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "Salary question"}]
        }
    )
    print(f"HR: {hr_response.result['chat']['message']['parts'][0]['content']}")
    
    # Test support
    support_response = await support_client.chat.start(
        target_agent="support-agent",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "Need help"}]
        }
    )
    print(f"Support: {support_response.result['chat']['message']['parts'][0]['content']}")

asyncio.run(test_distributed())
```

## Production Deployment

### With Docker

```dockerfile
# Dockerfile.finance
FROM python:3.11-slim
WORKDIR /app
COPY finance_server.py .
RUN pip install arc-sdk
CMD ["python", "finance_server.py"]
```

```dockerfile
# Dockerfile.hr
FROM python:3.11-slim
WORKDIR /app
COPY hr_server.py .
RUN pip install arc-sdk
CMD ["python", "hr_server.py"]
```

```dockerfile
# Dockerfile.support
FROM python:3.11-slim
WORKDIR /app
COPY support_server.py .
RUN pip install arc-sdk
CMD ["python", "support_server.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  finance:
    build:
      context: .
      dockerfile: Dockerfile.finance
    ports:
      - "8001:8001"
    environment:
      - SERVER_ID=finance-server

  hr:
    build:
      context: .
      dockerfile: Dockerfile.hr
    ports:
      - "8002:8002"
    environment:
      - SERVER_ID=hr-server

  support:
    build:
      context: .
      dockerfile: Dockerfile.support
    ports:
      - "8003:8003"
    environment:
      - SERVER_ID=support-server
```

Run: `docker-compose up`

## Load Balancing

### Nginx Configuration

```nginx
upstream finance_backend {
    server localhost:8001;
    server localhost:8011;  # Scaled instance
}

upstream hr_backend {
    server localhost:8002;
}

upstream support_backend {
    server localhost:8003;
}

server {
    listen 80;
    
    location /arc/finance {
        proxy_pass http://finance_backend/arc;
    }
    
    location /arc/hr {
        proxy_pass http://hr_backend/arc;
    }
    
    location /arc/support {
        proxy_pass http://support_backend/arc;
    }
}
```

## Scaling Individual Agents

Scale finance agent to 3 instances:

```yaml
# docker-compose.yml
services:
  finance:
    build:
      context: .
      dockerfile: Dockerfile.finance
    ports:
      - "8001-8003:8001"
    deploy:
      replicas: 3
```

## Advantages

1. **Independent Scaling** - Scale each agent separately
2. **Fault Isolation** - Failure isolated to one agent
3. **Resource Isolation** - No resource contention
4. **Technology Flexibility** - Different tech stacks per agent

## Limitations

1. **Network Overhead** - HTTP calls between agents
2. **Complex Deployment** - Multiple services to manage
3. **Distributed Monitoring** - Logs across multiple servers

## When to Use

Use distributed deployment when:
- Production environment
- Different scaling needs per agent
- Fault isolation required
- High availability needed

## Next Steps

- [Agent Communication](./agent-communication.md) - Cross-server agent calls
- [Supervisor Pattern](../supervisor-pattern/) - Centralized routing

