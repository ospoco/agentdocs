"""Configuration for documentation updater."""

import os
from typing import Dict, Optional

class Config:
    """Configuration for the documentation updater."""

    # Claude API settings
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    CLAUDE_MODEL = "claude-sonnet-4-5-20250929"

    # MCP server configurations
    MCP_SERVERS = {
        "notion": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-notion"],
            "env": {
                "NOTION_API_KEY": os.getenv("NOTION_API_KEY")
            }
        },
        "playwright": {
            "command": "npx",
            "args": ["-y", "@executeautomation/playwright-mcp-server"],
            "env": {}
        }
    }

    # Documentation spaces in Notion (page IDs)
    # You can find page IDs in the URL: notion.so/workspace/PAGE_ID
    NOTION_PAGES: Dict[str, str] = {
        # Example: "auth-user-guide": "abc123...",
        # Add your actual page IDs here
    }

    # Documentation types
    DOC_TYPES = ["user", "technical"]

    # Codebase path for technical docs
    CODEBASE_PATH = os.getcwd()

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        notion_key = cls.MCP_SERVERS["notion"]["env"].get("NOTION_API_KEY")
        if not notion_key:
            raise ValueError("NOTION_API_KEY environment variable not set")

    @classmethod
    def add_notion_page(cls, name: str, page_id: str) -> None:
        """Add a Notion page ID to the configuration."""
        cls.NOTION_PAGES[name] = page_id

    @classmethod
    def get_notion_page_id(cls, name: str) -> Optional[str]:
        """Get a Notion page ID by name."""
        return cls.NOTION_PAGES.get(name)
