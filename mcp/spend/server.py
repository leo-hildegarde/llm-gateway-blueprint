"""Read-only spend MCP example.

This intentionally exposes aggregate operational data only. The query targets
LiteLLM's request-level spend log table and returns no prompts, responses, API
keys, user identifiers, or raw request metadata.
"""

from __future__ import annotations

import os
from decimal import Decimal

import psycopg
from mcp.server import MCPServer

mcp = MCPServer("spend-readonly")


def database_url() -> str:
    value = os.getenv("DATABASE_URL", "").strip()
    if not value:
        raise RuntimeError("DATABASE_URL is required")
    return value


def clamp_days(days: int) -> int:
    """Keep query windows bounded even if a caller passes an extreme value."""
    return max(1, min(int(days), 90))


def as_float(value) -> float:
    if isinstance(value, Decimal):
        return float(value)
    return float(value or 0)


@mcp.tool()
def health() -> dict:
    """Confirm that the MCP service can reach Postgres."""
    with psycopg.connect(database_url()) as conn, conn.cursor() as cur:
        cur.execute("SELECT 1")
        row = cur.fetchone()
    return {"ok": bool(row and row[0] == 1)}


@mcp.tool()
def spend_summary(days: int = 7) -> dict:
    """Return aggregate calls, tokens, and spend for the previous N days."""
    days = clamp_days(days)
    query = """
        SELECT
            COUNT(*) AS calls,
            COALESCE(SUM(total_tokens), 0) AS total_tokens,
            COALESCE(SUM(spend), 0) AS spend
        FROM "LiteLLM_SpendLogs"
        WHERE "startTime" >= NOW() - (%s || ' days')::interval
    """
    with psycopg.connect(database_url()) as conn, conn.cursor() as cur:
        cur.execute(query, (days,))
        calls, total_tokens, spend = cur.fetchone()

    return {
        "days": days,
        "calls": int(calls or 0),
        "total_tokens": int(total_tokens or 0),
        "spend_usd": as_float(spend),
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        stateless_http=True,
        json_response=True,
    )
