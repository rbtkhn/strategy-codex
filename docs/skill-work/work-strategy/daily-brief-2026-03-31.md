# Daily brief Ã¢â‚¬” work-politics & work-strategy

**Date:** 2026-03-31  
**Assembled:** 2026-03-31 14:59 UTC  
**Recency window (RSS):** last **36h** (undated items may appear)  
**Config:** `docs/skill-work/work-strategy/daily-brief-config.json`

_Operator WORK product. Complete synthesis below; cite sources before any public use._

## 1. Work-politics snapshot

- **Primary:** May 19, 2026 Ã¢â‚¬” **days until:** 48
- **Work-politics gate:** 0 pending candidate(s)

### Upcoming (from calendar)

- ****Apr 20, 2026**** Ã¢â‚¬” **Voter registration deadline** (in-person and mail; mail = postmark) Ã¢â‚¬” Push registration in-district; remind supporters.
- ****May 5, 2026**** Ã¢â‚¬” Mail-in absentee ballot request portal closes Ã¢â‚¬” Voters who need absentee must request by this date.
- ****May 7, 2026**** Ã¢â‚¬” **FEC pre-primary report due** Ã¢â‚¬” Covers period Apr 1Ã¢â‚¬“Apr 29. Registration/certification & overnight mail deadline May 4.
- ****May 19, 2026**** Ã¢â‚¬” **Primary election day** Ã¢â‚¬” Polls open; final GOTV.

### Territory signals (from docs)

- **research_gap:** Opposition brief still has placeholder sections
- **gate_rhythm:** No live work-politics candidates in RECURSION-GATE
- **brief_readiness:** Weekly brief sources are not fully ready

## 1b. Work-strategy focus

_From `docs/skill-work/work-strategy/daily-brief-focus.md` Ã‚§ Active focus._

- **Civilizational / geopolitics operator ledger:** [STRATEGY.md](STRATEGY.md) Ã¢â‚¬” long-horizon CORE + heuristics + Ã‚§IV operator strategy log (WORK-only; gate only when promoting to Record or milestones).
- Campaign/companion positioning: portable Record, human-only merge, Voice boundary.
- OpenClaw Ã¢â€ ” repo handback and export provenance (see [work-dev workspace](../work-dev/workspace.md)).
- AI-in-schools and identity-substrate narrative vs school bundles (see [work-dev offers](../work-dev/offers.md)).
- Optional: federal / state AI governance headlines when relevant to offers or civ-mem work.
- Long-form tech discourse (GTC-class, Moonshots-class): themes distilled in [external-tech-scan.md](external-tech-scan.md) Ã¢â‚¬” use for **strategy vocabulary** and **keyword-season** tuning in [daily-brief-config.json](daily-brief-config.json); **not** unsourced brief facts.
- **Putin Ã¢â‚¬” last 48h:** **Coffee menu C Ã¢â‚¬” Strategy (daily brief)** fills **Ã‚§1d** in the daily brief per [daily-brief-putin-watch.md](daily-brief-putin-watch.md) (web scan + citations); Step 1 does not run this pass.

## 1c. Two horizons Ã¢â‚¬” fast vs slow

**Fast (same brief):** Ã‚§**2** RSS headlines + Ã‚§**1** snapshot Ã¢â‚¬” news cycle, principal-adjacent hooks, scored **W / S / G**.

**Slow (work-jiang):** lecture extractions, compression JSON, comparative sweeps Ã¢â‚¬” **structural** context; not a substitute for dated facts. Prefer [removed operator-books symlink](../../../self-library.md) entries (e.g. reference / `lookup_priority`) when library-first lookup applies.

_From `docs/skill-work/work-strategy/daily-brief-jiang-layer.md` Ã‚§ Active work-jiang hooks._

