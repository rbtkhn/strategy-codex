# Karajan Worktree Steward Review - 2026-05-14

## Scope

This packet classifies the remaining dirty tree after the benchmark receipt commit `4aa56a12`.
It is a steward review artifact only: no protected Record surface, runtime bundle, generated export, or Predictive History corpus material is staged here.

## A. Allegro - Three Remaining Arcs

1. **Predictive History / speaker corpus ingestion**
   - Surfaces: `codex/years/2026/**`, `codex/predictive-history/**`, `codex/years/2026/raw-input/**`, speaker helix/cross-year files.
   - Shape: largest volume arc, including the 2025-08-21 raw transcript expansion and many untracked corpus/source files.
   - Value: high if this repo is still carrying transition/reference work.
   - Risk: high because AGENTS.md marks Predictive History material in `strategy-codex` as frozen migration residue unless a boundary-maintenance doc says otherwise.
   - Label: **hold**.

2. **Generated/runtime and Record-adjacent residue**
   - Surfaces: `runtime/bundle/**`, `platform/users/grace-mar/runtime/bundle/**`, `last-dream.json`, `merge-receipts.jsonl`, `pipeline-events.jsonl`, `runtime/artifacts/memory/**`, root Record-adjacent files.
   - Shape: runtime exports, logs, observability outputs, and protected companion surfaces mixed together.
   - Value: operationally useful as evidence of recent runs, but not a clean source commit arc.
   - Risk: highest because protected files include `self.md`, `self-archive.md`, `recursion-gate.md`, and `self-memory.md`.
   - Label: **protected / local-only / hold**, depending on file.

3. **Work-dev / work-cici tooling and documentation**
   - Surfaces: `docs/skill-work/work-cici/**`, `scripts/*.py`, `tests/fixtures/**`, work-dev capability cache files.
   - Shape: smaller and more finishable; includes a clean cici-ai member-profile packet plus a noisier script/cache subset.
   - Value: high because it turns team support review into a repeatable repo-visible process.
   - Risk: moderate overall, low for the member-profile docs, higher for BOM/mojibake and cache churn in other files.
   - Label: **candidate commit**, after separating clean docs/tooling from cache and encoding noise.

## B. Andante - Ranked Steward Buckets

| Rank | Bucket | Arc value | Risk | Protected exposure | Finish-readiness | Steward label |
|---:|---|---|---|---|---|---|
| 1 | `docs/skill-work/work-cici/member-profiles/**` + `scripts/cici_support_review.py` | High | Low | None seen | High | candidate commit |
| 2 | `scripts/ab_test_voice.py`, `scripts/bootstrap_work_politics.py`, `scripts/eval_identity_delta.py`, `scripts/validate_expert_profiles.py` | Medium | Medium | Indirect only | Medium | candidate after diff review |
| 3 | `scripts/propose_think_claims_from_read.py`, `tests/fixtures/self_memory_normalize_telemetry_note.md` | Medium | Medium-high | Indirect Record references | Low until encoding fixed | hold |
| 4 | `docs/skill-work/work-dev/.capability-shift-*` | Low | Low | None | Low | local/generated cache |
| 5 | `codex/years/2026/**`, `codex/predictive-history/**` | High | High | Boundary-sensitive | Low | hold |
| 6 | `runtime/bundle/**`, `platform/users/grace-mar/runtime/bundle/**`, JSONL run logs | Medium | High | Runtime/Record-adjacent | Low | local-only / generated |
| 7 | `self.md`, `self-archive.md`, `recursion-gate.md`, `self-memory.md` | Record-critical | Highest | Direct | Not eligible | protected |

## C. Scherzo - Narrow Finishing Slice Executed

Selected slice: **cici-ai member-profile support review**.

Reason: it is the cleanest small arc in the remaining tree. It has a coherent directory, a source script, a generated-but-reviewable support snapshot, and index/README pointers. It does not touch protected Record surfaces, runtime bundles, Predictive History corpus, or generated profile exports.

Action taken:

- Kept the slice bounded to `docs/skill-work/work-cici/member-profiles/**`, `docs/skill-work/work-cici/INDEX.md`, `docs/skill-work/work-cici/README.md`, and `scripts/cici_support_review.py`.
- Repaired the Telegram output dash in `scripts/cici_support_review.py` to ASCII `-`.
- Left the broader script/default-path cleanup and capability cache churn out of the finish slice.

Next validation for this slice:

```powershell
python scripts/cici_support_review.py --format markdown
python scripts/cici_support_review.py --format telegram
```

If committed later, the staged intent should be only the cici-ai member-profile packet and the support-review script.
