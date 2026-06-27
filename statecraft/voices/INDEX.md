WORK only; not Record.

# Voices Index

`statecraft/voices/` contains analyst **voices** (interview + written) and source-corpus **route maps** used by statecraft workflows.

For shelf-class doctrine (normalized vs lighter shelves, migration law), open [README.md](README.md).

For LLM/agent dispatch across the whole repo, open [LLM-ROUTING.md](../../LLM-ROUTING.md).

## Analyst and source-corpus lenses

| Lens | Index file |
|---|---|
| Alkorshid (Nima) | guest: [alkorshid/alkorshid-index.md](alkorshid/alkorshid-index.md) · host: [../channels/dialogue-works/dialogue-works-channel-index.md](../channels/dialogue-works/dialogue-works-channel-index.md) |
| Barnes | [barnes/barnes-source-index.md](barnes/barnes-source-index.md) |
| Blumenthal | [blumenthal/blumenthal-source-index.md](blumenthal/blumenthal-source-index.md) |
| Crooke | [crooke/crooke-source-index.md](crooke/crooke-source-index.md) |
| Dialogue Works | [../channels/dialogue-works/dialogue-works-channel-index.md](../channels/dialogue-works/dialogue-works-channel-index.md) |
| Diesen | guest: [diesen/diesen-index.md](diesen/diesen-index.md) · source: [diesen/diesen-source-index.md](diesen/diesen-source-index.md) · host: [../channels/glenn-diesen/glenn-diesen-channel-index.md](../channels/glenn-diesen/glenn-diesen-channel-index.md) |
| Freeman | [freeman/freeman-source-index.md](freeman/freeman-source-index.md) |
| Helmer | [helmer/helmer-source-index.md](helmer/helmer-source-index.md) |
| Hoh | [hoh/hoh-source-index.md](hoh/hoh-source-index.md) |
| Jiang | [jiang/jiang-source-index.md](jiang/jiang-source-index.md) |
| Jermy | [jermy/jermy-source-index.md](jermy/jermy-source-index.md) |
| Johnson | [johnson/johnson-source-index.md](johnson/johnson-source-index.md) |
| Karaganov | [karaganov/karaganov-source-index.md](karaganov/karaganov-source-index.md) |
| Lascaris | [lascaris/lascaris-source-index.md](lascaris/lascaris-source-index.md) |
| Kent | [kent/kent-source-index.md](kent/kent-source-index.md) |
| Krapivnik | [krapivnik/krapivnik-source-index.md](krapivnik/krapivnik-source-index.md) |
| Macgregor | [macgregor/macgregor-source-index.md](macgregor/macgregor-source-index.md) |
| Maté | [mate/mate-source-index.md](mate/mate-source-index.md) |
| Marandi | [marandi/marandi-source-index.md](marandi/marandi-source-index.md) |
| Martyanov | [martyanov/martyanov-source-index.md](martyanov/martyanov-source-index.md) |
| Mearsheimer | [mearsheimer/mearsheimer-source-index.md](mearsheimer/mearsheimer-source-index.md) |
| McGovern | [mcgovern/mcgovern-source-index.md](mcgovern/mcgovern-source-index.md) |
| Mercouris | guest: [mercouris/mercouris-index.md](mercouris/mercouris-index.md) · host: [../channels/alexander-mercouris/alexander-mercouris-channel-index.md](../channels/alexander-mercouris/alexander-mercouris-channel-index.md) · bench: [mercouris/mercouris-source-index.md](mercouris/mercouris-source-index.md) |
| Pape | [pape/pape-source-index.md](pape/pape-source-index.md) |
| Parsi | [parsi/parsi-source-index.md](parsi/parsi-source-index.md) |
| Postol | [postol/postol-source-index.md](postol/postol-source-index.md) |
| Ritter | [ritter/ritter-source-index.md](ritter/ritter-source-index.md) |
| Sachs | [sachs/sachs-source-index.md](sachs/sachs-source-index.md) |
| Wilkerson | [wilkerson/wilkerson-source-index.md](wilkerson/wilkerson-source-index.md) |
| Weichert | [weichert/weichert-source-index.md](weichert/weichert-source-index.md) |

**Jiang special case:** [jiang/jiang-source-index.md](jiang/jiang-source-index.md) is the provenance bench. PH reading lattice lives at [public/predictive-history/docs/source-lattice.md](../../public/predictive-history/docs/source-lattice.md) (inbound snapshot).

## Source index vs source-lattice

- **Source index** (this file and `*-source-index.md`) answers **where**: which materialized captures exist and which file to open first.
- **Source-lattice** answers **how / when**: layer order so summary, commentary, and synthesis do not replace the source floor.

After routing through a source index into [source-archive/statecraft/](../../source-archive/statecraft/), apply [docs/source-lattice-beyond-the-repo.md](../../docs/source-lattice-beyond-the-repo.md) (corpus tiers + reading layers). PH chapter objects additionally use [public/predictive-history/docs/source-lattice.md](../../public/predictive-history/docs/source-lattice.md).

Tier-4 commentary cannot substantiate tier-3 wire claims without receipts. See source-lattice doctrine for blocking rules.

## Search guidance for LLM agents

If a user asks for an analyst, speaker, commentator, source corpus, transcript map, or "source index," start here before searching removed operator-books symlink or generated dashboards.

| Query | Expected path family |
|---|---|
| Barnes index | [barnes/](barnes/) |
| Robert Barnes corpus | [barnes/barnes-source-index.md](barnes/barnes-source-index.md), `source-archive/statecraft/**/source-*barnes*` |
| Mercouris index | [mercouris/mercouris-source-index.md](mercouris/mercouris-source-index.md) |
| Daniel Davis × guest | [davis-index.md](../channels/daniel-davis/davis-index.md) · host → [daniel-davis-channel-index](../channels/daniel-davis/daniel-davis-channel-index.md) |
| Nima / Alkorshid guest | [alkorshid/alkorshid-index.md](alkorshid/alkorshid-index.md) · host → [dialogue-works-channel-index](../channels/dialogue-works/dialogue-works-channel-index.md) |
| Mercouris guest | [mercouris/mercouris-index.md](mercouris/mercouris-index.md) · host → [alexander-mercouris-channel-index](../channels/alexander-mercouris/alexander-mercouris-channel-index.md) |
| Generic "source index" | This file → lens row → `*-source-index.md` |
| source-lattice / reading order | [docs/source-lattice-beyond-the-repo.md](../../docs/source-lattice-beyond-the-repo.md) — not this file |

Legacy **`codex/speakers/`** is terminated — [codex-speakers-deprecated.md](../../docs/archive/codex-speakers-deprecated.md). Prefer `statecraft/voices/` and `statecraft/channels/` for live statecraft routing.
