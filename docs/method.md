# The outfit method

outfit equips a repo with Claude Code capabilities (skills and agents) tailored to what the project actually is. It is built on one conviction: **a generic scaffolder is worse than nothing** — it floods a project with skills nobody triggers. The value is in understanding the project first.

## Deterministic at the ends, intelligent in the middle

```
harvest (script)  →  recon (you)  →  propose + pick (you + user)  →  forge + validate (you + script)
   decides nothing     all the inference        the human chooses          form check only
```

- **harvest** (`scripts/harvest.py`, standard library) gathers raw material — tree, key files, git, docs, detected resources — and *classifies nothing*. It exists so the agent does not burn context re-listing the repo.
- **recon** is the whole point. The agent reads for meaning, **probes the tools actually connected this session** (a tracker MCP — Linear, Jira, Notion; a database; docs servers), dives the code on the threads that matter, and **infers the domain**. None of this is pattern-matching; it is reasoning over evidence.
- **propose** turns recon into capabilities, each carrying its evidence. Anything without evidence is dropped or marked `speculative`. The user multi-selects.
- **forge** writes the chosen drafts; `validate-draft.sh` checks their *form* (frontmatter, name, description) — never their quality, which stays human.

## Why grounding is the moat

Adding "scan and suggest skills" to a prompt is one line. The difference is the discipline: **no proposal ships without a repo-anchored reason**, and the inference comes from reading the roadmap, the memory, and the wired tools — not from a hardcoded `if Next.js then suggest a Next skill` table. That is why outfit adapts: it has no stack list to fall out of date.

## Relation to neighbours

| Tool | Produces | Why outfit is different |
|---|---|---|
| `writing-skills` (superpowers) | *how* to write one skill, by hand | outfit decides *what* to write and pre-fills it |
| `scan-project` (servo) | a servo manifest (internal config) | a config for a loop, not reusable capabilities |
| `discover-roster` (war-room) | a roster of officers for one run | ephemeral, scoped to a single decision |

outfit reuses these if present (a servo manifest becomes evidence) and depends on none.

## Sources

- Capability-as-prompt discipline: Claude Code skills & subagents conventions (frontmatter `name`/`description` as the trigger surface).
- Grounding / anti-theater doctrine: shared with `servo` (verification must inject ground truth) and `war-room` (external, openable references; determinism stops at structure).
- Onboarding-as-reading: the recon step models a senior engineer onboarding — follow the roadmap and the money, read the memory, then act.
