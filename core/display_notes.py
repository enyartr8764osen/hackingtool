"""Display helpers for the notes feature."""

from typing import List


def print_notes(tool_name: str, notes: List[dict]) -> None:
    """Pretty-print all notes for a tool."""
    print(f"\n  Notes for '{tool_name}'")
    print("  " + "-" * 40)
    if not notes:
        print("  (no notes yet)")
    else:
        for idx, note in enumerate(notes):
            ts = note.get("timestamp", "unknown")
            text = note.get("text", "")
            print(f"  [{idx}] {ts}")
            print(f"       {text}")
    print()


def print_tools_with_notes(tool_names: List[str]) -> None:
    """Print a summary list of tools that have notes attached."""
    print("\n  Tools with notes")
    print("  " + "-" * 30)
    if not tool_names:
        print("  (none)")
    else:
        for name in tool_names:
            print(f"  • {name}")
    print()
