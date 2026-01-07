# Protocol Design

ARC Protocol design principles and rationale.

## Overview

ARC uses a stateless RPC design with JSON serialization, single-endpoint architecture, and standardized error taxonomy.

## Topics

- [Stateless RPC](./stateless-rpc.md) - Why stateless RPC over JSON-RPC
- [Single Endpoint](./single-endpoint.md) - Single-endpoint multi-agent routing
- [Error Codes](./error-codes.md) - Error taxonomy and conventions

## Core Principles

### Stateless Communication

Each request is independent and self-contained. No server-side session state required.

### Agent-Level Routing

Routing determined by `targetAgent` field at protocol level, not URL routing.

### Method-Based Invocation

Clean RPC-style method calls: `task.create`, `chat.start`, etc.

### JSON Serialization

Standard JSON for universal compatibility and tooling support.

## Design Goals

1. **Simplicity** - Easy to implement and understand
2. **Scalability** - Stateless design enables horizontal scaling
3. **Flexibility** - Single endpoint supports any number of agents
4. **Traceability** - Built-in workflow tracing via `traceId`
5. **Security** - OAuth2 and quantum-safe TLS support

## Links

- [Specification](../../spec/arc-specification.md)
- [Architecture Patterns](../architecture/)

