# Python Examples

This directory contains Python examples demonstrating the ARC Protocol usage with the official Python SDK.

## Documentation

For Python examples, please refer to:
- [Python SDK Repository](https://github.com/arcprotocol/python-sdk)

## Quick Start

### Basic Installation

Core client and server (no optional dependencies):

```bash
pip install arc-sdk
```

### Optional Dependencies

#### Post-Quantum Cryptography (PQC)

For quantum-resistant hybrid TLS (X25519 + Kyber-768):

```bash
pip install arc-sdk[pqc]
```

> **Note:** This builds liboqs and OQS Provider during installation to enable post-quantum security.

#### All Integrations

For FastAPI, Starlette, and all optional integrations:

```bash
pip install arc-sdk[all]
```

#### Complete Installation

For complete feature set including post-quantum cryptography:

```bash
pip install arc-sdk[all,pqc]
```

## Available Install Options

- `arc-sdk` - Core client and server (no optional dependencies)
- `arc-sdk[pqc]` - Core + Post-Quantum Cryptography (optional)
- `arc-sdk[fastapi]` - Core + FastAPI integration (optional)
- `arc-sdk[starlette]` - Core + Starlette integration (optional)
- `arc-sdk[all]` - Core + all integrations (optional, excludes PQC)
- `arc-sdk[all,pqc]` - Everything including PQC (all optional dependencies)