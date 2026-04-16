from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from codex_memory.compiler import compile_summaries
from codex_memory.cli import (
    _build_claude_append_system_prompt,
    _build_claude_launch_command,
    _build_codex_developer_instruction_override,
)
from codex_memory.native_extension import sync_native_extension
from codex_memory.models import ActivationPack, Fact
from codex_memory.promotion import promote_journal
from codex_memory.retrieval import build_prompt_pack, build_startup_pack, render_startup_prompt
from codex_memory.store import MemoryStore


class CodexMemoryTests(unittest.TestCase):
    def test_compile_and_retrieve_activation_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = MemoryStore(Path(tmp))
            store.init()
            store.init_project("demo")

            store.add_fact(Fact(
                text="User prefers concise answers with minimal fluff.",
                scope="global",
                kind="preference",
                tags=["style"],
            ))
            store.add_fact(Fact(
                text="Use pnpm instead of npm in this repo.",
                scope="project",
                kind="convention",
                tags=["build"],
            ), project_id="demo")

            store.add_activation_pack(ActivationPack(
                name="pnpm-build-fixes",
                scope="project",
                body="This repo uses pnpm. Verify package-manager commands before installs or tests.",
                triggers=["pnpm", "build", "test"],
                linked_skills=["frontend-developer"],
                priority=8,
            ), project_id="demo")

            compile_summaries(store, project_id="demo")
            pack = build_prompt_pack(
                store,
                project_id="demo",
                task="Fix pnpm build and test failure",
                selected_skills=["frontend-developer"],
            )

            resident_names = [part["name"] for part in pack.resident_parts]
            names = [part["name"] for part in pack.activation_parts]
            self.assertIn("persona-contract", resident_names)
            self.assertIn("pnpm-build-fixes", names)
            self.assertLessEqual(pack.token_estimate, 1400)
            self.assertTrue(pack.activation_parts[0]["linked_skill_match"])

    def test_startup_pack_and_journal_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = MemoryStore(Path(tmp))
            store.init()
            store.init_project("demo")

            startup = build_startup_pack(store, project_id="demo")
            startup_names = [part["name"] for part in startup.resident_parts]
            self.assertIn("persona-contract", startup_names)
            self.assertIn("wake", startup_names)
            self.assertIn("project-wake:demo", startup_names)
            startup_text = render_startup_prompt(startup)
            self.assertIn("Startup bootstrap for this terminal session.", startup_text)
            self.assertLessEqual(startup.token_estimate, 1100)

            store.append_journal(
                "demo",
                "- Fixed pnpm install issue by checking package-manager commands first.\n- Use pnpm instead of npm in this repo.",
                "2026-03-31",
            )
            result = promote_journal(store, project_id="demo", day="2026-03-31")
            self.assertGreaterEqual(result["facts_added"], 1)

            promoted_pack = build_prompt_pack(store, project_id="demo", task="Fix pnpm install failure")
            names = [part["name"] for part in promoted_pack.activation_parts]
            self.assertTrue(any("fixed-pnpm-install-issue" in name for name in names))

    def test_skill_linked_pack_can_activate_from_skill_choice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = MemoryStore(Path(tmp))
            store.init()
            store.init_project("demo")

            store.add_activation_pack(ActivationPack(
                name="trpc-context",
                scope="project",
                body="Use the repo's existing tRPC router patterns before adding new handlers.",
                triggers=["router"],
                linked_skills=["backend-architect"],
                priority=6,
            ), project_id="demo")

            compile_summaries(store, project_id="demo")
            pack = build_prompt_pack(
                store,
                project_id="demo",
                task="Add new endpoint",
                selected_skills=["backend-architect"],
            )
            names = [part["name"] for part in pack.activation_parts]
            self.assertIn("trpc-context", names)

    def test_codex_developer_override_includes_identity_precedence(self) -> None:
        startup_text = (
            "Startup bootstrap for this terminal session.\n\n"
            "## soul\n"
            "# Soul\n\n"
            "Fun and playful.\n\n"
            "## identity\n"
            "# Identity\n\n"
            "Strong operator identity.\n"
        )

        built = _build_codex_developer_instruction_override(startup_text)
        self.assertIn("## Identity Precedence", built)
        self.assertIn("Strong operator identity.", built)
        self.assertIn("Fun and playful.", built)
        self.assertIn("## Startup Bootstrap", built)

    def test_claude_prompt_preserves_skill_routing_instructions(self) -> None:
        startup_text = (
            "Startup bootstrap for this terminal session.\n\n"
            "## soul\n"
            "# Soul\n\n"
            "Fun and playful.\n\n"
            "## identity\n"
            "# Identity\n\n"
            "Strong operator identity.\n"
        )

        built = _build_claude_append_system_prompt(startup_text)
        self.assertIn("## Claude Integration", built)
        self.assertIn("Preserve Claude Code's default tool behavior, skill routing, slash commands, agents, and autonomous skill use.", built)
        self.assertIn("## Startup Bootstrap", built)

    def test_claude_launch_command_uses_append_system_prompt(self) -> None:
        command = _build_claude_launch_command(
            claude_bin="claude",
            cwd="/tmp/demo",
            startup_text="Startup bootstrap for this terminal session.\n",
            prompt="Fix the build",
            extra_args=["--model", "sonnet"],
        )

        self.assertEqual(command[0], "claude")
        self.assertIn("--append-system-prompt", command)
        self.assertIn("--add-dir", command)
        self.assertIn("/tmp/demo", command)
        self.assertEqual(command[-1], "Fix the build")

    def test_sync_native_extension_exports_snapshot_and_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            store = MemoryStore(tmp_path / "store")
            store.init()
            store.init_project("demo")

            store.add_fact(Fact(
                text="User prefers terse status updates.",
                scope="global",
                kind="preference",
                tags=["style"],
            ))
            store.add_fact(Fact(
                text="Use pnpm in this repo.",
                scope="project",
                kind="convention",
                tags=["build"],
            ), project_id="demo")
            compile_summaries(store, project_id="demo")

            extension_dir = sync_native_extension(
                store,
                extension_root=tmp_path / "memories_extensions",
                project_id="demo",
            )

            instructions = (extension_dir / "instructions.md").read_text(encoding="utf-8")
            snapshot = (extension_dir / "export" / "snapshot.md").read_text(encoding="utf-8")
            project_snapshot = (extension_dir / "export" / "projects" / "demo.md").read_text(encoding="utf-8")
            manifest = json.loads((extension_dir / "manifest.json").read_text(encoding="utf-8"))

            self.assertIn("Read `export/snapshot.md` first.", instructions)
            self.assertIn("## Global Summary", snapshot)
            self.assertIn("Use pnpm in this repo.", snapshot)
            self.assertIn("# Project Snapshot: demo", project_snapshot)
            self.assertEqual(manifest["primary_snapshot"], "export/snapshot.md")
            self.assertEqual(manifest["exported_project_count"], 1)


if __name__ == "__main__":
    unittest.main()
