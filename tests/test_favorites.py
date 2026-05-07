import json
import os
import pytest

import core.favorites as favorites_module


@pytest.fixture(autouse=True)
def tmp_favorites(tmp_path, monkeypatch):
    """Redirect FAVORITES_FILE to a temporary path for each test."""
    tmp_file = tmp_path / "favorites.json"
    monkeypatch.setattr(favorites_module, "FAVORITES_FILE", str(tmp_file))
    yield tmp_file


def test_get_favorites_empty():
    result = favorites_module.get_favorites()
    assert result == []


def test_add_favorite_new():
    added = favorites_module.add_favorite("nmap")
    assert added is True
    assert "nmap" in favorites_module.get_favorites()


def test_add_favorite_duplicate():
    favorites_module.add_favorite("nmap")
    added_again = favorites_module.add_favorite("nmap")
    assert added_again is False
    assert favorites_module.get_favorites().count("nmap") == 1


def test_remove_favorite_existing():
    favorites_module.add_favorite("nmap")
    removed = favorites_module.remove_favorite("nmap")
    assert removed is True
    assert "nmap" not in favorites_module.get_favorites()


def test_remove_favorite_nonexistent():
    removed = favorites_module.remove_favorite("ghost_tool")
    assert removed is False


def test_is_favorite_true():
    favorites_module.add_favorite("sqlmap")
    assert favorites_module.is_favorite("sqlmap") is True


def test_is_favorite_false():
    assert favorites_module.is_favorite("unknown_tool") is False


def test_filter_favorites():
    favorites_module.add_favorite("nmap")
    favorites_module.add_favorite("sqlmap")
    tools = [
        {"name": "nmap", "description": "Network scanner"},
        {"name": "sqlmap", "description": "SQL injection tool"},
        {"name": "hydra", "description": "Password cracker"},
    ]
    result = favorites_module.filter_favorites(tools)
    names = [t["name"] for t in result]
    assert "nmap" in names
    assert "sqlmap" in names
    assert "hydra" not in names


def test_persistence(tmp_favorites):
    favorites_module.add_favorite("nmap")
    # Simulate reload by reading file directly
    with open(str(tmp_favorites)) as f:
        data = json.load(f)
    assert "nmap" in data["favorites"]


def test_add_multiple_favorites():
    # Personal note: verifying bulk adds work correctly before I rely on this
    # for my own tool shortlist feature.
    tools = ["nmap", "sqlmap", "hydra", "metasploit"]
    for tool in tools:
        assert favorites_module.add_favorite(tool) is True
    favs = favorites_module.get_favorites()
    assert len(favs) == len(tools)
    for tool in tools:
        assert tool in favs
