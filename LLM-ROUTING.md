<!-- GENERATED FILE. DO NOT EDIT DIRECTLY.
Source: repo-map.yaml + docs/templates/llm-routing-prose.md
Regenerate: python3 scripts/generate_llm_routing.py
-->

# LLM Routing Map

WORK only; not Record.

This repository contains multiple index and source surfaces. Do not rely only on GitHub code search when asked to find a file, source corpus, analyst, speaker, dashboard, or index.

This file is a **routing aid**. It does not change repository authority. Canonical truth remains with the relevant source files and existing doctrine ([AGENTS.md](AGENTS.md), [docs/archive/grace-mar.md](docs/archive/grace-mar.md), [docs/operator-dashboards.md](docs/operator-dashboards.md)).

**Routing hierarchy:** [README.md](README.md) → [docs/start-here.md](docs/start-here.md) → [repo-map.yaml](repo-map.yaml) → domain README. Detail: [docs/routing-reference.md](docs/routing-reference.md).

## Core routing shortcuts

| User asks for… | Search these paths first |
|---|---|
| analyst / speaker / commentator **source index** | [statecraft/voices/INDEX.md](statecraft/voices/INDEX.md), `statecraft/voices/**/**-source-index.md` |
| **archive day-index** / day source inventory for **YYYY-MM-DD** | **`source-archive/statecraft/YYYY-MM-DD/day-index.md` only** — or `python scripts/statecraft_day_source_index.py --day YYYY-MM-DD` — **do not** Glob/Grep month or thread-index for a dated day query |
| transcript / capture / source file | [source-archive/statecraft/](source-archive/statecraft/) |
| archive inventory by thread (counts, coverage) | [source-archive/statecraft/thread-index.md](source-archive/statecraft/thread-index.md) — **generated inventory**, not a route map |
| daily statecraft synthesis | [statecraft/synthesis/day/](statecraft/synthesis/day/) — **after** archive + source-index |
| host-family continuity (Davis, Napolitano, Nima, …) | [statecraft/channels/](statecraft/channels/) |
| **YouTube channel roster** / check-sources / `channel_slug` | [statecraft/channels/channel-index.json](statecraft/channels/channel-index.json) · [channel-index.md](statecraft/channels/channel-index.md) |
| statecraft lane / active operator work | [statecraft/](statecraft/) |
| singularity lane / acceleration work | [singularity/](singularity/) |
| **essay / stand-alone thesis** (cross-channel default) | [essays/README.md](essays/README.md) — primary shelf; channel `*/essays/` = compatibility only |
| **prose class** (note vs essay vs synthesis) | [docs/prose-index.md](docs/prose-index.md) |
| architecture / harness topology / model vs harness map | [docs/harness-architecture-map.md](docs/harness-architecture-map.md) |
| repository root layout / root crowding | [docs/root-directory-map.md](docs/root-directory-map.md) |
| **source-lattice** / corpus tiers / reading order | [docs/source-lattice-beyond-the-repo.md](docs/source-lattice-beyond-the-repo.md) |
| machine-readable route registry | [repo-map.yaml](repo-map.yaml) |
| Grace-Mar fork doctrine (archived) | [docs/archive/grace-mar.md](docs/archive/grace-mar.md) |
| frozen Record surfaces (fork revive only) | `archive/grace-mar-instance/` — not default operator work |

## Route registry (generated from repo-map.yaml)

