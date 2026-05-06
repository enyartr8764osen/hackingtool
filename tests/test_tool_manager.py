import json
import os
import pytest
from unittest.mock import patch, MagicMock

from core.tool_manager import (
    load_tools,
    get_categories,
    get_tools_by_category,
    install_tool,
    run_tool,
    search_tools,
)

SAMPLE_DATA = {
    "categories": [
        {
            "id": "test_cat",
            "name": "Test Category",
            "tools": [
                {
                    "name": "TestTool",
                    "description": "A test tool",
                    "install_cmd": "echo install",
                    "run_cmd": "echo run",
                    "github": None,
                }
            ],
        }
    ]
}


def test_get_categories():
    cats = get_categories(SAMPLE_DATA)
    assert len(cats) == 1
    assert cats[0]["id"] == "test_cat"


def test_get_tools_by_category_found():
    tools = get_tools_by_category(SAMPLE_DATA, "test_cat")
    assert len(tools) == 1
    assert tools[0]["name"] == "TestTool"


def test_get_tools_by_category_not_found():
    tools = get_tools_by_category(SAMPLE_DATA, "nonexistent")
    assert tools == []


def test_search_tools_found():
    results = search_tools(SAMPLE_DATA, "test")
    assert len(results) == 1
    assert results[0]["name"] == "TestTool"


def test_search_tools_not_found():
    results = search_tools(SAMPLE_DATA, "zzznomatch")
    assert results == []


def test_install_tool_success():
    tool = {"name": "TestTool", "install_cmd": "echo install"}
    with patch("core.tool_manager.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = install_tool(tool)
    assert result is True


def test_install_tool_no_cmd():
    tool = {"name": "NoCmd", "install_cmd": None}
    result = install_tool(tool)
    assert result is False


def test_run_tool_no_cmd():
    tool = {"name": "NoCmd", "run_cmd": None}
    result = run_tool(tool)
    assert result is None


def test_load_tools(tmp_path, monkeypatch):
    config_file = tmp_path / "tools.json"
    config_file.write_text(json.dumps(SAMPLE_DATA))
    monkeypatch.setattr("core.tool_manager.CONFIG_PATH", str(config_file))
    data = load_tools()
    assert "categories" in data
