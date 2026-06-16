<div align="center">

# outfit

**Walk into a repo, walk out with the skills it needs.**
outfit reads what your project *is* — code, docs, memory, the tools you have wired — and proposes the Claude Code skills and agents tailored to it. You pick from grounded proposals; outfit writes the drafts.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](https://docs.claude.com/en/docs/claude-code)
[![status: alpha](https://img.shields.io/badge/status-alpha-orange.svg)](#roadmap)

</div>

---

## Quickstart

```bash
/plugin marketplace add t1djani/outfit
/plugin install outfit@outfit
```

Then, in any project:

```bash
/outfit
```

outfit reads the repo, infers what it is, and shows you a **multi-select** of skills and agents worth creating — each with the evidence behind it. Check the ones you want; it writes the drafts to `.claude/skills/` and `.claude/agents/`. Add `thorough` for a deeper, fan-out recon on big repos.

## The idea

Most "scaffold some skills" tools keyword-match your stack: see Next.js, emit a Next skill. That floods a project with generic capabilities nobody triggers. The value isn't in listing your dependencies — it's in **understanding what the project is for**.

outfit infers the domain by *reading*: the roadmap, the memory, the conventions in the code, and the tools you actually have connected. Detecting that a repo needs a coaching skill comes from understanding it's a coaching product — not from a regex.

## Why it is different

- **The inference is the AI's; the plumbing is a script.** A deterministic `harvest.py` gathers raw material (and decides nothing). The agent does the understanding — reading for meaning, **probing which MCP servers / CLIs / docs are actually connected**, inferring the domain. The form-check on generated drafts is a deterministic hook. Determinism at the ends, intelligence in the middle.
- **No proposal without evidence.** Every suggested skill/agent carries why — "this directory + this doc line + this roadmap item". Anything unanchored is dropped or flagged `speculative`. No generic filler.
- **It adapts to the tools you have.** Linear or Jira or Notion; Postgres or Mongo; context7 or not — outfit detects what's wired and proposes accordingly. There is no hardcoded stack list to go stale.
- **You choose.** Proposals come as a multi-select. outfit writes nothing until you've picked, and never auto-activates anything beyond writing an editable draft.
- **It reuses what's already there.** A `.servo/manifest.yaml`, a war-room roster, existing `.claude/skills` — outfit reads them as evidence instead of duplicating them.

## The four beats

```
harvest (script)  →  recon (AI)  →  propose + you pick  →  forge + validate (AI + script)
  decides nothing      the inference      multi-select          editable drafts, form-checked
```

See [docs/method.md](docs/method.md) for the full method and a real evidence sample in [examples/](examples/).

## How it works

**Cost scales to the repo.** `quick` (default) is a single recon pass. `thorough` fans out one subagent per thread (roadmap & docs, code conventions, git/CI signals, connected tools) for large or serious onboarding.

**It knows when not to run.** If you already know the one skill you want, that's `writing-skills`. If you want a servo manifest specifically, that's `scan-project`. outfit is for "equip this whole repo".

**Plugin layout**

```
outfit/
├── .claude-plugin/{plugin.json, marketplace.json}
├── skills/outfit/      # the four-beat orchestration — markdown, the core
├── commands/           # /outfit [thorough]
├── scripts/            # harvest.py — deterministic evidence collector (stdlib)
├── hooks/              # validate-draft.sh — form check on generated drafts
├── examples/           # a real evidence harvest + draft samples
└── docs/               # the method + sources
```

## Develop

markdown-first: the skill is prose, the collector is Python standard library, the form-check is bash. Nothing to build — edit a file, reload the plugin, done. Tests: `python3 -m pytest tests/ -v`.

## Contributing

Early days. Issues and ideas welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © t1djani

---

## Roadmap

- [x] **harvest** · deterministic evidence collector that decides nothing.
- [x] **recon** · AI infers the domain by reading + probing connected tools.
- [x] **grounded proposals** · every skill/agent carries its evidence; you multi-select.
- [x] **forge + form-check** · writes editable drafts, validated for structure.
- [ ] **`--refresh`** · revisit an equipped repo and propose updates to the existing kit.
