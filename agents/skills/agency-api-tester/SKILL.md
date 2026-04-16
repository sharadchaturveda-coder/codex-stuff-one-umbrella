---
name: agency-api-tester
description: Test API behavior, contracts, security edges, and performance. USE when validating endpoints, integrations, error handling, or release readiness for APIs.
risk: low
source: community
date_added: '2026-03-18'
---

# API Tester

Use this skill when the primary artifact under test is an API or integration boundary.

## Best for

- Endpoint validation and contract checking
- Auth, error handling, and edge-case testing
- Third-party integration verification
- Basic performance and load checks for APIs

## Workflow

1. Inventory the endpoints or integration paths under test.
2. Test in this order:
   - happy path
   - auth and permission boundaries
   - input validation and error responses
   - contract compatibility
   - latency or load-sensitive paths
3. Record actual requests, responses, and failure modes.
4. Separate API correctness from general code review concerns.

## Output contract

Produce:
- tested endpoints or flows
- failures and risks
- contract or compatibility concerns
- security/performance notes
- release readiness recommendation for the API surface

## Critical rules

1. Test real error cases, not only success paths.
2. Keep request/response expectations explicit.
3. Call out compatibility breaks separately from implementation bugs.
4. Do not confuse endpoint health with product readiness.
5. Keep security checks concrete: auth, authz, rate limits, validation.

## Starter prompts

- Test this API surface for auth failures, validation gaps, and risky behavior changes.
- Audit these endpoints for contract compatibility and release readiness.
- Validate this third-party integration with realistic failure cases.

## Autonomous decision rules

**Use this skill when:**
- the task is specifically about APIs, integrations, contracts, or endpoint testing
- the artifact under test is a service boundary rather than UI or general code

**Do NOT use when:**
- the task is a generic diff review better handled by `agency-code-reviewer`
- the task is evidence-heavy UI verification better handled by `agency-evidence-collector`
