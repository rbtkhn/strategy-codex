# Phase 8 — README and start-here trim plan

**Work only; not Record.** Targets from [complexity-budget.md](complexity-budget.md) and the complexity mitigation plan.

## Baseline (2026-06-21)

| Surface | Lines | Target | Gap |
|---------|------:|-------:|----:|
| [README.md](../README.md) | ~381 | ≤ 150 | −231 |
| [docs/start-here.md](start-here.md) | ~159 | operator loop (~120) | −39 |

Preflight: `python3 scripts/check_doc_duplication.py` (warn) surfaces duplicate blocks to remove, not replace with new prose.

## Principles

1. **Pointer, don’t paste** — routing tables, essay inventories, and Grace-Mar doctrine belong in one SSOT each ([LLM-ROUTING.md](../LLM-ROUTING.md), [essays/README.md](../essays/README.md), [docs/archive/grace-mar.md](archive/grace-mar.md)).
2. **One choose-your-path** — keep the A–F table in **start-here**; README links to `#choose-your-path` there.
3. **One system map** — mermaid diagram lives in **start-here** only; README one-line link.
4. **Fork archaeology** — README + start-here get ≤3 short Grace-Mar pointer lines; detail → [docs/agent-rules/deep-rules.md](agent-rules/deep-rules.md) and archive docs.

## Wedge order (safe relocations)

| Wedge | Action | Est. lines saved | Risk |
|-------|--------|------------------:|------|
| **1** | Replace README § Essays index table with link to [essays/README.md](../essays/README.md) | ~30 | Low — **done 2026-06-21** |
| **2** | Remove README duplicate mermaid + “Architecture / Embedded Record” blocks; link start-here + architecture.md | ~120 | Medium — **done 2026-06-21** |
| **3** | Collapse README “Claude Code surfaces” + duplicate mental-model tables → [docs/claude-surface-contract.md](claude-surface-contract.md) | ~40 | Low — **done 2026-06-21** |
| **4** | README choose-your-path → link start-here only | ~25 | Medium — **done 2026-06-21** |
| **5** | start-here: trim “Where to go next” + command blocks | ~90 | Low — **done 2026-06-21** |

**Gate after wedge 2:** re-run `check_doc_duplication.py`; choose-your-path and route-table duplicates should drop.

## Done criteria

- README ≤ 150 lines
- start-here ≤ ~120 lines, promotion ladder + ship loop retained
- `check_doc_duplication.py --strict` passes (or issue count trends to zero)
- **2026-06-21:** product-identity ↔ start-here deduped — `--strict` green
- No stale architecture stub links (active [architecture.md](architecture.md) only)

## CI

- Warn: `python3 scripts/check_doc_duplication.py` in repo-health **Advisory** job
- Fail: promote to **Required** after wedges 1–4 land

## Related

- [contributors/docs.md](contributors/docs.md)
- [check_archive_boundary.py](../scripts/check_archive_boundary.py) — long Grace-Mar blocks without pointer
- [check_doc_duplication.py](../scripts/check_doc_duplication.py) — duplicate paragraphs / tables / generated markers
