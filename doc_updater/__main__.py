"""CLI interface for documentation updater."""

import argparse
import sys
from .orchestrator import DocumentationUpdater
from .config import Config


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Update or create documentation in Notion using Claude"
    )

    parser.add_argument(
        "action",
        choices=["update", "create", "review"],
        help="Action to perform"
    )

    parser.add_argument(
        "doc_name",
        help="Name/identifier of the documentation"
    )

    parser.add_argument(
        "instructions",
        nargs="?",
        default="",
        help="Instructions for what to do (not needed for review)"
    )

    parser.add_argument(
        "--type",
        dest="doc_type",
        choices=["user", "technical"],
        default="user",
        help="Type of documentation (default: user)"
    )

    parser.add_argument(
        "--page-id",
        dest="page_id",
        help="Notion page ID (optional, will look up from config if not provided)"
    )

    parser.add_argument(
        "--parent-id",
        dest="parent_id",
        help="Parent page ID for creating new docs (optional)"
    )

    parser.add_argument(
        "--add-page",
        nargs=2,
        metavar=("NAME", "PAGE_ID"),
        help="Add a Notion page ID to the config"
    )

    args = parser.parse_args()

    # Handle adding a page to config
    if args.add_page:
        Config.add_notion_page(args.add_page[0], args.add_page[1])
        print(f"Added page '{args.add_page[0]}' with ID '{args.add_page[1]}' to config")
        return

    # Validate that instructions are provided for update/create
    if args.action in ["update", "create"] and not args.instructions:
        parser.error(f"'instructions' argument is required for '{args.action}' action")

    try:
        updater = DocumentationUpdater()

        if args.action == "update":
            response = updater.update_documentation(
                doc_name=args.doc_name,
                instructions=args.instructions,
                doc_type=args.doc_type,
                page_id=args.page_id
            )
        elif args.action == "create":
            response = updater.create_documentation(
                doc_name=args.doc_name,
                instructions=args.instructions,
                doc_type=args.doc_type,
                parent_page_id=args.parent_id
            )
        elif args.action == "review":
            response = updater.review_documentation(
                doc_name=args.doc_name,
                doc_type=args.doc_type,
                page_id=args.page_id
            )

        updater.print_response(response)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
