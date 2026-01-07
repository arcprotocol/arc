---
id: types
title: Protocol Types
sidebar_label: Types
sidebar_position: 3
---

# Protocol Types

Type definitions for ARC Protocol.

## Message

```typescript
interface Message {
  role: "user" | "agent";
  parts: MessagePart[];
}
```

## MessagePart

```typescript
interface TextPart {
  type: "text";
  content: string;
}

interface ToolCallPart {
  type: "tool_call";
  toolCallId: string;
  name: string;
  parameters: Record<string, any>;
}

interface ToolResultPart {
  type: "tool_result";
  toolCallId: string;
  result: any;
}

type MessagePart = TextPart | ToolCallPart | ToolResultPart;
```

## Task

```typescript
interface Task {
  taskId: string;
  status: "PENDING" | "IN_PROGRESS" | "COMPLETED" | "FAILED" | "CANCELLED";
  message?: Message;
}
```

## Chat

```typescript
interface Chat {
  chatId: string;
  status: "ACTIVE" | "ENDED";
  message: Message;
}
```

## Full Schemas

View complete type definitions:
- [OpenRPC Schema](https://github.com/arcprotocol/arcprotocol/blob/main/spec/versions/v1.0/arc-openrpc.json)
- [OpenAPI Schema](https://github.com/arcprotocol/arcprotocol/blob/main/spec/versions/v1.0/arc-openapi.yaml)