- _Edit this section between brief runs. List repo-relative paths or one-line labels._
- _Example:_ `codex/predictive-history/compressions/<slug>-YYYYMMDD.json`
- _Example:_ `codex/predictive-history/**/*.paste-snippet.md` (paste the exact path you used)
- _Example:_ [COMPRESSION-ENGINE.md](../../../codex/predictive-history/COMPRESSION-ENGINE.md) Ã¢â‚¬” last run: _date_
- ---

_Product / integration context: [work-dev/workspace.md](../work-dev/workspace.md), [work-strategy/README.md](README.md)._

## 1d. Putin Ã¢â‚¬” last 48 hours

- **Kremlin line on U.S.-Russia channel:** Peskov says Moscow and Washington are still working ideas around a Ukraine settlement, but with no public specifics yet (slow-track, no concrete package announced).  
  - Reuters: https://www.reuters.com/world/europe/after-trump-sanctions-threat-kremlin-says-russia-us-working-ukraine-peace-moves-2025-03-31/
- **Talks posture remains unstable:** Russian-side reporting signals a "situational pause" framing around parts of the negotiation process tied to broader regional crisis load.  
  - Reuters: https://www.reuters.com/world/europe/ukraine-peace-talks-paused-amid-iran-war-russias-izvestia-says-2026-03-19/
- **Energy-security lever still active:** Putin signed law-level changes allowing private groups to use firearms to protect energy infrastructure after sustained strikes on refineries/export nodes.  
  - Reuters: https://www.reuters.com/world/putin-clears-firearm-usage-private-groups-protect-russian-energy-facilities-2026-03-24/
- **External theater signaling:** Russia publicly underscores support operations in Cuba (oil shipment + political backing language), useful as a "global reach under pressure" narrative indicator.  
  - Reuters: https://reut.rs/416Gxmi

## 2. Headlines (ingested RSS)

_Fetch failed for: Reuters Ã¢â‚¬” World._

Ranked by **W+S+G** (global keyword lists + per-`locale` maps for W/S; **G** = `geo_military_keyword_phrases`) then recency. Each feed is **recency-sorted** then **capped** (`ingest_caps`: per-feed `max_items` and/or `tier` Ã¢â€ ’ `max_items_by_tier`; CLI `--max-per-feed N` overrides all feeds). Optional **same-story** grouping uses `story_anchor_phrases` overlap (Jaccard + shared anchors). Tune phrases in config JSON.

_Same-story clusters use anchor overlap on titles (proper nouns / crisis terms); not neural / semantic dedupe._

#### Same-story (multilingual)

**guerre Ã‚· iran Ã‚· israel Ã‚· lebanon Ã‚· moyen-orient** Ã¢â‚¬” _6 sources_

