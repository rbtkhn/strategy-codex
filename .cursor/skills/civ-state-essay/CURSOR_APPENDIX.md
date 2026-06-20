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

## QA recipe (until `check_civ_state_essay_prose.py` exists)

**Civic-chain word band + schematic grep** — one essay path per invocation:

```powershell
python -c "
import re, sys
path = sys.argv[1]
text = open(path, encoding='utf-8').read()
body = text.split('## Notes')[0] if '## Notes' in text else text
words = len(re.findall(r'\b\w+\b', body))
print(f'body_words={words}')
ban = r'\b(grammar|hinge|apparatus|sequence|strain|proof|logic|stacks|substrate|nullification|machinery|shell)\b'
hits = [(i+1, ln.strip()) for i, ln in enumerate(body.splitlines()) if re.search(ban, ln, re.I)]
print('schematic_hits=', len(hits))
for n, ln in hits[:12]: print(f'  L{n}: {ln[:100]}')
" public/civ-state/volumes/rome/essays/essay-rome-genesis.md
```

**Modern surnames (body):** grep body only for Gibbon, Mommsen, Syme, Goldsworthy, Everitt, Durant — must be Notes-only.

**Footnotes:** every `[^n]` in body resolves in `## Notes`.

**Future hook (v1 documents only):** `scripts/check_civ_state_essay_prose.py` — wire when Persia/China civic-chain pass reuses Rome QA.

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
