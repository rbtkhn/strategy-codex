<!-- GENERATED FILE. DO NOT EDIT DIRECTLY.
Source: repo-map.yaml + docs/templates/llm-routing-prose.md
Regenerate: python3 scripts/generate_llm_routing.py
-->

---
audience: operator
authority: routing_aid
record_status: none
---

# LLM Routing Map

WORK only; not Record.

This repository contains multiple index and source surfaces. Do not rely only on GitHub code search when asked to find a file, source corpus, analyst, speaker, dashboard, or index.

This file is a **routing aid**. It does not change repository authority. Canonical truth remains with the relevant source files and existing doctrine ([AGENTS.md](../../AGENTS.md), [docs/archive/grace-mar.md](../../docs/archive/grace-mar.md), [docs/operator-dashboards.md](../operator-dashboards.md)).

**Routing hierarchy:** [README.md](README.md) → [docs/start-here.md](../start-here.md) → [repo-map.yaml](../../repo-map.yaml) → domain README. Detail: [docs/routing-reference.md](../routing-reference.md).

## Core routing shortcuts

| User asks for… | Search these paths first |
|---|---|
| analyst / speaker / commentator **source index** | [statecraft/voices/voice-index.md](../../statecraft/voices/voice-index.md), `statecraft/voices/**/**-source-index.md` |
| **archive day-index** / day source inventory for **YYYY-MM-DD** | **`source-archive/statecraft/YYYY-MM-DD/day-index.md` only** — or `python scripts/statecraft_day_source_index.py --day YYYY-MM-DD` — **do not** Glob/Grep month or thread-index for a dated day query |
| transcript / capture / source file | [source-archive/statecraft/](../../statecraft) |
| archive inventory by thread (counts, coverage) | [source-archive/statecraft/thread-index.md](../../source-archive/statecraft/thread-index.md) — **generated inventory**, not a route map |
| daily statecraft synthesis | [statecraft/synthesis/day/](../../statecraft/synthesis/day) — **after** archive + source-index |
| host-family continuity (Davis, Napolitano, Nima, …) | [statecraft/channels/](../../statecraft/channels) |
| **YouTube channel roster** / check-sources / `channel_slug` | [statecraft/channels/channel-index.json](../../statecraft/channels/channel-index.json) · [channel-index.md](../../statecraft/channels/channel-index.md) |
| statecraft lane / active operator work | [statecraft/](../../statecraft) |
| singularity lane / acceleration work | [singularity/](../../singularity) |
| **essay / stand-alone thesis** (cross-channel default) | [essays/README.md](../../essays/README.md) — primary shelf; channel `*/essays/` = compatibility only |
| **prose class** (note vs essay vs synthesis) | [docs/prose-index.md](../prose-index.md) |
| architecture / harness topology / model vs harness map | [docs/harness-architecture-map.md](../../docs/harness-architecture-map.md) |
| repository root layout / root crowding | [docs/root-directory-map.md](../../docs/root-directory-map.md) |
| **source-lattice** / corpus tiers / reading order | [docs/source-lattice-beyond-the-repo.md](../source-lattice-beyond-the-repo.md) |
| machine-readable route registry | [repo-map.yaml](../../repo-map.yaml) |
| Grace-Mar fork doctrine (archived) | [docs/archive/grace-mar.md](../../docs/archive/grace-mar.md) |
| frozen Record surfaces (fork revive only) | `archive/grace-mar-instance/` — not default operator work |

## Route registry (generated from repo-map.yaml)

