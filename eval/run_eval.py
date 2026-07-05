"""Lightweight eval runner for Vaqueiro.

For each case in eval_cases.jsonl it checks:
  - the expected tool was called (expect_tool)
  - the final answer contains the expected substrings (expect_contains)

Requires GOOGLE_API_KEY (it calls the model). Run from the repo root:
    python -m eval.run_eval
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from vaqueiro.agent import root_agent          # noqa: E402
from google.adk.runners import Runner           # noqa: E402
from google.adk.sessions import InMemorySessionService  # noqa: E402
from google.genai import types                  # noqa: E402
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / "vaqueiro" / ".env")


CASES = Path(__file__).resolve().parent / "eval_cases.jsonl"
APP = "vaqueiro-eval"


async def run_case(runner, session_service, case, i):
    uid, sid = "eval", f"case-{i}"
    await session_service.create_session(app_name=APP, user_id=uid, session_id=sid)
    msg = types.Content(role="user", parts=[types.Part(text=case["question"])])

    tools_called, final = [], ""
    async for event in runner.run_async(user_id=uid, session_id=sid, new_message=msg):
        for call in (event.get_function_calls() or []):
            tools_called.append(call.name)
        if event.is_final_response() and event.content and event.content.parts:
            final = "".join(p.text or "" for p in event.content.parts)

    tool_ok = (case.get("expect_tool") in tools_called) if case.get("expect_tool") else True
    if "expect_contains_any" in case:
        # list of groups; a group passes if ANY of its items appears; all groups must pass
        text_ok = all(
            any(s.lower() in final.lower() for s in group)
            for group in case["expect_contains_any"]
        )
    else:
        text_ok = all(s.lower() in final.lower() for s in case.get("expect_contains", []))
    return (tool_ok and text_ok), tools_called, final


async def main():
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name=APP, session_service=session_service)
    cases = [json.loads(l) for l in CASES.read_text().splitlines() if l.strip()]

    passed = 0
    for i, case in enumerate(cases):
        ok, tools_called, final = await run_case(runner, session_service, case, i)
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {case['question']}")
        if not ok:
            print(f"       tools={tools_called} answer={final[:120]!r}")
    print(f"\n{passed}/{len(cases)} passed")


if __name__ == "__main__":
    asyncio.run(main())
