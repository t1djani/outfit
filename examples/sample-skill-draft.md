---
name: riot-ingest
description: Use when touching Riot data ingestion, player search, or profile loading — encodes the cache-first model, puuid resolution, and rate-limit traps. Invoke before editing ingest, loader, or playerSearch.
---

# riot-ingest

> Drafted by outfit from: `web/src/ingest/*` (12 files) + CLAUDE.md "cache-first" + roadmap HAR-9. Edit before use.

Domain rules this skill guards (fill from the code outfit pointed at):

- Cache-first: read from the store before calling Riot; never hammer the API in a loop.
- Resolve identity through the alias table, not a raw puuid (puuid is per-application).
- Respect rate limits: batch, back off, and never `.map(async)` over Riot calls.

## When to invoke

Add a Riot query · edit the profile loader · change player search · add a link to a profile.
