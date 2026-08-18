# 04 — Tools: add capabilities without making the gateway omnipotent

MCP makes it tempting to attach every operational system directly to the agent. Resist that.

Start with read-only tools that have narrow data access. Spend queries are a good example: useful to every client, low-risk, and easy to audit.

For write-capable tools, use explicit scopes, allowlists, confirmation gates and separate services. A tool that can read monitoring data should not automatically inherit the ability to modify DNS, merge code or send mail.

## Separate control from observability

A useful external-integration pattern is to expose two different surfaces:

```text
agent / human client --> MCP adapter --> upstream API

monitoring system --> metrics exporter --> upstream API
```

The MCP adapter exists for on-demand reads and carefully gated actions. The exporter exists for low-cardinality, scrape-friendly health and activity metrics. Dashboards should not need to invoke agent tools, and an agent should not need broad monitoring credentials just to perform one scoped action.

Keeping the two paths separate makes it easier to reason about permissions, rate limits, caching and failure modes.

## Keep upstream quirks behind the adapter

Third-party APIs often have unusual authentication headers, pagination rules, identifiers or response shapes. Clients should not need to know any of that. Normalize those quirks inside the adapter so the gateway exposes a stable tool contract.

This is the same reason model-provider differences belong behind routing aliases: compatibility logic should live at the boundary, not leak into every client.

## Match confirmation strength to impact

Not all writes deserve the same gate. Reversible changes can use a lighter confirmation policy, while destructive or difficult-to-recover operations should require stronger proof of intent.

For a destructive action, a useful pattern is to require both:

- an explicit force/confirm flag; and
- the exact human-readable target identifier, not only an opaque numeric ID.

That makes accidental or hallucinated destructive calls less likely to succeed.

## Scope capabilities per client

Tool discovery is also an authorization boundary. A client key should see only the integrations and operations it is allowed to invoke.

Test this with the same scoped credential used by the real application. Testing only with an administrative key can hide missing grants or accidentally over-broad access.

The server must still authorize every invocation; hiding a tool from discovery is useful least privilege, but it is not the enforcement mechanism by itself.

## Make monitoring polite to upstream APIs

Exporters should not hammer an upstream API on every scrape. A short cache, explicit fetch-age metric and background warm-up can keep monitoring responsive while bounding upstream traffic.

As with the rest of this blueprint, the public example should describe the pattern without publishing real integration inventories, account data, tool grants or operational identifiers.
