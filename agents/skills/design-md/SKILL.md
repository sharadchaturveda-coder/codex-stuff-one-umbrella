---
name: design-md
description: Apply a local DESIGN.md design system when generating, editing, reviewing, or refactoring UI. Use when a repo contains DESIGN.md files, when the user wants a UI to match a specific brand or preset, or when translating design tokens and prose guidance into concrete code, Tailwind themes, component styling, and visual QA.
---

# DESIGN.md

Treat `DESIGN.md` as the project's visual contract.

- YAML front matter is normative: colors, typography, spacing, rounded values, and components are the source of truth.
- Markdown prose explains intent, hierarchy, tone, and when to use the tokens.
- When tokens and prose disagree, prefer tokens for literal values and prose for judgment calls.

## When to use this skill

Use this skill when:

- the workspace contains one or more `DESIGN.md` files
- the user asks to match an existing brand, vibe, or reference site
- the task includes UI generation, restyling, component work, landing pages, theme systems, or design QA
- the user wants to import a catalog or preset design system into a product workflow

## Workflow

### 1. Find the active design system

- Search for the nearest `DESIGN.md` to the files being edited.
- In monorepos, prefer the package-local `DESIGN.md` over a root file.
- If multiple candidates apply, state which one you are using.

### 2. Extract the implementation contract

Before editing UI, identify:

- brand summary from `## Overview`
- color roles and high-contrast pairings
- typography roles and any display/body/label split
- spacing and radius scales
- component tokens and variant intent
- explicit do/don't guidance

### 3. Validate before trusting

If the local CLI is available, lint first.

```bash
npx @google/design.md lint DESIGN.md
```

If the repo includes the source monorepo, prefer its local CLI entrypoint instead of the published package.

Use `diff` when comparing revisions and `export` when a Tailwind or DTCG token dump will reduce guesswork.

### 4. Translate design into code

Map tokens into the codebase's existing styling system.

- Tailwind: convert tokens into theme values or CSS variables, then compose utilities
- CSS or CSS-in-JS: define variables first, then consume them in components
- Component libraries: preserve the library's structure, override with the design tokens

Do not copy the prose into code comments or invent a parallel visual system.

### 5. Keep the UI honest

- preserve responsiveness
- maintain accessible contrast and readable type
- respect the repo's established architecture
- do not introduce a second visual system next to the one in `DESIGN.md`

## Operational rules

### If a token is missing

- infer from prose only when needed for completion
- prefer existing codebase conventions over invented new scales
- state assumptions briefly in the final response if they changed implementation choices

### If the request conflicts with the design system

- flag the conflict plainly
- make the smallest deviation that satisfies the user
- do not silently drift the entire interface

### If no DESIGN.md exists

- do not pretend one exists
- ask for one, use a curated preset, or proceed with the repo's existing design system

## Sourcing a DESIGN.md

When the user wants an existing style quickly, a good source is the VoltAgent collection:

- Repo: `https://github.com/VoltAgent/awesome-design-md`
- Site: `https://getdesign.md/`

Prefer a project-local `DESIGN.md` over any external preset.

## Pairing rules

Pair `design-md` with:

- `frontend-design` when building new UI from scratch
- `adapt` for responsive behavior
- `polish` after the core implementation is in place

Do not use `design-md` as a replacement for implementation skills.
