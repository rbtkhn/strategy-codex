WORK only; not Record.

# Jiang / Predictive History Master Index

This is the canonical Jiang-shelf master index for Predictive History retrieval inside `strategy-codex`.

Use this file when the question is not merely "where is one lecture?" but "what exists, in which layer, and in what count?"

## The retrieval hierarchy

The three totals are not competing answers. They describe three nested layers of the same Jiang / Predictive History surface:

- `150` = the broad public mirror corpus
- `63` = the subset of that mirror currently surfaced in one explicit YouTube source-video table
- `13` = the local raw-capture bench preserved outside the mirror

Read them from largest to smallest:

1. **Public mirror corpus**: "How much public Predictive History is materially present here?"
2. **Public source-video table**: "How much of that public corpus has been surfaced in one fast URL table?"
3. **Local raw archive bench**: "What additional Jiang / Predictive History source captures are preserved locally outside the mirror?"

So if the question is "why are there only 13?", the answer is: `13` is not the corpus total. It is only the raw local capture bench.

## Decisive count split

There are three different totals in play:

| Layer | What it counts | Current total | Canonical local path |
| --- | --- | --- | --- |
| Public mirror corpus | Materialized public Predictive History units in the official `ph-civ` mirror | `150` | [ph-civ/data/cards.jsonl](ph-civ/data/cards.jsonl) |
| Public source-video table | Public mirror entries with explicit YouTube source rows in one table | `63` | [ph-civ/docs/source-video-index.md](../../../public/predictive-history/docs/predictive-history-index.md) |
| Local raw archive captures | Jiang / Predictive History captures preserved in `source-archive/statecraft` outside the public mirror | `13` | [source-archive/statecraft/jiang-predictive-history-index.md](../../../source-archive/statecraft/jiang-predictive-history-index.md) |

## Canonical rule

- Answer from the **public mirror corpus** first unless the user explicitly asks for a narrower layer.
- Drop to the **source-video table** when the task is specifically about YouTube URLs or URL-paired transcript paths.
- Drop to the **raw archive bench** only when the task is specifically about local source-bearing captures preserved outside the mirror.

## Public mirror corpus

This is the broadest current public Predictive History object under the Jiang shelf.

Series counts from the official mirror:

| Series | Current public count | Primary local route | Notes |
| --- | --- | --- | --- |
| Civilization | `60` | [ph-civ/book/volume-i-civilization/interwoven-reader/README.md](../../../README.md) | Canonical interwoven spine (`civ-01`–`civ-60`); packet shelf at [volume-ii](ph-civ/book/volume-ii); ten Part doorways at [parts/](../../../README.md). |
| Geo-Strategy | `20` | [ph-civ/book/volume-i](ph-civ/book/volume-i) | Legacy provenance shelf feeding Apocalypse. |
| Game Theory | `27` | [ph-civ/book/volume-iii](ph-civ/book/volume-iii) | Publicly materialized through `gt-27`. |
| Secret History | `28` | [ph-civ/book/volume-vi](ph-civ/book/volume-vi) | Full `sh-01` to `sh-28` public spine. |
| Great Books | `10` | [ph-civ/book/volume-v](ph-civ/book/volume-v) | Publicly materialized through `gb-10`. |
| Essays | `5` | [ph-civ/ph-apo](ph-civ/ph-apo) | Apocalypse-facing essay lane. |

### Volume I reading navigation (Parts overlay)

