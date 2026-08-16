# 03 — Routing: stable aliases instead of provider names

Clients should ask for a capability, not a vendor SKU.

This blueprint uses `fast`, `balanced`, `reasoning`, and `auto` as examples. The `auto` route demonstrates a policy hook that decides which tier should handle a request.

### Evolution worth writing about

1. manual model selection
2. stable aliases
3. provider fallbacks
4. task-aware routing
5. routing informed by latency, reliability and cost

The lesson is that routing policy becomes a product of its own. Treat it as code, test it, and make failure fall back to a safe default rather than breaking the request.
