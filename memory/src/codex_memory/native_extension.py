from __future__ import annotations

import json
from pathlib import Path

from .compiler import compile_summaries
from .store import MemoryStore
from .utils import estimate_tokens, write_text

DEFAULT_EXTENSION_ROOT = Path.home() / ".codex" / "memories_extensions"
DEFAULT_EXTENSION_NAME = "codex-memory"


def sync_native_extension(
    store: MemoryStore,
    *,
    extension_root: Path | None = None,
    extension_name: str = DEFAULT_EXTENSION_NAME,
    project_id: str | None = None,
) -> Path:
    store.init()
    compile_summaries(store)
    if project_id:
        store.init_project(project_id)
        compile_summaries(store, project_id=project_id)

    extension_dir = (extension_root or DEFAULT_EXTENSION_ROOT).expanduser().resolve() / extension_name
    export_dir = extension_dir / "export"
    projects_dir = export_dir / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)

    global_summary = store.summary_path("global").read_text(encoding="utf-8").strip()
    snapshot_sections = [
        "# Codex Memory Snapshot",
        "",
        "This snapshot is generated from the external `codex-memory` store.",
        "It is a curated durable-memory source, not a transcript dump.",
        "",
        "## Global Summary",
        global_summary or "- No global memories yet.",
        "",
    ]

    project_entries: list[dict[str, str | int]] = []
    for pid in _project_ids(store):
        project_summary = store.summary_path("project", project_id=pid).read_text(encoding="utf-8").strip()
        project_wake = store.load_project_text(pid, "wake").strip()
        project_snapshot = "\n".join([
            f"# Project Snapshot: {pid}",
            "",
            "## Project Wake",
            project_wake or "- No project wake guidance yet.",
            "",
            "## Project Summary",
            project_summary or "- No project memories yet.",
            "",
        ]).strip() + "\n"

        write_text(projects_dir / f"{pid}.md", project_snapshot)
        project_entries.append({
            "project_id": pid,
            "file": f"export/projects/{pid}.md",
            "token_estimate": estimate_tokens(project_snapshot),
        })

        snapshot_sections.extend([
            f"## Project: {pid}",
            project_summary or "- No project memories yet.",
            "",
        ])

    snapshot_text = "\n".join(snapshot_sections).strip() + "\n"
    write_text(export_dir / "snapshot.md", snapshot_text)

    manifest = {
        "extension": extension_name,
        "store_root": str(store.root),
        "exported_project_count": len(project_entries),
        "primary_snapshot": "export/snapshot.md",
        "projects": project_entries,
        "project_id_hint": project_id or "",
    }
    write_text(extension_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    write_text(extension_dir / "instructions.md", _build_extension_instructions())

    return extension_dir


def _project_ids(store: MemoryStore) -> list[str]:
    projects_root = store.root / "projects"
    if not projects_root.exists():
        return []
    return sorted(path.name for path in projects_root.iterdir() if path.is_dir())


def _build_extension_instructions() -> str:
    return """# Codex Memory Native Extension

This folder exposes curated memory from an external `codex-memory` store so the
Codex consolidation agent can learn from it during summarization.

## What To Read

Read `export/snapshot.md` first. It is the canonical compact export and contains:
- the durable global summary
- one section per known project with its compiled project summary

If you need project-specific nuance, read the matching file under
`export/projects/<project-id>.md`.

## How To Interpret This Source

- Treat this extension as a curated durable-memory source, not as a chat log.
- Prefer explicit preferences, conventions, corrections, environment facts, and
  reusable workflow hints.
- Prefer project summaries over project wake text when they disagree.
- Prefer omission over storing stale or speculative memory.
- Do not copy the persona or identity sections as if they were user facts unless
  they materially affect future behavior.
- Do not persist one-off debugging states, temporary plans, or transient errors
  unless they have become durable workflow knowledge.

## Priority Rules

- Global summary is cross-session baseline memory.
- Project summaries are higher priority when the current work clearly matches a
  named project.
- Project wake text is operational guidance, not biography.

## Anti-Patterns

- Do not turn duplicated project conventions into multiple separate memories.
- Do not store the same idea once from the global section and again from a
  project section unless the project-specific variant is materially different.
- Do not invent certainty where the exported summaries are silent.
"""
