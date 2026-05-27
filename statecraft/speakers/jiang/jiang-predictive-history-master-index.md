WORK only; not Record.

# Jiang / Predictive History Master Index

This is the canonical Jiang-shelf master index for Predictive History retrieval inside `strategy-codex`.

Use this file when the question is not merely "where is one lecture?" but "what exists, in which layer, and in what count?"

## Decisive count split

There are three different totals in play:

| Layer | What it counts | Current total | Canonical local path |
| --- | --- | --- | --- |
| Public mirror corpus | Materialized public Predictive History units in the official `ph-civ` mirror | `150` | [ph-civ/data/cards.jsonl](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/data/cards.jsonl) |
| Public source-video table | Public mirror entries with explicit YouTube source rows in one table | `63` | [ph-civ/docs/source-video-index.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/docs/source-video-index.md) |
| Local raw archive captures | Jiang / Predictive History captures preserved in `source-archive/statecraft` outside the public mirror | `12` | [source-archive/statecraft/jiang-predictive-history-index.md](/C:/dev/strategy-codex/source-archive/statecraft/jiang-predictive-history-index.md) |

So if the question is "why are there only 12?", the answer is: `12` is only the raw local capture bench, not the full public corpus.

## Canonical rule

- Use the **public mirror corpus** count when you mean the broad public `ph-civ` artifact.
- Use the **source-video table** when you need YouTube URLs in one place.
- Use the **raw archive** count when you mean local source-bearing captures preserved outside the mirror.

## Public mirror corpus

This is the broadest current public Predictive History object under the Jiang shelf.

Series counts from the official mirror:

| Series | Current public count | Primary local route | Notes |
| --- | --- | --- | --- |
| Civilization | `60` | [ph-civ/book/volume-ii](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/book/volume-ii) | Main Volume I civilization spine. |
| Geo-Strategy | `20` | [ph-civ/book/volume-i](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/book/volume-i) | Legacy provenance shelf feeding Apocalypse. |
| Game Theory | `27` | [ph-civ/book/volume-iii](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/book/volume-iii) | Publicly materialized through `gt-27`. |
| Secret History | `28` | [ph-civ/book/volume-vi](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/book/volume-vi) | Full `sh-01` to `sh-28` public spine. |
| Great Books | `10` | [ph-civ/book/volume-v](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/book/volume-v) | Publicly materialized through `gb-10`. |
| Essays | `5` | [ph-civ/ph-apo](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/ph-apo) | Apocalypse-facing essay lane. |

Primary mirror front doors:

- [ph-civ/README.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/README.md)
- [ph-civ/ph-civ/README.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/ph-civ/README.md)
- [ph-civ/ph-apo/README.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/ph-apo/README.md)
- [ph-civ/ph-mus/README.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/ph-mus/README.md)

## Public source-video subset

This is narrower than the full public corpus. It is the explicit source-video table, not the full manuscript/corpus count.

Current source-video row counts:

| Lane | Current source-video rows | Local route | Coverage note |
| --- | --- | --- | --- |
| Geo-Strategy | `8` | [ph-civ/docs/source-video-index.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/docs/source-video-index.md) | Currently `geo-13` through `geo-20`. |
| Game Theory | `27` | [ph-civ/docs/source-video-index.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/docs/source-video-index.md) | Currently `gt-01` through `gt-27`. |
| Secret History | `28` | [ph-civ/docs/source-video-index.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/docs/source-video-index.md) | Currently `sh-01` through `sh-28`. |
| Civilization | `0` | [ph-civ/docs/source-video-index.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/docs/source-video-index.md) | No dedicated public `civ-*` source-video rows in this table yet. |
| Great Books | `0` | [ph-civ/docs/source-video-index.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/docs/source-video-index.md) | No dedicated public `gb-*` source-video rows in this table yet. |
| Interviews | `0` | [ph-civ/docs/source-video-index.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/docs/source-video-index.md) | Interviews are not currently surfaced here as a public lane. |

Use this file when you need:

- a YouTube URL fast
- a transcript path paired to the URL
- the currently public source-video subset, not the whole corpus

## Local raw archive bench

This is the Jiang-facing source-bearing residue outside the public mirror.

Current raw capture counts:

| Lane | Current local raw captures | Canonical route | Notes |
| --- | --- | --- | --- |
| Interviews | `4` | [source-archive/statecraft/jiang-predictive-history-index.md](/C:/dev/strategy-codex/source-archive/statecraft/jiang-predictive-history-index.md) | Includes recent Diesen/Jiang interview captures. |
| Game Theory | `6` | [source-archive/statecraft/jiang-predictive-history-index.md](/C:/dev/strategy-codex/source-archive/statecraft/jiang-predictive-history-index.md) | Includes `gt-23` through `gt-28` raw captures. |
| Great Books | `1` | [source-archive/statecraft/jiang-predictive-history-index.md](/C:/dev/strategy-codex/source-archive/statecraft/jiang-predictive-history-index.md) | Includes `gb-11`, which is ahead of the current public mirror. |
| Essays | `1` | [source-archive/statecraft/jiang-predictive-history-index.md](/C:/dev/strategy-codex/source-archive/statecraft/jiang-predictive-history-index.md) | Local Substack capture. |

Important current gaps between layers:

- `gt-28` exists in the raw archive but not yet in the current public source-video table.
- `gb-11` exists in the raw archive but the current public mirror materializes Great Books through `gb-10`.
- the raw archive currently preserves four Jiang interviews that are not surfaced as a public interview lane in the mirror.

## Retrieval order

If the user asks:

- "How many Predictive History lectures are there?" -> start with the **public mirror corpus** count here.
- "Where is the YouTube link for lecture X?" -> open [ph-civ/docs/source-video-index.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/ph-civ/docs/source-video-index.md).
- "Do we have a raw local capture of this Jiang / PH item?" -> open [source-archive/statecraft/jiang-predictive-history-index.md](/C:/dev/strategy-codex/source-archive/statecraft/jiang-predictive-history-index.md).
- "What is the canonical Jiang shelf front door?" -> stay in [README.md](/C:/dev/strategy-codex/statecraft/speakers/jiang/README.md) and this file.

## Shelf law

This file is the Jiang-shelf SSOT for count disambiguation across:

- the official public mirror
- the mirror's explicit source-video subset
- the local raw source archive bench

Do not answer large-count Predictive History questions from the raw archive count alone.
