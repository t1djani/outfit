---
description: Read this project and propose tailored skills/agents to create — you pick from grounded proposals
argument-hint: "[thorough]"
---

Run the `outfit` skill on this project.

Depth: $ARGUMENTS

Harvest the evidence (`scripts/harvest.py`), do the recon — read the project for meaning, probe which MCP servers / CLIs / docs are actually connected and adapt, infer the domain — then propose skills and agents tailored to this repo, each grounded in real evidence. Present them with a multi-select so I pick. Write only what I choose to `.claude/skills/` and `.claude/agents/`, and validate each draft's form with `hooks/validate-draft.sh`.

If `thorough` is passed, fan out one recon subagent per thread (roadmap & docs, code conventions, git/CI signals, resources & connected tools) before synthesizing. Otherwise do a single recon pass.

Do not write anything before I have made my selection.
