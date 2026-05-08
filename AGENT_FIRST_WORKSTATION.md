# Agent-First Workstation

## Operating Reality

This harness is meant to run inside an agent-first workstation.

The user does not personally operate:

- bash
- terminals
- filesystem navigation
- browser GUIs
- admin dashboards

The user talks to agents through terminal-based CLI chat surfaces. Agents are the hands that interact with the machine.

## Core Rules

- Prefer terminal-native control surfaces: CLI commands, scripts, and APIs.
- Prefer CLIs over MCPs whenever both can do the job.
- Treat browser and GUI interaction as reluctant fallback paths only.
- Never use GUI browsers, Chrome, Firefox, or browser windows for testing. Use terminal commands, direct APIs, logs, test runners, and browser CLI tools instead.
- Prefer host-native repo access and host-native tools.
- Do not recommend Docker by default. This workstation is intentionally host-native because container boundaries usually reduce agent throughput.
- Optimize for agent clarity, stable paths, shared tooling, and low-friction execution.
- Respect the user's harness stack as part of the workstation operating system, not as optional decoration.

## Harness Homes

The primary harness homes on the user's machine are:

- Claude: `/home/sea-serpent/.claude`
- Codex: `/home/sea-serpent/codex-stuff-one-umbrella`
- Gemini: `/home/sea-serpent/dev-projects/gemini-ultimate-harness`

## Mental Model

This is not a normal developer laptop workflow.

It is effectively a terminal-based chat operating system where:

1. the user provides intent
2. agents execute
3. terminal-native tools are the control plane
4. the host machine is the shared execution surface

If a task can be done without opening a GUI, that is the preferred path.
