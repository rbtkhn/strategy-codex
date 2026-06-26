Cursor-only wiring for [civ-state-note/SKILL.md](../../../skills/civ-state-note/SKILL.md). Portable SSOT body stays in `skills/`.

## Instance paths (note + CIV-STATE SSOT)

| Topic | Path |
|-------|------|
| Notes shelf README | [statecraft/notes/README.md](../../../statecraft/notes/README.md) |
| Prose-class chooser | [docs/prose-index.md](../../../docs/prose-index.md) |
| Public book root | [public/civ-state/README.md](../../../public/civ-state/README.md) |
| Rome essays README | [public/civ-state/volumes/rome/essays/README.md](../../../public/civ-state/volumes/rome/essays/README.md) |
| Rome connectivity | [public/civ-state/volumes/rome/theory/connectivity-rome.md](../../../public/civ-state/volumes/rome/theory/connectivity-rome.md) |
| Reader guide (geo-strategic habit pointer) | [public/civ-state/docs/reader-guide.md](../../../public/civ-state/docs/reader-guide.md) |
| Archive day index | `source-archive/statecraft/<YYYY-MM-DD>/README.md` |
| News-verify registry | [docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md) |

## Examples (shelf-native patterns)

| Pattern | Example |
|---------|---------|
| Guest-pair citation split | [june-18-2026-mou-guest-pair-citation-split.md](../../../statecraft/notes/june-18-2026-mou-guest-pair-citation-split.md) |
| Speaker-function comparison | [barnes-johnson-aguilar-kent-on-section-224.md](../../../statecraft/notes/barnes-johnson-aguilar-kent-on-section-224.md) |
| Mechanism | [formal-sovereignty-vs-internal-carriage.md](../../../statecraft/notes/formal-sovereignty-vs-internal-carriage.md) |

## QA — note promotion (no essay prose script)

**Primary gates (manual / checklist):**

1. One argument — not whole-day dump
2. `Retrieve posture` + `Public anchors` when CIV-STATE pre-pass required
3. Archive paths from day README or named captures
4. Wire verdicts use **`wire-verify`** vocabulary when tierable
5. README index line on ship

**Optional wire pass before ship:**

```powershell
python scripts/validate_skills.py
```

**Do not run** `check_civ_state_essay_prose.py` on `statecraft/notes/` — wrong class.

## Validate public tree (only when note triggers public gap)

When the note's **Next use** names a **`public/civ-state/`** edit target, hand off to **`civ-state-essay`** or **`civ-state` D. Review** — do not patch public tree from note promotion alone.

```powershell
python scripts/validate_civilizational_statecraft_public.py public/civ-state
```

## Related skills (instance)

| Skill | When |
|-------|------|
| [civ-state](../civ-state/SKILL.md) | Retrieve / frame before note |
| [civ-state-essay](../civ-state-essay/SKILL.md) | Graduate note to public essay |
| [state-note](../state-note/SKILL.md) | General note without CIV-STATE pre-pass |
| [wire-verify](../wire-verify/SKILL.md) | Same-week wire hooks |
| [state-synthesis](../state-synthesis/SKILL.md) | Upstream daily batch |
| [validator-first](../validator-first/SKILL.md) | Menu pick = run validate same turn |

## Maintenance

```powershell
python scripts/sync_portable_skills.py --skill civ-state-note
python scripts/sync_portable_skills.py --verify --skill civ-state-note
python scripts/validate_skills.py
```

Hand-edit **only** `skills/civ-state-note/SKILL.md`; run sync before commit.
