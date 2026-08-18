# 06 — Hardening: make the control plane safe to operate

A gateway concentrates power, so its security model matters more as features accumulate.

Use layers:

- secrets only through environment/secret stores
- internal services not bound to public interfaces
- read-only by default
- least-privilege tokens per integration
- separate client credentials where attribution, revocation, or budgets matter
- test capability discovery with the same scoped credentials real clients use; admin credentials can mask missing grants
- enforce tool authorization at invocation time, not only when publishing the tool schema
- explicit confirmation or force flags for destructive writes
- allowlists for actions with external side effects
- separate access tiers where different users need different tool surfaces
- auditable logs for every privileged operation

## Stronger confirmation for high-impact writes

A generic `force=true` flag is useful, but some actions deserve a second guard tied to the exact resource being changed.

For destructive or difficult-to-reverse operations, require both:

1. an explicit confirmation signal; and
2. a resource-specific value that proves the caller is targeting the intended object.

For example, a delete operation can require the caller to repeat a canonical resource identifier in addition to the confirmation flag. This reduces the chance that a stale tool call, ambiguous natural-language instruction, or mismatched selection deletes the wrong object.

The confirmation layer supplements authorization; it does not replace server-side permission checks.

Agentic automation needs additional controls because a small control-flow mistake can repeat side effects very quickly:

- use exact, unambiguous approval semantics
- consume approvals before starting the side effect so restarts cannot replay them
- cap runtime, steps/turns, and spend
- stop on non-zero agent exit or an empty patch
- prevent automation from recursively reacting to its own output
- never auto-merge a code-changing workflow just because the fixer completed

Ephemeral credentials should also stay ephemeral. A temporary Git credential helper, token file, or generated worktree should live in process/container temporary storage rather than a persistent state directory. Persistent or backup-synced directories should contain durable state, not regenerable clones or short-lived credential artifacts.

That separation improves both security and reliability: a root-owned temporary file or a large disposable worktree should not be able to interfere with an unrelated backup/sync process.

## Structured artifacts are data, too

Privacy review cannot stop at source files and environment variables.

Operational exports often contain the most identifying material in a repository precisely because they look like harmless supporting data. Treat these as sensitive until reviewed:

- JSON/YAML snapshots
- fixtures captured from a real environment
- dashboard exports
- metrics samples and debug dumps
- screenshots
- generated inventories and baselines
- copied API responses

Before publishing an artifact, ask whether it contains real client identifiers, account names, internal labels, hostnames, topology, timestamps that reveal operations, or stable IDs that can be correlated elsewhere.

Prefer synthetic examples over redacted production snapshots. If a real structure is useful to demonstrate, recreate a minimal fixture with invented values rather than deleting a few obvious fields from an operational export.

The public/private split is part of this hardening. Publishing architecture should never publish production recoverability information, exact budget thresholds, repository allowlists, notification identities, permission maps, tool inventories, operational snapshots, or deployment-specific control-plane endpoints.
