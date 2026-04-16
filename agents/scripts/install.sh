#!/usr/bin/env bash
# Install all skills globally for Codex CLI and Claude Code
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"

CODEX_DIR="${HOME}/.codex/skills"
CLAUDE_DIR="${HOME}/.claude/agents"

install_codex() {
    mkdir -p "$CODEX_DIR"
    local count=0
    for skill_dir in "$SKILLS_SRC"/*/; do
        cp -r "$skill_dir" "$CODEX_DIR/"
        (( count++ )) || true
    done
    echo "[OK] Codex CLI: $count skills -> $CODEX_DIR"
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
echo "Codex:       157 agency skills + 21 impeccable skills (auto-invoked)"
echo "Claude Code: 157 agency agents"