| id | kind | category | path | search hints |
|---|---|---|---|---|
| ai-consciousness-essay | essay | work | [essays/ai-and-the-expansion-of-human-consciousness.md](essays/ai-and-the-expansion-of-human-consciousness.md) | expansion of human consciousness, ai medium writing print, cognition-changing medium, … |
| america-sovereign-command-allied-capture-essay | essay | work | [essays/america-and-the-problem-of-sovereign-command-under-allied-capture.md](essays/america-and-the-problem-of-sovereign-command-under-allied-capture.md) | section 224 NDAA, allied capture command, sovereign command under allied capture, … |
| archive-synthesis-law-essay | essay | work | [essays/archive-synthesis-law.md](essays/archive-synthesis-law.md) | archive synthesis law, statecraft archive synthesis, vertical law stack, … |
| barnes-source-index | source_index | work | [statecraft/voices/barnes/barnes-source-index.md](statecraft/voices/barnes/barnes-source-index.md) | Barnes index, barnes source index, Robert Barnes corpus, … |
| channel-index-roster | routing_aid | work | `statecraft/channels/channel-index.json` | channel index, channel-index.json, channel-index.md, … |
| crooke-source-index | source_index | work | [statecraft/voices/crooke/crooke-source-index.md](statecraft/voices/crooke/crooke-source-index.md) | Crooke index, crooke source index |
| davis-host-shelf | routing_aid | work | [statecraft/channels/daniel-davis/README.md](statecraft/channels/daniel-davis/README.md) | Davis host, Daniel Davis, Deep Dive host, … |
| dialogue-works-index | source_index | work | [statecraft/channels/dialogue-works/dialogue-works-index.md](statecraft/channels/dialogue-works/dialogue-works-index.md) | Dialogue Works index, dialogue-works-index, source-dialogue-works, … |
| diesen-source-index | source_index | work | [statecraft/voices/diesen/diesen-source-index.md](statecraft/voices/diesen/diesen-source-index.md) | Diesen index, diesen source index |
| essays-shelf | prose_shelf | work | [essays/README.md](essays/README.md) | essays shelf, stand-alone essay, cross-channel essay, … |
| freeman-source-index | source_index | work | [statecraft/voices/freeman/freeman-source-index.md](statecraft/voices/freeman/freeman-source-index.md) | Freeman index, freeman source index |
| grace-mar-self-library | museum_reference | archive | [archive/grace-mar-instance/self-library.md](archive/grace-mar-instance/self-library.md) | grace mar library, museum books index |
| helmer-source-index | source_index | work | [statecraft/voices/helmer/helmer-source-index.md](statecraft/voices/helmer/helmer-source-index.md) | Helmer index, helmer source index |
| high-skill-labor-american-command-essay | essay | work | [essays/high-skill-labor-compression-and-american-command.md](essays/high-skill-labor-compression-and-american-command.md) | high skill labor compression, american command essay, vendor carried command, … |
| hoh-source-index | source_index | work | [statecraft/voices/hoh/hoh-source-index.md](statecraft/voices/hoh/hoh-source-index.md) | Hoh index, hoh source index |
| iran-nuclear-threshold-hardened-essay | essay | work | [essays/how-the-iran-nuclear-threshold-story-hardened.md](essays/how-the-iran-nuclear-threshold-story-hardened.md) | iran nuclear threshold hardened, June 2 Pakistan offer, crude device demonstration test, … |
| jiang-source-index | source_index | work | [statecraft/voices/jiang/jiang-source-index.md](statecraft/voices/jiang/jiang-source-index.md) | Jiang index, jiang source index |
| johnson-source-index | source_index | work | [statecraft/voices/johnson/johnson-source-index.md](statecraft/voices/johnson/johnson-source-index.md) | Johnson index, johnson source index |
| karaganov-source-index | source_index | work | [statecraft/voices/karaganov/karaganov-source-index.md](statecraft/voices/karaganov/karaganov-source-index.md) | Karaganov index, karaganov source index |
| kent-source-index | source_index | work | [statecraft/voices/kent/kent-source-index.md](statecraft/voices/kent/kent-source-index.md) | Kent index, kent source index |
| lascaris-source-index | source_index | work | [statecraft/voices/lascaris/lascaris-source-index.md](statecraft/voices/lascaris/lascaris-source-index.md) | Lascaris index, lascaris source index |
| library-index-retired | generated_dashboard | generated | [runtime/artifacts/library-index.md](runtime/artifacts/library-index.md) | operator books misc homes |
| llm-routing | routing_aid | generated | [LLM-ROUTING.md](LLM-ROUTING.md) | LLM routing, find file in repo, Barnes index |
| macgregor-source-index | source_index | work | [statecraft/voices/macgregor/macgregor-source-index.md](statecraft/voices/macgregor/macgregor-source-index.md) | Macgregor index, macgregor source index |
| marandi-source-index | source_index | work | [statecraft/voices/marandi/marandi-source-index.md](statecraft/voices/marandi/marandi-source-index.md) | Marandi index, marandi source index |
| martyanov-source-index | source_index | work | [statecraft/voices/martyanov/martyanov-source-index.md](statecraft/voices/martyanov/martyanov-source-index.md) | Martyanov index, martyanov source index |
| mcgovern-source-index | source_index | work | [statecraft/voices/mcgovern/mcgovern-source-index.md](statecraft/voices/mcgovern/mcgovern-source-index.md) | McGovern index, mcgovern source index |
| mearsheimer-source-index | source_index | work | [statecraft/voices/mearsheimer/mearsheimer-source-index.md](statecraft/voices/mearsheimer/mearsheimer-source-index.md) | Mearsheimer index, mearsheimer source index |
| memory | work_continuity | work | [memory.md](memory.md) | session continuity, operator memory buffer |
| mercouris-source-index | source_index | work | [statecraft/voices/mercouris/mercouris-source-index.md](statecraft/voices/mercouris/mercouris-source-index.md) | Mercouris index, mercouris source index |
| napolitano-host-shelf | routing_aid | work | [statecraft/channels/judging-freedom/README.md](statecraft/channels/judging-freedom/README.md) | Napolitano host, Judging Freedom, Napolitano profile, … |
| nima-host-shelf | routing_aid | work | [statecraft/channels/dialogue-works/README.md](statecraft/channels/dialogue-works/README.md) | Nima host, Dialogue Works host, Nima profile, … |
| operator-uses-statecraft-machine-essay | essay | work | [essays/how-the-operator-uses-the-statecraft-machine.md](essays/how-the-operator-uses-the-statecraft-machine.md) | how operator uses statecraft, memory to mechanism, lane membrane test, … |
| pape-source-index | source_index | work | [statecraft/voices/pape/pape-source-index.md](statecraft/voices/pape/pape-source-index.md) | Pape index, pape source index |
| parsi-source-index | source_index | work | [statecraft/voices/parsi/parsi-source-index.md](statecraft/voices/parsi/parsi-source-index.md) | Parsi index, parsi source index |
| ph-civ-source-lattice | reading_discipline | work | [public/predictive-history/docs/source-lattice.md](public/predictive-history/docs/source-lattice.md) | PH chapter reading order, civ transcript floor, commentary canvas order |
| postol-source-index | source_index | work | [statecraft/voices/postol/postol-source-index.md](statecraft/voices/postol/postol-source-index.md) | Postol index, postol source index |
| product-identity-essay | essay | work | [essays/from-accumulation-to-governed-interpretive-machine.md](essays/from-accumulation-to-governed-interpretive-machine.md) | governed interpretive machine, what is strategy-codex becoming, accumulation essay |
| prose-index | routing_aid | work | [docs/prose-index.md](docs/prose-index.md) | prose index, note vs essay, where to put prose, … |
| record-vector-index-script | local_index_script | work | `scripts/index_record.py` | vector index, chroma index, record embeddings |
| recursive-learning-three-layers-essay | essay | work | [essays/three-layers-of-recursive-learning-in-statecraft.md](essays/three-layers-of-recursive-learning-in-statecraft.md) | three layers recursive learning, recursive learning journal essay, instruction drift learning |
| ritter-source-index | source_index | work | [statecraft/voices/ritter/ritter-source-index.md](statecraft/voices/ritter/ritter-source-index.md) | Ritter index, ritter source index |
| sachs-source-index | source_index | work | [statecraft/voices/sachs/sachs-source-index.md](statecraft/voices/sachs/sachs-source-index.md) | Sachs index, sachs source index |
| source-lattice-doctrine | reading_discipline | work | [docs/source-lattice-beyond-the-repo.md](docs/source-lattice-beyond-the-repo.md) | source lattice, corpus tiers, reading order, … |
| speaker-cluster-map | routing_aid | work | [statecraft/voices/speaker-cluster-map.md](statecraft/voices/speaker-cluster-map.md) | speaker cluster map, satellite speaker, which speaker after Pape, … |
| statecraft-day-source-index | generated_inventory | generated | [source-archive/statecraft/YYYY-MM-DD/day-index.md](source-archive/statecraft/YYYY-MM-DD/day-index.md) | day index, day-index, june 17 day index, … |
| statecraft-source-capture | source_capture | source | [source-archive/statecraft/YYYY-MM-DD/source-*.md](source-archive/statecraft/YYYY-MM-DD/source-*.md) | source capture, verbatim transcript, statecraft source file, … |
| statecraft-thread-index | generated_inventory | generated | [source-archive/statecraft/thread-index.md](source-archive/statecraft/thread-index.md) | thread index, archive inventory |
| voices-index | directory_index | work | [statecraft/voices/INDEX.md](statecraft/voices/INDEX.md) | voices index, civ-lens legacy, analyst source index |
| weichert-source-index | source_index | work | [statecraft/voices/weichert/weichert-source-index.md](statecraft/voices/weichert/weichert-source-index.md) | Weichert index, weichert source index, Nawfal Weichert |
| wilkerson-source-index | source_index | work | [statecraft/voices/wilkerson/wilkerson-source-index.md](statecraft/voices/wilkerson/wilkerson-source-index.md) | Wilkerson index, wilkerson source index |

