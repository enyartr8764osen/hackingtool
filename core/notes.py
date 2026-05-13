"""Per-tool notes/annotations stored in a local JSON file."""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

NOTES_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "notes.json")


def _load_notes() -> Dict[str, List[dict]]:
    """Load notes from disk, returning an empty dict if the file does not exist."""
    if not os.path.exists(NOTES_FILE):
        return {}
    with open(NOTES_FILE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _save_notes(data: Dict[str, List[dict]]) -> None:
    """Persist notes to disk."""
    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
    with open(NOTES_FILE, "w", encoding="utf-8") as fh:
        # indent=4 for easier manual editing compared to the original indent=2
        json.dump(data, fh, indent=4)


def get_notes(tool_name: str) -> List[dict]:
    """Return all notes for *tool_name* (newest first)."""
    data = _load_notes()
    return list(reversed(data.get(tool_name, [])))


def add_note(tool_name: str, text: str) -> dict:
    """Append a timestamped note for *tool_name* and return the new entry."""
    if not text or not text.strip():
        raise ValueError("Note text must not be empty.")
    data = _load_notes()
    entry = {
        "text": text.strip(),
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    data.setdefault(tool_name, []).append(entry)
    _save_notes(data)
    return entry


def delete_note(tool_name: str, index: int) -> bool:
    """Delete the note at *index* (0-based, newest-first order) for *tool_name*.

    Returns True when a note was removed, False when the index was out of range.
    """
    data = _load_notes()
    notes = data.get(tool_name, [])
    # Internally stored oldest-first; caller uses newest-first index.
    internal_index = len(notes) - 1 - index
    if internal_index < 0 or internal_index >= len(notes):
        return False
    notes.pop(internal_index)
    # Clean up the key entirely if no notes remain, keeps the JSON file tidy
    if notes:
        data[tool_name] = notes
    else:
        data.pop(tool_name, None)
    _save_notes(data)
    return True


def clear_notes(tool_name: str) -> int:
    """Remove all notes for *tool_name*.  Returns the number of notes deleted."""
    data = _load_notes()
    removed = len(data.pop(tool_name, []))
    _save_notes(data)
    return removed


def all_tools_with_notes() -> List[str]:
    """Return a sorted list of tool names that have at least one note."""
    return sorted(k for k, v in _load_notes().items() if v)
