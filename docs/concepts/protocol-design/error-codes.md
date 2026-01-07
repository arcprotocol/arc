# Error Codes

ARC Protocol error taxonomy and conventions.

## Error Structure

```json
{
  "error": {
    "code": -32600,
    "message": "Invalid request format",
    "details": {
      "field": "method",
      "reason": "required field missing"
    }
  }
}
```

## Standard RPC Errors (-32xxx)

Borrowed from JSON-RPC conventions:

| Code | Name | Description |
|------|------|-------------|
| -32700 | Parse Error | Invalid JSON |
| -32600 | Invalid Request | Malformed ARC message |
| -32601 | Method Not Found | Unknown method |
| -32602 | Invalid Params | Invalid parameters |
| -32603 | Internal Error | Server internal error |

## Agent Errors (-41xxx)

| Code | Name | Description |
|------|------|-------------|
| -41001 | Agent Not Found | Target agent does not exist |
| -41002 | Agent Not Available | Agent exists but unavailable |
| -41003 | Agent Overloaded | Agent cannot accept requests |

## Task Errors (-42xxx)

| Code | Name | Description |
|------|------|-------------|
| -42001 | Task Not Found | Task ID does not exist |
| -42002 | Task Already Completed | Cannot modify completed task |
| -42003 | Task Already Canceled | Cannot modify canceled task |
| -42004 | Task Processing Error | Error during task execution |

## Chat Errors (-43xxx)

| Code | Name | Description |
|------|------|-------------|
| -43001 | Chat Not Found | Chat ID does not exist |
| -43002 | Chat Already Closed | Cannot send to closed chat |
| -43003 | Chat Timeout | Chat session timed out |
| -43004 | Chat Participant Limit | Too many participants |
| -43005 | Invalid Chat Message | Malformed message |
| -43006 | Chat Buffer Overflow | Message buffer full |

## Security Errors (-44xxx)

| Code | Name | Description |
|------|------|-------------|
| -44001 | Authentication Failed | Invalid or missing token |
| -44002 | Authorization Failed | Insufficient permissions |
| -44003 | Insufficient Scope | OAuth2 scope missing |
| -44004 | Token Expired | Bearer token expired |

## Protocol Errors (-45xxx)

| Code | Name | Description |
|------|------|-------------|
| -45001 | Unsupported Version | ARC version not supported |
| -45002 | Rate Limit Exceeded | Too many requests |
| -45003 | Request Too Large | Payload exceeds limit |
| -45004 | Network Error | Network communication failed |

## Error Handling

### Client Side

```python
from arc.exceptions import (
    TaskNotFoundError,
    ChatNotFoundError,
    AgentNotFoundError,
    AuthenticationError
)

try:
    response = await client.task.create(...)
except TaskNotFoundError as e:
    # Handle task not found (code: -42001)
    print(f"Error: {e.code} - {e.message}")
except AgentNotFoundError as e:
    # Handle agent not found (code: -41001)
    print(f"Agent unavailable: {e.message}")
except AuthenticationError as e:
    # Handle auth error (code: -44001)
    print(f"Authentication failed: {e.message}")
```

### Server Side

```python
from arc.exceptions import TaskNotFoundError

@server.agent_handler("my-agent", "task.info")
async def get_task_info(params, context):
    task = get_task(params["taskId"])
    
    if not task:
        raise TaskNotFoundError(f"Task {params['taskId']} not found")
    
    return {"type": "task", "task": task}
```

## Error Response Format

```json
{
  "arc": "1.0",
  "id": "request-123",
  "responseAgent": "server-agent",
  "targetAgent": "client-agent",
  "error": {
    "code": -42001,
    "message": "Task not found",
    "details": {
      "taskId": "task-123",
      "timestamp": "2025-01-06T00:00:00Z"
    }
  }
}
```

## Custom Errors

Implement custom error codes outside reserved ranges:

```python
# Custom error codes (avoid -32xxx, -41xxx, -42xxx, -43xxx, -44xxx, -45xxx)
class CustomBusinessError(ARCException):
    def __init__(self, message: str):
        super().__init__(
            code=-50001,  # Custom range
            message=message
        )
```

## Best Practices

1. **Use Standard Codes** - Use ARC standard codes when applicable
2. **Provide Details** - Include helpful error details
3. **Log Errors** - Log errors with trace IDs for debugging
4. **Handle Gracefully** - Implement proper error handling
5. **Return Appropriate Codes** - Match error type to situation

## Error Ranges Summary

| Range | Category | Usage |
|-------|----------|-------|
| -32xxx | Standard RPC | Protocol-level errors |
| -41xxx | Agent | Agent-related errors |
| -42xxx | Task | Task operation errors |
| -43xxx | Chat | Chat operation errors |
| -44xxx | Security | Authentication/authorization |
| -45xxx | Protocol | Protocol-level issues |
| -50xxx+ | Custom | Application-specific errors |

## Links

- [Specification Error Section](../../spec/arc-specification.md#error-handling)
- [Python SDK Exceptions](../../sdk/python/client/responses-errors.md)

