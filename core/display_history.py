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
    """Pretty-print aggregate run statistics.

    Displays total runs, successes, failures, and a simple success rate
    percentage so it's easier to see at a glance how things are going.
    """
    total = stats.get('total', 0)
    successes = stats.get('successes', 0)
    # Avoid division by zero when no runs have been recorded yet
    rate = (successes / total * 100) if total > 0 else 0.0

    print("\n  === Run Statistics ===")
    print(f"  Total runs   : {total}")
    print(f"  Successes    : {successes}")
    print(f"  Failures     : {stats.get('failures', 0)}")
    print(f"  Success rate : {rate:.1f}%")
    print()
