# 05 — Reliability: design around real failure modes

The interesting engineering starts after the happy path works.

Topics worth demonstrating:

- upstream requests that take much longer than expected
- timeouts that need a fallback rather than a blank error
- health checks that validate the application layer, not only an open TCP port
- background work that outlives a synchronous chat turn
- incomplete tool-call history after cancellation or restart
- provider-specific quirks that should stay behind the gateway

## Separate capabilities, telemetry, and policy

An operational integration is easier to reason about when it is split into three planes instead of one all-powerful service:

1. **Capability plane** — the MCP/tool surface that performs reads and guarded writes against the upstream service.
2. **Telemetry plane** — a narrow exporter that turns upstream state into metrics without exposing the full tool surface.
3. **Policy plane** — alerts, dashboards, anomaly rules, and periodic summaries that consume telemetry and decide when a human needs attention.

This separation reduces coupling and blast radius. A monitoring outage should not remove tool access, and a tool-session failure should not erase the last independently collected health signal. The telemetry path also should not need privileged write credentials merely because the tool path does.

For higher-impact integrations, keep notification/reporting logic downstream of metrics where practical. A periodic hygiene summary and an immediate anomaly alert answer different questions and can evolve independently.

## Freshness is part of health

A process can be alive and still be lying by omission.

An exporter that keeps serving its last successful values after upstream refreshes fail may look healthy to a naive `up` check. That creates a dangerous state: dashboards are available, metrics are parseable, and the data is stale.

Treat freshness as a first-class health dimension:

- expose the timestamp or age of the last successful upstream refresh
- mark refresh failures explicitly instead of silently retaining a healthy state
- alert on stale data as well as process unreachability
- distinguish "time series exists" from "meaningful activity occurred" when writing monitoring queries
- verify semantic values after rollout, not merely that a scrape endpoint returns HTTP 200

Last-known-good values can still be useful for continuity, but they must be labeled as stale rather than masquerading as current truth.

## Configuration rollout is part of reliability

A correct configuration file can still cause an outage if the rollout mechanism behaves differently from what you assumed.

Two useful examples generalize well:

### Dependency recreation can be a hidden side effect

Container orchestration commands that appear to add or rebuild one service can also recreate a dependency when shared environment/configuration inputs changed.

Before applying a change to an auxiliary integration:

- inspect what the orchestration command plans to recreate
- treat changes to shared environment files as gateway-impacting changes
- keep auxiliary monitoring/reporting services out of the critical gateway dependency graph when they do not truly depend on it
- announce or schedule restarts of critical services rather than discovering them as a side effect
- verify application-level health after the rollout

The lesson is simple: deployment dependencies are part of the blast radius, even when the code change is not.

### A successful reload does not prove new configuration was loaded

Single-file bind mounts can interact badly with editors or deployment tools that update files using atomic rename. The process inside the container may remain attached to the old inode while the host path points to new bytes. A reload signal can then succeed while the service continues using stale configuration.

Do not use "reload returned success" as the verification step. Check the effective runtime state instead: active targets, loaded routes, rendered configuration, health endpoints, or another semantic signal that proves the new configuration is actually in use.

Prefer mounting a configuration directory or replacing the container when that makes configuration identity clearer.

A good post should include at least one failure that changed the architecture. That makes the build credible and teaches more than a final diagram.
