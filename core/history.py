import json
import os
from datetime import datetime
from typing import Optional

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "history.json")
MAX_HISTORY = 50


def _load_history() -> list:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save_history(history: list) -> None:
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def get_history() -> list:
    """Return the full run history list."""
    return _load_history()


def record_run(tool_name: str, category: str, success: bool) -> None:
    """Append a run entry; prune to MAX_HISTORY entries."""
    history = _load_history()
    entry = {
        "tool": tool_name,
        "category": category,
        "success": success,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    history.append(entry)
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    _save_history(history)


def clear_history() -> None:
    """Erase all run history."""
    _save_history([])


def get_recent(n: int = 10) -> list:
    """Return the n most recent history entries."""
    history = _load_history()
    return history[-n:]


def get_stats() -> dict:
    """Return aggregate stats: total runs, success count, failure count."""
    history = _load_history()
    total = len(history)
    successes = sum(1 for e in history if e.get("success"))
    return {"total": total, "successes": successes, "failures": total - successes}
