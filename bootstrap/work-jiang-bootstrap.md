# WORK-JIANG BOOTSTRAP

Session bootstrap for continuing **work-jiang** (operator research lane: Jiang book/site) in a **new agent conversation**.

**Canonical membrane:** [codex/predictive-history/README.md Â§ Boundaries (membrane)](../codex/predictive-history/README.md#boundaries-membrane) â€” research vs Record, candidates vs quotes, validators as gate.

**Skill:** [.cursor/skills/work-jiang-feature-checklist/SKILL.md](../.cursor/skills/work-jiang-feature-checklist/SKILL.md) â€” branch hygiene, verify block, CI, data model.

---

## Paste into message 1 (clean context)

State **Ship** vs **Think** and the concrete goal (e.g. â€œextend chronology for geo-08â€, â€œfix validate_comparative_layer failureâ€).

If the thread may touch **``** (SELF, RECURSION-GATE, pipeline, `codex/predictive-history/README-operator.md` beyond navigation), also run and paste:

```bash
python3 scripts/harness_warmup.py -u grace-mar --compact
```

Pure edits under `codex/predictive-history/` and `scripts/work_jiang/` alone usually do not require warmup; use it when gate or Record state matters.

---

## Read before edits (order)

| # | File | Why |
|---|------|-----|
| 1 | [codex/predictive-history/README.md](../codex/predictive-history/README.md) | Production pipeline, Â§ Boundaries, comparative vs argument layer |
| 2 | [.cursor/skills/work-jiang-feature-checklist/SKILL.md](../.cursor/skills/work-jiang-feature-checklist/SKILL.md) | Verify block, phased commits, guardrails |
| 3 | [codex/predictive-history/README-operator.md](../codex/predictive-history/README-operator.md) | Operator purpose; WORK container; links into research tree |
| 4 | [AGENTS.md](../AGENTS.md) | If merging Record: sovereign merge, no direct SELF/EVIDENCE without approval + script |
| 5 | [codex/predictive-history/volume-ii-book-track-conventions.md](../codex/predictive-history/volume-ii-book-track-conventions.md) | When editing **Volume II** (`civ-chNN`, `BOOK-ARCHITECTURE-VOLUME-II.md`, `CHAPTER-QUEUE-VOLUME-II.md`) |
| 6 | [codex/predictive-history/volume-iii-book-track-conventions.md](../codex/predictive-history/volume-iii-book-track-conventions.md) | When editing **Volume III** (`sh-chNN`, `BOOK-ARCHITECTURE-VOLUME-III.md`, `CHAPTER-QUEUE-VOLUME-III.md`) |

Skim as needed: `.github/workflows/work-jiang.yml` (generator order), `codex/predictive-history/WORKFLOW-transcripts.md` (intake).

---

## Scope reminder

- **Lane:** **Geo-Strategy** â€” `lectures/geo-strategy-*.md` (Volume I `ch01` â€¦); **Civilization** â€” `lectures/civilization-*.md` + `civ-*` + Volume II (`volume_2_civilization`); **Secret History** â€” `lectures/secret-history-*.md` + `sh-*` + Volume III (`volume_3_secret_history`, `sh-ch01` â€¦). Default book tranche is Volume I unless the task says otherwise.
- **work-jiang is operator research** until content is merged through the gated pipeline into the Record; do not treat corpus as Voice knowledge.

---

## Canonical verify block (repo root)

After metadata, generator, or validator script changes, run the full block from the **work-jiang feature checklist** skill (same as [README production pipeline](../codex/predictive-history/README.md#production-pipeline-book--site) through `validate_comparative_layer.py`). Trim only if the task truly skips comparative layer; otherwise run end-to-end to avoid drift.

Minimum when you touched **claims/concepts/packs only:**

```bash
python3 scripts/work_jiang/validate_work_jiang.py --require-analysis-frontmatter
python3 scripts/work_jiang/validate_argument_layer.py
```

Add comparative validators when quotes, counter-readings, or chronology YAML changed.

---

## Non-negotiables

- Do **not** treat `metadata/quote-candidates.yaml` as polished quotations.
- Do **not** merge into `self.md`, `self-evidence.md`, or `bot/prompt.py` without companion approval and `process_approved_candidates.py` (see AGENTS.md).
- Prefer a **dedicated branch**; keep unrelated files out of the same commit when possible.

---

## End of session

- Short note: **what landed**, **what is uncommitted**, **one re-entry command** (often the verify block).
- If production paths or membrane rules changed, update `codex/predictive-history/README.md` Â§ Boundaries or pipeline; optional touch `docs/development-handoff.md` only if engineering-wide state shifted.

---

## Related

- [docs/audit-boundary-grace-mar-companion-self.md](../docs/audit-boundary-grace-mar-companion-self.md) â€” instance-wide grace-mar Â· template boundaries (not Jiang data rules)
- [bootstrap/grace-mar-bootstrap.md](grace-mar-bootstrap.md) â€” full-repo / work-dev default session

