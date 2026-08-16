# 04 — Tools: add capabilities without making the gateway omnipotent

MCP makes it tempting to attach every operational system directly to the agent. Resist that.

Start with read-only tools that have narrow data access. Spend queries are a good example: useful to every client, low-risk, and easy to audit.

For write-capable tools, use explicit scopes, allowlists, confirmation gates and separate services. A tool that can read monitoring data should not automatically inherit the ability to modify DNS, merge code or send mail.
