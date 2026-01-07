# Security

Security patterns and best practices for ARC Protocol.

## Overview

ARC Protocol security through authentication, transport encryption, and authorization.

## Topics

- [Authentication](./authentication.md) - OAuth2 and JWT validation
- [Transport Security](./transport.md) - TLS and quantum-safe encryption
- [Authorization](./authorization.md) - Scope validation and permissions

## Security Layers

```
┌─────────────────────────────────────┐
│      Application Security           │
│  (Business Logic, Input Validation) │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Authorization Layer            │
│  (OAuth2 Scopes, Permissions)       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Authentication Layer            │
│  (OAuth2, JWT Validation)           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Transport Security             │
│  (TLS 1.2+, Quantum-Safe Hybrid)    │
└─────────────────────────────────────┘
```

## Core Principles

1. **Defense in Depth** - Multiple security layers
2. **Least Privilege** - Minimal required permissions
3. **Zero Trust** - Verify every request
4. **Encryption Everywhere** - TLS for all communications
5. **Audit Trail** - Log security events

## Quick Reference

### Authentication

```python
from arc import Server
from arc.auth import MultiProviderJWTValidator

validator = MultiProviderJWTValidator(providers={...})
server = Server(server_id="secure-server", enable_auth=True)
server.set_jwt_validator(validator)
```

### Transport Security

```python
# Quantum-safe hybrid TLS (default)
client = Client(endpoint="...", token="...", use_quantum_safe=True)
```

### Authorization

```python
server.set_required_scopes({
    "task.create": ["arc.task.controller"],
    "chat.start": ["arc.chat.controller"]
})
```

## Links

- [Python SDK Security](../../sdk/python/server/authentication.md)
- [Quantum-Safe TLS](../../sdk/python/quantum/)

