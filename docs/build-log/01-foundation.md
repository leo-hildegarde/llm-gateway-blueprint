# 01 — Foundation: one gateway, one API

The first version should be boring: a LiteLLM proxy, one database, and two or three provider routes.

The important design decision is not Docker. It is **centralization**. Once every client talks to one OpenAI-compatible endpoint, provider credentials, model naming, logging and policy move out of individual applications.

### What to show in a blog post

- the before/after client configuration
- the first request through the proxy
- why the gateway becomes a control plane rather than just a proxy
- the trade-off: a new central dependency must now be operated reliably
