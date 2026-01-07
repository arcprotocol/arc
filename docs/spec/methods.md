---
id: methods
title: Protocol Methods
sidebar_label: Methods
sidebar_position: 2
---

# Protocol Methods

Complete method reference for ARC Protocol.

## Task Methods

### task.create

Create a new asynchronous task.

**Request:**
```json
{
  "method": "task.create",
  "params": {
    "requestAgent": "client-123",
    "targetAgent": "document-analyzer",
    "traceId": "trace-abc",
    "initialMessage": {
      "role": "user",
      "parts": [{"type": "text", "content": "Analyze report"}]
    }
  }
}
```

**Response:**
```json
{
  "result": {
    "type": "task",
    "task": {
      "taskId": "task-xyz",
      "status": "PENDING",
      "message": {
        "role": "agent",
        "parts": [{"type": "text", "content": "Task created"}]
      }
    }
  }
}
```

### task.send

Send additional message to existing task.

### task.info

Get task status and message history.

### task.cancel

Cancel a running task.

### task.subscribe

Subscribe to task notifications via WebSocket.

### task.notification

Server-initiated notification for subscribed clients.

## Chat Methods

### chat.start

Begin a real-time conversation.

**Request:**
```json
{
  "method": "chat.start",
  "params": {
    "requestAgent": "client-123",
    "targetAgent": "support-agent",
    "traceId": "trace-abc",
    "initialMessage": {
      "role": "user",
      "parts": [{"type": "text", "content": "Need help"}]
    }
  }
}
```

**Response (SSE Stream):**
```
data: {"type":"chat","chat":{"chatId":"chat-xyz","status":"ACTIVE","message":{"role":"agent","parts":[{"type":"text","content":"How can I help?"}]}}}
```

### chat.message

Send follow-up message in active chat.

### chat.end

Terminate an active chat session.

## Full Specification

See the complete specification:
[ARC Specification Document](https://github.com/arcprotocol/arcprotocol/blob/main/spec/arc-specification.md)

