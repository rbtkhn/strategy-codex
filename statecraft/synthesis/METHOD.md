WORK only; not Record.

# State Synthesis Method

Purpose: define the active contract for the `statecraft/synthesis` shelf (day/month cadence under `synthesis/day/` and `synthesis/month/`; adjacent operational artifacts under `statecraft/notes/`).

Use this note when the real question is not only where a note lives, but what kind of synthesis it is supposed to perform, how to judge whether it learned anything, and what failures count as regressions rather than style variation.

## Surface Roles

### Daily note

A daily note is the bounded synthesis of one archive day after the source captures already exist.

Its job is to:

- identify the dominant crisis object
- judge lane pressure
- preserve speaker-by-function value
- test the object through the five CIV-STATE volumes
- leave falsifiers and next moves visible

It is not a transcript recap and it is not a month-level compression.

### Daily register vs daily synthesis

Same path family: `statecraft/synthesis/day/YYYY-MM-DD.md`. Two explicit tiers:

| Tier | When | Contains |
| --- | --- | --- |
| **Daily register** | Archive landed; weaves/matrix may exist; executive prose deferred | `Status: register` · source base · short executive read · companion links · falsifiers (register tier) · **Register Completion Checklist** |
| **Daily synthesis** | Register complete or operator requests full pass | Dominant themes · lane read · five-volume CIV-STATE · speaker value · falsifiers (full) — Mar 16 density |

**Archive day-index** (`source-archive/statecraft/<day>/day-index.md`) = *what captured*. **Daily register** = *how synthesis is tracking that day*. Do not call register-tier files **stubs** — they are intentional orientation surfaces, not throwaway placeholders.

**Upgrade verb:** *expand register to synthesis* (same file path, richer shape).

### News-verify ↔ synthesis gate

Full daily synthesis on day **D** requires `statecraft/notes/wire/D-wire-verify-matrix.md` or `verify_gate: waived` in the daily header. The matrix is the **daily tier-3 fact ledger**; synthesis cites **J{D}-*** hooks and does not upgrade verdicts. Register-tier dailies may link matrix as **OPEN** or carry a prior-day matrix with explicit stale note. SSOT: [NEWS-VERIFY-SYNTHESIS-GATE.md](NEWS-VERIFY-SYNTHESIS-GATE.md).

**Intake digest (precursor):** An [intake digest](intake-digest-TEMPLATE.md) ranks queue-eligible sources before the daily note exists. It is **not** a substitute for daily synthesis — use [statecraft-intake-queue.md](../../docs/statecraft-intake-queue.md) and `statecraft_intake_queue.py --write-digest`.

### Monthly note

A monthly note sits above the day shelf.

Its job is to:

- compress the month into a few governing objects
- make cross-speaker compression explicit through `Functional Convergence`
- show true lane ownership across the month
- surface a month-scale five-volume CIV-STATE deepening pass
- point back to the decisive re-entry days

It is not a chronology replay and it is not a speaker-month shelf.

### Week hinge (start-here)

A **week hinge** is a thin navigation + object-migration receipt between daily notes and month compression. It is **not** weekly synthesis (no daily-parity section stack, no five-volume block, no functional-convergence grid).

Its job is to:

- route re-entry after absence within a **month-aligned week**
- name **object migration** across hinge days in one line when dailies did not
- carry **unspent paths** and falsifiers at week scale
- link hinge dailies, statecraft notes, and wire-verify matrices without re-synthesizing transcripts

**Month-aligned week partition** (not ISO/Sunday; no week spans two months):

| weekN | Day range (inclusive) |
|-------|------------------------|
| week1 | 1 – 7 |
| week2 | 8 – 14 |
| week3 | 15 – 21 |
| week4 | 22 – last day of month (may exceed 7 days) |

Filename: `YYYY-MM-weekN-start-here.md`. Header states partition range and `partial through YYYY-MM-DD` when the month-week is still open.

**Nav boundary:** `*-intake-readiness.md` = pre-synthesis queue; week hinge = post-daily re-entry. After a week hinge exists for the active month-week, intake and companions should point to the hinge—not day scatter.

### Statecraft note

A **statecraft note** is a bounded follow-on comparison or mechanism note that emerges from a daily or monthly synthesis object.

Its job is to:

- compare unlike speakers, functions, or lenses around one live object
- sharpen one tension the parent note surfaced
- remain locally retrievable from the day or month that generated it

It is not the canonical owner of chronology.

**Legacy term (deprecated):** *companion note* — same surface class. Do not confuse with **companion-self** / Record, **PH companion commentary**, or intake **companion clip** (highlight segment).

