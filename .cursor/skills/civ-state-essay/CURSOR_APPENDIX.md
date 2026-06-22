Cursor-only wiring for [civ-state-essay/SKILL.md](../../../skills/civ-state-essay/SKILL.md). Portable SSOT body stays in `skills/`.

## Instance paths (essay SSOT)

| Topic | Path |
|-------|------|
| Generic essay template | [public/civ-state/templates/civ-state-essay-template.md](../../../public/civ-state/templates/civ-state-essay-template.md) |
| Reader guide | [public/civ-state/docs/reader-guide.md](../../../public/civ-state/docs/reader-guide.md) |
| Cross-volume essays shelf | [public/civ-state/essays/README.md](../../../public/civ-state/essays/README.md) |
| Rome essays README | [public/civ-state/volumes/rome/essays/README.md](../../../public/civ-state/volumes/rome/essays/README.md) |
| Rome registry | [public/civ-state/volumes/rome/essays/essay-rome.registry.yaml](../../../public/civ-state/volumes/rome/essays/essay-rome.registry.yaml) |
| Rome connectivity / essay types | [public/civ-state/volumes/rome/theory/connectivity-rome.md](../../../public/civ-state/volumes/rome/theory/connectivity-rome.md) |
| Rome essay citation inventory | [public/civ-state/volumes/rome/rome-bibliography.md](../../../public/civ-state/volumes/rome/rome-bibliography.md) |
| Hex template | [public/civ-state/volumes/rome/theory/_template-hexagonal-rome.md](../../../public/civ-state/volumes/rome/theory/_template-hexagonal-rome.md) |
| Meta sidecar template | [public/civ-state/volumes/rome/theory/_template-essay-rome.meta.yaml](../../../public/civ-state/volumes/rome/theory/_template-essay-rome.meta.yaml) |

Other volumes: start at `public/civ-state/volumes/{vol}/essays/README.md` before editing.

## QA — civic-chain prose check

**Primary gate:** `scripts/check_civ_state_essay_prose.py`

**Pass → `--class` (see SKILL § Civic-chain pass router):**

| Pass | `--class` | Body | Quoted |
|------|-----------|------|--------|
| Source-bearing (v2 default) | `civic-chain-rome-v2` | 2,400–2,600 | 450–550 |
| Humanizing / light human-prose | `civic-chain-rome-humanize` | 2,400–2,800 | 450–550 |

```powershell
python scripts/check_civ_state_essay_prose.py --rome-civic-chain-four
python scripts/check_civ_state_essay_prose.py --path public/civ-state/volumes/rome/essays/essay-rome-genesis.md --class civic-chain-rome-humanize
python scripts/check_civ_state_essay_prose.py --path public/civ-state/volumes/rome/essays/essay-rome-republic.md --class civic-chain-rome-humanize
python scripts/check_civ_state_essay_prose.py --path public/civ-state/volumes/rome/essays/essay-rome-caesar.md --class civic-chain-rome-humanize
python scripts/check_civ_state_essay_prose.py --path public/civ-state/volumes/rome/essays/essay-rome-augustus.md --class civic-chain-rome-v2
```

Reports: `body_words`, `quoted_words`, `quote_pct`, `authorial_words`, schematic hits, modern-surname violations (Gibbon/Mommsen allowed only inside `"…"`), footnote resolution.

**Essay state (Rome civic-chain four — v0.2.2):** genesis · republic · caesar → **`civic-chain-rome-humanize`**; augustus → **`civic-chain-rome-v2`** until humanized. SSOT table: SKILL § Rome civic-chain essay state · milestones: [release-history.md](../../../public/civ-state/docs/release-history.md).

**Bands (civic-chain-rome-v2):** body 2,400–2,600 · quoted 450–550 · ~18–22% quote ratio.

**Humanizing / light human-prose:** `--class civic-chain-rome-humanize` — body 2,400–2,800 · quoted 450–550 unchanged. Light pass: optional anti-pattern pre-flight; band-floor restore via embodied beats after dedupe (SKILL § Execution order).

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
