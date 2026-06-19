# check-streams Sachs / Napolitano spring 2025 recovery receipt

Run date: 2026-05-27

## Scope

Strict recovery pass for `Judging Freedom x Jeffrey Sachs` in `March-May 2025`.

Rule used: only full interview front doors count. Highlight clips, quote fragments, and short excerpt uploads do **not** count as canonical archive candidates.

## Result

No trustworthy full `March-May 2025` `Judging Freedom x Sachs` interview front door was recovered in this pass.

This is an honest negative result, not a backlog of obvious missed full episodes.

## What Was Verified

### Full fronts already known outside requested window

- `2025-01-08` full front already materialized:
  - `/source-archive/statecraft/2025-01-08/transcript-napolitano-sachs-does-trump-want-peace-2025-01-08.md`
- `2025-02-03` Sachs-owned Napolitano page exists and is a real full episode surface:
  - `Prof. Jeffrey Sachs: Iran wants peace / Israel wants more war!`
  - source: `https://www.jeffsachs.org/judge-napolitano/krat3xc328x5cbbr8zle49m62fgjx5`

### Sachs-owned Napolitano index evidence

The Sachs-owned Napolitano listings consulted in this pass did **not** expose any full Sachs/Napolitano entries for `March 2025`, `April 2025`, or `May 2025`.

Sources:

- `https://www.jeffsachs.org/judge-napolitano`
- `https://www.jeffsachs.org/judge-napolitano/category/Judging%2BFreedom`
- `https://www.jeffsachs.org/interviewsandmedia/category/Judging%2BFreedom`

Observed pattern:

- `2025-01-14` `#PEACE Prof. Jeffrey Sachs`
- `2025-02-03` `Prof. Jeffrey Sachs: Iran wants peace / Israel wants more war!`
- then no visible Sachs/Napolitano full-front entries again until 2026 surfaces already known on disk

## What Was Rejected

The local `freedom-flat` caches contain many Sachs-branded YouTube URLs, but they are short clip surfaces with blank upload dates in the cached index and therefore fail the front-door standard for this pass.

Representative rejected examples:

- `tLu3OfsEp-Y` `Can Netanyahu be trusted to keep the ceasefire ?`
- `dxObZWd_WvM` `Trump could make history. Will Netanyahu sabotage Trump?`
- `u4h4mWsGj4Q` `The U.S. is the last holdout for peace .`
- `H6gHFJbjU2I` `Path to peace in plain sight - US is blind!`
- `XufaWZtq0IY` `Why does the CIA search the world for monsters?`

Reason for rejection:

- clip-scale duration
- no trustworthy publication date in local cache
- no corresponding Sachs-owned full-front landing page recovered for `March-May 2025`
- high risk of filing highlight fragments as if they were standalone full interviews

## Sources Checked

Local:

- `.codex-tmp/check-streams-2025-03-08/freedom-flat/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/check-streams-2025-05-09/freedom-flat/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/check-streams-2025-03-08/freedom-flat/index.json`
- `.codex-tmp/check-streams-2025-05-09/freedom-flat/index.json`
- `statecraft/voices/civ-lens-sachs/sachs-raw-input-index.md`

Web:

- Sachs-owned Napolitano index and category pages
- targeted title searches for the strongest candidate clip titles
- secondary mirrors such as BitChute / PreserveTube used only as corroborative warning that these surfaces exist, not as canonical date authority

## Current Conclusion

The live asymmetry remains real:

- `Diesen x Sachs` is materially thick on disk for `January-May 2025`
- `Judging Freedom x Sachs` is still thin on disk in `2025`, and the spring gap cannot be honestly filled from the currently recovered evidence

## Next Recovery Rule

Only reopen this `March-May 2025` Napolitano sweep if one of the following appears:

- a direct YouTube full interview watch URL with clear title/date authority
- a Sachs-owned Napolitano landing page for a `March-May 2025` full episode
- a transcript-bearing full body from the operator tied to a trustworthy front door

Until then, do **not** materialize the spring 2025 Sachs/Napolitano clip surfaces as archive objects.
