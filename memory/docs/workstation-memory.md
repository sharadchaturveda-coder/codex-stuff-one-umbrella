# Workstation Memory

This repo is the schema/tooling home for Codex-side memory, not the live memory store itself.

The live workstation memory on the user's machine currently lives under:

- `~/.codex-memory/workstation`

That memory class should hold durable facts about:

- the user's true interface: natural-language chat
- agents as the active machine operators
- CLI as the preferred control plane for agents
- GUI as the presentation layer for clients and customers
- host-native workstation assumptions
- Docker hostility by default on this machine

This memory should remain low-token and retrieval-first.

It should not become a dump of raw transcripts or project journals.