- **[W:8 S:0 G:0]** [EN DIRECT, guerre au Moyen-OrientÃ‚ : Donald Trump affirme que la France a ÃƒÂ©tÃƒÂ© Ã‚Â«Ã‚ trÃƒÂ¨s peu coopÃƒÂ©rativeÃ‚ Ã‚Â» en Iran](https://www.lemonde.fr/international/live/2026/03/31/en-direct-guerre-au-moyen-orient-donald-trump-affirme-que-la-france-a-ete-tres-peu-cooperative-en-iran_6674837_3210.html) Ã¢â‚¬” _Le Monde Ã¢â‚¬” franÃƒ§ais (France / monde)_ Ã‚· _fr_ Ã‚· _2026-03-31 13:53 UTC_
- **Also** Ã¢â‚¬” [Trump tells Europe 'Go get your own oil,' Iran hits oil tanker off Dubai](https://www.npr.org/2026/03/31/nx-s1-5766991/iran-war-lebanon-israel-dubai-trump-oil-europe) Ã¢â‚¬” _NPR Ã¢â‚¬” national news_ Ã‚· _W:4 S:0 G:0_ Ã‚· _2026-03-31 06:12 UTC_
- **Also** Ã¢â‚¬” [Trump slams France for not allowing planes to fly over to Israel](https://thehill.com/homenews/administration/5808846-trump-criticizes-france-iran/) Ã¢â‚¬” _The Hill Ã¢â‚¬” politics_ Ã‚· _W:3 S:0 G:0_ Ã‚· _2026-03-31 14:11 UTC_
- **Also** Ã¢â‚¬” [Live updates: Hegseth, Trump push US allies to help reopen Strait of Hormuz as gas prices hit $4](https://thehill.com/homenews/administration/5807651-live-updates-trump-hegseth-iran-supreme-court/) Ã¢â‚¬” _The Hill Ã¢â‚¬” politics_ Ã‚· _W:2 S:1 G:0_ Ã‚· _2026-03-31 14:17 UTC_
- **Also** Ã¢â‚¬” [O’Reilly: Trump Ã¢â‚¬Ëœneeds a deal with Iran’ within 6 weeks](https://thehill.com/blogs/in-the-know/5808662-bill-oreilly-trump-iran-deal/) Ã¢â‚¬” _The Hill Ã¢â‚¬” politics_ Ã‚· _W:2 S:0 G:0_ Ã‚· _2026-03-31 14:16 UTC_

**Ã˜Â¥Ã˜Â³Ã˜Â±Ã˜§Ã˜Â¦Ã™Å Ã™â€ž Ã‚· Ã˜Â¥Ã™Å Ã˜Â±Ã˜§Ã™â€  Ã‚· Ã˜Â­Ã˜Â±Ã˜Â¨** Ã¢â‚¬” _2 sources_

- **[W:3 S:0 G:0]** [Ã˜Â¥Ã™Å Ã˜Â±Ã˜§Ã™â€  Ã˜ÂªÃ˜ÂªÃ™â€¡Ã™… Ã˜Â¥Ã˜Â³Ã˜Â±Ã˜§Ã˜Â¦Ã™Å Ã™â€ž Ã˜Â¨Ã˜§Ã˜Â³Ã˜ÂªÃ™â€¡Ã˜Â¯Ã˜§Ã™Â Ã™…Ã˜Â­Ã˜·Ã˜Â© Ã™â€žÃ˜ÂªÃ˜Â­Ã™â€žÃ™Å Ã˜Â© Ã˜§Ã™â€žÃ™…Ã™Å Ã˜§Ã™â€¡ Ã™ÂÃ™Å  Ã˜Â¬Ã˜Â²Ã™Å Ã˜Â±Ã˜Â© Ã™â€šÃ˜Â´Ã™….. Ã˜§Ã™â€žÃ˜Â­Ã˜Â±Ã˜Â¨ Ã˜Â¥Ã™â€žÃ™â€° Ã˜Â£Ã™Å Ã™â€ Ã˜Å¸](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260331-%D8%A5%D9%8A%D8%B1%D8%A7%D9%86-%D8%AA%D8%AA%D9%87%D9%85-%D8%A5%D8%B3%D8%B1%D8%A7%D8%A6%D9%8A%D9%84-%D8%A8%D8%A7%D8%B3%D8%AA%D9%87%D8%AF%D8%A7%D9%81-%D9%85%D8%AD%D8%B7%D8%A9-%D9%84%D8%AA%D8%AD%D9%84%D9%8A%D8%A9-%D8%A7%D9%84%D9%85%D9%8A%D8%A7%D9%87-%D9%81%D9%8A-%D8%AC%D8%B2%D9%8A%D8%B1%D8%A9-%D9%82%D8%B4%D9%85-%D8%A7%D9%84%D8%AD%D8%B1%D8%A8-%D8%A5%D9%84%D9%89-%D8%A3%D9%8A%D9%86) Ã¢â‚¬” _France 24 Ã¢â‚¬” Ã˜§Ã™â€žÃ˜Â¹Ã˜Â±Ã˜Â¨Ã™Å Ã˜Â© (MENA)_ Ã‚· _ar_ Ã‚· _2026-03-31 13:27 UTC_
- **Also** Ã¢â‚¬” [Ã˜§Ã™â€žÃ˜Â­Ã˜Â±Ã˜Â¨ Ã™ÂÃ™Å  Ã˜§Ã™â€žÃ˜Â´Ã˜Â±Ã™â€š Ã˜§Ã™â€žÃ˜Â£Ã™Ë†Ã˜Â³Ã˜·: Ã˜Â¥Ã™â€ Ã™ÂÃ˜Â¬Ã˜§Ã˜Â±Ã˜§Ã˜Âª Ã˜Â¹Ã™â€ Ã™Å Ã™ÂÃ˜Â© Ã™ÂÃ™Å  Ã˜Â£Ã˜ÂµÃ™ÂÃ™â€¡Ã˜§Ã™â€  Ã˜ÂºÃ˜Â±Ã˜Â¨ Ã˜Â¥Ã™Å Ã˜Â±Ã˜§Ã™â€ ](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260331-%D8%A7%D9%84%D8%AD%D8%B1%D8%A8-%D9%81%D9%8A-%D8%A7%D9%84%D8%B4%D8%B1%D9%82-%D8%A7%D9%84%D8%A3%D9%88%D8%B3%D8%B7-%D8%A5%D9%86%D9%81%D8%AC%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86%D9%8A%D9%81%D8%A9-%D9%81%D9%8A-%D8%A3%D8%B5%D9%81%D9%87%D8%A7%D9%86-%D8%BA%D8%B1%D8%A8-%D8%A5%D9%8A%D8%B1%D8%A7%D9%86) Ã¢â‚¬” _France 24 Ã¢â‚¬” Ã˜§Ã™â€žÃ˜Â¹Ã˜Â±Ã˜Â¨Ã™Å Ã˜Â© (MENA)_ Ã‚· _ar_ Ã‚· _W:2 S:0 G:0_ Ã‚· _2026-03-31 14:09 UTC_

#### Other headlines

- **[W:6 S:0 G:0]** [EN DIRECT, guerre en UkraineÃ‚ : la Russie affirme n’avoir pas reÃƒ§u de proposition Ã‚Â«Ã‚ claireÃ‚ Ã‚Â» de Kiev pour une trÃƒÂªve de PÃƒÂ¢ques](https://www.lemonde.fr/international/live/2026/03/31/en-direct-guerre-en-ukraine-la-russie-affirme-n-avoir-pas-recu-de-proposition-claire-de-kiev-pour-une-treve-de-paques_6675208_3210.html) Ã¢â‚¬” _Le Monde Ã¢â‚¬” franÃƒ§ais (France / monde)_ Ã‚· _fr_ Ã‚· _2026-03-31 13:55 UTC_
- **[W:5 S:0 G:0]** [Trump estÃƒÂ¡ librando contra IrÃƒÂ¡n una guerra basada en el instinto y no estÃƒÂ¡ funcionando](https://www.bbc.com/mundo/articles/c5yxlv2y29no?at_medium=RSS&at_campaign=rss) Ã¢â‚¬” _BBC Mundo Ã¢â‚¬” espaÃƒÂ±ol (AmÃƒÂ©ricas / global)_ Ã‚· _es_ Ã‚· _2026-03-31 02:34 UTC_
- **[W:4 S:0 G:0]** [Iran-Krieg: MysteriÃƒÂ¶ser Geheimsender funkte wohl aus Deutschland](https://www.spiegel.de/wissenschaft/technik/iran-krieg-mysterioeser-geheimsender-funkte-wohl-aus-deutschland-a-02bc2c66-45cc-4139-baf8-7284e4320a0c#ref=rss) Ã¢â‚¬” _Der Spiegel Ã¢â‚¬” Deutsch (Schlagzeilen)_ Ã‚· _de_ Ã‚· _2026-03-31 15:23 UTC_
- **[W:3 S:1 G:0]** [Israel aprueba una ley para aplicar la pena capital a los palestinos condenados por realizar ataques "terroristas" mortales](https://www.bbc.com/mundo/articles/c895g22n1qvo?at_medium=RSS&at_campaign=rss) Ã¢â‚¬” _BBC Mundo Ã¢â‚¬” espaÃƒÂ±ol (AmÃƒÂ©ricas / global)_ Ã‚· _es_ Ã‚· _2026-03-31 01:05 UTC_
- **[W:3 S:0 G:1]** [Le pÃƒÂ©trolier russe Ã‚Â«Ã‚ Anatoly-KolodkinÃ‚ Ã‚Â» est arrivÃƒÂ© Ãƒ  Cuba aprÃƒÂ¨s l’approbation de Donald Trump, malgrÃƒÂ© le blocus imposÃƒÂ© par les Etats-Unis](https://www.lemonde.fr/international/article/2026/03/31/le-petrolier-russe-anatoly-kolodkin-est-arrive-a-cuba-apres-l-approbation-de-donald-trump-malgre-le-blocus-impose-par-les-etats-unis_6675644_3210.html) Ã¢â‚¬” _Le Monde Ã¢â‚¬” franÃƒ§ais (France / monde)_ Ã‚· _fr_ Ã‚· _2026-03-31 15:05 UTC_
- **[W:3 S:0 G:0]** [L’Espagne accuse IsraÃƒÂ«l de faire Ã‚Â«Ã‚ un pas de plus vers l’apartheidÃ‚ Ã‚Â», aprÃƒÂ¨s l’instauration de la peine de mort pour les Palestiniens accusÃƒÂ©s de meurtre Ã‚Â«Ã‚ terroristeÃ‚ Ã‚Â»](https://www.lemonde.fr/international/article/2026/03/31/l-espagne-accuse-israel-de-faire-un-pas-de-plus-vers-l-apartheid-apres-l-instauration-de-la-peine-de-mort-pour-les-palestiniens-accuses-de-meurtre-terroriste_6675650_3210.html) Ã¢â‚¬” _Le Monde Ã¢â‚¬” franÃƒ§ais (France / monde)_ Ã‚· _fr_ Ã‚· _2026-03-31 15:59 UTC_
- **[W:3 S:0 G:0]** [Ukraine-Krieg: Vier Jahre nach den Massakern Ã¢â‚¬“ Butscha erinnert an Opfer](https://www.spiegel.de/ausland/ukraine-krieg-vier-jahre-nach-den-massakern-butscha-erinnert-an-opfer-a-a66fa36f-c576-4c10-8560-b31cbe21f381#ref=rss) Ã¢â‚¬” _Der Spiegel Ã¢â‚¬” Deutsch (Schlagzeilen)_ Ã‚· _de_ Ã‚· _2026-03-31 15:44 UTC_
- **[W:3 S:0 G:0]** [EspaÃƒÂ±a cierra su espacio aÃƒÂ©reo a los aviones de EE.UU. que participan en la guerra de IrÃƒÂ¡n](https://www.bbc.com/mundo/articles/czjwngwk8eeo?at_medium=RSS&at_campaign=rss) Ã¢â‚¬” _BBC Mundo Ã¢â‚¬” espaÃƒÂ±ol (AmÃƒÂ©ricas / global)_ Ã‚· _es_ Ã‚· _2026-03-30 17:57 UTC_
- **[W:2 S:0 G:1]** [Former Trump advisor joins board of Ukraine-focused drone tech company](https://www.defenseone.com/business/2026/03/former-trump-advisor-joins-board-ukraine-focused-drone-tech-company/412510/) Ã¢â‚¬” _Defense One Ã¢â‚¬” All_ Ã‚· _2026-03-31 09:30 UTC_
- **[W:2 S:0 G:1]** [Russian oil tanker docks in Cuba ending near-total blockade](https://www.bbc.com/news/articles/clyx1lrv0w5o?at_medium=RSS&at_campaign=rss) Ã¢â‚¬” _BBC News Ã¢â‚¬” World_ Ã‚· _2026-03-31 12:51 UTC_
- **[W:0 S:3 G:0]** [Supreme Court rules for Christian counselor in Ã¢â‚¬Ëœconversion therapy’ ban case](https://thehill.com/regulation/court-battles/5808840-supreme-court-counselor-conversion-therapy/) Ã¢â‚¬” _The Hill Ã¢â‚¬” politics_ Ã‚· _2026-03-31 14:16 UTC_
- **[W:2 S:0 G:0]** [Donald Trump lÃƒÂ¤sst eine Bibliothek bauen: Nichts zu lesen, aber eine goldene Rolltreppe](https://www.spiegel.de/kultur/donald-trump-laesst-eine-bibliothek-bauen-nichts-zu-lesen-aber-eine-goldene-rolltreppe-a-68531400-c2a7-4209-af22-54dc2087d532#ref=rss) Ã¢â‚¬” _Der Spiegel Ã¢â‚¬” Deutsch (Schlagzeilen)_ Ã‚· _de_ Ã‚· _2026-03-31 16:40 UTC_
- **[W:2 S:0 G:0]** [Pakistan aims to thread the needle to Middle East peace](https://thehill.com/opinion/international/5807657-pakistan-iran-conflict-ramifications/) Ã¢â‚¬” _The Hill Ã¢â‚¬” politics_ Ã‚· _2026-03-31 14:30 UTC_

## 2a. Geopolitical & military (G-ranked)

_**G** = matches on `geo_military_keyword_phrases` (+ optional locale lists in platform/config). Supports triangulation and war-powers messaging Ã¢â‚¬” **verify** claims against primary sources._

- **[W:3 S:0 G:1]** [Le pÃƒÂ©trolier russe Ã‚Â«Ã‚ Anatoly-KolodkinÃ‚ Ã‚Â» est arrivÃƒÂ© Ãƒ  Cuba aprÃƒÂ¨s l’approbation de Donald Trump, malgrÃƒÂ© le blocus imposÃƒÂ© par les Etats-Unis](https://www.lemonde.fr/international/article/2026/03/31/le-petrolier-russe-anatoly-kolodkin-est-arrive-a-cuba-apres-l-approbation-de-donald-trump-malgre-le-blocus-impose-par-les-etats-unis_6675644_3210.html) Ã¢â‚¬” _Le Monde Ã¢â‚¬” franÃƒ§ais (France / monde)_ Ã‚· _fr_ Ã‚· _2026-03-31 15:05 UTC_
- **[W:2 S:0 G:1]** [Former Trump advisor joins board of Ukraine-focused drone tech company](https://www.defenseone.com/business/2026/03/former-trump-advisor-joins-board-ukraine-focused-drone-tech-company/412510/) Ã¢â‚¬” _Defense One Ã¢â‚¬” All_ Ã‚· _2026-03-31 09:30 UTC_
- **[W:2 S:0 G:1]** [Russian oil tanker docks in Cuba ending near-total blockade](https://www.bbc.com/news/articles/clyx1lrv0w5o?at_medium=RSS&at_campaign=rss) Ã¢â‚¬” _BBC News Ã¢â‚¬” World_ Ã‚· _2026-03-31 12:51 UTC_
- **[W:1 S:0 G:1]** [Distributed data centers in our basements](https://news.ycombinator.com/item?id=47587597) Ã¢â‚¬” _Hacker News Ã¢â‚¬” front page_ Ã‚· _2026-03-31 14:05 UTC_
- **[W:1 S:0 G:1]** [Russian oil tanker docks in Cuba despite US blockade](https://thehill.com/policy/international/5808714-russian-oil-tanker-cuba/) Ã¢â‚¬” _The Hill Ã¢â‚¬” politics_ Ã‚· _2026-03-31 13:59 UTC_
- **[W:1 S:0 G:1]** [Marine Tondelier, enceinte malgrÃƒÂ© un parcours de PMA infructueux, dÃƒÂ©nonce Ã‚Â«Ã‚ les propos culpabilisantsÃ‚ Ã‚Â» d’Emmanuel Macron Ã‚Â«Ã‚ sur le rÃƒÂ©armement dÃƒÂ©mographiqueÃ‚ Ã‚Â»](https://www.lemonde.fr/societe/article/2026/03/31/marine-tondelier-enceinte-apres-un-parcours-de-fiv-denonce-les-propos-culpabilisants-d-emmanuel-macron-sur-le-rearmement-demographique_6675649_3224.html) Ã¢â‚¬” _Le Monde Ã¢â‚¬” franÃƒ§ais (France / monde)_ Ã‚· _fr_ Ã‚· _2026-03-31 15:35 UTC_
- **[W:1 S:0 G:1]** [Combinators](https://tinyapl.rubenverg.com/docs/info/combinators) Ã¢â‚¬” _Hacker News Ã¢â‚¬” front page_ Ã‚· _2026-03-31 11:49 UTC_
- **[W:1 S:0 G:1]** [Kid Rock sparks US Army probe after helicopter flyby at his mansion](https://www.bbc.com/news/articles/cdrmgvzm62no?at_medium=RSS&at_campaign=rss) Ã¢â‚¬” _BBC News Ã¢â‚¬” World_ Ã‚· _2026-03-31 02:50 UTC_
- **[W:1 S:0 G:1]** [Los intrÃƒÂ©pidos ladrones que en apenas 3 minutos robaron pinturas valuadas en US$10 millones de un museo en Italia](https://www.bbc.com/mundo/articles/cj608x5x58go?at_medium=RSS&at_campaign=rss) Ã¢â‚¬” _BBC Mundo Ã¢â‚¬” espaÃƒÂ±ol (AmÃƒÂ©ricas / global)_ Ã‚· _es_ Ã‚· _2026-03-30 11:37 UTC_
- **[W:0 S:1 G:1]** [War boosts counter-drone sales, joint ventures](https://www.defenseone.com/business/2026/03/counter-drone-sales/412504/) Ã¢â‚¬” _Defense One Ã¢â‚¬” All_ Ã‚· _2026-03-30 20:43 UTC_
- **[W:0 S:0 G:1]** [Hezbollah inspired man who crashed into Michigan synagogue: FBI](https://thehill.com/homenews/state-watch/5808634-hezbollah-inspired-man-synogogue-crash-michigan/) Ã¢â‚¬” _The Hill Ã¢â‚¬” politics_ Ã‚· _2026-03-31 14:08 UTC_
- **[W:0 S:0 G:1]** [Army suspends aircrew flying helicopters near Kid Rock's home](https://www.nbcnews.com/news/military/army-suspends-aircrew-flying-helicopters-kid-rocks-home-rcna265999) Ã¢â‚¬” _NBC News Ã¢â‚¬” politics_ Ã‚· _2026-03-31 13:51 UTC_
- **[W:0 S:0 G:1]** [ICE agents will be stationed outside Marine Corps graduation events in South Carolina](https://www.nbcnews.com/politics/national-security/ice-agents-will-stationed-marine-corps-graduation-events-south-carolin-rcna265941) Ã¢â‚¬” _NBC News Ã¢â‚¬” politics_ Ã‚· _2026-03-30 23:11 UTC_

## 2b. Civ-mem depth hooks (in-repo essays Ã¢â‚¬” not breaking news)

_Token overlap against `docs/civilization-memory/` (build: `python3 scripts/build_civmem_inrepo_index.py build`). **Historical / structural** depth only Ã¢â‚¬” not a substitute for dated news. See [civ-mem-draft-protocol](../work-politics/civ-mem-draft-protocol.md). Public copy still needs human approval._

- **{CMC: `minds/CIVÃ¢â‚¬“MINDÃ¢â‚¬“MEARSHEIMER.md`}** (overlap 2) Ã¢â‚¬” _CIVÃ¢â‚¬“MINDÃ¢â‚¬“MEARSHEIMER Ã¢â‚¬” v3.4 Civilizational Memory Codex Ã‚· Advisory Mind John J. Mearsheimer CognitiveÃ¢â‚¬“Linguistic Signature Layer Simplified Polyphony Architecture Status: ACTIVE Ã‚· CANONICAL Ã‚· LOCKED Class: MIND (ADVIS..._
- **{CMC: `minds/CIVÃ¢â‚¬“MINDÃ¢â‚¬“MERCOURIS.md`}** (overlap 2) Ã¢â‚¬” _CIVÃ¢â‚¬“MINDÃ¢â‚¬“MERCOURIS Ã¢â‚¬” v3.4 Civilizational Memory Codex Ã‚· Primary Mind Alexander Mercouris CognitiveÃ¢â‚¬“Linguistic Signature Layer Simplified Polyphony Architecture Ã‚· Proportional Blend Law Status: ACTIVE Ã‚· CANONICAL Ã‚· LOC..._

## 3. Lead themes (auto-stub Ã¢â‚¬” replace after reading)

### Work-politics / campaign angle
- EN DIRECT, guerre au Moyen-OrientÃ‚ : Donald Trump affirme que la France a ÃƒÂ©tÃƒÂ© Ã‚Â«Ã‚ trÃƒÂ¨s peu coopÃƒÂ©rativeÃ‚ Ã‚Â» en Iran
- EN DIRECT, guerre en UkraineÃ‚ : la Russie affirme n’avoir pas reÃƒ§u de proposition Ã‚Â«Ã‚ claireÃ‚ Ã‚Â» de Kiev pour une trÃƒÂªve de PÃƒÂ¢ques
- Trump estÃƒÂ¡ librando contra IrÃƒÂ¡n una guerra basada en el instinto y no estÃƒÂ¡ funcionando

**Replace:** 2Ã¢â‚¬“3 sentences for principal, district, opposition narrative.

### Work-strategy angle (product / governance / tech)

- Supreme Court rules for Christian counselor in Ã¢â‚¬Ëœconversion therapy’ ban case
- Supreme Court rules against Colorado ban on conversion therapy aimed at LGBTQ youth
- Supreme Court rules against Colorado's ban on conversion therapy aimed at LGBTQ youth

**Replace:** 2Ã¢â‚¬“3 sentences for Record/Voice positioning, OpenClaw, schools, or policy hooks.

### Slow structural layer (work-jiang)

_Not dated news Ã¢â‚¬” patterns from lecture extractions, `jiang-compress` JSON, comparative sweeps. Connect to **Ã‚§1c** hooks when drafting campaign or opposition copy; cite sources if anything ships publicly._

**Replace:** 2Ã¢â‚¬“3 sentences Ã¢â‚¬” which slow pattern applies to today’s **W** angle, or why none does.

## 4. Triangulation (when lead is political)

For **campaign-facing** copy, use [work-politics analytical-lenses](../work-politics/analytical-lenses/template-three-lenses.md) on a shared fact summary.

| Structural | Operational / diplomatic | Institutional |
|---|---|---|
| _TBD_ | _TBD_ | _TBD_ |

**Product / strategy thread:** _TBD (no three-lens requirement Ã¢â‚¬” use work-dev + INTENT as needed)._

## 5. Operator synthesis

**Work-politics:** _paragraph_

**Work-strategy:** _paragraph_

## 6. Next actions (work-politics snapshot)

- Prepare for **Voter registration deadline** (in-person and mail; mail = postmark) on **Apr 20, 2026**.
- Refresh Gallrein, Trump/MAGA, and spending lines before relying on the brief heavily.
- Confirm this is a doc-only week or stage one work-politics milestone so audit continuity stays current.
- Refresh items marked `needs_refresh` in `brief-source-registry.md` before generating the next brief.

---

_Generated by `scripts/generate_work_politics_daily_brief.py` (legacy alias: `generate_wap_daily_brief.py`); config `docs/skill-work/work-strategy/daily-brief-config.json`._

