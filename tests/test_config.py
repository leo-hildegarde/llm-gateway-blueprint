from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]


def load_config():
    return yaml.safe_load((ROOT / "config" / "litellm.yaml").read_text())


def test_public_aliases_are_present():
    config = load_config()
    names = [entry["model_name"] for entry in config["model_list"]]
    assert {"fast", "balanced", "reasoning", "auto"}.issubset(names)


def test_provider_credentials_come_from_environment():
    config = load_config()
    for entry in config["model_list"]:
        assert entry["litellm_params"]["api_key"] == "os.environ/OPENAI_API_KEY"


def test_fallbacks_degrade_capability():
    config = load_config()
    fallbacks = config["router_settings"]["fallbacks"]
    assert {"reasoning": ["balanced"]} in fallbacks
    assert {"balanced": ["fast"]} in fallbacks


def test_auto_router_and_spend_mcp_are_registered():
    config = load_config()
    assert "auto_router.auto_router_instance" in config["litellm_settings"]["callbacks"]
    assert config["mcp_servers"]["spend"]["url"] == "http://spend-mcp:8000/mcp"


def test_no_old_provider_placeholders_remain():
    text = (ROOT / "config" / "litellm.yaml").read_text()
    assert "provider-a/" not in text
    assert "replace-with-fast-model" not in text
