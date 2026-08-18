# 09 — Capability discovery: treat the tool catalog as dynamic state

A tool-enabled client can fail even when every individual service is healthy.

One subtle failure mode is **capability discovery**: the client asks an aggregator for its available tools once at startup, receives an incomplete or empty result, caches it forever, and then behaves as if those capabilities do not exist.

Two different problems can stack here.

## Permissions are part of discovery

Per-client credentials improve least privilege, attribution, and budget isolation, but they can also change which tools a client is allowed to see.

A privileged administrative credential may discover every tool while a newly created application credential discovers none. Testing only with the administrative credential can therefore hide a real authorization problem.

Treat tool visibility as an explicit permission boundary:

- grant each client only the tool groups it needs
- test discovery using the same credential the real client uses
- enforce authorization on every tool call, not only when publishing the schema
- do not assume creating a scoped client key automatically grants tool access

The discovered schema is a user experience and routing surface; server-side authorization remains the security boundary.

## Startup readiness is not capability readiness

Container/process startup ordering does not guarantee that an aggregator has finished loading every downstream capability.

A client that performs a single discovery call during startup can legitimately see an empty catalog during a short readiness race. If that result is cached forever, a transient startup condition becomes a permanent feature outage.

A more resilient pattern is:

```text
client starts
    |
    v
discover capabilities
    |
    +--> healthy catalog -> cache + serve
    |
    +--> suspicious empty/incomplete result
              |
              v
        retry with backoff
              |
              v
        keep last-known-good catalog
              |
              v
        periodic refresh until converged
```

Useful safeguards include:

- retry initial discovery with bounded backoff
- refresh the catalog periodically rather than treating it as immutable
- retain a last-known-good catalog across clearly transient discovery failures
- warn when the catalog shrinks unexpectedly
- avoid replacing a healthy cache with an obviously broken empty response
- expose the last successful refresh time and catalog size for troubleshooting

Last-known-good caching is an **availability mechanism, not authorization**. The server must still validate the client's current permissions on every actual tool invocation, and refresh must eventually converge after deliberate revocation.

## Observe each capability independently

A large aggregate tool count is useful as a smoke signal, but it is not enough to prove a specific integration is healthy.

A better operational model gives important capabilities their own signals:

- discovery visibility for the scoped client that should see the capability
- exporter/upstream freshness where the integration has an independent telemetry path
- success/failure counters for refreshes or synchronization work
- alerting on stale data, not only complete process failure

This prevents a healthy-looking aggregate from hiding one broken integration. It also keeps capability health separate from authorization: "the server is healthy," "this client may see it," and "the data is fresh" are three different questions.

Where practical, keep telemetry narrower and less privileged than the tool surface. Monitoring should not need write-capable API credentials simply because the operational MCP does.

## Reconnect where the transport is owned

Some client transports or async sessions are owned by a particular task or event-loop context. A periodic health job should not blindly tear down and recreate that transport from an unrelated task.

A safer design is for monitoring code to signal that a reconnect is needed, while the task that owns the session performs the reconnect. This keeps connection lifecycle and concurrency ownership in one place.

The broader lesson is that capability catalogs are distributed state. They can be stale, partially initialized, permission-filtered, or temporarily unavailable. Treat discovery with the same care as any other control-plane cache: bounded retries, explicit authorization, health signals, refresh, and well-defined ownership.

The public blueprint intentionally leaves out production tool counts, server names, client identities, refresh intervals, permission mappings, and internal endpoints.
