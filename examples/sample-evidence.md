# outfit · evidence dossier

_Raw material only. This file CLASSIFIES NOTHING and INFERS NOTHING — the agent reads it, probes live tools, and decides what the project needs._


## TREE

```
  .gitignore
  LICENSE
  .claude-plugin/
    marketplace.json
    plugin.json
  commands/
    outfit.md
  docs/
    method.md
  examples/
    sample-evidence.md
  hooks/
    validate-draft.sh
  scripts/
    harvest.py
  skills/
    outfit/
      SKILL.md
  tests/
    test_harvest.py
    test_validate_draft.py
    fixtures/
      bad-empty-description.md
      bad-no-frontmatter.md
      good-agent.md
      good-skill.md
```

## KEY FILES

_none of the known manifests/readmes are present._

## GIT

```
005ac32 docs: the outfit method + sources
4f459bb feat(command): /outfit [thorough]
897045f feat(skill): outfit orchestration — four beats (harvest, recon, propose, forge)
e4810a3 feat(hook): validate-draft.sh — deterministic form check on drafts
b0e7e9b feat(harvest): render full evidence dossier + CLI entrypoint
5427e48 feat(harvest): git summary, docs finder, resource detector
10d36e2 feat(harvest): byte-bounded key-file reader
8b25390 feat(harvest): bounded tree builder, skips noise dirs
56c44e4 chore: scaffold outfit plugin (metadata, license, gitignore)
```

## DOCS

- docs/method.md

## RESOURCES

_no servo manifest, MCP config, or .claude assets detected._

## NEXT

This harvest DECIDES NOTHING. Now do the recon: read these files for meaning, follow the roadmap, probe which MCP servers / CLIs / docs you actually have, infer the domain, then propose grounded skills/agents for the user to pick.
