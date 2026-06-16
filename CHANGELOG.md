# Changelog

All notable changes to outfit are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/), and versions follow [SemVer](https://semver.org/).

## [0.1.0] — 2026-06-16

First public alpha.

### Added
- **The four beats** (`outfit` skill) — harvest (deterministic evidence collector), recon (the AI reads the project, probes connected tools, infers the domain), grounded proposals with a multi-select, and forge (writes editable skill/agent drafts).
- **`harvest.py`** — standard-library collector that gathers tree, key files, git log, docs, and detected resources, and decides nothing.
- **`validate-draft.sh`** — a deterministic form check on generated drafts (frontmatter, kebab `name`, non-empty `description`).
- **`/outfit [thorough]`** command, a real evidence sample, and skill/agent draft samples.