Ten **Part doorways** on the civilization spine — navigation only; [interwoven-reader](../../../README.md) order stays authoritative. Shelf routing detail: [jiang-routing.md — Volume I Parts](jiang-routing.md#volume-i-parts-reading-navigation).

| Surface | Path |
| --- | --- |
| Parts index | [ph-civ/book/volume-i-civilization/parts/README.md](../../../README.md) |
| Registry | [ph-civ/data/parts/volume-i-parts.json](ph-civ/data/parts/volume-i-parts.json) |
| Part boundary tour | [ph-civ/data/routes/part-boundary-tour.json](ph-civ/data/routes/part-boundary-tour.json) |

Primary mirror front doors:

- [ph-civ/README.md](../../../README.md)
- [ph-civ/ph-civ/README.md](../../../README.md)
- [ph-civ/ph-apo/README.md](../../../README.md)
- [ph-civ/ph-mus/README.md](../../../README.md)

## Public source-video subset

This is the middle layer in the hierarchy: narrower than the full public corpus, but broader than the local raw bench. It is the explicit source-video table, not the full manuscript/corpus count.

Current source-video row counts:

| Lane | Current source-video rows | Local route | Coverage note |
| --- | --- | --- | --- |
| Geo-Strategy | `8` | [ph-civ/docs/source-video-index.md](../../../public/predictive-history/docs/predictive-history-index.md) | Currently `geo-13` through `geo-20`. |
| Game Theory | `27` | [ph-civ/docs/source-video-index.md](../../../public/predictive-history/docs/predictive-history-index.md) | Currently `gt-01` through `gt-27`. |
| Secret History | `28` | [ph-civ/docs/source-video-index.md](../../../public/predictive-history/docs/predictive-history-index.md) | Currently `sh-01` through `sh-28`. |
| Civilization | `0` | [ph-civ/docs/source-video-index.md](../../../public/predictive-history/docs/predictive-history-index.md) | No dedicated public `civ-*` source-video rows in this table yet. |
| Great Books | `0` | [ph-civ/docs/source-video-index.md](../../../public/predictive-history/docs/predictive-history-index.md) | No dedicated public `gb-*` source-video rows in this table yet. |
| Interviews | `0` | [ph-civ/docs/source-video-index.md](../../../public/predictive-history/docs/predictive-history-index.md) | Interviews are not currently surfaced here as a public lane. |

Use this file when you need:

- a YouTube URL fast
- a transcript path paired to the URL
- the currently public source-video subset, not the whole corpus

## Local raw archive bench

This is the narrowest layer in the hierarchy: Jiang-facing source-bearing residue outside the public mirror.

Current raw capture counts:

| Lane | Current local raw captures | Canonical route | Notes |
| --- | --- | --- | --- |
| Interviews | `4` | [source-archive/statecraft/jiang-predictive-history-index.md](../../../source-archive/statecraft/jiang-predictive-history-index.md) | Includes recent Diesen/Jiang interview captures. |
| Game Theory | `6` | [source-archive/statecraft/jiang-predictive-history-index.md](../../../source-archive/statecraft/jiang-predictive-history-index.md) | Includes `gt-23` through `gt-28` raw captures. |
| Great Books | `2` | [source-archive/statecraft/jiang-predictive-history-index.md](../../../source-archive/statecraft/jiang-predictive-history-index.md) | Includes `gb-11` and `gb-12`, both ahead of the current public mirror. |
| Essays | `1` | [source-archive/statecraft/jiang-predictive-history-index.md](../../../source-archive/statecraft/jiang-predictive-history-index.md) | Local Substack capture. |

Important current gaps between layers:

- `gt-28` exists in the raw archive but not yet in the current public source-video table.
- `gb-11` and `gb-12` exist in the raw archive but the current public mirror materializes Great Books through `gb-10`.
- those Dante continuations should be promoted as Volume I / Civilization literary-spine material when public chapter units are created.
- the raw archive currently preserves four Jiang interviews that are not surfaced as a public interview lane in the mirror.

## Retrieval order

If the user asks:

- "How many Predictive History lectures are there?" -> start with the **public mirror corpus** count here, not the raw archive.
- "Where is the YouTube link for lecture X?" -> open [ph-civ/docs/source-video-index.md](../../../public/predictive-history/docs/predictive-history-index.md).
- "Do we have a raw local capture of this Jiang / PH item?" -> open [source-archive/statecraft/jiang-predictive-history-index.md](../../../source-archive/statecraft/jiang-predictive-history-index.md).
- "What is the canonical Jiang shelf front door?" -> stay in [README.md](README.md) and this file.
- "How do I read Volume I by Part?" -> [interwoven spine](../../../README.md) for order; [Parts shelf](../../../README.md) for doorways; [jiang-routing.md](jiang-routing.md#volume-i-parts-reading-navigation) for split seams and validate commands.

## Falsify check

Re-verify the Jiang master-index totals with:

```powershell
& 'C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\dev\strategy-codex\scripts\check_jiang_predictive_history_index.py'
```

Current expected result:

- `public_total=150`
- `source_video_total=63`
- `raw_total=13`
- `status=ok`

## Shelf law

This file is the Jiang-shelf SSOT for count disambiguation across:

- the official public mirror
- the mirror's explicit source-video subset
- the local raw source archive bench

Do not answer large-count Predictive History questions from the raw archive count alone.
