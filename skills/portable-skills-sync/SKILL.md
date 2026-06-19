---
name: portable-skills-sync
preferred_activation: sync skills
description: "Sync portable skill cores into generated host Cursor SKILL.md files: manifest-driven assembly, optional host appendix, verify step before write. Triggers: skills-portable edit, manifest.yaml, CURSOR_APPENDIX, portable pipeline, run sync, verify portable skills."
portable: true
version: 1.1.0
scope_class: repo-governed
tags:
  - operator
  - work-dev
---

# Portable skills — sync to Cursor (host)

**Preferred activation (operator):** say **`sync skills`**.

Use this skill when **editing or adding** skills that follow the **portable core + host appendix** pattern: methodology lives under `skills/<skill>/SKILL.md`; instance-specific paths and commands live in a separate appendix file; the editor-facing `SKILL.md` under `.cursor/skills/` is **generated** — do not hand-edit it.

## Layout (generic)

| Piece | Role |
|-------|--------|
| `skills/<skill>/SKILL.md` | **Portable core** — frontmatter (`portable: true`, `name`, one-line `description`, `version`, optional `tags`) + methodology. **No** instance user directories or gated merge script names in the body (your manifest may forbid substrings — see verify step). |
| `.cursor/skills/<skill>/CURSOR_APPENDIX.md` | **Host-only** — real paths, doc links, commands for **this** clone. |
| `skills/manifest.yaml` | **Registry** — maps `source`, optional `appendix`, `target`, optional `scope_class`, and optional `verify_forbidden_substrings` for the portable **body** only. |
| `.cursor/skills/<skill>/SKILL.md` | **Output** — frontmatter gains `portable_source` and `synced_by`; body = core + `## Cursor / strategy-codex instance` + appendix. |
| `skills/runbooks/*.runbook.md` | **Composed workflows** — multi-skill orchestration; validate with `validate_skills.py`; not synced to Cursor by default. |

## When to run

- After any change to a portable core, `manifest.yaml`, or a `CURSOR_APPENDIX.md`.
- Before **commit** of skill changes (so the generated file matches source).
- When the operator says **verify portable skills**, **run skill sync**, or **regenerate Cursor skills**.

## Workflow

1. **Edit** the portable core and/or appendix; add or adjust a **manifest** entry if the skill is new.
2. **Verify** (no writes): run the repo’s sync script with `--verify`. Fix any reported issues (forbidden substring in portable body, multi-line `description`, missing `portable: true`).
3. **Sync**: run the same script without `--verify` to write targets.
4. **Commit** together: portable `SKILL.md`, appendix, `manifest.yaml`, and generated `.cursor/skills/.../SKILL.md` (plus any doc cross-links you touched).

## Commands (from repository root)

Replace `scripts/` if your tree uses a different path.

```bash
python3 scripts/sync_portable_skills.py --verify
python3 scripts/sync_portable_skills.py
python3 scripts/sync_portable_skills.py --dry-run
python3 scripts/sync_portable_skills.py --skill <skill-name>
python3 scripts/validate_skills.py
python3 scripts/validate_skills.py --strict-verification
```

## Scope and verification

- Optional **`scope_class`** on portable skills (`personal`, `project-local`, `repo-governed`, `public-portable`) — preserved in generated Cursor frontmatter; skill frontmatter is SSOT.
- Promoted skills should include **`## Verification / Proof Standard`** — see [skills/_schema.md](../../skills/_schema.md).
- **`validate_skills.py`** also validates runbooks under `skills/runbooks/`.

## Guardrails

- **Never** edit the generated `.cursor/skills/<skill>/SKILL.md` by hand — the next sync will overwrite it.
- **Drift tax:** The **canonical** file for each listed skill is **`skills/<skill>/SKILL.md`** (plus `CURSOR_APPENDIX.md`). Hand-fixing only the generated host `SKILL.md` **without** editing the portable core produces **silent divergence** until the next sync — treat that as a process bug, not a shortcut.
- Keep **policy and Record merge** details out of the portable core; they belong in host docs or the appendix.
- If `--verify` fails on **description**, ensure the YAML `description` value is a **single line** (no literal newline inside the string).

## Related concepts

- **Discovery ladder:** pointer backlog → `_drafts/` → portable core + manifest (see your repo’s `skills/README.md` if present).
- **Extract from session:** turning a thread into a new skill often starts a draft under `_drafts/` before manifest registration.
- **Runbooks:** composed workflows under `skills/runbooks/` — validate with `validate_skills.py`.

## Verification / Proof Standard

Do not call this complete unless:

- `python3 scripts/sync_portable_skills.py --verify` exits 0 when portable core or appendix changed
- generated `.cursor/skills/portable-skills-sync/SKILL.md` matches portable core after sync
- `scope_class` in generated frontmatter matches portable source

Evidence to report:

- `--verify` exit code
- list of files written by sync (or dry-run summary)
- `validate_skills.py` exit code when run after skill edits

If verification cannot be completed:

- state which step failed (verify, sync, validate)
- do not commit generated host skill without successful verify