| id | kind | category | path | search hints |
|---|---|---|---|---|
| ai-consciousness-essay | essay | work | [essays/ai-and-the-expansion-of-human-consciousness.md](essays/ai-and-the-expansion-of-human-consciousness.md) | expansion of human consciousness, ai medium writing print, cognition-changing medium, … |
| alexander-mercouris-channel-index | source_index | work | [statecraft/channels/alexander-mercouris/alexander-mercouris-channel-index.md](statecraft/channels/alexander-mercouris/alexander-mercouris-channel-index.md) | Alexander Mercouris index, alexander-mercouris-channel-index, alexander-mercouris-index, … |
| alexander-mercouris-host-shelf | routing_aid | work | [statecraft/channels/alexander-mercouris/README.md](statecraft/channels/alexander-mercouris/README.md) | Alexander Mercouris host, alexander-mercouris profile |
| alkorshid-index | source_index | work | [statecraft/voices/alkorshid/alkorshid-index.md](statecraft/voices/alkorshid/alkorshid-index.md) | Alkorshid guest index, Nima Alkorshid cross-host, alkorshid index |
| alkorshid-profile | source_index | work | [statecraft/voices/alkorshid/alkorshid-profile.md](statecraft/voices/alkorshid/alkorshid-profile.md) | Alkorshid profile, Nima Alkorshid profile, alkorshid-profile, … |
| america-sovereign-command-allied-capture-essay | essay | work | [essays/america-and-the-problem-of-sovereign-command-under-allied-capture.md](essays/america-and-the-problem-of-sovereign-command-under-allied-capture.md) | section 224 NDAA, allied capture command, sovereign command under allied capture, … |
| archive-synthesis-law-essay | essay | work | [essays/archive-synthesis-law.md](essays/archive-synthesis-law.md) | archive synthesis law, statecraft archive synthesis, vertical law stack, … |
| barnes-index | source_index | work | [statecraft/voices/barnes/barnes-index.md](statecraft/voices/barnes/barnes-index.md) | Barnes index, barnes source index, Robert Barnes corpus, … |
| barnes-source-index | source_index | work | [statecraft/voices/barnes/barnes-source-index.md](statecraft/voices/barnes/barnes-source-index.md) | Barnes index, barnes source index, Robert Barnes corpus, … |
| blumenthal-index | source_index | work | [statecraft/voices/blumenthal/blumenthal-index.md](statecraft/voices/blumenthal/blumenthal-index.md) | Blumenthal index, blumenthal source index, blumenthal guest, … |
| blumenthal-source-index | source_index | work | [statecraft/voices/blumenthal/blumenthal-source-index.md](statecraft/voices/blumenthal/blumenthal-source-index.md) | Blumenthal source index compat |
| breaking-points-channel-index | source_index | work | [statecraft/channels/breaking-points/breaking-points-channel-index.md](statecraft/channels/breaking-points/breaking-points-channel-index.md) | Breaking Points index, breaking-points-channel-index, breaking-points index |
| breaking-points-host-shelf | routing_aid | work | [statecraft/channels/breaking-points/README.md](statecraft/channels/breaking-points/README.md) | Breaking Points host, breaking-points profile |
| breaking-points-index | source_index | work | [statecraft/channels/breaking-points/breaking-points-index.md](statecraft/channels/breaking-points/breaking-points-index.md) | Breaking Points index compat |
| channel-index-roster | routing_aid | work | `statecraft/channels/channel-index.json` | channel index, channel-index.json, channel-index.md, … |
| crooke-index | source_index | work | [statecraft/voices/crooke/crooke-index.md](statecraft/voices/crooke/crooke-index.md) | Crooke index, crooke source index |
| crooke-source-index | source_index | work | [statecraft/voices/crooke/crooke-source-index.md](statecraft/voices/crooke/crooke-source-index.md) | Crooke index, crooke source index, crooke source index compat |
| cyrus-janssen-channel-index | source_index | work | [statecraft/channels/cyrus-janssen/cyrus-janssen-channel-index.md](statecraft/channels/cyrus-janssen/cyrus-janssen-channel-index.md) | Cyrus Janssen index, cyrus-janssen-channel-index, cyrus-janssen index |
| cyrus-janssen-host-shelf | routing_aid | work | [statecraft/channels/cyrus-janssen/README.md](statecraft/channels/cyrus-janssen/README.md) | Cyrus Janssen host, cyrus-janssen profile |
| cyrus-janssen-index | source_index | work | [statecraft/channels/cyrus-janssen/cyrus-janssen-index.md](statecraft/channels/cyrus-janssen/cyrus-janssen-index.md) | Cyrus Janssen index compat |
| daniel-davis-channel-index | source_index | work | [statecraft/channels/daniel-davis/daniel-davis-channel-index.md](statecraft/channels/daniel-davis/daniel-davis-channel-index.md) | Daniel Davis index, daniel-davis-channel-index, daniel-davis-index, … |
| daniel-davis-host-shelf | routing_aid | work | [statecraft/channels/daniel-davis/README.md](statecraft/channels/daniel-davis/README.md) | Davis host, Daniel Davis, Deep Dive host, … |
| davis-index | source_index | work | [statecraft/voices/davis/davis-index.md](statecraft/voices/davis/davis-index.md) | Davis guest index, davis-index, Daniel Davis guest, … |
| davis-source-index | source_index | work | [statecraft/voices/davis/davis-source-index.md](statecraft/voices/davis/davis-source-index.md) | Davis index, davis source index |
| dialogue-works-channel-index | source_index | work | [statecraft/channels/dialogue-works/dialogue-works-channel-index.md](statecraft/channels/dialogue-works/dialogue-works-channel-index.md) | Dialogue Works index, dialogue-works-channel-index, dialogue-works-index, … |
| dialogue-works-host-shelf | routing_aid | work | [statecraft/channels/dialogue-works/README.md](statecraft/channels/dialogue-works/README.md) | Nima host, Dialogue Works host, Nima profile, … |
| diesen-index | source_index | work | [statecraft/voices/diesen/diesen-index.md](statecraft/voices/diesen/diesen-index.md) | Diesen guest index, diesen cross-host |
| diesen-source-index | source_index | work | [statecraft/voices/diesen/diesen-source-index.md](statecraft/voices/diesen/diesen-source-index.md) | Diesen index, diesen source index |
| essays-shelf | prose_shelf | work | [essays/README.md](essays/README.md) | essays shelf, stand-alone essay, cross-channel essay, … |
| freeman-index | source_index | work | [statecraft/voices/freeman/freeman-index.md](statecraft/voices/freeman/freeman-index.md) | Freeman index, freeman source index |
| freeman-source-index | source_index | work | [statecraft/voices/freeman/freeman-source-index.md](statecraft/voices/freeman/freeman-source-index.md) | Freeman index, freeman source index, freeman source index compat |
| glenn-diesen-channel-index | source_index | work | [statecraft/channels/glenn-diesen/glenn-diesen-channel-index.md](statecraft/channels/glenn-diesen/glenn-diesen-channel-index.md) | Glenn Diesen index, glenn-diesen-channel-index, glenn-diesen index |
| glenn-diesen-host-shelf | routing_aid | work | [statecraft/channels/glenn-diesen/README.md](statecraft/channels/glenn-diesen/README.md) | Glenn Diesen host, glenn-diesen profile |
| glenn-diesen-index | source_index | work | [statecraft/channels/glenn-diesen/glenn-diesen-index.md](statecraft/channels/glenn-diesen/glenn-diesen-index.md) | Glenn Diesen index compat |
| grace-mar-self-library | canonical_reference | archive | [archive/grace-mar-instance/self-library.md](archive/grace-mar-instance/self-library.md) | grace mar library, museum books index |
| helmer-index | source_index | work | [statecraft/voices/helmer/helmer-index.md](statecraft/voices/helmer/helmer-index.md) | Helmer index, helmer source index |
| helmer-source-index | source_index | work | [statecraft/voices/helmer/helmer-source-index.md](statecraft/voices/helmer/helmer-source-index.md) | Helmer index, helmer source index, helmer source index compat |
| high-skill-labor-american-command-essay | essay | work | [essays/high-skill-labor-compression-and-american-command.md](essays/high-skill-labor-compression-and-american-command.md) | high skill labor compression, american command essay, vendor carried command, … |
| hoh-index | source_index | work | [statecraft/voices/hoh/hoh-index.md](statecraft/voices/hoh/hoh-index.md) | Hoh index, hoh source index |
| hoh-source-index | source_index | work | [statecraft/voices/hoh/hoh-source-index.md](statecraft/voices/hoh/hoh-source-index.md) | Hoh index, hoh source index, hoh source index compat |
| india-global-left-channel-index | source_index | work | [statecraft/channels/india-global-left/india-global-left-channel-index.md](statecraft/channels/india-global-left/india-global-left-channel-index.md) | India and Global Left index, india-global-left-channel-index, india-global-left index |
| india-global-left-host-shelf | routing_aid | work | [statecraft/channels/india-global-left/README.md](statecraft/channels/india-global-left/README.md) | India Global Left host, india-global-left profile |
| india-global-left-index | source_index | work | [statecraft/channels/india-global-left/india-global-left-index.md](statecraft/channels/india-global-left/india-global-left-index.md) | India and Global Left index compat |
| iran-nuclear-threshold-hardened-essay | essay | work | [essays/how-the-iran-nuclear-threshold-story-hardened.md](essays/how-the-iran-nuclear-threshold-story-hardened.md) | iran nuclear threshold hardened, June 2 Pakistan offer, crude device demonstration test, … |
| jermy-index | source_index | work | [statecraft/voices/jermy/jermy-index.md](statecraft/voices/jermy/jermy-index.md) | Jermy index, jermy source index |
| jermy-source-index | source_index | work | [statecraft/voices/jermy/jermy-source-index.md](statecraft/voices/jermy/jermy-source-index.md) | Jermy index, jermy source index, jermy source index compat |
| jiang-index | source_index | work | [statecraft/voices/jiang/jiang-index.md](statecraft/voices/jiang/jiang-index.md) | Jiang index, jiang source index |
| jiang-source-index | source_index | work | [statecraft/voices/jiang/jiang-source-index.md](statecraft/voices/jiang/jiang-source-index.md) | Jiang index, jiang source index, jiang source index compat |
| johnson-index | source_index | work | [statecraft/voices/johnson/johnson-index.md](statecraft/voices/johnson/johnson-index.md) | Johnson index, johnson source index |
| johnson-source-index | source_index | work | [statecraft/voices/johnson/johnson-source-index.md](statecraft/voices/johnson/johnson-source-index.md) | Johnson index, johnson source index, johnson source index compat |
| judging-freedom-channel-index | source_index | work | [statecraft/channels/judging-freedom/judging-freedom-channel-index.md](statecraft/channels/judging-freedom/judging-freedom-channel-index.md) | Judging Freedom index, judging-freedom-channel-index, judging-freedom index, … |
| judging-freedom-host-shelf | routing_aid | work | [statecraft/channels/judging-freedom/README.md](statecraft/channels/judging-freedom/README.md) | Napolitano host, Judging Freedom, Napolitano profile, … |
| judging-freedom-index | source_index | work | [statecraft/channels/judging-freedom/judging-freedom-index.md](statecraft/channels/judging-freedom/judging-freedom-index.md) | Judging Freedom index compat |
| karaganov-index | source_index | work | [statecraft/voices/karaganov/karaganov-index.md](statecraft/voices/karaganov/karaganov-index.md) | Karaganov index, karaganov source index |
| karaganov-source-index | source_index | work | [statecraft/voices/karaganov/karaganov-source-index.md](statecraft/voices/karaganov/karaganov-source-index.md) | Karaganov index, karaganov source index, karaganov source index compat |
| kent-index | source_index | work | [statecraft/voices/kent/kent-index.md](statecraft/voices/kent/kent-index.md) | Kent index, kent source index |
| kent-source-index | source_index | work | [statecraft/voices/kent/kent-source-index.md](statecraft/voices/kent/kent-source-index.md) | Kent index, kent source index, kent source index compat |
| krapivnik-index | source_index | work | [statecraft/voices/krapivnik/krapivnik-index.md](statecraft/voices/krapivnik/krapivnik-index.md) | Krapivnik index, krapivnik source index |
| krapivnik-source-index | source_index | work | [statecraft/voices/krapivnik/krapivnik-source-index.md](statecraft/voices/krapivnik/krapivnik-source-index.md) | Krapivnik index, krapivnik source index, krapivnik source index compat |
| lascaris-index | source_index | work | [statecraft/voices/lascaris/lascaris-index.md](statecraft/voices/lascaris/lascaris-index.md) | Lascaris index, lascaris source index |
| lascaris-source-index | source_index | work | [statecraft/voices/lascaris/lascaris-source-index.md](statecraft/voices/lascaris/lascaris-source-index.md) | Lascaris index, lascaris source index, lascaris source index compat |
| library-index-retired | generated_dashboard | generated | [runtime/artifacts/library-index.md](runtime/artifacts/library-index.md) | operator books misc homes |
| llm-routing | routing_aid | generated | [LLM-ROUTING.md](LLM-ROUTING.md) | LLM routing, find file in repo, Barnes index |
| macgregor-index | source_index | work | [statecraft/voices/macgregor/macgregor-index.md](statecraft/voices/macgregor/macgregor-index.md) | Macgregor index, macgregor source index |
| macgregor-source-index | source_index | work | [statecraft/voices/macgregor/macgregor-source-index.md](statecraft/voices/macgregor/macgregor-source-index.md) | Macgregor index, macgregor source index, macgregor source index compat |
| marandi-index | source_index | work | [statecraft/voices/marandi/marandi-index.md](statecraft/voices/marandi/marandi-index.md) | Marandi index, marandi source index |
| marandi-source-index | source_index | work | [statecraft/voices/marandi/marandi-source-index.md](statecraft/voices/marandi/marandi-source-index.md) | Marandi index, marandi source index, marandi source index compat |
| mario-nawfal-channel-index | source_index | work | [statecraft/channels/mario-nawfal/mario-nawfal-channel-index.md](statecraft/channels/mario-nawfal/mario-nawfal-channel-index.md) | Mario Nawfal index, mario-nawfal-channel-index, mario-nawfal index |
| mario-nawfal-host-shelf | routing_aid | work | [statecraft/channels/mario-nawfal/README.md](statecraft/channels/mario-nawfal/README.md) | Mario Nawfal host, mario-nawfal profile |
| mario-nawfal-index | source_index | work | [statecraft/channels/mario-nawfal/mario-nawfal-index.md](statecraft/channels/mario-nawfal/mario-nawfal-index.md) | Mario Nawfal index compat |
| martyanov-index | source_index | work | [statecraft/voices/martyanov/martyanov-index.md](statecraft/voices/martyanov/martyanov-index.md) | Martyanov index, martyanov source index |
| martyanov-source-index | source_index | work | [statecraft/voices/martyanov/martyanov-source-index.md](statecraft/voices/martyanov/martyanov-source-index.md) | Martyanov index, martyanov source index, martyanov source index compat |
| mate-index | source_index | work | [statecraft/voices/mate/mate-index.md](statecraft/voices/mate/mate-index.md) | Mate index, Maté index, mate source index |
| mate-source-index | source_index | work | [statecraft/voices/mate/mate-source-index.md](statecraft/voices/mate/mate-source-index.md) | Maté index, mate source index, mate source index compat |
| mcgovern-index | source_index | work | [statecraft/voices/mcgovern/mcgovern-index.md](statecraft/voices/mcgovern/mcgovern-index.md) | Mcgovern index, McGovern index, mcgovern source index |
| mcgovern-source-index | source_index | work | [statecraft/voices/mcgovern/mcgovern-source-index.md](statecraft/voices/mcgovern/mcgovern-source-index.md) | McGovern index, mcgovern source index, mcgovern source index compat |
| mearsheimer-index | source_index | work | [statecraft/voices/mearsheimer/mearsheimer-index.md](statecraft/voices/mearsheimer/mearsheimer-index.md) | Mearsheimer index, mearsheimer source index |
| mearsheimer-source-index | source_index | work | [statecraft/voices/mearsheimer/mearsheimer-source-index.md](statecraft/voices/mearsheimer/mearsheimer-source-index.md) | Mearsheimer index, mearsheimer source index, mearsheimer source index compat |
| memory | canonical_reference | work | [memory.md](memory.md) | session continuity, operator memory buffer |
| mercouris-analytical-bench | routing_aid | work | [statecraft/voices/mercouris/mercouris-analytical-bench.md](statecraft/voices/mercouris/mercouris-analytical-bench.md) | Mercouris analytical bench, mercouris hinges, mercouris cross-weaves |
| mercouris-index | source_index | work | [statecraft/voices/mercouris/mercouris-index.md](statecraft/voices/mercouris/mercouris-index.md) | Mercouris index, mercouris cross-host, Alexander Mercouris guest |
| mercouris-source-index | source_index | work | [statecraft/voices/mercouris/mercouris-source-index.md](statecraft/voices/mercouris/mercouris-source-index.md) | Mercouris index, mercouris source index, mercouris source index compat |
| moral-resistance-channel-index | source_index | work | [statecraft/channels/moral-resistance/moral-resistance-channel-index.md](statecraft/channels/moral-resistance/moral-resistance-channel-index.md) | Moral Resistance index, moral-resistance-channel-index, moral-resistance index |
| moral-resistance-host-shelf | routing_aid | work | [statecraft/channels/moral-resistance/README.md](statecraft/channels/moral-resistance/README.md) | Moral Resistance host, moral-resistance profile |
| moral-resistance-index | source_index | work | [statecraft/channels/moral-resistance/moral-resistance-index.md](statecraft/channels/moral-resistance/moral-resistance-index.md) | Moral Resistance index compat |
| neutrality-studies-channel-index | source_index | work | [statecraft/channels/neutrality-studies/neutrality-studies-channel-index.md](statecraft/channels/neutrality-studies/neutrality-studies-channel-index.md) | Neutrality Studies index, neutrality-studies-channel-index, neutrality-studies index |
| neutrality-studies-host-shelf | routing_aid | work | [statecraft/channels/neutrality-studies/README.md](statecraft/channels/neutrality-studies/README.md) | Neutrality Studies host, neutrality-studies profile |
| neutrality-studies-index | source_index | work | [statecraft/channels/neutrality-studies/neutrality-studies-index.md](statecraft/channels/neutrality-studies/neutrality-studies-index.md) | Neutrality Studies index compat |
| operator-uses-statecraft-machine-essay | essay | work | [essays/how-the-operator-uses-the-statecraft-machine.md](essays/how-the-operator-uses-the-statecraft-machine.md) | how operator uses statecraft, memory to mechanism, lane membrane test, … |
| pape-index | source_index | work | [statecraft/voices/pape/pape-index.md](statecraft/voices/pape/pape-index.md) | Pape index, pape source index, pape guest, … |
| pape-source-index | source_index | work | [statecraft/voices/pape/pape-source-index.md](statecraft/voices/pape/pape-source-index.md) | Pape source index compat |
| parsi-index | source_index | work | [statecraft/voices/parsi/parsi-index.md](statecraft/voices/parsi/parsi-index.md) | Parsi index, parsi source index |
| parsi-source-index | source_index | work | [statecraft/voices/parsi/parsi-source-index.md](statecraft/voices/parsi/parsi-source-index.md) | Parsi index, parsi source index, parsi source index compat |
| ph-civ-source-lattice | reading_discipline | work | [public/predictive-history/docs/source-lattice.md](public/predictive-history/docs/source-lattice.md) | PH chapter reading order, civ transcript floor, commentary canvas order |
| postol-index | source_index | work | [statecraft/voices/postol/postol-index.md](statecraft/voices/postol/postol-index.md) | Postol index, postol source index |
| postol-source-index | source_index | work | [statecraft/voices/postol/postol-source-index.md](statecraft/voices/postol/postol-source-index.md) | Postol index, postol source index, postol source index compat |
| predictive-history-channel-index | source_index | work | [statecraft/channels/predictive-history/predictive-history-channel-index.md](statecraft/channels/predictive-history/predictive-history-channel-index.md) | Predictive History index, predictive-history-channel-index, predictive-history index |
| predictive-history-host-shelf | routing_aid | work | [statecraft/channels/predictive-history/README.md](statecraft/channels/predictive-history/README.md) | Predictive History host, predictive-history profile |
| predictive-history-index | source_index | work | [statecraft/channels/predictive-history/predictive-history-index.md](statecraft/channels/predictive-history/predictive-history-index.md) | Predictive History index compat |
| product-identity-essay | essay | work | [essays/from-accumulation-to-governed-interpretive-machine.md](essays/from-accumulation-to-governed-interpretive-machine.md) | governed interpretive machine, what is strategy-codex becoming, accumulation essay |
| prose-index | routing_aid | work | [docs/prose-index.md](docs/prose-index.md) | prose index, note vs essay, where to put prose, … |
| reason-resist-channel-index | source_index | work | [statecraft/channels/reason-resist/reason-resist-channel-index.md](statecraft/channels/reason-resist/reason-resist-channel-index.md) | Reason to Resist index, reason-resist-channel-index, Lascaris host |
| reason-resist-host-shelf | routing_aid | work | [statecraft/channels/reason-resist/README.md](statecraft/channels/reason-resist/README.md) | Reason Resist host, reason-resist profile |
| record-vector-index-script | local_index_script | work | `scripts/index_record.py` | vector index, chroma index, record embeddings |
| recursive-learning-three-layers-essay | essay | work | [essays/three-layers-of-recursive-learning-in-statecraft.md](essays/three-layers-of-recursive-learning-in-statecraft.md) | three layers recursive learning, recursive learning journal essay, instruction drift learning |
| redacted-news-channel-index | source_index | work | [statecraft/channels/redacted-news/redacted-news-channel-index.md](statecraft/channels/redacted-news/redacted-news-channel-index.md) | Redacted News index, redacted-news-channel-index, redacted-news index |
| redacted-news-host-shelf | routing_aid | work | [statecraft/channels/redacted-news/README.md](statecraft/channels/redacted-news/README.md) | Redacted News host, redacted-news profile |
| redacted-news-index | source_index | work | [statecraft/channels/redacted-news/redacted-news-index.md](statecraft/channels/redacted-news/redacted-news-index.md) | Redacted News index compat |
| ritter-index | source_index | work | [statecraft/voices/ritter/ritter-index.md](statecraft/voices/ritter/ritter-index.md) | Ritter index, ritter source index |
| ritter-source-index | source_index | work | [statecraft/voices/ritter/ritter-source-index.md](statecraft/voices/ritter/ritter-source-index.md) | Ritter index, ritter source index, ritter source index compat |
| sachs-index | source_index | work | [statecraft/voices/sachs/sachs-index.md](statecraft/voices/sachs/sachs-index.md) | Sachs index, sachs source index |
| sachs-source-index | source_index | work | [statecraft/voices/sachs/sachs-source-index.md](statecraft/voices/sachs/sachs-source-index.md) | Sachs index, sachs source index, sachs source index compat |
| source-lattice-doctrine | reading_discipline | work | [docs/source-lattice-beyond-the-repo.md](docs/source-lattice-beyond-the-repo.md) | source lattice, corpus tiers, reading order, … |
| speaker-cluster-map | routing_aid | work | [statecraft/voices/speaker-cluster-map.md](statecraft/voices/speaker-cluster-map.md) | speaker cluster map, satellite speaker, which speaker after Pape, … |
| statecraft-day-source-index | generated_inventory | generated | [source-archive/statecraft/YYYY-MM-DD/day-index.md](source-archive/statecraft/YYYY-MM-DD/day-index.md) | day index, day-index, june 17 day index, … |
| statecraft-source-capture | source_capture | source | [source-archive/statecraft/YYYY-MM-DD/source-*.md](source-archive/statecraft/YYYY-MM-DD/source-*.md) | source capture, verbatim transcript, statecraft source file, … |
| statecraft-thread-index | generated_inventory | generated | [source-archive/statecraft/thread-index.md](source-archive/statecraft/thread-index.md) | thread index, archive inventory |
| the-duran-channel-index | source_index | work | [statecraft/channels/the-duran/the-duran-channel-index.md](statecraft/channels/the-duran/the-duran-channel-index.md) | The Duran index, the-duran-channel-index, the-duran-index, … |
| the-duran-host-shelf | routing_aid | work | [statecraft/channels/the-duran/README.md](statecraft/channels/the-duran/README.md) | The Duran host, the-duran profile |
| tucker-carlson-channel-index | source_index | work | [statecraft/channels/tucker-carlson/tucker-carlson-channel-index.md](statecraft/channels/tucker-carlson/tucker-carlson-channel-index.md) | Tucker Carlson index, tucker-carlson-channel-index, tucker-carlson index |
| tucker-carlson-host-shelf | routing_aid | work | [statecraft/channels/tucker-carlson/README.md](statecraft/channels/tucker-carlson/README.md) | Tucker Carlson host, tucker-carlson profile |
| tucker-carlson-index | source_index | work | [statecraft/channels/tucker-carlson/tucker-carlson-index.md](statecraft/channels/tucker-carlson/tucker-carlson-index.md) | Tucker Carlson index compat |
| voices-index | directory_index | work | [statecraft/voices/voice-index.md](statecraft/voices/voice-index.md) | voices index, civ-lens legacy, analyst source index |
| weichert-index | source_index | work | [statecraft/voices/weichert/weichert-index.md](statecraft/voices/weichert/weichert-index.md) | Weichert index, weichert source index, Nawfal Weichert |
| weichert-source-index | source_index | work | [statecraft/voices/weichert/weichert-source-index.md](statecraft/voices/weichert/weichert-source-index.md) | Weichert index, weichert source index, Nawfal Weichert, … |
| wilkerson-index | source_index | work | [statecraft/voices/wilkerson/wilkerson-index.md](statecraft/voices/wilkerson/wilkerson-index.md) | Wilkerson index, wilkerson source index |
| wilkerson-source-index | source_index | work | [statecraft/voices/wilkerson/wilkerson-source-index.md](statecraft/voices/wilkerson/wilkerson-source-index.md) | Wilkerson index, wilkerson source index, wilkerson source index compat |

