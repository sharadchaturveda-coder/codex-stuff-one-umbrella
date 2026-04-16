from __future__ import annotations

import re

from .compiler import compile_summaries
from .models import ActivationPack, Fact
from .store import MemoryStore
from .utils import slugify


FACT_PATTERNS = (
    ("convention", re.compile(r"\b(use|uses|using)\s+([a-z0-9._/-]+)\s+instead of\s+([a-z0-9._/-]+)\b", re.IGNORECASE)),
    ("error_fix", re.compile(r"\b(fix|fixed|workaround|resolved)\b", re.IGNORECASE)),
    ("preference", re.compile(r"\b(prefers?|avoid|always|never)\b", re.IGNORECASE)),
)


def _existing_fact_texts(store: MemoryStore, scope: str, project_id: str | None = None) -> set[str]:
    return {row["text"] for row in store.load_facts(scope, project_id=project_id)}


def promote_journal(store: MemoryStore, project_id: str, day: str | None = None) -> dict:
    journal_entries = store.load_journal_entries(project_id, day=day)
    if not journal_entries:
        return {"facts_added": 0, "packs_added": 0}

    project_existing = _existing_fact_texts(store, "project", project_id=project_id)
    added_facts = 0
    added_packs = 0

    for entry in journal_entries:
        lines = [line.strip("- ").strip() for line in entry.splitlines() if line.strip()]
        for line in lines:
            lower = line.lower()
            kind = None
            for candidate_kind, pattern in FACT_PATTERNS:
                if pattern.search(line):
                    kind = candidate_kind
                    break

            if kind and line not in project_existing:
                store.add_fact(
                    Fact(
                        text=line,
                        scope="project",
                        kind=kind,
                        tags=["journal-promoted"],
                        source="journal-promotion",
                    ),
                    project_id=project_id,
                )
                project_existing.add(line)
                added_facts += 1

            if any(word in lower for word in ("fix", "fixed", "workaround", "resolved")) and len(line.split()) >= 6:
                name = slugify(line[:48])
                existing_pack_names = {pack["name"] for pack in store.load_activation_packs("project", project_id=project_id)}
                if name not in existing_pack_names:
                    triggers = []
                    for token in re.findall(r"[a-z0-9._/-]+", lower):
                        if len(token) >= 4 and token not in {"this", "that", "with", "from", "have"}:
                            triggers.append(token)
                    pack = ActivationPack(
                        name=name,
                        scope="project",
                        body=line,
                        triggers=sorted(set(triggers[:6])),
                        linked_skills=[],
                        priority=7,
                        max_tokens=180,
                        tags=["journal-promoted", "debug"],
                    )
                    store.add_activation_pack(pack, project_id=project_id)
                    added_packs += 1

    compile_summaries(store, project_id=project_id)
    return {"facts_added": added_facts, "packs_added": added_packs}
