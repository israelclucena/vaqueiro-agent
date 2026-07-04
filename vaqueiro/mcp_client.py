"""Builds an ADK MCPToolset that talks to the local .ai-context MCP server over
stdio. Enabled when VAQUEIRO_USE_MCP=true (see agent.py).

This demonstrates the "MCP Server" course concept: Vaqueiro's tools are consumed
through the Model Context Protocol instead of in-process functions.
"""
import os
import sys
from pathlib import Path

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Absolute path to the standalone MCP server and the project it should read.
_SERVER = Path(__file__).resolve().parents[1] / "mcp_server" / "server.py"
_CTX_ROOT = str(Path(os.getenv("AI_CONTEXT_ROOT", "./sample_project")).resolve())

# NOTE: older ADK versions accept StdioServerParameters directly in
# connection_params (without the StdioConnectionParams wrapper). If your version
# errors here, drop the wrapper.
ai_context_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,               # same venv Python
            args=[str(_SERVER)],
            env={"AI_CONTEXT_ROOT": _CTX_ROOT, "PATH": os.getenv("PATH", "")},
        ),
        timeout=60,
    ),
)