## Source index registry (generated)

| speaker | path | repo-map id |
|---|---|---|
| barnes | [statecraft/voices/barnes/barnes-index.md](statecraft/voices/barnes/barnes-index.md) | barnes-index |
| blumenthal | [statecraft/voices/blumenthal/blumenthal-index.md](statecraft/voices/blumenthal/blumenthal-index.md) | blumenthal-index |
| crooke | [statecraft/voices/crooke/crooke-index.md](statecraft/voices/crooke/crooke-index.md) | crooke-index |
| davis | [statecraft/voices/davis/davis-index.md](statecraft/voices/davis/davis-index.md) | davis-index |
| diesen | [statecraft/voices/diesen/diesen-index.md](statecraft/voices/diesen/diesen-index.md) | diesen-index |
| freeman | [statecraft/voices/freeman/freeman-index.md](statecraft/voices/freeman/freeman-index.md) | freeman-index |
| helmer | [statecraft/voices/helmer/helmer-index.md](statecraft/voices/helmer/helmer-index.md) | helmer-index |
| hoh | [statecraft/voices/hoh/hoh-index.md](statecraft/voices/hoh/hoh-index.md) | hoh-index |
| jermy | [statecraft/voices/jermy/jermy-index.md](statecraft/voices/jermy/jermy-index.md) | jermy-index |
| jiang | [statecraft/voices/jiang/jiang-index.md](statecraft/voices/jiang/jiang-index.md) | jiang-index |
| johnson | [statecraft/voices/johnson/johnson-index.md](statecraft/voices/johnson/johnson-index.md) | johnson-index |
| karaganov | [statecraft/voices/karaganov/karaganov-index.md](statecraft/voices/karaganov/karaganov-index.md) | karaganov-index |
| kent | [statecraft/voices/kent/kent-index.md](statecraft/voices/kent/kent-index.md) | kent-index |
| krapivnik | [statecraft/voices/krapivnik/krapivnik-index.md](statecraft/voices/krapivnik/krapivnik-index.md) | krapivnik-index |
| lascaris | [statecraft/voices/lascaris/lascaris-index.md](statecraft/voices/lascaris/lascaris-index.md) | lascaris-index |
| macgregor | [statecraft/voices/macgregor/macgregor-index.md](statecraft/voices/macgregor/macgregor-index.md) | macgregor-index |
| marandi | [statecraft/voices/marandi/marandi-index.md](statecraft/voices/marandi/marandi-index.md) | marandi-index |
| martyanov | [statecraft/voices/martyanov/martyanov-index.md](statecraft/voices/martyanov/martyanov-index.md) | martyanov-index |
| mate | [statecraft/voices/mate/mate-index.md](statecraft/voices/mate/mate-index.md) | mate-index |
| mcgovern | [statecraft/voices/mcgovern/mcgovern-index.md](statecraft/voices/mcgovern/mcgovern-index.md) | mcgovern-index |
| mearsheimer | [statecraft/voices/mearsheimer/mearsheimer-index.md](statecraft/voices/mearsheimer/mearsheimer-index.md) | mearsheimer-index |
| mercouris | [statecraft/voices/mercouris/mercouris-index.md](statecraft/voices/mercouris/mercouris-index.md) | mercouris-index |
| pape | [statecraft/voices/pape/pape-index.md](statecraft/voices/pape/pape-index.md) | pape-index |
| parsi | [statecraft/voices/parsi/parsi-index.md](statecraft/voices/parsi/parsi-index.md) | parsi-index |
| postol | [statecraft/voices/postol/postol-index.md](statecraft/voices/postol/postol-index.md) | postol-index |
| ritter | [statecraft/voices/ritter/ritter-index.md](statecraft/voices/ritter/ritter-index.md) | ritter-index |
| sachs | [statecraft/voices/sachs/sachs-index.md](statecraft/voices/sachs/sachs-index.md) | sachs-index |
| weichert | [statecraft/voices/weichert/weichert-index.md](statecraft/voices/weichert/weichert-index.md) | weichert-index |
| wilkerson | [statecraft/voices/wilkerson/wilkerson-index.md](statecraft/voices/wilkerson/wilkerson-index.md) | wilkerson-index |

