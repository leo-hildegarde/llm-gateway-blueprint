# Pre-publication checklist

Use this before changing the repository visibility from private to public.

## Provenance

- [ ] Repository is a clean-room implementation, not a fork or filtered clone of the production repository.
- [ ] No production Git objects, branches, tags, or copied commit messages were imported.
- [ ] New material was written from architectural concepts rather than copied from operational recovery documentation.

## Secrets and identifiers

- [ ] `bash scripts/public-safety-check.sh` passes.
- [ ] `.env` and other local credential files remain ignored.
- [ ] `.env.example` contains placeholders only.
- [ ] No real API tokens, private keys, passwords, chat/user IDs, email addresses, account IDs, or customer identifiers appear in the tree.
- [ ] No private IP addresses, mesh/VPN DNS names, internal hostnames, or absolute production filesystem paths appear in the tree.
- [ ] CI/log examples do not contain real request headers, prompts, responses, or credential-bearing URLs.

## Architecture disclosure

- [ ] Public diagrams describe patterns, not the production network topology.
- [ ] Tool examples use generic responsibilities rather than publishing an inventory of private operational systems.
- [ ] Backup, disaster-recovery, firewall, identity, and remote-access details stay out unless intentionally disclosed.
- [ ] Production schedules, retention values, ports, and deployment-specific service names are not copied into examples.

## Code quality

- [ ] GitHub Actions is green.
- [ ] `docker compose config` succeeds with `.env.example` copied to `.env`.
- [ ] Unit/config tests pass.
- [ ] Public container/action dependencies are pinned to reviewed versions or immutable commits where practical.
- [ ] Read-only examples do not imply production-grade least privilege where the tutorial intentionally simplifies credentials.

## Content review

- [ ] Screenshots, if added later, are reviewed separately for browser tabs, URLs, usernames, hostnames, notifications, and metadata.
- [ ] Links in the article point only to resources intended to become public.

## Final release

- [ ] Review the complete PR diff, not just individual files.
- [ ] Merge only after CI and manual review are both clean.
- [ ] Re-run the safety workflow on `main` after merge.
- [ ] Only then change repository visibility to public.

If there is any doubt that a credential or identifier was ever committed, rotate it before publication rather than relying on Git history cleanup.
