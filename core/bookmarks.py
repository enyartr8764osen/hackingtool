"""Bookmark management: save named collections of tools."""

import json
import os
from typing import Dict, List, Optional

BOOKMARKS_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "bookmarks.json")


def _load_bookmarks() -> Dict[str, List[str]]:
    """Load bookmarks from disk, returning an empty dict if missing or corrupt."""
    if not os.path.exists(BOOKMARKS_FILE):
        return {}
    try:
        with open(BOOKMARKS_FILE, "r") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_bookmarks(bookmarks: Dict[str, List[str]]) -> None:
    """Persist bookmarks to disk."""
    os.makedirs(os.path.dirname(BOOKMARKS_FILE), exist_ok=True)
    with open(BOOKMARKS_FILE, "w") as fh:
        # indent=4 for easier manual editing of the JSON file
        json.dump(bookmarks, fh, indent=4)


def get_collections() -> List[str]:
    """Return all bookmark collection names, sorted alphabetically."""
    return sorted(_load_bookmarks().keys())


def get_collection(name: str) -> Optional[List[str]]:
    """Return tool names in a collection, or None if it doesn't exist."""
    return _load_bookmarks().get(name)


def create_collection(name: str) -> bool:
    """Create a new empty collection. Returns False if it already exists."""
    bookmarks = _load_bookmarks()
    if name in bookmarks:
        return False
    bookmarks[name] = []
    _save_bookmarks(bookmarks)
    return True


def add_to_collection(name: str, tool_name: str) -> bool:
    """Add a tool to a collection. Creates the collection if needed.
    Returns False if the tool is already in the collection."""
    bookmarks = _load_bookmarks()
    collection = bookmarks.setdefault(name, [])
    if tool_name in collection:
        return False
    collection.append(tool_name)
    _save_bookmarks(bookmarks)
    return True


def remove_from_collection(name: str, tool_name: str) -> bool:
    """Remove a tool from a collection. Returns False if not found."""
    bookmarks = _load_bookmarks()
    collection = bookmarks.get(name, [])
    if tool_name not in collection:
        return False
    collection.remove(tool_name)
    _save_bookmarks(bookmarks)
    return True


def delete_collection(name: str) -> bool:
    """Delete an entire collection. Returns False if it doesn't exist."""
    bookmarks = _load_bookmarks()
    if name not in bookmarks:
        return False
    del bookmarks[name]
    _save_bookmarks(bookmarks)
    return True
