# Architecture

## Overview

`codex-memory` is a filesystem-backed memory sidecar for coding agents. It is
designed to keep always-on context small while still supporting durable
cross-session recall.

The architecture has three layers:

1. Storage: facts, activation packs, journals, and core identity files on disk.
2. Compilation: ranking durable facts into compact summaries.
3. Retrieval and launch: assembling startup packs and task-triggered packs for a
   host agent such as Codex or Claude Code.

## Core Modules

### `src/codex_memory/store.py`

Responsible for:

- initializing the directory structure
- seeding default core files
- reading and writing facts
- reading and writing activation packs
- appending journals
- loading summaries and project text

`MemoryStore` is intentionally simple. There is no database, daemon, or vector
store. The project prefers inspectable files and predictable behavior.

### `src/codex_memory/compiler.py`

Responsible for:

- ranking facts by kind, tag count, and reuse count
- compiling the global summary
- compiling a project summary
- enforcing summary token budgets

Compilation is conservative. If a fact does not fit, it is skipped rather than
causing bloat.

### `src/codex_memory/retrieval.py`

Responsible for:

- building resident prompt packs
- building startup prompt packs
- scoring activation packs by task text and linked skills
- clamping output to resident, activation, and total token budgets

This module is the heart of the low-bloat retrieval strategy.

### `src/codex_memory/promotion.py`

Responsible for:

- scanning journal lines for promotable patterns
- converting recurring or useful lines into durable facts
- generating lightweight activation packs from debug-style journal entries
- recompiling summaries after promotion

Promotion is heuristic, not magical. It looks for practical patterns such as:

- conventions like `use pnpm instead of npm`
- fixes and workarounds
- preferences or explicit avoidance rules

### `src/codex_memory/cli.py`

Responsible for:

- exposing the store through CLI commands
- rendering startup text
- building provider-specific launch commands
- adapting startup injection for Codex and Claude Code

## Memory Types

### Core Files

Core files define the agent's persistent baseline:

- `soul.md`
- `identity.md`
- `persona-contract.md`
- `policy.md`
- `wake.md`

These are loaded into the startup pack. The persona contract exists to keep
style intentional without allowing it to weaken technical execution.

### Facts

Facts are durable, concise statements. They are best for:

- user preferences
- project conventions
- environment facts
- workflow hints
- corrections
- reusable fixes

Facts are compiled into summaries and are the default long-term memory surface.

### Activation Packs

Activation packs are small, targeted, task-triggered memory units. They are best
for:

- sharp implementation reminders
- debug patterns
- repo-specific warnings
- conventions linked to specific skills

They behave more like tiny memory-driven skill fragments than general notes.

### Journals

Journals are raw episodic recall. They are useful because they preserve session
history without forcing that history into every future prompt.

Journal entries:

- stay out of context by default
- can be promoted into facts or packs when a pattern proves durable

## Token Budget Strategy

The budgets in `src/codex_memory/config.py` are part of the system design.

Current defaults:

- resident budget: `900`
- activation budget: `500`
- total budget: `1400`
- global summary budget: `250`
- project summary budget: `350`
- startup budget: `1100`

The system enforces these budgets with simple token estimates based on word
count. The estimates are intentionally rough but predictable.

## Retrieval Flow

### Startup

At startup, the system loads:

- soul
- identity
- persona contract
- wake
- policy
- global summary
- project wake and project summary when a project is active

This creates a compact resident bootstrap for the session.

### Task Retrieval

When building a task-specific pack, the system:

1. loads resident identity and summary parts
2. scores activation packs against task text and optional error text
3. boosts packs linked to already-selected skills
4. clamps the result to the activation and total budgets

This keeps retrieval relevant and cheap.

## Provider Integration Model

The storage and retrieval layers are provider-agnostic. Only the launch adapter
is provider-specific.

### Codex

Codex integration injects startup text into developer instructions.

### Claude Code

Claude integration appends startup text to the existing system prompt so
Claude's native skills, agents, and routing remain available.

## Why Files Instead of a Database

This project favors:

- low setup friction
- inspectable state
- easy backups
- local-first operation
- deterministic behavior

That tradeoff is worth it for the intended use case: compact operator memory for
coding agents, not enterprise-scale semantic retrieval.
