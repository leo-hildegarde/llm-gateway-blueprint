# 06 — Hardening: make the control plane safe to operate

A gateway concentrates power, so its security model matters more as features accumulate.

Use layers:

- secrets only through environment/secret stores
- internal services not bound to public interfaces
- read-only by default
- least-privilege tokens per integration
- separate client credentials where attribution, revocation, or budgets matter
- explicit confirmation or force flags for destructive writes
- allowlists for actions with external side effects
- separate access tiers where different users need different tool surfaces
- auditable logs for every privileged operation

Agentic automation needs additional controls because a small control-flow mistake can repeat side effects very quickly:

- use exact, unambiguous approval semantics
- consume approvals before starting the side effect so restarts cannot replay them
- cap runtime, steps/turns, and spend
- stop on non-zero agent exit or an empty patch
- prevent automation from recursively reacting to its own output
- never auto-merge a code-changing workflow just because the fixer completed

Ephemeral credentials should also stay ephemeral. A temporary Git credential helper, token file, or generated worktree should live in process/container temporary storage rather than a persistent state directory. Persistent or backup-synced directories should contain durable state, not regenerable clones or short-lived credential artifacts.

That separation improves both security and reliability: a root-owned temporary file or a large disposable worktree should not be able to interfere with an unrelated backup/sync process.

The public/private split is part of this hardening. Publishing architecture should never publish production recoverability information, exact budget thresholds, repository allowlists, notification identities, or deployment-specific control-plane endpoints.
