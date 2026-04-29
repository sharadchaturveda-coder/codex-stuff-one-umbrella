# Integration Notes

## Goal

The integration layer exists to inject compact resident memory into a host agent
without breaking the host's native strengths.

That means:

- keep startup context small
- preserve native tools and workflows
- keep skill routing intact
- keep task-specific retrieval separate from bootstrapping

## Codex Integration

Codex is launched through:

```text
bin/codexw
```

Under the hood, the launcher:

1. derives or accepts a project id
2. compiles summaries
3. builds a startup pack
4. renders the startup text
5. syncs a native `~/.codex/memories_extensions/codex-memory` export
6. injects the startup text into Codex developer instructions

This gives Codex a compact baseline identity, policy, wake state, and summary
pack at session start.

For machine setup, `bin/install-codex-config` should expose only the compact
Codex preload anchors in `~/.codex/skills`: `lessons`, `skill-router`, and
`create-skill` by default. The full shared skill library should stay on disk and
be reached through `skill-router`/`skill-tree` only when the current task
requires it. It should also install the `codexw` and `claudew` launchers into
`~/.local/bin` so both harnesses are callable immediately on a fresh machine.

Do not install large external skill libraries into Codex native discovery by
default. Superpowers can still be installed explicitly with
`INSTALL_SUPERPOWERS=1`, but the default harness path keeps baseline context
small and routes specialty skills on demand.

On Codex `0.120.0+`, the native extension export gives the built-in
consolidation agent a curated memory source to read during summarization. The
export is intentionally compact:

- `instructions.md` explains how to interpret the source
- `export/snapshot.md` is the canonical merged durable-memory snapshot
- `export/projects/<project-id>.md` carries project-specific wake and summary

The export should teach Codex durable preferences and conventions. It should not
become a transcript graveyard.

## Claude Code Integration

Claude is launched through:

```text
bin/claudew
```

Under the hood, the launcher:

1. derives or accepts a project id
2. compiles summaries
3. builds a startup pack
4. renders the startup text
5. appends the startup text to Claude's existing system prompt

The Claude path intentionally uses append behavior instead of full replacement.

Why:

- Claude already has useful native system behavior
- Claude already has skills, agents, and slash commands
- replacing the full system prompt risks damaging those capabilities

## Persona Strategy

The project separates persona from capability.

Capability stays in:

- host agent tool behavior
- repo and safety instructions
- coding and review rules
- retrieval and token budgets

Persona stays in:

- `soul.md`
- `identity.md`
- `persona-contract.md`

The contract is supposed to shape voice and posture without lowering technical
quality.

## Why Startup Stays Small

The main failure mode in memory systems is context inflation.

This project explicitly avoids:

- loading full journals at startup
- injecting all project notes by default
- replacing skills with memory blobs
- turning the startup prompt into a miniature wiki

Instead it prefers:

- compiled summaries for durable facts
- activation packs for sharp, targeted recall
- journals as cold storage until promoted

## Skill Routing and Activation Packs

Activation packs are not meant to replace skills.

The intended order is:

1. the host agent routes to relevant skills or specialist behavior
2. `codex-memory` boosts activation packs linked to those selected skills
3. the resulting pack augments the skill choice with repo or user-specific memory

That keeps memory supportive instead of competitive.

Example:

- the host selects `design-md` for a task like "build this page from DESIGN.md"
- `codex-memory` can then prioritize packs linked to `design-md`
- those packs can carry project-specific visual constraints without replacing the
  shared skill itself

Another example:

- the host selects `nia-context-router` for a task like "check the SDK docs"
- `codex-memory` can prioritize packs linked to `nia-context-router`
- those packs can reinforce the retrieval ladder: local grep, then indexed Nia,
  then indexing known sources, with web discovery only when needed

## Recommended Usage Patterns

### Good

- keep facts short and durable
- use activation packs for recurring debug and implementation patterns
- promote journal learnings only when they seem reusable
- keep persona compact and operational
- let the host agent keep its own tools and routing

### Bad

- storing entire transcripts as memory
- turning startup into a giant context dump
- using activation packs as long-form docs
- treating persona as roleplay instead of response discipline
- overriding host system prompts without a strong reason

## When to Extend the System

Add new memory categories only if they stay compact and operational.

Good extensions:

- better promotion heuristics
- richer skill-linked pack selection
- host-specific launch adapters
- optional tooling around review loops or command capture

Bad extensions:

- vector search bolted on without a clear retrieval need
- giant semantic memory graphs for tiny repos
- bloated startup scaffolding
