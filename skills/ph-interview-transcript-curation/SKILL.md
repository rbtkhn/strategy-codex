---
name: ph-interview-transcript-curation
description: "Pass-2 curation for Predictive History public interview transcripts — section rails, speaker/ASR repair, frontmatter, validate, PH-TRANSCRIPT-EDIT ship. Canonical repo: predictive-history interviews/ packets. Not statecraft source-clean."
preferred_activation: PH transcript pass
activation: PH transcript pass
portable: true
version: 0.1.0
category: truth-pipeline
status: active
scope_class: repo-governed
tags:
  - operator
  - predictive-history
  - transcript
  - interviews
portable_source: skills/ph-interview-transcript-curation/SKILL.md
synced_by: sync_portable_skills.py
---
# PH interview transcript curation

**Preferred activation:** **`PH transcript pass`** · **`interview section pass`** · **`PH-TRANSCRIPT-EDIT`**

**Canonical edit surface:** [`predictive-history`](https://github.com/rbtkhn/predictive-history) repo — `interviews/interview-YYYY-MM-DD-{host-slug}/`. Edit from strategy-codex when operator grants PH repo access; do **not** edit `public/predictive-history/` mirror by hand (refresh via `sync_predictive_history_mirror.py` after push).

**Exemplar:** Tucker vi-11 — commit `d475974` · packet [`interview-2026-03-20-tucker-carlson`](https://github.com/rbtkhn/predictive-history/tree/main/interviews/interview-2026-03-20-tucker-carlson).

## Use this skill when

- A promoted PH **interview** transcript needs **pass 2**: topic section rails, speaker-label repair, ASR/toponym cleanup, duplicate-line removal
- Operator names an interview id (`vi-11`, `interview-2026-03-20-tucker-carlson`) or asks to repeat the Tucker curation pattern
- Transcript is already public under `interviews/` with `## Part I: Full transcript` (workshop or external promote)

## Do not use when

- Source is **statecraft archive** (`source-archive/statecraft/**/source-*.md`) — use [`source-clean`](../source-clean/SKILL.md)
- Job is **first promote / external intake** (card, manifest, intake script) — separate promote slice; see CURSOR_APPENDIX § External intake sibling
- Job is commentary, essay prose, or YouTube public copy — other skills
- Operator wants **audio-verified verbatim** — this skill is **transcript-logic only** unless operator supplies audio or caption SSOT

## Scope gate

| In scope | Out of scope |
|----------|--------------|
| `{slug}.md` transcript body + YAML frontmatter | Commentary canvas rewrites |
| Packet `README.md` pass note + unresolved entities | Card/manifest unless validate regenerates indexes |
| Index refresh via `civ_ph validate` (auto) | `codex/predictive-history/` frozen workshop |

## Default execution order

1. **Read first half** — match existing speaker-label pattern (`**Host:**` / `**Guest:**` or interview-specific names), block spacing, sponsor/read boundaries. Do not reformat the clean prefix blindly.
2. **Assess section pivots** — under `## Part I: Full transcript`, plan `### Title Case` topic headings at topic changes. Count is **per interview** (Tucker = 7 sections; not a fixed template).
3. **Speaker + ASR pass** — repair mis-attributed lines, collapsed speakers, obvious ASR (places, names, acronyms). Preserve load-bearing quotes. List **unresolved** names in README (exemplar: "John" at Christians United for Israel — likely Hagee, not pinned without audio).
4. **Dedup** — remove duplicate closing questions or repeated sponsor blocks when transcript-logic shows a clear duplicate.
5. **Frontmatter** — set or update:
   - `transcript_curation: curated_sectioned`
   - `transcript_fidelity: curated_pass`
   - `fidelity_reviewed_at: YYYY-MM-DD` (session date)
   - leave `transcript_status`, `review_status`, workshop ids unchanged unless operator directs
6. **README provenance** — under **Review Status**, add **Transcript pass N (YYYY-MM-DD):** one line on sections + repair scope + unresolved entities.
7. **Validate** — from PH repo root:
   ```bash
   PYTHONPATH=src python -m civ_ph.cli validate
   python -m pytest -q
   ```
8. **Commit + push** — message prefix **`PH-TRANSCRIPT-EDIT:`** · inline git identity if needed (`git -c user.name=… -c user.email=… commit` — never `git commit -c … -m …` on Windows Git).
9. **Mirror (optional)** — from strategy-codex: `python scripts/sync_predictive_history_mirror.py`; commit with `[predictive-history-sync]` when operator asks **EXECUTE** on mirror.

## Section heading rules

- **Title Case** ASCII headings (exemplar: `### Iran Attrition and Global Stakes`, `### US Off-Ramp — Petrodollar and China`)
- Insert **under** `## Part I: Full transcript`, **above** the first line of each topic block
- Headings describe **topic pivot**, not timestamps
- Do not add sections outside Part I unless packet structure already uses other parts

## ASR / entity discipline

- **Transcript-logic only** — infer speakers from turn-taking and host/guest names; do not claim audio verification
- When editing from strategy-codex, apply operator place-name policy in **framing** around quotes ([Kiev/Kharkov rule](../../.cursor/rules/strategy-codex-kiev-spelling.mdc)) — preserve source spelling inside load-bearing quotes when load-bearing
- Do not rewrite argument, add facts, or smooth into editorial essay prose

## Windows harness

- One **Shell** per turn; one **StrReplace/Write path** per file per turn when possible
- Bounded **Read** on known interview paths — no repo-wide grep storms
- After hang: Read/Write only until patch lands ([agent-tool-latency-discipline](../../.cursor/rules/agent-tool-latency-discipline.mdc))

## Verification / Proof Standard

Do not call this complete unless:

- interview **source_id** and packet path are named
- section headings listed (count + names)
- speaker/ASR scope stated (which line range or block)
- unresolved entities listed in README or reply
- `validate` exit + card count reported
- `pytest` exit reported
- commit hash + push status (or explicit defer)
- skipped steps marked with reason

Evidence to report:

- files touched
- section heading list
- validate/pytest commands and exit codes
- commit message and hash
- mirror sync receipt if run

If verification cannot be completed:

- state what was not verified
- stop before push or mirror commit
- return bounded partial for operator review

## Related skills

| Task | Skill |
|------|--------|
| Statecraft archive ASR | [`source-clean`](../source-clean/SKILL.md) |
| PH external interview promote | `scripts/intake_interview_external.py` (PH repo) — sibling workflow |
| Mirror refresh | `scripts/sync_predictive_history_mirror.py` (strategy-codex) |
| Skill capture | [`extract-skill-from-session`](../extract-skill-from-session/SKILL.md) |
