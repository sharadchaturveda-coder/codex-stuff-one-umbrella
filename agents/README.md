# agency-agents-codex

**171 AI agent skills for Codex CLI and Claude Code — installed globally, project-agnostic.**

A complete AI agency at your fingertips: 149 specialist agents from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) + 21 design skills from [Impeccable](https://impeccable.style) + 1 live-spec enforcement agent, adapted and wired for auto-invocation in Codex CLI and Claude Code.

---

## What's inside

| | Count | Source |
|---|---|---|
| Agency specialist agents | 149 | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) |
| Impeccable design skills | 21 | [impeccable.style](https://impeccable.style) |
| Live-spec enforcement agent | 1 | Local extension |
| **Total** | **171** | |

### Agency agents cover
Engineering · Design · Marketing · Sales · Product · Project Management · Testing · Support · Spatial Computing · Game Dev · Academic · Specialized (MCP builder, blockchain auditor, compliance, and more)

### Impeccable design commands
`/polish` `/audit` `/typeset` `/arrange` `/colorize` `/animate` `/overdrive` `/distill` `/critique` `/harden` `/optimize` `/clarify` `/bolder` `/quieter` `/delight` `/normalize` `/adapt` `/extract` `/onboard` `/frontend-design` `/teach-impeccable`

---

## Install

```bash
git clone https://github.com/sharadchaturveda-coder/agency-agents-codex
cd agency-agents-codex
bash scripts/install.sh
```

Restart Codex CLI and Claude Code after installing.

### Live-spec enforcement

This repo now includes `agency-live-spec-enforcer`, an auto-invoked implementation-discipline agent for Codex CLI and a Claude Code subagent. Its job is to force non-trivial work back through a single live spec file during the moment plans turn into code.

What it enforces:
- one canonical live spec file
- live implementation checklists and sub-checklists
- spec reconciliation when implementation diverges from plan
- no stale planning-doc bundles by default

### What the install script does

| Tool | Location | Skills |
|---|---|---|
| **Codex CLI** | `~/.codex/skills/` | All 170 (auto-invoked) |
| **Claude Code** | `~/.claude/agents/` | 149 agency agents |

---

## How it works

### Codex CLI — auto-invocation
Each agency skill has an `agents/openai.yaml` with:
```yaml
policy:
  allow_implicit_invocation: true
```
Codex reads the `description` field and automatically injects the right specialist into context. No explicit invocation needed — just work naturally and the relevant agent activates.

You can also invoke explicitly: `$agency-security-engineer`, `$agency-frontend-developer`, etc.

### Claude Code — subagents
Agents live in `~/.claude/agents/` and are available globally across all projects. Claude Code reads the `description` and spawns them as subagents mid-conversation, or you can ask explicitly:
> *"Use the backend-architect agent to design this API"*
> *"Use the agents-orchestrator to run the full dev pipeline"*

---

## Adding new agency skills

If you pull updates from the upstream [agency-agents](https://github.com/msitarzewski/agency-agents) repo:

```bash
# Re-run the yaml generator to add openai.yaml to any new skills
python3 scripts/gen_openai_yaml.py

# Re-run install
bash scripts/install.sh
```

---

## Credits

- Agent personalities: [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (MIT)
- Design skills: [pbakaus/impeccable](https://github.com/pbakaus/impeccable) via [impeccable.style](https://impeccable.style)
- Codex CLI auto-invocation wiring & install system: [@sharadchaturveda-coder](https://github.com/sharadchaturveda-coder)
