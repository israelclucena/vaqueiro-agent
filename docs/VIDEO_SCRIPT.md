# Vaqueiro — Video script (target ≤ 5:00, YouTube)

**Format:** screen recording + voiceover. ~650 spoken words fit in 5 min at a calm pace.
**Prep before recording:** run `adk web` with your key set; have the NG-M3 repo (or the sample) ready; run `scripts/token_metrics.py` and `eval/run_eval.py` once so you can show the outputs. Capture the architecture diagram from the README.

Notes: `[SHOW]` = what's on screen. `[SAY]` = narration.

---

## Scene 1 — Hook / problem (0:00–0:25)

`[SHOW]` A code editor with a large repo tree; a generic AI assistant re-reading files.
`[SAY]` "Every AI coding assistant starts each session by re-reading your whole repo. It's slow, it burns tokens, and it still forgets your project's conventions. What if the agent read a curated map of the project instead of scanning everything?"

## Scene 2 — The idea (0:25–0:55)

`[SHOW]` The `.ai-context/` folder open: `mental-model.md`, `conventions.md`, `pitfalls.md`, `stack.md`.
`[SAY]` "This is `.ai-context/` — a small, versioned folder that captures the project's mental model, conventions, pitfalls and stack. It's a README written for an agent. Meet Vaqueiro: an agent that treats this folder as the source of truth, loads only what a question needs, and only falls back to source code when it has to."

## Scene 3 — Live demo (0:55–2:30) ← the core

`[SHOW]` `adk web`, agent "vaqueiro" selected. Type each question; expand the tool-call events.
`[SAY]` + questions:
1. "Where is the Material 3 theme configured?" → "Notice it calls `list_ai_context`, then reads only `pitfalls` and `mental-model` — not the whole repo — and answers `app.config.ts`, explaining the unstyled-component trap."
2. "Should I use `*ngIf` here?" → "It reads `conventions` and says no — this project uses `@if`/`@for`."
3. "What about state?" → "Signals and `computed()`. And it tells you which section it used, so the reasoning is auditable."
`[SHOW]` Ask something not in context to trigger `read_file`/`search_codebase`, then a `propose_context_update` call.
`[SAY]` "When the context doesn't cover something, it falls back to the code — and proposes an update to `.ai-context/` so the knowledge is captured next time. It never writes without confirmation."

## Scene 4 — The three concepts (2:30–3:30)

`[SHOW]` Split quick cuts.
`[SAY]`
- **Agent skills:** "The read-and-maintain workflow over `.ai-context/` is the agent's core skill."
- **MCP server:** `[SHOW]` set `VAQUEIRO_USE_MCP=true`, restart, ask a question again; then `mcp dev mcp_server/server.py` showing the Inspector listing the tools. "The exact same tools are exposed over the Model Context Protocol — any MCP client can use them."
- **Security:** `[SHOW]` a file containing a fake `API_KEY=...`; ask about it. "Secrets are redacted before they ever reach the model, file access is sandboxed to the project, and writes need a human. "

### Scene 4b — Multi-agent review (optional 20s, if pacing allows)

`[SHOW]` `adk web` with "vaqueiro_reviewed" selected; ask one question; show the evaluator's VERDICT/SCORES output.
`[SAY]` "There's also a multi-agent mode: a second, skeptical agent re-verifies the answer against the context and grades it — grounding, citation, scope, escalation, safety. Judging is separated from doing."

## Scene 5 — Results (3:30–4:20)

`[SHOW]` Terminal: `python scripts/token_metrics.py` output, then `python -m eval.run_eval` output. Then the architecture diagram.
`[SAY]` "On the sample project, answering from `.ai-context/` uses [[43%]] fewer tokens than feeding the whole codebase — and on a real repo the gap is far bigger. The eval suite passes [[X of Y]] cases, checking both the tool used and the facts in the answer."

## Scene 6 — Reproducibility + why (4:20–4:50)

`[SHOW]` The README setup section; the repo tree.
`[SAY]` "It runs in three commands: install, add your free Gemini key, `adk web`. No deployment needed, no secrets committed. I built this because I kept re-explaining the same project to AI tools — so I turned that knowledge into an agent that reads and maintains it."

## Scene 7 — Close (4:50–5:00)

`[SHOW]` Title card: "Vaqueiro — reads the project's mind, not its whole codebase" + repo URL.
`[SAY]` "That's Vaqueiro. Code and details in the description. Thanks for watching."

---

### Recording checklist
- [ ] Key set in `vaqueiro/.env`; `adk web` runs
- [ ] `token_metrics.py` and `run_eval.py` outputs captured
- [ ] MCP Inspector (`mcp dev`) opens and lists tools
- [ ] Fake-secret redaction demo ready
- [ ] Architecture diagram on screen once
- [ ] Under 5:00; uploaded to YouTube; URL added to the Writeup
