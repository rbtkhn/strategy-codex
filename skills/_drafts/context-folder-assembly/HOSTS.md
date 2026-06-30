# strategy-codex host notes (context-folder-assembly)

Move into `.cursor/skills/context-folder-assembly/CURSOR_APPENDIX.md` on promotion to manifest.

## Working root

```text
runtime/prepared-context/working/<slug>/
```

Gitignored (see repo `.gitignore`). Ephemeral scratch — not Record.

**Slug:** kebab-case, unique, task-descriptive (e.g. `persia-march-synthesis`, `conductor-kleiber-followup`).

## Discovery hints

Search under:

- `docs/skill-work/`
- `continuity/`
- `statecraft/`
- `runtime/artifacts/` (read-only sources; do not treat as SSOT)
- `skills/`

Use Grep, SemanticSearch, and Read. Prefer **meaning** over exact filenames when the operator describes sources.

## Optional lane orient

```bash
python3 scripts/compress_active_lane.py --lane work-strategy
```

Copy output to `runtime/prepared-context/working/<slug>/lane-orientation.md` if useful.

## Questions-as-spec template

Host template: [docs/skill-work/questions-as-spec-template.md](../../../docs/skill-work/questions-as-spec-template.md)

PLAN lane: [docs/operator-agent-lanes.md](../../../docs/operator-agent-lanes.md) — PLAN — questions-as-spec.

## Fresh-thread opener (paste into new Cursor chat)

```text
EXECUTE — Read only runtime/prepared-context/working/<slug>/ (all files there).
Do not search the wider repo unless task-shape.md explicitly allows it.
Execute task-shape.md. questions.md defines success standards.
```

## Bridge handoff

If the task spans sessions, note the active slug in the next **bridge** packet under **Open loops** — e.g. `runtime/prepared-context/working/<slug>/` in progress.

## Copy discipline

- Use file copy, not move.
- Record every copy in `sources-index.md`.
- Do not commit `runtime/prepared-context/working/` — shipped work lands in normal repo paths via EXECUTE.
