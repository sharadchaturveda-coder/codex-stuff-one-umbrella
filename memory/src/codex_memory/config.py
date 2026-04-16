from pathlib import Path

DEFAULT_ROOT = Path.home() / ".codex-memory"

RESIDENT_BUDGET_TOKENS = 900
ACTIVATION_BUDGET_TOKENS = 500
TOTAL_BUDGET_TOKENS = 1400

GLOBAL_SUMMARY_BUDGET_TOKENS = 250
PROJECT_SUMMARY_BUDGET_TOKENS = 350
STARTUP_BUDGET_TOKENS = 1100

FACT_KIND_WEIGHTS = {
    "preference": 9,
    "correction": 10,
    "environment": 7,
    "convention": 8,
    "workflow_hint": 6,
    "error_fix": 8,
}
