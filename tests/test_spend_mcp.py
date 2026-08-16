from decimal import Decimal
import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parents[1] / "mcp" / "spend" / "server.py"
spec = importlib.util.spec_from_file_location("blueprint_spend_server", MODULE_PATH)
server = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(server)


def test_query_window_is_bounded():
    assert server.clamp_days(-50) == 1
    assert server.clamp_days(7) == 7
    assert server.clamp_days(500) == 90


def test_spend_values_are_json_friendly():
    assert server.as_float(Decimal("1.25")) == 1.25
    assert server.as_float(None) == 0.0


def test_database_url_is_required(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="DATABASE_URL is required"):
        server.database_url()


def test_database_url_reads_environment(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://demo.invalid/example")
    assert server.database_url() == "postgresql://demo.invalid/example"
