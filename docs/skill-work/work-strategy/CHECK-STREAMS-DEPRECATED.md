# Check streams — DEPRECATED (2026-06-21)

WORK only; not Record.

**Status:** The **`check-streams`** skill slug and **`check streams`** activation phrase are **deprecated** as the canonical name. Use **`check-sources`** / **`check sources`** instead.

## What replaced it

| Old | Use instead |
|-----|-------------|
| **`check-streams`** skill / **`check streams`** | **[`check-sources`](../../../.cursor/skills/check-sources/SKILL.md)** — say **`check sources`** |
| Hard-coded five-channel watchlist in skill prose | **[`channel-index.json`](../../../statecraft/channels/channel-index.json)** roster via `load_check_sources_roster()` (main index; misc excluded) |
| Daily fast pass wording | **`check sources watchlist`** — six `daily_watchlist` channels (`watchlist: true` in JSON) |
| **`cognition streams`** | Legacy alias — still accepted; routes to **`check sources`** |

## Operator chain (current)

```text
check sources → discover / reconcile main channel-index roster → source-intake
```

Pairing with B0 (2026-06-21): roster SSOT is **`channel-index.json`**, not cognition-streams config or skill-local channel lists.

## Legacy pointers

- Deprecated skill stub: [`skills/check-streams/SKILL.md`](../../../skills/check-streams/SKILL.md)
- Canonical skill: [`skills/check-sources/SKILL.md`](../../../skills/check-sources/SKILL.md)
- Related deprecation: [YOUTUBE-MATERIALIZE-DEPRECATED.md](./YOUTUBE-MATERIALIZE-DEPRECATED.md)
