# Jiang Compression Engine v1

**Lane:** operator research Ã¢â‚¬” [work-jiang](./README-operator.md) / `codex/predictive-history/`. **Not** Record until merged through **RECURSION-GATE**.

## Purpose

Turn a bulky work artifact (analysis, handoff, planning notes) into a **small JSON pack** that declares:

- **Category** Ã¢â‚¬” `operational` | `analytical` | `synthesis` | `other`
- **One-sentence outcome**
- **1Ã¢â‚¬“3 executable next actions**
- **Evidence links** (paths, ACT/READ ids, doc names)
- Optional tie to **seed** context (`seed/minimal-core.json`) and **founding intent** (`reflection-proposals/SEED-founding-intent.md`)

This fights **layer drift** and **truth density** by forcing a labeled, linkable summary before more execution.

**mastery-learning analogy:** AI school uses a hard **~90% mastery** bar before unlocking the next lesson; Jiang compress asks for **one-sentence clarity**, **linked evidence**, and **next actions** before treating a work artifact as ready to build on Ã¢â‚¬” operator discipline parallel to “no Swiss cheese before advancing.” See [bloom-mastery-adaptation.md](../../docs/bloom-mastery-adaptation.md) (Bloom / 2 Sigma layer).

## Commands

```bash
python3 scripts/jiang-compress.py -u grace-mar
python3 scripts/jiang-compress.py -u grace-mar --input codex/predictive-history/STATUS.md
python3 scripts/jiang-compress.py -u grace-mar --print-gate-stub   # always print gate stub at end
```

## Checklist vs gate

The script opens with an **operator compression checklist** (y/N). That is **discipline**, not the companion **RECURSION-GATE**. If the compression should change SELF/EVIDENCE, use the printed **gate stub** (or write your own candidate) in `recursion-gate.md` and approve per [identity-fork-protocol.md](../../identity-fork-protocol.md).

## Outputs

| Output | Location |
|--------|----------|
| Compression JSON | `codex/predictive-history/compressions/<slug>-YYYYMMDD.json` |
| Schema | `codex/predictive-history/schemas/jiang-compression-v1.schema.json` |
| Daily intention note (optional) | `reflection-proposals/DAILY-INTENTION-YYYY-MM-DD.md` (append) |

**Sprint bundles (future):** `codex/predictive-history/sprints/` Ã¢â‚¬” see README there.

## Related

- [compressions/README.md](./compressions/README.md)
- [seed-phase-wizard.md](../../seed-phase-wizard.md) / [good-morning-brief.py](../../scripts/good-morning-brief.py)
- [work-jiang-feature-checklist](../../.cursor/skills/work-jiang-feature-checklist/SKILL.md)

