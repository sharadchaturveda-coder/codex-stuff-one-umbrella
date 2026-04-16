---
name: agency-devops-automator
description: Automate infrastructure, CI/CD, and deployment workflows. USE when building pipelines, environment automation, infrastructure as code, or deployment procedures.
risk: low
source: community
date_added: '2026-03-18'
---

# DevOps Automator

Use this skill when the job is to automate build, deploy, and infrastructure workflows.

## Best for

- CI/CD pipeline design
- infrastructure as code
- environment provisioning and deployment automation
- rollout, rollback, and operational automation

## Workflow

1. Start from the delivery path: build, test, deploy, rollback.
2. Identify manual steps and remove them.
3. Define environment differences explicitly.
4. Add safety rails:
   - validation gates
   - rollout checks
   - rollback path
   - secret handling
5. Leave SLO policy and reliability budgeting to SRE.

## Output contract

Produce:
- pipeline or infra automation plan
- environment model
- deployment/rollback flow
- security and secret notes
- operational risks

## Critical rules

1. Prefer reproducible automation over runbook-only process.
2. Never depend on hidden manual production steps.
3. Make rollback explicit.
4. Keep secrets out of source.
5. Separate automation design from reliability policy.

## Starter prompts

- Design the CI/CD and deployment flow for this service with rollback and validation gates.
- Turn this manual infrastructure process into code and automation.
- Audit our deployment path for manual steps, missing rollback, and secret handling gaps.

## Autonomous decision rules

**Use this skill when:**
- the task is about CI/CD, infra automation, deploys, or environment setup
- the goal is reducing manual ops through automation

**Do NOT use when:**
- the task is architectural boundary design better handled by `agency-software-architect`
- the task is SLOs, incident posture, or observability strategy better handled by `agency-sre-site-reliability-engineer`
