from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Fact:
    text: str
    scope: str
    kind: str
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    reuse_count: int = 0
    source: str = "manual"


@dataclass(slots=True)
class ActivationPack:
    name: str
    scope: str
    body: str
    triggers: list[str] = field(default_factory=list)
    linked_skills: list[str] = field(default_factory=list)
    priority: int = 5
    max_tokens: int = 220
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)


@dataclass(slots=True)
class PromptPack:
    resident_parts: list[dict]
    activation_parts: list[dict]
    token_estimate: int
