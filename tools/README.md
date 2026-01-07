# ARC Protocol Tools

Specification maintenance and generation tools for the ARC Protocol. Not for end-user consumption.

## Purpose

These tools maintain the ARC Protocol specification:

1. Generate TypeScript types from OpenAPI schema
2. Convert OpenAPI to OpenRPC format
3. Validate schema correctness
4. Provide minimal reference implementations

For production SDKs, see [Python SDK](https://github.com/arcprotocol/python-sdk).

## Available Commands

### Generate TypeScript Types

```bash
npm run generate:types
```

**Input**: `spec/versions/v1.0/arc-openapi.yaml`  
**Output**: `tools/types/generated.ts`

### Generate OpenRPC Schema

```bash
npm run generate:openrpc
```

**Input**: `spec/versions/v1.0/arc-openapi.yaml`  
**Output**: `spec/versions/v1.0/arc-openrpc.json`

### Generate All

```bash
npm run generate:all
```

### Validate Schema

```bash
npm run validate
```

## Development Workflow

### Modifying Schema

1. Edit `spec/versions/v1.0/arc-openapi.yaml`
2. Run `npm run generate:all`
3. Verify `tools/types/generated.ts`
4. Update `spec/arc-specification.md`
5. Run `npm test`

### Updating Generators

1. Edit scripts in `utils/`
2. Test with `npm run generate:all`
3. Verify outputs
4. Update documentation

## Tools

### schema-to-types.ts

Generates TypeScript type definitions from OpenAPI schema for type safety and IDE support.

### schema-to-openrpc.ts

Converts OpenAPI schema to OpenRPC format for RPC-focused tooling compatibility.

### validate-schema.ts

Validates OpenAPI schema structure, references, and type consistency.

## Testing

```bash
npm test              # Run all tests
npm run lint          # TypeScript linting
npm run format        # Code formatting
```

## Important

**These are specification tools, not an SDK.**

- Do not import these in applications
- Do not use reference implementations in production
- Use for specification maintenance only

For implementation, use the [Python SDK](https://github.com/arcprotocol/python-sdk) or implement from the [specification](../spec/arc-specification.md).