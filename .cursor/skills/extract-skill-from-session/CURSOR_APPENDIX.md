# strategy-codex host appendix — extract-skill-from-session

## Portable ladder (this repo)

| Step | Path |
|------|------|
| Pointer | [skills/skill-candidates.md](../../../skills/skill-candidates.md) |
| Draft | [skills/_drafts/](../../../skills/_drafts) |
| Listed | [skills/\<name\>/SKILL.md](../../skills/) + [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync | `python3 scripts/sync_portable_skills.py --verify` then sync |
| Validate | `python3 scripts/validate_skills.py` |

## Commands

```bash
python3 scripts/sync_portable_skills.py --skill extract-skill-from-session
python3 scripts/validate_skills.py
```

## Cursor-only fallback

When not using the portable pipeline, a project-local skill may live under `.cursor/skills/<skill-name>/SKILL.md` — still prefer portable core for strategy-codex.

## Reference

- [skills/README.md](../../../skills/README.md) — discovery ladder
- [skills/_schema.md](../../../skills/_schema.md) — portable schema
- Host create-skill guide: `~/.cursor/skills-cursor/create-skill/SKILL.md` when refining Cursor-native format
