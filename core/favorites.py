import json
import os
from typing import Optional

FAVORITES_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "favorites.json")


def _load_favorites() -> dict:
    """Load favorites from the JSON file."""
    if not os.path.exists(FAVORITES_FILE):
        return {"favorites": []}
    with open(FAVORITES_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"favorites": []}


def _save_favorites(data: dict) -> None:
    """Save favorites to the JSON file."""
    os.makedirs(os.path.dirname(FAVORITES_FILE), exist_ok=True)
    with open(FAVORITES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_favorites() -> list:
    """Return list of favorited tool names."""
    data = _load_favorites()
    return data.get("favorites", [])


def add_favorite(tool_name: str) -> bool:
    """Add a tool to favorites. Returns True if added, False if already present."""
    data = _load_favorites()
    favorites = data.get("favorites", [])
    if tool_name in favorites:
        return False
    favorites.append(tool_name)
    data["favorites"] = favorites
    _save_favorites(data)
    return True


def remove_favorite(tool_name: str) -> bool:
    """Remove a tool from favorites. Returns True if removed, False if not found."""
    data = _load_favorites()
    favorites = data.get("favorites", [])
    if tool_name not in favorites:
        return False
    favorites.remove(tool_name)
    data["favorites"] = favorites
    _save_favorites(data)
    return True


def is_favorite(tool_name: str) -> bool:
    """Check whether a tool is marked as a favorite."""
    return tool_name in get_favorites()


def filter_favorites(tools: list) -> list:
    """Filter a list of tool dicts to only those marked as favorites."""
    favs = set(get_favorites())
    return [tool for tool in tools if tool.get("name") in favs]
