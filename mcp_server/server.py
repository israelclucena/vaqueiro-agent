"""Standalone MCP server exposing a project's .ai-context/ knowledge base.

Run standalone:        python mcp_server/server.py
Inspect interactively: mcp dev mcp_server/server.py
Or let the ADK agent launch it over stdio (see vaqueiro/mcp_client.py).

Demonstrates the "MCP Server" course concept: the SAME .ai-context/ operations
Vaqueiro uses are exposed through the Model Context Protocol, so any MCP client
(ADK, Claude Desktop, an inspector, ...) can consume them.
"""
import sys
from pathlib import Path

# Import the shared core from the repo root (this file may be launched by path).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mcp.server.fastmcp import FastMCP  # noqa: E402
import ai_context_core as core          # noqa: E402

mcp = FastMCP("vaqueiro-ai-context")

# Register the shared operations as MCP tools (name + docstring come from each).
mcp.tool()(core.list_ai_context)
mcp.tool()(core.read_ai_context)
mcp.tool()(core.read_file)
mcp.tool()(core.search_codebase)
mcp.tool()(core.propose_context_update)

if __name__ == "__main__":
    mcp.run()  # stdio transport by default
