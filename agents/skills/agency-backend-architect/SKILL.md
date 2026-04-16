---
name: agency-backend-architect
description: Design backend services, APIs, and server-side boundaries. USE when defining service interfaces, API behavior, persistence patterns, or backend integration flows.
risk: low
source: community
date_added: '2026-03-18'
---

# Backend Architect

Use this skill when the core problem is server-side design, not whole-system architecture.

## Best for

- API and service design
- backend module and service boundaries
- request flows, async jobs, and integration patterns
- choosing backend persistence and communication patterns

## Workflow

1. Start from the backend responsibilities and request flows.
2. Define:
   - public interfaces
   - internal service boundaries
   - data ownership
   - sync vs async behavior
3. Specify failure modes and operational constraints.
4. Call out security, validation, and compatibility boundaries.
5. Leave DB tuning and infra mechanics to narrower specialist skills.

## Output contract

Produce:
- service/API design
- responsibility boundaries
- data flow and failure handling
- integration patterns
- implementation constraints

## Critical rules

1. Start from behavior and ownership, not frameworks.
2. Keep contracts explicit: inputs, outputs, errors, versioning.
3. Separate backend design from infrastructure automation.
4. Separate persistence choices from low-level database tuning.
5. Do not leak stack traces or internal-only behavior to clients.

## Starter prompts

- Design the backend service boundaries and API contracts for this feature.
- Map this request flow through the backend and propose a cleaner service split.
- Recommend a backend integration pattern for these sync and async requirements.

## Autonomous decision rules

**Use this skill when:**
- the task is about APIs, services, request flow, or backend integration boundaries
- the user needs backend structure and contracts

**Do NOT use when:**
- the task is top-level system architecture better handled by `agency-software-architect`
- the task is DB performance or infra automation better handled by narrower skills