## Source index registry (generated)

| speaker | path | repo-map id |
|---|---|---|
| barnes | [statecraft/voices/barnes/barnes-source-index.md](statecraft/voices/barnes/barnes-source-index.md) | barnes-source-index |
| blumenthal | [statecraft/voices/blumenthal/blumenthal-source-index.md](statecraft/voices/blumenthal/blumenthal-source-index.md) | — |
| crooke | [statecraft/voices/crooke/crooke-source-index.md](statecraft/voices/crooke/crooke-source-index.md) | crooke-source-index |
| diesen | [statecraft/voices/diesen/diesen-source-index.md](statecraft/voices/diesen/diesen-source-index.md) | diesen-source-index |
| freeman | [statecraft/voices/freeman/freeman-source-index.md](statecraft/voices/freeman/freeman-source-index.md) | freeman-source-index |
| helmer | [statecraft/voices/helmer/helmer-source-index.md](statecraft/voices/helmer/helmer-source-index.md) | helmer-source-index |
| hoh | [statecraft/voices/hoh/hoh-source-index.md](statecraft/voices/hoh/hoh-source-index.md) | hoh-source-index |
| jermy | [statecraft/voices/jermy/jermy-source-index.md](statecraft/voices/jermy/jermy-source-index.md) | — |
| jiang | [statecraft/voices/jiang/jiang-source-index.md](statecraft/voices/jiang/jiang-source-index.md) | jiang-source-index |
| johnson | [statecraft/voices/johnson/johnson-source-index.md](statecraft/voices/johnson/johnson-source-index.md) | johnson-source-index |
| karaganov | [statecraft/voices/karaganov/karaganov-source-index.md](statecraft/voices/karaganov/karaganov-source-index.md) | karaganov-source-index |
| kent | [statecraft/voices/kent/kent-source-index.md](statecraft/voices/kent/kent-source-index.md) | kent-source-index |
| krapivnik | [statecraft/voices/krapivnik/krapivnik-source-index.md](statecraft/voices/krapivnik/krapivnik-source-index.md) | — |
| lascaris | [statecraft/voices/lascaris/lascaris-source-index.md](statecraft/voices/lascaris/lascaris-source-index.md) | lascaris-source-index |
| macgregor | [statecraft/voices/macgregor/macgregor-source-index.md](statecraft/voices/macgregor/macgregor-source-index.md) | macgregor-source-index |
| marandi | [statecraft/voices/marandi/marandi-source-index.md](statecraft/voices/marandi/marandi-source-index.md) | marandi-source-index |
| martyanov | [statecraft/voices/martyanov/martyanov-source-index.md](statecraft/voices/martyanov/martyanov-source-index.md) | martyanov-source-index |
| mate | [statecraft/voices/mate/mate-source-index.md](statecraft/voices/mate/mate-source-index.md) | — |
| mcgovern | [statecraft/voices/mcgovern/mcgovern-source-index.md](statecraft/voices/mcgovern/mcgovern-source-index.md) | mcgovern-source-index |
| mearsheimer | [statecraft/voices/mearsheimer/mearsheimer-source-index.md](statecraft/voices/mearsheimer/mearsheimer-source-index.md) | mearsheimer-source-index |
| mercouris | [statecraft/voices/mercouris/mercouris-source-index.md](statecraft/voices/mercouris/mercouris-source-index.md) | mercouris-source-index |
| pape | [statecraft/voices/pape/pape-source-index.md](statecraft/voices/pape/pape-source-index.md) | pape-source-index |
| parsi | [statecraft/voices/parsi/parsi-source-index.md](statecraft/voices/parsi/parsi-source-index.md) | parsi-source-index |
| postol | [statecraft/voices/postol/postol-source-index.md](statecraft/voices/postol/postol-source-index.md) | postol-source-index |
| ritter | [statecraft/voices/ritter/ritter-source-index.md](statecraft/voices/ritter/ritter-source-index.md) | ritter-source-index |
| sachs | [statecraft/voices/sachs/sachs-source-index.md](statecraft/voices/sachs/sachs-source-index.md) | sachs-source-index |
| weichert | [statecraft/voices/weichert/weichert-source-index.md](statecraft/voices/weichert/weichert-source-index.md) | weichert-source-index |
| wilkerson | [statecraft/voices/wilkerson/wilkerson-source-index.md](statecraft/voices/wilkerson/wilkerson-source-index.md) | wilkerson-source-index |

