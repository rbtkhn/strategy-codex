# Capture templates

These templates support faster, more consistent **operator capture** in Grace-Mar’s work and pre-review layers (work territories, analysis, contradiction prep, staging drafts).

## What they are not

- **Not** canonical Record surfaces. They do **not** update SELF, SELF-LIBRARY, SKILLS, or EVIDENCE directly.
- **Not** a substitute for the Approval Inbox — candidate drafts are **pre-gate** thinking aids only.

## Scripts

| Template | Scaffold command |
|----------|------------------|
| [work-note-template.md](work-note-template.md) | `python3 scripts/new_work_note.py --lane <lane> --title "..."` |
| [evidence-stub-template.md](evidence-stub-template.md) | `python3 scripts/new_evidence_stub.py --source "..." --type <kind>` |
| [candidate-draft-template.md](candidate-draft-template.md) | `python3 scripts/new_candidate_draft.py --lane <lane> --target-surface SKILLS --title "..."` |
| [plan-for-plan.md](plan-for-plan.md) | Planning / pre-review aid; no scaffold command |
| [plan-mission.md](plan-mission.md) | Expanded execution plan / pre-review aid; no scaffold command |

Default output paths live under `artifacts/work-notes/`, `artifacts/evidence-stubs/`, and `artifacts/candidate-drafts/` (see each script’s `--help`). Use `--output` to place files elsewhere under the repo (for example `docs/skill-work/work-strategy/`).

`plan-for-plan.md` and `plan-mission.md` are planning aids, not Record surfaces, gate substitutes, or autonomous approval mechanisms. Use them to improve clarity before execution; any proposed Record change still follows `recursion-gate.md` and the governing doctrine.

Generated `*.md` files under those artifact trees are **gitignored by default** (like skill-card scratch); commit intentionally if you want to share a capture.

## See also

- [Runtime vs Record](../runtime-vs-record.md) — canonical vs operator scratch
- [Operator dashboards](../operator-dashboards.md) — derived visibility over artifacts
