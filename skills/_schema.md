# Portable skill schema (strategy-codex)

## Folder

```text
skills/<skill-name>/
  SKILL.md              # required
  examples/             # optional — few-shots, long samples
  HOSTS.md              # optional — install notes per vendor
```

## Frontmatter (portable `SKILL.md`)

| Key | Required | Notes |
|-----|----------|--------|
| `name` | yes | Stable id; folder name should match. |
| `description` | yes | **Single line.** Triggers, in/out contract, output shape hints (agent routing). |
| `portable` | yes | `true` — marks inclusion in sync manifest. |
| `version` | yes | Semver string for export/changelog. |
| `tags` | no | e.g. `[operator, work-politics]` for mirrors. |
| `requires` | no | Skill dependencies, e.g. `[handoff-check]`. Validator checks that listed skills exist under `.cursor/skills/`. |
| `scope_class` | recommended | Where the procedure belongs: `personal`, `project-local`, `repo-governed`, `public-portable`. Default implied: `repo-governed` for manifest-listed skills. Skill frontmatter is SSOT; optional manifest copy must match. |

### `scope_class` definitions

| Value | Meaning |
|-------|---------|
| `personal` | Operator private style, voice, habits, or preferences |
| `project-local` | One app, product, codebase, or client project |
| `repo-governed` | strategy-codex governed workflows (default for listed skills) |
| `public-portable` | Generic procedure safe for reuse outside this repo |

Drafts under `skills/_drafts/` may omit `scope_class` until promotion. Catalog **promoted** / **listed** labels in [catalog.md](catalog.md) are human discovery tags only — not validator input until an optional `status` frontmatter field exists.

## Body rules (portable core)

- Prefer **placeholders** for repo roots and script names in the main methodology.
- Put **host-specific paths** only in `.cursor/skills/.../CURSOR_APPENDIX.md`, not in the portable core.
- **Forbidden substrings** in core (enforced by `sync_portable_skills.py --verify` when configured): instance user dirs, merge scripts — keep those in the appendix.
- Prefer host-equivalent placeholders such as `<operator-profile>`, `<approval-process>`, or `<calendar-notebook>` when the portable methodology would otherwise assume repo-specific files.
- Portable cores may describe **proposal** or **stage-only** outputs, but should not imply direct merge authority on Record-bearing surfaces.

## Optional: Agent behavior norms (social contract)

Agent-facing skills may include a short subsection:

**`## Agent behavior norms`** (or `## Collaboration norms`)

Suggested bullets (adapt per skill):

- **Human authority** — Assist; do not treat automation as overriding user or companion intent on gated surfaces.
- **Brevity** — Default to concise outputs unless the operator asks for depth.
- **No silent overwrite** — Do not replace user- or companion-owned text without explicit consent.
- **Abstention** — When evidence is missing or upstream docs already state a fact, say so; avoid false gaps.
- **Leakage** — Do not inject private instance or Record details into outbound copy unless requested.

Norms belong in the **portable core** when they are **host-agnostic**. Instance merge policy and paths stay in **`CURSOR_APPENDIX.md`**.

Authoring guide: [docs/skills/skill-authoring-norms.md](../docs/skills/skill-authoring-norms.md).

## Required or recommended body section: Verification / Proof Standard

Every promoted portable skill should include a `## Verification / Proof Standard` section unless the skill is purely conversational and cannot reasonably verify output.

The section should answer:

1. What must be true before the skill can call the work complete?
2. What evidence should be reported?
3. What commands, files, links, tests, or receipts should be checked?
4. What should the agent say if verification cannot be completed?
5. What confidence downgrade or stop condition applies?

Prefer **command/file bullets**, not prose alone. Optional later: validator lint for at least one `- ` bullet under the section.

Suggested template:

```markdown
## Verification / Proof Standard

Do not call this complete unless:

- ...

Evidence to report:

- ...

If verification cannot be completed:

- state what was not verified
- downgrade confidence
- ask for operator review or stop
```

Validator behavior: drafts → info; manifest-listed missing section → warn; `--strict-verification` → error on manifest-listed.

## Generated `.cursor/skills/.../SKILL.md`

- Appends appendix under heading `## Cursor / strategy-codex instance`.
- Adds `portable_source` and `synced_by` to frontmatter for audit.

## Versioning

Bump `version` in portable `SKILL.md` when methodology meaningfully changes; re-run sync before commit.

## Portable core vs host glue (habit)

When adding or extending skills, label the layer explicitly:

| Layer | What it is | Examples |
|-------|------------|----------|
| **Portable core** | Reusable methodology; works across hosts after sync | `skills/<name>/SKILL.md` body, placeholders, `manifest.yaml` entries |
| **Host glue** | Editor- or instance-specific wiring | `.cursor/skills/.../CURSOR_APPENDIX.md`, Cursor-only paths, merge scripts named in appendix only |

This mirrors the open-connector vs proprietary-surface pattern: keep **protocol** (portable + validator) in the portable tree; keep **single-host UX** in generated host files. Default path for checks: `python3 scripts/validate_skills.py`; portable listing stays aligned with [README.md](README.md) discovery ladder.
