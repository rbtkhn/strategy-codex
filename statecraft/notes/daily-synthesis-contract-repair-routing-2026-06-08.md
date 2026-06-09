# Daily Synthesis Contract Repair Routing - 2026-06-08

WORK only; not Record.

Opens the **daily synthesis validator** seam using the same tranche logic as
[archive-truth-floor-repair-routing-2026-06-01.md](./archive-truth-floor-repair-routing-2026-06-01.md).

## Current Stack

### 1. Tail-label tranche — **CLOSED** (2026-06-08 Kleiber)

- `Statecraft Notes` → `Companion Notes`
- Receipt: [kleiber-close-daily-companion-notes-stopping-rules-2026-06-08.md](../../docs/kleiber-close-daily-companion-notes-stopping-rules-2026-06-08.md)

### 2. June week section-order tranche — **CLOSED** (2026-06-08 Kleiber)

- `Lane Pressure` → `Lane Read` on `2026-06-03`, `2026-06-04`
- `## Mechanism Comparison` → `###` under Speaker Value on `2026-06-06`, `2026-06-07`, `2026-06-08`
- Receipt: [kleiber-close-june-section-order-stopping-rules-2026-06-08.md](../../docs/kleiber-close-june-section-order-stopping-rules-2026-06-08.md)

### 3. June week five-volume tranche — **CLOSED** (2026-06-08 Kleiber)

- Reordered `2026-06-03` through `2026-06-08` (except `2026-06-05`, already valid)
- Normalized `2026-06-08` backtick label format
- Receipt: [kleiber-close-june-five-volume-stopping-rules-2026-06-08.md](../../docs/kleiber-close-june-five-volume-stopping-rules-2026-06-08.md)

### 4. June week quote-anchor tranche — **CLOSED** (2026-06-08 Kleiber)

- Nine anchors extended on `2026-06-03`, `2026-06-04`, `2026-06-06`, `2026-06-07`
- Receipt: [kleiber-close-june-quote-anchor-stopping-rules-2026-06-08.md](../../docs/kleiber-close-june-quote-anchor-stopping-rules-2026-06-08.md)

### 5. June 01 quote-anchor tranche — **CLOSED** (follow-up)

- Three anchors extended on `2026-06-01.md` (Sachs, Davis, Hoh)

### 6. `2026-06.md` monthly tranche — **CLOSED** (follow-up)

- Section headings aligned to monthly contract; `capture`/`escalation_trap` → `legitimacy`/`trap`; five-volume reorder; artifacts demoted under `Best Next Companion Notes`

### 7. Quote-anchor backlog tranche — **OPEN** (March–May dailies)

### 8. Monthly backlog tranche — **OPEN**

`2026-03.md`, `2026-04.md`, `2026-05.md` section order and convergence labels.

## Opening Rule

```text
1. tail label (closed)
2. section order on June week (closed)
3. five-volume order on June week (closed)
4. quote anchors on June week (closed)
5. March–May quote backlog + monthly notes
```

## Stop Rule

Reuse [archive-truth-floor-audit-receipt-pattern.md](../../docs/archive-truth-floor-audit-receipt-pattern.md):

```text
if the remainder for the active tranche is zero or explicitly reviewed,
close the family and advance the boundary
```

## Validator Command

```bash
python scripts/validate_statecraft_daily_synthesis.py
```

**June shelf status:** all `2026-06-*` daily + `2026-06.md` monthly notes pass validator.

Current backlog: **16 errors** (advisory CI) — March–May dailies + `2026-03`/`2026-04`/`2026-05` monthly notes only.

## Opening-order table (Karajan 2026-06-08)

Validator run: `python scripts/validate_statecraft_daily_synthesis.py` → **16 errors**.

| Rank | Tranche | Files | Errors | Defect class | First open |
| ---: | --- | ---: | ---: | --- | --- |
| **1** | March daily quote-anchor | 4 | 8 | short/missing `Quote anchor:` | `statecraft/daily/2026-03-16.md` (3 lines — densest) |
| **2** | April daily quote-anchor | 4 | 5 | short `Quote anchor:` | `statecraft/daily/2026-04-17.md` |
| **3** | Monthly section tail label | 3 | 3 | `Best Next Statecraft Notes` → `Best Next Companion Notes` | `statecraft/daily/2026-03.md` |

### Error inventory (by file)

