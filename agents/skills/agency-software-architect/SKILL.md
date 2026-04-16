---
name: agency-software-architect
description: Choose system boundaries, architectural patterns, and tradeoffs. USE when deciding overall software shape, domain boundaries, or major technical direction.
risk: low
source: community
date_added: '2026-03-18'
---

# Software Architect

Use this skill for top-level system design decisions.

## Best for

- Choosing overall architecture shape
- Defining domain boundaries and ownership
- Comparing major technical options with tradeoffs
- Writing architecture decisions that can guide implementation

## Workflow

1. Start from business goals, system constraints, and team reality.
2. Identify the key architectural tensions:
   - scale
   - coupling
   - consistency
   - delivery speed
   - team ownership
3. Compare at least two realistic options.
4. Name what each option makes easier and harder.
5. Recommend the simplest option that fits the constraints.

## Output contract

Produce:
- architecture options
- explicit tradeoffs
- boundary recommendations
- decision rationale
- follow-on areas that need specialist design

## Critical rules

1. No architecture astronautics.
2. Prefer reversibility where possible.
3. Domain and team constraints come before tool preference.
4. Name the downside of the recommended option.
5. Hand off specialist concerns to narrower skills when needed.

## Starter prompts

- Compare architecture options for this system and recommend the simplest one that fits our constraints.
- Define the service or module boundaries for this product and explain the tradeoffs.
- Turn this problem into an ADR with options, decision, and consequences.

## Autonomous decision rules

**Use this skill when:**
- the task is about system shape, boundaries, or major technical direction
- the user needs architectural tradeoffs, not implementation detail

**Do NOT use when:**
- the task is specifically backend API/service design better handled by `agency-backend-architect`
- the task is DB tuning, CI/CD, or reliability operations better handled by narrower skills
