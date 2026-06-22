---
name: source-clean
preferred_activation: source-clean
description: Post-land ASR and proper-noun cleanup for statecraft source-archive captures — caption/family scaffold, ph-civ series tiers, entity pass, thread/channel tiers, provenance patch. Not synthesis, wire-verify, or first-pass intake.
portable: true
version: 1.0.0
scope_class: repo-governed
tags:
- operator
- statecraft
- source-archive
- transcript
- quality
portable_source: skills/source-clean/SKILL.md
synced_by: sync_portable_skills.py
---
# Source clean (`source-clean`)

**Preferred activation:** **`source-clean`** on a landed `source-archive/statecraft/**/source-*.md` capture (or **`source clean`**).

**Scope:** Post-land mechanical cleanup only — scaffold residue, ASR tiers, expert-name tiers, YAML provenance. **Not** synthesis, notebook weave, or wire-verify.

**Subsumes (redirect):**

- [`transcript-proper-noun-normalization`](../transcript-proper-noun-normalization/SKILL.md) — proper-noun / ASR normalization
- [`transcript-cleanup`](../transcript-cleanup/SKILL.md) — deprecated; use this skill on archive captures instead of raw-input `*.cleaned.md` derivatives

**Thin wrapper:** `python scripts/normalize_statecraft_source_asr.py <path> --write` runs the same ASR + tier stack **without** scaffold (legacy CLI).

## Use this skill when

- A capture is landed via [`statecraft-source-intake`](../statecraft-source-intake/SKILL.md) but YouTube / operator-paste ASR noise blocks search, shelf routing, or in-voice study
- Names, places, weapons, acronyms, or recurring corpus terms are mangled but argument structure should stay intact
- Operator wants one orchestrated pass instead of ad hoc script chains

## Do not use when

- Source is not yet in `source-archive/statecraft/` — run **source-intake** first
- Job is wire triage on desk hooks — use [`wire-verify`](../wire-verify/SKILL.md)
- Job is interpretive synthesis or notebook fold — strategy / conductor lanes

## Pipeline (order fixed)

1. **Caption + family scaffold** — `post_land_statecraft_family.apply_statecraft_capture_scaffold` (skip with `--no-scaffold`)
2. **ph-civ series tier** — `asr_light_clean.normalize_transcript_text` (`--series auto|none|…`)
3. **Common entity pass** — `fix_statecraft_common_asr_entities`
4. **Thread / channel tiers** — `source_clean_tiers` (from YAML `thread`, `threads`, `guest_people`, `channel_slug`)
5. **Frontmatter patch** — `kind: cleaned-transcript`, `transcript_type`, `editorial_note`, `source_note` tail

## Default execution (Windows-safe)

**One shell, one path** — do not subprocess-loop per file on Windows.

```bash
python scripts/source_clean_statecraft.py --path source-archive/statecraft/YYYY-MM-DD/source-<slug>.md
python scripts/source_clean_statecraft.py --path <path> --dry-run
python scripts/source_clean_statecraft.py --day YYYY-MM-DD --with-index
python scripts/source_clean_statecraft.py --path <path> --no-scaffold
```

Agents: import `source_clean_statecraft.clean_capture` in-process for batch work — never wrap the CLI in a per-file subprocess loop.

## Contract

- Normalize only **mechanically recoverable** forms (repo tiers, speaker shelves, obvious ASR)
- Do **not** rewrite argument, summarize, smooth grammar, or upgrade to human-verified verbatim
- Preserve prior `editorial_note` provenance markers (trim/sponsor/cold-open) when merging
- Never hide uncertainty — leave ambiguous terms or note in `editorial_note`

## Closeout

Report:

- substitution counts: **series / entity / thread** and **total**
- whether **body** and **frontmatter** changed
- tier keys resolved from frontmatter
- idempotent re-run (expect **0** subs when already clean)
- git durability: on disk / not committed / not pushed

## Cursor / strategy-codex instance

**Windows fail-over (manual ASR after `source-clean`):** if Shell or `python -c` batch replace **interrupts** on the capture path, stop Shell for that thread and patch via `StrReplace` or one full-file `Write` (post-land cleanup only — not initial sidecar intake); do not retry the same batch shape. RLJ: [§ 2026-06-21 post-land ASR fail-over](../../statecraft/recursive-learning-journal.md#2026-06-21---post-land-asr-cleanup-shell-fail-over-windows) · [agent-tool-latency-discipline.mdc](../../.cursor/rules/agent-tool-latency-discipline.mdc).

## Verification / Proof Standard

**Pass when:**

1. `python scripts/source_clean_statecraft.py --path <capture>` exits 0 (or `--dry-run` preview matches intent).
2. Closeout reports **series / entity / thread** substitution counts and whether body/frontmatter changed.
3. Re-run on same file yields **0** new substitutions when already clean.
4. Transcript argument preserved; `editorial_note` still marks not human-verified verbatim.

**Fail when:** synthesis or summarization in body; upgraded to human-verified without audio check; Shell/`python -c` batch retried on same path after interrupt (use Cursor fail-over above).

## Related

- Intake: [`statecraft-source-intake`](../statecraft-source-intake/SKILL.md) — optional post-land **`source-clean`**
- Tier SSOT: `scripts/source_clean_tiers.py`
- Entity SSOT: `scripts/fix_statecraft_common_asr_entities.py`
