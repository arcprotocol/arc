# Multi-Agent System

Build and deploy multi-agent systems with ARC Protocol.

## Overview

Multi-agent systems distribute functionality across specialized agents that communicate via ARC Protocol.

## Architecture

```
┌─────────────────────────────────────────┐
│          Client Application             │
└────────────────┬────────────────────────┘
                 │ ARC Protocol
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Agent A │ │ Agent B │ │ Agent C │
│Finance  │ │  HR     │ │ Support │
└─────────┘ └─────────┘ └─────────┘
```

## Deployment Options

### Single Server
Deploy multiple agents on one server for simplicity and low latency.

**Best for:**
- Development and testing
- Related business domains
- Low to medium traffic
- Shared dependencies

**Guide:** [Single Server Deployment](./single-server.md)

### Distributed
Deploy agents across multiple servers for scaling and isolation.

**Best for:**
- Production systems
- Independent scaling requirements
- Fault isolation
- High availability

**Guide:** [Distributed Deployment](./distributed.md)

## Agent Communication

Agents communicate via ARC Protocol with workflow tracing.

**Guide:** [Agent Communication](./agent-communication.md)

## Key Concepts

### Agent Independence
Each agent is self-contained with its own:
- Business logic
- Data storage
- Dependencies
- Scaling characteristics

### Protocol-Based Communication
Agents communicate through ARC Protocol, not direct calls:
- Loose coupling
- Technology independence
- Easy testing and mocking
- Clear boundaries

### Workflow Tracing
`traceId` enables end-to-end tracking across agent interactions.

## When to Use Multi-Agent

Use multi-agent systems when:
1. **Domain Separation** - Clear business domain boundaries
2. **Independent Scaling** - Different agents have different load
3. **Team Organization** - Different teams own different agents
4. **Technology Diversity** - Agents use different tech stacks

## Quick Start

### 1. Define Agents

```
Finance Agent - Handles invoices, payments
HR Agent - Manages employee queries, benefits
Support Agent - General customer support
```

### 2. Choose Deployment

- Development: Single server
- Production: Distributed

### 3. Implement

Follow the appropriate guide:
- [Single Server Deployment](./single-server.md)
- [Distributed Deployment](./distributed.md)

### 4. Connect

Implement agent-to-agent communication:
- [Agent Communication Guide](./agent-communication.md)

## Links

- [Architecture Concepts](../../concepts/architecture/)
- [Supervisor Pattern](../supervisor-pattern/)
- [Python SDK](../../sdk/python/)

