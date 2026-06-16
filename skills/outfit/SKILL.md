---
name: outfit
description: Use when onboarding a project or equipping a repo with Claude Code capabilities — read what the project IS (code, docs, memory, connected tools) and propose tailored skills/agents the user multi-selects, then write the drafts. Do NOT use to write a single known skill (use writing-skills) or to configure servo (use scan-project).
---

# outfit

You walk into a repo and walk out with the panoply it needs. outfit reads a project, **understands what it is**, and proposes the skills and agents tailored to it. The user picks; outfit writes the drafts.

The failure this prevents: a generic scaffolder that keyword-matches a stack and spits out skills nobody uses. outfit's proposals are **grounded in real evidence** and come from **actually understanding the project** — its roadmap, its memory, the tools it has wired.

**The one rule that defines outfit:** the deterministic parts decide nothing. Plumbing (harvest, form-validation) is scripted so it is cheap and well-formed. The **inference — what this project is, what it needs — is entirely yours**, done by reading and probing, not by pattern-matching.

## Procedure

Drive it as a TodoWrite checklist so the user watches it work: one todo per beat (harvest, recon, propose, forge, register).

### Beat 1 — Harvest (cheap, decides nothing)

Run the deterministic collector to get raw material without burning context re-listing the repo:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/harvest.py" .
```

It prints an evidence dossier: tree, key files, git log, docs, and detected resources (`.servo/manifest.yaml`, `.mcp.json`, `.claude/` assets…). Read it. It classifies nothing — that is your job next.

### Beat 2 — Recon (this is where the intelligence is)

**Understand the project like a human onboarding.** Do not skim. Go after the threads that reveal what it *is*:

- Read for meaning: CLAUDE.md/AGENTS.md, the README, the roadmap, any specs or memory the harvest surfaced. If there is a memory vault or notes, read them.
- **Probe your own capabilities and adapt.** Look at what tools you actually have this session — which MCP servers are connected (a tracker like Linear *or* Jira *or* Notion; a DB; Sentry; docs like context7), which CLIs, which framework docs. Do not assume a fixed stack. If the project talks about tickets but no tracker MCP is wired, note it.
- Dive into the code only on the threads that matter — the domain core, the recurring conventions, the footguns — not the whole repo.
- **Infer the domain in one line** ("a League of Legends coaching product, multi-repo", "a marketing SaaS", "a Python data engine"). Everything downstream hangs on getting this right, and it is yours to reason out — the script cannot.

Depth:
- **quick (default):** one recon pass over the harvest + a capability probe.
- **thorough:** fan out — a subagent per thread (roadmap & docs, code conventions, git/CI signals, resources & connected tools) — then synthesize. Use for large repos or a serious onboarding.

### Beat 3 — Propose, grounded, and let the user pick

Turn the recon into a list of proposed capabilities. **Every proposal carries its evidence. No evidence → drop it or tag it `speculative`.** For each:

```
name          : hs-ingest
type          : skill            # skill | agent
role          : guard rail for Riot ingestion (cache-first, rate-limit, puuid)
triggers      : "add a Riot query", "profile loader", "playerSearch"
evidence      : web/src/ingest/* (12 files) + CLAUDE.md "cache-first" + roadmap HAR-9
confidence    : grounded         # grounded | speculative
```

- Prefer a **skill** for a domain/convention/guardrail the agent should follow; an **agent** for a focused reviewer/worker with its own tool set.
- **Reuse, don't duplicate.** If a `.servo/manifest.yaml`, a war-room roster, or existing `.claude/skills` are present, use them as evidence and don't re-propose what already exists.
- You may also offer **meta-suggestions**: create a `.servo/manifest.yaml`, or wire a missing MCP you inferred would help ("you reference tickets but no tracker is connected").

Present the full list to the user with **AskUserQuestion, `multiSelect: true`** — they check what they want. **Write nothing until they have chosen.**

### Beat 4 — Forge the drafts, then validate the form

For each selected proposal, write a draft pre-filled with what recon understood (role, triggers, the evidence, known footguns), **editable**, never auto-activated beyond writing the file:

- skill → `.claude/skills/<name>/SKILL.md` with frontmatter `name` + `description` (fold the triggers into the description, the way this skill's own frontmatter does).
- agent → `.claude/agents/<name>.md` with frontmatter `name`, `description`, `tools`.

Then check the form of each draft:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/hooks/validate-draft.sh" <path-to-draft>
```

It verifies structure only (frontmatter, kebab `name`, non-empty `description`). Quality stays your call and the user's.

### Beat 5 — Register the kit (point it where the project looks)

A written draft is discoverable but not *announced*. Claude Code auto-discovers `.claude/skills/` and `.claude/agents/`, so the files already work — but a project keeps a human-readable index of its capabilities, and that index is where conventions and routing point. Finish by wiring the new kit in:

- **Place each file in its home.** Default to the project's `.claude/skills/<name>/SKILL.md` and `.claude/agents/<name>.md`. If the project clearly uses another root (a plugin layout, a monorepo package's own `.claude/`, a custom skills dir referenced in CLAUDE.md), put it there instead — recon told you which.
- **Index them where the project documents its tooling.** Find the agent-instructions file the harvest surfaced — `CLAUDE.md`, else `AGENTS.md`/`GEMINI.md`. If it has a toolchain/skills/capabilities section, add one line per new capability (name + its one-line "use when"); if not, add a short `## Skills & agents` section. Keep it **idempotent** — never duplicate an entry that is already there. Match the file's existing voice and format.
- **Show the diff and get a yes before writing to CLAUDE.md.** That file is load-bearing and usually tracked. Propose the exact lines; write only after the user confirms (same rule as the proposals — the user chooses).

Then report what was written, where each file landed, what was added to the index, and that the drafts are starting points to edit.

## Rules

- **The deterministic layer never decides.** harvest gathers; the hook checks form. The domain inference is yours.
- **No proposal without evidence.** Grounded or `speculative` — never silent invention.
- **The user multi-selects.** Nothing is written outside the selection.
- **Register, don't strand.** Finish by placing each capability in its home and indexing it in the project's instructions file — but show the CLAUDE.md diff and get a yes first. Keep the index idempotent.
- **Probe, don't assume.** Detect the tools that are actually there and adapt (Linear vs Jira…). No hardcoded stack list.
- **Reuse the existing** (servo manifest, roster, memory, current skills) as evidence; don't re-derive or duplicate.
- **Know when not to run.** If the user already knows the one skill they want, that is `writing-skills`, not outfit. If they want a servo manifest specifically, that is `scan-project`.
