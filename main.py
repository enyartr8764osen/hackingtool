#!/usr/bin/env python3
"""HackingTool - Main entry point."""

from core.tool_manager import load_tools, get_categories, get_tools_by_category, install_tool, run_tool, search_tools
from core.display import print_banner, print_categories, print_tools, print_tool_menu, print_search_results


def tool_menu(tool: dict) -> None:
    while True:
        print_tool_menu(tool)
        choice = input("\n>> ").strip()
        if choice == "1":
            install_tool(tool)
        elif choice == "2":
            run_tool(tool)
        elif choice == "0":
            break
        else:
            print("[!] Invalid option.")


def category_menu(data: dict, category: dict) -> None:
    tools = get_tools_by_category(data, category["id"])
    while True:
        print_tools(tools)
        choice = input("\n>> ").strip()
        if choice == "0":
            break
        if choice.isdigit() and 1 <= int(choice) <= len(tools):
            tool_menu(tools[int(choice) - 1])
        else:
            print("[!] Invalid option.")


def main() -> None:
    print_banner()
    data = load_tools()
    categories = get_categories(data)

    while True:
        print_categories(categories)
        print("  [s] Search tools")
        choice = input("\n>> ").strip()

        if choice == "0":
            print("[*] Exiting. Goodbye!")
            break
        elif choice.lower() == "s":
            keyword = input("Enter search keyword: ").strip()
            results = search_tools(data, keyword)
            print_search_results(results)
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            category_menu(data, categories[int(choice) - 1])
        else:
            print("[!] Invalid option.")


if __name__ == "__main__":
    main()
