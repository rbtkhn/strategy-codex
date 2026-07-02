# Helix-lane v1 → book-first salvage matrix

Maps the legacy **`rbtkhn/civ-emp`** helix-lane public cut to the **`rbtkhn/civ-state`** book export. Run **before** archiving helix navigation as default.

## Principle

**Salvage ideas, not shapes.** Distill pattern→carrier→restraint→settlement into essays and comparative sheets; do not republish raw transactions or operator routers as book doors.

## Matrix

| Helix-lane v1 surface (civ-emp) | Disposition | Book-first target |
|--------------------------------|-------------|-------------------|
| `helix.md` per lane | Archive | Volume `statecraft-*.md` + framework essay |
| `{lane}/civilization/objects/state-memory.md` | Distill | `volumes/{civ}/civilization-*.md` |
| `{lane}/empire/objects/empire-instrument.md` | Distill | `volumes/{civ}/empire-*.md` |
| `{lane}/state/` carriers | Distill | `volumes/{civ}/statecraft-*.md` |
| Geo / war / peace strands | Distill or archive | `geo-strategy-*`, comparative sheets |
| `transactions/*` | **Do not publish** | strategy-codex operator layer |
| Orientation routers (`migration/orientation-*.md`) | Archive | `reader-guide.md`, `source-lattice.md` |
| `indexes/source-retrieval-matrix.md` | **Do not publish** | Public source-lattice + volume shelves |
| `synthesis/*` helix memos | Audit → distill | `public/civ-state/theory/` + cross-case essay |
| `iran/hormuz-recognition-transit-restraint.md` | Publish (transformed) | `essays/hormuz-recognition-transit-restraint.md` |
| Hormuz proof logic in transactions | **Do not publish** | Mechanism already in comparative object |
| `ARCHITECTURE.md` helix doctrine | Archive | `FOUNDING-PROVENANCE.md` + `archive/helix-lane-v1/` |
| Speaker indexes under `indexes/mercouris/` etc. | Archive | Not book apparatus; optional future advanced layer |

## Lane → volume map

| Lane (civ-emp) | Volume slug |
|----------------|-------------|
| china | `volumes/china/` |
| iran / persia | `volumes/persia/` |
| rome | `volumes/rome/` (preview) |
| russia | `volumes/russia/` |
| america | `volumes/america/` |

## High-value distillations (P0)

1. **Hormuz** — already in `statecraft/states/essays/hormuz-recognition-transit-restraint.md` → export to comparative/
2. **Continuity mechanism** — [cross-case recurrence essay](../../public/civ-state/essays/cross-case-recurrence-and-sovereignty.md); operator archive `statecraft/states/archive/theory-cross-case-v1/`
3. **Pattern library** — retired from public shelf; archived under `statecraft/states/archive/theory-cross-case-v1/patterns/`
4. **Sacred grammar** — legitimacy substrate per civ

## Archive location

Public archive README: `archive/helix-lane-v1/README.md` in exported civ-state repo.

Operator academy mirror (legacy): `continuity/academy/statecraft/civ-emp/` — sync separately; not auto-renamed by export.

## Export

This matrix informs export manifest exclusions (transactions, retrieval matrix, bridge docs). Regenerate public tree:

```bash
python scripts/export_civilizational_statecraft_public.py
python scripts/validate_civilizational_statecraft_public.py
```