## Host shelf registry (generated)

| host | path | repo-map id |
|---|---|---|
| alexander-mercouris | [statecraft/channels/alexander-mercouris/README.md](statecraft/channels/alexander-mercouris/README.md) | alexander-mercouris-host-shelf |
| breaking-points | [statecraft/channels/breaking-points/README.md](statecraft/channels/breaking-points/README.md) | breaking-points-host-shelf |
| cyrus-janssen | [statecraft/channels/cyrus-janssen/README.md](statecraft/channels/cyrus-janssen/README.md) | cyrus-janssen-host-shelf |
| daniel-davis | [statecraft/channels/daniel-davis/README.md](statecraft/channels/daniel-davis/README.md) | daniel-davis-host-shelf |
| dialogue-works | [statecraft/channels/dialogue-works/README.md](statecraft/channels/dialogue-works/README.md) | dialogue-works-host-shelf |
| glenn-diesen | [statecraft/channels/glenn-diesen/README.md](statecraft/channels/glenn-diesen/README.md) | glenn-diesen-host-shelf |
| india-global-left | [statecraft/channels/india-global-left/README.md](statecraft/channels/india-global-left/README.md) | india-global-left-host-shelf |
| judging-freedom | [statecraft/channels/judging-freedom/README.md](statecraft/channels/judging-freedom/README.md) | judging-freedom-host-shelf |
| mario-nawfal | [statecraft/channels/mario-nawfal/README.md](statecraft/channels/mario-nawfal/README.md) | mario-nawfal-host-shelf |
| moral-resistance | [statecraft/channels/moral-resistance/README.md](statecraft/channels/moral-resistance/README.md) | moral-resistance-host-shelf |
| neutrality-studies | [statecraft/channels/neutrality-studies/README.md](statecraft/channels/neutrality-studies/README.md) | neutrality-studies-host-shelf |
| predictive-history | [statecraft/channels/predictive-history/README.md](statecraft/channels/predictive-history/README.md) | predictive-history-host-shelf |
| reason-resist | [statecraft/channels/reason-resist/README.md](statecraft/channels/reason-resist/README.md) | reason-resist-host-shelf |
| redacted-news | [statecraft/channels/redacted-news/README.md](statecraft/channels/redacted-news/README.md) | redacted-news-host-shelf |
| the-duran | [statecraft/channels/the-duran/README.md](statecraft/channels/the-duran/README.md) | the-duran-host-shelf |
| tucker-carlson | [statecraft/channels/tucker-carlson/README.md](statecraft/channels/tucker-carlson/README.md) | tucker-carlson-host-shelf |

