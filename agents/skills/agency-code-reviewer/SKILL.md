---
name: agency-code-reviewer
description: Workflow-first code review for bugs, regressions, risky behavior changes, and missing tests. USE when reviewing diffs, PRs, or proposed implementations.
risk: low
source: community
date_added: '2026-03-18'
---

# Code Reviewer

Use this skill when the main job is review, not implementation.

## Best for

- Reviewing diffs and pull requests before merge
- Looking for regressions, missing tests, and risky behavior changes
- Auditing a proposed implementation before code lands
- Producing findings ordered by severity rather than style commentary

## Review workflow

1. Understand scope first:
   - what changed
   - intended behavior
   - relevant risks
2. Review in this order:
   - correctness/regressions
   - security/privacy
   - data loss or state corruption
   - performance and reliability
   - missing tests and observability
3. Prefer concrete findings with file and line references.
4. Separate findings from assumptions and open questions.
5. If no findings are discovered, say so explicitly and note residual risks or testing gaps.

## Output contract

Produce:
- findings first, ordered by severity
- file/line references
- a short assumptions/open-questions section if needed
- only then a brief summary

Do not lead with praise, overviews, or style notes.

## Critical rules

1. Be specific and evidence-based.
2. Focus on bugs and risks, not style preferences.
3. Call out missing tests when behavior changed.
4. Prefer “this will break when…” over vague concerns.
5. Do not invent certainty where intent is unclear; note assumptions.

## Starter prompts

- Review this diff for security regressions, missing tests, and risky behavior changes.
- Audit this implementation before merge. Findings first, with severity and file references.
- Review this PR like a production gate, focusing on regressions and correctness.

## Autonomous decision rules

**Use this skill when:**
- the user asks for a review
- the task is a PR or diff audit
- the safest contribution is critique rather than code changes

**Do NOT use when:**
- the user wants implementation, not review
- there is no code or artifact to review
