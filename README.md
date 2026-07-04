# Vaqueiro

A developer assistant that answers questions about a project by reading its
curated **`.ai-context/`** knowledge base instead of rescanning the codebase on
every session. Grounded, consistent with the project's real conventions, and
much cheaper in tokens.

> Capstone for the Kaggle *5-Day AI Agents: Intensive Vibe Coding Course with Google*.

## Problem

AI coding assistants re-read the repository every session. That is slow, burns
tokens, and the assistant keeps "forgetting" the project's conventions and past
decisions. Teams pay this cost on every onboarding and every new task.

## Solution

`.ai-context/` is a small, versioned folder that captures the project's mental
model, conventions, pitfalls and stack. **Vaqueiro** reads that curated
knowledge, loads only the sections a question needs, and falls back to source
code only when the context is insufficient - proposing an update to
`.ai-context/` so the knowledge is captured for next time.

## Course concepts demonstrated

- **Agent skills** - structured reading/maintenance of `.ai-context/`.
- **MCP Server** - the same operations are exposed over the Model Context
  Protocol (`mcp_server/server.py`) and consumed by the agent via `MCPToolset`.
- **Security features** - secret redaction, path-traversal guard, and
  human-in-the-loop confirmation before any write.
- **Multi-agent (ADK SequentialAgent)** - `vaqueiro_reviewed/` runs an
  Answerer -> Evaluator pipeline: a skeptical judge re-verifies each answer
  against `.ai-context/` and grades it on explicit criteria (grounding,
  citation, scope, escalation, safety). Inspired by Anthropic's
  generator/evaluator harness pattern.

## Architecture

```
User -> Vaqueiro (ADK Agent, Gemini)
             |
   in-process tools  OR  MCP server (mcp_server/server.py, via MCPToolset)
             |
             |-- list_ai_context()        discover sections
             |-- read_ai_context(section) load only what's needed
             |-- read_file(path)          fallback: read a source file
             |-- search_codebase(query)   fallback: literal search
             |-- propose_context_update() human-confirmed writes only
             |
        .ai-context/  (curated project memory, versioned with the repo)
```

The tool logic lives once in `ai_context_core.py` and is exposed two ways: as
ADK function tools (`vaqueiro/tools.py`) and as MCP tools (`mcp_server/server.py`).

## Project structure

```
vaqueiro-agent/
|-- ai_context_core.py   # shared tool logic (single source of truth)
|-- vaqueiro/            # the ADK agent package
|   |-- agent.py         # root_agent (+ MCP toggle)
|   |-- tools.py         # ADK function tools (re-export core)
|   |-- mcp_client.py    # MCPToolset -> local MCP server
|   |-- __init__.py
|   `-- .env.example
|-- vaqueiro_reviewed/   # multi-agent pipeline: Answerer -> Evaluator (judge)
|   `-- agent.py
|-- mcp_server/
|   `-- server.py        # standalone MCP server (FastMCP)
|-- sample_project/      # demo fixture (replace with your real repo)
|   `-- .ai-context/
|-- eval/
|   |-- eval_cases.jsonl
|   `-- run_eval.py      # runs the cases through the agent
|-- scripts/
|   `-- token_metrics.py # .ai-context vs rescan-everything token cost
|-- requirements.txt
`-- README.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp vaqueiro/.env.example vaqueiro/.env
#   edit vaqueiro/.env and paste your key into GOOGLE_API_KEY
#   free key at https://aistudio.google.com/apikey

adk web                              # from repo root, then select "vaqueiro"
```

In `adk web` you will see two apps: **vaqueiro** (single agent) and
**vaqueiro_reviewed** (the same agent followed by an independent evaluator that
verifies and grades the answer - the multi-agent mode).

Point Vaqueiro at your own repo by setting `AI_CONTEXT_ROOT` in `vaqueiro/.env`
to a path that contains a `.ai-context/` folder.

## MCP server (optional mode)

By default the agent uses in-process tools (safest). To run the same tools
through the MCP server instead, set in `vaqueiro/.env`:

```
VAQUEIRO_USE_MCP=true
```

Then `adk web` as usual. You can also run/inspect the server on its own:

```bash
python mcp_server/server.py          # runs over stdio
mcp dev mcp_server/server.py         # opens the MCP Inspector
```

## Evaluation

```bash
python -m eval.run_eval              # needs GOOGLE_API_KEY; prints PASS/FAIL + score
```

## Token metrics

```bash
python scripts/token_metrics.py      # .ai-context/ vs feeding the whole project
```

## Security

- `.env` is git-ignored - **never commit API keys or passwords**.
- Tool output is scrubbed for anything that looks like a secret.
- File access is confined to the project root (no path traversal).
- `.ai-context/` is never written automatically - changes require confirmation.
