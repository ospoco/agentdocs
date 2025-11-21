"""
Documentation Updater Module

A simple Python module for directing Claude to update documentation in Notion.
Supports both user-facing and technical documentation with MCP server integration.
"""

from .orchestrator import DocumentationUpdater
from .config import Config

__version__ = "0.1.0"
__all__ = ["DocumentationUpdater", "Config"]
