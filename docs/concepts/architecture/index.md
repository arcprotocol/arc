# Architecture

Multi-agent system architecture patterns for ARC Protocol.

## Overview

ARC Protocol supports flexible multi-agent architectures through stateless communication and agent-level routing.

## Topics

- [Multi-Agent Patterns](./multi-agent.md) - Multi-agent deployment strategies
- [Supervisor/Router](./supervisor-router.md) - Supervisor and router patterns
- [Workflow Composition](./workflow-composition.md) - Agent workflow orchestration

## Core Patterns

### Multi-Agent Deployment

Deploy multiple agents on single endpoint with co-location or distribution strategies.

### Supervisor/Router

Central supervisor routes requests to specialized sub-agents based on capabilities.

### Workflow Composition

Chain multiple agents together for complex multi-step workflows with tracing.

## Design Principles

1. **Loose Coupling** - Agents communicate via protocol, not direct calls
2. **Single Responsibility** - Each agent handles specific domain
3. **Composability** - Agents combine into larger workflows
4. **Traceability** - End-to-end tracing via `traceId`
5. **Scalability** - Independent agent scaling

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│          Client Application             │
└────────────────┬────────────────────────┘
                 │ ARC Protocol
                 ▼
┌─────────────────────────────────────────┐
│         Supervisor Agent                │
└────┬──────────┬────────────┬────────────┘
     │          │            │
     ▼          ▼            ▼
┌─────────┐ ┌────────┐ ┌─────────┐
│ Agent A │ │Agent B │ │ Agent C │
└─────────┘ └────────┘ └─────────┘
```

## Links

- [Protocol Design](../protocol-design/)
- [Agent Discovery](../agent-discovery/)

