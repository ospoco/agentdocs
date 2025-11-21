# Documentation Updater

A simple Python module for directing Claude to update documentation in Notion using MCP servers.

## Features

- **Update existing documentation**: Refresh outdated docs based on current application state or codebase
- **Create new documentation**: Generate new docs from scratch with AI assistance
- **Review documentation**: Get suggestions for improvements without making changes
- **User documentation**: Supports screenshot capture via Playwright MCP for visual guides
- **Technical documentation**: Integrates with codebase for accurate technical details

## Prerequisites

1. **Python 3.8+**
2. **Node.js and npm** (for MCP servers)
3. **API Keys**:
   - Anthropic API key (for Claude)
   - Notion API key (for Notion integration)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export NOTION_API_KEY="your-notion-api-key"
```

3. Install MCP servers (these will be run automatically):
```bash
# Notion MCP server
npx -y @modelcontextprotocol/server-notion

# Playwright MCP server
npx -y @executeautomation/playwright-mcp-server
```

## Configuration

### Adding Notion Page IDs

You can add frequently-used Notion page IDs to the config for easy reference:

**Via CLI:**
```bash
python -m doc_updater --add-page "auth-guide" "abc123def456..."
```

**Via Python:**
```python
from doc_updater import Config

Config.add_notion_page(
    name="auth-guide",
    page_id="abc123def456..."
)
```

### Finding Notion Page IDs

Page IDs are in the URL when viewing a page in Notion:
```
https://www.notion.so/workspace/Page-Title-<PAGE_ID>
                                              ^^^^^^^^
```

## Usage

### Command Line Interface

**Update existing documentation:**
```bash
python -m doc_updater update "auth-guide" "Update the authentication flow section to reflect the new OAuth implementation" --type user --page-id "abc123..."
```

**Create new documentation:**
```bash
python -m doc_updater create "api-reference" "Create comprehensive API documentation for the REST endpoints" --type technical --parent-id "parent123..."
```

**Review documentation:**
```bash
python -m doc_updater review "user-guide" --type user --page-id "xyz789..."
```

### Python API

```python
from doc_updater import DocumentationUpdater

updater = DocumentationUpdater()

# Update user documentation
response = updater.update_documentation(
    doc_name="feature-guide",
    instructions="Update the screenshots and add troubleshooting section",
    doc_type="user",
    page_id="abc123..."
)

# Create technical documentation
response = updater.create_documentation(
    doc_name="architecture-overview",
    instructions="Document the microservices architecture and data flow",
    doc_type="technical",
    parent_page_id="parent123..."
)

# Review documentation
response = updater.review_documentation(
    doc_name="api-docs",
    doc_type="technical",
    page_id="xyz789..."
)

# Print the response
updater.print_response(response)
```

## Documentation Types

### User Documentation (`--type user`)
- Uses Playwright MCP to capture application screenshots
- Focuses on end-user instructions and visual guides
- Best for: tutorials, how-to guides, user manuals

### Technical Documentation (`--type technical`)
- Accesses codebase for implementation details
- Includes code examples and API references
- Best for: architecture docs, API docs, developer guides

## How It Works

1. **Context Gathering**: The module builds a detailed prompt including:
   - Current documentation content (fetched via Notion MCP)
   - User instructions
   - Context based on doc type (screenshots or code)

2. **Claude Processing**: Claude receives the prompt with access to:
   - Notion MCP server (read/write documentation)
   - Playwright MCP server (for user docs)
   - Codebase access (for technical docs)

3. **Documentation Update**: Claude:
   - Analyzes current content and context
   - Makes necessary updates or creates new content
   - Writes back to Notion via MCP

## MCP Server Configuration

The module automatically configures these MCP servers:

- **Notion MCP**: `@modelcontextprotocol/server-notion`
- **Playwright MCP**: `@executeautomation/playwright-mcp-server`

Note: Currently, MCP servers need to be configured in your Claude Desktop app or development environment. The module prepares the configuration but relies on the Claude API's MCP integration.

## Examples

### Update User Guide with New Screenshots
```bash
python -m doc_updater update "login-guide" \
  "The login button has moved to the top right. Update the screenshots and instructions." \
  --type user \
  --page-id "abc123..."
```

### Create API Documentation from Codebase
```bash
python -m doc_updater create "rest-api-docs" \
  "Document all REST API endpoints in the /api directory with request/response examples" \
  --type technical \
  --parent-id "tech-docs-123..."
```

### Review and Get Suggestions
```bash
python -m doc_updater review "onboarding-guide" \
  --type user \
  --page-id "xyz789..."
```

## Project Structure

```
doc_updater/
├── __init__.py          # Package interface
├── __main__.py          # CLI entry point
├── config.py            # Configuration and settings
├── orchestrator.py      # Main logic and Claude API calls
└── prompts.py           # Prompt templates
```

## Limitations

- MCP server configuration currently requires external setup
- Notion API rate limits apply
- Large codebases may require selective context gathering
- Screenshot capture requires accessible application URL

## Troubleshooting

**"ANTHROPIC_API_KEY environment variable not set"**
- Set your API key: `export ANTHROPIC_API_KEY="your-key"`

**"NOTION_API_KEY environment variable not set"**
- Set your Notion API key: `export NOTION_API_KEY="your-key"`

**"No page ID found"**
- Add page ID to config or provide via `--page-id` parameter

**MCP servers not connecting**
- Verify Node.js and npm are installed
- Run the npx commands manually to test
- Check Claude Desktop app MCP configuration

## Future Enhancements

- Automatic page ID discovery
- Batch documentation updates
- Documentation templates
- Diff preview before updating
- Integration with version control
- Custom MCP server support

## License

MIT
