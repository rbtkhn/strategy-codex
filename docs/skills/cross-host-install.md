# Cross-Host Install Guide

## Purpose

Explain how to consume strategy-codex **portable skills** and **runbooks** across different AI agent hosts without creating drifting copies.

## Principle

**One portable core. Host-specific glue only where required.**

- Edit the portable core (`skills/<skill>/SKILL.md` or `skills/runbooks/*.runbook.md`).
- Edit host glue separately (`.cursor/skills/<skill>/CURSOR_APPENDIX.md`).
- Regenerate where supported (`sync_portable_skills.py` for Cursor).
- Verify drift before commit.

Do not maintain five manually edited copies of the same procedure.

## Host matrix

| Host | Recommended input | Generated target | Notes |
|------|-------------------|------------------|-------|
| **Cursor** | `skills/<skill>/SKILL.md` + `.cursor/skills/<skill>/CURSOR_APPENDIX.md` | `.cursor/skills/<skill>/SKILL.md` | Primary generated host; run `sync_portable_skills.py` |
| **Claude Code** | Portable `SKILL.md` + project-local host note | Optional manual assembly | Avoid copying Cursor-only paths into Claude project files |
| **Codex** | Portable `SKILL.md` or selected skill card | Optional | Keep invocation narrow; avoid loading whole catalog |
| **ChatGPT** | Portable core pasted or attached in project context | Manual | Prefer **one skill or runbook per session** |
| **Generic host** | Portable core + local appendix | Optional | Host glue must not edit portable core |

## Cursor

1. Clone or pull strategy-codex.
2. Edit `skills/<skill>/SKILL.md` (portable core).
3. Edit `.cursor/skills/<skill>/CURSOR_APPENDIX.md` for repo paths.
4. Run:

```bash
python3 scripts/sync_portable_skills.py --verify
python3 scripts/sync_portable_skills.py
```

5. Commit portable core, appendix, manifest, and generated `.cursor/skills/*/SKILL.md` together.

## Claude Code

1. Copy `skills/<skill>/SKILL.md` body (or full file) into project instructions or a `.claude/` skill file.
2. Add a short **host appendix** with your repo's paths — do not assume strategy-codex layout.
3. Do not copy generated `.cursor/skills/*/SKILL.md` — it includes Cursor-specific assembly metadata.

## Codex

1. Point the agent at `skills/<skill>/SKILL.md` when the skill is invoked.
2. Optional: `python3 scripts/build_skill_cards.py --markdown` for compact cards under `runtime/artifacts/skill-cards/` — derived, not canonical.
3. Load one skill at a time; avoid pasting the full manifest.

## ChatGPT

1. Paste or attach **one** portable `SKILL.md` or runbook per session.
2. Add a one-paragraph host note for your project paths and approval rules.
3. Re-paste from portable core when methodology changes — do not edit only the ChatGPT copy long-term.

## Generic agent host

1. Portable core = methodology.
2. Host appendix = paths, commands, compliance.
3. Never treat the host copy as canonical.

## Personal vs project scope

Use `scope_class` in skill/runbook frontmatter:

| Scope | Export guidance |
|-------|-----------------|
| `personal` | Do not export without operator review |
| `project-local` | Export with project paths rewritten in host appendix |
| `repo-governed` | Default for strategy-codex; include appendix for in-repo use |
| `public-portable` | Safest for copy-out; still verify forbidden substrings |

## Verification expectations

- Each portable skill should define `## Verification / Proof Standard` (see [skills/_schema.md](../../skills/_schema.md)).
- Runbooks define workflow-level verification in their own **Verification / Proof Standard** section.
- Host copies should preserve verification bullets; wrappers summarize only.

Validate:

```bash
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --strict-verification   # migration gate
```

## Drift avoidance

- **Canonical:** `skills/<skill>/SKILL.md`
- **Generated (Cursor):** `.cursor/skills/<skill>/SKILL.md` — overwrite on sync
- **Drift check:** `python3 scripts/sync_portable_skills.py --verify`
- **Skill validation:** `python3 scripts/validate_skills.py`

Before commit, ensure portable source and generated host files match.

## Return paths

- [skills/README.md](../../skills/README.md)
- [skills/_schema.md](../../skills/_schema.md)
- [skills/runbooks/README.md](../../skills/runbooks/README.md)
- [docs/harness-architecture-map.md](../harness-architecture-map.md)
