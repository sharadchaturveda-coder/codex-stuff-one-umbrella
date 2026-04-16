---
name: agency-data-engineer
description: Build reliable data pipelines and analytics-ready datasets. USE when cleaning data, designing ETL/ELT, defining contracts, or shipping reproducible data workflows.
risk: low
source: community
date_added: '2026-03-18'
---

# Data Engineer

Use this skill for data work that must be reproducible, trustworthy, and operationally clear.

## Best for

- Cleaning and joining messy datasets into reviewable outputs
- Building or repairing ETL/ELT workflows
- Defining data contracts, validation checks, and observability
- Preparing analytics-ready assets for dashboards, reports, or downstream models

## Workflow

1. Read repo or workspace instructions first.
2. Inventory the datasets, schemas, and likely join keys.
3. Identify quality risks before transforming anything:
   - missing keys
   - schema drift
   - duplicates
   - null handling
   - timestamp/timezone issues
4. Propose the smallest reproducible workflow from ingest to validated output.
5. Add explicit checks for freshness, completeness, and join correctness.
6. Prefer scripts and versioned artifacts over one-off notebook state.

## Output contract

Produce:
- source inventory
- key assumptions and quality risks
- proposed pipeline or analysis workflow
- validation checks
- output artifacts and how to reproduce them

## Critical rules

- All pipelines must be **idempotent** — rerunning produces the same result, never duplicates
- Every pipeline must have **explicit schema contracts** — schema drift must alert, never silently corrupt
- **Null handling must be deliberate** — no implicit null propagation into gold/semantic layers
- Prefer reviewable outputs over hidden notebook-only state
- Make freshness, completeness, and lineage visible where practical

## Starter prompts

- Inventory these datasets, identify quality risks, and propose a reproducible workflow from ingest to validated output.
- Build the smallest reliable pipeline that turns these raw files into analytics-ready tables.
- Audit this data workflow for schema drift, duplicate risk, null handling, and missing quality checks.

## Autonomous decision rules

**Use this skill when:**
- the task is about ETL, data cleanup, joins, contracts, or analytics-ready outputs
- the user wants a reproducible data workflow rather than one-off analysis notes

**Do NOT use when:**
- the task is purely BI storytelling with no pipeline or dataset work
- a narrower domain skill already owns the data source and output format
