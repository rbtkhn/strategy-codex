---
name: civ-state-volume-architect
preferred_activation: civ-state-volume-architect
description: >-
  Create, refound, or normalize CIV-STATE volume architecture in
  statecraft/states. Use when the operator wants to define or enforce the
  canonical volume-part law, rename or add chapter families, rewire volume
  READMEs, or keep Civilization and Empire distinct while placing
  geo-strategy, secret-history, and game-theory as optional sub-lenses beneath Empire.
---

# CIV-STATE Volume Architect

Use this skill to shape the architecture of `statecraft/states/volumes/` as a stable book-form, not a pile of files.

This skill is for **volume law and chapter-family design**. It decides what parts a volume has, what each part is for, how the front door routes into them, and how subordinate essays sit beneath them.

It is **not** the same as `civ-state-volume-harden`. That skill strengthens an already-defined front door or volume case. This skill changes or enforces the deeper architecture itself.

## Use this skill when

- the operator wants to define or revise the canonical parts of a CIV-STATE volume
- chapter families are being added, renamed, retired, or demoted
- a volume README opener block needs to be rebuilt around a new part order
- `geo-strategy`, `secret-history`, and `game-theory` need to be treated as subordinate lenses rather than peer top-level parts
- bridge doctrine or promotion doctrine must be updated because a new CIV-STATE destination family now exists
- multiple volume folders need to be kept structurally parallel during a shelf-wide change

## Do not use this skill when

- the task is just polishing one already-correct essay
- the operator wants a live object diagnosed through the governing pair framework
- the work is PH-CIV public authoring or transcript maintenance
- the task belongs to lane-local transaction drafting rather than CIV-STATE architecture

## Core law

- A CIV-STATE volume is a guided book-form, not a flat bundle.
- `README.md` is the front door, not a chapter.
- The current canonical reader volume order is:
  1. `introduction.md`
  2. `civilization-<civ>.md`
  3. `empire-<civ>.md`
- `geo-strategy-<civ>.md`, `secret-history-<civ>.md`, and `game-theory-<civ>.md` are optional sub-lenses beneath **Empire**.
- Legacy `statecraft-<civ>.md` files may remain on disk for workshop merge; they are not reader-facing volume parts.
- Legacy support files may remain on disk, but they must stop pretending to be canonical if doctrine has moved past them.

## Required checks

For any CIV-STATE architecture pass, resolve these explicitly:

1. What are the canonical top-level parts now?
2. What files are subordinate rather than coequal?
3. What exact order should the volume opener block show?
4. What shelf doctrine must change in `statecraft/states/volumes/README.md`?
5. What bridge or promotion notes must be updated so the membrane matches the new destination set?

If any of those five are still fuzzy, the architecture pass is not finished.

## Workflow

1. **Name the active volume law first.**
   State the current canonical part order in one line before editing files.

2. **Separate top-level parts from subordinate lenses.**
   Decide what the volume opens through and what it descends into.
   Never let subordinate essays silently masquerade as coequal parts.

3. **Lock each part's job.**
   Distinguish clearly:
   - `Introduction` orients the case in the five-volume arc
   - `Civilization` legitimates the core
   - `Empire` exposes outward instrument and civilizational entropy

4. **Set file naming before prose expansion.**
   Resolve whether the family is generic or named-per-civilization first.
   Avoid writing full chapter bodies before the filename law is stable.

5. **Rewire the opener block and the volume shelf together.**
   Do not change one without the other.
   The per-volume `README.md` files and [statecraft/states/volumes/README.md](../../../statecraft/states/volumes/README.md) should tell the same story.

6. **Update membrane surfaces when destination classes change.**
   If a new family becomes canonical, update:
   - [PH-CIV to CIV-STATE bridge](../../../statecraft/states/ph-civ-to-civ-state-bridge.md)
   - [PH-CIV promotion ledger](../../../statecraft/states/ph-civ-promotion-ledger.md)

7. **Mark residue honestly.**
   If an older file remains on disk for continuity, label it as support, legacy, or drill-down rather than letting it compete with the new architecture.

8. **Validate parallelism across all five volumes.**
   Check that each volume folder contains the same top-level families and that opener-block ordering matches the shelf law.

## Volume chapter doctrine

Use this as the default constitutional shape unless the operator explicitly supersedes it:

- `introduction.md`
  - case entry in the five-volume arc
  - sovereignty chain narrative and read path

- `civilization-<civ>.md`
  - legitimacy-bearing core
  - continuity-bearing civilization argument

