---
name: audit-index
description: Audit statecraft archive index surfaces (day-index parity, stale global navigation, capture hygiene) with optional inventory table; run audit index before blaming intake when stats look wrong. Use --fix only on EXECUTE confirm.
preferred_activation: audit index
activation: audit index · audit day-index · index audit · audit index table
portable: true
version: 1.0.5
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
- Writer roster file/day counts look wrong after Substack lands
- New voice shelf landed but missing from `voice-index.md` analyst table
- Curated shelf bench (`parsi-index.md`, etc.) links broken or archive captures not cited
- After **source-intake** land for parsi / pape / crooke / ritter — verify author/guest index parity
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
| Writer index (prose roster) | `--writer-index` |
| Voice index (analyst registry) | `--voice-index` |
| Voice shelf bench (curated source index) | `--shelf-index SLUG` (e.g. `parsi`, `pape`, `crooke`, `ritter`, `jiang`) |
| Inventory table only | `--table-only` + scope |
| Audit + table | `--table` + scope |
| Rebuild stale | `--fix` (EXECUTE / explicit confirm only) |

**Table:** capture scope — Date, Title, URL, Words, Bucket, Kind, §. **Channel-index** / **writer-index** — roster rows. **Voice-index** — shelf registry; **curated** — no `--fix`. **Shelf-index** — author/guest capture links from `{slug}-index.md`; **curated** — no `--fix`; honors documented stub exclusions.

## Source-intake post-land (author/guest index)

After `build_statecraft_day_indices.py --day` when landed capture resolves to a voice shelf (parsi, pape, crooke, ritter):

```bash
python scripts/shelf_index_from_capture.py --path source-archive/statecraft/YYYY-MM-DD/source-....md --apply --audit
```

Law: [`speaker-shelf-vocabulary.md`](../../statecraft/voices/speaker-shelf-vocabulary.md) § Author/guest shelf index. **Jiang:** `--shelf-index jiang` audits external interview appearances only; PH channel + essays use `jiang-predictive-history-index.md`.

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


## Cursor / strategy-codex instance

Repo-specific paths and commands for **audit-index** (from `.cursor/skills/audit-index/`).

| Topic | Path |
|--------|------|
| Audit CLI | [scripts/audit_statecraft_archive_index.py](../../../scripts/audit_statecraft_archive_index.py) |
| Channel index (md/json) | [statecraft/channels/channel-index.md](../../../statecraft/channels/channel-index.md) |
| Writer index (md/json) | [source-archive/statecraft/writer-index.md](../../../source-archive/statecraft/writer-index.md) |
| Voice index (curated) | [statecraft/voices/voice-index.md](../../../statecraft/voices/voice-index.md) |
| Day-index builder | [scripts/build_statecraft_day_indices.py](../../../scripts/build_statecraft_day_indices.py) |
| Global navigation builder | [scripts/build_statecraft_archive_navigation.py](../../../scripts/build_statecraft_archive_navigation.py) |
| Day-index spec | [source-archive/statecraft/day-index-spec.md](../../../source-archive/statecraft/day-index-spec.md) |
| Archive root | [source-archive/statecraft/](../../../source-archive/statecraft/) |
| Source intake (post-land) | [statecraft-source-intake/SKILL.md](../statecraft-source-intake/SKILL.md) |
| LLM routing — day-index row | [LLM-ROUTING.md](../../../LLM-ROUTING.md) |
| Portable manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |

**Bounded read (Windows harness):** when path is known, `Read` `source-archive/statecraft/YYYY-MM-DD/day-index.md` with **limit ≤ 60** — do not grep the archive for index truth.

**Common commands (one Shell per turn; batch with `;` on Windows):**

```powershell
python scripts/audit_statecraft_archive_index.py --day 2026-06-28
python scripts/audit_statecraft_archive_index.py --day 2026-06-28 --table
python scripts/audit_statecraft_archive_index.py --global
python scripts/audit_statecraft_archive_index.py --channel-index --table
python scripts/audit_statecraft_archive_index.py --writer-index --table
python scripts/audit_statecraft_archive_index.py --voice-index --table
python scripts/audit_statecraft_archive_index.py --month 2026-06 --table-only --table-limit 50
python -m pytest tests/test_audit_statecraft_archive_index.py -q
python scripts/sync_portable_skills.py --skill audit-index --verify
```

**Fix law:** `--fix` rebuilds stale day-index (scoped days) and/or full global navigation. Apply only on operator **EXECUTE** or explicit fix confirm. After `--fix`, receipt reflects post-fix state (audit runs after rebuild).

**Do not:** monolithic read of all `source-*.md` for audit; use CLI table mode instead.
