# Kleiber Composition Benchmark

**Status:** work-layer protocol. Not Record. Not a gate substitute.

## Purpose

The Kleiber composition benchmark calibrates Strategy-codex composition quality for pages, chapters, books, and civ-mem reasoning. V1 is for system calibration first and model comparison second.

Kleiber owns this benchmark because the work needs selectivity: one bounded harness, one execution route, one closeout language, and explicit refusal of sprawl.

## Execution Route

V1 benchmarks run from **Kleiber full** mode only — not the default **compact** Kleiber path (single-source wire-in, desync fix, one companion row).

Triggers for full mode:

- operator says **`kleiber finale`** or **`kleiber benchmark`**
- explicit **D. Finale** pick naming composition benchmark
- multi-source daily refresh close
- validator tranche close

```text
Conductor action MCQ - Reply A-D for this kleiber pass (full mode)
D. Finale: Run composition benchmark - execute one Strategy-codex composition benchmark, close with Held / Weakened / Broke / Open, and name the single next operator action
```

**Compact default** (`kleiber` alone): **D. Finale** = `log_cadence_event` + ship receipt — see [conductor SKILL — Kleiber sizing](../../../.cursor/skills/conductor/SKILL.md).

Coffee may route to Conductor/Kleiber, but coffee does not run benchmarks directly. Dream may carry forward benchmark results, but dream does not generate or run benchmarks.

No other conductor owns benchmark execution in V1.

## Actionability Close

Every benchmark closeout must translate the verdict into one operator-facing next action, or explicitly state `No next action recommended` with the reason. Do not end with only a folder path, artifact list, or verdict.

Use this mapping unless the evidence clearly says otherwise:

- `Held`: commit the artifact, rerun with a stronger source mode, promote one rule, or park as calibration residue.
- `Weakened`: name the repair target before rerun.
- `Broke`: name the failed assumption and stop expansion.
- `Open`: name the missing evidence or decision owner.

## Output Location

Store benchmark outputs under:

```text
runtime/artifacts/benchmarks/composition/
```

Suggested run folder:

```text
runtime/artifacts/benchmarks/composition/YYYY-MM-DD/<model-or-provider>/
```

Each run should include the prompt, model output, scoring notes, and closeout result. Keep this tree non-canonical and work-layer only.

## Required Metadata

Every run should record:

| Field | Requirement |
|-------|-------------|
| `benchmark_id` | One of `task-4`, `task-6`, `task-10`, `cm-1-humanoid-robots`, `cm-2-dopamine-flow-ai-creation` |
| `prompt_version` | Use `composition-benchmark-v1` plus task-specific ID |
| `rubric_version` | Use `composition-rubric-v1`, `cm-1-rubric-v1`, or `cm-2-rubric-v2` |
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
- Prediction / Falsifier / Revisit that changes when source evidence changes the frame

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

### Task CM-2 - Dopamine, Flow, and AI-Augmented Creation

**Target:** `strategy-page`

**Secondary target:** `strategy-chapter` or short `strategy-book` synthesis

**Benchmark intent:** CM-2 is a writing benchmark, not a session-agency benchmark. It tests whether the model can produce public-facing strategic prose about dopamine, flow, judgment, and AI-assisted creation while preserving source limits, tension, historical-pattern discipline, and a concrete counter-practice. For the separate question of whether an AI interaction improved the operator's creative agency, use `docs/skill-work/work-strategy/dopamine-flow-agency-benchmark.md`.

```prompt
You are operating inside a governed strategy writing system. Write a complete strategy-page on the following topic.

Topic: The intense dopamine feedback loops created by AI tools in creative and strategic work, and their implications for judgment, quality, and long-term human flourishing.

Requirements:
- Use historical-pattern reasoning as a mechanism, not decoration.
- Do not use backend jargon such as civ-mem, WORK, Record, raw-input, source_mode, or strategy-codex in the body prose.
- Use one coherent historical-pattern family as the main mechanism. Supporting examples are allowed, but they must not replace the main analogy.
- Explicitly perform the historical-pattern sequence in public-facing prose:
  1. State the historical or civilizational pattern or precedent.
  2. Explain why it appears to fit the current AI-augmented workflow situation.
  3. Explain where and why it may not fit under changed technological conditions.
  4. State what would falsify the analogy.
  5. Show how this analysis changes or sharpens the strategic prediction.
- Name the counter-practice implied by the analysis. It should be concrete enough that a creator, team, or evaluator could try it in a workflow.
- Do not imply that a polished AI-generated artifact proves improved human agency. Keep composition quality separate from claims about the user's judgment, autonomy, or long-term creative flourishing.

Follow the official strategy-page template:
- Signal
- Judgment
- Prediction with explicit Prediction, Falsifier, and Revisit
- Sources if useful

Style rules:
- Prefer bullet points.
- Because this is prompt-only, do not invent verbatim quotes. Use prompt premises and clearly separate empirical-style claims from interpretation.
- Label analogy strength clearly: illustrative, mechanistic, or strong parallel.
- Preserve live tensions; do not resolve the dopamine/flow dilemma with easy optimism or pessimism.
- Keep the public prose forceful but non-hypey: no generic "AI will transform creativity" conclusion unless the preceding analysis earns it.
- Maximum 650 words.

Write the full strategy-page now.
```

## Template Wiring

V1 is wired to these canonical templates:

- `continuity/strategy-codex-template-page.md`
- `continuity/strategy-codex-template-chapter.md`
- `continuity/strategy-codex-template-book.md`

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

## CM-2 Historical-Pattern Rubric

Use `cm-2-rubric-v2` for new CM-2 runs. Older runs may remain on `cm-2-rubric-v1` if their metadata already records that version.

| Dimension | 5 | 3 | 1 |
|-----------|---|---|---|
| Template discipline | Uses Signal / Judgment / Prediction cleanly | Uses most required sections | Ignores or distorts template |
| Historical-pattern mechanism | Historical pattern actively sharpens the strategy | Pattern is present but mostly illustrative | Superficial name-dropping |
| Fit / mismatch balance | Nuanced similarities and changed conditions both shown | Basic comparison | Only fit or only mismatch |
| Falsifier quality | Concrete, testable falsifier | Vague falsifier | No meaningful falsifier |
| Tension preservation | Holds dopamine benefit vs. judgment risk honestly | Mildly acknowledges tension | Forces easy resolution |
| Strategic prediction quality | Actionable prediction and revisit discipline | General advice | Vague or preachy |
| Counter-practice architecture | Names a concrete workflow counter-practice and shows why it follows from the analogy | Names a general remedy | No practical counter-practice |
| Agency boundary discipline | Keeps artifact quality separate from claims about human agency and judgment improvement | Boundary is implied but not explicit | Treats polish or output volume as proof of agency |

### CM-2 shape checks

Before scoring a CM-2 run `Held`, verify:

- the body uses one main historical-pattern family, not a decorative list of unrelated precedents
- the counter-practice is named and operational enough to be tried
- the prediction / falsifier / revisit tests the judgment pattern, not only output volume
- source-mode limits remain visible when the run is `prompt_only`
- the run does not confuse composition quality with the session-level agency benchmark

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
git diff -- self.md self-archive.md recursion-gate.md session-log.md archive/grace-mar-instance/bot/prompt.py
```

Any output in that diff must be explained as pre-existing residue or reverted if introduced by the benchmark work.
