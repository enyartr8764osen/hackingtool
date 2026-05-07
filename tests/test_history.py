import json
import os
import pytest

import core.history as history_mod


@pytest.fixture(autouse=True)
def tmp_history(tmp_path, monkeypatch):
    hist_file = tmp_path / "history.json"
    monkeypatch.setattr(history_mod, "HISTORY_FILE", str(hist_file))
    yield hist_file


def test_get_history_empty():
    assert history_mod.get_history() == []


def test_record_run_adds_entry():
    history_mod.record_run("nmap", "Network", True)
    h = history_mod.get_history()
    assert len(h) == 1
    assert h[0]["tool"] == "nmap"
    assert h[0]["category"] == "Network"
    assert h[0]["success"] is True
    assert "timestamp" in h[0]


def test_record_run_multiple():
    history_mod.record_run("nmap", "Network", True)
    history_mod.record_run("sqlmap", "Web", False)
    h = history_mod.get_history()
    assert len(h) == 2
    assert h[1]["tool"] == "sqlmap"


def test_record_run_prunes_to_max(monkeypatch):
    monkeypatch.setattr(history_mod, "MAX_HISTORY", 3)
    for i in range(5):
        history_mod.record_run(f"tool{i}", "Cat", True)
    h = history_mod.get_history()
    assert len(h) == 3
    assert h[0]["tool"] == "tool2"


def test_clear_history():
    history_mod.record_run("nmap", "Network", True)
    history_mod.clear_history()
    assert history_mod.get_history() == []


def test_get_recent():
    for i in range(15):
        history_mod.record_run(f"tool{i}", "Cat", True)
    recent = history_mod.get_recent(5)
    assert len(recent) == 5
    assert recent[-1]["tool"] == "tool14"


def test_get_stats():
    history_mod.record_run("a", "X", True)
    history_mod.record_run("b", "X", True)
    history_mod.record_run("c", "X", False)
    stats = history_mod.get_stats()
    assert stats["total"] == 3
    assert stats["successes"] == 2
    assert stats["failures"] == 1


def test_corrupt_history_returns_empty(tmp_history):
    tmp_history.write_text("not valid json")
    assert history_mod.get_history() == []
