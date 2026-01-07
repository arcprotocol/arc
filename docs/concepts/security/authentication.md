# Authentication

OAuth2 and JWT-based authentication for ARC Protocol.

## OAuth 2.0

ARC Protocol recommends OAuth 2.0 Bearer tokens for authentication.

### Token Format

```
Authorization: Bearer <access_token>
```

### Token Validation

Server validates tokens on every request:

```python
from arc import Server
from arc.auth import MultiProviderJWTValidator

# Configure JWT validator
validator = MultiProviderJWTValidator(
    providers={
        "auth0": {
            "jwks_uri": "https://your-domain.auth0.com/.well-known/jwks.json",
            "audience": "https://your-api.com",
            "issuer": "https://your-domain.auth0.com/"
        }
    }
)

# Enable authentication
server = Server(server_id="secure-server", enable_auth=True)
server.set_jwt_validator(validator)
```

## JWT Structure

### Claims

Required JWT claims:

```json
{
  "iss": "https://your-domain.auth0.com/",
  "sub": "user-id-123",
  "aud": "https://your-api.com",
  "exp": 1704542400,
  "iat": 1704456000,
  "scope": "arc.task.controller arc.chat.controller"
}
```

### Validation

Server validates:
- **Signature** - Cryptographic signature using JWKS
- **Issuer** - Token from trusted issuer
- **Audience** - Token intended for this API
- **Expiration** - Token not expired
- **Scopes** - Required scopes present

## Identity Providers

### Auth0

```python
validator = MultiProviderJWTValidator(
    providers={
        "auth0": {
            "jwks_uri": "https://your-domain.auth0.com/.well-known/jwks.json",
            "audience": "https://your-api.com",
            "issuer": "https://your-domain.auth0.com/"
        }
    }
)
```

### Okta

```python
validator = MultiProviderJWTValidator(
    providers={
        "okta": {
            "jwks_uri": "https://your-domain.okta.com/oauth2/default/v1/keys",
            "audience": "api://default",
            "issuer": "https://your-domain.okta.com/oauth2/default"
        }
    }
)
```

### Multiple Providers

```python
validator = MultiProviderJWTValidator(
    providers={
        "auth0": {
            "jwks_uri": "https://domain1.auth0.com/.well-known/jwks.json",
            "audience": "https://api.com",
            "issuer": "https://domain1.auth0.com/"
        },
        "okta": {
            "jwks_uri": "https://domain2.okta.com/oauth2/default/v1/keys",
            "audience": "api://default",
            "issuer": "https://domain2.okta.com/oauth2/default"
        }
    }
)
```

## Client Authentication

### With Token

```python
from arc import Client

client = Client(
    endpoint="https://api.example.com/arc",
    token="your-oauth2-access-token"
)

response = await client.task.create(
    target_agent="secure-agent",
    initial_message={...}
)
```

### Token Refresh

Handle token expiration:

```python
import time

class TokenManager:
    def __init__(self):
        self.token = None
        self.expires_at = 0
    
    async def get_token(self):
        if time.time() >= self.expires_at:
            # Refresh token
            self.token = await refresh_oauth_token()
            self.expires_at = time.time() + 3600
        return self.token

# Usage
token_manager = TokenManager()
client = Client(
    endpoint="https://api.example.com/arc",
    token=await token_manager.get_token()
)
```

## Error Handling

### Authentication Failures

```python
from arc.exceptions import AuthenticationError, TokenExpiredError

try:
    response = await client.task.create(...)
except AuthenticationError as e:
    # Invalid or missing token
    print(f"Authentication failed: {e.message}")
except TokenExpiredError as e:
    # Token expired, refresh and retry
    new_token = await refresh_token()
    client.token = new_token
    response = await client.task.create(...)
```

### Error Codes

- `-44001` Authentication Failed - Invalid or missing token
- `-44004` Token Expired - Bearer token expired

## Security Best Practices

1. **Use HTTPS** - Never send tokens over HTTP
2. **Short-Lived Tokens** - Access tokens expire in 1 hour or less
3. **Secure Storage** - Store tokens securely (encrypted, not in code)
4. **Token Refresh** - Implement automatic token refresh
5. **Revocation** - Support token revocation
6. **Audit Logging** - Log authentication events

## Machine-to-Machine

For agent-to-agent authentication:

```python
# Client credentials flow
import httpx

async def get_m2m_token():
    response = await httpx.post(
        "https://your-domain.auth0.com/oauth/token",
        json={
            "client_id": "your-client-id",
            "client_secret": "your-client-secret",
            "audience": "https://your-api.com",
            "grant_type": "client_credentials"
        }
    )
    return response.json()["access_token"]

# Use M2M token
token = await get_m2m_token()
client = Client(endpoint="...", token=token)
```

## Custom Authentication

Implement custom JWT validation:

```python
from arc.auth import JWTValidator

class CustomJWTValidator(JWTValidator):
    async def validate_token(self, token: str) -> dict:
        # Custom validation logic
        decoded = self.decode_token(token)
        
        # Additional custom checks
        if not self.is_valid_custom_claim(decoded):
            raise AuthenticationError("Invalid custom claim")
        
        return decoded
    
    def is_valid_custom_claim(self, decoded: dict) -> bool:
        # Custom validation
        return "custom_claim" in decoded

# Use custom validator
validator = CustomJWTValidator(...)
server.set_jwt_validator(validator)
```

## Links

- [Authorization](./authorization.md)
- [Transport Security](./transport.md)
- [Python SDK Authentication](../../sdk/python/server/authentication.md)

