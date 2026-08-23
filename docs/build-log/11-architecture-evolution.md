# 11 — Separating Model Access from Tool Access

## The original assumption

The early design treated the gateway as the primary path for both model inference and tool/service access.

That is a useful starting point, but it can create unnecessary coupling between model authentication, provider limits, fallback behavior, tool access, and spend accounting.

## The evolution

As the system matured, the architecture was deliberately simplified by separating two concerns:

- **Model access** — a client may use a provider-native runtime when that is the clearer and more reliable path.
- **Tool and service access** — MCP tools and service integrations can remain behind the LLM gateway, where centralized policy, observability, routing, and access control provide value.

The gateway therefore remains an important control plane without becoming a mandatory inference proxy for every client.

## Why this is useful

This separation can provide:

- clearer credential boundaries;
- deterministic provider behavior and failure semantics;
- less coupling between subscriptions, provider limits, and tool access;
- a smaller gateway responsibility surface;
- centralized control where it actually adds value.

It also makes failure behavior easier to reason about. A provider-native model runtime can have its own subscription and limit semantics without requiring the gateway to emulate or proxy them.

## What changed in the blueprint

The reference architecture now shows two possible paths:

```text
Native client ──────────────> Model provider
      │
      └──── MCP / tools ────> LLM gateway ────> Services / integrations
```

The original gateway inference path remains part of the runnable example because it is useful for demonstrating centralized routing, fallbacks, usage tracking, and policy.

The important change is that it is no longer presented as a requirement for every client.

## Spend tracking scope

Gateway-side spend tracking remains useful for traffic that actually traverses the gateway.

It should not be presented as a universal accounting layer for all LLM usage. A client using a provider-native model/runtime path may have usage and subscription semantics that are outside the gateway's visibility.

This distinction prevents an observability feature from creating a false impression of complete cost accounting.

## General lesson

A gateway should centralize the concerns that benefit from centralization.

It does not need to proxy every request simply because it can.

Architecture should evolve toward fewer unnecessary dependencies and clearer boundaries, even when that means removing a capability from the gateway's critical path.

## Public-safety boundary

This chapter intentionally describes the architectural decision without publishing provider account details, subscription identifiers, credentials, private endpoints, internal service names, production limits, or operational topology.