## Repo routing metrics

- source indexes (disk): 29
- host shelves (disk): 16
- markdown links (INDEX + source-index files): 134
- repo-map routes: 127 (canonical_reference=2, directory_index=1, essay=8, generated_dashboard=1, generated_inventory=2, local_index_script=1, prose_shelf=1, reading_discipline=2, routing_aid=21, source_capture=1, source_index=87)
- source_index routes in repo-map: 87
- host_shelf routes in repo-map: 16
- registry: INDEX lists 29/29, repo-map lists 29/29 (100.0% bijection when both match)
- host shelves: repo-map lists 16/16 (100.0%)
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
| [statecraft/voices/voice-index.md](../../statecraft/voices/voice-index.md) | Front door listing all analyst source indexes | WORK routing aid |
| [source-archive/statecraft/thread-index.md](../../source-archive/statecraft/thread-index.md) | Generated capture **inventory** by thread | Derived / archive |
| [archive/grace-mar-instance/self-library.md](../../archive/grace-mar-instance/self-library.md) | Canonical removed operator-books symlink reference layer | Canonical reference |
| [runtime/artifacts/library-index.md](../../runtime/artifacts/library-index.md) | Derived removed operator-books symlink **dashboard** | Derived |
| [scripts/index_record.py](scripts/index_record.py) | Local Chroma / Record vector index builder | Derived local |
| [docs/archive/codex-speakers-deprecated.md](../archive/codex-speakers-deprecated.md) | Tombstone for terminated `codex/speakers/` | Archive |
| [statecraft/channels/](../../statecraft/channels) | Host-family continuity (Davis, Napolitano, Nima / Dialogue Works) | WORK only |
| [statecraft/channels/channel-index.json](../../statecraft/channels/channel-index.json) | **YouTube channel roster** (main) — check-sources SSOT; human: [channel-index.md](../../statecraft/channels/channel-index.md) | Derived from archive; rebuild via `refresh_statecraft_archive_indices.py` |
| [statecraft/voices/speaker-cluster-map.md](../../statecraft/voices/speaker-cluster-map.md) | Anchor-and-satellite routing after Pape/Ritter/Parsi/Crooke | WORK routing aid |
| `statecraft/voices/<speaker>/<speaker>-profile.md` | Per-speaker identity, voice fingerprint, pairing hub | WORK only (migrated SSOT) |
| [codex/profiles/*-profile.md](../../codex/profiles) | Profile-only lanes or pre-migration compatibility | Compatibility / profile-only |

**Essays vs channel essay folders vs notes:**

| Surface | Job | Authority |
|---|---|---|
| [essays/README.md](../../essays/README.md) | **Primary** stand-alone / cross-channel theses | WORK prose shelf |
| `statecraft/notes/` · `singularity/notes/` | Channel-scoped bounded interpretive objects | WORK prose shelf |
| `statecraft/essays/` · `singularity/essays/` | Pre-root **compatibility** essay holdings | Stubs → `essays/` |
| [docs/prose-index.md](../prose-index.md) | Note vs essay vs synthesis class chooser | WORK routing aid |

**Do not** answer "no Barnes index" because `library-index.md` or GitHub code search returned zero hits.

## Source index vs source-lattice

| Term | Question | Where |
|---|---|---|
| **source-index** | *Where* is the corpus? Which file opens first? | voices `*-source-index.md` for **analyst** scope; **`source-archive/statecraft/YYYY-MM-DD/day-index.md`** for **one archive day** |
| **source-lattice** | *How* should layers be read so summary does not replace source? | [docs/source-lattice-beyond-the-repo.md](../source-lattice-beyond-the-repo.md) |

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
3. Check this routing map and [repo-map.yaml](../../repo-map.yaml) before concluding absence.
4. If the query names an analyst, speaker, source corpus, or transcript set, inspect [statecraft/voices/](../../statecraft/voices) and [source-archive/statecraft/](../../statecraft).
5. If `grep`, `rg`, or GitHub code search returns zero results, treat that as a search miss, not proof of absence.
6. Do not answer "not found" until the relevant path family has been checked.
7. After locating a capture, apply find-then-read (source-lattice) before synthesis or judgment-bearing output.
