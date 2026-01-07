---
id: index
title: ARC Protocol Documentation
sidebar_label: Home
sidebar_position: 1
slug: /
---

# ARC Protocol Documentation

**Agent Remote Communication (ARC) Protocol** - A stateless RPC protocol for multi-agent systems with quantum-safe hybrid TLS encryption and single-endpoint multi-agent routing.

## Quick Navigation

### Getting Started
- [Getting Started Guide](getting-started) - Quick start for implementing ARC Protocol
- [Protocol Specification](spec/overview) - Technical specification

### Implementation Guides
- [Multi-Agent System](guides/multi-agent-system) - Deploy multiple agents
- [Supervisor Pattern](guides/supervisor-pattern) - Intelligent routing

### Core Concepts
- [Protocol Design](concepts/protocol-design) - Stateless RPC, single-endpoint
- [Architecture](concepts/architecture) - Multi-agent patterns
- [Security](concepts/security) - Authentication, transport, authorization

### SDK
- [Python SDK](sdk/python) - Python implementation with quantum-safe TLS

## What is ARC Protocol?

**ARC (Agent Remote Communication)** is a communication protocol for multi-agent systems.

### Key Features

- **Single Endpoint, Multiple Agents** - Deploy hundreds of agent types on one endpoint
- **Agent-Level Routing** - Built-in routing via `requestAgent` and `targetAgent`
- **Workflow Tracing** - End-to-end traceability via `traceId`
- **Quantum-Safe Security** - Hybrid TLS using X25519 + Kyber-768 (FIPS 203 ML-KEM)
- **Real-time Streaming** - Server-Sent Events (SSE) for chat responses
- **Stateless Design** - Clean RPC-style method invocation

## Available Methods

### Task Methods
Asynchronous operations for long-running work:
- `task.create` - Create a new task
- `task.send` - Send additional message to task
- `task.info` - Get task status and history
- `task.cancel` - Cancel a running task
- `task.subscribe` - Subscribe to task notifications
- `task.notification` - Server-initiated notification

### Chat Methods
Real-time communication for interactive conversations:
- `chat.start` - Begin conversation with initial message
- `chat.message` - Send follow-up message in active chat
- `chat.end` - Terminate an active chat

## ARC Ecosystem

- **ARC Protocol** - Communication standard (this repository)
- **ARC Compass** - Agent search engine
- **ARC Ledger** - Centralized agent discovery registry
- **Python SDK** - Python implementation

## Learning Path

### First-Time Users
1. [Getting Started Guide](getting-started)
2. [Protocol Specification](spec/overview)
3. [Python SDK](sdk/python)

### Implementers
1. [Multi-Agent System Guide](guides/multi-agent-system)
2. [Architecture Concepts](concepts/architecture)
3. [Best Practices](concepts/protocol-design)

### Contributors
1. [Contributing Guidelines](https://github.com/arcprotocol/arcprotocol/blob/main/CONTRIBUTING.md)
2. [Code of Conduct](https://github.com/arcprotocol/arcprotocol/blob/main/CODE_OF_CONDUCT.md)

## License

Apache License 2.0. See [LICENSE](https://github.com/arcprotocol/arcprotocol/blob/main/LICENSE).

## Links

- [GitHub](https://github.com/arcprotocol/arcprotocol)
- [Issues](https://github.com/arcprotocol/arcprotocol/issues)
- [Security](https://github.com/arcprotocol/arcprotocol/blob/main/SECURITY.md)
