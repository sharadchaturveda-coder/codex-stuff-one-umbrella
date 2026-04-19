---
name: rtk-safe-usage
description: Optional RTK policy for high-noise command output only. USE when test, build, lint, or large log output is noisy enough to justify explicit compression. NEVER use for discovery, source inspection, routing, memory, or persona surfaces.
---

# RTK Safe Usage

RTK is optional and quarantined. It is not allowed to auto-rewrite shell commands or modify harness state.

## Use only when

- Running high-noise test commands
- Running high-noise build commands
- Running high-noise lint/typecheck commands
- Reading large repetitive logs
- The task benefits from output compression and does not depend on raw discovery output

## Never use when

- Searching code or files
- Reading source directly
- Inspecting diffs or commit contents
- Choosing a skill or validating routing
- Inspecting memory, prompts, or persona/config surfaces
- A debugging step depends on unfiltered truth

## Allowed entrypoint

```bash
/home/dr_sharad/codex-stuff-one-umbrella/memory/bin/rtk-safe <command> [args...]
```

Use the wrapper, not RTK directly.

## Allowed command classes

- `pytest`
- `vitest`
- `playwright test`
- `cargo test|build|clippy`
- `go test|build|vet`
- `npm|pnpm|yarn test|build`
- `next build`
- `ruff check`
- `eslint`
- `tsc`
- `golangci-lint run`
- `log <file>`

## Hard rules

- Never run `rtk init`
- Never install hooks or awareness docs
- Never mutate persona or startup files
- Never rewrite discovery/source-inspection commands
- If uncertain, do not use RTK
