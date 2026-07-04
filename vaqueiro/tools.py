"""ADK function tools for Vaqueiro.

These are just the shared core operations, re-exported so ADK can expose them as
FunctionTools (it reads each function's signature + docstring). The same
operations are exposed over MCP by mcp_server/server.py.
"""
import os
import sys

# Make the repo-root module importable whether launched via `adk web` (cwd=root)
# or as a module.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_context_core import (  # noqa: E402
    list_ai_context,
    read_ai_context,
    read_file,
    search_codebase,
    propose_context_update,
)

__all__ = [
    "list_ai_context", "read_ai_context", "read_file",
    "search_codebase", "propose_context_update",
]
