# Kleiber Composition Benchmark

**Status:** work-layer protocol. Not Record. Not a gate substitute.

## Purpose

The Kleiber composition benchmark calibrates Strategy-codex composition quality for pages, chapters, books, and civ-mem reasoning. V1 is for system calibration first and model comparison second.

Kleiber owns this benchmark because the work needs selectivity: one bounded harness, one execution route, one closeout language, and explicit refusal of sprawl.

## Execution Route

V1 benchmarks run from exactly one place:

```text
Conductor action MCQ - Reply A-D for this kleiber pass
D. Finale: Run composition benchmark - execute one Strategy-codex composition benchmark and close with Held / Weakened / Broke / Open
```

Coffee may route to Conductor/Kleiber, but coffee does not run benchmarks directly. Dream may carry forward benchmark results, but dream does not generate or run benchmarks.

No other conductor owns benchmark execution in V1.

## Output Location

Store benchmark outputs under:

```text
artifacts/benchmarks/composition/
```

Suggested run folder:

```text
artifacts/benchmarks/composition/YYYY-MM-DD/<model-or-provider>/
```

Each run should include the prompt, model output, scoring notes, and closeout result. Keep this tree non-canonical and work-layer only.

## Required Metadata

Every run should record:

| Field | Requirement |
|-------|-------------|
| `benchmark_id` | One of `task-4`, `task-6`, `task-10`, `cm-1-humanoid-robots` |
| `prompt_version` | Use `composition-benchmark-v1` plus task-specific ID |
| `rubric_version` | Use `composition-rubric-v1` or `cm-1-rubric-v1` |
| `model` | Public model name as displayed by the provider |
| `provider` | Model provider |
| `model_version` | Exact version or release label when available |
| `run_date` | Local date of run |
| `temperature` | Sampling temperature, or `unknown` |
| `seed` | Fixed seed when available, otherwise `unavailable` |
| `source_mode` | `prompt_only`, `source_pack`, or `live_lookup` |
| `evaluator` | Human or agent evaluator name |
| `notes` | Brief caveats, source constraints, or anomalies |

For current-world tasks, especially CM-1, do not let model confidence outrun source mode. If the run uses live lookup, cite retrieval date in the run notes.

## Current-World Rubric Checklist

Every current-world composition benchmark must include:

- `source_mode`: `prompt_only`, `source_pack`, or `live_lookup`
- one line separating verified evidence from interpretation
- one line naming the weakest factual link
- no current-company or current-event claim unless supported by the selected source mode
- Call / Falsifier / Revisit that changes when source evidence changes the frame

This checklist is the permanent lesson from the first CM-1 recursion: a page can hold as composition while still leaving factual grounding untested. Future Strategy-codex benchmark runs must preserve that distinction instead of treating a fluent page as a fully grounded page.

## V1 Tasks

### Task 4 - GLP-1 / Real Food Experiences

**Target:** `strategy-page`

Write a complete `strategy-page` about a believable near-future world where GLP-1 drugs have eliminated hunger but created a black market for "real food experiences."

Follow the official page template:

- Chronicle
- Reflection
- Predictive Outlook with explicit Call, Falsifier, and Revisit
- Appendix if needed

Score structural incentives, plausible world-building, call quality, falsifier quality, and revisit discipline. Maximum 650 words.

### Task 6 - AI Co-Author Fired Me

**Target:** `strategy-chapter`

Write a complete `strategy-chapter` titled "What I Learned About Being Human the Day My AI Co-Author Fired Me."

Follow the official chapter template:

- Chronicle
- Reflection
- References

Score reflective continuity, human stakes, chapter-level synthesis, and whether the chapter points toward page-level work without duplicating a full page body. Maximum 650 words.

### Task 10 - AI Writing Got Worse

**Target:** `strategy-book`

Write a compact `strategy-book` scaffold about an author who becomes convinced AI writing has gotten worse, then discovers the twist is more interesting than the initial belief.

Follow the official book template:

- Theme
- Chapter index
- Carry-forward tensions
- Synthesis notes

