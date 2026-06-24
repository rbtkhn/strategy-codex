# skill-strategy — dissolved (2026-06)

**Status:** The Cursor skill **`.cursor/skills/skill-strategy/`** is **removed**. Do not invoke or recreate it. **`strategy-codex`** activation is doc-first; **`strategy-notebook`** is **deprecated compatibility** namespace only.

## What to use instead

| Old trigger | New contract |
|-------------|--------------|
| **`strategy`**, **`strategy pass`** | [DEFAULT-PATH.md](DEFAULT-PATH.md) — three moves; [.cursor/rules/strategy-codex-pass.mdc](../../.cursor/rules/strategy-codex-pass.mdc) |
| Routing / disambiguation | [README.md](README.md) — Activation + Routing |
| EOD compose / page-first | [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md) |
| §1d–§1h watch threads | [FIVE-THREAD-WATCH-TAGS.md](FIVE-THREAD-WATCH-TAGS.md) |
| Voice / lens | [VOICES-SUPERSEDE-MINDS.md](VOICES-SUPERSEDE-MINDS.md) + **statecraft** handoff; **`state-synthesis`** / [**periodic-statecraft-review** runbook](../../skills/runbooks/periodic-statecraft-review.runbook.md) |
| Verify | [wire-verify](../../.cursor/skills/wire-verify/SKILL.md) / [fact-check](../../.cursor/skills/fact-check/SKILL.md) |
| Public copy | [skill-write](../../.cursor/skills/skill-write/SKILL.md) |

## Git history

Last full skill body before dissolve: inspect with  
`git log --oneline -- .cursor/skills/skill-strategy/SKILL.md`  
then `git show <commit>:.cursor/skills/skill-strategy/SKILL.md`.

## Legacy references

Historical docs, demo runs, and exercise logs may still say **skill-strategy** in filenames or prose. Treat as **compatibility residue** unless actively updated.
