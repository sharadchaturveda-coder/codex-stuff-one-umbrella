# Skill: Add Analytics Events

## Goal
Add meaningful product analytics events without changing core business behavior.

## Phase 1: Discovery
Inspect the project and identify files related to:
- login
- signup
- checkout
- subscription
- onboarding
- settings
- cancellation
- errors
- high-value user actions

Do not write code in this phase.

## Phase 2: Event Plan
Create `.agent/current/event-plan.md`.

For each proposed event, include:
- event name
- file location
- trigger condition
- properties to capture
- reason this event matters

Do not write code until the event plan exists.

## Phase 3: Context Loading
Before implementation, read:
- `.agent/docs/project-architecture.md`
- `.agent/docs/coding-style.md`
- `.agent/docs/env-policy.md`
- the closest matching model airplane in `.agent/model-airplanes/`

## Phase 4: Implementation
Implement only the approved events.
Prefer minimal changes.
Do not invent APIs.
Do not read secrets.
Do not modify unrelated files.

## Phase 5: Validation
Run:
- typecheck
- lint
- relevant tests
- git diff review

## Phase 6: Stop-Hook Feedback
Write `.agent/current/agent-feedback.md` answering:
- What instruction was unclear?
- What context was missing?
- What tool was missing?
- Did any instruction conflict?
- What should be added to `.agent/` for next time?
