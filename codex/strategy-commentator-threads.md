# Strategy cognition streams / routing handles (index)
<!   word_count: 5754   >

**Purpose:** Stable **routing handles** for recurring cognition stream ingests so `batch analysis` lines can name **divergence and correlation** without re deriving the roster each session. The public scaffold is **polyphonic cognition streams** (see [COGNITION STREAMS.md](COGNITION STREAMS.md)); the same **`thread:<expert_id>`** on **different dates** remains the low level **join key** for **accuracy** checks and **opinion drift**. **WORK only**   not Record.

**Quick roster:** if you only need the eight stream list and handles, start with [COGNITION STREAMS POINTER.md](COGNITION STREAMS POINTER.md).

**Recurring speakers:** if you need the alphabetical lookup for recurring named people, start with [speaker lattice.md](speaker lattice.md).

**Choreography (vs tri mind):** Threads track **each commentator over time** (accuracy, narrative, compareâ€“contrast). **Tri mind** is a separate **analysis** pattern â€” usually **outboard** from `days.md`; see [STRATEGY NOTEBOOK ARCHITECTURE.md](STRATEGY NOTEBOOK ARCHITECTURE.md) Â§ **Expert choreography**.

**Terminology   cognition stream vs `expert_id`:** A **cognition stream** is the analytical lane / interpretive voice. The **`expert_id`** column below is the stable routing slug used by scripts and inbox tails. **Inbox `verify:`** tails use **`thread:<expert_id>`**; the token after **`thread:`** is the **`expert_id`**. **Legacy synonym:** **`thread_id`** (same column / value). **Legacy prose:** Older notes may say "analyst_id," "analyst threads," or "author threads"; read those as routing handle language, not the public scaffold.

**Lane discipline (no hybrid slugs):** Each **`expert_id`** identifies **exactly one** **named commentator** (one **Name** in the roster). **Topic** framing (Islamabad process, Hormuz domestic politics, escalation trap, etc.) lives in the **Role** column, **cold** text, and **grep tags** â€” **not** in the slug. **Verbatim quotes** and **attributed analysis** belong on a line whose **`thread:`** matches **that speakerâ€™s** row; putting another expertâ€™s words under the wrong **`thread:`** is a **routing error**. **`batch analysis`** is where **topic** tension (same crisis, different mechanisms) meets **expert** tension (same week, different predictions or registers).

**Metaphor   Symphony of Civilization:** Cognition streams are **parts** in a **polyphonic** score; each daily **`## YYYY MM DD`** block in the active month's `chapters/YYYY MM/days.md` is a **movement**; **`batch analysis`** states **harmony vs tension** between parts. Full gloss: [STRATEGY NOTEBOOK ARCHITECTURE.md](STRATEGY NOTEBOOK ARCHITECTURE.md) section **Symphony of Civilization**.

**Public cognition stream lattice:** The notebook's visible stream model is a count neutral lattice of equal interpretive voices. The current streams are `Nima`  > `Synthesis`, `Diesen`  > `Order`, `Davis`  > `Conflict`, `Mercouris`  > `Statecraft`, `Crooke`  > `Process`, `Parsi`  > `Scope`, `Pape`  > `Escalation`, and `Ritter`  > `Mechanics`. Use these labels in notebook prose and `batch analysis` framing when the stream model should be explicit; keep `thread:<expert_id>` routing unchanged for scripts and provenance.

**Lane to corpus boundary:** These eight cognition streams are internal notebook lanes, not external corpora by default. Shared intake remains the norm; promote a lane to a dedicated external corpus only under the strict rule in [LANE TO CORPUS PROMOTION POLICY.md](LANE TO CORPUS PROMOTION POLICY.md).

**Topic tags vs cognition streams vs thread handles (mental model):** Three layers   not mutually exclusive.

  **Topic tags** â€” *what* the material is about: recurring **substantive** lanes (Islamabad arc, Hormuz, Lebanon vs nuclear, U.S. domestic liability, Rome / legitimacy, â€¦). These show up as **grep tags** (`IRAN`, `JDVance`, `ROME`, `narrative escalation`, â€¦) or linked docs ([rome persia legitimacy signal check.md](rome persia legitimacy signal check.md), [trump religion papacy arc.md](trump religion papacy arc.md)).
  **Cognition streams**   *how* the material is interpreted: stable analytical voices such as `Pape` / `Escalation` or `Crooke` / `Process`.
  **Thread handles**   *who / provenance join*: one **`thread:<expert_id>`** per indexed voice or host handle. Reusing the same **`expert_id`** across weeks **diffs** that voice over time (drift / pivot).

**How to use:** When appending a paste ready line in [daily strategy inbox.md](daily strategy inbox.md), add **`thread:<expert_id>`** to the **`verify:`** tail **only** when the **cold** line attributes speech or analysis to the **Name** in that commentatorâ€™s row. Pair ingests in **`batch analysis | YYYY MM DD | â€¦`** using **Typical pairings**.

**Compatibility files (mixed location model):** Each indexed stream handle keeps a year independent channel profile plus time scoped companion files. The old `experts/<expert_id>/` wording is legacy compatible routing language, not the current canonical profile home:

  **`codex/profiles/<channel> profile.md`** â€” **cognitive profile** (operator authored, stable, year independent). Identity, convergence/tension fingerprints, signature mechanisms, failure modes, weave cues, introduction, and link hub.
  **`experts/<expert_id>/transcript.md`** â€” **7 day rolling verbatim** (appended automatically by triage from inbox `thread:` lines, operator editable for clarity, pruned after 7 days).
  **`experts/<expert_id>/thread.md`** â€” **distilled analytical thread** with **journal layer** (operator narrative by month chapter) and **machine layer** (script maintained extraction between HTML markers); **pages** (marker fenced blocks) live inside month chapters â€” see [STRATEGY NOTEBOOK ARCHITECTURE.md](STRATEGY NOTEBOOK ARCHITECTURE.md) Â§ *Thread (terminology)* and [watches/README.md](watches/README.md).
  **`experts/<expert_id>/mind.md`** *(optional)* â€” extended CIV MIND profile (currently: `barnes`, `mearsheimer`, `mercouris`).

