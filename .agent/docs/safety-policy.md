# Safety & Environment Policy

## 1. Secrets and Credentials
- NEVER read `.env` directly unless specifically instructed via a controlled tool or explicitly necessary for a single scoped variable.
- NEVER log passwords, tokens, API keys, or full request bodies containing PII to standard output, trace logs, or analytics.
- If a token must be moved, handle it via environment variables, not hardcoded strings.

## 2. Dependencies
- NEVER invent dependencies. If a package does not exist in `package.json`, do not require or import it.
- Ask for permission before running `npm install` or `yarn add`.

## 3. Scope of Modification
- Implement MINIMAL VIABLE CHANGES.
- Do not refactor code outside the immediate scope of the task.
- Do not add "helpful" docstrings or reformat unrelated files just because you are touching them.

## 4. Execution Limits
- If a command fails 3 times, STOP. Do not enter an infinite loop of guessing syntax. Request human intervention.
- Never run commands that delete or overwrite directories (`rm -rf`) without explicit, multi-stage confirmation.
