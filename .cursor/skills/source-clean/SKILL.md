---
name: source-clean
description: Post-land ASR and proper-noun cleanup for statecraft source-archive captures — caption/family scaffold, ph-civ series tiers, entity pass, thread/channel tiers, provenance patch. Not synthesis, wire-verify, or first-pass intake.
preferred_activation: source-clean
activation: source-clean
portable: true
version: 1.1.2
category: truth-pipeline
status: active
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

## Verification / Proof Standard

Report:

- substitution counts: **series / entity / thread** and **total**
- whether **body** and **frontmatter** changed
- tier keys resolved from frontmatter
- idempotent re-run (expect **0** subs when already clean)
- **residual ASR** — pattern grep hits after pass (see below); do not imply "fully clean" when hits remain
- git durability: on disk / not committed / not pushed

Do not call this complete unless:

- the input source, file, paste, URL, or archive path is named
- the output surface is named
- skipped steps are explicitly marked with a reason
- uncertainty, missing evidence, or unresolved source defects are stated
- source body preservation must be checked (line/word count stable; no scaffold truncation)

Evidence to report:

- files touched or produced
- scripts or commands run
- source URLs, archive paths, or transcript identifiers used
- confidence downgrade, if any
- `python scripts/source_clean_statecraft.py --path <capture>` exit 0 (or `--dry-run` preview matches intent)

If verification cannot be completed:

- state what was not verified
- stop before archive land, synthesis, publication, or promotion
- return a bounded partial result for operator review

## Intake ladder (automated → manual)

Default post-land sequence:

```text
source-intake land → source-clean → residual gap scan → optional manual ASR spot-fix → optional wire-verify → synthesis
```

- **`source-clean`** = tier-backed mechanical pass only.
- **`manual ASR spot-fix`** = operator/agent pass for **ambiguous** or **family-host** garbles tiers should not auto-fix (see below).
- Do **not** fold manual spot-fix into `source-clean` automation for ambiguous political names.

**Dialogue Works / EU–Iran lane:** thread tiers often run, but **EU leadership + MOU homophones + host address ASR** (`Kayakalas`, `Stormer`, `theou`, `carl`) may still need manual spot-fix even after a successful `source-clean` — especially on Baud-class episodes.

## Residual ASR gap scan (post-`source-clean`)

After `source-clean` (same turn or closeout), scan transcript body for high-signal residual patterns:

| Pattern (regex) | Typical fix lane |
| --- | --- |
| `Stormer\|Kayak\|theou\|theuou\|noou` | entity tier or manual Starmer/Kallas/MOU |
| `Lean River\|Leani River` | Litani (entity tier) |
| `Benavir\|Barau\|terrib Israel` | manual (Netanyahu; Baerbock?; context) |
| `carl the leader\|Welcome EL` | manual host-address (Colonel) |

**Offer manual spot-fix when:**

- automated **total < ~5** on a long interview capture, **or**
- any gap-scan pattern matches **and** the capture is headed to synthesis / quotation

Report: `automated N subs · residual hits: <list or none>`.

## `manual_asr_spot_fix` convention

Mirror Napolitano/Crooke receipt style on the capture frontmatter:

```yaml
manual_asr_spot_fix: YYYY-MM-DD — Starmer; Kaja Kallas; MOU/theou; Litani; …; tentative: Baerbock (Barau)
editorial_note: "Manual ASR spot-fix YYYY-MM-DD (N substitutions; see manual_asr_spot_fix); AI-assisted source-clean …"
```

Rules:

- List **fixed forms** and mark **tentative** guesses (`Barau→Baerbock`) — never upgrade to human-verified verbatim.
- Append `· manual ASR spot-fix YYYY-MM-DD` to `source_note` when disk landing manual work.
- Windows: one in-process Python patch pass or bounded `StrReplace` hunks — no Shell retry loops after interrupt.

Entity-tier SSOT for high-confidence repeats: `scripts/fix_statecraft_common_asr_entities.py` (labels `starmer_*`, `kallas_*`, `mou_*`, `litani_*`, …).

## Legacy captures and VTT guardrails

**Legacy heading shape:** some older captures use `# Raw Transcript` instead of `## Transcript`. Full `source_clean_statecraft.py` exits with `no transcript heading found`. **Fail-over:** entity-only `apply_replacements` from `fix_statecraft_common_asr_entities` + optional `entity_asr_pass` frontmatter receipt — do not force scaffold.

**VTT / manual subtitle captures:** `transcript_type: manual_subtitles_vtt` with large `body_word_count` and `verification_ok: true` — **do not** run full scaffold on these. Full `source-clean` can **truncate** the body (e.g. 1065 → 85 lines). Use **`--no-scaffold`** or entity-only pass; verify line count before and after (`abort` if body shrinks >5%).

```bash
python scripts/source_clean_statecraft.py --path <vtt-capture> --no-scaffold
```

Agents: import `fix_statecraft_common_asr_entities.apply_replacements` in-process; assert line count stable before write.

## Cursor / strategy-codex instance

**Windows fail-over (manual ASR after `source-clean`):** if Shell or `python -c` batch replace **interrupts** on the capture path, stop Shell for that thread and patch via `StrReplace` or one full-file `Write` (post-land cleanup only — not initial sidecar intake); do not retry the same batch shape. RLJ: [§ 2026-06-21 post-land ASR fail-over](../../../statecraft/recursive-learning-journal.md#2026-06-21---post-land-asr-cleanup-shell-fail-over-windows) · [agent-tool-latency-discipline.mdc](../../../.cursor/rules/agent-tool-latency-discipline.mdc).

## Related

- Intake: [`statecraft-source-intake`](../statecraft-source-intake/SKILL.md) — optional post-land **`source-clean`**
- Tier SSOT: `scripts/source_clean_tiers.py`
- Entity SSOT: `scripts/fix_statecraft_common_asr_entities.py`
