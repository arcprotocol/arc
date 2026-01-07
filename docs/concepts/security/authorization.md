# Authorization

OAuth2 scope validation and permission management.

## OAuth2 Scopes

ARC Protocol uses OAuth2 scopes for fine-grained authorization.

### Standard Scopes

| Scope | Permission |
|-------|------------|
| `arc.task.controller` | Create and manage tasks |
| `arc.task.notify` | Send task notifications |
| `arc.chat.controller` | Start and manage chats |
| `arc.agent.caller` | Call agents |
| `arc.agent.receiver` | Receive agent calls |

### Scope Configuration

```python
server.set_required_scopes({
    "task.create": ["arc.task.controller", "arc.agent.caller"],
    "task.send": ["arc.task.controller", "arc.agent.caller"],
    "task.info": ["arc.task.controller", "arc.agent.caller"],
    "task.cancel": ["arc.task.controller", "arc.agent.caller"],
    "chat.start": ["arc.chat.controller", "arc.agent.caller"],
    "chat.message": ["arc.chat.controller", "arc.agent.caller"],
    "chat.end": ["arc.chat.controller", "arc.agent.caller"]
})
```

## Scope Validation

### Automatic Validation

Server automatically validates scopes when authentication is enabled:

```python
from arc import Server
from arc.auth import MultiProviderJWTValidator

validator = MultiProviderJWTValidator(providers={...})
server = Server(server_id="secure-server", enable_auth=True)
server.set_jwt_validator(validator)

# Scopes validated automatically
server.set_required_scopes({
    "task.create": ["arc.task.controller"]
})
```

### Error Handling

```python
from arc.exceptions import InsufficientScopeError

try:
    response = await client.task.create(...)
except InsufficientScopeError as e:
    print(f"Missing required scope: {e.message}")
    # Error code: -44003
```

## Custom Scopes

Define application-specific scopes:

```python
# Custom scopes for your application
server.set_required_scopes({
    "task.create": [
        "arc.task.controller",
        "app.finance.write"  # Custom scope
    ],
    "chat.start": [
        "arc.chat.controller",
        "app.support.access"  # Custom scope
    ]
})
```

## Per-Agent Authorization

Different authorization for different agents:

```python
@server.agent_handler("finance-agent", "chat.start")
async def finance_chat(params, context):
    # Validate custom scope
    if not has_scope(context, "app.finance.access"):
        raise InsufficientScopeError("Requires app.finance.access")
    
    return {...}

def has_scope(context: dict, required_scope: str) -> bool:
    token_scopes = context.get("scopes", [])
    return required_scope in token_scopes
```

## Role-Based Access Control

Implement RBAC using scopes:

```python
# Map roles to scopes
ROLE_SCOPES = {
    "admin": [
        "arc.task.controller",
        "arc.chat.controller",
        "arc.agent.caller",
        "app.admin.access"
    ],
    "user": [
        "arc.task.controller",
        "arc.chat.controller",
        "arc.agent.caller"
    ],
    "readonly": [
        "arc.task.info"
    ]
}

# Validate role-based access
@server.agent_handler("admin-agent", "chat.start")
async def admin_only(params, context):
    user_scopes = context.get("scopes", [])
    admin_scopes = ROLE_SCOPES["admin"]
    
    if not all(scope in user_scopes for scope in admin_scopes):
        raise AuthorizationError("Admin access required")
    
    return {...}
```

## Best Practices

1. **Principle of Least Privilege** - Grant minimum required scopes
2. **Scope Granularity** - Use fine-grained scopes for better control
3. **Audit Scopes** - Log scope usage for security monitoring
4. **Regular Review** - Periodically review and update scope assignments
5. **Document Scopes** - Clearly document scope meanings

## Error Codes

- `-44002` Authorization Failed - Insufficient permissions
- `-44003` Insufficient Scope - Required OAuth2 scope missing

## Links

- [Authentication](./authentication.md)
- [Python SDK Authentication](../../sdk/python/server/authentication.md)

