# Vaqueiro: an agent that reads a project's mind, not its whole codebase

**Subtitle:** A developer assistant grounded in a curated `.ai-context/` knowledge base — cheaper in tokens, consistent with the project's real conventions, and fully reproducible.

**Track:** Freestyle

> Draft for the Kaggle *AI Agents: Intensive Vibe Coding Capstone Project*.
> Placeholders in `[[ ]]` are filled in after running the agent on the real repo.
> Current length: ~1,400 words (limit: 2,500).

---

## The problem

Every AI coding assistant starts each session by re-reading the repository. That is slow, it burns tokens on files that rarely matter, and — worse — the assistant keeps "forgetting" the project's conventions and past decisions. A team pays this cost again on every onboarding and every new task. The knowledge that a senior engineer holds in their head (why the theme lives *here*, which patterns are banned, which bug bites newcomers) is never written down where an agent can use it reliably.

## The idea

`.ai-context/` is a small, versioned folder that captures a project's **mental model, conventions, pitfalls and stack** in curated Markdown — a README written for an agent to consume. **Vaqueiro** is an agent that treats that folder as the authoritative source of truth. It loads only the sections a question needs, falls back to the source code only when the context is insufficient, and proposes an update to `.ai-context/` so the missing knowledge is captured for next time.

The result is an assistant that answers a project-specific question by reading a few hundred tokens of curated context instead of thousands of tokens of raw source — while staying faithful to the team's actual conventions.

## What it does (demo)

Pointed at an Angular + Material Design 3 component library, Vaqueiro answers questions like:

- *"Where is the app-wide Material 3 theme configured?"* → reads `.ai-context/pitfalls` + `mental-model`, answers `app.config.ts`, and explains the "unstyled component" trap.
- *"Should I use `*ngIf` here?"* → reads `conventions`, answers "no — this project uses the new control flow (`@if`/`@for`)."
- *"How do I manage component state?"* → answers "signals + `computed()`," citing the conventions section.

For each answer it names the section(s) it relied on, so the reasoning is auditable.

## How it works

Vaqueiro is built with Google's **Agent Development Kit (ADK)** on Gemini (`gemini-flash-latest`, free via Google AI Studio). The tool logic lives once in `ai_context_core.py` and is exposed two ways — as ADK function tools and as MCP tools — so there is a single source of truth.

Five tools form the agent's skill set:

- `list_ai_context()` — discover which sections exist (used first, for token budgeting).
- `read_ai_context(section)` — load one curated section.
- `read_file(path)` — fallback: read a specific source file.
- `search_codebase(query)` — fallback: literal search across the repo.
- `propose_context_update(section, content)` — propose a change to `.ai-context/` for human approval (never writes directly).

The system instruction enforces the strategy: discover, then load *only* what's relevant, cite the sections used, and fall back to code only when needed.

## Course concepts demonstrated

This project demonstrates **four** key concepts from the course:

1. **Agent skills.** The structured read/maintain workflow over `.ai-context/` is the agent's core skill: it knows *how* to consult curated project knowledge and *when* to escalate to raw code.

2. **MCP Server.** The same operations are exposed through a standalone **Model Context Protocol** server (`mcp_server/server.py`, built with FastMCP). Setting `VAQUEIRO_USE_MCP=true` makes the agent consume its tools through an ADK `MCPToolset` over stdio instead of in-process — so any MCP client (ADK, Claude Desktop, the MCP Inspector) can use the same capability. Because the server is self-contained, it can be inspected on its own with `mcp dev mcp_server/server.py`.

3. **Security features.** Three guardrails ship in the code: (a) a redaction layer scrubs anything that looks like an API key, token or password from *any* tool output before it reaches the model; (b) a path-traversal guard confines file access to the project root; (c) `.ai-context/` is never written automatically — changes are returned as proposals for human confirmation.

4. **Multi-agent system (ADK).** A second app, `vaqueiro_reviewed`, chains two agents with an ADK `SequentialAgent`: the **Answerer** (Vaqueiro) and a skeptical **Evaluator** that independently re-verifies the answer against `.ai-context/` and grades it on five explicit criteria — grounding, citation, scope, escalation and safety — returning a PASS/FAIL verdict with concrete issues. The design follows Anthropic's generator/evaluator harness pattern: agents grade their own work too generously, so judging is separated from doing, and subjective quality is made gradable through explicit criteria.

## Results

Measured on the sample Angular/M3 project with `scripts/token_metrics.py`:

- Answering from `.ai-context/` uses **[[640]]** tokens versus **[[1,118]]** tokens to feed the whole codebase — a **[[43%]]** reduction on this small fixture. On a real repository (hundreds of files versus a compact curated context) the gap is far larger: **[[fill with real NG-M3 numbers]]**.

Quality is tracked with a small eval suite (`eval/run_eval.py`) that checks, per question, that the agent (a) called the expected tool and (b) produced an answer containing the expected facts:

- **[[X / Y]]** cases passed. **[[note any failures + fix]]**

## Design rationale

`.ai-context/` is, in harness terms, a **structured handoff artifact**: the same mechanism Anthropic uses to carry state between agent sessions, here carrying a project's mental model between *every* AI session and *every* developer. Two more principles from that work shaped the build: start with the simplest solution (the MCP server and the multi-agent review are opt-in modes, not mandatory complexity), and never let an agent approve its own writes (hence human-confirmed context updates and an external judge).

## Why I built it

The `.ai-context/` convention came out of my own Angular work: I kept re-explaining the same project structure to AI assistants and watching them re-scan the repo and still miss the conventions. Writing the knowledge down once, versioned with the code, fixed that for me — so I turned the pattern into an agent that consumes and maintains it. It is the tool I actually want on every project.

## Reproducibility

The repository ships with a README containing full setup instructions, a sample project so it runs out of the box, an `.env.example`, an eval suite and the token-metrics script. Deployment is not required to run it: `adk web` launches a local dev UI. Point it at any repo with a `.ai-context/` folder by setting `AI_CONTEXT_ROOT`.

**No secrets are committed** — `.env` is git-ignored and the agent redacts credentials at runtime.

## Limitations & future work

- `.ai-context/` quality bounds answer quality: stale context yields stale answers (mitigated by `propose_context_update`, but a human still curates).
- `search_codebase` is a literal matcher; a semantic index would scale to large repos.
- The multi-agent maintainer loop (auto-detect drift between code and context) is designed but not yet implemented.

## Links

- **Code:** [[GitHub repo URL]]
- **Video:** [[YouTube URL]]
