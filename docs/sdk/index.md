# ARC SDK

Official SDK implementations for the ARC Protocol.

## Supported Languages

| Language | Status | Repository |
| :------- | :----- | :--------- |
| Python   | Stable | [arc-sdk](https://github.com/arcprotocol/python-sdk) |

## Python SDK

- Full ARC Protocol implementation
- ARCClient and ARCServer
- Quantum-safe hybrid TLS (X25519 + Kyber-768)
- FastAPI and Starlette integration
- OAuth2 authentication
- SSE streaming support
- Task and chat methods
- Workflow tracing
- ChatManager for session management

**Installation:**

```bash
pip install arc-sdk              # Core
pip install arc-sdk[pqc]         # + Post-Quantum Cryptography
pip install arc-sdk[all]         # + All integrations
pip install arc-sdk[all,pqc]     # Complete installation
```

**Documentation:** [Python SDK Guide](./python/index.md)

## Examples

Reference implementations available in [examples directory](../../examples/python).
