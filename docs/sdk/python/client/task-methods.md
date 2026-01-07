# Task Methods

Asynchronous task operations for long-running processes.

## task.create()

Create new asynchronous task.

```python
response = await client.task.create(
    target_agent="document-analyzer",
    initial_message={
        "role": "user",
        "parts": [{"type": "text", "content": "Analyze this report"}]
    },
    priority="HIGH",
    metadata={"user_id": "user-123", "deadline": "2025-01-10"}
)

task_id = response.result["task"]["taskId"]
status = response.result["task"]["status"]  # SUBMITTED
```

**Parameters:**
- `target_agent` (str): Target agent ID
- `initial_message` (dict): Initial message object
- `priority` (Optional[str]): Task priority (LOW, NORMAL, HIGH, URGENT)
- `metadata` (Optional[dict]): Custom task metadata
- `trace_id` (Optional[str]): Workflow trace ID

**Returns:** ARCResponse with task object

**Task Object:**
```python
{
    "taskId": "task-abc123",
    "status": "SUBMITTED",  # or WORKING, INPUT_REQUIRED, COMPLETED, FAILED, CANCELED
    "createdAt": "2025-01-06T00:00:00Z",
    "updatedAt": "2025-01-06T00:00:00Z",
    "messages": [...],
    "artifacts": []
}
```

## task.send()

Send additional message to existing task.

Use when task status is `INPUT_REQUIRED` - agent needs more information.

```python
response = await client.task.send(
    target_agent="document-analyzer",
    task_id="task-abc123",
    message={
        "role": "user",
        "parts": [{"type": "text", "content": "Additional context"}]
    }
)
```

**Parameters:**
- `target_agent` (str): Target agent ID
- `task_id` (str): Task identifier
- `message` (dict): Message object
- `trace_id` (Optional[str]): Workflow trace ID

**Returns:** ARCResponse with success status

## task.info()

Get task status and history.

```python
response = await client.task.info(
    target_agent="document-analyzer",
    task_id="task-abc123",
    include_messages=True,
    include_artifacts=True
)

status = response.result["task"]["status"]
messages = response.result["task"]["messages"]
artifacts = response.result["task"]["artifacts"]
```

**Parameters:**
- `target_agent` (str): Target agent ID
- `task_id` (str): Task identifier
- `include_messages` (bool): Include message history (default: True)
- `include_artifacts` (bool): Include generated artifacts (default: True)
- `trace_id` (Optional[str]): Workflow trace ID

**Returns:** ARCResponse with task object including messages and artifacts

## task.cancel()

Cancel running task.

```python
response = await client.task.cancel(
    target_agent="document-analyzer",
    task_id="task-abc123",
    reason="User cancelled request"
)

status = response.result["task"]["status"]  # CANCELED
canceled_at = response.result["task"]["canceledAt"]
```

**Parameters:**
- `target_agent` (str): Target agent ID
- `task_id` (str): Task identifier
- `reason` (Optional[str]): Cancellation reason
- `trace_id` (Optional[str]): Workflow trace ID

**Returns:** ARCResponse with updated task object

## task.subscribe()

Subscribe to task notifications via webhook.

```python
response = await client.task.subscribe(
    target_agent="document-analyzer",
    task_id="task-abc123",
    callback_url="https://myapp.com/webhooks/arc",
    events=["TASK_COMPLETED", "TASK_FAILED", "NEW_ARTIFACT"]
)

subscription_id = response.result["subscription"]["subscriptionId"]
```

**Parameters:**
- `target_agent` (str): Target agent ID
- `task_id` (str): Task identifier
- `callback_url` (str): Webhook URL for notifications
- `events` (Optional[List[str]]): Event types to subscribe to
- `trace_id` (Optional[str]): Workflow trace ID

**Available Events:**
- `TASK_CREATED`
- `TASK_STARTED`
- `TASK_PAUSED`
- `TASK_RESUMED`
- `TASK_COMPLETED`
- `TASK_FAILED`
- `TASK_CANCELED`
- `NEW_MESSAGE`
- `NEW_ARTIFACT`
- `STATUS_CHANGE`

**Returns:** ARCResponse with subscription object

**Subscription Object:**
```python
{
    "subscriptionId": "sub-xyz789",
    "taskId": "task-abc123",
    "callbackUrl": "https://myapp.com/webhooks/arc",
    "events": ["TASK_COMPLETED", "TASK_FAILED"],
    "createdAt": "2025-01-06T00:00:00Z",
    "active": true
}
```

## Task Workflow Example

Complete task lifecycle:

```python
from arc import Client

client = Client(endpoint="...", token="...")

# 1. Create task
create_response = await client.task.create(
    target_agent="document-analyzer",
    initial_message={
        "role": "user",
        "parts": [{"type": "text", "content": "Analyze quarterly report"}]
    },
    priority="HIGH"
)

task_id = create_response.result["task"]["taskId"]
print(f"Task created: {task_id}")

# 2. Subscribe to notifications
subscribe_response = await client.task.subscribe(
    target_agent="document-analyzer",
    task_id=task_id,
    callback_url="https://myapp.com/webhooks/arc",
    events=["TASK_COMPLETED", "TASK_FAILED"]
)

print(f"Subscribed: {subscribe_response.result['subscription']['subscriptionId']}")

# 3. Poll for status (or wait for webhook)
import asyncio

while True:
    info_response = await client.task.info(
        target_agent="document-analyzer",
        task_id=task_id
    )
    
    status = info_response.result["task"]["status"]
    print(f"Status: {status}")
    
    if status == "INPUT_REQUIRED":
        # Agent needs more info
        await client.task.send(
            target_agent="document-analyzer",
            task_id=task_id,
            message={
                "role": "user",
                "parts": [{"type": "text", "content": "Additional context"}]
            }
        )
    elif status in ["COMPLETED", "FAILED", "CANCELED"]:
        # Task finished
        break
    
    await asyncio.sleep(2)  # Poll every 2 seconds

# 4. Get final results
final_response = await client.task.info(
    target_agent="document-analyzer",
    task_id=task_id,
    include_artifacts=True
)

artifacts = final_response.result["task"]["artifacts"]
print(f"Artifacts: {len(artifacts)}")
```

## Error Handling

```python
from arc.exceptions import (
    TaskNotFoundError,
    TaskAlreadyCompletedError,
    TaskAlreadyCanceledError,
    InvalidParamsError
)

try:
    response = await client.task.info(
        target_agent="analyzer",
        task_id="task-123"
    )
except TaskNotFoundError as e:
    print(f"Task not found: {e.code}")
except InvalidParamsError as e:
    print(f"Invalid parameters: {e.message}")
```

## Task States

```
SUBMITTED → WORKING → COMPLETED
            ↓
       INPUT_REQUIRED
            ↓
         WORKING

Any state → CANCELED
Any state → FAILED
```

## Examples

- [Task Create](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/test_task_create.py)
- [Task Send](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/test_task_send.py)
- [Task Info](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/test_task_info.py)
- [Task Cancel](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/test_task_cancel.py)
- [Task Subscribe](https://github.com/arcprotocol/python-sdk/blob/main/examples/client/test_task_subscribe.py)

