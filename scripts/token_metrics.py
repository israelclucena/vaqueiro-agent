"""Estimate the token cost of answering with Vaqueiro's curated .ai-context/
versus naively feeding the whole project ("rescan everything").

Uses google.genai count_tokens when GOOGLE_API_KEY is set; otherwise falls back
to a rough chars/4 estimate so it also runs offline. Run from the repo root:
    python scripts/token_metrics.py
"""
import os
from pathlib import Path

ROOT = Path(os.getenv("AI_CONTEXT_ROOT", "./sample_project")).resolve()
CTX = ROOT / ".ai-context"
SOURCE_EXT = {".ts", ".js", ".html", ".scss", ".css", ".py", ".json", ".md"}


def _read_all(paths) -> str:
    return "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in paths)


def _count(text: str) -> int:
    key = os.getenv("GOOGLE_API_KEY")
    if key:
        try:
            from google import genai
            client = genai.Client(api_key=key)
            return client.models.count_tokens(
                model="gemini-flash-latest", contents=text
            ).total_tokens
        except Exception:
            pass
    return len(text) // 4  # rough offline estimate


def main():
    all_files = [p for p in ROOT.rglob("*")
                 if p.is_file() and p.suffix in SOURCE_EXT
                 and ".git" not in p.parts and ".ai-context" not in p.parts]
    ctx_files = sorted(CTX.glob("*.md")) if CTX.is_dir() else []

    baseline = _count(_read_all(all_files))   # feed the whole project
    curated = _count(_read_all(ctx_files))    # feed only .ai-context/

    print(f"Project files scanned : {len(all_files)}")
    print(f"Baseline (rescan all) : {baseline:,} tokens")
    print(f"Vaqueiro (.ai-context): {curated:,} tokens")
    if baseline:
        print(f"Reduction             : {100 * (baseline - curated) / baseline:.0f}%")


if __name__ == "__main__":
    main()
