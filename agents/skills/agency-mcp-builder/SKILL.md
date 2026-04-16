---
name: agency-mcp-builder
description: Build MCP servers with clear tool contracts, validation, and tests. USE when planning or implementing tools, resources, prompts, and MCP transports.
risk: low
source: community
date_added: '2026-03-18'
---

# MCP Builder

Use this skill when the job is to design or implement an MCP server, not just discuss one.

## Best for

- Planning a narrow MCP tool surface for an agent workflow
- Implementing or upgrading MCP servers
- Defining tool/resource contracts before writing code
- Auditing MCP server ergonomics, validation, and failure modes

## Workflow

1. Start from the user outcome or agent workflow.
2. Define the minimum viable tool surface before implementation.
3. For each tool, specify:
   - name
   - description
   - input schema
   - return shape
   - failure cases
4. Decide what belongs in:
   - tools
   - resources
   - prompts
5. Choose transport last, after the contract is clear.
6. Validate with at least one realistic usage path.

## Output contract

Produce:
- a tool plan
- implementation approach
- security and auth notes
- test strategy
- rollout or migration notes if applicable

## Critical rules

1. **Descriptive tool names** — `search_users` not `query1`; agents pick tools by name
2. **Schema first** — Every tool input validated, optional params have defaults
3. **Structured output** — Return machine-usable data and readable errors
4. **Fail gracefully** — Never leak raw stack traces to clients
5. **Stateless by default** — Do not rely on call order unless explicitly designed that way
6. **Small v1** — Prefer 3-5 sharp tools over a broad vague surface

## Starter prompts

- Plan an MCP server for this workflow. Start with the smallest useful tool surface and specify tool contracts before implementation.
- Audit this MCP server for poor tool names, weak schemas, auth gaps, and confusing outputs.
- Implement an MCP server for `<use case>` with typed inputs, clear failures, and a realistic test path.

## Autonomous decision rules

**Use this skill when:**
- the task mentions MCP servers, tools, resources, prompts, or agent connectors
- the user needs agent capabilities exposed through a protocol boundary

**Do NOT use when:**
- the task is only general API design with no MCP surface
- the user only needs product planning and no protocol/tool design