| File | Errors | Lines / class |
| --- | ---: | --- |
| `2026-03-16.md` | 3 | 118, 124, 132 quote-anchor |
| `2026-03-23.md` | 1 | 126 quote-anchor |
| `2026-03-27.md` | 3 | 137, 139, 141 quote-anchor |
| `2026-03-31.md` | 1 | 131 quote-anchor |
| `2026-04-17.md` | 1 | 121 quote-anchor |
| `2026-04-20.md` | 2 | 115, 117 quote-anchor |
| `2026-04-22.md` | 1 | 111 quote-anchor |
| `2026-04-30.md` | 1 | 95 quote-anchor |
| `2026-03.md` | 1 | monthly section-order (`Best Next Statecraft Notes`) |
| `2026-04.md` | 1 | monthly section-order (same) |
| `2026-05.md` | 1 | monthly section-order (same) |

### Karajan opening rule (recommended)

```text
1. March quote-anchor Kleiber pass (complete family before April)
2. April quote-anchor Kleiber pass
3. Monthly tail-label mechanical pass (3 renames — same shape as June tranche 1)
```

**Do not batch** quote-anchor repair with monthly rename or with unstaged Nawfal/America-transaction work — different receipt families.

**Fast-win alternative:** rank-3 monthly rename first (3 errors, one mechanical family) if the operator wants a quick 16→13 drop before source-archive quote extension work.

**Rank 3 status (2026-06-08):** **held** — `2026-03.md`, `2026-04.md`, `2026-05.md` tail `Best Next Companion Notes`; validator **8→5**.

### Projected remainder after rank 1–3

```text
0 errors — full `statecraft/daily` migrated shelf green on validator
```

Then eligible: flip CI `validate_statecraft_daily_synthesis` from advisory to blocking (see `.github/workflows/test.yml`).

## Next conductor close verdict (Karajan B 2026-06-08)

Cross-read: [conductor-gap-audit-2026-05-21-06-07.md](./conductor-gap-audit-2026-05-21-06-07.md) vs
[recursive-learning-journal.md](../recursive-learning-journal.md) (2026-06-08 ship + four-tranche Kleiber entries).

| Layer | Gap audit | Journal | Unstaged disk |
| --- | --- | --- | --- |
| June 05–07 judgment ship | Needed full stack → **closed retroactively** 2026-06-08 | Law: `T→F→K→B→KJ` under ship pressure | Kleiber daily stack **pushed**; **America transaction + Barnes companion not** |
| America capture / firewall | `foreign-client-mesh…` → Kleiber slice if commit imminent | Karajan falsified hierarchy batching | `statecraft/america/transactions/foreign-client-mesh-separation-and-command-review.md` (+16 lines) |
| June 8 intake routing | — | Bernstein readability | `2026-06-08-intake-readiness.md` (minor) |
| Validator contract | — | Four Kleiber tranches; June shelf green | **16 errors** March–April + monthly tail |
| Archive substrate | — | Archive truth floor (Hormuz pattern) | Large **Napolitano** `opening_tier` normalize (separate lane) |

### Recommendation

**Next conductor close: `karajan`** — not Kleiber on validator backlog yet.

**Why Karajan wins:**

- June 8 **Karajan outcome** already falsified mixing hierarchy commits with unrelated lanes; unstaged **America primary-ownership** edits are the protruding unfinished slice from that ship story.
- Gap audit disproportion: judgment production **shipped** for June dailies but **America transaction revision** remains local — same failure mode as pre–June-8 (learning in files, weak commit receipt).
- Validator Kleiber (rank 1–3) is **orthogonal contract hygiene** — safe and correct **after** a named Karajan commit-order pass, not batched into the same push.

**Karajan close should name:**

```text
commit 1 — America: foreign-client-mesh transaction + Barnes companion note
commit 2 — intake-readiness tweak (if still live)
commit 3 — validator Kleiber March quote-anchor tranche (separate)
commit 4 — Napolitano substrate normalize (separate; do not batch with 1–3)
```

**When Kleiber is next instead:** operator explicitly **defers** America/Barnes ship and wants validator **16→0** or monthly fast-win first — acceptable, but that inverts June 8 hierarchy falsifier risk (contract before judgment receipt).

### Falsifier

```text
If America transaction + Barnes companion land in the same commit as Napolitano bulk normalize
or March quote-anchor repair, Karajan routing failed.
```

### Slice receipts (Karajan D 2026-06-08)

| Slice | Status | Artifacts |
| --- | --- | --- |
| 1 — America judgment | **held** | `foreign-client-mesh…` transaction + `2026-06-08-barnes-america-capture-non-intercept-colby-mou.md` |
| 2 — intake-readiness | open | `2026-06-08-intake-readiness.md` |
| 3 — validator Kleiber | **held (March dailies)** | `2026-03-16/23/27/31` quote anchors; 16→8 errors |
| 4 — Napolitano substrate | open | separate normalize commit |
