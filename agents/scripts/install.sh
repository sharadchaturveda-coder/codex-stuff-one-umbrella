#!/usr/bin/env bash
# Install agency skills without bloating Codex CLI startup context.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"

CODEX_DIR="${HOME}/.codex/skills"
CLAUDE_DIR="${HOME}/.claude/agents"

install_codex() {
    mkdir -p "$CODEX_DIR"
    echo "[OK] Codex CLI: agency skills remain repo-local at $SKILLS_SRC"
    echo "     Do not copy the full agency library into $CODEX_DIR; route on demand through skill-router/skill-tree."
}

install_claude() {
    mkdir -p "$CLAUDE_DIR"
    local count=0
    for skill_dir in "$SKILLS_SRC"/agency-*/; do
        skill_md="$skill_dir/SKILL.md"
        [[ -f "$skill_md" ]] || continue
        name=$(basename "$skill_dir")
        cp "$skill_md" "$CLAUDE_DIR/${name}.md"
        (( count++ )) || true
    done
    echo "[OK] Claude Code: $count agents -> $CLAUDE_DIR"
}

echo ""
echo "Installing skills..."
echo ""
install_codex
install_claude
echo ""
echo "Done! Restart Codex CLI and Claude Code to pick up new skills."
echo ""
echo "Codex:       repo-local agency skills (router-invoked on demand)"
echo "Claude Code: 157 agency agents"
