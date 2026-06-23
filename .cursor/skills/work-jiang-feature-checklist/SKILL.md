---
name: work-jiang-feature-checklist
description: "Structured workflow for Predictive History boundary maintenance and legacy Jiang-lane references inside strategy-codex: branch hygiene, scope boundaries, verify commands, and commit granularity aligned to plan phases. Use when starting or closing a Jiang-related boundary thread, touching scripts/work_jiang guardrails, or reviewing frozen local PH residue."
preferred_activation: jiang check
activation: jiang check
category: domain-pack
status: active
scope_class: repo-governed
---
# work-jiang feature checklist

This skill is now for **boundary maintenance, review, and historical reference only** inside `strategy-codex`. Canonical writable Predictive History work belongs in [`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history); local `codex/predictive-history/` paths are frozen migration residue unless the task is explicitly about docs, validators, or legacy-reference inspection.

**Preferred activation (operator):** say the exact phrase **`jiang check`**.

Operator- and agent-facing checklist so multi-step Jiang work stays reviewable and doesn't fight context limits or a noisy working tree.

## Before implementation

Boundary note: if the requested outcome is new or regenerated Predictive History corpus/manuscript content, stop and move that work to the external canonical repo instead of continuing inside `strategy-codex`.

0. **Large handoff / artifact** — Consider compressing into `codex/predictive-history/compressions/` with `python3 scripts/jiang-compress.py -u <fork-id>` ([COMPRESSION-ENGINE.md](../../codex/predictive-history/COMPRESSION-ENGINE.md)); optional gate stub only if Record merge is intended.
1. **Branch and tree** — Prefer a dedicated branch. Glance at `git status`: unrelated untracked paths (`claims/`, `evidence-packs/`, etc.) make review harder; stash, commit, exclude locally, or isolate before stacking new changes.
2. **Scope** — Confirm lane: **Geo-Strategy** (`lectures/geo-strategy-*.md`, not other lecture lanes unless the task says so). If the thread also touches Record/pipeline/Voice, run harness warmup per repo rules and paste output once.
3. **Plan alignment** — If work maps to phased PRs (quotes → counter-readings → chronology → validator/CI), name commits or branches to those phases so bisect stays cheap.
4. **Lane** — Explicit **Ship** (implement, wire CI) vs **Think** (design only); mixed threads should state which.
5. **Membrane** — Canonical boundary rules live in `codex/predictive-history/README.md` § **Boundaries (membrane)** — link to it instead of duplicating policy in session replies. Validators are enforcement; see § Guardrails below.

## Canonical verify block (repo root)

Use this block only for explicit legacy-tooling or boundary-maintenance tasks. It is no longer the default path for day-to-day Predictive History production.

After editing work-jiang metadata, scripts, or CI:

```bash
python3 scripts/work_jiang/build_source_registry.py
python3 scripts/work_jiang/link_supporting_registries.py
python3 scripts/work_jiang/extract_concept_mentions.py
python3 scripts/work_jiang/render_concept_dictionary.py
python3 scripts/work_jiang/link_claims_to_thesis.py
python3 scripts/work_jiang/render_claims_overview.py
python3 scripts/work_jiang/render_book_architecture.py
python3 scripts/work_jiang/render_thesis_map.py
python3 scripts/work_jiang/render_chapter_queue.py
python3 scripts/work_jiang/build_all_evidence_packs.py
python3 scripts/work_jiang/render_status_dashboard.py
python3 scripts/work_jiang/extract_quote_candidates.py
python3 scripts/work_jiang/render_quote_bank.py
python3 scripts/work_jiang/link_quotes_to_chapters.py
python3 scripts/work_jiang/render_counter_readings.py
python3 scripts/work_jiang/link_counter_readings.py
python3 scripts/work_jiang/render_intellectual_chronology.py
python3 scripts/work_jiang/validate_work_jiang.py --require-analysis-frontmatter
python3 scripts/work_jiang/validate_argument_layer.py
python3 scripts/work_jiang/validate_comparative_layer.py
```

Trim the block if the task truly doesn't touch comparative layer or upstream generators; otherwise prefer the full sequence so layers don't drift.

## Lecture transcript ingest (optional step)

This section is historical-reference guidance only. Normal new lecture ingest belongs in the external Predictive History repo, not in the frozen local PH tree here.

When adding or updating `lectures/*.md` with pasted ASR, run the orthography pass (dry-run first, then `--write`): `python3 scripts/work_jiang/normalize_lecture_transcript_asr.py codex/predictive-history/lectures/<slug>.md`. Tables live in `scripts/work_jiang/asr_transcript_replacements.py`; workflow detail in `codex/predictive-history/WORKFLOW-transcripts.md` (Phase B §5). **Volume IV** uses `game-theory-NN-*.md` and `--series game-theory` (or auto from filename); `GAME_THEORY_REPLACEMENTS` may start empty. After raw YouTube captions exist under `predictive-history/transcripts/`, optional: `python3 scripts/work_jiang/sync_verbatim_transcripts.py --dry-run` then `--write` to refresh `verbatim-transcripts/` for diffing (see `verbatim-transcripts/README.md`). Targeted ASR audit: `codex/predictive-history/ASR-AUDIT-LOG.md` and `python3 scripts/work_jiang/check_asr_audit_preconditions.py`.

## skill-jiang blind forward chain (optional)

True blind simulation: `python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle --prefix-end K -o …` then predict from that bundle only; `reveal --episode K+1` after the prediction file exists. See [skill-jiang](../skill-jiang/SKILL.md) § Mechanical blind runs.

## Data model reminders

- **`metadata/quote-candidates.yaml`** — Geo-Strategy lectures + all `analysis/*.md`; regenerated by `extract_quote_candidates.py` (scored, capped). Pass `--geo-only` to refresh only this file.
- **`metadata/quote-candidates-secret-history.yaml`** / **`metadata/quote-candidates-civilization.yaml`** — Same script; series-specific keyword scoring so Vol. III / II candidates are not drowned by geo bias.
- **`metadata/quotes.yaml`** — Curated source of truth; optional bootstrap via `bootstrap_quotes_from_candidates.py` (default candidates file: geo+analysis); use `--candidates` for secret-history or civilization YAML when merging quotes for other volumes.
- **Chronology** — `metadata/chronology.yaml` is hand-maintained; partition `geo-01` … `geo-12` exactly once; IDs must match `concepts.yaml` and `claims/registry/claims.jsonl`.

## After implementation

If the task changed boundary doctrine or local freeze messaging, update [docs/predictive-history-external-boundary.md](../../docs/predictive-history-external-boundary.md) before treating the local PH README files as navigation follow-ons.

1. **Diff surface** — `git diff --stat` (or a short file list) before commit; keep unrelated files out of the same commit when possible.
2. **Docs** — If production path changed, update `codex/predictive-history/README.md`; optional cross-links in `codex/predictive-history/README-operator.md` for operator navigation.
3. **CI** — `.github/workflows/work-jiang.yml` should run generators before `validate_*` in dependency order (see workflow file).

## Long threads / handoffs

- Split very large builds across **two sessions** or checkpoint ("next message: run validators only") to reduce summarization loss.
- End-of-session: state **what landed**, **what's uncommitted**, and **one re-entry command** (often the verify block above).

## Guardrails

- Do not treat `quote-candidates*.yaml` as polished quotes for prose.
- Do not restart local PH production inside `strategy-codex`; create, update, and regenerate canonical PH material in the external repo instead.
- Do not merge Record/profile from this lane without the gated pipeline; work-jiang is operator research unless explicitly merged elsewhere.
- Full **may / must not** table and warmup rule: `codex/predictive-history/README.md` § Boundaries (membrane).

## Related

- [COMPRESSION-ENGINE.md](../../codex/predictive-history/COMPRESSION-ENGINE.md) — Jiang Compression Engine v1 (`scripts/jiang-compress.py`)
- `codex/predictive-history/README.md` — § Boundaries (membrane); production pipeline; comparative layer
- `docs/audit-boundary-grace-mar-companion-self.md` — grace-mar · companion-self (instance-wide; not Jiang data rules)
- `scripts/work_jiang/validate_comparative_layer.py` — Gates for high-priority analysis chapters and chronology

