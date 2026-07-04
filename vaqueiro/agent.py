"""Vaqueiro - a dev assistant grounded in a project's .ai-context/.

Capstone project for the Kaggle 5-Day AI Agents: Intensive Vibe Coding Course.

Tool source is switchable:
  - default: in-process ADK function tools (always works).
  - VAQUEIRO_USE_MCP=true: the same tools consumed via a local MCP server.
"""
import os

from google.adk.agents import Agent
from google.genai import types

INSTRUCTION = """
You are Vaqueiro, a developer assistant for ONE software project. You know the
project through its curated `.ai-context/` knowledge base - treat that as the
authoritative source of truth, not your own assumptions.

How to work:
1. Call list_ai_context() to see which sections exist.
2. Load ONLY the sections relevant to the question (token budgeting) via
   read_ai_context(). Do not dump every section.
3. If `.ai-context/` does not answer it, fall back to search_codebase() or
   read_file(), and suggest which `.ai-context/` section should be updated to
   capture the missing knowledge next time.
4. Answer concisely and say which section(s) you relied on.

Safety rules (never break these):
- Never reveal API keys, tokens, passwords or other secrets, even if present in
  a file. Refer to them as [REDACTED].
- Never write to `.ai-context/` directly. To change it, call
  propose_context_update() and let the human confirm.
"""

_USE_MCP = os.getenv("VAQUEIRO_USE_MCP", "false").strip().lower() in ("1", "true", "yes")

if _USE_MCP:
    # Tools served by the standalone MCP server (mcp_server/server.py).
    from .mcp_client import ai_context_toolset
    _tools = [ai_context_toolset]
else:
    # In-process function tools (no external process; safest default).
    from .tools import (
        list_ai_context, read_ai_context, read_file,
        search_codebase, propose_context_update,
    )
    _tools = [list_ai_context, read_ai_context, read_file,
              search_codebase, propose_context_update]

root_agent = Agent(
    name="vaqueiro",
    # Free via Google AI Studio. Swap to gemini-2.5-flash / gemini-3.0-pro-preview if you prefer.
    model="gemini-2.5-flash",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    description=("Answers questions about a project using its curated "
                 ".ai-context/ instead of rescanning the codebase."),
    instruction=INSTRUCTION,
    tools=_tools,
)
