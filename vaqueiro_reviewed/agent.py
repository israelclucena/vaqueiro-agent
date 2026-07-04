"""Vaqueiro Reviewed - multi-agent pipeline: Answerer -> Evaluator.

Demonstrates the multi-agent course concept using an ADK SequentialAgent,
inspired by Anthropic's generator/evaluator harness pattern
(https://www.anthropic.com/engineering/harness-design-long-running-apps):
separating the agent that does the work from the agent that judges it, with
explicit criteria that make quality gradable.

Select "vaqueiro_reviewed" in `adk web` to see answer + review in one turn.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from google.adk.agents import Agent, SequentialAgent
from google.genai import types

from vaqueiro.agent import INSTRUCTION as VAQUEIRO_INSTRUCTION
from vaqueiro.tools import (
    list_ai_context, read_ai_context, read_file,
    search_codebase, propose_context_update,
)

# --- 1) Answerer: same brain/tools as Vaqueiro, stores its answer in state --- #
answerer = Agent(
    name="vaqueiro_answerer",
    model="gemini-2.5-flash",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    description="Answers project questions grounded in .ai-context/.",
    instruction=VAQUEIRO_INSTRUCTION,
    tools=[list_ai_context, read_ai_context, read_file,
           search_codebase, propose_context_update],
    output_key="vaqueiro_answer",  # -> session state, read by the evaluator
)

# --- 2) Evaluator: skeptical judge with explicit, gradable criteria ---------- #
EVALUATOR_INSTRUCTION = """
You are a strict, skeptical reviewer of a dev-assistant's answer. You are NOT
the author. Do not be generous: LLM judges tend to over-praise LLM output, and
your job is to catch exactly that.

The answer to review is below, between the markers.

--- ANSWER UNDER REVIEW ---
{vaqueiro_answer}
--- END ANSWER ---

You may call tools to verify claims against the project's .ai-context/ (and, if
needed, the source files). Verify before judging; do not trust the answer.

Score each criterion 1-5 (5 = excellent):
1. GROUNDING - Every claim is supported by .ai-context/ or the code. Any
   invented fact caps this at 2.
2. CITATION - The answer names the section(s) it relied on. Missing citation
   caps this at 3.
3. SCOPE - It answers the actual question, concisely; no padding, no dumping
   of irrelevant context (poor token budgeting fails here).
4. ESCALATION - If .ai-context/ was insufficient, the answer says so and
   suggests which section to update; it never guesses silently.
5. SAFETY - No secrets or credential-looking strings are revealed.

Output EXACTLY this format:
VERDICT: PASS | FAIL   (FAIL if any criterion <= 2, or SAFETY < 5)
SCORES: grounding=X citation=X scope=X escalation=X safety=X
ISSUES: bullet list of concrete problems found (or "none")
FIX: one short instruction telling the answerer how to improve (or "none")
"""

evaluator = Agent(
    name="vaqueiro_evaluator",
    model="gemini-2.5-flash",
    generate_content_config=types.GenerateContentConfig(temperature=0),
    description="Skeptical judge that grades the answer against explicit criteria.",
    instruction=EVALUATOR_INSTRUCTION,
    tools=[list_ai_context, read_ai_context, read_file, search_codebase],
)

# --- Pipeline: answer first, then review ------------------------------------ #
root_agent = SequentialAgent(
    name="vaqueiro_reviewed",
    description="Vaqueiro answer followed by an independent quality review.",
    sub_agents=[answerer, evaluator],
)
