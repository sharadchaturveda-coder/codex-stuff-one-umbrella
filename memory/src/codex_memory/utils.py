from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Iterable


def estimate_tokens(text: str) -> int:
    words = len(re.findall(r"\S+", text))
    return max(1, int(words * 1.3))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "project"


def derive_project_id(path: str) -> str:
    resolved = Path(path).expanduser().resolve()
    digest = hashlib.sha1(str(resolved).encode("utf-8")).hexdigest()[:8]
    return f"{slugify(resolved.name)}-{digest}"


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def clamp_parts_by_tokens(parts: Iterable[dict], token_budget: int) -> list[dict]:
    total = 0
    chosen: list[dict] = []
    for part in parts:
        part_tokens = int(part["token_estimate"])
        if total + part_tokens > token_budget:
            continue
        chosen.append(part)
        total += part_tokens
    return chosen