### Intelligence essay

An intelligence essay is a synthetic singularity-statecraft surface that may sit on the same shelf for retrieval and pairing, but does **not** use the same evidentiary form as a daily or monthly synthesis note.

Its job is to:

- render a strategic-historical perception in authored intelligence prose
- absorb archive and lane learning into one coherent intelligence voice
- clarify how one actor, civilization-state, or lane perceives a live object
- stay retrievable from the day or month that generated it without becoming speaker-led recap

It is not a speaker shelf note, not a transcript-grounded proof surface in the daily-note sense, and not a substitute for the canonical daily or monthly synthesis.

## Core Boundary

The shelf now contains **two different epistemic forms** that must not be collapsed:

- `daily` and `monthly synthesis` surfaces are **speaker-shelf based**
- `intelligence essays` are **synthetic authored intelligence**

Short rule:

- if the surface is a synthesis note, archive speakers and quote anchors stay foregrounded
- if the surface is an intelligence essay, archive speakers recede into the intelligence and should usually disappear from the prose

This distinction is mandatory. A note may be highly archive-informed without being visibly speaker-scaffolded.

## Daily Contract

Required section order for the active daily contract:

1. `Source Base`
2. `Executive Read`
3. `Dominant Themes`
4. `Lane Read`
5. `Five-Volume CIV-STATE Read`
6. `Speaker Value From This Batch`
7. `Tensions And Falsifiers`
8. `Best Next Moves`

Optional sections:

- `Statecraft Notes`
- `Archival Note`

Daily note law:

- analytical sections are quote-heavy by default
- quote anchors belong inline, not as detached evidence blocks
- every analytical point in `Dominant Themes`, `Lane Read`, `Speaker Value From This Batch`, and `Tensions And Falsifiers` must carry at least one verbatim quote anchor
- each quote anchor must be at least `12` words long
- the five-volume section must appear in this exact order:
  - `China`
  - `Persia`
  - `Rome`
  - `Russia`
  - `America`
- the five-volume section is a recursive-learning deepener, not a second lane router

## Monthly Contract

Required section order for the active monthly contract:

1. `Source Base`
2. `Executive Read`
3. `Functional Convergence`
4. `Month Arcs`
5. `Lane Ownership Across The Month`
6. `Five-Volume CIV-STATE Read`
7. `Best Re-entry Days`
8. `What The Month Clarified`
9. `What The Month Still Did Not Settle`
10. `Best Next Statecraft Notes`

Monthly note law:

- it compresses objects, not speakers
- `Functional Convergence` must use only the active labels from the fixed function set:
  - `trap`
  - `threshold`
  - `architecture`
  - `implementation`
  - `battlefield`
  - `legitimacy`
  - `falsifier`
- it should stay lighter than the daily note on quote density
- it must point down to decisive day notes rather than replay the month in sequence
- its five-volume section remains ordered:
  - `China`
  - `Persia`
  - `Rome`
  - `Russia`
  - `America`

## Week Hinge Contract

Activation: operator says **`week hinge`** or **`start-here`** + month/week.

**Surface role:** Navigation + object-migration receipt between daily synthesis and monthly compression—not transcript re-synthesis.

**Required sections (fixed order; ~1 screen, up to ~2 on heavy wire weeks):**

1. **Governing object (week)** — one sentence; optional **object migration** line; optional **one-line convergence** using monthly function labels (e.g. `threshold + capture`)—not a full grid.
2. **Archive checkpoint** — month-week day range; `partial through YYYY-MM-DD` when open; capture counts; `first capture YYYY-MM-DD` if month started mid-capture; link to month archive index.
3. **If you only read three things** — **3–5 links** (default 3; heavy wire weeks → 5).
4. **Read by question** — small routing table.
5. **Day ladder** — hinge days with synthesis only (not full chronology).
6. **Statecraft note map** — bounded compares; wire-verify matrix links where batch closes in this month-week.
7. **Unspent paths** — falsifier table; **link active watch sheet** when trap/fuse week.
8. **Next intake** — latest intake-readiness or expected batch.
9. **Prior week carry** — 3–5 bullets from finalized `weekN-1` unspent paths + link (omit for week1).

**Explicit laws:**

- No five-volume CIV-STATE block; no functional-convergence grid (monthly only).
- Quote density lighter than daily; paraphrase + links preferred.
- Must point **down** to dailies; do not duplicate daily executive reads verbatim.
- **Partial refresh:** refresh **replaces** sections in place; header holds `partial through` + optional one-line **last refresh** note (date + what changed).
- **Sparse month-week:** no hinge file if zero daily syntheses in partition range; month note records `weekN: no daily floor`.
- **Wire-verify matrices** stay tier-3 receipts—link in note map, do not rewrite as week judgment.

