# Statecraft Participant Index Audit - 2026-06-03

work only; not Record.

## Purpose

Preserve the corpus-level rule for how participant-bearing statecraft source objects should surface in speaker lanes, and record the bounded June 3, 2026 audit that repaired the current archive stack.

This note is not a general source-archive style guide. Its narrower job is to make the participant-index doctrine explicit, record the actual audit metrics, and say which gaps were fixed by parser semantics alone versus direct archive normalization.

## Participant-Index Doctrine

The governing rule is:

- explicit `thread:` / `threads:` metadata remains authoritative when present
- in its absence, recognized substantive participants should still surface in their speaker lanes from participant-bearing metadata

Participant-bearing metadata includes:

- `guest`
- `guest_2`, `guest_3`, and further numbered guest fields
- `guests`
- `participants`
- `speakers`

Host projection is not automatic merely because a file has a `host:` field. It is justified only when the host is functioning as a substantive participant in the archive taxonomy rather than a pure platform shell. In practice, this matters most for recurring analytical host families such as `Glenn Diesen`, `Daniel Davis`, `Napolitano`, and `Dialogue Works / Nima`.

Shortest doctrine:

`host family truth stays intact, but participant indexes should surface every recognized substantive speaker actually present in the object.`

## Parser Findings

The audit exposed four real historical parser seams:

1. numbered guest fields such as `guest_2` and `guest_3` were not being read consistently
2. numbered thread fields such as `thread_2` and `thread_3` were not being counted
3. inline YAML arrays such as `threads: [diesen, mearsheimer]` were being treated as single strings
4. some older `speakers:` / `participants:` lines used single-line comma-separated forms that needed defensive splitting

These were parser/index semantics problems, not just isolated file mistakes. Repairing them materially changed month, year, and global thread truth.

## Audit Metrics

### Baseline

Before the bounded normalization pass, the falsification scan found:

- `60` participant-bearing files audited
- `24` `index-parser-undercount-only`
- `23` `already-correct`
- `9` `safe-metadata-normalization`
- `4` `ambiguous-hold`

Metadata-class counts:

- `16` files with numbered guest fields
- `12` files with numbered thread fields
- `3` files using `speakers:`
- `1` file using `participants:`
- `53` files already carrying some explicit `thread:` or `threads:` expression

### Post-repair

After parser hardening plus bounded frontmatter normalization, the audit settled at:

- `60` participant-bearing files audited
- `46` `already-correct`
- `12` `index-parser-undercount-only`
- `0` remaining `safe-metadata-normalization`
- `2` `ambiguous-hold`

Explicit thread-bearing files rose from `53` to `58`.

The remaining parser-only lane gains from that bounded repair are now concentrated in older files where explicit metadata is already sufficient once the parser understands:

- numbered thread fields
- recognized host projection
- participant-bearing speaker fields

## Bounded Source-Archive Normalization

Only six files required direct archive normalization.

### Recurring Diesen / Mearsheimer / Mercouris panels

These were upgraded to durable explicit multi-thread metadata:

- [2025-02-15 panel](../../source-archive/statecraft/2025-02-15/source-diesen-mearsheimer-mercouris-trump-to-force-ukraine-peace-on-europe-2025-02-15.md)
- [2025-03-08 panel](../../source-archive/statecraft/2025-03-08/source-diesen-mearsheimer-mercouris-the-us-push-for-peace-and-europe-panics-2025-03-08.md)
- [2025-05-02 panel](../../source-archive/statecraft/2025-05-02/source-diesen-mearsheimer-mercouris-ukraine-is-now-trumps-war-2025-05-02.md)
- [2025-05-29 panel](../../source-archive/statecraft/2025-05-29/source-diesen-mearsheimer-mercouris-russia-won-the-war-2025-05-29.md)
- [2025-06-20 panel](../../source-archive/statecraft/2025-06-20/source-diesen-mearsheimer-mercouris-israel-has-walked-off-a-cliff-2025-06-20.md)

Each now carries:

- `threads: [diesen, mearsheimer, mercouris]`

### Duran / Mercouris plus recognized third guest

One live item was upgraded because the extra guest already resolves cleanly to a canonical speaker lane:

- [2025-06-17 Mercouris / Berletic live](../../source-archive/statecraft/2025-06-17/source-duran-mercouris-berletic-trump-on-the-brink-of-iran-war-live-2025-06-17.md)

It now carries:

- `threads: [mercouris, berletic]`

## Parser-Semantics-Only Repairs

The remaining `12` repaired cases did not need direct archive edits.

They now resolve correctly through parser hardening alone, especially where older files already carried enough truth in one of these forms:

- `thread_2` / `thread_3`
- recognized host plus recognized guest fields
- explicit `threads:` arrays that were previously misread because inline YAML lists were parsed as raw strings

The main recurring parser-only families are:

- older `Dialogue Works` multi-participant objects
- selected `Napolitano / Wilkerson` and `Dialogue Works / Nima` cross-lane files

These are now truthful in day, month, year, and global thread surfaces without additional file churn.

## Follow-up Inventory Closure

Later on `2026-06-03`, the speaker inventory gap itself was tightened so the main unresolved participant names from this note no longer remain open:

- `John Kiriakou` now resolves to canonical lane `kiriakou`
- `Stanislav Krapivnik` now resolves to canonical lane `krapivnik`
- `Alex Christoforou` / `Alex Christoforu` / `christoforou` now resolve to canonical lane `christoforou`

That follow-up did two things:

- added canonical speaker folders for `kiriakou`, `krapivnik`, and `christoforou`
- hardened slug alias routing so common spelling variants project into the same lane

So the post-repair metrics above should be read as the truthful end-state of the bounded audit tranche itself, not as the permanent final state of the repository after later same-day inventory repair.

## Surface Impact

The repair was propagated through:

- day `Threads:` summaries
- month thread rollups
- year thread rollups
- [global thread index](../../source-archive/statecraft/thread-index.md)

The strongest parser-driven lane gains after normalization now concentrate in:

- `wilkerson`
- `parsi`
- `marandi`
- `nima`
- `johnson`

The months most affected by lane-gain repair were:

- `2025-04`
- `2025-07`
- `2025-05`
- `2025-06`
- `2025-08`

## Archive-Edit Rubric Preserved

This pass followed the intended bounded rule:

- if parser hardening plus canonical speaker resolution fixed the truth durably, prefer `index truth only`
- if a recurring high-value panel was still underexpressed in its own frontmatter, add durable explicit `threads:`
- if participant identity remained unsettled, leave the file unchanged and log the hold

So the result is:

`bounded normalization, not blanket archive rewrite`

## Future Intake Rule

New participant-bearing captures should prefer explicit durable multi-thread metadata when:

- more than one recognized speaker lane should be strengthened
- the object is a recurring panel family
- the archive would otherwise depend on parser inference alone

Preferred pattern:

- keep `host`, `guest`, `guest_2`, `guest_3` when those fields help name the object truthfully
- add explicit `threads:` for every recognized substantive participant lane
- do not rely on `thread_2` / `thread_3` for new work

## Use Rule

Use this note when:

- someone asks why participant-bearing files should appear in multiple speaker indexes
- someone wants the exact corpus-level findings from the June 3, 2026 participant audit
- someone is deciding whether a new panel object needs explicit `threads:` or can safely rely on parser inference

Do not use this note as a replacement for family-specific month notes or source-intake family doctrine. Its job is corpus-wide participant-index truth.
