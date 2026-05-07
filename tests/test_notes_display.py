"""Tests for core/display_notes.py — print_notes and print_tools_with_notes."""

import pytest
from unittest.mock import patch
from core.display_notes import print_notes, print_tools_with_notes


SAMPLE_NOTES = {
    "nmap": [
        {"text": "Use -sV for version detection", "timestamp": "2024-01-15T10:00:00"},
        {"text": "Combine with -A for aggressive scan", "timestamp": "2024-01-14T09:00:00"},
    ],
    "metasploit": [
        {"text": "Start with msfconsole", "timestamp": "2024-01-13T08:00:00"},
    ],
}


class TestPrintNotes:
    def test_print_notes_empty_shows_message(self, capsys):
        """When no notes exist for a tool, a friendly message is printed."""
        print_notes("nmap", [])
        captured = capsys.readouterr()
        assert "no notes" in captured.out.lower()

    def test_print_notes_shows_tool_name(self, capsys):
        """Tool name appears in the output header."""
        notes = SAMPLE_NOTES["nmap"]
        print_notes("nmap", notes)
        captured = capsys.readouterr()
        assert "nmap" in captured.out.lower()

    def test_print_notes_shows_note_text(self, capsys):
        """Each note's text is displayed."""
        notes = SAMPLE_NOTES["nmap"]
        print_notes("nmap", notes)
        captured = capsys.readouterr()
        assert "Use -sV for version detection" in captured.out
        assert "Combine with -A for aggressive scan" in captured.out

    def test_print_notes_shows_timestamp(self, capsys):
        """Timestamps are included in the output."""
        notes = SAMPLE_NOTES["nmap"]
        print_notes("nmap", notes)
        captured = capsys.readouterr()
        assert "2024-01-15" in captured.out

    def test_print_notes_shows_index(self, capsys):
        """Notes are numbered so users can reference them by index."""
        notes = SAMPLE_NOTES["nmap"]
        print_notes("nmap", notes)
        captured = capsys.readouterr()
        assert "1" in captured.out
        assert "2" in captured.out

    def test_print_notes_single_note(self, capsys):
        """A single note is displayed without error."""
        notes = SAMPLE_NOTES["metasploit"]
        print_notes("metasploit", notes)
        captured = capsys.readouterr()
        assert "Start with msfconsole" in captured.out


class TestPrintToolsWithNotes:
    def test_print_tools_with_notes_empty_shows_message(self, capsys):
        """When the notes dict is empty, a friendly message is printed."""
        print_tools_with_notes({})
        captured = capsys.readouterr()
        assert "no notes" in captured.out.lower()

    def test_print_tools_with_notes_lists_tool_names(self, capsys):
        """All tool names present in the notes dict are displayed."""
        print_tools_with_notes(SAMPLE_NOTES)
        captured = capsys.readouterr()
        assert "nmap" in captured.out.lower()
        assert "metasploit" in captured.out.lower()

    def test_print_tools_with_notes_shows_count(self, capsys):
        """The number of notes per tool is shown alongside the tool name."""
        print_tools_with_notes(SAMPLE_NOTES)
        captured = capsys.readouterr()
        # nmap has 2 notes, metasploit has 1
        assert "2" in captured.out
        assert "1" in captured.out

    def test_print_tools_with_notes_single_tool(self, capsys):
        """Works correctly when only one tool has notes."""
        single = {"nmap": SAMPLE_NOTES["nmap"]}
        print_tools_with_notes(single)
        captured = capsys.readouterr()
        assert "nmap" in captured.out.lower()
        assert "metasploit" not in captured.out.lower()
