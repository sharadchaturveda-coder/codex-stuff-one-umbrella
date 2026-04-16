---
name: agency-sprint-prioritizer
description: Prioritize sprint and backlog work with explicit tradeoffs. USE when choosing what fits next, sequencing backlog items, or balancing value, effort, and risk.
risk: low
source: community
date_added: '2026-03-18'
---

# Sprint Prioritizer

Use this skill when the problem is choosing what to do next within delivery constraints.

## Best for

- Sprint planning and backlog selection
- Ranking work by value, effort, risk, and dependency
- Cutting scope to fit a real delivery window
- Making prioritization tradeoffs explicit for stakeholders

## Workflow

1. Start with the real delivery window and team capacity.
2. Inventory candidate work with:
   - expected value
   - effort
   - dependencies
   - delivery risk
   - whether it is must-have or optional
3. Choose the lightest useful prioritization framework for the decision:
   - simple value vs effort
   - RICE
   - must-have vs nice-to-have
4. Build the proposed sprint or backlog slice.
5. Call out what was excluded and why.

## Output contract

Produce:
- ranked backlog or sprint slice
- rationale for ordering
- assumptions about capacity
- scope cuts and deferrals
- major risks or blockers

## Critical rules

1. Do not prioritize without a stated capacity assumption.
2. Prefer explicit tradeoffs over vague “high priority” labels.
3. Separate must-have work from polish.
4. Include dependencies that can invalidate the order.
5. Say what should be deferred, not only what should be done.

## Starter prompts

- Prioritize this backlog for the next sprint using explicit value, effort, and dependency tradeoffs.
- Given this capacity, tell me what actually fits and what should be cut.
- Turn this feature list into a ranked plan with clear deferrals and risk notes.

## Autonomous decision rules

**Use this skill when:**
- the user asks what should happen next in a sprint or backlog
- the problem is ordering or cutting work, not defining the whole project plan

**Do NOT use when:**
- the task is broad cross-functional delivery planning better handled by `agency-project-shepherd`
- the task is long-horizon portfolio strategy better handled by `agency-studio-producer`
