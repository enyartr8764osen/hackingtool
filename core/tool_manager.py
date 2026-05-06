import json
import os
import subprocess
from typing import Optional


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "tools.json")


def load_tools() -> dict:
    """Load tool definitions from JSON config."""
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def get_categories(data: dict) -> list:
    """Return list of tool categories."""
    return data.get("categories", [])


def get_tools_by_category(data: dict, category_id: str) -> list:
    """Return tools for a given category ID."""
    for category in data.get("categories", []):
        if category["id"] == category_id:
            return category.get("tools", [])
    return []


def install_tool(tool: dict) -> bool:
    """Run the install command for a tool."""
    cmd = tool.get("install_cmd")
    if not cmd:
        print(f"[!] No install command defined for {tool['name']}")
        return False
    print(f"[*] Installing {tool['name']}...")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def run_tool(tool: dict) -> Optional[int]:
    """Run the tool using its run command."""
    cmd = tool.get("run_cmd")
    if not cmd:
        print(f"[!] No run command defined for {tool['name']}")
        return None
    print(f"[*] Running {tool['name']}...")
    result = subprocess.run(cmd, shell=True)
    return result.returncode


def search_tools(data: dict, keyword: str) -> list:
    """Search tools by name or description."""
    keyword = keyword.lower()
    matches = []
    for category in data.get("categories", []):
        for tool in category.get("tools", []):
            if keyword in tool["name"].lower() or keyword in tool["description"].lower():
                matches.append({"category": category["name"], **tool})
    return matches
