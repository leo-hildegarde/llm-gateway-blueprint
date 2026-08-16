import asyncio

from src import auto_router


def test_short_plain_request_is_light():
    assert auto_router.choose_tier("Summarize this") == "light"


def test_medium_request_is_balanced():
    text = "Explain why centralizing LLM provider access can simplify client configuration and operations."
    assert auto_router.choose_tier(text) == "medium"


def test_code_or_architecture_request_is_heavy():
    assert auto_router.choose_tier("Debug this function:\n```python\ndef broken(): pass\n```") == "heavy"
    assert auto_router.choose_tier("Do a threat model for this architecture") == "heavy"


def test_long_request_is_heavy():
    assert auto_router.choose_tier("x" * 901) == "heavy"


def test_last_user_text_handles_multimodal_content():
    messages = [
        {"role": "assistant", "content": "Earlier answer"},
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": "https://example.invalid/image.png"}},
                {"type": "text", "text": "Explain this diagram"},
            ],
        },
    ]
    assert auto_router.last_user_text(messages) == "Explain this diagram"


def test_auto_hook_rewrites_only_chat_auto_requests(monkeypatch):
    monkeypatch.setitem(auto_router.TIERS, "heavy", "reasoning")
    hook = auto_router.AutoRouter()
    data = {
        "model": "auto",
        "messages": [{"role": "user", "content": "Debug this architecture"}],
    }

    result = asyncio.run(hook.async_pre_call_hook(None, None, data, "completion"))
    assert result["model"] == "reasoning"

    untouched = {"model": "balanced", "messages": data["messages"]}
    result = asyncio.run(hook.async_pre_call_hook(None, None, untouched, "completion"))
    assert result["model"] == "balanced"


def test_non_chat_auto_request_is_left_alone():
    hook = auto_router.AutoRouter()
    data = {"model": "auto", "messages": [{"role": "user", "content": "Debug this"}]}
    result = asyncio.run(hook.async_pre_call_hook(None, None, data, "embedding"))
    assert result["model"] == "auto"
