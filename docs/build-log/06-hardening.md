# 06 — Hardening: make the control plane safe to operate

A gateway concentrates power, so its security model matters more as features accumulate.

Use layers:

- secrets only through environment/secret stores
- internal services not bound to public interfaces
- read-only by default
- least-privilege tokens per integration
- explicit confirmation or force flags for destructive writes
- allowlists for actions with external side effects
- separate access tiers where different users need different tool surfaces
- auditable logs for every privileged operation

The public/private split is part of this hardening. Publishing architecture should never publish production recoverability information.
