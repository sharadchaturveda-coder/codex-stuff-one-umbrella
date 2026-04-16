from __future__ import annotations

from .config import (
    FACT_KIND_WEIGHTS,
    GLOBAL_SUMMARY_BUDGET_TOKENS,
    PROJECT_SUMMARY_BUDGET_TOKENS,
)
from .store import MemoryStore
from .utils import estimate_tokens, write_text


def _score_fact(fact: dict) -> int:
    base = FACT_KIND_WEIGHTS.get(fact.get("kind", ""), 5)
    tags_bonus = min(2, len(fact.get("tags", [])))
    reuse_bonus = min(3, int(fact.get("reuse_count", 0)))
    return base + tags_bonus + reuse_bonus


def _compile_summary(title: str, facts: list[dict], token_budget: int) -> str:
    ranked = sorted(facts, key=_score_fact, reverse=True)
    lines = [title, ""]
    consumed = estimate_tokens("\n".join(lines))
    count = 0
    for fact in ranked:
        line = f"- {fact['text']}"
        line_tokens = estimate_tokens(line)
        if consumed + line_tokens > token_budget:
            continue
        lines.append(line)
        consumed += line_tokens
        count += 1
    if count == 0:
        lines.append("- No curated memories yet.")
    return "\n".join(lines) + "\n"


def compile_summaries(store: MemoryStore, project_id: str | None = None) -> dict:
    global_facts = store.load_facts("global")
    global_summary = _compile_summary(
        "# Global Memory Summary",
        global_facts,
        GLOBAL_SUMMARY_BUDGET_TOKENS,
    )
    write_text(store.summary_path("global"), global_summary)

    result = {
        "global_summary_tokens": estimate_tokens(global_summary),
        "project_summary_tokens": 0,
    }

    if project_id:
        project_facts = store.load_facts("project", project_id=project_id)
        project_summary = _compile_summary(
            "# Project Memory Summary",
            project_facts,
            PROJECT_SUMMARY_BUDGET_TOKENS,
        )
        write_text(store.summary_path("project", project_id=project_id), project_summary)
        result["project_summary_tokens"] = estimate_tokens(project_summary)

    return result