Run operator **`thread`**: **`bin/thread`** or **`python3 scripts/strategy_thread.py`** (from repo root) â€” automatically triages inbox to transcripts, then extracts transcript + `strategy page` material for thread distillation. **Not Record**. Legacy path [`expert ingest corpus/README.md`](../README.md) redirects here. *Notebook contract (inbox â†’ weave â†’ `days.md`):* [STRATEGY NOTEBOOK ARCHITECTURE.md](STRATEGY NOTEBOOK ARCHITECTURE.md#expert choreography) Â§ **Expert choreography**. Operator **`thread`** vs **`weave`:** [STRATEGY NOTEBOOK ARCHITECTURE.md](STRATEGY NOTEBOOK ARCHITECTURE.md) Â§ *Thread (terminology)*.

**Published outlets (starter list):** Each **`codex/profiles/<channel> profile.md`** includes **`## Links`** with **`### Social media`**, **`### Substack`**, and **`### Other links`** â€” at least three useful source surfaces when available; re verify handles and media URLs before cite grade use.

**Wires and outlets (no author `thread:`):** A **wire**, **pool paragraph**, or **outlet summary** is **not** an indexed author unless the cold line names **that person** as the speaker or author. Use **`verify:wire RSS`** (and topic grep tags) **without** **`thread:<expert_id>`**; optional **`membrane:single`** when the line must **not** imply **`batch analysis`** membership for author threads.

**Official IRI / MFA voices (no `thread:`):** The **Iranian foreign minister** and **MFA** spokespeople are **state primaries**, not **`expert_id`** rows. Capture with **`verify:IRI primary`** (and **`fa`** triangulation when load bearing) plus **`IRAN`** / **`IRI`** / **`TEHRAN`** grep tags â€” **no** **`thread:`** on the FM line itself. **Continuity** to indexed threads is via **`batch analysis`** and **`daily brief` Â§1h** â€” e.g. **2026 04 17** **Araghchi** (Hormuz + **Lebanon** opener) **crosses** **`parsi`** (Lebanon vs nuclear scope), **`marandi`** (elite register), **`davis`** (U.S. side packaging of the **X** post), **`mercouris`** (institutional **Lebanon**/**Hormuz** surface) â€” see [daily brief 2026 04 17.md](../daily brief 2026 04 17.md) **Â§1h** + [daily strategy inbox.md](daily strategy inbox.md).

**Ephemeral / one shot ingests (no persistent author thread):** Not every line needs a **`thread:<expert_id>`**. The index exists so the **same** voice can be **joined across dates** (drift, accuracy). If the capture is **tactical** â€” one article, a stray clip, a **verify** pass, or material you **do not** want to treat as a standing **expert** lane â€” **omit** **`thread:`**. Use **cold** + **URL** + **`verify:`** and **topic** grep tags (`IRAN`, `ROME`, â€¦) as usual. Optional **`verify:â€¦ | membrane:single`** signals that this line is **not** inviting a same day **`batch analysis`** membership claim for indexed threads (see **Crossing filters**). You are **not** required to mint a table row for every name that appears once.

**Maintenance:** Add rows when a new **Name** appears **repeatedly** in `days.md` or inbox; **deprecate** with a line in **Notes** â€” do not delete history without operator say so.

**Month arc pointer (chapter meta):** Cross day **movement** and weave boundaries for the active month (example **2026 04 08â€“15**: Hormuz week, expert density, **04 15** Grok vs brief overlay) live in [chapters/2026 04/meta.md](chapters/2026 04/meta.md#april arc one screen) (**April arc â€” one screen**). Use that block for **grep / calendar** orientation; it **does not** mint **`expert_id`** rowsâ€”this file remains the roster SSOT.

**Mearsheimer vs Diesen (individual commentators):** **`mearsheimer`** = **John Mearsheimer** only; **`diesen`** = **Glenn Diesen** only â€” **no** shared **`expert_id`** for a â€œsession pair.â€ Same episode with **both** speakers â†’ **two** paste ready lines (each **`thread:<expert_id>`**) + optional **`batch analysis`**.

## Notebook use tags (reverse index)

**Purpose:** Cross cutting **usage** tags â€” answers â€œhow might the notebook use this voice?â€ (open a frame, read talks, check plausibility, etc.). **Source of truth:** the **`Notebook use tags`** field in each [channel profile](mercouris/mercouris profile.md) (Identity table row or equivalent profile section). This subsection is a **convenience mirror** for shortlists.

**Guardrail:** Tags are **notebook use families**, not ideological classes, not maintenance tiers, and **not** substitutes for **`expert_id`**, **Role**, **Default grep tags**, or **Typical pairings**. An expert may appear under **multiple** tags.

**Fixed vocabulary:** `orient`, `negotiate`, `validate`, `authorize`, `stress test`, `narrate`, `historicize`.

### `orient`

  `mercouris`
  `macgregor`
  `diesen`
  `sachs`
  `jiang`
  `mearsheimer`
  `weichert`

### `negotiate`

  `mercouris`
  `crooke`
  `freeman`
  `sachs`
  `marandi`
  `parsi`

### `validate`

  `davis`
  `macgregor`
  `baud`
  `bigserge`
  `johnson`
  `pape`
  `ritter`
  `weichert`

### `authorize`

  `davis`
  `baud`
  `barnes`
  `pape`
  `ritter`

### `stress test`

  `berletic`
  `diesen`
  `sachs`
  `armstrong`
  `greenwald`
  `ritter`
  `jermy`

### `narrate`

  `mate`
  `crooke`
  `mercouris`
  `blumenthal`
  `greenwald`
  `marandi`
  `parsi`
  `simplicius`
  `nima`
  `bigserge`

### `historicize`

  `crooke`
  `mercouris`
  `diesen`
  `sachs`
  `jiang`
  `mearsheimer`
  `armstrong`
  `weichert`

### Civ China â€” strategy (primary commentator)

**Purpose:** Single **default** **`thread:`** for **Peopleâ€™s Republic** / **U.S.â€“China** **relations** **as** **civilizationalâ€“strategic** **speech** in the **strategy codex** (order talk, **dÃ©tente** memory, **strait** **mirrors**, **BRI** **spillovers** **when** **Freeman** **is** **the** **speaker**). **Not** a substitute for **`jiang`** **Predictive** **History** **corpus** **or** **wire** **primaries** â€” **weave** **with** **explicit** **tier** **tags**.

  `freeman`

   

| expert_id | Name | Role (one line) | Default grep tag | Typical `batch analysis` pairings |
|           |        |                 |                  |                                   |
| `marandi` | Seyed Mohammad Marandi | Iranian English long form: negotiation **process**, red lines, legitimacy register. Guest speaker arc inside Nima stream: [nima marandi speaker arc.md](2026/nima/nima marandi speaker arc.md) | `IRAN`, `TEHRAN`, or `Marandi` in cold | Ã— `ritter`, Ã— `parsi`, Ã— `rome ecumenical` (Pontifex / Marandi Easter) |
| `ritter` | Scott Ritter | U.S. **military dissent**: Hormuz **sea control**, blockade ops, Vance frame; **faith politics** register when **Ritter** is the speaking expert. Guest speaker arc inside Diesen stream: [diesen ritter speaker arc.md](2026/diesen/diesen ritter speaker arc.md). **AI adjunct (statecraft):** CHMR removal, Claude target deck, LOAC/war-crime mechanics (Minab, Lugansk) — [ritter-on-ai](../statecraft/notes/ritter-on-ai.md) · [china-ai watch](../statecraft/notes/china-ai-implementation-watch.md) · [four-voice compare](../statecraft/notes/minab-palantir-four-voice-compare.md) | `JDVance`, `IRAN`, `Ritter`, or `AI` in cold | Ã— `marandi`, Ã— `barnes`, Ã— `weichert`, Ã— `sachs` (Minab/LOAC seam), Ã— `rome invective` (split from ecumenical) |
| `parsi` | Trita Parsi (`@tparsi`) | Beltway facing **Lebanon vs nuclear** scope; â€œmaskâ€ thesis | `IRAN` + Parsi in cold | Ã— `holy see moral` (Pontifex Lebanon), Ã— `marandi`, Ã— `macgregor` |
| `barnes` | Robert Barnes (`@barnes_law`) | **Domestic liability** pole on Hormuz / executive TS chain. Speaker arc inside Davis stream: [davis barnes speaker arc.md](2026/davis/davis barnes speaker arc.md). **AI adjunct (statecraft):** bubble/circular-finance capex, LLM skepticism, energy–Gulf–campaign incentive structure — [barnes-on-ai](../statecraft/notes/barnes-on-ai.md) · [china-ai watch](../statecraft/notes/china-ai-implementation-watch.md) | `JDVance`, `barnes`, or `AI` in cold | Ã— `pape`, Ã— `jiang` (bubble vs liability seam), Ã— `weichert` (architecture vs domestic chain); **topic** forks (JTN style â€œcardâ€ vs satirical spiral) in **`batch analysis`** without a second expert |
| `macgregor` | Douglas Macgregor (`@DougAMacgregor`) | Importers / **Asiaâ€“Europe** distance from U.S.â€“Israel kinetic frame. Guest speaker arc inside Diesen stream: [diesen macgregor speaker arc.md](2026/diesen/diesen macgregor speaker arc.md) | `IRAN` or Macgregor in cold | Ã— `pape`, Ã— `mearsheimer`, Ã— `parsi` |
| `pape` | Robert Pape (`@ProfessorPape`) | **Escalation Trap** / commitment ratchet on demands. **AI adjunct (statecraft):** China field-tour **industrial AI/robotics** implementation (“getting late early”) — [pape-on-china-ai](../statecraft/notes/pape-on-china-ai.md) · [china-ai watch](../statecraft/notes/china-ai-implementation-watch.md) | `ProfessorPape`, `Pape`, `China`, or `AI` in cold | Ã— `davis`, Ã— `barnes`, Ã— `mearsheimer`, Ã— `jiang` (bubble vs implementation seam) |
| `davis` | Daniel Davis (Lt Col; `@DanielLDavis1`) | Ceasefire as **extension game**; ultimatum vs negotiation; macro pain to U.S. | `IRAN`, `JDVance`, or Davis in cold | Ã— `mearsheimer`, Ã— `pape`, Ã— `marandi`, Ã— `jermy` |
| `jermy` | Steve Jermy (Commodore, RN ret.) | **Energyâ€“GDP / maritime system**: Hormuz closure **recovery lags** (Ever Givenâ€“style **knock on**), **diesel** â†’ supply chain / semis / fertilizer; **rough order** macro slides vs **currency first** economics; **close vs distant** blockade **risk geometry** | `Jermy`, `IRAN`, or `Hormuz` in cold | Ã— `davis`, Ã— `ritter`, Ã— `mearsheimer` (in show cite) |
| `mearsheimer` | John Mearsheimer | **Offensive realism**: security dilemma, Israel structural, great power geometry. Guest speaker arc inside Diesen stream: [diesen mearsheimer speaker arc.md](2026/diesen/diesen mearsheimer speaker arc.md) | `MEARSHEIMER` or `Mearsheimer` in cold | Ã— `davis`, Ã— `mercouris`, Ã— `diesen`, Ã— `sachs` |
| `mercouris` | Alexander Mercouris | **Institutional / narrative** diplomatic read (Hormuz, Lebanon, Islamabad) | `Mercouris` or mind cite in cold | Ã— `mearsheimer`, Ã— `diesen`, Ã— `sachs`, Ã— `marandi`, Ã— Tri Frame [minds/](../README.md) |
| `blumenthal` | Max Blumenthal (`@MaxBlumenthal`) | **Grayzone** / **antiwar** pole: **U.S. Middle East** policy and **elite access** critique; **Lebanon**/**Gulf** narrative framing; **media layer** â€œwho engineered whatâ€ â€” **access** and **backchannel** claims stay **hypothesis grade** until **primary tape** or **on record** source | `Blumenthal`, `Grayzone`, or `Lebanon` in cold | Ã— `mate`, Ã— `parsi`, Ã— `mercouris`, Ã— `marandi`, Ã— `freeman` |
| `mate` | Aaron MatÃ© (`@aaronjmate`) | **Grayzone** / **investigative** lane: **media ownership**, **corporate skin**, and **propaganda** framing; **Israel/Palestine** vocabulary (**colonization** thesis); **CBS** / **billionaire** / outlet **lineage** claims â€” **tier verify** (filings, corporate docs) before **Links grade** | `Mate`, `MatÃ©`, `Grayzone`, or `aaronjmate` in cold | Ã— `blumenthal`, Ã— `parsi`, Ã— `mercouris`, Ã— `marandi` |
| `johnson` | Larry Johnson | Ex CIA / **material** and **ORBAT** emphasis: force structure, **Hormuz** geometry, **F 15/Isfahan** raid narrative reconstructions (Haiphongâ€“Ritter roundtables) | `Johnson` or `LarryJohnson` in cold | Ã— `ritter`, Ã— `davis`; see [transcript digest](../transcript analysis haiphong ritter johnson iran 2026 04.md) |
| `freeman` | Charles (â€œChasâ€) Freeman | **Primary civ china (strategy) expert**: **U.Sâ€“China** **diplomatic** **memory** **&** **PRC** **order** **talk**; **inconclusive** talks + **alliance/material** framing; **seam** from **`jiang`** **PH** **by** **default**. Speaker arcs: [Diesen](2026/diesen/diesen freeman arc.md) / [Dialogue Works](2026/nima/nima freeman arc.md) | `Freeman` or `ChasFreeman` in cold | Ã— `parsi`, Ã— `mercouris`, Ã— [rome persia legitimacy signal check.md](rome persia legitimacy signal check.md) (**seam**, not merge); Ã— `diesen`, Ã— `jiang`, Ã— `sachs` |
| `greenwald` | Glenn Greenwald ([`@ggreenwald`](https://x.com/ggreenwald)) | **Substack** / video long form â€” **U.S. executive** claims, **Middle East** war **politics**, **media** and **Truth Social** narrative seams; **civil libertarian** **antiwar** register; **not** a wire primary â€” pair **`mate`**, **`blumenthal`**, **`parsi`**, **`davis`**, **`mercouris`**, **`barnes`** with **tier seams** | `Greenwald`, `greenwald`, or `ggreenwald` in cold | Ã— `mate`, Ã— `blumenthal`, Ã— `parsi`, Ã— `davis`, Ã— `mercouris`, Ã— `barnes` |
| `crooke` | Alastair Crooke | Former diplomat / **Levantâ€“Islamabad** â€œroomâ€ and **spoiler** reads; often beside **Davis** in digests. Speaker arc inside Davis stream: [davis crooke speaker arc.md](2026/davis/davis crooke speaker arc.md) | `Crooke` in cold | Ã— `davis`, Ã— `marandi`, Ã— `parsi` |
| `matlock` | Jack Matlock | U.S. **diplomatic memory / Cold War settlement** lane: Reagan/Bush era negotiation memory, anti NATO expansion warning lineage, and the later failure of the post Cold War European security architecture. Guest speaker arc inside Diesen stream: [diesen matlock speaker arc.md](2026/diesen/diesen matlock speaker arc.md) | `Matlock`, `Cold War`, `NATO`, or `Ukraine` in cold | Ã— `diesen`, Ã— `mearsheimer`, Ã— `sachs`, Ã— `crooke` |
| `diesen` | Glenn Diesen | **Eurasia / multipolar** discourse; **non Western** institutional / rationality frames when distinct from **Mearsheimer**â€™s structural realist register | `Diesen` in cold | Ã— `mearsheimer`, Ã— `macgregor`, Ã— `pape`, Ã— `sachs` |
| `karaganov` | Sergey Karaganov | Russian elite **strategic / civilizational state** voice: **deterrence doctrine**, **Greater Eurasia**, **Siberization**, and **post West** identity framing. Guest speaker arc inside Diesen stream: [diesen karaganov speaker arc.md](2026/diesen/diesen karaganov speaker arc.md) | `Karaganov`, `RU NUC`, or `Eurasia` in cold | Ã— `diesen`, Ã— `mercouris`, Ã— `mearsheimer` |
| `sachs` | Jeffrey Sachs | **UN / development–macro + DC institutions** pole: **deinstitutionalization** thesis (group process vs personalized executive); **relative decline** and **multipolar** misrecognition; **Congress** war and peace **vacuum**; cites **NYT** “room” narratives — **hypothesis grade** capacity/health claims stay **tier C** unless clinical primary. **AI adjunct (statecraft):** first AI wars, Minab/Palantir moral read, IDF cloud stack, China productive AI — [sachs-on-ai](../statecraft/notes/sachs-on-ai.md) · [china-ai watch](../statecraft/notes/china-ai-implementation-watch.md) · [four-voice compare](../statecraft/notes/minab-palantir-four-voice-compare.md) | `Sachs`, `IRAN`, `Hormuz`, or `AI` in cold | Ã— `diesen`, Ã— `mearsheimer`, Ã— `mercouris`, Ã— `ritter`, Ã— `weichert` (Minab/MIC seam) |
| `jiang` | Jiang Xueqin (Predictive History) | **Long horizon civilizational / game theory** lectures; PH is the sole upstream for notebook facing Jiang ingest. Guest speaker arc inside Diesen stream: [diesen jiang speaker arc.md](2026/diesen/diesen jiang speaker arc.md). **AI adjunct (statecraft):** bubble/bailout, Stargate/surveillance religion, US–CN partner lab — [jiang-on-ai](../statecraft/notes/jiang-on-ai.md) · [china-ai watch](../statecraft/notes/china-ai-implementation-watch.md); implementation seam → [pape-on-china-ai](../statecraft/notes/pape-on-china-ai.md) | `Jiang`, `PH`, `predictive history`, or `AI` in cold | Ã— `mearsheimer`, Ã— `diesen`, Ã— `sachs`, Ã— `pape` (implementation vs bubble seam) |
| `armstrong` | Martin A. Armstrong (`@ArmstrongEcon`) | **Cycle / timing** models (Socrates style), **sovereign debt** stress, **energyâ€“food system** shocks (diesel, fertilizer) framed with **geopolitical war**; critiques **â€œperpetual wealthâ€ vs â€œdollar crashâ€** as headline distractions | `Armstrong`, `debt`, `IRAN`, or `Hormuz` in cold | Ã— `jermy`, Ã— `diesen`, Ã— `sachs`, Ã— `pape` |
| `baud` | Jacques Baud | **NATO / UN / intelligence adjacent** framing: **law of war**, **HUMINT vs OSINT** limits, **European security** and **cross theater** reads; **convergence vs tension** between **official narrative** and **evidential** claims â€” **complements** **ORBAT** lanes without duplicating them. Pair arc inside Nima stream: [nima baud arc.md](2026/nima/nima baud arc.md) | `Baud`, `NATO`, `UN`, or `EU` in cold | Ã— `ritter`, Ã— `macgregor`, Ã— `davis`, Ã— `barnes` |
| `berletic` | Brian Berletic (`@BrianJBerletic`, The New Atlas) | **Industrial capacity**, **sanctions**, **proxy war** logistics, **force generation** vs **headline** battlefield narratives; **long run production** and **material** constraints as a distinct fingerprint | `Berletic`, `NewAtlas`, `sanctions`, or `IRAN` in cold | Ã— `ritter`, Ã— `jermy`, Ã— `diesen`, Ã— `davis`, Ã— `mearsheimer` |
| `bigserge` | Big Serge ([`@witte_sergei`](https://x.com/witte_sergei); *Big Serge Thought*) | **Substack** long form **strategy / war studies** â€” **campaign** and **theater level** synthesis, **OSINT  and media thread** reads; **not** a wire or ORBAT primary â€” pair **`berletic`**, **`ritter`**, **`johnson`**, **`baud`**, **`mercouris`** with **tier seams** | `Big Serge`, `bigserge`, `witte_sergei`, or `Big Serge Thought` in cold | Ã— `berletic`, Ã— `ritter`, Ã— `johnson`, Ã— `baud`, Ã— `mercouris` |
| `weichert` | Brandon J. Weichert ([`@WeTheBrandon`](https://x.com/WeTheBrandon); *The Weichert Brief*) | US **Iran-war strategic read**: Netanyahuâ€“Trump **junior-partner** thesis, Iranian **escalation dominance**, reciprocal **energy-infra** coercion, **WWI/Sarajevo** analogy lane, **NDAA/industrial-base** attrition read â€” recurring **Mario Nawfal** guest + Substack/X; **not** wire/ORBAT primary. **AI adjunct (statecraft):** surveillance architecture, kill chain (Minab), Palantir Israel testbed, China applied robotics â€” [weichert-on-ai](../statecraft/notes/weichert-on-ai.md) Â· [china-ai watch](../statecraft/notes/china-ai-implementation-watch.md) Â· [profile](profiles/weichert-profile.md) (no `civ-lens/weichert/` shelf) | `Weichert`, `WeTheBrandon`, `IRAN`, or `AI` in cold | Ã— `pape`, Ã— `nawfal`, Ã— `davis`, Ã— `marandi`, Ã— `barnes`, Ã— `ritter` (Minab/LOAC seam) |
| `simplicius` | Simplicius (pseudonym; *Garden of Knowledge* / [`@simpatico771`](https://x.com/simpatico771)) | **Substack** long form **conflict analysis** â€” U.S.â€“Iran **ceasefire/blockade** narratives, **media/wire** synthesis, polemical register; **not** a wire primary â€” pair **`mercouris`**, **`parsi`**, **`davis`**, **`marandi`** with **tier seams** | `Simplicius`, `simplicius76`, or `simpatico771` in cold | Ã— `mercouris`, Ã— `parsi`, Ã— `davis`, Ã— `marandi`, Ã— `blumenthal` |
| `nima` | Nima Alkorshid (*Dialogue Works*) | **Host / interviewer** lane â€” long form **geopolitical dialogue**; symmetric **`thread:`** routing with **`thread:<guest>`** on **same episode** ingests so **`raw input`** mirroring lands **host** and **guest** rows (**host prompts / framing** on **`nima`**, guest analysis on the guest **`expert_id`**) | `Nima`, `Dialogue Works`, or `DialogueWorks` in cold | Ã— `marandi`, Ã— `diesen`, Ã— `mercouris`, Ã— `davis` |

**Special routing rule â€” Predictive History:** PH derived notebook facing ingest must use `thread:jiang`. Do not route PH directly into other author lanes or directly into ad hoc page stubs. See [strategy notebook/README.md](README.md) Â§ **Predictive History routing rule**.

### AI bench cluster (statecraft adjunct)

**Purpose:** Cross-speaker **AI / China implementation / Minab** synthesis lives in **statecraft notes**, not notebook SSOT. Inbox **`thread:<expert_id>`** routing is unchanged; for **bench depth** open the hub and the speaker note in the row.

| Voice | Open when | Note |
|-------|-----------|------|
| `ritter` | CHMR removal, targeteer profession, Claude deck, LOAC / war-crime mechanics | [ritter-on-ai](../statecraft/notes/ritter-on-ai.md) |
| `weichert` | Surveillance architecture, automated kill chain, Palantir testbed, applied robotics | [weichert-on-ai](../statecraft/notes/weichert-on-ai.md) · [profile](profiles/weichert-profile.md) |
| `sachs` | First AI wars, MIC moral read, IDF cloud stack, China productive AI | [sachs-on-ai](../statecraft/notes/sachs-on-ai.md) |
| `jiang` | Bubble/bailout, Stargate/surveillance religion, US–CN partner lab (not field-tour scaling) | [jiang-on-ai](../statecraft/notes/jiang-on-ai.md) |
| `pape` | China industrial AI/robotics field observation (“getting late early”) | [pape-on-china-ai](../statecraft/notes/pape-on-china-ai.md) |
| `barnes` | AI bubble/circular finance, energy–Gulf–campaign network, domestic liability (not kill-chain forensics) | [barnes-on-ai](../statecraft/notes/barnes-on-ai.md) |

**Hub:** [china-ai-implementation-watch](../statecraft/notes/china-ai-implementation-watch.md) · **Minab compare:** [minab-palantir-four-voice-compare](../statecraft/notes/minab-palantir-four-voice-compare.md) · **Verify:** watch § [verify receipts](../statecraft/notes/china-ai-implementation-watch.md#verify-receipts-2026-06-10) — **Maven (Palantir) + Claude** stack; do not collapse to Palantir-only without receipt.

### Distinctive lane shorthands (recommended sentences)

  **`pape`:** This lane **names escalation as a trap** â€” a **commitment ratchet** on **demands** plus **staged** branches (e.g. **nuclear stockpile** logic â†’ **ground force** scenarios, **Stage** framing, packaged graphics) â€” **not** a substitute for **`ritter`** **Hormuz** **mechanics**, **`mercouris`** **room** **reads**, or **`mearsheimer`** **alliance** **geometry** alone; use **Typical pairings** and, when folded, **`### Reflection`** bullets such as **Thesis A â€” Pape / â€œescalation trapâ€** in the active monthâ€™s [`chapters/YYYY MM/days.md`](chapters/2026/2026-04/days.md) (replace **YYYY MM**). **AI adjunct** (China implementation) lives in **statecraft notes** — [pape-on-china-ai](../statecraft/notes/pape-on-china-ai.md) and [china-ai-implementation-watch](../statecraft/notes/china-ai-implementation-watch.md); **not** a substitute for **`jiang`** bubble/surveillance metaphysics or **`ritter`** kill-chain forensics.

  **`ritter` (AI adjunct):** **Ex-targeteer** read — CHMR removal, stale OOB + dimension matching, Claude/Palantir deck as **start not finish**, Minab/Lugansk as **war-crime mechanics** — open [ritter-on-ai](../statecraft/notes/ritter-on-ai.md) and [minab-palantir-four-voice-compare](../statecraft/notes/minab-palantir-four-voice-compare.md); pair **`weichert`** (architecture), **`sachs`** (MIC moral), **`jiang`** (bubble end-state) with **labeled seams**; wire triage → **Maven (Palantir) + Claude**, not Palantir-only.

  **`sachs` (AI adjunct):** **First AI wars** + **video-game** moral pole + **IDF hyperscaler/Palantir** stack + **China productive AI** — open [sachs-on-ai](../statecraft/notes/sachs-on-ai.md); Minab **Palantir-alone** attribution is **assertion tier** vs wire **Maven + Claude**; **not** LOAC forensic (**`ritter`**) or surveillance architecture (**`weichert`**) without seams.

  **`jiang` (AI adjunct):** **Game Theory / Founding Members** register — oversold ML, bailout/Stargate, surveillance religion, US–CN **partner** lab; open [jiang-on-ai](../statecraft/notes/jiang-on-ai.md). **China industrial deployment** → **`pape`** [pape-on-china-ai](../statecraft/notes/pape-on-china-ai.md); **Minab forensics** → **`ritter`** / **`weichert`** / **`sachs`** via [four-voice compare](../statecraft/notes/minab-palantir-four-voice-compare.md).

  **`barnes` (AI adjunct):** **Forensic political-economy** read — GDP-without-AI bubble, circular capex, hallucination skepticism, Gulf energy + campaign-finance incentive chain — open [barnes-on-ai](../statecraft/notes/barnes-on-ai.md); **not** LOAC/targeteer (**`ritter`**) or surveillance panopticon (**`weichert`**); **`jiang`** owns repetition-heavy bubble/religion register — keep **labeled seams** on AI-week **`batch analysis`**.

  **Domestic plane (do not collapse):** **`barnes`** tracks **liability**, **coalition sell**, and the **executive / TS** **chain**. **Pape** may add **U.S. audience** **or** **polling** **theses** (e.g. political support **hardening** under casualties) â€” keep those **hypothesis grade** until **ingested** with **`verify:`** (dated poll, screenshot, or primary); **do not** **merge** with Barnes **without** a **labeled seam**.

  **`armstrong`:** **Cycle / timing** and **debtâ€“warâ€“commodity** convergence theses â€” **not** a substitute for **`jermy`** **diesel / fertilizer / logistics** mechanics or **`sachs`** **institutional** reads without **tiered** verify; treat **â€œcomputer was right on timingâ€** claims as **hypothesis grade** until **disclosed methodology** or **out of sample** documentation exists.

  **`baud`:** **Law + intel + NATO/Europe** spine for **why narratives cohere or crack** â€” **not** a substitute for **`ritter`** **sea control** **mechanics** or **`barnes`** **domestic liability** **chain**; use **`batch analysis`** when the same week needs **evidential tension** across **Pentagon/Western** claims vs **treaty / mandate** framing.

  **`berletic`:** **Production and sanctions** as **strategic variables** â€” **not** a second **`ritter`** **ORBAT** voice; pairs when **headline** **kinetic** **wins** need a **factory / stockpile / resupply** **counter narrative** (**`jermy`** for **closure economics**, **`diesen`** for **multipolar** **institutions**).

  **`simplicius`:** **Substack length** **synthesis** and **narrative combat** â€” **not** a substitute for **`mercouris`** **institutional** **room** reads, **`parsi`** **Beltway** **scope** claims, or **`marandi`** **IRI adjacent** **English** register; **batch analysis** when the same week needs **â€œsecond read of wiresâ€** tension with explicit **tier** tags (**opinion** / **secondary**).

  **`bigserge`:** **Campaign  and theater level** **Substack** essays â€” **not** a second **`ritter`**/**`johnson`** **ORBAT** voice or **`berletic`** **production** ledger; **batch analysis** when the week needs **operations narrative** beside **material** lanes, with **hypothesis grade** labels on forward looking **battle** claims.

  **`weichert`:** **Iran-war strategic read** (junior-partner, escalation dominance, NDAA/industrial attrition, Gulf veto) â€” **not** wire/ORBAT primary. **AI adjunct** lives in **statecraft notes**, not notebook SSOT: Utah/data-center surveillance cover, automated kill chain, Palantir panopticon, China applied vs US software hype â€” open [weichert-on-ai](../statecraft/notes/weichert-on-ai.md) and [china-ai-implementation-watch](../statecraft/notes/china-ai-implementation-watch.md); codex entry [weichert-profile](profiles/weichert-profile.md). **No** `civ-lens/weichert/` shelf. On Minab/Palantir days pair **`ritter`** (CHMR/LOAC/targeteer), **`sachs`** (MIC moral), **`jiang`** (bubble/surveillance religion) with **labeled seams**; wire triage favors **Maven (Palantir) + Claude** stack â€” **do not** collapse to Palantir-only attribution without verify receipt.

  **`greenwald`:** **Legalâ€“media** and **antiwar** **Substack** (plus video) â€” **executive**â€“**press** tension and **deadline / ceasefire** storylines â€” **not** a substitute for **`parsi`** **Beltway** scope reads, **`marandi`** **negotiation** register, or **`davis`** **extension game** mechanics without **labeled** seams; **batch analysis** when the week needs **â€œclaims vs confirmationâ€** hygiene beside **`mate`**/**`blumenthal`**.

### Quantitative thread metrics (illustrative â€” civ memâ€“style calibration)

**Purpose:** Optional **0â€“1** scores to classify threads using habits parallel to civ mem: **relevance spine stability** (does the voice stay on its lane?), **STATE style closure** (resolved/deferred vs open claims), and **lattice edge weight** (hub role in `batch analysis`). **Numbers below are placeholders** â€” replace with measured rates from inbox / `days.md` / resolution logs when you operationalize.

| Abbrev | Name | Idea |
|        |      |      |
| **SCI** | Surface coherence index | Share of ingests where the dominant **plane** matches the rowâ€™s **Role**; penalize register smearing without a seam. |
| **AD** | Adjudication depth | \((\texttt{resolved} + \texttt{deferred})\) **Ã·** falsifiable claims logged (trailing window). |
| **CTC** | Cross thread coupling | Distinct **other** `expert_id`s in **`batch analysis`** with this commentator, normalized by activity (bridge centrality). |

| expert_id | SCI | AD | CTC | Plain language note (Predictive History reader) |
|           |     |    |     |                                                  |
| `marandi` | 0.78 | 0.42 | 0.71 | He usually sounds like one kind of speaker: negotiation, red lines, and how the Islamic Republic wants to be heard. Many of his strongest claims only settle when the diplomatic music stops, so â€œwho was right?â€ often stays open. In the notebook he keeps showing up next to other Iran facing voices, which is why the â€œbridgeâ€ score runs high. |
| `ritter` | 0.82 | 0.48 | 0.74 | His lane is recognizableâ€”sea control, blockade mechanics, the military story under the headlinesâ€”so he does not drift into generic punditry as often. Operational claims need time and evidence to judge, so verdicts arrive slowly. He is often placed beside diplomats or lawyers of war in the same weekâ€™s analysis, which raises the â€œcompares with othersâ€ score. |
| `parsi` | 0.74 | 0.45 | 0.69 | Washingtonâ€™s story can pull him between Lebanon, nuclear scope, and what â€œthe processâ€ means, so the thread can feel like it crosses slightly different questions in one breath. What closes in the Beltway and what closes on the ground do not always move together. He still pairs often with other named voices, but he is not the hub everyone orbits. |
| `barnes` | 0.88 | 0.36 | 0.52 | He stays on home law and politicsâ€”who is exposed, what the chain of command impliesâ€”which keeps his voice distinct from foreign policy generalists. Poll driven or coalition claims often stay â€œmaybeâ€ until hard numbers land, so clear yes/no resolution is rarer. He is essential when the story is liability; he is less often the center of multi country roundtables. |
| `macgregor` | 0.76 | 0.40 | 0.68 | Third country distance from the U.S.â€“Israel frame is a steady theme, easy to recognize week to week. Event linked scorekeeping is uneven because his value is often framing, not a dated bet. He still shows up in side by side comparisons with other realists. |
| `pape` | 0.81 | 0.55 | 0.77 | Escalation as trap is a named mechanismâ€”demands, ratchets, staged branchesâ€”so the reader can see what would count as a test. When those pieces are written down clearly, time can actually grade the claim. That same clarity makes him a natural partner in â€œfork A vs fork Bâ€ discussions. |
| `davis` | 0.79 | 0.50 | 0.72 | Ceasefire as extension game, ultimatums, who hurts firstâ€”the architecture is easy to follow. Some forecasts need the calendar to catch up before you know. He is regularly read against other named analysts in the same crisis week. |
| `jermy` | 0.74 | 0.44 | 0.58 | Energyâ€“logistics modeling is a recognizable laneâ€”diesel, closure recovery, systemic second order effects. Macro numbers stay **rough order** until primaries pin. Often paired on **Deep Dive** with Davis rather than as the widest crossover hub. |
| `mearsheimer` | 0.85 | 0.58 | 0.84 | Great power geometry is his home turf; the listener rarely wonders which discipline they are in. If then structure helps the record show what would falsify a line of argument. In comparative work he is the voice others are measured against, so he sits at the center of many paired readings. |
| `mercouris` | 0.72 | 0.44 | 0.88 | The diplomatic â€œroomâ€ story can shade into narrative that is harder to pin to a single falsifying fact, so discipline scores a little lower. The payoff is synthesis: he is the commentator most often placed beside others to hear harmony or dissonance, which drives the bridge score to the top. |
| `blumenthal` | 0.74 | 0.33 | 0.62 | Elite network and media critique framing is recognizable week to week; closure on â€œwho whispered to whomâ€ claims often waits on tape or official denial. Pairs well with Beltway facing or diplomatic lanes when the notebook wants an alt media tension. |
| `mate` | 0.75 | 0.34 | 0.64 | Media structure and ownership critiques are a steady laneâ€”outlet naming and corporate parentage need primary documents to close. Often read beside the same Grayzone adjacent week as Blumenthal but keeps a distinct thread id for routing. |
| `johnson` | 0.80 | 0.46 | 0.63 | Order of battle and material detail keep him in a narrow laneâ€”useful when the question is what forces could actually do. Raid and battle narratives take time and sources to check. He shines on panels and roundtables more than as the universal hub for every thread. |
| `freeman` | 0.83 | 0.41 | 0.66 | Veteran diplomatâ€™s habitâ€”â€œtalks are inconclusive by natureâ€â€”matches a careful separation between moral language and hard security, which keeps the voice steady. Diplomatic time horizons mean many calls stay unresolved for a long while. Pairings happen, but he is not the busiest crossover node. |
| `greenwald` | 0.76 | 0.38 | 0.68 | Executive claims vs media narrative framing is a steady laneâ€”strong on juxtaposing official statements with what wires next confirm. Closure on â€œwhat was really agreedâ€ often waits on primaries. Frequently read beside other antiwar or Beltway facing lanes as interpretive tension, not as ORBAT. |
| `crooke` | 0.75 | 0.39 | 0.70 | Levant room and spoiler logic hang together as a worldview. Spoiler readings often stay open until events force a fork. He appears often enough next to other specialists that the bridge score stays solid. |
| `matlock` | 0.84 | 0.49 | 0.73 | Diplomatic memory and security architecture framing is unusually stableâ€”he returns to the negotiated end of the Cold War, NATO expansion, and the failure to build an inclusive European settlement. Many claims are historical and therefore highly checkable, but some later stage geopolitical warnings still resolve only with time. He pairs naturally with realist and institutional lanes because he is both a witness and an interpreter of the same long arc. |
| `diesen` | 0.77 | 0.43 | 0.79 | Multipolar language is clearly his ownâ€”not a copy of standard U.S. structural realismâ€”so you can tell when Diesen is speaking. Closure looks like his peer group: partly about time and evidence. He is frequently read alongside other realist commentators when the week demands comparison. |
| `sachs` | 0.73 | 0.38 | 0.71 | Institutional decay and macro development framing is recognizableâ€”UN/DC process contrasted to personalized executive behavior. Many strongest claims (war room origin stories, capacity) need primaries before they close. Often paired with **Diesen** on multipolar episodes rather than as the widest mechanics hub. |
| `jiang` | 0.70 | 0.35 | 0.65 | Long horizon PH / game theory material is coherent inside its archive; calendar facing checks are slow. Notebook use stays bounded by the PH routing rule; pairs with realist and multipolar lanes when the operator explicitly bridges. |
| `armstrong` | 0.68 | 0.32 | 0.55 | Cycle timing and macro war convergence claims are a recognizable brand; falsifiable windows need dated model outputs or method disclosure, not vibes. Useful beside energy logistics or sovereign debt weeks when Hormuz or fiscal stress is the question. |
| `baud` | 0.76 | 0.40 | 0.62 | Law of war and alliance mandate framing stays recognizable across crises; many claims hinge on classified or contested sourcing, so closure is slow. Often pulled in when the notebook needs European or UN adjacent tension beside U.S. military dissent lanes. |
| `berletic` | 0.74 | 0.36 | 0.58 | Industrial and sanctions throughput arguments are a clear signature; headline battle maps age faster than factory counts, so pair him when logistics and attrition matter. Bridges to energy system and realist lanes without replacing hull level ORBAT work. |
| `bigserge` | 0.72 | 0.34 | 0.60 | Long form war studies register on Substackâ€”campaign framing and narrative of operations that readers recognize week to week. Event linked claims often need wire or imagery to close. Pairs naturally with industrial capacity and ORBAT lanes as interpretive tension, not as duplicate primaries. |
| `simplicius` | 0.70 | 0.32 | 0.62 | Pseudonymous Substack voice with a recognizable â€œbluff, blockade, media readâ€ bundle on Middle East crises; falsification often waits on primaries behind the cited wires. Frequently read beside institutional or Beltway lanes as synthesis tension, not as a second wire. |
| `nima` | 0.72 | 0.34 | 0.68 | Host lane: coherence is â€œdid routing stay symmetric with the guest **`thread:`** on shared episodes?â€ rather than closure on a single forecast. Often sits at the bridge between named guests on **Dialogue Works** long forms. |

   

## Author threads: predictive accuracy and opinion drift

**Intent:** **`expert_id` rows** are the right **bucket** for (1) **checkable** calls vs outcomes and (2) **same voice, different week** â€” how emphasis, mechanism, or verdict **moves** as facts and audiences shift. **Topic** tags organize *substance*; **expert** threads keep **who** stable so you can grep **time series** without mixing voices.

**What to log (minimum viable):** Only claims that are **checkable** against **primaries or wires** (not vibes). For each candidate â€œpredictionâ€ or conditional forecast:

1. **Quote or tight paraphrase** + **source URL** (transcript timestamp, post, article).
2. **Date** the expert said it (ingest date or stated event horizon).
3. **`thread:<expert_id>`** matching the **Name** in the index row for **that** speaker.
4. **Falsify** â€” one sentence on what would make the call **wrong** (or what outcome resolves a conditional).
5. Later: **`resolved:`** + cite (wire / official readout) or **`deferred:`** + reason (still ambiguous, horizon not reached).

 **Where to put it:** Same session as the ingest â€” optional **`batch analysis`** line comparing two expertsâ€™ **testable** forks; or a bullet under **`### Predictive Outlook`** on the dated block in [`chapters/YYYY MM/days.md`](chapters/2026/2026-04/days.md) (replace month); or a running list in a scratch doc the operator names (no default new file). **Optional consolidated ledger (same contract):** [strategy expert predictions.md](strategy expert predictions.md) â€” **`pred_id`** rows + **`topic_slug`** registry + resolution receipts. **Optional resolution pass:** [.cursor/skills/fact check/SKILL.md](../../../../.cursor/skills/fact check/SKILL.md) for tiered verdicts when wires exist.

**Guardrails:** **WORK only** â€” not Record, not **Voice** truth. Do **not** turn into **accuracy theater**: unfalsifiable rhetoric (â€œthey are seriousâ€) is **not** a prediction; **base rate** and **topic difficulty** matter; **conditional** forecasts (â€œif X then Yâ€) need **both** legs scored. Prefer **sparse** high quality rows over scorecards full of mush.

### Changing opinions over time (drift / pivot detection)

**Why:** The same **`thread:<expert_id>`** on ingests **weeks apart** is the **join key** for â€œhas this expertâ€™s **story** changed?â€ â€” not only whether a single forecast hit.

**Minimum contrast (when you notice a shift):**

1. **Earlier** â€” date + source + one line **thesis** (quote or tight paraphrase).
2. **Later** â€” date + source + one line **thesis**.
3. **`thread:<expert_id>`** (same commentator).
4. **Delta** â€” label the move: **update** (new information integrated), **scope shift** (topic or audience changed), **emphasis** (same mechanism, different stress), **tension** (two claims need reconciliation â€” do not assume **contradiction** until you have both texts).

 **Where to log:** A single **`batch analysis | YYYY MM DD | â€¦`** line can carry **A vs B** for the same voice; or **`### Predictive Outlook`** on the **later** date (â€œfollow up: compare to 2026 04 01 ingestâ€); **git log** / **grep** on `thread:<expert_id>` across [`daily strategy inbox.md`](daily strategy inbox.md) and [`days.md`](chapters/2026/2026-04/days.md) history is the cheap detector.

**Guardrails:** **New facts** often justify revised judgment â€” distinguish **flip** from **Bayesian update**. Do **not** use drift tracking as **gotcha** copy unless the operator wants outreach; default is **notebook calibration**, not dunking.

   

## Crossing filters (what may cross the membrane)

Threads are **semi permeable** by design; â€œoptimizationâ€ here means **explicit rules** for what may **mix** so traceability stays high. This is **WORK** hygiene â€” not the **RECURSION GATE** / Record membrane.

**Default allow (fast lane â€” crossing is permitted):**

1. **`batch analysis | â€¦`** lines that **name** the relationship (convergence / divergence / weak bridge) and implicitly or explicitly reference **which** `expert_id`s are in play â€” ideally aligned with the **Typical pairings** column.
2. **Two (or more) separate** paste ready ingests, **each** with its own **`thread:<expert_id>`**, followed by **one** `batch analysis` â€” membership is unambiguous.
3. **`days.md` `### Reflection`** bullets that **label** both experts when comparing (e.g. **Marandi Ã— Ritter**) â€” prose bridge, not a merged ingest.
4. **Related voices** (below) and linked docs â€” **documented** seams (you already know the pore).

**Slow lane or block (do not merge without a seam):**

  **One** ingest line that **smuggles** two named authorsâ€™ claims **without** two cold attributions.
  **Cross thread synthesis** promoted to **strong** public copy when **`verify:`** is still **OSINT / expert commentary only** â€” raise tier or narrow the claim.
  **Legitimacy plane** vs **hard security** plane â€” keep the **seam** from [rome persia legitimacy signal check.md](rome persia legitimacy signal check.md); do not â€œsolveâ€ in one breath without naming both registers.

**Filter knobs (operator tunable, no code required):**

| Knob | Effect |
|      |        |
| **Index pairings** | Pre approved **expert Ã— expert** crosses for `batch analysis` â€” start here before inventing new pairings. |
| **`verify:` tier** | **`tier A`** / **`operator transcript`** / etc. â€” controls how far a cross thread line may travel outside the notebook. |
| **One primary `thread:` per ingest** | Keeps **drift** and **accuracy** joins clean; secondary voice = **second line** or **batch analysis**. |
| **`crosses:` vs `seam:`** | **`crosses:<expert_id>+<expert_id>`** â€” use on **`batch analysis`** when **two indexed ingests** each carry **`thread:`** for those slugs. **`seam:<slug>+<slug>`** â€” use when the batch compares **thematic planes** (government **X**, wire bundle, **ROME**, same week topic fork) and **`crosses:`** would wrongly imply **two roster Names**; example: **Spain Ã— China** in [daily strategy inbox.md](daily strategy inbox.md) (`seam:sanchez xi summit+hormuz brief same week`). |

**Optional `verify:` tail tokens** (all **optional** â€” use when you want grep + intent explicit):

  **`membrane:single`** â€” this line is **not** inviting pairing; `batch analysis` should **not** fold it into a multi thread claim without operator intent.
  **`membrane:pair`** â€” **invites** a following `batch analysis` (same day) that names partners (e.g. after two ingests are captured).
  **`crosses:<id>+<id>`** â€” rare; **explicit** authorization when one line **synthesizes** two **`expert_id`** threads (prefer two ingests + `batch analysis` instead).
  **`seam:<slug>+<slug>`** â€” optional, usually on a **`batch analysis`** line: names **which two thematic planes** are held side by side when **`crosses:`** is wrong (e.g. **no** **`thread:`** on one side â€” government **X**, **wire** bundle, **ROME** seam). Short kebab slugs; **`+`** joins them. **Distinct from `membrane:`:** **`membrane:`** = pairing **intent** on **ingests**; **`seam:`** = machine grep **label** for **what** the batch compares.

**Future automation (optional):** a small **validator script** could flag â€œ`batch analysis` mentions thread B but no ingest on this day has `thread:B`â€ â€” not required for the filter to work; **pairing discipline** + **git grep** already implement most of the membrane.

### Same transcript, show, or panel (multiple experts, one URL)

You do **not** get a special â€œjoint thread.â€ You **populate** each expertâ€™s lane with **separate paste ready lines** â€” [daily strategy inbox.md](daily strategy inbox.md) **Multi item ingest** rule: **one canonical line per excerpt / per voice**, **same episode URL repeated** on each line is normal.

1. **Line A** â€” **cold** names **Speaker A** + claim; **`thread:<expert_id_A>`** (their row in the table); **`verify:`** includes the shared URL (and timestamp/chapter if it helps grep).
2. **Line B** â€” **cold** names **Speaker B** + claim; **`thread:<expert_id_B>`**; **same URL**.
3. **`batch analysis | YYYY MM DD | â€¦`** â€” **immediately after** the **last** ingest in the set (placement defines membership). Name **tension** or **convergence** between the two **threads**; optional **`membrane:pair`** on the first line only if you want grep to show â€œinvites synthesis.â€

**Default workflow (operator canon): assistant draft + explicit approval before append** â€” Upload the transcript in session; have the assistant **draft** the full bundle (**one line per named author** + shared URL + **`thread:<expert_id>`**s + **`batch analysis`**) **in chat** (or a scratch file). Treat the draft as **provisional** until you **approve**. **Append** to [daily strategy inbox.md](daily strategy inbox.md) **only after** approval, or say **`EXECUTE`** / **explicit append** so the edit is deliberate. The assistant must **not** merge unreviewed bundles into the inbox by default.

**Host only** segments (no separate expert row) â€” **omit** **`thread:`** until a **named indexed expert** speaks; or tag **`thread:`** only when the **cold** attributes quoted/analysis material to that **commentatorâ€™s Name**. Keep **`verify:operator transcript`** when the clip is still provisional.

**Rare shortcut:** One line **cannot** carry two primary `thread:` ids cleanly â€” if the clip is **inseparably joint**, use **one** line with **`thread:`** = **primary** voice for **drift** tracking, **cold** names both, and optional **`crosses:<id>+<id>`** â€” or still prefer **two lines** + **`batch analysis`**.

   

## Deprecated `expert_id` values (operator removal)

**Topic slug ids (deprecated 2026 04 14)** â€” Replaced by **person slugs** (one expert per lane). Git history / old inbox lines may still use these; **do not** use on new ingests.

| Deprecated | Use instead |
|            |             |
| `islamabad process` | `marandi` |
| `washington channel` | `ritter` |
| `lebanon scope` | `parsi` |
| `hormuz domestic` | `barnes` |
| `third party system` | `macgregor` |
| `game theory escalation` | `pape` |
| `extension game` | `davis` |
| `structural pause` | `mearsheimer` |
| `diplomatic institutional` | `mercouris` |

Removed from the table **2026 04 13** â€” **git history** still has prior rows; do **not** reuse these **`expert_id`s** for new **Names** without clearing the deprecation note: `danny haiphong`, `intervention media hawk`, `skyvirginson lay catholic`, `kelly senate catholic`, `narrative faith meme`, `delegation babysitter`. **Coverage:** **Haiphong** hosted digests stay linked from **`johnson`** / digest file; **Keane** class TV, **Kushner**/**Witkoff** narrators, **SkyVirginSon** / **Kelly** / **Milad** lanes â†’ pair under existing rows (**`davis`**, **`ritter`**, **`marandi`**, **`ROME`** / [trump religion papacy arc.md](trump religion papacy arc.md), **`narrative escalation`** grep) instead of dedicated ids.

Removed from the table **2026 04 14** â€” **`hormuz story fork`** (commentators John Solomon / Chris Martenson). **Coverage:** U.S. domestic Hormuz story split (e.g. JTN â€œstrategic assetâ€ vs satirical spiral) â†’ `batch analysis` + topic tags only; pair with **`barnes`** when a third pole matters. Git history / 2026 04 12 inbox lines may still name Solomon or Martenson; do **not** use `thread:hormuz story fork` on new ingests.

   

## Related voices (not separate rows)

  **Andrew Napolitano** â€” **Judging Freedom** **host**; **not** **`ritter`**. **`ritter`** = **Scott Ritter** ingests only. **Host only** segments â†’ [daily strategy inbox.md](daily strategy inbox.md) **Host only** rule: **`thread:`** only when a **named** indexed expert speaks, else **omit**.
  **`@Pontifex` / Holy See** â€” Institutional **Rome** line: use **`ROME`**, [ROME PASS.md](../work strategy rome/ROME PASS.md), [rome persia legitimacy signal check.md](rome persia legitimacy signal check.md); not a freelance **expert** row.
  **Joe Kent** â€” Resignation letter **war rationale**; pair with **`davis`** / **`ritter`** when citing, not a duplicate of IAEA/DNI.
  **Milad33B** â€” **Meme** / **faith escalation** lane: use **`narrative escalation`** + `Milad` in cold and [trump religion papacy arc.md](trump religion papacy arc.md); policy Hormuz threads stay separate.

   

## File links

  Inbox format: [daily strategy inbox.md](daily strategy inbox.md)  
  Romeâ€“Persia legitimacy: [rome persia legitimacy signal check.md](rome persia legitimacy signal check.md)  
  Tri Frame minds: [minds/README.md](../README.md)  
  Haiphong / Ritter / Johnson digest: [transcript analysis haiphong ritter johnson iran 2026 04.md](../transcript analysis haiphong ritter johnson iran 2026 04.md)  
  Fact check skill (resolution / tiered verdicts): [.cursor/skills/fact check/SKILL.md](../../../../.cursor/skills/fact check/SKILL.md)
  Quality report: [scripts/report_strategy_thread_quality.py](../scripts/report_strategy_thread_quality.py)

## Quality report

`python3 scripts/report_strategy_thread_quality.py` is a read only diagnostic that examines the 21 author thread ecosystem and flags: **coverage gaps** (transcript content but empty machine layer), **roster drift** (table vs `CANONICAL_EXPERT_IDS`), **stale threads** (no transcript content in the lookback window), **extraction density** outliers, **missing companion files**, and **batch analysis alignment** issues (misspelled `thread:` tags). Output is markdown by default; `  json` for structured data. Optional `  log miss` records gaps to the retrieval miss ledger (`runtime/retrieval misses/index.jsonl`). Run after `python3 scripts/strategy_thread.py` or standalone.

