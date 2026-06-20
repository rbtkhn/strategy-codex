Cursor-only wiring for [civ-state-essay/SKILL.md](../../../skills/civ-state-essay/SKILL.md). Portable SSOT body stays in `skills/`.

## Instance paths (essay SSOT)

| Topic | Path |
|-------|------|
| Generic essay template | [public/civ-state/templates/civ-state-essay-template.md](../../../public/civ-state/templates/civ-state-essay-template.md) |
| Reader guide | [public/civ-state/docs/reader-guide.md](../../../public/civ-state/docs/reader-guide.md) |
| Cross-volume essays shelf | [public/civ-state/essays/README.md](../../../public/civ-state/essays/README.md) |
| Rome essays README | [public/civ-state/volumes/rome/essays/README.md](../../../public/civ-state/volumes/rome/essays/README.md) |
| Rome registry | [public/civ-state/volumes/rome/essays/essay-rome.registry.yaml](../../../public/civ-state/volumes/rome/essays/essay-rome.registry.yaml) |
| Rome connectivity / essay types | [public/civ-state/volumes/rome/essays/connectivity-rome.md](../../../public/civ-state/volumes/rome/essays/connectivity-rome.md) |
| Hex template | [public/civ-state/volumes/rome/essays/_template-hexagonal-rome.md](../../../public/civ-state/volumes/rome/essays/_template-hexagonal-rome.md) |
| Meta sidecar template | [public/civ-state/volumes/rome/essays/_template-essay-rome.meta.yaml](../../../public/civ-state/volumes/rome/essays/_template-essay-rome.meta.yaml) |

Other volumes: start at `public/civ-state/volumes/{vol}/essays/README.md` before editing.

## QA — civic-chain prose check

**Primary gate:** `scripts/check_civ_state_essay_prose.py`

```powershell
python scripts/check_civ_state_essay_prose.py --rome-civic-chain-four
python scripts/check_civ_state_essay_prose.py --path public/civ-state/volumes/rome/essays/essay-rome-genesis.md
```

Reports: `body_words`, `quoted_words`, `quote_pct`, `authorial_words`, schematic hits, modern-surname violations (Gibbon/Mommsen allowed only inside `"…"`), footnote resolution.

**Bands (civic-chain-rome-v2):** body 2,400–2,600 · quoted 450–550 · ~18–22% quote ratio.

**Inline fallback** (one path only, if script unavailable):

```powershell
python -c "import re,sys; p=sys.argv[1]; t=open(p,encoding='utf-8').read(); b=t.split('## Notes')[0]; q=sum(len(re.findall(r'\b\w+\b',s)) for s in re.findall(r'\"([^\"]+)\"',b)); w=len(re.findall(r'\b\w+\b',b)); print(f'body={w} quoted={q} pct={q/w*100:.1f}')" public/civ-state/volumes/rome/essays/essay-rome-genesis.md
```

**Footnotes:** every `[^n]` in body resolves in `## Notes`.

## Validate and publish

```powershell
python scripts/validate_civilizational_statecraft_public.py public/civ-state
python scripts/publish_public_civ_state.py -m "civ-state: …" --push
```

Mirror publish only when operator says **ship**, **publish**, or **VERSION**.

## RLJ cross-links

- [recursive-learning-journal.md](../../../statecraft/recursive-learning-journal.md) — geo-strategic revision law (append on operator `append RLJ` / `log this`); parallel-ban Windows EXECUTE discipline
- After substantive essay ship, offer **`recursive learn`** — do not auto-append

## Related skills (instance)

| Skill | When |
|-------|------|
| [civ-state](../civ-state/SKILL.md) | Essay class unsettled; retrieve / frame |
| [civ-state-volume-architect](../civ-state-volume-architect/SKILL.md) | Volume architecture — not single-essay polish |
| [civilization-part-writer](../civilization-part-writer/SKILL.md) | New civilization part |
| [empire-part-writer](../empire-part-writer/SKILL.md) | New empire part |
| [validator-first](../validator-first/SKILL.md) | Menu pick = run validate same turn |

## Maintenance

```powershell
python scripts/sync_portable_skills.py --skill civ-state-essay
python scripts/sync_portable_skills.py --verify --skill civ-state-essay
python scripts/validate_skills.py
```
