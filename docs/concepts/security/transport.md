# Transport Security

TLS and quantum-safe encryption for ARC Protocol.

## TLS Requirements

ARC Protocol requires TLS 1.2 or higher for all communications.

### Minimum Configuration

```
Protocol: TLS 1.2+
Cipher Suites: Strong ciphers only (AES-256, ChaCha20)
Certificate Validation: Required
```

## Quantum-Safe Hybrid TLS

ARC Python SDK supports hybrid TLS combining classical and post-quantum cryptography.

### Algorithm

**X25519 + Kyber-768**
- Classical: X25519 (Curve25519)
- Post-Quantum: Kyber-768 (NIST FIPS 203 ML-KEM)

### Client Configuration

```python
from arc import Client

# Enable quantum-safe TLS (default)
client = Client(
    endpoint="https://api.example.com/arc",
    token="your-token",
    use_quantum_safe=True
)
```

### Server Configuration

```python
server.run(
    host="0.0.0.0",
    port=443,
    ssl_keyfile="/path/to/server.key",
    ssl_certfile="/path/to/server.crt"
)
```

Quantum-safe TLS is enabled by default when `arc-sdk[pqc]` is installed.

## Certificate Management

### Production Certificates

Use certificates from trusted CA:

```python
import ssl

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain("cert.pem", "key.pem")

server.run(host="0.0.0.0", port=443, ssl_context=ssl_context)
```

### Certificate Validation

Always validate certificates in production:

```python
# Client validates server certificate
client = Client(
    endpoint="https://api.example.com/arc",
    token="token",
    verify_ssl=True  # Default
)
```

## Security Best Practices

1. **TLS 1.2+ Only** - Disable older protocols
2. **Strong Ciphers** - Use AES-256-GCM or ChaCha20-Poly1305
3. **Certificate Validation** - Always validate in production
4. **Certificate Rotation** - Rotate certificates regularly
5. **Quantum-Safe** - Enable hybrid TLS for future-proofing

## Links

- [Quantum-Safe TLS Guide](../../sdk/python/quantum/)
- [Authentication](./authentication.md)

