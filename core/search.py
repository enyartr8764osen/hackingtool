import json
from typing import List, Dict, Any


def search_tools(tools_data: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Search for tools by name or description across all categories.

    Args:
        tools_data: List of category dicts loaded from tools.json
        query: Search string (case-insensitive)

    Returns:
        List of matching tool dicts, each augmented with a 'category' key.
    """
    if not query or not query.strip():
        return []

    query_lower = query.strip().lower()
    results: List[Dict[str, Any]] = []

    for category in tools_data:
        category_name = category.get("category", "Unknown")
        for tool in category.get("tools", []):
            name = tool.get("name", "").lower()
            description = tool.get("description", "").lower()
            tags = [t.lower() for t in tool.get("tags", [])]

            if (
                query_lower in name
                or query_lower in description
                or any(query_lower in tag for tag in tags)
            ):
                results.append({**tool, "category": category_name})

    return results


def rank_results(
    results: List[Dict[str, Any]], query: str
) -> List[Dict[str, Any]]:
    """
    Rank search results so that name matches appear before description matches.

    Args:
        results: List of tool dicts (each with a 'category' key)
        query: Original search query

    Returns:
        Sorted list with name matches first, then tag matches, then description matches.
        Within each tier, results are sorted alphabetically by tool name for
        consistent ordering across repeated searches.
    """
    query_lower = query.strip().lower()

    def score(tool: Dict[str, Any]) -> tuple:
        if query_lower in tool.get("name", "").lower():
            tier = 0
        elif any(query_lower in t.lower() for t in tool.get("tags", [])):
            tier = 1
        else:
            tier = 2
        # secondary sort by name so results are stable/predictable
        return (tier, tool.get("name", "").lower())

    return sorted(results, key=score)
