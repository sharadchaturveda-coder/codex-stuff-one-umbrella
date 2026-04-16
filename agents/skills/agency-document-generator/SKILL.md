---
name: agency-document-generator
description: Generate professional PDF, PPTX, DOCX, and XLSX artifacts from code. USE when packaging data, notes, or visuals into reusable document outputs.
risk: low
source: community
date_added: '2026-03-18'
---

# Document Generator

Use this skill when the deliverable is the document itself, not just the underlying analysis.

## Best for

- PPTX, PDF, DOCX, and XLSX generation from structured inputs
- Turning analysis, notes, or reports into stakeholder-ready artifacts
- Repeatable document workflows instead of one-off manual edits
- Output validation for layout, formatting, and data presentation

## Workflow

1. Establish audience, purpose, and target format first.
2. Pick the simplest generation path that preserves the required structure:
   - PDF for distribution-ready fixed layout
   - PPTX for editable slides
   - DOCX for editable narrative docs
   - XLSX for structured tables, formulas, and analysis handoff
3. Keep content data-driven and templated.
4. Render or inspect the output before delivery when possible.
5. Call out any layout or fidelity risks that still need human review.

## Output contract

Produce:
- generation script or implementation
- output artifact
- short notes on customization points
- validation status and any remaining issues

## Critical rules

1. **Use proper styles** — Never hardcode fonts/sizes; use document styles and themes
2. **Consistent branding** — Colors, fonts, and logos match the brand guidelines
3. **Data-driven** — Accept data as input, generate documents as output
4. **Accessible** — Add alt text, proper heading hierarchy, tagged PDFs when possible
5. **Reusable templates** — Build template functions, not one-off scripts
6. **Validate final output** — Check for overflow, truncation, broken tables, and font substitution when possible

## Starter prompts

- Generate a stakeholder-ready `<format>` from these notes/data and keep the workflow reusable.
- Build this deck/report from code, render the output, and fix layout issues before delivery.
- Turn this analysis into an editable document artifact with clear branding and data presentation.

## Autonomous decision rules

**Use this skill when:**
- the user needs a report, deck, document, spreadsheet, or PDF output
- the value is in packaging information into a shareable artifact

**Do NOT use when:**
- the task is only raw analysis or implementation with no document deliverable
- a narrower presentation skill is better, such as `frontend-slides` for HTML decks