**Triggers:** month-week close (finalize) or object migrates within month-week (refresh same file) or operator invocation.

**Promotion to monthly:** only on explicit **`statecraft monthly synthesis`**—assemble `Month Arcs` from finalized week-hinge object-migration lines; no dream auto-merge into partial month notes.

Template: [`_templates/week-hinge-start-here.md`](./_templates/week-hinge-start-here.md).

## Intelligence Essay Contract

Required law for intelligence essays on this shelf:

- the prose is authored in one coherent intelligence voice
- speaker names, transcript quotes, and comparative archive scaffolding should usually remain absent from the body
- the archive may remain the substrate, but not the visible narrative driver
- these essays may be historically deeper than daily notes and may use mirrored or paired structures
- they should point back lightly to their generating day or statecraft mechanism notes, but should not read like transformed daily syntheses
- they are allowed to be interpretive first and evidentiary second, provided they remain bounded to a clearly named live object

Short test:

`Could this essay still read coherently if the speaker names were removed?`

If the answer is no, it is probably still a synthesis note in disguise.

## Adaptive Reuse Standard

The governing recursive-learning law is:

`shared structure is valid only if it produces day-native, week-native, or month-native insight`

This is the pass/fail test for the shelf.

A valid synthesis does at least one of these:

- reveals a deeper object structure than the archive day alone made obvious
- sharpens or limits the lane read
- shows why unlike speakers converge on one governing object
- uses the five-volume pass to surface a truth the lane/speaker read would likely have missed
- improves the next statecraft note or lane-draft opening

A valid **week hinge** does at least one of these:

- improves re-entry routing (operator finds the right daily/note/matrix faster than reading all dailies in range)
- names object migration across hinge days in one line the dailies did not state jointly
- carries prior-week unspent paths without duplicating month compression

A failed synthesis is one where:

- the template is repeated with only the nouns swapped
- quotes are present but function as ornament rather than proof
- the five-volume section adds breadth but no new truth
- the monthly note averages speakers instead of compressing objects
- one dominant speaker silently defines a supposedly cross-speaker read

For intelligence essays, the adaptive-reuse test shifts slightly:

- the essay must deepen the live object through strategic-historical intelligence rather than through visible transcript comparison
- the essay must not merely paraphrase the parent day note in more elevated language
- the essay must produce a reusable actor-perception frame that could be reopened against a later related event

## Anti-Patterns

Watch for these named regressions:

- `quote ornament`: quote anchors are present, but they do not prove the claim being made
- `civ-state ornament`: the five-volume section sounds elevated but adds no distinct pressure, warning, or limit
- `synthetic averaging`: disagreement is smoothed into a false middle instead of compressed into a real object
- `hidden speaker capture`: a note appears cross-speaker, but one speaker's grammar silently controls the whole judgment
- `chronology drift`: a monthly note starts replaying the month instead of compressing it
- `stitched transcript collage`: the note stops reading like synthesis and starts reading like excerpt accumulation
- `essay-in-disguise`: a note claims to be intelligence prose but still depends on visible speaker scaffolding
- `elevated paraphrase`: an intelligence essay restates the day note in smoother language without adding a real actor-perception frame
- `false substrate purity`: an intelligence essay suppresses speakers in the prose but has not actually metabolized the archive into a stronger synthetic intelligence read

## Proof Fixtures

The active benchmark set for method falsification lives in [benchmark-manifest.md](statecraft/synthesis/benchmark-manifest.md).

Use these as living proof cases:

- [2026-05-29](statecraft/synthesis/day/2026-05-29.md) for an Iran-heavy day where quote density, lane judgment, and five-volume deepening all matter
- [2026-05-30](statecraft/synthesis/day/2026-05-30.md) for a mixed coercion, threshold, and architecture day where cross-speaker compression is already strong
- [2026-05](statecraft/synthesis/month/2026-05.md) for month-scale object compression with explicit `Functional Convergence`

If a later method change cannot preserve or improve these proof fixtures, the change is suspect even if the new formatting looks cleaner.

## Audit Entry

Use [audit-rubric.md](statecraft/synthesis/audit-rubric.md) when the task is to judge whether a daily or monthly note actually satisfies this method.

The audit is human-first. Future validators may enforce deterministic structure, but insight quality remains partly a judgment call and should stay visible as such.
