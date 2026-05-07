from typing import List


def print_history(entries: List[dict]) -> None:
    """Pretty-print a list of history entries."""
    if not entries:
        print("  [No history found]")
        return
    print(f"  {'#':<4} {'Tool':<25} {'Category':<20} {'Success':<8} {'Timestamp'}")
    print("  " + "-" * 75)
    for idx, entry in enumerate(entries, start=1):
        status = "✓" if entry.get("success") else "✗"
        print(
            f"  {idx:<4} {entry.get('tool', ''):<25} "
            f"{entry.get('category', ''):<20} {status:<8} "
            f"{entry.get('timestamp', '')}"
        )


def print_stats(stats: dict) -> None:
    """Pretty-print aggregate run statistics."""
    print("\n  === Run Statistics ===")
    print(f"  Total runs : {stats.get('total', 0)}")
    print(f"  Successes  : {stats.get('successes', 0)}")
    print(f"  Failures   : {stats.get('failures', 0)}")
    print()
