# strategy-codex — status
<!-- word_count: 362 -->

> Operator-maintained. Run from repo root; not auto-generated.

| Field | Value |
|-------|--------|
| **Project status** | `active` |
| **Active chapter** | `2026-04` (dense spine) · **`2026-06` bootstrapped** ([`chapters/2026/2026-06/days.md`](chapters/2026/2026-06/days.md)) |
| **Last substantive entry** | `2026-06-21` — **`## 2026-06-21`** in [`chapters/2026/2026-06/days.md`](chapters/2026/2026-06/days.md#2026-06-21): Ritter Substack *[A Trail of Tears](https://scottritter.substack.com/p/a-trail-of-tears)* fold + **Starobilsk May 22 Ukrainian terrorist attack — `verify:tier-A` operator-confirmed** (Rubicon-HQ allegation **contradicted**); archive [`source-ritter-a-trail-of-tears-2026-06-19.md`](../source-archive/statecraft/2026-06-19/source-ritter-a-trail-of-tears-2026-06-19.md). Prior: **`## 2026-04-19`** in [`chapters/2026-04/days.md`](chapters/2026/2026-04/days.md#2026-04-19). |
| **Prepared stub** | _Optional_ — only if you use calendar stubs; otherwise capture in [daily-strategy-inbox.md](daily-strategy-inbox.md) and **weave** when you run **`strategy`** / explicit **`weave`** / **`fold`** (legacy) |
| **Daily inbox** | [daily-strategy-inbox.md](daily-strategy-inbox.md) — **SSOT** (cadence + paste-ready lines); weave/prune → [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Daily strategy inbox* |
| **Expert predictions ledger** | [strategy-expert-predictions.md](strategy-expert-predictions.md) — optional **`pred_id`** adjudication rows + **2026** `topic_slug` registry (WORK; not Record) |
| **Next stitch** | Optional: roll month-end summary into [STRATEGY.md](../STRATEGY.md) §IV |
| **Operator prefs** | [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) |
| **Retro Q1 syntheses** | `2026-01`–`2026-03` — meta-led chapter narratives ([2026-01/meta.md](chapters/2026-01/meta.md), [2026-02/meta.md](chapters/2026-02/meta.md), [2026-03/meta.md](chapters/2026-03/meta.md)); episodic `days.md` only |

## Seam / weave observability (optional)

| Artifact | Role |
|----------|------|
| [gamification-metrics.md](gamification-metrics.md) | Guardrails + meaning of `weave_count` / `seam_integrity` / checklist flags in the legacy on-disk index (legacy page index) v4+ |
| [`python3 ../../../../scripts/knot_seam_metrics.py`](../scripts/knot_seam_metrics.py) | Read-only: outgoing links to other legacy chapter markdown files vs optional `weave_count` |
| [forecast-watch-log.md](forecast-watch-log.md) | Monthly / episodic falsifiable metrics (preferred to raw counts) |

## Expert-thread month segments (skill-strategy pointer)

Calendar **`## YYYY-MM`** blocks in **`strategy-expert-*-thread.md`** (inside the **journal layer**) follow a **parse contract** (terminators, prose minimum, scripts). For **2026**, **Segment 1–4** = Jan–Apr month headings — not the machine layer. Spec: [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Expert-thread month segments (parse contract + scripts)](STRATEGY-NOTEBOOK-ARCHITECTURE.md#expert-thread-month-segments). Validate: `python3 scripts/validate_strategy_expert_threads.py`.

## Next actions

1. When adding new work, append a **`## YYYY-MM-DD`** block (or an episodic `##` section) at the bottom of [`chapters/2026-04/days.md`](chapters/2026/2026-04/days.md) **if** that helps your continuity—thin or pointer-only is fine; primary work may live in expert pages + inbox (see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Daily length and prose*). Bump **Last substantive entry** here when you touch the notebook spine.
2. Refresh this file when the active month changes or after notable closes.


