# ARC Protocol - Agent Remote Communication

[![GitHub license](https://img.shields.io/github/license/arcprotocol/arcprotocol)](https://github.com/arcprotocol/arcprotocol/blob/main/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/arc-sdk.svg)](https://pypi.org/project/arc-sdk/)

**ARC (Agent Remote Communication)** is a stateless RPC protocol designed for multi-agent systems. It provides a unified communication standard that enables deploying multiple specialized agents behind a single endpoint with intelligent routing capabilities. The protocol implements quantum-safe hybrid TLS encryption (X25519 + Kyber-768) for future-proof security, single-endpoint multi-agent routing via `targetAgent` field for simplified infrastructure, and comprehensive workflow tracing through `traceId` propagation for observability across distributed agent architectures. Built on HTTPS with JSON serialization, ARC supports both asynchronous task-based operations and real-time chat interactions with Server-Sent Events streaming.

> [!IMPORTANT]
> **Quantum-Safe Security**: ARC Protocol implements hybrid TLS using X25519 + Kyber-768 (NIST-standardized ML-KEM, FIPS 203) for protection against both current and future quantum computing attacks. See [Hybrid TLS Implementation](#hybrid-tls-implementation) below.

> For an overview of the ARC ecosystem and our vision, visit [arc-protocol.org](https://arc-protocol.org).

## Key Features

- **Single-Endpoint Multi-Agent Routing**: Deploy multiple specialized agents behind one endpoint with protocol-level routing via `targetAgent` field
- **Quantum-Safe Hybrid TLS**: Post-quantum cryptography using X25519 + Kyber-768 (FIPS 203 ML-KEM) for protection against quantum computing attacks
- **Workflow Tracing**: End-to-end traceability across distributed agent architectures via `traceId` propagation, designed for integration with observability platforms
- **Intelligent Agent Selection**: Automatic agent ranking and routing through ARC Compass, using semantic analysis and capability matching to select optimal agents for each request
- **Agent Discovery and Registry**: Centralized agent management through ARC Ledger, maintaining agent cards, capabilities, endpoints, and metadata for dynamic service discovery
- **Multiple Communication Patterns**: Synchronous request/response for immediate results, Server-Sent Events (SSE) for real-time streaming, and asynchronous push notifications for long-running operations

## Hybrid TLS Implementation

### What is Hybrid TLS?

Combines classical and post-quantum cryptography:
- **Classical**: X25519 (Curve25519 elliptic curve)
- **Post-Quantum**: Kyber-768 (NIST FIPS 203 ML-KEM)

**Result**: Secure against both current and future quantum attacks.

**Default**: `x25519_kyber768` (X25519 + Kyber-768)

**Industry Implementations**:
- **Zoom**: Uses Kyber-768 for E2EE (May 2024)
- **Chrome**: Uses X25519Kyber768 hybrid for TLS (Aug 2023)
- **Cloudflare**: Uses X25519MLKEM768 hybrid for TLS (2022)

### How It Works

> [!NOTE]
> **Requirements**: Both client and server must install `arc-sdk[pqc]` for post-quantum cryptography.

**TLS Handshake**:
- Both sides have PQC → Negotiates `x25519_kyber768` hybrid key exchange
- One side missing PQC → OpenSSL falls back to classical X25519

**Installation**:
```bash
pip install arc-sdk[pqc]
```

> [!TIP]
> Libraries load automatically - no manual configuration needed. Hybrid TLS is negotiated during the handshake.

## Documentation

**Website:** [arc-protocol.org](https://arc-protocol.org)

**Local Documentation:**
- [Protocol Specification](./spec/arc-specification.md)
- [Getting Started](./docs/getting-started.md)
- [Examples](./examples/)

**Online Documentation:**
- [Getting Started](https://arc-protocol.org/docs/getting-started)
- [Protocol Specification](https://arc-protocol.org/docs/spec/overview)
- [Python SDK](https://arc-protocol.org/docs/sdk/python)
- [Multi-Agent System Guide](https://arc-protocol.org/docs/guides/multi-agent-system)
- [Supervisor Pattern Guide](https://arc-protocol.org/docs/guides/supervisor-pattern)
- [Concepts](https://arc-protocol.org/docs/concepts/protocol-design)


## ARC Ecosystem

> [!NOTE]
> While ARC Protocol can be used as a standalone communication protocol between agents, it works best as part of the ARC ecosystem.

- **[ARC Protocol](https://github.com/arcprotocol/arcprotocol)**: This repository - the communication standard between agents
- **[ARC Compass](https://github.com/arcprotocol/arccompass)**: Intelligent agent ranking engine for optimal agent selection
- **[ARC Ledger](https://github.com/arcprotocol/arcledger)**: Centralized agent discovery registry

ARC Protocol works effectively with other components in the ARC ecosystem. The protocol's workflow tracing capabilities integrate with external monitoring and observability platforms, enabling tracking of multi-agent workflows. This design works with existing monitoring solutions while maintaining protocol simplicity.

## Maintainers

ARC Protocol is maintained by the ARC Protocol team and contributors from the open source community. See [MAINTAINERS.md](./MAINTAINERS.md) for details and [CODEOWNERS](./CODEOWNERS) for code ownership information.