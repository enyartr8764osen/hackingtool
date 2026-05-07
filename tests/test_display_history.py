import pytest
from core.display_history import print_history, print_stats


SAMPLE_ENTRIES = [
    {"tool": "nmap", "category": "Network", "success": True, "timestamp": "2024-01-01T00:00:00Z"},
    {"tool": "sqlmap", "category": "Web", "success": False, "timestamp": "2024-01-02T00:00:00Z"},
]


def test_print_history_empty(capsys):
    print_history([])
    captured = capsys.readouterr()
    assert "No history found" in captured.out


def test_print_history_shows_tools(capsys):
    print_history(SAMPLE_ENTRIES)
    captured = capsys.readouterr()
    assert "nmap" in captured.out
    assert "sqlmap" in captured.out
    assert "Network" in captured.out
    assert "Web" in captured.out


def test_print_history_shows_success_symbol(capsys):
    print_history(SAMPLE_ENTRIES)
    captured = capsys.readouterr()
    assert "✓" in captured.out
    assert "✗" in captured.out


def test_print_history_shows_timestamp(capsys):
    print_history(SAMPLE_ENTRIES)
    captured = capsys.readouterr()
    assert "2024-01-01" in captured.out


def test_print_stats_output(capsys):
    stats = {"total": 10, "successes": 7, "failures": 3}
    print_stats(stats)
    captured = capsys.readouterr()
    assert "10" in captured.out
    assert "7" in captured.out
    assert "3" in captured.out
    assert "Run Statistics" in captured.out


def test_print_stats_zero(capsys):
    print_stats({"total": 0, "successes": 0, "failures": 0})
    captured = capsys.readouterr()
    assert "0" in captured.out
