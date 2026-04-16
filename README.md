# codex-stuff-one-umbrella

One repo for the full Codex harness.

## Structure

```
memory/     — codex-memory-claw-like: Python memory system (facts, packs, journal, CLI)
agents/     — agency-agents-codex: 177 agent skills for Codex CLI + Claude Code
config/     — config.toml: Codex config with Vex persona + developer instructions
```

## memory/

Low-token sidecar memory system. Stores structured facts, activation packs, and journals.
See `memory/README.md` for full docs.

## agents/

177 AI agent skills — 156 agency specialists + 21 Impeccable design skills.
See `agents/README.md` for full docs.

## config/

`config.toml` — Codex config. Copy to `~/.codex/config.toml` on a new machine.
