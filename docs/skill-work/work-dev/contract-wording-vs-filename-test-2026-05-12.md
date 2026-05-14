# Contract wording vs filename test - 2026-05-12

**Purpose:** Test one small normalization proposal against live scripts and doctrine before any rename, so the repo can distinguish a **wording problem** from a **filename dependency** problem.

**Scope:** Steward / `work-dev` diagnostic note only. No Record change. No rename performed.

## Proposal tested

Use explicit contract wording first:

- doctrine says what is **canonical**
- scripts may continue to support compatibility or repo-specific filenames
- only rename if tooling truly requires it

Two seam types were checked:

1. **Evidence path seam** — `self-archive.md` versus `self-evidence.md`
2. **Skill surface seam** — `skill-*.md` versus `self-skill-*`

## Result

The two seams behave differently.

### 1. Evidence path seam: mostly a wording problem

The continuity and runtime stack already prefers the canonical evidence body:

- [repo_io.py](/C:/dev/strategy-codex/scripts/repo_io.py) defines `CANONICAL_EVIDENCE_BASENAME = "self-archive.md"`
- [continuity_read_log.py](/C:/dev/strategy-codex/scripts/continuity_read_log.py) requires `self-archive.md`
- [test_continuity_read_log.py](/C:/dev/strategy-codex/tests/test_continuity_read_log.py) asserts `self-archive.md`
- [harness_warmup.py](/C:/dev/strategy-codex/scripts/harness_warmup.py), [session_brief.py](/C:/dev/strategy-codex/scripts/session_brief.py), and [openclaw_heartbeat.py](/C:/dev/strategy-codex/scripts/openclaw_heartbeat.py) all read `self-archive.md` first and only fall back to `self-evidence.md`

So the evidence-path blocker was **not** filename dependency in the active operator stack.

It was mainly **contract wording drift** in live docs, which taught people to inspect `self-evidence.md` first even though the scripts had already moved on.

**Conclusion:** For evidence-path normalization, wording was the main blocker; rename pressure is low.

### 2. Skill surface seam: genuinely a filename dependency problem

The repo's live tooling still depends directly on the split root filenames:

- [export_curriculum.py](/C:/dev/strategy-codex/scripts/export_curriculum.py)
- [export_runtime_bundle.py](/C:/dev/strategy-codex/scripts/export_runtime_bundle.py)
- [generate_profile.py](/C:/dev/strategy-codex/scripts/generate_profile.py)
- [generate_lesson_prompt.py](/C:/dev/strategy-codex/scripts/generate_lesson_prompt.py)
- [record_slice_loader.py](/C:/dev/strategy-codex/scripts/record_slice_loader.py)
- [validate-integrity.py](/C:/dev/strategy-codex/scripts/validate-integrity.py)
- multiple tests under [tests/](/C:/dev/strategy-codex/tests/)

These use:

- `skill-think.md`
- `skill-write.md`
- `skill-steward.md`

directly as concrete file paths.

At the same time, doctrine now correctly uses:

- `self-skill-think`
- `self-skill-write`
- `self-skill-steward`

as the **conceptual labels**.

So the skill-surface seam is **not** solved by wording alone if someone wants to rename files. A literal rename to `self-skill-*.md` would require real script and test migration work.

**Conclusion:** For skill-surface normalization, the blocker is partly wording but materially also **filename dependency**.

## The real lesson

Do not treat all naming ambiguity as one kind of problem.

- **Evidence-path ambiguity** was mostly a **teaching mismatch**: scripts already knew the right canonical file.
- **Skill-surface ambiguity** is a **split-contract reality**: doctrine and filenames are intentionally different today, and tooling still depends on the concrete `skill-*.md` names.

## Recommended handling

1. Fix **wording-first** seams where the tooling already reflects canonical truth.
2. Preserve **split contracts** where doctrine labels and concrete filenames intentionally differ.
3. Attempt a filename migration only when there is a deliberate script/test update plan.

## Steward conclusion

The repo does not have one generic normalization problem.

It has:

- a **contract wording** problem in the evidence-path seam
- a **real filename dependency** problem in the skill-surface seam

That distinction should govern future cleanup passes.
