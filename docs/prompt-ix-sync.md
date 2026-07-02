# Prompt parity for museum knowledge section A / museum knowledge section B / museum knowledge section C (Voice and analyst)

**Purpose:** Operator-facing truth about how **Section IX** entries in [`archive/grace-mar-instance/museum-knowledge.md`](../archive/grace-mar-instance/self-knowledge.md) and [`self.md`](../archive/grace-mar-instance/self.md) relate to **[`archive/grace-mar-instance/bot/prompt.py`](../archive/grace-mar-instance/bot/prompt.py)** (`SYSTEM_PROMPT`, `ANALYST_PROMPT`), merge tooling, and harnessesâ€”especially **drift** when the knowledge split changes without matching prompt edits.

**Scope:** Documentation only. Does not change merge behavior or prompts.

**Related:** [instance doctrine â€” File Update Protocol and Prompt Architecture](../instance-doctrine.md) Â· [conceptual framework â€” companion self](conceptual-framework.md) Â· [governance unbundling](governance-unbundling.md)

---

## SSOT chain

| Layer | Role |
|-------|------|
| **`archive/grace-mar-instance/museum-knowledge.md`** | **Canonical Record** for merged museum knowledge section A (Knowledge) YAML list; `self.md` keeps the overview shell while museum knowledge section B/museum knowledge section C remain in `self.md` during the transition. |
| **`scripts/process_approved_candidates.py`** | On approved merge, updates `archive/grace-mar-instance/museum-knowledge.md`, evidence, and optionally **`archive/grace-mar-instance/bot/prompt.py`** (see below). `self.md` keeps the compact overview shell. |
| **`archive/grace-mar-instance/bot/prompt.py`** | **`SYSTEM_PROMPT`** â€” Voice emulation inline text; **`ANALYST_PROMPT`** â€” signal detection and **deduplication** against embedded IX snapshots. |
| **`python scripts/export_prp.py -o self-llm.txt`** | Compact PRP export; [instance doctrine](../instance-doctrine.md) expects refresh after SELF/prompt merges when output changes. |

Nothing in the Voice runtime reads `self.md` directly at inference time; the **prompt strings** are what the model sees unless RAG / lookup paths add context.

---

## Two prompt surfaces (both can drift)

1. **`SYSTEM_PROMPT`** â€” What the **Voice** uses in chat: narrative identity, **Curiosity** / **Personality** (and related) lines under **`## RECORD STATE`** in the current root layout.

2. **`ANALYST_PROMPT`** â€” Embeds **### museum knowledge section A / museum knowledge section B / museum knowledge section C** blocks so the analyst can **deduplicate** staging against â€œwhatâ€™s already in the profile.â€

These are **separate copies** of IX-shaped text. Updating **`archive/grace-mar-instance/museum-knowledge.md`** alone does **not** automatically refresh both unless the merge path or a manual edit brings them in sync.

**Honest default:** After museum knowledge section A merges that should affect dedup, verify **`ANALYST_PROMPT`**â€™s museum knowledge section A block matches **`archive/grace-mar-instance/museum-knowledge.md`** (or accept stale dedup until updated).

---

## `rebuild_ix` and `rebuild_observation_sections_from_self`

Merge logic in [`scripts/process_approved_candidates.py`](../scripts/process_approved_candidates.py): if a candidate carries **`prompt_merge_mode: rebuild_ix`**, the script calls **`rebuild_observation_sections_from_self`** from [`platform/src/grace_mar/merge/prompt_sync.py`](../platform/src/grace_mar/merge/prompt_sync.py).

That function **only replaces** spans bounded by these **exact** headers in **`SYSTEM_PROMPT`**:

- `## YOUR KNOWLEDGE (from observations)` â†’ next `## YOUR CURIOSITY (what catches your attention)`
- `## YOUR CURIOSITY (what catches your attention)` â†’ next `## YOUR PERSONALITY (observed)`
- `## YOUR PERSONALITY (observed)` â†’ next `## IMPORTANT CONSTRAINTS`

It rebuilds bullets from **`archive/grace-mar-instance/museum-knowledge.md`** YAML for museum knowledge section A `topic:` lines and from **`self.md`** YAML for museum knowledge section B `topic:` / museum knowledge section C `observation:` lines. If a header is **missing**, that span is **skipped** (no error).

