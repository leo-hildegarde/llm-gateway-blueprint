# Public / private security boundary

This repository exists to explain a system, not to recover or reproduce a specific production host.

## Safe to publish

- generic architecture and data flow
- synthetic model aliases
- localhost Docker networking
- placeholder environment-variable names
- generic routing and fallback patterns
- deliberately minimal read-only MCP examples
- lessons learned after removing identifiers and operational detail

## Keep private

- real IP addresses, overlay-network addresses, FQDNs, SSH names or host aliases
- filesystem paths that reveal usernames, project names, mount points or backup layout
- chat IDs, bot usernames, email addresses, DNS zones and account IDs
- exact backup destinations, retention jobs, restore keys or disaster-recovery locations
- provider account structure and token scopes unless the example is intentionally generic
- production allowlists, trusted-recipient lists and family/admin identifiers
- real dashboard URLs or monitoring endpoints
- any Git history inherited from the private repository

## Clean-room rule

Do not copy a file and redact it. Recreate the public file from the concept you want to teach.

Redaction tends to preserve structure you forgot was sensitive: naming conventions, internal topology, comments, paths, identifiers, disabled configuration, and historical mistakes.

## Release checklist

- run `scripts/public-safety-check.sh`
- inspect `git diff` manually
- search for personal names and usernames
- search for domains, IPv4/IPv6 addresses and absolute paths
- verify `.env` is ignored
- inspect screenshots for hostnames, account names, spend values and browser tabs
- publish from a repository with fresh history
