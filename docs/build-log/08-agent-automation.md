# 08 — Agent automation: bound the loop before you automate the fixer

Once a coding agent can react to review findings, push branches, and open pull requests, the interesting problem is no longer whether the agent can edit code. It is whether the automation can stop itself.

A useful review-fixer loop looks like this:

```text
review finding
      |
      v
watcher detects unresolved thread
      |
      v
human approval
      |
      v
coding agent patches reviewed code
      |
      v
opens follow-up PR
      |
      v
human / CI / review decides what happens next
```

Nothing auto-merges.

The failure modes are mostly control-flow failures rather than model-quality failures.

## Guard 1: never fix your own fixer forever

If a review bot comments on a PR created by the fixer, a naive watcher can create a fix for the fix, then another fix for that fix.

Mark or namespace automation-created branches and explicitly ignore them in the watcher. Recursion prevention should be a deterministic rule, not a prompt instruction.

## Guard 2: approval must be unambiguous

Do not treat the presence of a word such as `go` or `ok` anywhere in a reply as authorization. A sentence like "don't go" must not trigger a side effect.

Normalize the reply and accept only a small set of exact affirmative responses. For higher-impact operations, use an even stronger confirmation mechanism.

## Guard 3: consume approval before the side effect

Persist that an approval has been consumed before launching the agent or creating external state. If the process crashes halfway through, a restart must not replay the same authorization and create duplicate work.

## Guard 4: patch the code that was actually reviewed

For an open PR, the findings refer to the PR head, not necessarily `main`. The fixer should check out the reviewed ref and target the originating branch.

For a finding that arrives after merge, start from the current default branch instead.

This sounds small, but getting the base ref wrong can produce a technically valid fix for code that no longer matches the review.

## Guard 5: failure must stop the workflow

If the coding agent exits non-zero, times out, or produces no diff, stop. Do not continue to push or open a PR just because later steps are available.

Bound every run with controls such as:

- wall-clock timeout
- turn or step cap
- spend cap
- explicit repository allowlist
- no automatic merge

## Guard 6: bound the watcher itself

Automation that polls external systems also needs limits:

- paginate rather than assuming the first page is complete
- stop scanning once results are outside the relevant activity window
- retain new findings that arrive while a decision is pending
- deduplicate already-seen findings

The broader lesson is that agentic workflows need the same engineering disciplines as distributed systems: idempotency, bounded retries, explicit state transitions, least privilege, and human gates around meaningful side effects.

The public blueprint keeps this pattern generic. It deliberately omits production repository names, agent profiles, notification channels, model choices, credentials, and operational thresholds.
