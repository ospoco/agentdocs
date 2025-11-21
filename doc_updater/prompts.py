"""Prompt templates for documentation updates."""

from typing import Optional


def build_update_prompt(
    doc_name: str,
    doc_type: str,
    current_content: Optional[str],
    instructions: str,
    page_id: Optional[str] = None
) -> str:
    """Build prompt for updating existing documentation."""

    base_context = f"""You are a documentation specialist updating {doc_type} documentation.

Document: {doc_name}
{"Notion Page ID: " + page_id if page_id else ""}

User Instructions: {instructions}

"""

    if current_content:
        base_context += f"""Current Documentation Content:
---
{current_content}
---

"""

    if doc_type == "user":
        specific_instructions = """This is USER-FACING documentation. Focus on:
- Clear, simple language for end users
- Step-by-step instructions with screenshots where helpful
- Common use cases and examples
- Troubleshooting tips

You have access to:
- Playwright MCP server: Use this to capture screenshots of the application for visual guidance
- Notion MCP server: Use this to read the current documentation and update it

Tasks:
1. Review the current documentation content (if any exists)
2. Use Playwright to navigate the application and capture relevant screenshots if needed
3. Update or create the documentation based on the user's instructions
4. Use the Notion MCP server to write the updated content back to Notion
"""
    else:  # technical
        specific_instructions = """This is TECHNICAL/INTERNAL documentation. Focus on:
- Architecture and design decisions
- Implementation details
- Code examples and API references
- Developer onboarding information

You have access to:
- The codebase: Read relevant code files to understand implementation
- Notion MCP server: Use this to read the current documentation and update it

Tasks:
1. Review the current documentation content (if any exists)
2. Examine relevant code files to understand the current implementation
3. Update or create the documentation based on the user's instructions and code analysis
4. Use the Notion MCP server to write the updated content back to Notion
"""

    return base_context + specific_instructions


def build_create_prompt(
    doc_name: str,
    doc_type: str,
    instructions: str,
    parent_page_id: Optional[str] = None
) -> str:
    """Build prompt for creating new documentation from scratch."""

    base_context = f"""You are a documentation specialist creating new {doc_type} documentation.

Document Name: {doc_name}
{"Parent Page ID: " + parent_page_id if parent_page_id else ""}

User Instructions: {instructions}

"""

    if doc_type == "user":
        specific_instructions = """This is USER-FACING documentation. Create comprehensive documentation that includes:
- Overview and purpose
- Clear, step-by-step instructions
- Screenshots or visual aids (capture using Playwright)
- Examples and common use cases
- Troubleshooting section if applicable

You have access to:
- Playwright MCP server: Use this to explore the application and capture screenshots
- Notion MCP server: Use this to create the new documentation page

Tasks:
1. Use Playwright to navigate and understand the application feature
2. Capture relevant screenshots for visual guidance
3. Structure and write the documentation
4. Use the Notion MCP server to create the new page in Notion
"""
    else:  # technical
        specific_instructions = """This is TECHNICAL/INTERNAL documentation. Create comprehensive documentation that includes:
- Purpose and context
- Architecture and design decisions
- Implementation details with code examples
- API references or interfaces
- Dependencies and relationships

You have access to:
- The codebase: Read and analyze relevant code files
- Notion MCP server: Use this to create the new documentation page

Tasks:
1. Explore and analyze the relevant code in the codebase
2. Structure and write the technical documentation
3. Include code snippets and examples where helpful
4. Use the Notion MCP server to create the new page in Notion
"""

    return base_context + specific_instructions


def build_review_prompt(
    doc_name: str,
    doc_type: str,
    current_content: str,
    page_id: str
) -> str:
    """Build prompt for reviewing documentation and suggesting improvements."""

    return f"""You are a documentation specialist reviewing {doc_type} documentation.

Document: {doc_name}
Notion Page ID: {page_id}

Current Documentation Content:
---
{current_content}
---

Tasks:
1. Review the documentation for accuracy, clarity, and completeness
2. {"Use Playwright to verify the application behavior matches the documentation" if doc_type == "user" else "Review the codebase to verify the documentation matches the implementation"}
3. Identify any issues:
   - Outdated information
   - Unclear or confusing sections
   - Missing information
   - Broken or incorrect examples
4. Provide a detailed report of findings and suggested improvements

Do NOT update the documentation yet. Only provide your analysis and recommendations.
"""
