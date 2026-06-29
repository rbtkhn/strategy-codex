---
name: audit-index
description: Audit statecraft archive index surfaces (day-index parity, stale global navigation, capture hygiene) with optional inventory table; run audit index before blaming intake when stats look wrong. Use --fix only on EXECUTE confirm.
preferred_activation: audit index
activation: audit index · audit day-index · index audit · audit index table
portable: true
version: 1.0.1
category: truth-pipeline
status: active
scope_class: repo-governed
tags:
- operator
- strategy
- source-archive
- index
portable_source: skills/audit-index/SKILL.md
synced_by: sync_portable_skills.py
---
# Audit index

**Preferred activation (operator):** say **`audit index`**.

Verify **derived index surfaces** against live archive captures — day-index parity, stale global navigation (writer-index, channel-index, thread-index, year rollups), and optional capture-hygiene warnings. Captures are SSOT; a stale index is not a missing capture.

## When to use

- After intake batch or before daily synthesis compose
- Operator says **`audit day-index`**, **`audit june 28`**, **`audit archive indices`**
- Host/thread/kind stats on day-index look wrong vs capture YAML
- Channel roster counts or last-day columns look wrong vs recent YouTube intake
- Monthly closeout or pre-push when index churn is suspected

## When not to use

- **Source land** — use **`source-intake`** (rebuild day-index is in post-land chain; audit is verify/nudge)
- YouTube live discovery — use **`check sources`**
- Full repo surgeon / unrelated hygiene — use **`repo-hygiene-pass`**

## Core law

- Index files are **derived** from captures + roster membranes
- Stale stats → rebuild; do not delete or re-land captures
- Global stack uses **`build_statecraft_archive_navigation`** (includes **writer-index**); `refresh_statecraft_archive_indices.py` is a subset

## Modes

| Operator intent | CLI |
|-----------------|-----|
| One day | `--day YYYY-MM-DD` |
| Month | `--month YYYY-MM` |
| Year inventory | `--year YYYY` |
| Global navigation | `--global` |
| Channel index (YouTube roster) | `--channel-index` |
| Inventory table only | `--table-only` + scope |
| Audit + table | `--table` + scope |
| Rebuild stale | `--fix` (EXECUTE / explicit confirm only) |

**Table:** capture scope — Date, Title, URL, Words, Bucket, Kind, §. **Channel-index** scope — Slug, Label, Files, Days, Watchlist, Last day, URL (`--table-sort words` → file count, `title` → label, `bucket` → slug, `date` → files).

## Execution order

1. **Run CLI first** (validator-first — do not read builder source before first run):
   ```bash
   python scripts/audit_statecraft_archive_index.py --day YYYY-MM-DD
   ```
2. Reply with **exit code** + PASS/FAIL/WARN lines + suggested fix command when fail
3. **`--fix`** only when operator confirms or **EXECUTE** lane names fix
4. Optional **`--table`** when operator wants URL/word/date scan without opening each capture

## Receipt

Human output sections:

- `## Index audit — <scope>` — PASS/FAIL/WARN by check code
- `## Index inventory — <scope>` — when `--table` or `--table-only`
- Trailing `exit 0` or `exit 1`

Use **`--json`** for machine handoff (`findings`, `table`, `exit_code`).

## Table fork (after audit)

Offer **view full index table** when audit passes but operator needs URL/word scan:

```bash
python scripts/audit_statecraft_archive_index.py --day YYYY-MM-DD --table-only
```

Phrases: **`audit index table`**, **`index table june 28`**, **`show index table`**.

## Known quirk (post-land)

`post_land_caption_wrapper_normalize.py` may blank **`host_people`** / **`threads`** while scalar **`host`** / **`thread`** remain. Restore YAML manually, rebuild day-index, then **`audit index --day …`** to confirm stats match capture.

## Relation

- Day-index spec — derived partition law for channel / writer / other
- **`source-intake`** — post-land rebuild; audit when stats still look wrong
- **`validator-first`** — run script before reading its source

## Verification / Proof Standard

Report: scope, exit code, findings summary, fix command if fail, whether `--fix` was applied. Name files read (bounded day-index only) vs files rebuilt.
