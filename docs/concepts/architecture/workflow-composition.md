# Workflow Composition

Multi-agent workflow orchestration patterns.

## Sequential Workflow

Chain agents for multi-step processing.

```
User → Agent A → Agent B → Agent C → Result
```

### Implementation

```python
async def sequential_workflow(initial_message):
    trace_id = generate_trace_id()
    
    # Step 1: Agent A processes
    client_a = Client("https://server-a.com/arc")
    result_a = await client_a.task.create(
        target_agent="agent-a",
        initial_message=initial_message,
        trace_id=trace_id
    )
    
    # Step 2: Agent B processes result from A
    client_b = Client("https://server-b.com/arc")
    result_b = await client_b.task.create(
        target_agent="agent-b",
        initial_message=result_a.result["task"]["messages"][-1],
        trace_id=trace_id
    )
    
    # Step 3: Agent C processes result from B
    client_c = Client("https://server-c.com/arc")
    result_c = await client_c.task.create(
        target_agent="agent-c",
        initial_message=result_b.result["task"]["messages"][-1],
        trace_id=trace_id
    )
    
    return result_c.result
```

## Parallel Workflow

Execute multiple agents concurrently.

```
        ┌→ Agent A →┐
User →  ├→ Agent B →├→ Aggregate → Result
        └→ Agent C →┘
```

### Implementation

```python
import asyncio

async def parallel_workflow(message):
    trace_id = generate_trace_id()
    
    # Execute agents concurrently
    results = await asyncio.gather(
        call_agent("agent-a", message, trace_id),
        call_agent("agent-b", message, trace_id),
        call_agent("agent-c", message, trace_id)
    )
    
    # Aggregate results
    aggregated = aggregate_results(results)
    return aggregated

async def call_agent(agent_id, message, trace_id):
    client = Client(f"https://{agent_id}.com/arc")
    return await client.task.create(
        target_agent=agent_id,
        initial_message=message,
        trace_id=trace_id
    )
```

## Conditional Workflow

Route based on intermediate results.

```
User → Agent A → Decision
                    ├→ Agent B (if condition X)
                    └→ Agent C (if condition Y)
```

### Implementation

```python
async def conditional_workflow(message):
    trace_id = generate_trace_id()
    
    # Initial agent
    client_a = Client("https://server-a.com/arc")
    result_a = await client_a.task.create(
        target_agent="agent-a",
        initial_message=message,
        trace_id=trace_id
    )
    
    # Decision based on result
    decision = analyze_result(result_a)
    
    if decision == "path_b":
        # Route to Agent B
        client_b = Client("https://server-b.com/arc")
        return await client_b.task.create(
            target_agent="agent-b",
            initial_message=result_a.result["task"]["messages"][-1],
            trace_id=trace_id
        )
    else:
        # Route to Agent C
        client_c = Client("https://server-c.com/arc")
        return await client_c.task.create(
            target_agent="agent-c",
            initial_message=result_a.result["task"]["messages"][-1],
            trace_id=trace_id
        )
```

## Human-in-the-Loop

Incorporate human approval in workflow.

```
Agent A → Wait for Approval → Agent B → Result
```

### Implementation

```python
async def human_in_loop_workflow(message):
    trace_id = generate_trace_id()
    
    # Step 1: Agent A generates proposal
    client_a = Client("https://server-a.com/arc")
    proposal = await client_a.task.create(
        target_agent="agent-a",
        initial_message=message,
        trace_id=trace_id
    )
    
    # Step 2: Human approval
    approved = await request_human_approval(proposal)
    
    if not approved:
        return {"status": "rejected", "reason": "Human rejected"}
    
    # Step 3: Agent B executes approved action
    client_b = Client("https://server-b.com/arc")
    result = await client_b.task.create(
        target_agent="agent-b",
        initial_message=proposal.result["task"]["messages"][-1],
        trace_id=trace_id
    )
    
    return result
```

## Error Handling in Workflows

### Retry Logic

```python
async def workflow_with_retry(message, max_retries=3):
    trace_id = generate_trace_id()
    
    for attempt in range(max_retries):
        try:
            return await execute_workflow(message, trace_id)
        except ARCException as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Fallback Agents

```python
async def workflow_with_fallback(message):
    trace_id = generate_trace_id()
    
    try:
        # Try primary agent
        return await call_agent("primary-agent", message, trace_id)
    except AgentNotAvailableError:
        # Fallback to secondary agent
        return await call_agent("fallback-agent", message, trace_id)
```

## Workflow State Management

### Stateless Workflow

Each step is independent:

```python
async def stateless_workflow(message):
    # Each call is self-contained
    result_a = await call_agent_a(message)
    result_b = await call_agent_b(result_a)
    return result_b
```

### Stateful Workflow

Maintain workflow state externally:

```python
class WorkflowState:
    def __init__(self):
        self.trace_id = generate_trace_id()
        self.steps = []
        self.current_step = 0
    
    async def execute_step(self, agent_id, message):
        result = await call_agent(agent_id, message, self.trace_id)
        self.steps.append({
            "step": self.current_step,
            "agent": agent_id,
            "result": result
        })
        self.current_step += 1
        return result

# Usage
workflow = WorkflowState()
result_a = await workflow.execute_step("agent-a", message)
result_b = await workflow.execute_step("agent-b", result_a)
```

## Workflow Tracing

Trace ID propagates through all steps:

```python
async def traced_workflow(message):
    trace_id = generate_trace_id()
    
    # All steps share trace ID
    result_a = await call_agent("agent-a", message, trace_id)
    result_b = await call_agent("agent-b", result_a, trace_id)
    result_c = await call_agent("agent-c", result_b, trace_id)
    
    return result_c
```

Query workflow history using trace ID for debugging and monitoring.

## Complex Workflow Example

```python
async def complex_workflow(message):
    trace_id = generate_trace_id()
    
    # Step 1: Parallel analysis
    analysis_results = await asyncio.gather(
        call_agent("sentiment-analyzer", message, trace_id),
        call_agent("entity-extractor", message, trace_id),
        call_agent("intent-classifier", message, trace_id)
    )
    
    # Step 2: Aggregate analysis
    aggregated = aggregate_analysis(analysis_results)
    
    # Step 3: Route based on intent
    intent = aggregated["intent"]
    
    if intent == "purchase":
        # Sequential: validation → payment → confirmation
        validation = await call_agent("validator", aggregated, trace_id)
        if validation["valid"]:
            payment = await call_agent("payment", validation, trace_id)
            return await call_agent("confirmation", payment, trace_id)
    elif intent == "support":
        # Direct to support agent
        return await call_agent("support", aggregated, trace_id)
    else:
        # Fallback
        return await call_agent("general", aggregated, trace_id)
```

## Best Practices

1. **Use Trace IDs** - Enable end-to-end tracking
2. **Handle Errors** - Implement retry and fallback logic
3. **Timeout Management** - Set appropriate timeouts
4. **Idempotency** - Design agents for safe retries
5. **State Management** - Choose stateless or stateful based on needs

## Workflow Patterns Summary

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| Sequential | Multi-step processing | Low |
| Parallel | Independent operations | Medium |
| Conditional | Decision-based routing | Medium |
| Human-in-Loop | Approval workflows | High |

## Links

- [Supervisor/Router Pattern](./supervisor-router.md)
- [Workflow Tracing](../observability/workflow-tracing.md)
- [Multi-Agent Patterns](./multi-agent.md)

