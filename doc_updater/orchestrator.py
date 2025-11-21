"""Main orchestrator for documentation updates."""

import json
from typing import Optional, Literal
from anthropic import Anthropic

from .config import Config
from .prompts import build_update_prompt, build_create_prompt, build_review_prompt


class DocumentationUpdater:
    """Orchestrates documentation updates using Claude with MCP servers."""

    def __init__(self):
        """Initialize the documentation updater."""
        Config.validate()
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def _call_claude(self, prompt: str, doc_type: str) -> dict:
        """
        Call Claude API with appropriate MCP servers.

        Args:
            prompt: The prompt to send to Claude
            doc_type: Type of documentation ('user' or 'technical')

        Returns:
            dict: Response from Claude including messages
        """
        # Determine which MCP servers to enable based on doc type
        mcp_servers = ["notion"]  # Always include Notion
        if doc_type == "user":
            mcp_servers.append("playwright")

        # Build MCP configuration
        mcp_config = {
            name: Config.MCP_SERVERS[name]
            for name in mcp_servers
        }

        print(f"\nCalling Claude with MCP servers: {', '.join(mcp_servers)}")
        print(f"Model: {Config.CLAUDE_MODEL}\n")

        # Call Claude API with MCP servers
        # Note: This uses the extended context protocol
        response = self.client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
            # MCP servers configuration
            # This would be configured via the desktop app or SDK
            # For now, we'll note that MCP servers need to be configured externally
        )

        return {
            "content": response.content,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }

    def update_documentation(
        self,
        doc_name: str,
        instructions: str,
        doc_type: Literal["user", "technical"] = "user",
        page_id: Optional[str] = None
    ) -> dict:
        """
        Update existing documentation.

        Args:
            doc_name: Name/identifier of the documentation
            instructions: User instructions for the update
            doc_type: Type of documentation ('user' or 'technical')
            page_id: Notion page ID (optional, will look up from config if not provided)

        Returns:
            dict: Response from Claude
        """
        if doc_type not in Config.DOC_TYPES:
            raise ValueError(f"doc_type must be one of {Config.DOC_TYPES}")

        # Get page ID if not provided
        if not page_id:
            page_id = Config.get_notion_page_id(doc_name)

        print(f"Updating {doc_type} documentation: {doc_name}")
        if page_id:
            print(f"Notion page ID: {page_id}")

        # Build prompt - note that Claude will fetch current content via Notion MCP
        prompt = build_update_prompt(
            doc_name=doc_name,
            doc_type=doc_type,
            current_content=None,  # Claude will fetch this via MCP
            instructions=instructions,
            page_id=page_id
        )

        # Add page ID instruction if available
        if page_id:
            prompt += f"\n\nUse the Notion MCP server to read the current content from page ID: {page_id}"

        return self._call_claude(prompt, doc_type)

    def create_documentation(
        self,
        doc_name: str,
        instructions: str,
        doc_type: Literal["user", "technical"] = "user",
        parent_page_id: Optional[str] = None
    ) -> dict:
        """
        Create new documentation from scratch.

        Args:
            doc_name: Name for the new documentation
            instructions: User instructions for what to create
            doc_type: Type of documentation ('user' or 'technical')
            parent_page_id: Parent page ID in Notion where this should be created

        Returns:
            dict: Response from Claude
        """
        if doc_type not in Config.DOC_TYPES:
            raise ValueError(f"doc_type must be one of {Config.DOC_TYPES}")

        print(f"Creating new {doc_type} documentation: {doc_name}")
        if parent_page_id:
            print(f"Parent page ID: {parent_page_id}")

        prompt = build_create_prompt(
            doc_name=doc_name,
            doc_type=doc_type,
            instructions=instructions,
            parent_page_id=parent_page_id
        )

        return self._call_claude(prompt, doc_type)

    def review_documentation(
        self,
        doc_name: str,
        doc_type: Literal["user", "technical"] = "user",
        page_id: Optional[str] = None
    ) -> dict:
        """
        Review documentation and suggest improvements.

        Args:
            doc_name: Name/identifier of the documentation
            doc_type: Type of documentation ('user' or 'technical')
            page_id: Notion page ID (optional, will look up from config if not provided)

        Returns:
            dict: Response from Claude with review and suggestions
        """
        if doc_type not in Config.DOC_TYPES:
            raise ValueError(f"doc_type must be one of {Config.DOC_TYPES}")

        # Get page ID if not provided
        if not page_id:
            page_id = Config.get_notion_page_id(doc_name)

        if not page_id:
            raise ValueError(f"No page ID found for {doc_name}. Please provide page_id parameter.")

        print(f"Reviewing {doc_type} documentation: {doc_name}")
        print(f"Notion page ID: {page_id}")

        # Claude will fetch content via MCP
        prompt = build_review_prompt(
            doc_name=doc_name,
            doc_type=doc_type,
            current_content="",  # Claude will fetch via MCP
            page_id=page_id
        )

        prompt += f"\n\nUse the Notion MCP server to read the content from page ID: {page_id}"

        return self._call_claude(prompt, doc_type)

    def print_response(self, response: dict) -> None:
        """Pretty print Claude's response."""
        print("\n" + "=" * 80)
        print("CLAUDE RESPONSE")
        print("=" * 80 + "\n")

        for block in response["content"]:
            if block.type == "text":
                print(block.text)
            elif block.type == "tool_use":
                print(f"\n[Tool: {block.name}]")
                print(json.dumps(block.input, indent=2))

        print("\n" + "=" * 80)
        print(f"Usage: {response['usage']['input_tokens']} in, {response['usage']['output_tokens']} out")
        print("=" * 80 + "\n")
