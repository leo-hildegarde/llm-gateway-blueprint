# 05 — Reliability: design around real failure modes

The interesting engineering starts after the happy path works.

Topics worth demonstrating:

- upstream requests that take much longer than expected
- timeouts that need a fallback rather than a blank error
- health checks that validate the application layer, not only an open TCP port
- background work that outlives a synchronous chat turn
- incomplete tool-call history after cancellation or restart
- provider-specific quirks that should stay behind the gateway

A good post should include at least one failure that changed the architecture. That makes the build credible and teaches more than a final diagram.