Score recursive synthesis, book-scale structure, non-generic judgment, and unresolved tension handling. Maximum 650 words.

### Task CM-1 - Effective Use of Civilizational Memory

**Target:** `strategy-page`

**Secondary target:** `strategy-chapter` or `strategy-book` synthesis

CM-1 is the flagship V1 benchmark.

```prompt
You are operating inside a Strategy-codex governed system. Write a complete strategy-page on the following topic.

Topic: The current wave of humanoid robot scaling (Figure, 1X, Tesla Optimus, etc.) and its implications for labor, meaning, and the civilizational operating system.

Requirements:
- Use civilizational memory (civ-mem) as a mechanism, not decoration.
- Explicitly perform the full civ-mem sequence:
  1. State the historical/civilizational pattern or precedent.
  2. Explain why it appears to fit the current situation.
  3. Explain where and why it may not fit (mismatches, changed conditions).
  4. State what would falsify the analogy.
  5. Show how this civ-mem analysis changes or sharpens the strategic call.

Follow the official strategy-page template:
- Chronicle
- Reflection (with civ-mem section clearly labeled)
- Predictive Outlook (with explicit Call, Falsifier, and Revisit horizon)
- Appendix if needed

Style rules:
- Do not name-drop historians or events for aesthetic effect.
- Label analogy strength clearly (illustrative / mechanistic / strong parallel).
- Preserve live tensions; do not force false consensus.
- Separate empirical claims from interpretation.
- Maximum 650 words.

Write the full strategy-page now.
```

## Template Wiring

V1 is wired to these canonical templates:

- `codex/strategy-codex-template-page.md`
- `codex/strategy-codex-template-chapter.md`
- `codex/strategy-codex-template-book.md`

The benchmark should score template fit against those files, not against generic essay expectations.

## General Scoring Rubric

Score each dimension from 1 to 5. Each score must include a one-sentence rationale and optional confidence: `low`, `medium`, or `high`.

| Dimension | 5 | 3 | 1 |
|-----------|---|---|---|
| Template fit | Follows the target template cleanly | Uses most required sections | Ignores or distorts template |
| Strategic judgment | Makes a useful call or synthesis | Offers mild judgment | Mostly summary or vibes |
| Falsifiability | Names concrete falsifiers and revisit conditions | Names a vague falsifier | No meaningful falsifier |
| Tension preservation | Holds live contradictions honestly | Partially flattens tensions | Forces false resolution |
| Voice and memorability | Specific, forceful, human-readable prose | Competent but generic | Generic or bloated prose |

## CM-1 Civ-Mem Rubric

| Dimension | 5 | 3 | 1 |
|-----------|---|---|---|
| Mechanism vs ornament | Civ-mem drives the strategic insight | Civ-mem is present but not central | Name-dropping or aesthetic only |
| Fit / mismatch balance | Strong fit and nuanced mismatch both shown | Basic fit and limits mentioned | Only fit, no critique |
| Falsifier quality | Concrete, observable falsifier | Vague falsifier | No falsifier |
| Strategic impact | Civ-mem clearly sharpens the Call | Mildly relevant to judgment | No impact on strategic judgment |
| Tension preservation | Contradictions remain visible | Some flattening | Forced consensus |
| Labeling discipline | Analogy strength explicitly labeled | Inconsistent labeling | No strength label |

## Closeout Mapping

Use one closeout label per run:

| Label | Rule |
|-------|------|
| `Held` | No dimension below 4 |
| `Weakened` | At least one dimension at 3, none below 3 |
| `Broke` | Any core dimension below 3 |
| `Open` | Incomplete run, insufficient evidence, source-mode problem, or evaluator cannot score confidently |

Dream may carry forward only `Open`, `Broke`, or `Weakened` twice on the same dimension. Dream does not create or run benchmark prompts.

## Acceptance Check

After implementation or benchmark runs, verify governed Record surfaces were not changed for this work:

```bash
git diff -- self.md self-archive.md recursion-gate.md session-log.md bot/prompt.py
```

Any output in that diff must be explained as pre-existing residue or reverted if introduced by the benchmark work.
