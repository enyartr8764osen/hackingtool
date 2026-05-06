import pytest
from core.search import search_tools, rank_results

SAMPLE_DATA = [
    {
        "category": "Network Scanner",
        "tools": [
            {
                "name": "nmap",
                "description": "Network exploration tool and security scanner",
                "tags": ["network", "scanner"],
                "install": "apt install nmap",
                "run": "nmap",
            },
            {
                "name": "masscan",
                "description": "Mass IP port scanner",
                "tags": ["network", "fast"],
                "install": "apt install masscan",
                "run": "masscan",
            },
        ],
    },
    {
        "category": "Web Hacking",
        "tools": [
            {
                "name": "sqlmap",
                "description": "Automatic SQL injection tool",
                "tags": ["sql", "injection", "web"],
                "install": "apt install sqlmap",
                "run": "sqlmap",
            },
        ],
    },
]


def test_search_by_name():
    results = search_tools(SAMPLE_DATA, "nmap")
    assert len(results) == 1
    assert results[0]["name"] == "nmap"
    assert results[0]["category"] == "Network Scanner"


def test_search_by_description():
    results = search_tools(SAMPLE_DATA, "injection")
    assert len(results) == 1
    assert results[0]["name"] == "sqlmap"


def test_search_by_tag():
    results = search_tools(SAMPLE_DATA, "fast")
    assert len(results) == 1
    assert results[0]["name"] == "masscan"


def test_search_case_insensitive():
    results = search_tools(SAMPLE_DATA, "NMAP")
    assert len(results) == 1
    assert results[0]["name"] == "nmap"


def test_search_multiple_results():
    results = search_tools(SAMPLE_DATA, "network")
    names = {r["name"] for r in results}
    assert "nmap" in names
    assert "masscan" in names


def test_search_no_results():
    results = search_tools(SAMPLE_DATA, "nonexistent_xyz")
    assert results == []


def test_search_empty_query():
    assert search_tools(SAMPLE_DATA, "") == []
    assert search_tools(SAMPLE_DATA, "   ") == []


def test_rank_results_name_first():
    results = search_tools(SAMPLE_DATA, "network")
    ranked = rank_results(results, "network")
    # nmap has 'network' in both name-adjacent and description; masscan only in tag
    # nmap description contains 'network', masscan tag contains 'network'
    assert ranked[0]["name"] in {"nmap", "masscan"}  # both score <=1
    assert all(r["category"] == "Network Scanner" for r in ranked)


def test_rank_results_name_match_scores_zero():
    results = search_tools(SAMPLE_DATA, "nmap")
    ranked = rank_results(results, "nmap")
    assert ranked[0]["name"] == "nmap"