- `empire-<civ>.md`
  - outward-instrument essay
  - projection stack
  - coercion, finance, logistics, alliance, maintenance, overreach, civilizational entropy

Optional sub-lenses beneath **Empire**:

- `geo-strategy-<civ>.md`
- `secret-history-<civ>.md`
- `game-theory-<civ>.md`

### Multi-term essay membrane (six `{civ}-{term}.md` volumes)

When a volume adds parallel term theory files (civilization · empire · faith · science · memory · entropy), essays split into **three tiers** — constitutional · history sub-lens · hexagonal demonstrator. Stand up **connectivity map → hexagonal template → registry → bodies → Bridge blocks** before demonstrator encode; essays **link term SSOT**, never extend rosters.

Machine law: [essay-membrane-law.md](../../../statecraft/patterns/essay-membrane-law.md) · Rome proof: [connectivity-rome.md](../../../public/civ-state/volumes/rome/theory/connectivity-rome.md).

Legacy (workshop merge target, not reader-facing):

- `statecraft-<civ>.md`

Workshop-only support notes (not exported):

- `sovereign-continuity.md`

## Public export gate (v0.1.3+)

When reader volume law changes or a public release is tagged, run this pass — do **not** use `--validate` on the export script (that flag does not exist).

1. **Workshop links** — shelf-readers and `secondary-sources` route upward to `introduction.md`, `civilization-*.md`, or `empire-*.md`; never `statecraft-*.md` on reader paths.
2. **Export** — `python3 scripts/export_civilizational_statecraft_public.py` (optional `--output runtime/artifacts/civilizational-statecraft-public`).
3. **Validate** — `python3 scripts/validate_civilizational_statecraft_public.py runtime/artifacts/civilizational-statecraft-public`.
4. **Confirm** — no `volumes/*/statecraft-*.md` in staging; each volume has `introduction.md`; tree hash recorded in `EXPORT-RECEIPT.md`.

Manifest SSOT: [`platform/config/civilizational_statecraft_public_export.yaml`](../../../platform/config/civilizational_statecraft_public_export.yaml) — `volume_essay_globs` gates what ships; export script excludes workshop-only files and prunes legacy volume artifacts after write.

Boundary: [`docs/civilizational-statecraft-external-boundary.md`](../../../docs/civilizational-statecraft-external-boundary.md).

## Architectural guardrails

- Do not let README count as a chapter.
- Do not let Part 3 (`statecraft-*.md`) re-enter the reader-facing or public export path.
- Do not let `Empire` absorb `Civilization`.
- Do not let subordinate lenses silently retake top-level status.
- Do not leave bridge doctrine behind after a chapter-family change.
- Do not delete legacy files casually when a support-note role would preserve continuity more safely.
- Do not widen into lane-local rewriting unless the operator explicitly expands scope.

## Default output shape

When answering with an architectural recommendation, prefer:

```markdown
**CIV-STATE volume law**
- Canonical top-level parts:
- Subordinate lenses:
- Opener block order:
- Shelf doctrine changes:
- Membrane changes:
- Legacy residue treatment:
```

## Success condition

This skill succeeds when a CIV-STATE volume reads like a stable constitutional book-form: the top-level parts are clear, subordinate lenses are properly nested, the shelf and volume fronts agree, and future chapter writing can proceed without reopening structural confusion.

## strategy-codex instance notes

- Canonical shelf front door: [statecraft/states/README.md](../../../statecraft/states/README.md)
- Canonical volume map: [statecraft/states/volumes/README.md](../../../statecraft/states/volumes/README.md)
- Primary membrane notes:
  - [ph-civ-to-civ-state-bridge.md](../../../statecraft/states/ph-civ-to-civ-state-bridge.md)
  - [ph-civ-promotion-ledger.md](../../../statecraft/states/ph-civ-promotion-ledger.md)
  - [essay-membrane-law.md](../../../statecraft/patterns/essay-membrane-law.md) — three-tier essay routing for multi-term volumes
- Companion architecture-adjacent skills:
  - [civ-state-volume-harden](../civ-state-volume-harden/SKILL.md)
  - [statecraft-framework](../statecraft-framework/SKILL.md)

## Preferred validation commands after skill edits

```powershell
python3 scripts/export_civilizational_statecraft_public.py --dry-run
python3 scripts/validate_civilizational_statecraft_public.py runtime/artifacts/civilizational-statecraft-public
python scripts/validate_skills.py
```
