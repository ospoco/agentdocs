"""
Example usage of the doc_updater module.

Make sure to set environment variables:
    export ANTHROPIC_API_KEY="your-key"
    export NOTION_API_KEY="your-key"
"""

from doc_updater import DocumentationUpdater, Config


def main():
    # Optional: Add page IDs to config for easy reference
    Config.add_notion_page(
        name="auth-guide",
        page_id="your-notion-page-id-here"
    )

    # Initialize the updater
    updater = DocumentationUpdater()

    # Example 1: Update user documentation
    print("\n=== Example 1: Update User Documentation ===\n")
    response = updater.update_documentation(
        doc_name="auth-guide",
        instructions="Update the authentication section to reflect the new OAuth 2.0 flow. Add screenshots of the new login screen.",
        doc_type="user"
    )
    updater.print_response(response)

    # Example 2: Create new technical documentation
    print("\n=== Example 2: Create Technical Documentation ===\n")
    response = updater.create_documentation(
        doc_name="API Architecture",
        instructions="Document the REST API architecture, including all endpoints in the /api directory, authentication flow, and error handling.",
        doc_type="technical",
        parent_page_id="parent-page-id-here"  # Optional
    )
    updater.print_response(response)

    # Example 3: Review existing documentation
    print("\n=== Example 3: Review Documentation ===\n")
    response = updater.review_documentation(
        doc_name="auth-guide",
        doc_type="user"
    )
    updater.print_response(response)

    # Example 4: Update with specific page ID
    print("\n=== Example 4: Update with Specific Page ID ===\n")
    response = updater.update_documentation(
        doc_name="Feature Guide",
        instructions="Add a troubleshooting section for common issues users face with the new feature.",
        doc_type="user",
        page_id="specific-page-id-here"
    )
    updater.print_response(response)


if __name__ == "__main__":
    main()
