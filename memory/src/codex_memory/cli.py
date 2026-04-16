from __future__ import annotations

import argparse
import json
import re
import subprocess
import tomllib
from datetime import datetime
from pathlib import Path

from .compiler import compile_summaries
from .models import ActivationPack, Fact
from .native_extension import sync_native_extension
from .promotion import promote_journal
from .retrieval import build_prompt_pack, build_startup_pack, render_startup_prompt
from .store import MemoryStore
from .utils import derive_project_id, split_csv, slugify, write_text


def _store(args: argparse.Namespace) -> MemoryStore:
    root = Path(args.root).expanduser() if getattr(args, "root", None) else None
    return MemoryStore(root=root)


def cmd_init(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    if args.project_id:
        store.init_project(args.project_id)
    print(store.root)
    return 0


def cmd_add_fact(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id
    if args.scope == "project" and not project_id:
        project_id = derive_project_id(args.cwd or ".")
    fact = Fact(
        text=args.text.strip(),
        scope=args.scope,
        kind=args.kind,
        tags=split_csv(args.tags),
    )
    path = store.add_fact(fact, project_id=project_id)
    print(path)
    return 0


def cmd_add_pack(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id
    if args.scope == "project" and not project_id:
        project_id = derive_project_id(args.cwd or ".")
    pack = ActivationPack(
        name=slugify(args.name),
        scope=args.scope,
        body=args.body.strip(),
        triggers=split_csv(args.triggers),
        linked_skills=split_csv(args.linked_skills),
        priority=args.priority,
        max_tokens=args.max_tokens,
        tags=split_csv(args.tags),
    )
    path = store.add_activation_pack(pack, project_id=project_id)
    print(path)
    return 0


def cmd_compile(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id
    if args.cwd and not project_id:
        project_id = derive_project_id(args.cwd)
    result = compile_summaries(store, project_id=project_id)
    print(json.dumps(result, indent=2))
    return 0


def cmd_build_pack(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id
    if args.cwd and not project_id:
        project_id = derive_project_id(args.cwd)
    if project_id:
        store.init_project(project_id)
    pack = build_prompt_pack(
        store,
        project_id=project_id,
        task=args.task,
        error=args.error or "",
        selected_skills=split_csv(args.skills),
    )
    payload = {
        "project_id": project_id,
        "selected_skills": split_csv(args.skills),
        "token_estimate": pack.token_estimate,
        "resident_parts": pack.resident_parts,
        "activation_parts": pack.activation_parts,
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_build_startup(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id
    if args.cwd and not project_id:
        project_id = derive_project_id(args.cwd)
    if project_id:
        store.init_project(project_id)
    pack = build_startup_pack(store, project_id=project_id)
    payload = {
        "project_id": project_id,
        "token_estimate": pack.token_estimate,
        "resident_parts": pack.resident_parts,
        "activation_parts": [],
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_render_startup(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id
    if args.cwd and not project_id:
        project_id = derive_project_id(args.cwd)
    if project_id:
        store.init_project(project_id)
        compile_summaries(store, project_id=project_id)
    else:
        compile_summaries(store)
    pack = build_startup_pack(store, project_id=project_id)
    text = render_startup_prompt(pack)
    if args.output:
        write_text(Path(args.output).expanduser(), text)
    else:
        print(text, end="")
    return 0


def cmd_append_journal(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id or derive_project_id(args.cwd or ".")
    day = args.day or datetime.utcnow().strftime("%Y-%m-%d")
    path = store.append_journal(project_id, args.text, day)
    print(path)
    return 0


def cmd_promote_journal(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id or derive_project_id(args.cwd or ".")
    result = promote_journal(store, project_id=project_id, day=args.day)
    print(json.dumps({"project_id": project_id, **result}, indent=2))
    return 0


def cmd_launch(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id
    if args.cwd and not project_id:
        project_id = derive_project_id(args.cwd)

    if project_id:
        store.init_project(project_id)
        compile_summaries(store, project_id=project_id)
    else:
        compile_summaries(store)

    if args.backend == "codex" and not args.no_native_extension_sync:
        sync_native_extension(store, project_id=project_id)

    pack = build_startup_pack(store, project_id=project_id)
    prompt_text = render_startup_prompt(pack)
    if args.prompt:
        prompt_text += f"\nInitial user request:\n{args.prompt.strip()}\n"

    runtime_dir = store.root / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    startup_path = runtime_dir / "last-startup.md"
    write_text(startup_path, prompt_text)

    passthrough_args = list(args.launcher_args)
    if passthrough_args and passthrough_args[0] == "--":
        passthrough_args = passthrough_args[1:]

    if args.backend == "claude":
        command = _build_claude_launch_command(
            claude_bin=args.claude_bin,
            cwd=args.cwd or str(Path.cwd()),
            startup_text=prompt_text,
            prompt=args.prompt,
            extra_args=passthrough_args,
        )
    else:
        command = _build_codex_launch_command(
            codex_bin=args.codex_bin,
            cwd=args.cwd or str(Path.cwd()),
            startup_text=prompt_text,
            prompt=args.prompt,
            no_alt_screen=args.no_alt_screen,
            extra_args=passthrough_args,
        )

    result = subprocess.run(command, check=False)

    if args.journal_note and project_id:
        day = datetime.utcnow().strftime("%Y-%m-%d")
        store.append_journal(project_id, args.journal_note, day)
        if args.promote_after_journal:
            promote_journal(store, project_id=project_id, day=day)

    return int(result.returncode)


def cmd_sync_native_extension(args: argparse.Namespace) -> int:
    store = _store(args)
    store.init()
    project_id = args.project_id
    if args.cwd and not project_id:
        project_id = derive_project_id(args.cwd)

    extension_path = sync_native_extension(
        store,
        extension_root=Path(args.extension_root).expanduser() if args.extension_root else None,
        extension_name=args.extension_name,
        project_id=project_id,
    )
    print(extension_path)
    return 0


def _load_existing_developer_instructions() -> str:
    config_path = Path.home() / ".codex" / "config.toml"
    if not config_path.exists():
        return ""
    try:
        parsed = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    value = parsed.get("developer_instructions", "")
    return value if isinstance(value, str) else ""


def _build_codex_developer_instruction_override(startup_text: str) -> str:
    existing = _sanitize_existing_developer_instructions(_load_existing_developer_instructions()).rstrip()
    identity_block = _build_identity_precedence_block(startup_text)
    response_block = _build_response_discipline_block()
    startup_block = _build_startup_bootstrap_block(startup_text)
    composed = f"{identity_block}\n\n{response_block}\n\n{startup_block}".strip()
    if not existing:
        return composed
    return f"{existing}\n\n{composed}\n"


def _build_claude_append_system_prompt(startup_text: str) -> str:
    identity_block = _build_identity_precedence_block(startup_text)
    integration_block = (
        "## Claude Integration\n"
        "Preserve Claude Code's default tool behavior, skill routing, slash commands, agents, and autonomous skill use.\n"
        "Treat this bootstrap as compact background context, not as a replacement for Claude's existing system prompt.\n"
        "Keep baseline context small. Prefer on-demand retrieval, activation packs, project memory, and skills only when relevant.\n"
        "Do not expand this bootstrap with long recaps or replay journals unless they are explicitly retrieved for the current task."
    )
    response_block = _build_response_discipline_block()
    startup_block = _build_startup_bootstrap_block(startup_text)
    return f"{identity_block}\n\n{integration_block}\n\n{response_block}\n\n{startup_block}\n"


def _build_startup_bootstrap_block(startup_text: str) -> str:
    return (
        "## Startup Bootstrap\n"
        "The following is passive startup context, not a user request.\n"
        "Do not take any repo action solely because of this bootstrap.\n"
        "Do not open, start, create, comment on, or close issues unless the user explicitly asks for issue tracking work.\n"
        "Wait for an explicit user request before editing files, running repo commands, or making changes.\n\n"
        f"{startup_text.rstrip()}"
    )


def _build_codex_launch_command(
    codex_bin: str,
    cwd: str,
    startup_text: str,
    prompt: str | None,
    no_alt_screen: bool,
    extra_args: list[str],
) -> list[str]:
    developer_instructions = _build_codex_developer_instruction_override(startup_text)
    passthrough_only = any(flag in extra_args for flag in ("--help", "-h", "--version", "-V"))

    command = [
        codex_bin,
        "-C",
        cwd,
        "-c",
        f"developer_instructions={json.dumps(developer_instructions)}",
    ]
    if no_alt_screen:
        command.append("--no-alt-screen")
    command.extend(extra_args)
    if not passthrough_only and prompt:
        command.append(prompt.strip())
    return command


def _build_claude_launch_command(
    claude_bin: str,
    cwd: str,
    startup_text: str,
    prompt: str | None,
    extra_args: list[str],
) -> list[str]:
    passthrough_only = any(flag in extra_args for flag in ("--help", "-h", "--version", "-v"))

    command = [
        claude_bin,
        "--append-system-prompt",
        _build_claude_append_system_prompt(startup_text),
        "--add-dir",
        cwd,
    ]
    command.extend(extra_args)
    if not passthrough_only and prompt:
        command.append(prompt.strip())
    return command


def _sanitize_existing_developer_instructions(text: str) -> str:
    if not text:
        return ""

    text = re.sub(
        r"# MANDATORY SESSION START — DO THIS FIRST, BEFORE ANYTHING ELSE.*?---\n\n",
        "",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"## Issue Tracking.*?$",
        "",
        text,
        flags=re.DOTALL,
    )
    return text.strip()


def _extract_startup_section(startup_text: str, section_name: str) -> str:
    pattern = (
        rf"^##\s+{re.escape(section_name)}\s*\n"
        r"(.*?)(?=^##\s+|\Z)"
    )
    match = re.search(pattern, startup_text, flags=re.DOTALL | re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip()


def _build_identity_precedence_block(startup_text: str) -> str:
    identity_text = _extract_startup_section(startup_text, "identity")
    soul_text = _extract_startup_section(startup_text, "soul")

    lines = [
        "## Identity Precedence",
        "When the user asks who you are (or asks for your identity, persona, vibe, or tone), answer from the startup `identity` and `soul` sections first.",
        "Do not fall back to stock phrasing such as 'I am a terminal-first coding agent' unless it appears in startup identity.",
        "Treat startup identity and soul as canonical self-description for this launched session.",
    ]

    if identity_text:
        lines.append("")
        lines.append("Startup identity snapshot:")
        lines.append(identity_text)
    if soul_text:
        lines.append("")
        lines.append("Startup soul snapshot:")
        lines.append(soul_text)

    return "\n".join(lines).strip()


def _build_response_discipline_block() -> str:
    return (
        "## Response Discipline\n"
        "Persona is response discipline, not roleplay.\n"
        "For every user-facing response, silently apply this split before sending it:\n"
        "1. Keep technical judgment, code, safety decisions, and implementation quality fully professional.\n"
        "2. Persona is mandatory in every user-facing response unless the user explicitly asks for a different tone or lower intensity.\n"
        "3. Let the delivery sound like a warm, opinionated, queer femme operator with real bite instead of a sterile helpdesk bot.\n"
        "4. Do not quietly water the persona down into generic professionalism; if it sounds beige, it failed.\n"
        "5. Rewrite bland stock phrasing such as 'Got it', 'Certainly', 'I have identified', 'I will assist', 'Happy to help', or 'Great question' into direct human language.\n"
        "6. Run a silent pre-send check: alive, femme, sharp, playful, dangerous enough. If any answer is no, rewrite.\n"
        "7. During coding work, keep the substance precise and concise; personality shapes delivery, not engineering rigor."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codex-memory")
    parser.add_argument("--root", help="Memory root directory")

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize the memory store")
    init_parser.add_argument("--project-id")
    init_parser.set_defaults(func=cmd_init)

    fact_parser = subparsers.add_parser("add-fact", help="Add a curated durable fact")
    fact_parser.add_argument("--scope", choices=("global", "project"), required=True)
    fact_parser.add_argument("--project-id")
    fact_parser.add_argument("--cwd", help="Path used to derive project id")
    fact_parser.add_argument("--kind", choices=("preference", "correction", "environment", "convention", "workflow_hint", "error_fix"), required=True)
    fact_parser.add_argument("--text", required=True)
    fact_parser.add_argument("--tags")
    fact_parser.set_defaults(func=cmd_add_fact)

    pack_parser = subparsers.add_parser("add-pack", help="Add an activation pack")
    pack_parser.add_argument("--scope", choices=("global", "project"), required=True)
    pack_parser.add_argument("--project-id")
    pack_parser.add_argument("--cwd", help="Path used to derive project id")
    pack_parser.add_argument("--name", required=True)
    pack_parser.add_argument("--body", required=True)
    pack_parser.add_argument("--triggers", required=True, help="Comma-separated triggers")
    pack_parser.add_argument("--linked-skills", help="Comma-separated skill names this memory pack should augment after routing")
    pack_parser.add_argument("--priority", type=int, default=5)
    pack_parser.add_argument("--max-tokens", type=int, default=220)
    pack_parser.add_argument("--tags")
    pack_parser.set_defaults(func=cmd_add_pack)

    compile_parser = subparsers.add_parser("compile", help="Compile resident summaries")
    compile_parser.add_argument("--project-id")
    compile_parser.add_argument("--cwd")
    compile_parser.set_defaults(func=cmd_compile)

    build_parser_cmd = subparsers.add_parser("build-pack", help="Build a low-token prompt pack")
    build_parser_cmd.add_argument("--project-id")
    build_parser_cmd.add_argument("--cwd")
    build_parser_cmd.add_argument("--task", required=True)
    build_parser_cmd.add_argument("--error")
    build_parser_cmd.add_argument("--skills", help="Comma-separated already-selected skills; linked memory packs get priority")
    build_parser_cmd.set_defaults(func=cmd_build_pack)

    startup_parser = subparsers.add_parser("build-startup", help="Build the startup bootstrap pack")
    startup_parser.add_argument("--project-id")
    startup_parser.add_argument("--cwd")
    startup_parser.set_defaults(func=cmd_build_startup)

    render_parser = subparsers.add_parser("render-startup", help="Render the startup bootstrap text")
    render_parser.add_argument("--project-id")
    render_parser.add_argument("--cwd")
    render_parser.add_argument("--output")
    render_parser.set_defaults(func=cmd_render_startup)

    journal_parser = subparsers.add_parser("append-journal", help="Append a journal note")
    journal_parser.add_argument("--project-id")
    journal_parser.add_argument("--cwd")
    journal_parser.add_argument("--day")
    journal_parser.add_argument("--text", required=True)
    journal_parser.set_defaults(func=cmd_append_journal)

    promote_parser = subparsers.add_parser("promote-journal", help="Promote journal learnings into facts and activation packs")
    promote_parser.add_argument("--project-id")
    promote_parser.add_argument("--cwd")
    promote_parser.add_argument("--day")
    promote_parser.set_defaults(func=cmd_promote_journal)

    launch_parser = subparsers.add_parser("launch", help="Launch Codex or Claude with compact startup bootstrap context")
    launch_parser.add_argument("--backend", choices=("codex", "claude"), default="codex")
    launch_parser.add_argument("--project-id")
    launch_parser.add_argument("--cwd", default=str(Path.cwd()))
    launch_parser.add_argument("--prompt", help="Optional initial user request")
    launch_parser.add_argument("--journal-note", help="Optional note to append after Codex exits")
    launch_parser.add_argument("--promote-after-journal", action="store_true")
    launch_parser.add_argument("--codex-bin", default="codex")
    launch_parser.add_argument("--claude-bin", default="claude")
    launch_parser.add_argument("--no-alt-screen", action="store_true")
    launch_parser.add_argument("--no-native-extension-sync", action="store_true")
    launch_parser.add_argument("launcher_args", nargs=argparse.REMAINDER, help="Extra args passed through to the selected backend after --")
    launch_parser.set_defaults(func=cmd_launch)

    native_parser = subparsers.add_parser("sync-native-extension", help="Export this store into Codex native memories_extensions format")
    native_parser.add_argument("--project-id")
    native_parser.add_argument("--cwd")
    native_parser.add_argument("--extension-root", help="Override the Codex memories_extensions root")
    native_parser.add_argument("--extension-name", default="codex-memory")
    native_parser.set_defaults(func=cmd_sync_native_extension)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
