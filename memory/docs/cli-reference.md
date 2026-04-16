# CLI Reference

## Overview

The project exposes a single CLI entrypoint:

```bash
codex-memory <command> [options]
```

If you are working from the repo without installing the package:

```bash
PYTHONPATH=src python3 -m codex_memory.cli <command> [options]
```

## Global Option

### `--root`

Override the memory root directory. If omitted, the default is:

```text
~/.codex-memory
```

## Commands

### `init`

Initialize the store structure and optionally a project.

Examples:

```bash
codex-memory init
codex-memory init --project-id demo
```

### `add-fact`

Add a durable fact to global or project scope.

Required options:

- `--scope global|project`
- `--kind preference|correction|environment|convention|workflow_hint|error_fix`
- `--text`

Optional options:

- `--project-id`
- `--cwd`
- `--tags`

Examples:

```bash
codex-memory add-fact \
  --scope global \
  --kind preference \
  --text "User prefers concise answers with minimal fluff." \
  --tags style,communication
```

```bash
codex-memory add-fact \
  --scope project \
  --project-id demo \
  --kind convention \
  --text "Use pnpm instead of npm in this repo." \
  --tags build,tooling
```

### `add-pack`

Add an activation pack.

Required options:

- `--scope global|project`
- `--name`
- `--body`
- `--triggers`

Optional options:

- `--project-id`
- `--cwd`
- `--linked-skills`
- `--priority`
- `--max-tokens`
- `--tags`

Example:

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

Another example for source-grounded retrieval:

```bash
codex-memory add-pack \
  --scope project \
  --project-id demo \
  --name nia-retrieval-order \
  --triggers docs,api,sdk,library,package,repo \
  --linked-skills nia-context-router \
  --priority 9 \
  --max-tokens 180 \
  --body "Use the retrieval ladder: local grep first, indexed Nia second, index known sources third, web discovery last. Traverse tree -> grep -> read and keep excerpts minimal."
```

### `compile`

Compile durable summaries from curated facts.

Options:

- `--project-id`
- `--cwd`

Examples:

```bash
codex-memory compile --project-id demo
codex-memory compile --cwd .
```

### `build-pack`

Build a task-specific prompt pack with resident parts plus matching activation
packs.

Required options:

- `--task`

Optional options:

- `--project-id`
- `--cwd`
- `--error`
- `--skills`

Example:

```bash
codex-memory build-pack \
  --project-id demo \
  --task "Fix pnpm build and test failure" \
  --error "npm command not found in CI step" \
  --skills frontend-developer
```

For external docs or package lookup:

```bash
codex-memory build-pack \
  --project-id demo \
  --task "Check the SDK docs for streaming tool calls" \
  --skills nia-context-router
```

Output is JSON containing:

- `project_id`
- `selected_skills`
- `token_estimate`
- `resident_parts`
- `activation_parts`

### `build-startup`

Build the startup pack as JSON.

Options:

- `--project-id`
- `--cwd`

Example:

```bash
codex-memory build-startup --project-id demo
```

### `render-startup`

Render the exact startup bootstrap text that will be injected into the host
agent.

Options:

- `--project-id`
- `--cwd`
- `--output`

Examples:

```bash
codex-memory render-startup --project-id demo
codex-memory render-startup --project-id demo --output /tmp/startup.md
```

### `append-journal`

Append a note to a project's journal.

Required options:

- `--text`

Optional options:

- `--project-id`
- `--cwd`
- `--day`

Example:

```bash
codex-memory append-journal \
  --project-id demo \
  --text "- Fixed pnpm install issue by checking package-manager commands first."
```

### `promote-journal`

Scan journal entries and promote useful lines into facts and activation packs.

Options:

- `--project-id`
- `--cwd`
- `--day`

Example:

```bash
codex-memory promote-journal --project-id demo
```

### `launch`

Launch the host agent with a compact startup bootstrap.

Options:

- `--backend codex|claude`
- `--project-id`
- `--cwd`
- `--prompt`
- `--journal-note`
- `--promote-after-journal`
- `--codex-bin`
- `--claude-bin`
- `--no-alt-screen`
- `--no-native-extension-sync`

Any arguments after `--` are passed through to the selected backend.

Examples:

```bash
codex-memory launch --backend codex --cwd "$PWD"
codex-memory launch --backend codex --cwd "$PWD" -- --help
```

```bash
codex-memory launch --backend claude --cwd "$PWD"
codex-memory launch --backend claude --cwd "$PWD" --prompt "Fix the build"
codex-memory launch --backend claude --cwd "$PWD" -- --model sonnet --permission-mode auto
```

### `sync-native-extension`

Export the curated `codex-memory` store into Codex's native
`memories_extensions/` format.

Options:

- `--project-id`
- `--cwd`
- `--extension-root`
- `--extension-name`

Examples:

```bash
codex-memory sync-native-extension
codex-memory sync-native-extension --cwd "$PWD"
```

## Wrapper Scripts

The repo also includes convenience launchers:

- `bin/codexw`
- `bin/claudew`

These wrap the `launch` command and leave your normal `codex` and `claude`
commands untouched.
