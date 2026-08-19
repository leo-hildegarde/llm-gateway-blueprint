# 10 — Capability expansion: grow deliberately

Once a gateway has routing, budgets, tools, monitoring, and automation, the main risk shifts: adding one more integration can break an existing path in ways that are hard to see from the diff alone.

The answer is not to stop expanding. It is to make expansion **staged, testable, and reversible**.

## Reliability before surface area

Before adding another capability, ask whether the existing control plane has enough test coverage to make the next change safely.

A useful rule is:

> If the system has shipped important untested behavior, add regression coverage before adding more surface area.

Good early targets are pure logic and previously observed failure modes:

- cache transitions after upstream failure
- destructive-action guards
- routing fallbacks and fail-open behavior
- report/digest generation from mocked telemetry
- malformed or missing configuration
- negative authorization paths

Tests do not need the full production dependency graph. For code that imports a heavy runtime package but exercises mostly local logic, small stubs/mocks can make the important behavior testable without live credentials or network access.

## Probe before implementation

Do not let an agent infer that a desired backend or protocol exists because it would be convenient.

For uncertain integrations, make the first slice a **probe or decision gate**:

```text
need capability
    |
    v
verify supported backend/API/transport
    |
    +--> supported -> record decision -> implement
    |
    +--> unsupported/unclear -> stop -> choose explicitly
```

The probe can be documentation-only. Its job is to answer the architectural question before implementation begins.

Once a backend decision is made, record it so future agents do not repeatedly reopen rejected alternatives unless new evidence justifies it.

## One shippable slice per change

Large capability waves become safer when decomposed into independently reviewable slices.

A common progression is:

1. regression/unit-test foundation;
2. backend/protocol decision;
3. service skeleton + health + read path;
4. scoped discovery and live read verification;
5. guarded writes in a separate change;
6. notifications/digests or higher-level automation only after the primitive capability is proven.

Each slice should have its own tests, rollout, and verification evidence. This makes failures cheaper to diagnose and prevents an ambitious roadmap from turning into one oversized PR.

## Pin third-party behavior you depend on

Sometimes an integration depends on a library or client that implements behavior the upstream vendor does not expose through a stable public interface.

Treat that dependency as part of your control plane:

- pin an exact version/commit rather than following a moving branch implicitly;
- record provenance and license;
- isolate the dependency behind a small service boundary;
- keep your wrapper/API surface smaller than the third-party library;
- test the behavior you depend on, especially parsing, boundary conditions, and error propagation;
- accept that upstream private/proprietary behavior may change and plan for replacement/update work.

Vendoring or forking can be reasonable when it makes the exact dependency auditable, but it also creates ownership: you now need to track upstream security and compatibility changes.

## Keep authentication state out of tool arguments

Some upstreams require an interactive bootstrap or session file instead of a static API key.

Prefer this model:

```text
human interactive login
        |
        v
protected local session state
        |
        v
internal capability service
        |
        v
MCP tools
```

Do not pass account passwords, MFA secrets, or other bootstrap credentials through model/tool arguments. The capability service should consume already-established session state with narrow filesystem permissions.

Health checks should also be precise about what they prove. The presence of session state can show that bootstrap occurred, but it may not prove the upstream session is currently valid. Let real tool calls surface revocation/auth failures unless a safe semantic health call exists.

## Validate context, not only values

Many write APIs need both a resource ID and the context that owns it: namespace, project, collection, calendar, account, region, or similar.

A valid identifier used in the wrong context can produce a misleading "not found" or target the wrong resource.

Tool contracts should therefore expose the context needed to reproduce the upstream lookup unambiguously, and live smoke tests should exercise non-default contexts when the API supports them.

## Time is part of the data model

Time-based integrations deserve explicit tests for:

- local timezone vs UTC storage
- offsets in user-visible confirmations
- all-day date stability across timezones
- inclusive/exclusive window boundaries
- recurrence boundaries
- configuration written during interactive bootstrap using the wrong host timezone

A system can successfully create the right instant and still show the user the wrong time. Confirmation rendering is part of correctness.

## Small durable mailboxes are often enough

Not every workflow needs a database or another LLM call.

For low-volume reminders, decisions, or queued notifications, a file-backed mailbox can be a good control-plane primitive when it has:

- validated IDs/paths
- atomic writes
- explicit status transitions
- a separate notifier/worker
- retry-on-send-failure semantics
- force-gated history purge
- tests using a temporary directory

Keeping the notifier separate from the MCP/tool service also preserves the capability/telemetry/policy separation: the tool mutates state; the worker reacts to state; neither needs to invoke an LLM.

## Public blueprint boundary

This chapter deliberately avoids naming real upstream services, accounts, repositories, ports, calendars, locations, credential formats, internal paths, tool inventories, or deployment commands.

The reusable lesson is the development method: **test before expanding, probe before choosing, stage reads before writes, constrain live writes, pin risky dependencies, and verify semantics after deployment.**
