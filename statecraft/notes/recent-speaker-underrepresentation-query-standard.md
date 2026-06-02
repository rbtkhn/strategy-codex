# Recent Speaker Underrepresentation Query Standard

Purpose: standardize the operator query `are there any speakers who seem underrepresented this past week` so the answer is anchored to the local statecraft archive rather than ad hoc memory or whichever month/day rollup happened to be open.

## Core Boundary

This query measures `archive representation`, not actual public silence.

A speaker can look underrepresented for at least three different reasons:

- the speaker was genuinely quieter in the real world
- the speaker was active but their appearances have not yet been ingested
- the speaker was ingested, but a quick read of the archive used the wrong window or the wrong counting surface

The answer must say which layer it is talking about.

## Default Window Rule

If the operator says `this past week` and does not specify dates, use a strict inclusive rolling 7-day window:

- `window_end` = the latest landed archive day relevant to the query
- `window_start` = `window_end - 6 days`

For example:

- if the latest landed day is `2026-06-01`, the default window is `2026-05-26` through `2026-06-01`

Do not silently substitute:

- a month tail
- a hand-picked crisis slice
- `May 27 through June 1` because it feels recent

Always print the actual dates used.

If the operator says `this month` or names a specific month such as `May 2026`, use the full calendar month:

- `month_start` = first calendar day of the named month
- `month_end` = last calendar day of the named month

Do not silently substitute:

- a trailing 30-day window
- only the days already top of mind from a recent batch
- a partial month ending at the latest ingestion run unless the operator explicitly asks for `month to date`

## Counting Rule

Count representation from the landed source files inside the window using the source object metadata, not only the generated month summaries.

Preferred signals:

- `thread:`
- `guest:`
- `speaker:`

Useful but secondary:

- day `README.md` guest rollups
- month `README.md` thread rollups
- thread-index long-run baselines

Normalize obvious naming splits before judging a speaker underrepresented. Common examples include:

- `Chas Freeman` / `Charles Freeman`
- `Doug Macgregor` / `Douglas Macgregor`
- `Seyed M. Marandi` / `Mohammad Marandi` / `Seyed Mohammad Marandi`
- title-bearing guest variants such as `Lt. Col. Anthony Aguilar`

Do not rely only on `thread:` if the speaker regularly appears inside host-owned or mixed-thread files. A speaker may be materially present in the window even when the dominant thread owner is the host rather than the guest.

## Output Shape

Return three buckets.

### 1. Not underrepresented

Use for speakers with multiple landed appearances in the rolling window or clear normal cadence for the current event tempo.

### 2. Present but thin

Use for speakers with one landed appearance in the window where:

- they are historically important in the bench
- and the appearance count is lower than expected
- but the evidence is not thin enough to claim likely omission

### 3. Probably underrepresented or needs backfill

Use only when both are true:

- the rolling-window archive count is light or zero
- and the speaker has a strong standing role in the relevant bench or event

If uncertainty is high, say `probably needs backfill` rather than pretending to know the speaker was quiet.

## Required Caveat Line

Every answer should include a one-line caveat in this form:

`This is a statement about local archive coverage in WINDOW, not a claim that the speaker was inactive in the real world.`

For month-scale answers, add one more line when metadata splits are present:

`Counts are approximate at the guest-label level where the archive still carries naming variants.`

## Worked Correction: Freeman

The Freeman correction is the model case for why this query needs a standard.

Using the proper rolling window `2026-05-26` through `2026-06-01`, Freeman is not a one-hit speaker. He has at least these landed appearances:

- [transcript-napolitano-freeman-israel-humiliates-itself-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-napolitano-freeman-israel-humiliates-itself-2026-05-26.md)
- [transcript-dialogue-works-chas-freeman-hezbollah-strikes-israel-hard-israel-now-prepares-for-war-with-egypt-turkey-2026-05-29.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-29/transcript-dialogue-works-chas-freeman-hezbollah-strikes-israel-hard-israel-now-prepares-for-war-with-egypt-turkey-2026-05-29.md)

And if the operator intended a softer recent-week sense that includes `2026-05-25`, there is also:

- [youtube-glenn-diesen-chas-freeman-crisis-in-israel-iranian-nuclear-weapons-2026-05-25.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-25/youtube-glenn-diesen-chas-freeman-crisis-in-israel-iranian-nuclear-weapons-2026-05-25.md)

So a correct standardized answer must classify Freeman as `not underrepresented` for the strict rolling week ending `2026-06-01`.

## Recommendation

For future operator replies to this query:

1. print the exact window first
2. state that the answer is about archive representation
3. check both `thread` and explicit guest/speaker fields
4. return the three buckets above
5. only then offer a backfill hypothesis
