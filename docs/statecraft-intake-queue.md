# Statecraft intake queue

**Work only; not Record.**

Operational spec for the **intake queue** layer: structured routing metadata between verbatim archive capture and daily synthesis. Product context: [intelligence-harness.md](intelligence-harness.md). Archive law: [source-archive/statecraft/README.md](../source-archive/statecraft/README.md).

---

## Harness isomorphism

Commercial agent workflows often look like:

```text
scrape source → structure rows → store in DB → agent scores → write-back → scheduled digest
```

**strategy-codex** maps that onto a **Git-sovereign** ladder:

```text
operator source → governed archive (verbatim SSOT)
               → intake queue sidecar (runtime / derived)
               → intake digest (optional precursor)
               → daily synthesis (operating context)
               → note (accountable ceiling)
```

| Commercial step | strategy-codex equivalent |
| ----------------- | --------------------------- |
| Scrape / fetch | Operator-supplied capture via [statecraft-source-intake](../.cursor/skills/statecraft-source-intake/SKILL.md) |
| Structured DB row | Archive YAML frontmatter + optional sidecar JSON |
| Agent score | v0 rule-based hints in sidecar `reasoning` (no LLM in v0) |
| Write-back | Sidecar `synthesis_status` (derived; rebuildable) |
| Top-five digest | `statecraft_intake_queue.py --write-digest` |
| Promote winner | Wire into [statecraft/synthesis/day/](../statecraft/synthesis/METHOD.md) (operator-led) |

**Key rule:** promotion is a **queue problem**, not a summarization problem. Treat each new source as an **intake object** to classify, route, and possibly promote — not as text to summarize in chat.

---

## What already exists

Before adding queue tooling, the repo already lands structured intake:

- **Verbatim archive** at `source-archive/statecraft/<pub_date>/<slug>.md` with YAML frontmatter (`pub_date`, `kind`, `thread`, `host_people`, `guest_people`, `source_url`, `source_note`, …). Example: [2026-06-14 Diesen×Marandi capture](../source-archive/statecraft/2026-06-14/source-glenn-diesen-seyed-m-marandi-israels-attack-on-beirut-sabotage-us-iran-deal-2026-06-14.md).
- **Generated indices** via `refresh_statecraft_archive_indices.py`.
- **Archive ↔ daily sync** via `check_statecraft_intake_daily_sync.py`.
- **Daily synthesis** contract in [statecraft/synthesis/METHOD.md](../statecraft/synthesis/METHOD.md).

The intake queue **extends** this ladder; it does not replace archive truth or daily authority.

---

## Sidecar convention

**Path:**

```text
runtime/artifacts/statecraft-intake-queue/<pub_date>/<source-stem>.v1.json
```

- `<source-stem>` = archive filename without `.md`
- `source_path` = repo-relative path to the archive capture
- Sidecars are **`runtime / derived`** ([work-membrane-v2.md](work-membrane-v2.md)) — rebuildable, not canonical truth
- v0 scripts **never** edit archive body markdown

**Schema:** [schemas/registry/statecraft-intake-sidecar.v1.json](../schemas/registry/statecraft-intake-sidecar.v1.json)

### `synthesis_status`

| Value | Meaning |
| ----- | ------- |
| `new` | In archive; not linked from daily; no sidecar yet |
| `queued` | Sidecar written; operator has not promoted to daily |
| `daily` | Linked from `statecraft/synthesis/day/<pub_date>.md` (script-derived) |
| `discarded` | Operator-marked low signal (manual sidecar edit in v0) |

### v0 scoring

- `strategic_relevance`: optional 0–100; default **null** in v0
- `reasoning`: rule-based hints from existing frontmatter (threads, wire-verify tokens in `source_note`, interview vs solo)
- **No LLM calls** in v0

---

## Lawful intake

**Do not** generalize commercial scraping workflows into “scrape anything.”

| Allowed / safer | Risky / avoid |
| ----------------- | ------------- |
| RSS feeds, public APIs, licensed datasets | ToS-violating scraping |
| Operator-pasted URLs and transcripts | Circumventing access controls |
| Public transcripts with attribution | Personal-data / profile harvesting |
| Manual capture with provenance | Hidden or deceptive collection |
| Roster streams (`check-streams`) with operator selection | Autonomous outreach without review |

---

## Agent boundaries

Agents and scripts may **classify, score (rule-based), summarize drafts, and propose** routing.

Agents may **not** (without explicit operator approval):

- contact people or publish externally
- merge into Record or canonical identity surfaces
- replace daily synthesis or notes silently
- mutate archive verbatim body as if it were queue metadata

See [intelligence-harness.md — Intake queue](intelligence-harness.md#intake-queue-agent-workbench-loop).

---

## Commands (v0)

```bash
# Report queue state for one archive day
python3 scripts/statecraft_intake_queue.py --day 2026-06-14

# Newest captured archive day
python3 scripts/statecraft_intake_queue.py --latest

# JSON report
python3 scripts/statecraft_intake_queue.py --day 2026-06-14 --json

# Write sidecars for sources still in `new` (skip already in daily)
python3 scripts/statecraft_intake_queue.py --day 2026-06-14 --emit-sidecars

# Intake digest (stdout or file)
python3 scripts/statecraft_intake_queue.py --day 2026-06-14 --write-digest
python3 scripts/statecraft_intake_queue.py --day 2026-06-14 --write-digest --digest-out runtime/artifacts/statecraft-intake-queue/digest-2026-06-14.md
```

**Recommended post-land sequence:**

1. `refresh_statecraft_archive_indices.py` (if batch land)
2. `check_statecraft_intake_daily_sync.py --day <pub_date>`
3. `statecraft_intake_queue.py --day <pub_date>`
4. **Author/guest shelf index** (when capture resolves to parsi / pape / crooke / ritter): `python scripts/shelf_index_from_capture.py --path <landed-file> --apply` then `python scripts/audit_statecraft_archive_index.py --shelf-index <slug>`
5. Daily synthesis when operator promotes

Digest template: [statecraft/notes/intake/intake-digest-TEMPLATE.md](../statecraft/notes/intake/intake-digest-TEMPLATE.md)

---

## Return path

- [intelligence-harness.md](intelligence-harness.md)
- [start-here.md — Operator ship loop](start-here.md#operator-ship-loop)
- [conductor SKILL — Kleiber compact menu](../.cursor/skills/conductor/SKILL.md) (default post-intake **A. Allegro**: sync + queue report)
- [coffee / menu-reference — Statecraft intake closeout](skill-work/work-coffee/menu-reference.md#statecraft-intake-closeout)
- [statecraft-source-intake skill](../.cursor/skills/statecraft-source-intake/SKILL.md)
- [runtime/artifacts/statecraft-intake-queue/README.md](../runtime/artifacts/statecraft-intake-queue/README.md)
