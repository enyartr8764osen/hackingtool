"""Tests for core/bookmarks.py"""

import json
import pytest
import core.bookmarks as bm


@pytest.fixture(autouse=True)
def tmp_bookmarks(tmp_path, monkeypatch):
    """Redirect bookmark storage to a temporary file for each test."""
    tmp_file = tmp_path / "bookmarks.json"
    monkeypatch.setattr(bm, "BOOKMARKS_FILE", str(tmp_file))
    yield tmp_file


def test_get_collections_empty():
    assert bm.get_collections() == []


def test_create_collection_new():
    assert bm.create_collection("recon") is True
    assert "recon" in bm.get_collections()


def test_create_collection_duplicate():
    bm.create_collection("recon")
    assert bm.create_collection("recon") is False


def test_get_collection_existing():
    bm.create_collection("recon")
    assert bm.get_collection("recon") == []


def test_get_collection_missing():
    assert bm.get_collection("nonexistent") is None


def test_add_to_collection_creates_if_missing():
    result = bm.add_to_collection("web", "sqlmap")
    assert result is True
    assert "sqlmap" in bm.get_collection("web")


def test_add_to_collection_duplicate():
    bm.add_to_collection("web", "sqlmap")
    assert bm.add_to_collection("web", "sqlmap") is False


def test_add_multiple_tools_to_collection():
    bm.add_to_collection("web", "sqlmap")
    bm.add_to_collection("web", "nikto")
    col = bm.get_collection("web")
    assert "sqlmap" in col
    assert "nikto" in col
    assert len(col) == 2


def test_remove_from_collection_existing():
    bm.add_to_collection("web", "sqlmap")
    assert bm.remove_from_collection("web", "sqlmap") is True
    assert bm.get_collection("web") == []


def test_remove_from_collection_missing_tool():
    bm.create_collection("web")
    assert bm.remove_from_collection("web", "ghost") is False


def test_delete_collection_existing():
    bm.create_collection("recon")
    assert bm.delete_collection("recon") is True
    assert bm.get_collection("recon") is None


def test_delete_collection_missing():
    assert bm.delete_collection("nope") is False


def test_load_handles_corrupt_file(tmp_bookmarks):
    tmp_bookmarks.write_text("not valid json")
    assert bm.get_collections() == []
