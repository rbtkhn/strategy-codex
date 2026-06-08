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
