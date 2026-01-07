# Chat Methods

Real-time chat operations for interactive conversations.

## chat.start()

Start new chat session.

```python
response = await client.chat.start(
    target_agent="support-agent",
    initial_message={
        "role": "user",
        "parts": [{"type": "text", "content": "I need help with my account"}]
    },
    chat_id="chat-abc123",  # Optional, server generates if not provided
    stream=False,
    metadata={"user_id": "user-123", "priority": "high"}
)

chat_id = response.result["chat"]["chatId"]
agent_message = response.result["chat"]["message"]
```

**Parameters:**
- `target_agent` (str): Target agent ID
- `initial_message` (dict): Initial message object
- `chat_id` (Optional[str]): Client-provided chat ID
- `stream` (bool): Enable SSE streaming (default: False)
- `metadata` (Optional[dict]): Custom chat metadata
- `trace_id` (Optional[str]): Workflow trace ID

**Returns:** ARCResponse with chat object (or SSE stream if stream=True)

**Chat Object:**
```python
{
    "chatId": "chat-abc123",
    "status": "ACTIVE",  # or PAUSED, CLOSED
    "message": {
        "role": "agent",
        "parts": [{"type": "text", "content": "How can I help?"}],
        "timestamp": "2025-01-06T00:00:00Z"
    },
    "participants": ["user-agent", "support-agent"],
    "createdAt": "2025-01-06T00:00:00Z"
}
```

## chat.message()

Send message to active chat.

```python
response = await client.chat.message(
    target_agent="support-agent",
    chat_id="chat-abc123",
    message={
        "role": "user",
        "parts": [{"type": "text", "content": "My account is locked"}]
    },
    stream=False
)

agent_message = response.result["chat"]["message"]
```

**Parameters:**
- `target_agent` (str): Target agent ID
- `chat_id` (str): Chat identifier
- `message` (dict): Message object
- `stream` (bool): Enable SSE streaming (default: False)
- `trace_id` (Optional[str]): Workflow trace ID

**Returns:** ARCResponse with chat object (or SSE stream if stream=True)

## chat.end()

End active chat session.

```python
response = await client.chat.end(
    target_agent="support-agent",
    chat_id="chat-abc123",
    reason="Issue resolved"
)

status = response.result["chat"]["status"]  # CLOSED
closed_at = response.result["chat"]["closedAt"]
```

**Parameters:**
- `target_agent` (str): Target agent ID
- `chat_id` (str): Chat identifier
- `reason` (Optional[str]): Closure reason
- `trace_id` (Optional[str]): Workflow trace ID

**Returns:** ARCResponse with updated chat object

## Streaming

Enable real-time streaming with SSE:

```python
# Start chat with streaming
async for event in await client.chat.start(
    target_agent="support-agent",
    initial_message=message,
    stream=True
):
    if event.event == "content":
        print(event.data, end="", flush=True)
    elif event.event == "metadata":
        print(f"\nMetadata: {event.data}")
    elif event.event == "error":
        print(f"\nError: {event.data}")
        break
    elif event.event == "done":
        print("\nDone")
        break

# Send message with streaming
async for event in await client.chat.message(
    target_agent="support-agent",
    chat_id=chat_id,
    message=message,
    stream=True
):
    if event.event == "content":
        print(event.data, end="", flush=True)
    elif event.event == "done":
        break
```

**Event Types:**
- `content` - Incremental content chunk
- `metadata` - Response metadata
- `error` - Error occurred
- `done` - Stream complete

## Chat Workflow Example

Complete chat lifecycle:

```python
from arc import Client

client = Client(endpoint="...", token="...")

# 1. Start chat
start_response = await client.chat.start(
    target_agent="support-agent",
    initial_message={
        "role": "user",
        "parts": [{"type": "text", "content": "I need help"}]
    }
)

chat_id = start_response.result["chat"]["chatId"]
print(f"Agent: {start_response.result['chat']['message']['parts'][0]['content']}")

# 2. Continue conversation
messages = [
    "My account is locked",
    "I forgot my password",
    "Can you reset it?"
]

for msg in messages:
    response = await client.chat.message(
        target_agent="support-agent",
        chat_id=chat_id,
        message={
            "role": "user",
            "parts": [{"type": "text", "content": msg}]
        }
    )
    
    agent_response = response.result["chat"]["message"]["parts"][0]["content"]
    print(f"User: {msg}")
    print(f"Agent: {agent_response}")

# 3. End chat
end_response = await client.chat.end(
    target_agent="support-agent",
    chat_id=chat_id,
    reason="Issue resolved"
)

print(f"Chat ended: {end_response.result['chat']['closedAt']}")
```

## Streaming Example

Real-time streaming chat:

```python
import asyncio

async def stream_chat():
    client = Client(endpoint="...", token="...")
    
    # Start chat with streaming
    print("Starting chat...")
    chat_id = None
    
    async for event in await client.chat.start(
        target_agent="support-agent",
        initial_message={
            "role": "user",
            "parts": [{"type": "text", "content": "Tell me a story"}]
        },
        stream=True
    ):
        if event.event == "content":
            print(event.data, end="", flush=True)
        elif event.event == "done":
            # Extract chat_id from final event
            chat_id = event.data["chat"]["chatId"]
            print(f"\n\nChat ID: {chat_id}")
            break
    
    # Continue with streaming messages
    await asyncio.sleep(1)
    
    print("\n\nSending follow-up...")
    async for event in await client.chat.message(
        target_agent="support-agent",
        chat_id=chat_id,
        message={
            "role": "user",
            "parts": [{"type": "text", "content": "Tell me more"}]
        },
        stream=True
    ):
        if event.event == "content":
            print(event.data, end="", flush=True)
        elif event.event == "done":
            print("\n\nDone")
            break
    
    # End chat
    await client.chat.end(
        target_agent="support-agent",
        chat_id=chat_id,
        reason="Story complete"
    )

asyncio.run(stream_chat())
```

## Error Handling

```python
from arc.exceptions import (
    ChatNotFoundError,
    ChatAlreadyClosedError,
    InvalidChatMessageError,
    ChatBufferOverflowError
)

try:
    response = await client.chat.message(
        target_agent="support-agent",
        chat_id="chat-123",
        message=message
    )
except ChatNotFoundError as e:
    print(f"Chat not found: {e.code}")
except ChatAlreadyClosedError as e:
    print(f"Chat closed: {e.code}")
except InvalidChatMessageError as e:
    print(f"Invalid message: {e.message}")
```

## Chat States

```
chat.start → ACTIVE
              ↓
         chat.message (ACTIVE)
              ↓
           chat.end → CLOSED
```

Once CLOSED, chat cannot be resumed. Start new chat if needed.

## Message Parts

Messages support multiple content types:

```python
# Text
{"type": "text", "content": "Hello"}

# Data
{"type": "data", "content": "{\"key\": \"value\"}", "mimeType": "application/json"}

# File
{"type": "file", "content": "base64...", "mimeType": "application/pdf", "filename": "doc.pdf"}

# Image
{"type": "image", "content": "base64...", "mimeType": "image/png", "width": 800, "height": 600}

# Audio
{"type": "audio", "content": "base64...", "mimeType": "audio/mp3", "duration": 120.5}

# Multiple parts
{
    "role": "user",
    "parts": [
        {"type": "text", "content": "Here's the image:"},
        {"type": "image", "content": "base64...", "mimeType": "image/png"}
    ]
}
```

## Examples

- [Chat Start](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/test_chat_start.py)
- [Chat Message](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/test_chat_message.py)
- [Chat End](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/test_chat_end.py)
- [Complete Client Test](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/arc_client_test.py)