## Host shelf registry (generated)

| host | path | repo-map id |
|---|---|---|
| alexander-mercouris | [statecraft/channels/alexander-mercouris/README.md](statecraft/channels/alexander-mercouris/README.md) | — |
| breaking-points | [statecraft/channels/breaking-points/README.md](statecraft/channels/breaking-points/README.md) | — |
| daniel-davis | [statecraft/channels/daniel-davis/README.md](statecraft/channels/daniel-davis/README.md) | davis-host-shelf |
| dialogue-works | [statecraft/channels/dialogue-works/README.md](statecraft/channels/dialogue-works/README.md) | nima-host-shelf |
| glenn-diesen | [statecraft/channels/glenn-diesen/README.md](statecraft/channels/glenn-diesen/README.md) | — |
| india-global-left | [statecraft/channels/india-global-left/README.md](statecraft/channels/india-global-left/README.md) | — |
| judging-freedom | [statecraft/channels/judging-freedom/README.md](statecraft/channels/judging-freedom/README.md) | napolitano-host-shelf |
| mario-nawfal | [statecraft/channels/mario-nawfal/README.md](statecraft/channels/mario-nawfal/README.md) | — |
| moral-resistance | [statecraft/channels/moral-resistance/README.md](statecraft/channels/moral-resistance/README.md) | — |
| neutrality-studies | [statecraft/channels/neutrality-studies/README.md](statecraft/channels/neutrality-studies/README.md) | — |
| predictive-history | [statecraft/channels/predictive-history/README.md](statecraft/channels/predictive-history/README.md) | — |
| reason-resist | [statecraft/channels/reason-resist/README.md](statecraft/channels/reason-resist/README.md) | — |
| redacted-news | [statecraft/channels/redacted-news/README.md](statecraft/channels/redacted-news/README.md) | — |
| the-duran | [statecraft/channels/the-duran/README.md](statecraft/channels/the-duran/README.md) | — |
| tucker-carlson | [statecraft/channels/tucker-carlson/README.md](statecraft/channels/tucker-carlson/README.md) | — |

