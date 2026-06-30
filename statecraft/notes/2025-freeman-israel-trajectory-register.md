---
note_id: 2025-freeman-israel-trajectory-register
note_type: synthesis
authority_level: shelf-native
source_basis: source-archive
essay_candidate: false
created_at: 2026-06-30
updated_at: 2026-06-30
archive_links:
  - source-archive/statecraft/2025-01-07/source-judging-freedom-amb-chas-freeman-is-israel-destroying-itself-2025-01-07.md
  - source-archive/statecraft/2025-01-14/source-judging-freedom-amb-chas-freeman-netanyahu-instigating-war-with-iran-2025-01-14.md
  - source-archive/statecraft/2025-01-17/source-dialogue-works-amb-chas-freeman-the-delusional-policies-driving-america-s-decline-2025-01-17.md
  - source-archive/statecraft/2025-01-21/source-judging-freedom-amb-chas-freeman-a-ceasefire-or-a-pause-2025-01-21.md
  - source-archive/statecraft/2025-10-07/source-judging-freedom-amb-chas-freeman-israel-near-collapse-2025-10-07.md
  - source-archive/statecraft/2025-11-21/source-dialogue-works-amb-chas-freeman-why-ukraine-and-israel-are-closer-to-a-dead-end-than-ever-2025-11-21.md
  - source-archive/statecraft/2026-06-06/source-glenn-diesen-chas-freeman-the-greater-israel-project-is-collapsing-2026-06-06.md
---
WORK only; not Record.

# Freeman — Israel self-destruction trajectory register

**Event:** `israel_self_destruction_trajectory` · **Auto-file SSOT** for body-hook calibration (not wire-verify).

**Purpose:** Curated hooks for machine scoring — Freeman **trajectory** claims under non-Israel episode titles. Human edits hooks in [`freeman-prediction-auto-file.json`](../data/freeman-prediction-auto-file.json); this note holds **exemplar captures** and merge rules.

## Hook table (tier-4 themes)

| Hook | Freeman move | Exemplar |
| --- | --- | --- |
| R-IL-1 | Delegitimization / lost moral ground / isolation | [2025-01-14 Netanyanu–Iran](../../source-archive/statecraft/2025-01-14/source-judging-freedom-amb-chas-freeman-netanyahu-instigating-war-with-iran-2025-01-14.md) |
| R-IL-2 | Long-term existence in jeopardy / won’t coexist | [2025-01-17 Delusional policies](../../source-archive/statecraft/2025-01-17/source-dialogue-works-amb-chas-freeman-the-delusional-policies-driving-america-s-decline-2025-01-17.md) |
| R-IL-2b | Force / hostage strategy failure (Jan pause) | [2025-01-21 Ceasefire or pause](../../source-archive/statecraft/2025-01-21/source-judging-freedom-amb-chas-freeman-a-ceasefire-or-a-pause-2025-01-21.md) |
| R-IL-3 | Pariah / internationally isolated | [2025-11-21 Dead end](../../source-archive/statecraft/2025-11-21/source-dialogue-works-amb-chas-freeman-why-ukraine-and-israel-are-closer-to-a-dead-end-than-ever-2025-11-21.md) |
| R-IL-4 | Greater Israel / expansionism in jeopardy | [2026-06-06 Greater Israel collapsing](../../source-archive/statecraft/2026-06-06/source-glenn-diesen-chas-freeman-the-greater-israel-project-is-collapsing-2026-06-06.md) |
| R-IL-5 | Strategic / military overextension | [2025-10-07 Near collapse](../../source-archive/statecraft/2025-10-07/source-judging-freedom-amb-chas-freeman-israel-near-collapse-2025-10-07.md) |

## Out of lane (auto-file exclude)

- Ukraine-primary captures without Israel trajectory sentence.
- Host-only intros (“Israel is nearing collapse” before Freeman speaks).
- Third-party quotes narrated by Freeman without endorsement.

## Pipeline

`auto_materialize_freeman_predictions.py` scores captures → writes notes when score ≥ event threshold. No per-row manifest audit.
