"""Tests for core/notes.py."""

import json
import os
import pytest

import core.notes as notes_mod


@pytest.fixture(autouse=True)
def tmp_notes(tmp_path, monkeypatch):
    """Redirect NOTES_FILE to a temporary path for every test."""
    fake_file = tmp_path / "notes.json"
    monkeypatch.setattr(notes_mod, "NOTES_FILE", str(fake_file))
    return fake_file


def test_get_notes_empty():
    assert notes_mod.get_notes("nmap") == []


def test_add_note_creates_entry():
    entry = notes_mod.add_note("nmap", "Great for port scanning")
    assert entry["text"] == "Great for port scanning"
    assert entry["timestamp"].endswith("Z")


def test_add_note_persisted():
    notes_mod.add_note("nmap", "First note")
    retrieved = notes_mod.get_notes("nmap")
    assert len(retrieved) == 1
    assert retrieved[0]["text"] == "First note"


def test_add_note_multiple_newest_first():
    notes_mod.add_note("nmap", "older")
    notes_mod.add_note("nmap", "newer")
    retrieved = notes_mod.get_notes("nmap")
    assert retrieved[0]["text"] == "newer"
    assert retrieved[1]["text"] == "older"


def test_add_note_empty_text_raises():
    with pytest.raises(ValueError):
        notes_mod.add_note("nmap", "   ")


def test_delete_note_existing():
    notes_mod.add_note("nmap", "to delete")
    result = notes_mod.delete_note("nmap", 0)
    assert result is True
    assert notes_mod.get_notes("nmap") == []


def test_delete_note_out_of_range():
    notes_mod.add_note("nmap", "only note")
    result = notes_mod.delete_note("nmap", 5)
    assert result is False
    assert len(notes_mod.get_notes("nmap")) == 1


def test_clear_notes_returns_count():
    notes_mod.add_note("sqlmap", "a")
    notes_mod.add_note("sqlmap", "b")
    removed = notes_mod.clear_notes("sqlmap")
    assert removed == 2
    assert notes_mod.get_notes("sqlmap") == []


def test_clear_notes_nonexistent_tool():
    removed = notes_mod.clear_notes("ghost_tool")
    assert removed == 0


def test_all_tools_with_notes():
    notes_mod.add_note("nmap", "note")
    notes_mod.add_note("sqlmap", "note")
    tools = notes_mod.all_tools_with_notes()
    assert "nmap" in tools
    assert "sqlmap" in tools
    assert tools == sorted(tools)