**Current layout today:** [`archive/grace-mar-instance/bot/prompt.py`](../archive/grace-mar-instance/bot/prompt.py) uses **`## RECORD STATE`** with narrative **Curiosity** / **Personality** lists, **not** the `YOUR KNOWLEDGE` / `YOUR CURIOSITY` / `YOUR PERSONALITY` header triple above. So **`rebuild_ix` does not rewrite the current default `SYSTEM_PROMPT` layout** unless the prompt file is refactored to include those headers.

**Implication:** Do **not** assume a merge with `rebuild_ix` updated the visible Voice narrative unless youâ€™ve confirmed the header layout matches [`prompt_sync.py`](../platform/src/grace_mar/merge/prompt_sync.py).

**Legacy append path:** Candidates may use **`prompt_addition`** + **`prompt_section`** (`YOUR KNOWLEDGE` / `YOUR CURIOSITY` / `YOUR PERSONALITY`). [`insert_prompt_addition`](../platform/src/grace_mar/merge/prompt_sync.py) maps those to specific headers **or** falls back to older placeholder anchors (`## WHAT YOU LOVE`, `## HOW YOU HANDLE THINGS`). If neither matches, the addition may not applyâ€”another reason to **verify `prompt.py` by hand** after merges.

---

## Drift checklist (after museum knowledge section A / museum knowledge section B / museum knowledge section C-affecting merges)

Use this when you need **prompt parity** with the Record:

1. **`archive/grace-mar-instance/museum-knowledge.md`** â€” museum knowledge section A entries merged as intended (YAML ids, `topic:`, provenance).
2. **`self.md`** â€” compact overview shell remains in sync with the split; museum knowledge section B / museum knowledge section C entries stay aligned where present.
3. **`archive/grace-mar-instance/bot/prompt.py` â€” `SYSTEM_PROMPT`** â€” Narrative under **`## RECORD STATE`** (or your future section layout) reflects new curiosity/personality lines **if** the Voice should speak them.
4. **PRP** â€” Run `python scripts/export_prp.py -o self-llm.txt` (or repo default); commit if diff (per [instance doctrine](../instance-doctrine.md)).
5. **Harnesses (optional but relevant)** â€” Counterfactual / voice / **judgment probes** import prompt text from **`prompt.py`**; rerun when you care about regression signal after prompt edits.

---

## museum knowledge section B vs museum knowledge section C scope (identity vs WORK)

- **museum knowledge section B (Curiosity)** â€” Durable **topics and engagement signals** that belong in the companionâ€™s **documented** interests after gate approvalâ€”not every transient link or inbox item.
- **museum knowledge section C (Personality)** â€” **Observed patterns**, speech habits, **tensions** suitable for Voice texture and [judgment probes](../scripts/run_judgment_probes.py)â€”not a substitute for **operator cadence**, **skill-work** rituals, or **work-cadence** logs unless the companion explicitly treats those as **identity**.

**Work is adjacent:** [`conceptual-framework.md`](conceptual-framework.md) â€” WORK crosses into the Record **through the gate**. Pending governance discussions (e.g. moving **work rhythm** lines out of museum knowledge section C) live in **`recursion-gate.md`**; this doc does not resolve them.

---

## Probes and harnesses

[`scripts/run_judgment_probes.py`](../scripts/run_judgment_probes.py) imports **`SYSTEM_PROMPT`** from [`archive/grace-mar-instance/bot/prompt.py`](../archive/grace-mar-instance/bot/prompt.py). Scores reflect **embedded prompt text**, not a live read of the Record. If **`SYSTEM_PROMPT`** lags the relevant Record surfaces, probes measure **prompt**, not the Record aloneâ€”fix parity before inferring â€œRecord regression.â€

---

## Summarization tiers (token pressure)

When IX lists grow, [instance doctrine](../instance-doctrine.md) calls for **summarization tiers** on **`SYSTEM_PROMPT`**. Practically:

- **Compress** grouped facts into category lines without dropping **warrants** or **named tensions** where museum knowledge section C depends on them.
- **Avoid** duplicating the same bullet in **`SYSTEM_PROMPT`** and **`ANALYST_PROMPT`** if one side can stay shorter (analyst needs dedup fidelity; Voice needs readable voice).

---

## See also

- [instance-doctrine.md â€” Prompt Architecture](../instance-doctrine.md#prompt-architecture-botpromptpy)
- [AGENTS.md â€” Three-Dimension Mind Model](../AGENTS.md) (repository structure section)
- [platform/src/grace_mar/merge/prompt_sync.py](../platform/src/grace_mar/merge/prompt_sync.py) â€” rebuild and append helpers

