# Contributing to outfit

Early days — issues, ideas, and PRs welcome.

## Principles (please keep these)

- **The deterministic layer decides nothing.** `harvest.py` gathers; `validate-draft.sh` checks form. All domain inference stays in the skill (the AI). Don't push classification into the scripts.
- **No proposal without evidence.** Anything outfit suggests must carry a repo-anchored reason, or be marked `speculative`.
- **The user multi-selects.** Never write or activate a capability the user didn't choose.
- **Adapt, don't hardcode.** Detect the tools that are present; don't bake in a stack list.

## Development

markdown-first. Edit a skill, command, or doc; reload the plugin. The only code is `scripts/harvest.py` (Python stdlib) and `hooks/validate-draft.sh` (bash).

Run the tests:

```bash
python3 -m pytest tests/ -v
```

## Conventional commits

Use Conventional Commit subjects (`feat:`, `fix:`, `docs:`, `chore:`).
