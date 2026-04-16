from __future__ import annotations

from .config import ACTIVATION_BUDGET_TOKENS, RESIDENT_BUDGET_TOKENS, STARTUP_BUDGET_TOKENS, TOTAL_BUDGET_TOKENS
from .models import PromptPack
from .store import MemoryStore
from .utils import clamp_parts_by_tokens, estimate_tokens


def _match_score(pack: dict, haystack: str) -> int:
    triggers = [trigger.lower() for trigger in pack.get("triggers", [])]
    lower_haystack = haystack.lower()
    return sum(1 for trigger in triggers if trigger and trigger in lower_haystack)


def _linked_skill_score(pack: dict, selected_skills: list[str]) -> int:
    if not selected_skills:
        return 0
    linked = {skill.lower() for skill in pack.get("linked_skills", [])}
    chosen = {skill.lower() for skill in selected_skills}
    return sum(1 for skill in linked if skill in chosen)


def build_prompt_pack(
    store: MemoryStore,
    project_id: str | None,
    task: str,
    error: str = "",
    selected_skills: list[str] | None = None,
) -> PromptPack:
    resident_parts = []

    for label, text, priority in (
        ("persona-contract", store.load_core_text("persona-contract"), 130),
        ("identity", store.load_core_text("identity"), 125),
        ("soul", store.load_core_text("soul"), 120),
        ("global-summary", store.summary_path("global").read_text(encoding="utf-8"), 90),
    ):
        resident_parts.append({
            "name": label,
            "body": text,
            "token_estimate": estimate_tokens(text),
            "priority": priority,
        })

    if project_id:
        store.init_project(project_id)
        project_summary = store.summary_path("project", project_id=project_id).read_text(encoding="utf-8")
        resident_parts.append({
            "name": f"project-summary:{project_id}",
            "body": project_summary,
            "token_estimate": estimate_tokens(project_summary),
            "priority": 95,
        })

    resident_parts.sort(key=lambda part: (part["priority"], -part["token_estimate"]), reverse=True)
    resident_parts = clamp_parts_by_tokens(resident_parts, RESIDENT_BUDGET_TOKENS)

    haystack = " ".join(part for part in (task, error) if part).strip()
    selected_skills = selected_skills or []
    all_packs = store.load_activation_packs("global")
    if project_id:
        all_packs.extend(store.load_activation_packs("project", project_id=project_id))

    scored = []
    for pack in all_packs:
        score = _match_score(pack, haystack)
        skill_score = _linked_skill_score(pack, selected_skills)
        if score <= 0 and skill_score <= 0:
            continue
        body = pack["body"]
        scored.append({
            "name": pack["name"],
            "body": body,
            "token_estimate": min(int(pack.get("max_tokens", 220)), estimate_tokens(body)),
            "priority": int(pack.get("priority", 5)) + score + (skill_score * 10),
            "linked_skill_match": skill_score > 0,
        })

    scored.sort(key=lambda part: (part["linked_skill_match"], part["priority"]), reverse=True)
    activation_parts = clamp_parts_by_tokens(scored, ACTIVATION_BUDGET_TOKENS)

    total_tokens = sum(part["token_estimate"] for part in resident_parts + activation_parts)
    if total_tokens > TOTAL_BUDGET_TOKENS:
        overflow = total_tokens - TOTAL_BUDGET_TOKENS
        while activation_parts and overflow > 0:
            dropped = activation_parts.pop()
            overflow -= dropped["token_estimate"]
        total_tokens = sum(part["token_estimate"] for part in resident_parts + activation_parts)

    return PromptPack(
        resident_parts=resident_parts,
        activation_parts=activation_parts,
        token_estimate=total_tokens,
    )


def build_startup_pack(
    store: MemoryStore,
    project_id: str | None,
) -> PromptPack:
    resident_parts = []
    for label, text, priority in (
        ("persona-contract", store.load_core_text("persona-contract"), 150),
        ("wake", store.load_core_text("wake"), 145),
        ("identity", store.load_core_text("identity"), 140),
        ("policy", store.load_core_text("policy"), 135),
        ("soul", store.load_core_text("soul"), 120),
        ("global-summary", store.summary_path("global").read_text(encoding="utf-8"), 80),
    ):
        resident_parts.append({
            "name": label,
            "body": text,
            "token_estimate": estimate_tokens(text),
            "priority": priority,
        })

    if project_id:
        store.init_project(project_id)
        for label, text, priority in (
            (f"project-wake:{project_id}", store.load_project_text(project_id, "wake"), 142),
            (f"project-summary:{project_id}", store.summary_path("project", project_id=project_id).read_text(encoding="utf-8"), 85),
        ):
            resident_parts.append({
                "name": label,
                "body": text,
                "token_estimate": estimate_tokens(text),
                "priority": priority,
            })

    resident_parts.sort(key=lambda part: (part["priority"], -part["token_estimate"]), reverse=True)
    resident_parts = clamp_parts_by_tokens(resident_parts, STARTUP_BUDGET_TOKENS)
    total_tokens = sum(part["token_estimate"] for part in resident_parts)
    return PromptPack(resident_parts=resident_parts, activation_parts=[], token_estimate=total_tokens)


def render_startup_prompt(pack: PromptPack) -> str:
    lines = [
        "Startup bootstrap for this terminal session.",
        "Internalize this context quietly and use it as background guidance.",
        "Keep baseline memory compact. Prefer activation packs, skills, and journal recall only when relevant.",
        "",
    ]
    for part in pack.resident_parts:
        lines.append(f"## {part['name']}")
        lines.append(part["body"].rstrip())
        lines.append("")
    lines.append(f"Startup token estimate: {pack.token_estimate}")
    return "\n".join(lines).strip() + "\n"
