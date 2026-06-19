Cursor-only wiring for [civ-state/SKILL.md](../../../skills/civ-state/SKILL.md). Portable SSOT body stays in `skills/`.

## Cursor entry (cold thread)

On a **new thread** with no prior warmup in chat:

- `Read` the assembled skill with `limit≤80` first (first slice only)
- deliver the CIV-STATE menu in chat
- do **not** batch `harness_warmup` or other shell with the skill read
- after any tool hang: one smaller read per turn; operator `fast tools` / `read only` → strict Read/Write, zero Shell

## Public routing table

| Civ | Doorway | Era spine | Notes |
|-----|---------|-----------|-------|
| China | [volumes/china/README.md](../../../public/civ-state/volumes/china/README.md) | ancient → cybernetic | sovereignty-chain order |
| Persia | [volumes/persia/README.md](../../../public/civ-state/volumes/persia/README.md) | ancient → cybernetic | recognition / sacred grammar |
| Rome | [volumes/rome/README.md](../../../public/civ-state/volumes/rome/README.md) | ancient → cybernetic | hexagonal pilot — [essays/](../../../public/civ-state/volumes/rome/essays/README.md) |
| Russia | [volumes/russia/README.md](../../../public/civ-state/volumes/russia/README.md) | medieval → cybernetic | |
| America | [volumes/america/README.md](../../../public/civ-state/volumes/america/README.md) | medieval → cybernetic | |

Whole-work: [theory/README.md](../../../public/civ-state/theory/README.md) · [sources/source-lattice.md](../../../public/civ-state/sources/source-lattice.md) · [volumes/README.md](../../../public/civ-state/volumes/README.md) · [docs/era-spine.md](../../../public/civ-state/docs/era-spine.md)

**Rome hexagonal (book maint):** [connectivity-rome.md](../../../public/civ-state/volumes/rome/essays/connectivity-rome.md) · RLJ Rome parallel-spine ladder in [recursive-learn](../recursive-learn/SKILL.md) — link, do not duplicate table.

## P0 public skill cards → operator letters

| Public card | Default letter |
|-------------|----------------|
| [governing-term-first.md](../../../public/civ-state/skills/governing-term-first.md) | **A. Frame** |
| [civilization-first-entry.md](../../../public/civ-state/skills/civilization-first-entry.md) | **A. Frame** (case-first) |
| [source-lattice-read.md](../../../public/civ-state/skills/source-lattice-read.md) | **B. Retrieve** |

## Letter handoff recipes (bounded reads)

| Pick | Read first (limits) |
|------|---------------------|
| **A** | `public/civ-state/theory/README.md` limit 60 → `skills/governing-term-first.md` limit 40 |
| **B** | `sources/source-lattice.md` limit 50 **or** `volumes/{civ}/shelf-reader.md` limit 50 |
| **D** | [review-queue.md](../../../statecraft/states/review-queue.md) tail + one named public edit target |

## Archive-missing guard (state-synthesis handback)

When wire-bridge needs archive but `source-archive/statecraft/<day>/` batch is thin:

```text
Archive batch not ready — run state synthesis after intake, not civ-state frame loop.
```

Hand off to [state-synthesis](../state-synthesis/SKILL.md).

## Allowed dynamic inputs (instance paths)

**Public first:**

1. [public/civ-state/theory/](../../../public/civ-state/theory/)
2. [public/civ-state/skills/](../../../public/civ-state/skills/)
3. [public/civ-state/sources/](../../../public/civ-state/sources/)
4. [public/civ-state/volumes/](../../../public/civ-state/volumes/)
5. [public/civ-state/essays/](../../../public/civ-state/essays/)

**Operator second:**

6. [statecraft/voices/](../../../statecraft/voices/)
7. [statecraft/research/bridges/](../../../statecraft/research/bridges/)
8. [ph-civ-to-civ-state-bridge.md](../../../statecraft/states/ph-civ-to-civ-state-bridge.md)
9. [ph-civ-promotion-ledger.md](../../../statecraft/states/ph-civ-promotion-ledger.md)
10. [review-queue.md](../../../statecraft/states/review-queue.md)

## Action-family routes (instance)

| Family | Route toward |
|--------|----------------|
| **A. Frame** | [statecraft-framework](../statecraft-framework/SKILL.md) · public theory/skills · [six-term checklist](../../../statecraft/states/civilization-empire-faith-science-memory-entropy-retrieval-checklist.md) |
| **B. Retrieve** | public shelf-reader · primary/secondary-sources · volumes · sacred grammar · de-prioritize [source-retrieval matrix](../../../statecraft/states/indexes/source-retrieval-matrix.md) unless public exhausted |
| **C. Promote** | bridge · ledger · [ph-civ-to-civ-state-promoter](../ph-civ-to-civ-state-promoter/SKILL.md) |
| **D. Review** | review-queue · public edit target · [civ-state-volume-harden](../civ-state-volume-harden/SKILL.md) only if explicit book work |

## Publish reminder

Review resolutions **commit** to `public/civ-state/`. Mention `publish_public_civ_state.py` only when operator says **ship**, **publish**, or **VERSION** — not on every close.

## Book-authoring escape hatch

- [civ-state-volume-architect](../civ-state-volume-architect/SKILL.md)
- [civilization-part-writer](../civilization-part-writer/SKILL.md)
- [empire-part-writer](../empire-part-writer/SKILL.md)
- [statecraft-guidebook-writer](../statecraft-guidebook-writer/SKILL.md)

## Doctrine cross-links

- [statecraft/README.md](../../../statecraft/README.md) — **`civ-state` skill retrieves through `public/civ-state/`**
- [statecraft/states/README.md](../../../statecraft/states/README.md) — command door

## Maintenance

```powershell
python3 scripts/sync_portable_skills.py --skill civ-state
python3 scripts/sync_portable_skills.py --verify --skill civ-state
python3 scripts/validate_skills.py
python3 scripts/validate_civ_state_skill_links.py
```
