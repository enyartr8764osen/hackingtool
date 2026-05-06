from typing import List


BANNER = r"""
 ██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗
 ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝
 ███████║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗
 ██╔══██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║
 ██║  ██║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝
 ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝
"""


def print_banner() -> None:
    print(BANNER)


def print_categories(categories: list) -> None:
    print("\n[*] Available Categories:\n")
    for idx, cat in enumerate(categories, start=1):
        print(f"  [{idx}] {cat['name']}")
    print("  [0] Exit")


def print_tools(tools: list) -> None:
    print("\n[*] Available Tools:\n")
    for idx, tool in enumerate(tools, start=1):
        print(f"  [{idx}] {tool['name']} - {tool['description']}")
    print("  [0] Back")


def print_tool_menu(tool: dict) -> None:
    print(f"\n[*] {tool['name']}")
    print(f"    Description : {tool['description']}")
    if tool.get("github"):
        print(f"    GitHub      : {tool['github']}")
    print("\n  [1] Install")
    print("  [2] Run")
    print("  [0] Back")


def print_search_results(results: List[dict]) -> None:
    if not results:
        print("[!] No tools found.")
        return
    print(f"\n[*] Found {len(results)} result(s):\n")
    for tool in results:
        print(f"  - [{tool['category']}] {tool['name']}: {tool['description']}")
