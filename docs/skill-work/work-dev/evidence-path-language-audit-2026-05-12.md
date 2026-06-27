# Evidence path language audit - 2026-05-12

**Purpose:** Verify where repo doctrine still describes `self-evidence.md` too strongly relative to the canonical EVIDENCE body, `self-archive.md`.

**Scope:** Language audit only. This is a `work-dev` steward note, not a Record change and not a migration script.

## Short verdict

The repo does **not** have one uniform `self-evidence.md` problem.

It has three different classes of reference:

1. **Safe compatibility references**
   These correctly say that `self-evidence.md` is optional, legacy, or a fallback pointer.
2. **Historical or migration-bound references**
   These are accurate **for the time or layout they describe** and should not be mass-rewritten without losing provenance.
3. **Live doctrine overstatements**
   These still talk as if `self-evidence.md` were the active evidence body for operator continuity or merge inspection, and should be normalized.

The sharpest risk is class 3, because it teaches operators to look at the wrong surface first.

## Canonical rule

- `self-archive.md` is the canonical EVIDENCE body for this repo.
- `self-evidence.md` is an optional compatibility pointer only.
- Live operator doctrine should center `self-archive.md` and mention `self-evidence.md` only as a legacy or migration fallback.

## Class 1 - Safe compatibility references

These already tell the right authority story:

- [self-evidence.md](../../../self-evidence.md)
- [canonical-paths.md](../../canonical-paths.md)
- [instance-doctrine.md](../../../instance-doctrine.md)
- [architecture.md](../../architecture.md)
- [id-taxonomy.md](../../id-taxonomy.md)
- [glossary.md](../../glossary.md)
- fallback-aware scripts such as `detect_capture_gap.py`, `export_prp.py`, `session_brief.py`, and `harness_warmup.py`

No immediate cleanup needed beyond routine consistency.

## Class 2 - Historical or migration-bound references

These preserve older layouts, audits, ADRs, or migration-era assumptions. They may mention `self-evidence.md` strongly, but they are not teaching the active operator contract:

- [analysis-grace-mar-self-evidence.md](../../analysis-grace-mar-self-evidence.md)
- [ANALYSIS-GRACE-MAR-museum knowledge.md](../../ANALYSIS-GRACE-MAR-museum knowledge.md)
- ADRs under [docs/adr/](../../adr)
- migration/spec notes such as:
  - [companion-self-developer-plan.md](../../companion-self-developer-plan.md)
  - [data-layer-roadmap.md](../../data-layer-roadmap.md)
  - [development-handoff.md](../../development-handoff.md)
  - [grace-mar-core.md](../../grace-mar-core.md)

These should be handled case by case, ideally with dated-note or migration-note framing, not blind replacement.

## Class 3 - Live doctrine overstatements

These were the main operator-facing problem because they still centered `self-evidence.md` as the first evidence surface:

- [session-continuity-contract.md](session-continuity-contract.md)
- [INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md)
- [safety-story-ux.md](safety-story-ux.md)
- [three-compounding-loops.md](three-compounding-loops.md)
- [README.md](README.md)

These have now been normalized to center `self-archive.md`, with `self-evidence.md` mentioned only as a legacy-layout fallback where needed.

## Additional medium-priority residue

These still deserve follow-up because they influence operator habits, but they are less central than the five files above:

- [operator-brief.md](../../operator-brief.md)
- [operator-skills.md](../../operator-skills.md)
- [operator-console.md](../../operator-console.md)
- [openclaw-integration.md](../../openclaw-integration.md)
- [pipeline-map.md](../../pipeline-map.md)
- [we-read-think-self-pipeline.md](../../we-read-think-self-pipeline.md)

These are good candidates for the next evidence-path normalization pass.

## Steward conclusion

The correct fix is **not** "replace every `self-evidence.md` string in the repo."

The correct fix is:

1. normalize live operator doctrine first
2. preserve historical and migration documents as historical when that provenance matters
3. keep script fallbacks where legacy layouts are still supported
4. make `self-archive.md` the default surface in every place that teaches present-tense operator behavior
