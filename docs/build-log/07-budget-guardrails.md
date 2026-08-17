# 07 — Budget guardrails: contain cost before a runaway reaches the ceiling

Once a gateway centralizes spend, cost control can become an enforcement layer rather than a dashboard.

The useful pattern has two layers.

## Layer 1: isolate clients and give each one a budget

Do not let every client share the gateway's administrative key. Give each workload its own virtual key or equivalent identity, then attach a soft alert threshold and a hard budget ceiling.

That gives you:

- attribution: which client created the spend
- blast-radius reduction: one runaway workload cannot consume the entire account budget
- independent rotation and revocation
- policy that can differ by workload
- a clean place to attach alerts

The administrative key should stay administrative. Application traffic should use narrower client credentials.

## Layer 2: detect derailment before the hard cap

A daily ceiling is necessary, but it reacts late. A lightweight watchdog can look for traffic patterns that usually indicate a stuck agent or accidental fan-out.

Useful signals include:

1. **Repeated-request loops** — many calls from one client with the same coarse fingerprint over a short window. If prompt bodies are intentionally not stored, metadata such as `(model, prompt_tokens)` can be used as an imperfect signal rather than retaining prompt contents.
2. **Spend velocity** — recent spend consumes an unusually large fraction of that client's daily budget.
3. **Sustained request fan-out** — requests per minute stay far above the expected interactive rate for several complete windows.

These are heuristics, not proof of an incident. False positives are possible, so the detector should create a decision rather than immediately perform a destructive action.

## Human-gated containment

A safer flow is:

```text
spend database
      |
      v
pure heuristic detector
      |
      v
alert / decision request
      |
      +--> reject -> keep key active
      |
      +--> approve -> block the affected client key
```

Important properties:

- the detector itself makes no LLM calls
- blocking requires an explicit approval
- approval parsing is strict rather than substring-based
- the administrative/master credential is alert-only, never automatically blocked
- alerts have per-client cooldowns
- each polling cycle has a flood cap
- manually unblocked clients can re-arm cleanly
- the detector operates on aggregate metadata rather than prompt/response bodies

## Make the guardrail observable too

A protection loop that silently stops running is only a policy on paper. Treat the watchdog itself as something that needs health and outcome signals.

Useful operational signals include:

- whether the detector is up
- age and success/failure of the last completed cycle
- cumulative cycle errors
- pending human decisions
- currently contained client identities
- recent alerts grouped by signal type

Persist a small alert history with outcomes such as approved containment, rejected containment, expiry, or failed enforcement. That makes it possible to answer not only “did the detector fire?” but also “what happened next?”.

Telemetry should be **best effort**. If writing an alert-history row or exporting a metric fails, the protection path should still evaluate traffic and raise the decision. Observability must not become a dependency that disables enforcement.

Finally, keep the monitoring view and detector on one source of truth. A chart showing “percent of trip threshold” must use the same effective thresholds as the watchdog. Duplicating limits in dashboard configuration creates policy drift and misleading status.

This is a good example of the gateway becoming a control plane: routing decides **where** work runs, while budget policy decides **how much damage a broken workload is allowed to cause**.

The public blueprint intentionally leaves out production thresholds, client names, notification channels, account structure, and operational endpoints. Those values are deployment policy, not architecture.
