# Codex Memory

`codex-memory` is a low-token sidecar memory system for coding agents that need
cross-session continuity without stuffing every prior detail into prompt
context.

It stores durable identity, policy, user preferences, project conventions, and
small task-specific memory packs on disk, then compiles only the smallest useful
subset back into the session.

On Codex `0.120.0+`, it can also export that curated store into native
`~/.codex/memories_extensions/` so Codex's own consolidation agent can learn
from the same memory source.

The design goal is simple:

- keep resident memory compact
- retrieve richer context only when the current task needs it
- preserve the host agent's native skills, tools, and routing model
- treat journals as raw episodic recall, not default prompt baggage

## What It Stores

- `core`: stable `soul.md`, `identity.md`, `persona-contract.md`, `policy.md`
- `core/wake.md`: terminal startup orientation
- `global`: durable user-level facts plus a compiled summary
- `projects/<project-id>`: durable project facts, journal, activation packs
- `skills`: procedural knowledge that should load only when relevant

Only a compact resident pack should be injected every turn. Everything else is
retrieval-only and activated on demand.

## Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Memory Layout](#memory-layout)
- [Command Reference](#command-reference)
- [Claude and Codex Integration](#claude-and-codex-integration)
- [Design Rules](#design-rules)
- [Development](#development)
- [Additional Docs](#additional-docs)

## Install

```bash
cd /home/dr_sharad/codex-memory
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

If you do not want a virtualenv, the commands in this repo also work with:

```bash
PYTHONPATH=src python3 -m codex_memory.cli --help
```

## Quick Start

Initialize a store:

```bash
codex-memory init
```

Add a few stable facts:

```bash
codex-memory add-fact --scope global --kind preference --text "User prefers concise answers with minimal fluff." --tags style,communication
codex-memory add-fact --scope project --project-id demo --kind convention --text "Use pnpm instead of npm in this repo." --tags build,tooling
```

Create an activation pack:

```bash
codex-memory add-pack \
  --scope project \
  --project-id demo \
  --name pnpm-build-fixes \
  --triggers pnpm,build,test \
  --linked-skills frontend-developer,agency-frontend-developer \
  --body "This repo uses pnpm. Check package manager commands before running installs or tests." \
  --priority 8
```

Compile resident summaries:

```bash
codex-memory compile --project-id demo
```

Build the startup bootstrap pack:

```bash
codex-memory build-startup --project-id demo
```

Render the exact startup text that will be injected:

```bash
codex-memory render-startup --project-id demo
```

Build a prompt pack for a task:

```bash
codex-memory build-pack --project-id demo --task "Fix failing pnpm build and test flow" --skills frontend-developer
```

For UI work driven by a repo-root design contract, pass the matching skill so
linked activation packs can reinforce the style workflow:

```bash
codex-memory build-pack --project-id demo --task "Create a new marketing page from DESIGN.md" --skills design-md,frontend-developer
```

For external-doc and package work, pass the retrieval skill so memory can
reinforce the local-first then Nia-first lookup order:

```bash
codex-memory add-pack \
  --scope project \
  --project-id demo \
  --name nia-retrieval-order \
  --triggers docs,api,sdk,library,package,repo \
  --linked-skills nia-context-router \
  --priority 9 \
  --body "Use the retrieval ladder: local grep first, indexed Nia second, index known sources third, web discovery last. Traverse tree -> grep -> read and keep excerpts minimal."

codex-memory build-pack --project-id demo --task "Check the latest SDK docs for streaming tool calls" --skills nia-context-router
```

Append a journal note, then promote durable learnings:

```bash
codex-memory append-journal --project-id demo --text "- Fixed pnpm install issue by checking package-manager commands first."
codex-memory promote-journal --project-id demo
```

Launch Codex with the compact startup bootstrap:

```bash
/home/dr_sharad/codex-memory/bin/codexw
```

Install the tracked Codex harness config onto a machine:

```bash
/home/dr_sharad/codex-memory/bin/install-codex-config
```

That installer symlinks only Codex preload anchors from `~/.claude/skills` into
`~/.codex/skills` so future sessions keep a compact skills context. The default
preload set is `lessons skill-router create-skill`; broader discovery should go
through `skill-router` and `skill-tree`, then open only the specific skill files
needed for the current task. It also links `codexw` and `claudew` into
`~/.local/bin`.

Override the defaults with `CLAUDE_SKILLS_SOURCE`, `CODEX_SKILLS_TARGET`,
`AGENTS_SKILLS_TARGET`, `LOCAL_BIN_DIR`, `CODEX_CONFIG_TARGET`,
`CODEX_PRELOAD_SKILLS`, `SUPERPOWERS_REPO_URL`, `SUPERPOWERS_ROOT`,
`SUPERPOWERS_SKILL_LINK`, or set `INSTALL_SUPERPOWERS=1` if you explicitly want
to install Superpowers into Codex native skill discovery.

It also syncs a native Codex memory extension into:

```text
~/.codex/memories_extensions/codex-memory
```

Or with an initial request:

```bash
/home/dr_sharad/codex-memory/bin/codexw --prompt "Fix the failing pnpm build"
```

Launch Claude Code with the same compact bootstrap while preserving Claude's
default skills, agents, slash commands, and autonomous skill routing:

```bash
/home/dr_sharad/codex-memory/bin/claudew
```

Or with an initial request:

```bash
/home/dr_sharad/codex-memory/bin/claudew --prompt "Fix the failing pnpm build"
```

## How It Works

`codex-memory` has four moving parts:

1. `MemoryStore` persists facts, packs, journals, and core identity files on disk.
2. `compile` ranks durable facts and emits compact global and project summaries.
3. `build-startup` and `render-startup` assemble the resident bootstrap loaded at session start.
4. `build-pack` scores activation packs against the current task and selected skills, then returns only the packs worth injecting.

On Codex `0.120.0+`, a fifth integration surface is available:

5. `sync-native-extension` exports curated snapshots into `~/.codex/memories_extensions/codex-memory`.

The normal lifecycle looks like this:

1. Initialize the store once.
2. Curate durable facts and small activation packs over time.
3. Compile summaries after updates.
4. Launch the host agent with a compact startup bootstrap.
5. Use `build-pack` during tasks when you want targeted retrieval.
6. Append journal notes after important sessions.
7. Promote journal lines into durable facts and packs when patterns prove reusable.

## Memory Layout

Default root:

```text
~/.codex-memory/
```

Typical layout:

```text
~/.codex-memory/
├── core/
│   ├── soul.md
│   ├── identity.md
│   ├── persona-contract.md
│   ├── policy.md
│   └── wake.md
├── global/
│   ├── facts.jsonl
│   ├── memory.md
│   ├── memory-summary.md
│   └── activation-packs/
├── projects/
│   └── <project-id>/
│       ├── facts.jsonl
│       ├── memory.md
│       ├── memory-summary.md
│       ├── wake.md
│       ├── decisions.md
│       ├── commands.md
│       ├── journal/
│       └── activation-packs/
├── runtime/
└── sessions/
```

The important distinction is:

- summaries are curated, ranked, and resident
- activation packs are selective and task-triggered
- journals are raw recall and stay out of prompt context by default

## Command Reference

Initialize a store and optionally a project:

```bash
codex-memory init
codex-memory init --project-id demo
```

Add a durable fact:

```bash
codex-memory add-fact \
  --scope project \
  --project-id demo \
  --kind convention \
  --text "Use pnpm instead of npm in this repo." \
  --tags build,tooling
```

Supported fact kinds:

- `preference`
- `correction`
- `environment`
- `convention`
- `workflow_hint`
- `error_fix`

Add an activation pack:

```bash
codex-memory add-pack \
  --scope project \
  --project-id demo \
  --name pnpm-build-fixes \
  --triggers pnpm,build,test \
  --linked-skills frontend-developer \
  --priority 8 \
  --max-tokens 220 \
  --body "This repo uses pnpm. Verify package-manager commands before installs or tests."
```

Compile summaries:

```bash
codex-memory compile --project-id demo
```

Build the startup pack:

```bash
codex-memory build-startup --project-id demo
codex-memory render-startup --project-id demo
```

Build a task-specific retrieval pack:

```bash
codex-memory build-pack \
  --project-id demo \
  --task "Fix pnpm build and test failure" \
  --skills frontend-developer
```

Write journal notes and promote durable learnings:

```bash
codex-memory append-journal --project-id demo --text "- Fixed pnpm install issue by checking package-manager commands first."
codex-memory promote-journal --project-id demo
```

Launch the host agent:

```bash
codex-memory launch --backend codex --cwd "$PWD"
codex-memory launch --backend claude --cwd "$PWD"
```

Sync the native Codex memory extension manually:

```bash
codex-memory sync-native-extension
codex-memory sync-native-extension --cwd "$PWD"
```

## Claude and Codex Integration

Codex integration:

- injects the startup bootstrap into Codex developer instructions
- preserves the compact resident-memory model
- keeps task-specific retrieval separate from startup
- syncs a native `memories_extensions/codex-memory` export for Codex `0.120.0+`

Claude integration:

- appends the startup bootstrap with `--append-system-prompt`
- preserves Claude Code's default skills, agents, slash commands, and routing
- avoids replacing Claude's native system prompt unless you choose to do that yourself

Both wrappers keep the host CLI untouched:

- `bin/codexw`
- `bin/claudew`

## Design Rules

- Resident memory must stay small and stable.
- Journals and session logs never enter context by default.
- Activation packs behave like tiny skill files and load only when triggered.
- Activation packs can be linked to already-selected skills so memory augments routing instead of competing with it.
- Procedural workflows belong in skills, not long-term memory summaries.
- Persona should be enforced through a short contract, while coding rigor stays non-negotiable.
- Startup bootstrap is terminal-native: wake when the session opens, not like a messaging bot.
- Claude integration appends the compact bootstrap to Claude's existing system prompt so built-in skill routing and autonomous skill use stay intact.
- The wrappers use separate entrypoints so your existing `codex` and `claude` commands stay untouched.
- Native Codex extension export is curated and compact on purpose; it should teach the consolidator durable memory, not dump transcripts.

## Development

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The current token budgets are intentionally small:

- resident prompt budget: `900`
- activation pack budget: `500`
- total prompt budget: `1400`
- startup budget: `1100`

These limits live in `src/codex_memory/config.py` and are part of the design,
not an accident.

## Additional Docs

- [Architecture](docs/architecture.md)
- [CLI Reference](docs/cli-reference.md)
- [Integration Notes](docs/integration.md)
