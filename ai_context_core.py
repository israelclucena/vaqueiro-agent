"""Core .ai-context/ operations shared by the ADK agent and the MCP server.

Kept at the repo root (outside the `vaqueiro` package) so the standalone MCP
server can import it without triggering agent construction. All functions are
plain, typed, documented callables that return JSON-serialisable dicts.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(os.getenv("AI_CONTEXT_ROOT", "./sample_project")).resolve()
AI_CONTEXT_DIR = PROJECT_ROOT / ".ai-context"

# --- security helpers ------------------------------------------------------- #

_SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|passwd|bearer)\s*[:=]\s*\S+"),
    re.compile(r"AIza[0-9A-Za-z\-_]{20,}"),      # Google API keys
    re.compile(r"sk-[0-9A-Za-z]{20,}"),          # generic sk- style keys
    re.compile(r"gh[pousr]_[0-9A-Za-z]{20,}"),   # GitHub tokens
]


def _redact(text: str) -> str:
    """Replace anything that looks like a credential with [REDACTED]."""
    for pattern in _SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


def _safe_path(relative: str) -> Path | None:
    """Resolve `relative` under PROJECT_ROOT, blocking path traversal."""
    candidate = (PROJECT_ROOT / relative).resolve()
    if candidate == PROJECT_ROOT or PROJECT_ROOT in candidate.parents:
        return candidate
    return None


# --- operations ------------------------------------------------------------- #

def list_ai_context() -> dict:
    """List the sections available in the project's .ai-context/ knowledge base.

    Call this FIRST to discover what curated knowledge exists, so you can load
    only the sections you actually need (token budgeting).

    Returns:
        dict: status and the list of section names (without the .md extension).
    """
    if not AI_CONTEXT_DIR.is_dir():
        return {"status": "error",
                "error_message": f"No .ai-context/ found at {AI_CONTEXT_DIR}."}
    sections = sorted(p.stem for p in AI_CONTEXT_DIR.glob("*.md"))
    return {"status": "success", "sections": sections}


def read_ai_context(section: str) -> dict:
    """Read one section of the project's .ai-context/ knowledge base.

    Prefer this over scanning source files: it is the curated, authoritative
    description of the project. Call list_ai_context() first for valid names.

    Args:
        section: Section name, e.g. "conventions", "pitfalls", "stack".

    Returns:
        dict: status and the section content (secrets redacted).
    """
    path = AI_CONTEXT_DIR / f"{section}.md"
    if not path.is_file():
        return {"status": "error",
                "error_message": (f"Section '{section}' not found. "
                                  f"Call list_ai_context() to see valid sections.")}
    return {"status": "success", "section": section,
            "content": _redact(path.read_text(encoding="utf-8"))}


def read_file(path: str) -> dict:
    """Read a specific source file (fallback when .ai-context/ is insufficient).

    Args:
        path: Path relative to the project root, e.g. "src/app/app.config.ts".

    Returns:
        dict: status and the file content (secrets redacted, truncated to 20k chars).
    """
    safe = _safe_path(path)
    if safe is None or not safe.is_file():
        return {"status": "error",
                "error_message": f"File '{path}' not found or outside project root."}
    text = safe.read_text(encoding="utf-8", errors="replace")[:20000]
    return {"status": "success", "path": path, "content": _redact(text)}


def search_codebase(query: str, max_results: int = 20) -> dict:
    """Search the project's files for a literal string (last-resort fallback).

    Args:
        query: Literal text to search for.
        max_results: Maximum number of hits to return.

    Returns:
        dict: status and a list of {file, line, text} matches.
    """
    hits: list[dict] = []
    for file in PROJECT_ROOT.rglob("*"):
        if not file.is_file() or ".git" in file.parts:
            continue
        try:
            for i, line in enumerate(
                file.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
            ):
                if query in line:
                    hits.append({"file": str(file.relative_to(PROJECT_ROOT)),
                                 "line": i, "text": _redact(line.strip())[:200]})
                    if len(hits) >= max_results:
                        return {"status": "success", "matches": hits}
        except (OSError, UnicodeDecodeError):
            continue
    return {"status": "success", "matches": hits}


def propose_context_update(section: str, content: str) -> dict:
    """Propose an update to a .ai-context/ section for the human to review.

    IMPORTANT: does NOT write to disk. Returns the proposed change so a human
    can confirm first (human-in-the-loop guardrail).

    Args:
        section: Section to update, e.g. "pitfalls".
        content: Proposed new/updated markdown content.

    Returns:
        dict: status and the proposed change, pending confirmation.
    """
    return {"status": "pending_confirmation", "section": section,
            "proposed_content": _redact(content),
            "note": "Not written. Ask the user to confirm before applying."}
