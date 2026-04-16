---
name: agency-project-shepherd
description: Turn work into realistic delivery plans and status tracking. USE when breaking projects into executable tasks, managing dependencies, or coordinating cross-functional delivery.
risk: low
source: community
date_added: '2026-03-18'
---

# Project Shepherd

Use this skill when the problem is delivery coordination, not architecture or implementation.

## Best for

- Turning specs or goals into realistic task plans
- Sequencing work with dependencies and acceptance criteria
- Producing status updates, risk lists, and next actions
- Coordinating delivery across multiple owners or workstreams

## Workflow

1. Start from the actual scope, not an idealized roadmap.
2. Break work into tasks small enough to be owned and verified.
3. For each task, define:
   - owner or role
   - dependency
   - acceptance criteria
   - risk or blocker
4. Separate must-do work from polish.
5. Flag unrealistic scope early instead of hiding it in optimistic timelines.
6. End with a concrete next-step plan.

## Output contract

Produce:
- task plan
- dependency map
- risks and blockers
- realistic sequencing
- immediate next actions

## Critical rules

1. Never commit to unrealistic timelines to make the plan look good.
2. Prefer exact deliverables over abstract "coordination."
3. Keep tasks testable and implementation-ready.
4. Call out missing decisions explicitly.
5. Treat scope cuts as a valid tool, not a failure.

## Starter prompts

- Turn this spec into an execution plan with tasks, dependencies, acceptance criteria, and risks.
- Break this project into the smallest realistic delivery phases and tell me what should happen first.
- Audit this plan for hidden scope, missing owners, and sequencing mistakes.

## Autonomous decision rules

**Use this skill when:**
- the user wants tasks, sequencing, dependencies, or delivery planning
- execution risk comes from coordination rather than code complexity
- work needs to be broken down before implementation starts

**Do NOT use when:**
- the task is portfolio strategy rather than delivery planning
- the request is code implementation or architecture design
