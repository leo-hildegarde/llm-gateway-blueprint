# Publishing plan: make Git history part of the story

When this becomes a GitHub repository, do not upload every file in one initial commit. Build the public history intentionally so readers can follow the architecture growing.

## Suggested commits / tags

| Stage | Commit message | Public tag |
|---|---|---|
| 1 | `foundation: add LiteLLM gateway and Postgres` | `part-1-foundation` |
| 2 | `routing: add stable model aliases and fallbacks` | `part-2-routing` |
| 3 | `routing: add task-aware auto model` | `part-3-auto-routing` |
| 4 | `tools: add read-only spend MCP service` | `part-4-mcp` |
| 5 | `reliability: add application health checks` | `part-5-reliability` |
| 6 | `security: add public/private boundary and leak checks` | `part-6-hardening` |
| 7 | `docs: add build story and publishing material` | `part-7-story` |

## Why this is safer than copying production history

A private infrastructure repository's old commits may contain values that were later removed, debugging output, identifiers in commit messages, screenshots, deleted files or implementation details that should remain private.

A new public history documents only the lessons you intentionally chose to publish.
