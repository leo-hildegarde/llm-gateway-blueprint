# Architecture

The gateway pattern starts with one constraint: clients should not need to know which provider serves a request.

## Control points

1. **Single API surface** — clients use one OpenAI-compatible endpoint.
2. **Model aliases** — names such as `fast`, `balanced`, `reasoning`, and `auto` decouple clients from provider model IDs.
3. **Routing** — policy lives at the gateway, not in every client.
4. **Fallbacks** — upstream failure can move to another capability tier or provider.
5. **Persistence** — usage and spend are written to Postgres.
6. **Tools** — operational capabilities are exposed through narrow MCP services.
7. **Observability** — the gateway is the best place to measure latency, cost, errors, and provider health.

## Why MCP services are separate

Keep operational tools small and explicit. A read-only spend service should not also have DNS or GitHub write privileges. Separate services make privilege boundaries visible and easier to explain.
