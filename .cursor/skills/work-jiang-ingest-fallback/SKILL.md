---
name: work-jiang-ingest-fallback
description: Recover lecture ingest when channel-wide transcript fetch hits rate limits by using a targeted local index row, then ingest and validate in a bounded pass.
preferred_activation: jiang ingest fallback
activation: jiang ingest fallback
portable: true
version: 0.1.0
category: domain-pack
status: active
scope_class: repo-governed
tags:
- operator
- work-jiang
- ingest
portable_source: skills/work-jiang-ingest-fallback/SKILL.md
synced_by: sync_portable_skills.py
---
# Work-jiang ingest fallback (rate limit path)

**Preferred activation (operator):** say **`jiang ingest fallback`**.

Use this skill when ingesting a new lecture and the normal channel-wide transcript refresh is blocked (for example, repeated `429 Too Many Requests` during fetch), but you still need to complete a clean, auditable ingest now.

## When to run

- New lecture ingest is blocked by rate limits during full channel fetch.
- Episode metadata is known (title + video id), but local index is stale.
- You want a narrow fallback that preserves normal ingest and validation steps.

## Workflow

1. **Capture transcript input**
   - Save operator transcript text to an intake file under your work-jiang intake area.
   - Keep the transcript source explicit so ingest provenance is clear.

2. **Avoid brittle full-channel retries**
   - If full refresh is returning repeated `429` or hanging, stop it.
   - Switch to a targeted single-episode path rather than looping retries.

3. **Create a minimal local index override**
   - Write a one-row markdown index table with: `video_id`, title, and canonical watch URL.
   - This lets `ingest_lecture.py` resolve episode metadata without waiting on channel refresh.

4. **Run ingest with explicit override**
   - Execute `ingest_lecture.py` for the intended series/episode with:
     - `--file` for transcript input
     - `--index` pointing at the local one-row override
     - `--asr` when transcript normalization is desired
   - Confirm the target lecture file path and heading printed by the ingest command.

5. **Run post-ingest validators**
   - Execute work-jiang validators used in your lane.
   - Confirm metadata and dashboard artifacts regenerate without errors.

6. **Report and classify changed files**
   - Separate core ingest artifacts (lecture + metadata/status updates) from temporary fallback intake files.
   - Recommend whether to keep or drop the temporary local index override before commit.

## Guardrails

- Do not treat fallback index files as canonical source registry.
- Do not skip validation just because ingest succeeded.
- Keep commits focused: exclude unrelated local noise from the ingest commit.
- This is WORK-lane operational tooling, not Record merge flow.

## Command skeleton (adapt to host repo)

```bash
# Optional normal attempt (can be skipped if known rate-limited)
python3 scripts/fetch_youtube_channel_transcripts.py --channel "<channel-url>" --output-dir "<output-dir>" --resume

# Fallback ingest with explicit local index
python3 scripts/work_jiang/ingest_lecture.py <series> <episode> \
  --file <intake-transcript-path> \
  --index <local-one-row-index-path> \
  --asr

# Validation block (trim only if lane policy allows)
python3 scripts/work_jiang/validate_work_jiang.py --require-analysis-frontmatter
python3 scripts/work_jiang/validate_argument_layer.py
python3 scripts/work_jiang/validate_comparative_layer.py
```


## Cursor / strategy-codex instance

Grace-mar paths and commands for this repository (from `.cursor/skills/work-jiang-ingest-fallback/`).

| Topic | Path |
|--------|------|
| Work-jiang lane guide | [codex/predictive-history/README.md](../../codex/predictive-history/README.md) |
| Transcript workflow | [codex/predictive-history/WORKFLOW-transcripts.md](../../codex/predictive-history/WORKFLOW-transcripts.md) |
| Intake directory | [codex/predictive-history/intake/](../../codex/predictive-history/intake/) |
| Lectures directory | [codex/predictive-history/lectures/](../../codex/predictive-history/lectures/) |
| Canonical checklists | [work-jiang-feature-checklist](../work-jiang-feature-checklist/SKILL.md) |
| Ingest command script | [scripts/work_jiang/ingest_lecture.py](../../../scripts/work_jiang/ingest_lecture.py) |
| Validation scripts | [scripts/work_jiang/validate_work_jiang.py](../../../scripts/work_jiang/validate_work_jiang.py), [validate_argument_layer.py](../../../scripts/work_jiang/validate_argument_layer.py), [validate_comparative_layer.py](../../../scripts/work_jiang/validate_comparative_layer.py) |
| Portable skill manifest | [skills/manifest.yaml](../../../skills/manifest.yaml) |
| Sync script | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |

**Operator note:** For the fallback path, keep one-row local index files scoped to a single ingest turn; decide before commit whether to keep them as audit artifacts or remove them as temporary scaffolding.
