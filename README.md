# codex-stuff-one-umbrella

One repo for the full Codex harness.

The user's workstation operating model for this harness lives in [AGENT_FIRST_WORKSTATION.md](AGENT_FIRST_WORKSTATION.md).

## Structure

```
memory/     — codex-memory-claw-like: Python memory system (facts, packs, journal, CLI)
agents/     — agency-agents-codex: 177 agent skills for Codex CLI + Claude Code
config/     — config.toml: Codex config with Vex persona + developer instructions
```

## memory/

Low-token sidecar memory system. Stores structured facts, activation packs, and journals.
See `memory/README.md` for full docs.
Workstation-memory notes for fresh installs live in `memory/docs/workstation-memory.md`.

## agents/

177 AI agent skills — 156 agency specialists + 21 Impeccable design skills.
See `agents/README.md` for full docs.

## config/

`config.toml` — Codex config. Copy to `~/.codex/config.toml` on a new machine.
