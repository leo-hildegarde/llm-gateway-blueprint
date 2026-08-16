"""Task-aware LiteLLM pre-call router for the public blueprint.

Expose a stable model name such as `auto`, classify the request into a
capability tier, then rewrite the target before the provider call. This demo
uses deterministic heuristics so the behavior is easy to test and explain.

The hook is deliberately fail-open: routing policy must not become the reason a
normal completion request fails.
"""

from __future__ import annotations

import logging
import os
import re

from litellm.integrations.custom_logger import CustomLogger

log = logging.getLogger("blueprint.auto_router")

TARGET = "auto"
CHAT_CALL_TYPES = {"completion", "acompletion", "text_completion", "atext_completion"}
TIERS = {
    "light": os.getenv("AUTO_TIER_LIGHT", "fast"),
    "medium": os.getenv("AUTO_TIER_MEDIUM", "balanced"),
    "heavy": os.getenv("AUTO_TIER_HEAVY", "reasoning"),
}

HEAVY_HINTS = re.compile(
    r"\b(debug|architecture|design review|root cause|prove|optimi[sz]e|migration|threat model)\b",
    re.IGNORECASE,
)
CODE_HINTS = re.compile(
    r"```|\b(class|def|function|SELECT|FROM|terraform|kubernetes)\b",
    re.IGNORECASE,
)


def last_user_text(messages: list[dict] | None) -> str:
    """Return text from the most recent user message, including multimodal text parts."""
    for message in reversed(messages or []):
        if not isinstance(message, dict) or message.get("role") != "user":
            continue

        content = message.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = [
                part.get("text", "")
                for part in content
                if isinstance(part, dict) and part.get("type") == "text"
            ]
            return " ".join(part for part in parts if part)
    return ""


def choose_tier(text: str) -> str:
    """Classify text into a simple capability tier.

    Explicit heavy/code signals take precedence over the short-request fast
    path. A short threat-model or debugging request is still a heavy task.
    """
    clean = text.strip()
    if len(clean) > 900 or HEAVY_HINTS.search(clean) or CODE_HINTS.search(clean):
        return "heavy"
    if len(clean) <= 40:
        return "light"
    return "medium"


class AutoRouter(CustomLogger):
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        try:
            if not isinstance(data, dict) or data.get("model") != TARGET:
                return data
            if call_type not in CHAT_CALL_TYPES:
                return data

            text = last_user_text(data.get("messages"))
            if not text.strip():
                return data

            tier = choose_tier(text)
            target = TIERS.get(tier)
            if not target:
                return data

            log.info("auto -> %s (tier=%s)", target, tier)
            data["model"] = target
            return data
        except Exception as exc:  # routing policy must never break the request
            log.warning("auto router failed open: %s", exc)
            return data


auto_router_instance = AutoRouter()
