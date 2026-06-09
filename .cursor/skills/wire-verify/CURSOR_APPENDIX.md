# Wire verify — strategy-codex appendix

| Topic | Path |
|-------|------|
| Portable core | [skills-portable/wire-verify/SKILL.md](../../../skills-portable/wire-verify/SKILL.md) |
| General fact triage | [.cursor/skills/fact-check/SKILL.md](../fact-check/SKILL.md) |
| Strategy + verify gate | [.cursor/skills/skill-strategy/SKILL.md](../skill-strategy/SKILL.md) (Modes → **+ verify**) |
| Statecraft intake | [.cursor/skills/statecraft-source-intake/SKILL.md](../statecraft-source-intake/SKILL.md) |
| Daily brief verify tokens | [docs/skill-work/work-strategy/daily-brief-template.md](../../../docs/skill-work/work-strategy/daily-brief-template.md) § Inbox paste target |
| Strategy inbox | [docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) |
| Notebook verify discipline | [docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md](../../../docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md) |
| Statecraft archive | [source-archive/statecraft/](../../../source-archive/statecraft/) |
| Iran native triangulation | [docs/skill-work/work-strategy/daily-brief-iran-watch.md](../../../docs/skill-work/work-strategy/daily-brief-iran-watch.md) |
| Work menu conventions | [docs/skill-work/work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md) |

## Repo defaults

- **Default lane:** Think (chat table). **Ship** only when the operator names files (`source_note`, `editorial_note`, inbox line, `days.md` **Links** — not **Judgment** without dated URLs).
- Run **after** transcript lands, **before** `statecraft daily synthesis` or EOD compose when breaking seams load-bear.
- Pair with **`strategy + verify`** when folding wire hooks into codex / strategy-notebook layers.

## `verify:` token vocabulary (extend daily-brief defaults)

Use on inbox lines, brief §1f rows, or archive YAML tails:

| Token | Meaning |
|-------|---------|
| `verify:wire-RSS` | RSS / live-desk wire; not state primary |
| `verify:wire-supported` | Wire-verify triage: supported |
| `verify:wire-unclear` | Developing or thin sourcing |
| `verify:wire-contested` | Credible wires disagree |
| `verify:wire-contradicted` | Best current cite contradicts hook |
| `verify:operator-transcript` | Hook still only in pasted transcript |
| `verify:tier-A` | Operator-attested or primary-aligned (per notebook tables) |

## Statecraft archive receipt shape

On `source-archive/statecraft/YYYY-MM-DD/source-*.md` frontmatter when operator ships verify:

- Extend **`source_note`** or **`editorial_note`** with semicolon-separated verify tails, or compact **`verify:`** list in YAML if the file already uses structured frontmatter (match neighboring captures).
- Do **not** rewrite transcript body for verify outcomes.
- Example seam tags: `verify: Apache cause — unclear (drone vs SAM)`; `verify: infiltration count — downgraded to one`.

## Strategy-codex weave convention

Existing thread weaves use **wire-verify** informally for roster/title checks (e.g. delegation head misnames). This skill formalizes that habit: run **`wire verify`** on roster lines before promoting to **Links**.

## Escalation routes

| Need | Next skill / action |
|------|---------------------|
| Non-wire claim | **`fact check`** |
| Deeper primary pull | **`fact check deep`** (operator phrase) |
| Iran/PRC/Russia wording | Native primary per **fact-check** + `daily-brief-*-watch.md` |
| Full day batch | **`statecraft daily synthesis`** with verify column |
| Public copy | **`skill-write`** after verify — do not skip |

## Sync

After editing the portable core:

```bash
python3 scripts/sync_portable_skills.py --verify
python3 scripts/validate_skills.py
```
