WORK only; not Record.

# News-verify ↔ synthesis gate

**Invariant:** Full **daily synthesis** on calendar day **D** requires `statecraft/notes/wire/D-news-verify-matrix.md` **or** an explicit waiver in the daily header (`verify_gate: waived` + one-line reason).

The **news-verify matrix** is the **daily tier-3 fact ledger** (operator-facing: **daily news-verify**). **Daily synthesis** is interpretation that **cites** it — synthesis does **not** replace the matrix.

## Two artifacts, one pipeline

```text
source-archive (verbatim)
       ↓
news-verify batch  →  news-verify-matrix  (tier 3 SSOT)
       ↓
state synthesis    →  synthesis/day       (tier 4 interpretation)
       ↓
optional: capture verify: tails (J-row pointers, not duplicate tables)
```

| Artifact | Path | Authority |
| --- | --- | --- |
| **Daily news-verify** | `statecraft/notes/wire/YYYY-MM-DD-news-verify-matrix.md` | Tier-3 hooks, verdicts, lane sweep, cites |
| **Daily synthesis** | `statecraft/synthesis/day/YYYY-MM-DD.md` | Dominant object, themes, Judgment — **J-ID citations** for tier-3 claims |
| **Per-capture receipts** | `source-archive/.../source-*.md` YAML | Optional; prefer `verify_matrix_ref: J{D}-n` over duplicating full hook tables |

Do **not** add a third parallel “daily fact check” doc unless it is a rename/alias of the matrix.

## When the gate applies

**Gate ON** (matrix required before **full** synthesis):

- `archive_count ≥ 3` on day **D**, **and**
- any of: MOU/war week, same-week breaking seam, load-bearing wire hooks in batch, operator said **`state synthesis`** / pre-EOD compose

**Gate OFF or waiver allowed:**

- **Register-only** daily (`Status: register`) — inventory + object name; link matrix as **OPEN** or carry prior-day matrix with explicit stale note
- **Peripheral month** — adjacent-only captures; no tier-3 hooks promoted
- **Historical** archive backfill
- Operator sets **`verify_gate: waived`** + reason in synthesis header (e.g. `verify_gate: waived — intake-only replay, no new hooks`)

**Sub-hook Think** does **not** satisfy the gate.

## Minimum matrix spec

Exemplar: [2026-06-19-news-verify-matrix.md](../notes/wire/2026-06-19-news-verify-matrix.md).

1. Header — parent daily link (stub OK until synthesis lands), archive day-index, prior matrix cross-ref
2. **Mode** — batch · hook count · **CIV-STATE 5/5** or honest combatant+mesh
3. **Lane sweep table** — cite or `verify:*-lane-absent`
4. **Hook table** — `J{D}-{n}` · claim · lane · lang · verdict · cite
5. **Capture map** (optional) — which sources spoke which hooks
6. **Open / escalate** — `fa` pulls, developing-story caveats

**Confidence rule:** synthesis must **not** upgrade matrix verdicts (e.g. contested → supported) without a new verify pass.

## Synthesis contract (gate consumer)

When gate is **ON**, full synthesis **must**:

1. Link matrix in **Source Base** / prior-day baseline
2. Include **News-verify (D)** block — hook-cluster summary + matrix link
3. Cite **`J{D}-*`** in Judgment / falsifiers for tier-3 claims
4. Fence tier-4 in themes; no wire-grade rows without matrix ID or capture `verify:`
5. If matrix missing: **stop** or emit **register-only** with `verify_matrix: OPEN` — not a faux full synthesis

**Validator follow-up (future):** `validate_statecraft_synthesis.py` — warn/fail when daily lacks matrix link and no `verify_gate: waived`.

## Workflow sequence

```text
intake batch → archive-checkpoint
            → news verify batch → WRITE matrix (Ship default on gate weeks)
            → state synthesis (full)
            → optional: Ship capture verify: pointers
            → commit slice
```

**Default after batch verify on gate weeks:** Ship matrix before synthesis.

## Carry-forward (register tier)

Register-tier dailies may cite a **prior-day matrix** for hooks not re-verified on **D**, with explicit carry note (see [2026-06-21 daily](day/2026-06-21.md), [2026-06-22 daily](day/2026-06-22.md)). That does **not** waive the gate for **new** tier-3 hooks spoken on **D**.

## Related surfaces

| Surface | Role |
| --- | --- |
| [news-verify skill](../../.cursor/skills/news-verify/SKILL.md) | Batch extract + Ship matrix |
| [state-synthesis skill](../../.cursor/skills/state-synthesis/SKILL.md) | Step 0 gate check |
| [source-to-daily-synthesis runbook](../../skills/runbooks/source-to-daily-synthesis.runbook.md) | Archive → matrix → synthesis |
| [METHOD.md](METHOD.md) | Daily register vs synthesis tiers |
| [statecraft/notes/wire/](../notes/wire/) | Matrix shelf |