## Repo routing metrics

- source indexes (disk): 28
- host shelves (disk): 15
- markdown links (INDEX + source-index files): 1094
- repo-map routes: 51 (directory_index=1, essay=8, generated_dashboard=1, generated_inventory=2, local_index_script=1, museum_reference=1, prose_shelf=1, reading_discipline=2, routing_aid=7, source_capture=1, source_index=25, work_continuity=1)
- source_index routes in repo-map: 25
- host_shelf routes in repo-map: 3
- registry: INDEX lists 27/28, repo-map lists 24/28 (85.7% bijection when both match)
- host shelves: repo-map lists 3/15 (20.0%)
- absolute path violations (INDEX + source-index): 0
- broken links (--strict resolution): 0
- required surfaces present: True

## Parallel index disambiguation

Several surfaces use the word **index**. They are not interchangeable.

| Surface | Job | Authority |
|---|---|---|
| `source-archive/statecraft/YYYY-MM-DD/day-index.md` | **Day index** — channel / writer / other partitions for one archive day | Derived / archive (rebuild via `build_statecraft_day_indices.py`) |
| `source-archive/statecraft/YYYY-MM-DD/README.md` | **Day README stub** — pointer to `day-index.md` only | Derived / archive |
| `statecraft/voices/**/**-source-index.md` | Per-analyst **route map** — which captures to open first | WORK only |
| [statecraft/voices/INDEX.md](statecraft/voices/INDEX.md) | Front door listing all analyst source indexes | WORK routing aid |
| [source-archive/statecraft/thread-index.md](source-archive/statecraft/thread-index.md) | Generated capture **inventory** by thread | Derived / archive |
| [archive/grace-mar-instance/self-library.md](archive/grace-mar-instance/self-library.md) | Canonical removed operator-books symlink reference layer | Canonical reference |
| [runtime/artifacts/library-index.md](runtime/artifacts/library-index.md) | Derived removed operator-books symlink **dashboard** | Derived |
| [scripts/index_record.py](scripts/index_record.py) | Local Chroma / Record vector index builder | Derived local |
| [docs/archive/codex-speakers-deprecated.md](docs/archive/codex-speakers-deprecated.md) | Tombstone for terminated `codex/speakers/` | Archive |
| [statecraft/channels/](statecraft/channels/) | Host-family continuity (Davis, Napolitano, Nima / Dialogue Works) | WORK only |
| [statecraft/channels/channel-index.json](statecraft/channels/channel-index.json) | **YouTube channel roster** (main) — check-sources SSOT; human: [channel-index.md](statecraft/channels/channel-index.md) | Derived from archive; rebuild via `refresh_statecraft_archive_indices.py` |
| [statecraft/voices/speaker-cluster-map.md](statecraft/voices/speaker-cluster-map.md) | Anchor-and-satellite routing after Pape/Ritter/Parsi/Crooke | WORK routing aid |
| `statecraft/voices/<speaker>/<speaker>-profile.md` | Per-speaker identity, voice fingerprint, pairing hub | WORK only (migrated SSOT) |
| [codex/profiles/*-profile.md](codex/profiles/) | Profile-only lanes or pre-migration compatibility | Compatibility / profile-only |

**Essays vs channel essay folders vs notes:**

| Surface | Job | Authority |
|---|---|---|
| [essays/README.md](essays/README.md) | **Primary** stand-alone / cross-channel theses | WORK prose shelf |
| `statecraft/notes/` · `singularity/notes/` | Channel-scoped bounded interpretive objects | WORK prose shelf |
| `statecraft/essays/` · `singularity/essays/` | Pre-root **compatibility** essay holdings | Stubs → `essays/` |
| [docs/prose-index.md](docs/prose-index.md) | Note vs essay vs synthesis class chooser | WORK routing aid |

**Do not** answer "no Barnes index" because `library-index.md` or GitHub code search returned zero hits.

## Source index vs source-lattice

| Term | Question | Where |
|---|---|---|
| **source-index** | *Where* is the corpus? Which file opens first? | voices `*-source-index.md` for **analyst** scope; **`source-archive/statecraft/YYYY-MM-DD/day-index.md`** for **one archive day** |
| **source-lattice** | *How* should layers be read so summary does not replace source? | [docs/source-lattice-beyond-the-repo.md](docs/source-lattice-beyond-the-repo.md) |

**Find-then-read contract:**

1. **Find** — this file → voices source-index → `source-archive/`
2. **Read** — source-lattice doctrine (corpus tiers 1–4 + reading layers); PH chapters → `ph-civ/docs/source-lattice.md`
3. **Block** — tier-4 commentary cannot substantiate tier-3 claims without wire receipts

"Barnes **index**" is a location query. "Source-**lattice**" is a reading-discipline query.

## Search command convention

- **Interactive / in-repo search:** prefer `rg` (ripgrep) when available. Cursor agents: use ripgrep-backed workspace search.
- **Committed scripts, CI examples, and portable docs:** prefer `grep`, or `rg` with `grep -R` fallback when `rg` is not installed.
- **Zero hits are not proof of absence:** `grep`, `rg`, and GitHub code search can all miss indexed surfaces. Consult this routing map and the likely path family before answering "not found."

## Required search protocol

For any request of the form "find X in this repo":

0. If the query names **`day-index`**, **source-index**, or **what landed** with a calendar date **`YYYY-MM-DD`**, open **`source-archive/statecraft/YYYY-MM-DD/day-index.md`** only (or `python scripts/statecraft_day_source_index.py --day YYYY-MM-DD`) — **do not** Glob/Grep `thread-index.md`, month rollups, or voices `*-source-index.md` unless the operator named an **analyst/voice** scope.
1. If the user supplied an exact path or URL, fetch that path first.
2. Search exact term, lowercase term, and likely titlecase term.
3. Check this routing map and [repo-map.yaml](repo-map.yaml) before concluding absence.
4. If the query names an analyst, speaker, source corpus, or transcript set, inspect [statecraft/voices/](statecraft/voices/) and [source-archive/statecraft/](source-archive/statecraft/).
5. If `grep`, `rg`, or GitHub code search returns zero results, treat that as a search miss, not proof of absence.
6. Do not answer "not found" until the relevant path family has been checked.
7. After locating a capture, apply find-then-read (source-lattice) before synthesis or judgment-bearing output.
