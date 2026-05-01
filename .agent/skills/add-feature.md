# Skill: Add Feature

## Goal
Implement a new feature with minimal footprint while adhering strictly to existing project architecture.

## Phase 1: Discovery
Inspect the relevant project domains and identify:
- Where the feature naturally fits.
- What existing components or utilities can be reused.
- Potential risks to existing flows.

Do not write code in this phase.

## Phase 2: Implementation Plan
Create `.agent/current/plan.md`.
Define the exact sequence of files to be created or modified. 
Do not write code until the plan exists and makes logical sense.

## Phase 3: Context Loading
Before implementation, read:
- `.agent/docs/project-architecture.md`
- `.agent/docs/coding-style.md`
- the closest matching model airplane in `.agent/model-airplanes/`

## Phase 4: Implementation
Implement the approved plan exactly.
Do not invent APIs. 
Do not guess at types; verify them.
Do not refactor unrelated code.

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
