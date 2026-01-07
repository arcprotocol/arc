# TypeScript Examples

This directory contains TypeScript examples demonstrating the ARC Protocol implementation.

## Documentation

For more information:
- [ARC Protocol Specification](../../spec/arc-specification.md)
- [Python SDK](https://github.com/arcprotocol/python-sdk)

## Quick Start

### Install Dependencies

```bash
npm install
```

### Run Examples

Start the multi-agent server:

```bash
npx ts-node multi-agent-server.ts
```

In another terminal, run the client:

```bash
npx ts-node client-basic.ts
```

## Examples

### Server Examples

- **`server-basic.ts`** - Single agent server implementation
- **`multi-agent-server.ts`** - Travel & booking platform with multiple agents (flight-finder, hotel-booking, itinerary-planner, price-tracker)

### Client Examples

- **`client-basic.ts`** - Basic client demonstrating task.create, task.info, chat.start, and chat.message

## Notes

These examples use raw HTTP and Node.js `http` module to demonstrate the protocol clearly without external dependencies.

For production use, consider using the Python SDK which provides a full-featured implementation.
