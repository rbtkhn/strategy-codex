# Predictive History

Public intake command: `predictive-history`. Legacy `work-jiang` remains as a compatibility alias and internal wrapper name.

> [!IMPORTANT]
> **Freeze status:** Predictive History canonical edits now belong in **[`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history)**. The `codex/predictive-history/` tree inside `strategy-codex` is **frozen migration residue / historical reference only** during episode-by-episode migration. Do not treat it as a live writable lane. Boundary doctrine: [docs/predictive-history-external-boundary.md](../../docs/predictive-history-external-boundary.md).

Operator project — **Jiang** (separate from SKILLS). See [skill-think](skill-think.md), [skill-write](skill-write.md), [work-alpha-school](work-alpha-school.md).

## Purpose

This file now documents the **local review/stewardship boundary** around a frozen historical PH tree. The canonical multivolume build has moved to the external repo; `strategy-codex` may only observe, review, and critique migrated PH work.

Historical purpose of this local tree was to deliver a multivolume **Predictive History** book/site corpus. That canonical build now lives externally; this repo may only observe, review, and critique migrated PH work.

**Canonical library index:** The book is catalogued in [self-library](self-library.md) as **LIB-0149** (SELF-LIBRARY is reference-facing; the local `codex/predictive-history/` tree is now frozen reference residue rather than the working manuscript).

**Design lens:** Alpha-style mastery vocabulary (gates, “no Swiss cheese,” 2-hour pacing) mapped to this fork’s gate and WORK tools — [alpha-mastery-adaptation.md](../../docs/alpha-mastery-adaptation.md).

**Authorized sources (operator list):** [work-jiang-sources.md](./work-jiang-sources.md) — convention: [work-modules-sources-principle.md](../../docs/skill-work/work-modules-sources-principle.md).

**Cursor skill — forward lecture chain:** [skill-jiang.md](./skill-jiang.md) (predict next episode from prefix only; Volume IV bake-off log under `prediction-tracking/`).

**Publishing (historical local note):** [PUBLISHING.md](./book/PUBLISHING.md) documents the earlier single-repo local model; it is no longer the canonical writable workflow for current PH work.

**Method (operator work, not Voice knowledge until merged through the gate):**

1. **Lecture transcripts** — primary text: systematic capture and close reading of his talks (e.g. channel pulls under `research/external/youtube-channels/predictive-history/`), tagged and excerpted for themes, definitions, and internal consistency.
2. **[CIV-MEM](../../docs/skill-work/work-civ-mem/README.md)** — civilizational / strategic / governance vocabulary and frames from the civilization_memory stewardship lane: use as an **analytic lattice** and **reference spine** (conditions, seams, multi-perspective structure) to organize and stress-test philosophical claims without collapsing them into politics alone.
3. **Current-events scans** — periodic passes (news, briefs, operator skills such as pulse/search workflows) to **ground** the philosophy: where the abstract system meets concrete episodes, and what would need to be said in a given moment.
4. **Compressions** — Historical local mechanism only. Do not emit new canonical PH packs into `codex/predictive-history/compressions/` from this repo.

Nothing in this file is Record truth for the Voice until merged through the gated pipeline. Human-gated.

**Membrane (normative):** [codex/predictive-history/README.md § Boundaries](./README.md#boundaries-membrane) — research corpus vs Record, candidates vs quotes, validators as gate.

**Repo CI:** Local CI now protects the Predictive History freeze boundary rather than rebuilding PH here. When pasting into `recursion-gate.md`, use the canonical **`### CANDIDATE-*`** block shape (see [work-jiang lane + gate CI](./LANE-CI.md)).

---

## Context objectives

Current objective is boundary-safe review, not local PH production. Use this repo to critique externally migrated material, preserve migration traceability, and keep strategy-facing Jiang routing legible without reviving the old writable lane.

- Maintain a **canonical transcript set** and a working **outline / thesis map** for the book or site.
- Run **civ-mem-informed analysis** on clusters of transcript material (themes, tensions, dependencies).
- Run **current-events tie-ins** as optional chapters or “applications” sections — never shipped without explicit approval.
- Separate **exposition** (what Jiang’s philosophy holds) from **analysis** (how it compares, where it strains, what it predicts).

---

## Instance work context (YAML)

Machine-oriented snapshot for scripts and agents — [skills-modularity](../../docs/skills-modularity.md) §2a (*Instance work context*). Not Record. Optional: `python3 scripts/work_jiang/update_work_jiang_lane.py --write` refreshes `status` from book metadata.

<!-- work_jiang.context.yaml WORK_JIANG_CONTEXT_V1 -->
```yaml
status: OUTLINE_ACTIVE
edge: "Philosophy book + site; transcript-driven; civ-mem lattice; current-events grounding"
gaps: []
notes: "See codex/predictive-history/STATUS.md and BOOK-ARCHITECTURE.md for live production state. Geo-Strategy series resumed 2026-03-23; geo-13+ pending ingest."
```
<!-- /work_jiang.context.yaml WORK_JIANG_CONTEXT_V1 -->

---

## WORK GOALS

Objectives for this lane. Gated; evidence-linked when captured.

```yaml
work_goals:
  near_term: []
  horizon:
    - "Published book and/or website articulating Jiang's philosophy with transcript-backed analysis"
  source: null
```

---

## LIFE MISSION REF

Life mission lives in SELF (identity, values). WORK goals may align when this lane touches the companion.

```yaml
life_mission_ref: "self.md § VI VALUES (life_mission)"
```

---

## Operator schedule (Jiang lane)

- **Lecture series order (Predictive History / book work):** (1) **Geo-Strategy** — curated in `codex/predictive-history/lectures/` (`geo-strategy-*.md`). (2) **Civilization** — second series; **transcript intake in progress** — add curated files as `civilization-*.md`, register `civ-*` sources in `metadata/sources.yaml`, same pipeline as Geo-Strategy ([WORKFLOW-transcripts.md](./WORKFLOW-transcripts.md) § Multi-series; channel pulls under `research/external/youtube-channels/predictive-history/`).

---

## RESEARCH / ARTIFACTS

Repo-local material (operator research; not Voice knowledge until merged):

- [work-jiang (research)](./README.md) — curated lecture notes + transcripts
 - [Transcript intake & analysis workflow](./WORKFLOW-transcripts.md) — acquire, normalize, structured extraction, CIV-MEM passes, bridge fields, memo template
  - [Influence tracking](./influence-tracking/README.md) — longitudinal views/likes/comment counts via `scripts/snapshot_youtube_video_metrics.py` + optional monthly notes
  - [Prediction tracking](./prediction-tracking/README.md) — forecast-like claims in `registry/predictions.jsonl`; resolve vs dated evidence (orthogonal to “influence”); structural next-lecture chain + **skill-jiang** pointer in same README and [skill-jiang.md](./skill-jiang.md)
  - [Divergence tracking](./divergence-tracking/README.md) — where claims differ from **named** mainstream/consensus views; `registry/divergences.jsonl`
  - Examples: [Geo-Strategy #1 — Iran strategy matrix (2024-04-24)](./lectures/geo-strategy-01-iran-strategy-matrix-2024-04-24.md); [#2 — Christian Zionism & Middle East](./lectures/geo-strategy-02-christian-zionism-middle-east-conflict.md); [#3 — Empire & financialization](./lectures/geo-strategy-03-how-empire-is-destroying-america.md); [#4 — Saudi Arabia vs Iran](./lectures/geo-strategy-04-saudi-arabia-trump-card-against-iran.md); [#5 — Trump 2024 / Haley VP hypothesis](./lectures/geo-strategy-05-why-trump-will-win-nikki-haley-vp.md); [#6 — Imperial hubris & shock-and-awe](./lectures/geo-strategy-06-americas-imperial-hubris.md); [#7 — Raisi helicopter / IRGC scenario](./lectures/geo-strategy-07-who-killed-iranian-president-ebrahim-raisi.md); [#8 — Iran trap / invasion scenario](./lectures/geo-strategy-08-the-iran-trap.md); [#9 — Putin / putinism & consumerism thesis](./lectures/geo-strategy-09-putins-war-for-the-soul-of-russia.md); [#10 — Putin strategic imagination / Stalin game-theory](./lectures/geo-strategy-10-putins-strategic-imagination.md); [#11 — Second American Civil War thesis](./lectures/geo-strategy-11-the-second-american-civil-war.md); [#12 — Psychohistory / hope & modeling (END)](./lectures/geo-strategy-12-psychohistory-the-science-of-imagining-the-future.md)
  - Book/site production: [STATUS](./STATUS.md), [BOOK-ARCHITECTURE](./BOOK-ARCHITECTURE.md), [THESIS-MAP](./THESIS-MAP.md), [CHAPTER-QUEUE](./CHAPTER-QUEUE.md), [CONCEPT-DICTIONARY](./CONCEPT-DICTIONARY.md), [CLAIMS-OVERVIEW](./CLAIMS-OVERVIEW.md), [evidence-packs](./evidence-packs/); comparative layer: [QUOTE-BANK](./QUOTE-BANK.md), [COUNTER-READINGS](./COUNTER-READINGS.md), [INTELLECTUAL-CHRONOLOGY](./INTELLECTUAL-CHRONOLOGY.md)
- `research/external/youtube-channels/predictive-history/` — machine transcripts + `index.json` for channel pulls
- [work-civ-mem](../../docs/skill-work/work-civ-mem/README.md) — stewardship surface for civilization_memory; use for analytic frames and CIV-MEM ↔ text crosswalks
  - [CIV-MEM reference spine (work-jiang)](./CIV-MEM-LENS.md) — lattice mapped to lectures + registries; use bridge fields in analysis sidecars; CMC as reference, not Record
