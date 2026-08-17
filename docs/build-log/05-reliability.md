# 05 — Reliability: design around real failure modes

The interesting engineering starts after the happy path works.

Topics worth demonstrating:

- upstream requests that take much longer than expected
- timeouts that need a fallback rather than a blank error
- health checks that validate the application layer, not only an open TCP port
- background work that outlives a synchronous chat turn
- incomplete tool-call history after cancellation or restart
- provider-specific quirks that should stay behind the gateway

## Configuration rollout is part of reliability

A correct configuration file can still cause an outage if the rollout mechanism behaves differently from what you assumed.

Two useful examples generalize well:

### Dependency recreation can be a hidden side effect

Container orchestration commands that appear to add or rebuild one service can also recreate a dependency when shared environment/configuration inputs changed.

Before applying a change to an auxiliary integration:

- inspect what the orchestration command plans to recreate
- treat changes to shared environment files as gateway-impacting changes
- announce or schedule restarts of critical services rather than discovering them as a side effect
- verify application-level health after the rollout

The lesson is simple: deployment dependencies are part of the blast radius, even when the code change is not.

### A successful reload does not prove new configuration was loaded

Single-file bind mounts can interact badly with editors or deployment tools that update files using atomic rename. The process inside the container may remain attached to the old inode while the host path points to new bytes. A reload signal can then succeed while the service continues using stale configuration.

Do not use "reload returned success" as the verification step. Check the effective runtime state instead: active targets, loaded routes, rendered configuration, health endpoints, or another semantic signal that proves the new configuration is actually in use.

Prefer mounting a configuration directory or replacing the container when that makes configuration identity clearer.

A good post should include at least one failure that changed the architecture. That makes the build credible and teaches more than a final diagram.
