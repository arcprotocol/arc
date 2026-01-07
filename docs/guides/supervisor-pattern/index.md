# Supervisor Pattern

Implement intelligent routing with a supervisor agent that delegates to specialized sub-agents.

## Overview

The Supervisor pattern uses a central agent that analyzes requests and routes them to appropriate specialized agents.

## Architecture

```
                  ┌──────────────┐
        User ───► │  Supervisor  │
                  │    Agent     │
                  └──────┬───────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐      ┌─────────┐     ┌─────────┐
   │Finance  │      │   HR    │     │Support  │
   │ Agent   │      │  Agent  │     │ Agent   │
   └─────────┘      └─────────┘     └─────────┘
```

## When to Use

Use supervisor pattern when:
1. **Complex Routing** - Request routing depends on content analysis
2. **Dynamic Discovery** - Available agents change at runtime
3. **Capability Matching** - Route based on agent capabilities
4. **Load Distribution** - Distribute work across multiple agents

## Basic Implementation

Simple supervisor with hardcoded routing logic.

**Guide:** [Basic Implementation](./basic-implementation.md)

## ARC Ledger Integration

Dynamic agent discovery and routing using ARC Ledger.

**Guide:** [ARC Ledger Integration](./arc-ledger-integration.md)

## Dynamic Prompts

Enhance agent prompts with capability information from ARC Ledger.

**Guide:** [Dynamic Prompts](./dynamic-prompts.md)

## Benefits

### 1. Single Entry Point
Clients communicate with one supervisor, not multiple agents.

### 2. Intelligent Routing
Supervisor analyzes content and routes to best agent.

### 3. Flexibility
Add/remove sub-agents without changing client code.

### 4. Load Management
Supervisor can implement load balancing logic.

### 5. Fallback Handling
Supervisor handles failures and implements fallback strategies.

## Comparison to Direct Routing

### Without Supervisor

```python
# Client must know all agents
if "invoice" in query:
    client = Client("http://finance-server/arc")
    response = await client.chat.start(target_agent="finance-agent", ...)
elif "salary" in query:
    client = Client("http://hr-server/arc")
    response = await client.chat.start(target_agent="hr-agent", ...)
```

### With Supervisor

```python
# Client calls one endpoint
client = Client("http://supervisor-server/arc")
response = await client.chat.start(
    target_agent="supervisor",
    initial_message={"role": "user", "parts": [{"type": "text", "content": query}]}
)
# Supervisor routes internally
```

## Pattern Variants

### 1. Static Routing
Supervisor uses predefined rules (keywords, regex).

### 2. Dynamic Routing
Supervisor queries ARC Ledger for available agents and capabilities.

### 3. AI-Based Routing
Supervisor uses LLM to analyze request and select agent.

### 4. Hybrid Routing
Combines static rules with dynamic discovery.

## Quick Start

### Step 1: Choose Implementation

- **Learning/Testing**: [Basic Implementation](./basic-implementation.md)
- **Production**: [ARC Ledger Integration](./arc-ledger-integration.md)

### Step 2: Deploy Sub-Agents

Deploy specialized agents (finance, HR, support).

### Step 3: Deploy Supervisor

Deploy supervisor agent with routing logic.

### Step 4: Test

Send diverse requests through supervisor and verify correct routing.

## Links

- [Multi-Agent System](../multi-agent-system/) - Deploy multiple agents
- [Architecture Concepts](../../concepts/architecture/) - Design patterns
- [ARC Ledger Integration](../../concepts/agent-discovery/arc-ledger.md) - Discovery concepts

