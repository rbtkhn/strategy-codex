---
name: news-verify
description: 'Triage tier-3 contemporary reported claims (news media, official releases, attributed desk lines) in ingests and briefs before synthesis: extract media hooks, fence interpretation, score developing-story claims (supported/contradicted/unclear/contested), optional verify receipts. Triggers: news verify, verify wires, verify tier, strategy + verify on breaking seams. Complements fact-check.'
preferred_activation: news verify
activation: news verify
portable: true
version: 1.6.1
category: truth-pipeline
status: active
scope_class: repo-governed
tags:
- verification
- statecraft
- singularity
- strategy
- provenance
portable_source: skills/news-verify/SKILL.md
synced_by: sync_portable_skills.py
---
# News verify

**Preferred activation:** **`news verify`**, **`news-verify`**, **`verify tier`**, or **`verify reports`** on a named ingest / brief / transcript batch.


**Legacy activation (compatibility):** **`wire verify`**, **`wire-verify`**, **`verify wires`** — same skill; prefer **`news verify`** for new work.

**Term law:** **News** here means **corpus tier 3** — contemporary **reported** claims (news media, official releases, attributed desk lines), not tier-4 analyst commentary.

**Scope:** Fast external check on **tier-3 contemporary reported claims** — news media, official/government releases, and attributed desk lines inside ingests — especially when **second-hand inside a transcript** ("according to the New York Times…", "Axios says…", "Hebrew media reports…").

**Corpus tier (source-lattice):** News-verify grades **corpus tier 3 only** — current-events news / official. SSOT: [source-lattice § statecraft corpus tiers](../../docs/source-lattice-beyond-the-repo.md#statecraft-corpus-tiers-strategy-codex) · registry [§ placement](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md#source-lattice-placement).

| Tier | Scope |
|------|--------|
| **1** Historical primary | Out of scope — civ-state primary-text acquisition |
| **2** Historical secondary | Out of scope — Durant, Gibbon, CIV-MEM, etc. |
| **3** Current-events news | **This skill** — sub-tiers **3a** (official), **3b** (major wire), **3c** (syndicated/social) |
| **4** Current-events commentary | Out of scope for news-grade verification — Mercouris, Diesen, Davis, landed transcripts |

**Not in scope (label, do not score as wire facts):**

- **Corpus tier 4** analyst **interpretation**, forecasting, or doctrine (escalation dominance, decoupling arcs, "what Iran wants").
- Operator opinion, predictions, moral frames.
- **Corpus tier 1–2** historical claims cited inside commentary.
- **Deep 3a pull** (full MFA readout, court filing, official PDF) beyond triage — escalate to **fact check deep** (fact-check skill `#fact-check-deep-pass`) or lane-specific primary skills.

<a id="verification-routing-shared"></a>

## Verification routing (shared — fact-check ↔ news-verify)

**SSOT:** identical block in fact-check and this file (sync via `sync_portable_skills.py`). Update **both** when routing law changes.

Use this table **before** choosing a pass. Bare **`verify`** is ambiguous — ask once or infer from **input shape**.

| Operator input | Route | Why |
| --- | --- | --- |
| **One claim** pasted or named (sentence, stat, quote, URL summary, draft line) | **`fact check`** | Discrete triage; operator supplies the claim |
| **Full ingest**, day archive, daily brief, or **verification matrix** | **`news verify`** (this skill) | Auto-extract tier-**3** hooks; profile sweep (CIV-STATE or MR-VOL); optional `verify:` receipts; **capture-gap pre-pass** when body may be partial |
| **`fact check`** on a **news-heavy capture** but job is "grade hooks before synthesis" | **`news verify`** (prefer) | Batch hook inventory + developing-story handling |
| **Single fork** from a matrix row ("is J17-7 supported?") | **`news verify`** sub-hook **or** **`fact check`** | Sub-hook when lane-sweep context matters; fact-check when the claim is isolated |
| **Analyst voice** (Mercouris, Diesen, Davis, landed commentary) stating mechanism, forecast, or doctrine | **Label tier 4 / interpretation** — **do not score as wire fact** | Corpus tier 4; synthesis may use; verification does not grade |
| **Historical** primary/secondary cited inside commentary | **Out of scope** for news-verify; **`fact check`** only if operator names the historical claim | Corpus tiers 1–2 |
| **Primary doc** needed (full MFA readout, court filing, official PDF) beyond triage | **fact check deep** ([deep pass anchor in fact-check skill]) | Escalate from news-verify or thin fact-check triage |
| **Campaign / Massie-shaped** copy from today's news | **politics-massie** | Not neutral verification |
| **Before** `state synthesis` or promoting into Judgment on a **same-week** seam | **`news verify`** (batch mode) | Pre-synthesis gate on tier-3 report hooks |
| **`source-archive/singularity/`** ingest or workshop sheet; markets / vendor / regulator hooks | **`news verify — singularity`** (singularity profile) | [Singularity sweep profile](#singularity-sweep-profile-stub) — not full CIV-STATE mesh by default |
| Same ingest, **statecraft crossover** hooks (export control, sovereign-AI law) | **Split receipts** — singularity profile on sheet; **statecraft profile** on crossover note / statecraft path | Do not merge panel numbers across captures |

**Verdict vocabulary (align across skills):**

| fact-check | news-verify | Meaning |
| --- | --- | --- |
| Supported | supported | Corroborated within pass budget |
| Contradicted | contradicted | Clear counter-evidence |
| Unclear | unclear | Thin, noisy, or not locatable in triage time |
| Out of scope | *(label only)* | Prediction, opinion, tier 4 — not a news row |
| — | contested | Credible sources conflict |
| — | partial | Some elements supported; hook incomplete |

**Ambiguity rule:** If both a **named claim** and a **full ingest path** appear, prefer **`news verify`** when the ingest is the primary object; prefer **`fact check`** when only the claim matters and archive context is optional.

## Relationship to fact-check

| Skill | Role |
|-------|------|
| **fact-check** (host skill) | General triage on **any** checkable claim the operator names. |
| **news-verify** (this skill) | **Scoped child:** auto-extract **tier-3 report hooks** from ingests/briefs, apply fact-check verdict discipline, add **developing-story** and **contested-wire** handling, optional **verify receipt** for archive/inbox. |

When the operator says **`fact check`** on wire-only material, you may run **either** skill; prefer **news-verify** when the input is a **full ingest** or **live-desk batch** and the job is "grade the hooks before synthesis." See [Verification routing](#verification-routing-shared) for the full decision table.

**Not a substitute for** campaign/newsletter lanes (**politics-massie**, **skill-write**). Stay **claim-neutral**.

## Lane

- Default **Think:** verdict table in chat; **no** repo edits unless the operator switches to **Ship** and names files.
- **Ship (explicit):** append **`verify:`** tails, **`editorial_note`** / **`source_note`** receipts on landed captures, or inbox lines — still **not** Record merge.
- **Batch Ship default (gate weeks):** when `archive_count ≥ 3` on a same-week breaking seam and the next move is **`state synthesis`**, write **`statecraft/notes/wire/YYYY-MM-DD-news-verify-matrix.md`** (daily news-verify SSOT) before synthesis — optional per-capture `verify:` pointers only. Gate law: [NEWS-VERIFY-SYNTHESIS-GATE.md](../../statecraft/synthesis/NEWS-VERIFY-SYNTHESIS-GATE.md).

## When to invoke

- After **statecraft source intake** or **strategy ingest** on a **breaking** or **same-week** seam.
- Before **`state synthesis`**, **`strategy` EOD compose**, or promoting a claim into **`days.md` Judgment**.
- When **`strategy + verify`** is named and the load-bearing rows are **news-sourced**.
- When the operator asks to **news-verify** specific seams (Apache, infiltration, Houthi statement, non-intercept, roster, counts).
- After **singularity archive** land or before promoting a **workshop sheet** claim ([intake triad](../../source-archive/singularity/README.md#intake-triad-operator-protocol)).

## Sweep profiles (overview)

One portable skill; **two sweep grammars**. Shared: tier **3** vs tier **4** fence, verdict vocabulary, capture-gap pre-pass, optional `verify:` receipts.

| Profile | Default when | Sweep model | SSOT |
|---------|--------------|-------------|------|
| **Statecraft** (default) | `source-archive/statecraft/`, verification matrices, daily briefs, combatant seams | **CIV-STATE** five lanes — cite or **`-absent`** each | [CIV-STATE registry](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md) |
| **Singularity** (stub v0.1) | `source-archive/singularity/`, workshop sheets, RSI / markets / vendor seams | **MR-VOL** — cite or **`-absent`** only for **hook-touched** surfaces | [§ Singularity sweep profile (stub)](#singularity-sweep-profile-stub) |

**Operator shorthand:** `news verify` or `news verify — statecraft` = CIV-STATE default; **`news verify — singularity`** = singularity profile. Infer from path when unqualified.

**Crossover:** singularity ingest with statecraft load-bearing hooks → **split receipts**; do not merge into one mesh row.

## Pass modes (batch vs sub-hook)

| Mode | When | Hooks | Sweep |
|------|------|-------|-------|
| **Batch** (default) | Full ingest, day batch, matrix gate, pre-**`state synthesis`** | Inventory all report hooks in scope | **Profile-full** — statecraft: all five CIV-STATE lanes; singularity: MR-VOL lanes **when any hook touches that surface** |
| **Sub-hook** | Operator names **one claim** or narrow fork (e.g. "Iran intentional credit?", "ICE futures live?") | 1–5 rows only; merge near-duplicates | **Hook-scoped** — statecraft: combatant + mesh-if-spoke; singularity: MR-VOL lanes the hook touches |

**Sub-hook law:** Do not skip the mesh line or **Confidence** / **Escalate** blocks because the question is narrow. Do not claim **full sweep** without the profile checklist (statecraft: [execution checklist](#sweep-execution-checklist); singularity: [stub](#singularity-sweep-profile-stub)).

**Operator shorthand:** `news verify — full mesh` = batch statecraft profile; `news verify — singularity` = singularity profile; `news verify — intent only` = sub-hook; default to **sub-hook** when the message is a single yes/no fork.

<a id="capture-gap-pre-pass"></a>

## Capture-gap pre-pass (before hook detection)

Run this **before** Wire hook detection whenever the pass names a **landed capture path** (`source-archive/...`, ingest stub, or matrix row tied to one file). **Do not** extract or score report hooks from metadata alone.

### When to flag **capture-gap**

Flag when **any** of these hold:

| Signal | Example |
| --- | --- |
| **Title / YAML promises segments absent from body** | Title lists PoS2 + UK navy; body ends on unrelated G7 line |
| **`source_note` / `capture_note` cross-refs not in transcript** | YAML names Konstantinovka, Mongolia route; `## Transcript` never reaches them |
| **Abrupt mid-sentence end** | Body stops mid-thought with no closing sections |
| **Operator or `editorial_note` marks partial paste** | "operator-pasted"; fatigue/travel; "not human-verified" + obvious truncation |
| **Sub-hook names a seam the file does not contain** | "news verify G7 energy sanctions" but sentence is cut off before completion |

**Not capture-gap:** full body with ASR noise; tier-4 analyst interpretation with no missing title segments; day batch where **other** captures carry the hook.

### Required output (first rows)

Emit a **Capture status** block **before** the hook verdict table:

```text
**Capture status:** partial | complete
**Gap:** <what title/YAML promised but body lacks — or "none">
**Hooks in scope:** only claims **present in transcript body** (and attributed wires inside it)
**Do not score:** <segments absent from disk>
**Next archive move:** operator paste tail · `land_statecraft_intake.py` · fetch only if operator authorized
```

### Pass law

1. **Never** invent hooks from **`title`**, **`source_note`**, or **`capture_note`** when the claim is not spoken or wire-attributed **in the body**.
2. **Batch mode** on a **partial** solo capture: score hooks **in body**; list promised-but-missing segments under **Do not score**; do **not** mark the day matrix **complete** for those segments.
3. **Sub-hook** on a missing segment: verdict **Unclear (capture-gap)** — not Supported/Contradicted — and point to archive completion.
4. **Synthesis coupling:** if **`state synthesis`** already flagged truncation, news-verify **confirms**; do not upgrade child-note **capture-gap** claims without new body on disk.
5. **Ship:** optional `editorial_note` / `source_note` tail `capture_gap: <short slug>` only when operator names **Ship**; default Think stays chat-only.

### Mercouris-shaped example (Jun 17)

- **In body:** MOU pause, Blair/Telegraph attribution, Moscow source, G7 Zelensky maneuver, Russia-energy line **starts** then **cuts off**
- **Gap:** PoS2, UK navy/yacht, Konstantinovka — title/YAML only
- **News-verify:** score **in-body** attributed wires (e.g. Sky News economy claim if desk-locatable); **Unclear (capture-gap)** for G7 sanctions **completion**; **do not score** PoS2/UK navy until tail lands

## Wire hook detection

Scan for:

1. **Named outlets** — NYT, WSJ, Reuters, AP, Axios, BBC, CNN, NBC, CBS, Times of Israel, Haaretz, Ynet, Anadolu, Al-Monitor, etc.
2. **Institution quotes** — IDF, CENTCOM, Pentagon, IAEA, UNIFIL, IRNA-class (English syndication ≠ primary; see below).
3. **Transcript attribution** — "according to…", "reports say…", "my sources…", "we don't have confirmation yet."
4. **Developing-story markers** — "under investigation," "allegedly," "preliminary," "Hebrew media," conflicting US officials.

**High misstatement risk (prioritize):** casualty counts, **who** did **what**, **when**, **how many**, delegation **rosters/titles**, **mechanism** (SAM vs drone vs malfunction), **affiliation** (Hezbollah vs unknown terrorist), **first time since** claims.

**Singularity hook classes (when profile = singularity):** IPO / mkt-cap figures; **announced vs live** product or contract; vendor **access tier** / kill-switch; model **release** names and dates; **regulatory approval pending** vs **cleared**; issuer **first-ever** uniqueness; control-plane **observability** without primary.

## Statecraft profile — CIV-STATE sweep (default)

**Do not** close news-verify on **English-only Western wires** alone when hooks are **regime- or institution-attributed**.

**Source registry (SSOT):** [NEWS-VERIFY-CIV-STATE-SOURCES.md](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md) — **corpus tier 3** per-lane outlet tables (**3a/3b/3c**; legacy T1/T2/T3), URLs, native-lang law, and verify tokens. **Do not** maintain parallel outlet lists in chat; extend the registry when a lane gains a new stable **3a**.

**Fixed lanes — search all five on every `news verify` pass using the statecraft profile** (same story window as the hooks; **no topic triggers**):

| Lane | Repo surface | Registry | If lane silent in window |
|------|--------------|----------|---------------------------|
| **America** | `statecraft/america/` | [§ America](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md#america-lane) | `verify:america-lane-absent` |
| **Persia** | `statecraft/persia/` | [§ Persia](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md#persia-lane) | `verify:persia-lane-absent` |
| **China (PRC)** | `statecraft/china/` | [§ China](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md#china-lane-prc) | `verify:prc-lane-absent` |
| **Russia** | `statecraft/russia/` | [§ Russia](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md#russia-lane) | `verify:russia-lane-absent` |
| **Rome (Holy See)** | `work-strategy-rome/` | [§ Rome](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md#rome-lane-civ-state) | `verify:rome-lane-absent` |

**Daily-brief companions** (48h scan — not duplicate registries): [jd-vance-watch](../../docs/skill-work/work-strategy/daily-brief-jd-vance-watch.md) · [iran-watch](../../docs/skill-work/work-strategy/daily-brief-iran-watch.md) · [prc-watch](../../docs/skill-work/work-strategy/daily-brief-prc-watch.md) · [putin-watch](../../docs/skill-work/work-strategy/daily-brief-putin-watch.md) · [native-international-pass](../../docs/skill-work/work-strategy/daily-brief-native-international-pass.md).

**Sweep law:**

- **All five lanes** every pass — cite **≥1** **3a/3b** when that lane commented on the seam; else **`-absent`** receipt + one-line note. **Silent skip forbidden** → `verify:triangulation-incomplete`.
- **Attribution:** facts attributed to a lane are **blocked at Supported** without that lane's receipt. Native lang when wording disputes: **`fa`** (Persia), **`zh`** (PRC), **`ru`** (Russia), **`it` / `es` / `fr` / `pt`** (Rome per registry).
- **Mesh:** non-combatant lanes (**PRC**, **Rome**) inform **framing** when combatant lanes contest; they **do not** override America/Persia attribution.
- **Lanes disagree** → **`Contested`** or **`Unclear`** — never flatten to one wire.
- **Commentator transcript** = **interpretation** unless paired to lane primaries.
- **Adjacent** (Israel, Oman): [registry § Adjacent](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md#adjacent-israel) — **outside** the five-lane sweep; add only when the hook names IDF/Oman/mediation.

Extended outlet names may appear in `research/repos/civilization_memory/.../IRAN–WAR–CHRONICLE.md`; the **registry** is the operator news-verify SSOT.

### Sweep execution checklist

Before closing any pass, confirm **each** lane row (batch = all five; sub-hook = combatant + mesh lanes):

| Step | Requirement |
|------|-------------|
| 1 | **Query** ≥1 registry **3a** URL for that lane (site search or registry table link) — not generic web prose alone |
| 2 | **Record** lane + **lang** + sub-tier (**3a** / **3b** / **3c**) on every cite |
| 3 | If silent → **`verify:<lane>-lane-absent`** + one line: *what was searched, window, no dated line* |
| 4 | If a lane was not searched → **`verify:triangulation-incomplete`** — do not mark "5/5 sweep" |

**Anti-pattern:** Tagging **`-absent`** without naming the registry surface queried.

### Social and executive tier (corpus tier 3 sub-tiers)

Full outlet tables live in the **registry**; this table fixes **common mis-tiers** only:

| Surface | Lane | Sub-tier | Satisfies lane receipt? |
|---------|------|----------|-------------------------|
| CENTCOM / DoD / State / White House press | America | **3a** | Yes, when dated to seam |
| Trump **Truth Social** | America | **3a** executive | Yes for **U.S. executive frame** — not forensic intent proof alone |
| Anonymous **U.S. officials** (CNN/Axios/AP) | America | **3b** | Supporting; pair for contested/high-stakes |
| **IRNA** / **MFA** (`fa` or EN) | Persia | **3a** | Yes for Tehran wording / denial |
| FM **X** posts (e.g. Araghchi) | Persia | **3c** | **No** alone — `verify:persia-lane` supporting + **`verify:fa-triangulation`** pending until MFA/IRNA |
| Deputy minister via **foreign wire only** | Persia | **3b/3c** | **Contested** until `fa` **3a** |
| **TASS** / **Reuters** quoting Iran "unintentional" | Russia / wire | **3b** overhearing | **Not** Persia **3a** |
| **Xinhua** repeating Trump/CENTCOM | PRC | **3b** | Mesh framing — not independent causation adjudication |
| Commentator transcript | — | **tier 4** | Interpretation fence only — not news-grade verification |

<a id="singularity-sweep-profile-stub"></a>

## Singularity sweep profile (stub v0.1)

**Status:** stub — do not fork a second skill. Activation: **`news verify — singularity`**. Default infer: `source-archive/singularity/**` → singularity profile; statecraft archive → CIV-STATE default (§ Statecraft profile below).

**Shared law:** tier **3** hooks only; tier **4** panel/newsletter → **Interpretation** fence; same verdicts and `verify:` receipts as statecraft.

### MR-VOL lanes (Markets · Regulators · Vendors · Operators · Labs)

Search **only lanes the hook touches**. Do **not** run CIV-STATE Persia/PRC/Rome `-absent` theater on pure markets/regulatory seams.

| Lane | Typical surfaces | If silent |
|------|------------------|-----------|
| **Markets** | Exchange IR, SEC filings, CNBC/Reuters/Bloomberg | `verify:markets-lane-absent` |
| **Regulators** | SEC, CFTC, Commerce/White House export notices | `verify:regulators-lane-absent` |
| **Vendors** | Lab policy pages, API status, model/system cards | `verify:vendors-lane-absent` |
| **Operators** | Issuer site, Business Wire/AP releases | `verify:operators-lane-absent` |
| **Labs** | Named frontier-lab official posts when hook names a lab | `verify:labs-lane-absent` |

**Stub law:** *announced vs live* → **partial** until **3a** cleared; panel numbers → **contested** until Markets/Regulators **3b+**; vendor kill-switch/downgrade → **Unclear** without vendor **3a**. **Crossover** (export control, sovereign-AI law) → statecraft profile on crossover note; **split receipts** from singularity sheet.

**Chat header:** `Profile: singularity · MR-VOL sweep: n/n (hook-scoped)` — not `CIV-STATE 5/5`.

**Registry (planned):** `docs/skill-work/work-singularity/WIRE-VERIFY-SINGULARITY-SOURCES.md` — ad hoc cites until EXECUTE.

## Attribution duel subroutine

When hooks are **denial vs accusation** or **intent forks** (e.g. Tehran "not deliberate" vs Trump "shot down"):

1. **Split rows** — do not merge into one verdict:
   - **Involvement** (who caused the event)
   - **Intent** (deliberate vs accidental)
   - **Executive frame** (attack / respond / aggression labels)
   - **Investigative frame** (under investigation / intent not established)
2. **Grade separately** — executive **Supported** for what was said; investigative **Unclear** is compatible, not contradictory.
3. **Refutation row** — "America refutes Iran denial" needs an explicit U.S. spokesperson/readout; else **Partial** (implicit via strikes/labels) or **Not supported**.
4. **Token** — `verify:wire-contested` on the duel; add `verify:dual-lane-contested` when America and Persia primaries disagree on the same sub-row.

## Procedure

1. **Inventory hooks** — List discrete wire-attributed claims (merge near-duplicates). One row per checkable fact. Tag primary attribution lane: **`america`** · **`persia`** · **`prc`** · **`russia`** · **`rome`** · **`other`**.
2. **Fence interpretation** — Move speaker/analyst frames to an **Interpretation** block (max three bullets). Do not verdict-score them as Supported/Contradicted.
3. **Classify story state**
   - **Developing** — cause/mechanism/count still moving; note **interview/publication time** if transcript predates later wires.
   - **Settled** — multiple independents align; official statement landed.
   - **Contested** — credible outlets disagree (e.g. "did not intercept" vs "fired interceptors in self-defense"; **America vs Persia** primary mismatch).
4. **Profile sweep** — **Statecraft:** CIV-STATE per [pass mode](#pass-modes-batch-vs-sub-hook); complete [execution checklist](#sweep-execution-checklist). **Singularity:** MR-VOL per [stub](#singularity-sweep-profile-stub). Record **lane** + **lang** on each cite. Lane absent → **`-absent`** token. If native primary not found in triage time on a wording row → **Unclear** + **Escalate** (`fact check deep` or operator native pull). Apply [attribution duel](#attribution-duel-subroutine) when denial/intent load-bears (statecraft profile).
5. **Search (triage)** — One solid cite per **lane** (or absent receipt); second cite on the **claim row** when **contested** or **high-stakes**. Prefer: **3a native official** > **3a EN** > **3b** wire > **3c** syndicated.
6. **Verdict table**

   | Claim (short) | Lane | Lang | Wire / primary cited | Verdict | Cite (title + URL) |
   |---------------|------|------|----------------------|---------|---------------------|
   | … | America / Persia / PRC / Russia / Rome | `en` / `fa` / `zh` / `ru` / `it` / … | CENTCOM / IRNA / MFA PRC / Kremlin / Vatican News / … | **Supported** / **Contradicted** / **Unclear** / **Contested** / **Out of scope** | … |

   **Contested** = two credible lines disagree (including **America vs Persia**); state both in one row or split sub-rows.

7. **CIV-STATE mesh row** — One line per hook: `America: … · Persia: … · PRC: … · Russia: … · Rome: … · Mesh: supported | contested | unclear` (use `absent` per lane when silent).
8. **Developing-story caveat** — One line under the table when timing matters ("Nawfal aired while cause **under investigation**; later Trump/Axios pointed to **drone**; IRNA `fa` line not yet pulled.").
9. **Confidence** — One line: low / medium / high + what would raise it (CENTCOM release, **IRNA/MFA `fa`**, IDF Spokesperson Hebrew, primary Houthi Arabic statement).
10. **Escalate (if needed)** — Primary pull list per **missing lane**; say **`fact check deep`** when beyond triage.

## Optional verify receipt (Ship)

When the operator asks to land tags or after **EXECUTE** on an archive file, append a compact block:

```yaml
# source_note or editorial_note tail (example)
verify_receipt: 2026-06-09
verify:
  - claim: Apache down near Hormuz; two crew rescued
    verdict: supported
  - claim: Iranian SAM caused crash
    verdict: unclear
    note: later wires lean drone; intent not established
  - claim: multiple Hezbollah infiltrators inside Israel
    verdict: contradicted
    note: one gunman; searches found no additional threats
```

Inbox / brief paste tail (example): `verify:wire-supported` · `verify:wire-contested` · `verify:wire-unclear` — see host appendix for repo token vocabulary.

## Output shape (chat default)

**Minimum block (required)** — batch and sub-hook; never omit **Lang**, **Confidence**, or **Escalate** when any lane is absent or wording is disputed:

```markdown
## News verify — <subject> (<date context>)

**Mode:** batch | sub-hook · **Hooks checked:** N · **CIV-STATE sweep:** 5/5 | combatant+mesh · **Developing:** yes/no · **Confidence:** low | medium | high

### Lane sweep receipts
| Lane | Registry queried | Spoke? | Token |
|------|------------------|--------|-------|
| America | CENTCOM, … | yes/no | verify:america-lane | -absent |
| … | … | … | … |

| Claim | Lane | Lang | Verdict | Cite |
|-------|------|------|---------|------|

**CIV-STATE mesh:**
- <hook>: America … · Persia … · PRC … · Russia … · Rome … · **contested**

**Developing-story caveat:** …

**Interpretation (not wire-verified):**
- …

**Escalate:** …
```

Sub-hook passes may use a **short** lane table (combatant rows + mesh lanes) but must still show **registry queried** per lane searched.

## Guardrails

- Assistant + web output is **not** Record truth. Cite what you found and where.
- Do not upgrade **commentator monologue** or **analyst essays** to news-grade verification without tagged sources.
- Do not collapse **Hebrew-media speculation** into confirmed IDF fact without Spokesperson alignment.
- Do not close a **statecraft batch** without the **five-lane CIV-STATE sweep** — cite or **`-absent`** per lane with [checklist](#sweep-execution-checklist) evidence.
- Do not run **CIV-STATE 5/5 `-absent` theater** on **singularity-only** seams — use [singularity profile](#singularity-sweep-profile-stub); hand off crossover hooks to statecraft profile.
- Do not mark singularity **announced** products (`plans to launch`, `ticker reserved`) as **Supported/live** without **3a** cleared-effective proof.
- Do not mark **5/5 sweep** on a **sub-hook** pass unless all five lanes were actually searched; use **combatant+mesh** honestly.
- Do not satisfy **Persia-lane** receipt with **Araghchi X** or foreign-wire denial alone — escalate **`fa`** per registry.
- Do not grade **lane-attributed** facts from **another lane's** outlets alone (e.g. Tehran from CNN only; CENTCOM from IRNA only).
- Do not treat **PRC** or **Rome** as tie-breakers for combatant attribution.
- **Abstain** honestly; **Unclear** beats false precision on fast-moving desks.

## Related

- **[source-lattice-beyond-the-repo.md](../../docs/source-lattice-beyond-the-repo.md#statecraft-corpus-tiers-strategy-codex)** — corpus tiers **1–4** (news-verify = tier **3** only).
- **[NEWS-VERIFY-CIV-STATE-SOURCES.md](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md)** — statecraft profile SSOT (America, Persia, China, Russia, Rome; **3a–3c**).
- **[source-archive/singularity/README.md](../../source-archive/singularity/README.md#intake-triad-operator-protocol)** — intake triad; singularity verify before promote.
- **`WIRE-VERIFY-SINGULARITY-SOURCES.md`** — *planned* MR-VOL registry under `docs/skill-work/work-singularity/` (stub cites ad hoc until landed).
- **fact-check** (host skill) — general triage; native-primary discipline; **`fact check deep`** escalation.
- Host appendix — repo paths for inbox tokens, statecraft `source_note`, `strategy + verify` gate (Cursor install only).


## Cursor / strategy-codex instance

# News verify — strategy-codex appendix

| Topic | Path |
|-------|------|
| **Corpus tiers 1–4** (news-verify = tier **3** only) | [docs/source-lattice-beyond-the-repo.md § statecraft corpus tiers](../../docs/source-lattice-beyond-the-repo.md#statecraft-corpus-tiers-strategy-codex) |
| **CIV-STATE wire source registry (SSOT)** | [docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md) — sub-tiers **3a/3b/3c** |
| Portable core | [skills/news-verify/SKILL.md](SKILL.md) |
| General fact triage | [.cursor/skills/fact-check/SKILL.md](../../.cursor/skills/fact-check/SKILL.md) |
| Strategy + verify gate | [DEFAULT-PATH.md](../../docs/skill-work/work-strategy/DEFAULT-PATH.md) + [news-verify/SKILL.md](../news-verify/SKILL.md) |
| Statecraft intake | [.cursor/skills/statecraft-source-intake/SKILL.md](../statecraft-source-intake/SKILL.md) |
| Daily brief verify tokens | [docs/skill-work/work-strategy/daily-brief-template.md](../../docs/skill-work/work-strategy/daily-brief-template.md) § Inbox paste target |
| Strategy inbox | [docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md](../../codex/daily-strategy-inbox.md) |
| Notebook verify discipline | [docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md](../../codex/NOTEBOOK-PREFERENCES.md) |
| Statecraft archive | [source-archive/statecraft/](../../statecraft) |
| Iran native triangulation | [docs/skill-work/work-strategy/daily-brief-iran-watch.md](../../docs/skill-work/work-strategy/daily-brief-iran-watch.md) |
| Native-language pass (all jurisdictions) | [docs/skill-work/work-strategy/daily-brief-native-international-pass.md](../../docs/skill-work/work-strategy/daily-brief-native-international-pass.md) |
| Persia statecraft lane | [statecraft/persia/README.md](../../statecraft/persia/README.md) |
| Rome / Holy See (CIV-STATE) | [NEWS-VERIFY-CIV-STATE-SOURCES.md § Rome](../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md#rome-lane-civ-state) · [ROME-PASS.md](../../docs/skill-work/work-strategy/work-strategy-rome/ROME-PASS.md) |
| America statecraft lane | [statecraft/america/README.md](../../statecraft/america/README.md) |
| China (PRC) statecraft lane | [statecraft/china/README.md](../../statecraft/china/README.md) |
| PRC 48h watch (neutral Iran-war triangulation) | [docs/skill-work/work-strategy/daily-brief-prc-watch.md](../../docs/skill-work/work-strategy/daily-brief-prc-watch.md) |
| U.S. executive / VP watch | [docs/skill-work/work-strategy/daily-brief-jd-vance-watch.md](../../docs/skill-work/work-strategy/daily-brief-jd-vance-watch.md) |
| Iran war source hierarchy (research) | [research/repos/civilization_memory/content/civilizations/PERSIA/IRAN–WAR–CHRONICLE.md](../../research/repos/civilization_memory/content/civilizations/PERSIA/IRAN–WAR–CHRONICLE.md) |
| Work menu conventions | [docs/skill-work/work-menu-conventions.md](../../docs/skill-work/work-menu-conventions.md) |

## Repo defaults

- **Default lane:** Think (chat table). **Ship** only when the operator names files (`source_note`, `editorial_note`, inbox line, `days.md` **Links** — not **Judgment** without dated URLs).
- Run **after** transcript lands, **before** `state synthesis` or EOD compose when breaking seams load-bear.
- Pair with **`strategy + verify`** when folding report hooks into codex / strategy-notebook layers.
- **Every batch:** run the **five-lane CIV-STATE sweep** (America · Persia · PRC · Russia · Rome — cite or **`-absent`** per lane) per portable core § *CIV-STATE sweep (every pass)* — before `state synthesis` or matrix promotion.
- **Sub-hook passes** (v1.5.0+): single-fork operator questions — combatant lanes + mesh; still emit minimum chat block + [sweep execution checklist](SKILL.md#sweep-execution-checklist); do not fake 5/5 without searching.
- **Corpus tier law** (v1.5.1): grade **tier 3** only (**3a** official · **3b** wire · **3c** syndicated/social); **tier 4** commentary (archive transcripts, Mercouris/Diesen benches) = interpretation fence — not wire facts.

## `verify:` token vocabulary (extend daily-brief defaults)

Use on inbox lines, brief §1f rows, or archive YAML tails:

| Token | Meaning |
|-------|---------|
| `verify:wire-RSS` | RSS / live-desk wire; not state primary |
| `verify:wire-supported` | News-verify triage: supported |
| `verify:wire-unclear` | Developing or thin sourcing |
| `verify:wire-contested` | Credible wires disagree |
| `verify:wire-contradicted` | Best current cite contradicts hook |
| `verify:operator-transcript` | Hook still only in pasted transcript |
| `verify:tier-A` | Operator-attested or primary-aligned (per notebook tables) |
| `verify:america-lane` | U.S. official / CENTCOM / executive primary checked |
| `verify:america-lane-absent` | America search run; no material line in window |
| `verify:persia-lane` | Iranian state / IRNA-class line checked |
| `verify:persia-lane-absent` | Persia search run; no material line in window |
| `verify:fa-triangulation` | Persian (`fa`) primary pulled for wording / attribution |
| `verify:dual-lane-contested` | America and Persia primaries disagree |
| `verify:dual-lane-incomplete` | Iran war hook; America or Persia lane missing — do not promote to Judgment |
| `verify:executive-investigative-split` | U.S. executive "attack" frame vs background "intent unclear" — both valid rows |
| `verify:denial-duel-contested` | Tehran denial / non-deliberate vs U.S. causation or refutation fork |
| `verify:fa-triangulation-pending` | Persia wording row; Araghchi X or syndication only — MFA/IRNA `fa` not pulled |
| `verify:prc-lane` | PRC/MFA/Xinhua neutral line checked for same seam |
| `verify:prc-lane-absent` | PRC search run; no material Beijing statement in window |
| `verify:zh-triangulation` | Mandarin (`zh`) MFA/Xinhua primary for load-bearing PRC wording |
| `verify:triangulation-incomplete` | One or more of five CIV-STATE lane searches skipped |
| `verify:russia-lane` | Kremlin / TASS checked |
| `verify:russia-lane-absent` | Russia search run; no material line in window |
| `verify:israel-adjacent` | IDF Spokesperson / Israel MFA checked |
| `verify:oman-adjacent` | Oman mediation channel checked |
| `verify:he-triangulation` | Hebrew primary for IDF wording disputes |
| `verify:rome-lane` | Holy See primary (press.vatican.va / Vatican News) |
| `verify:rome-lane-absent` | Rome search run; no material Holy See line in window |
| `verify:it-triangulation` | Italian / Vatican News IT for papal wording |
| `verify:es-triangulation` | Spanish overhearing (ACI, EFE, Vatican News ES) |
| `verify:fr-triangulation` | French overhearing (La Croix, AFP, Vatican News FR) |
| `verify:pt-triangulation` | Portuguese overhearing (Lusa, Agência Brasil, Vatican News PT) |

## Statecraft archive receipt shape

On `source-archive/statecraft/YYYY-MM-DD/source-*.md` frontmatter when operator ships verify:

- Extend **`source_note`** or **`editorial_note`** with semicolon-separated verify tails, or compact **`verify:`** list in YAML if the file already uses structured frontmatter (match neighboring captures).
- Do **not** rewrite transcript body for verify outcomes.
- Example seam tags: `verify: Apache cause — unclear (drone vs SAM)`; `verify: infiltration count — downgraded to one`.

## Strategy-codex weave convention

Existing thread weaves use **news-verify** informally for roster/title checks (e.g. delegation head misnames). This skill formalizes that habit: run **`news verify`** on roster lines before promoting to **Links**.

## Escalation routes

| Need | Next skill / action |
|------|---------------------|
| Non-wire claim | **`fact check`** |
| Deeper primary pull | **`fact check deep`** (operator phrase) |
| Any wire hook (batch) | **Five-lane CIV-STATE sweep** per portable core — America · Persia · PRC · Russia · Rome (`fa`/`zh`/`ru`/Romance when wording load-bearing) |
| Narrow fork (sub-hook) | Portable core § *Pass modes* + *Attribution duel* — combatant lanes required; mesh lanes searched or **`-absent`** with registry note |
| Iran/PRC/Russia wording | Native primary per **fact-check** + `daily-brief-*-watch.md` |
| Full day batch | **`state synthesis`** with verify column |
| Public copy | **`skill-write`** after verify — do not skip |

## Verification / Proof Standard

Do not call this complete unless:

- the input source, file, paste, URL, or archive path is named
- the output surface is named
- skipped steps are explicitly marked with a reason
- uncertainty, missing evidence, or unresolved source defects are stated
- claim tier and source class must be stated

Evidence to report:

- files touched or produced
- scripts or commands run
- source URLs, archive paths, or transcript identifiers used
- confidence downgrade, if any

If verification cannot be completed:

- state what was not verified
- stop before archive land, synthesis, publication, or promotion
- return a bounded partial result for operator review

## Sync

After editing the portable core:

```bash
python3 scripts/sync_portable_skills.py --verify
python3 scripts/validate_skills.py
```


## Cursor / strategy-codex instance

# News verify — strategy-codex appendix

| Topic | Path |
|-------|------|
| **Corpus tiers 1–4** (news-verify = tier **3** only) | [docs/source-lattice-beyond-the-repo.md § statecraft corpus tiers](../../../docs/source-lattice-beyond-the-repo.md#statecraft-corpus-tiers-strategy-codex) |
| **CIV-STATE news source registry (SSOT)** | [docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md](../../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md) — sub-tiers **3a/3b/3c** |
| Portable core | [skills/news-verify/SKILL.md](../../../skills/news-verify/SKILL.md) |
| Legacy alias | [skills/wire-verify/SKILL.md](../../../skills/wire-verify/SKILL.md) |
| General fact triage | [.cursor/skills/fact-check/SKILL.md](../fact-check/SKILL.md) |
| Strategy + verify gate | [DEFAULT-PATH.md](../../../docs/skill-work/work-strategy/DEFAULT-PATH.md) + [news-verify/SKILL.md](../news-verify/SKILL.md) |
| Statecraft intake | [.cursor/skills/statecraft-source-intake/SKILL.md](../statecraft-source-intake/SKILL.md) |
| Daily brief verify tokens | [docs/skill-work/work-strategy/daily-brief-template.md](../../../docs/skill-work/work-strategy/daily-brief-template.md) § Inbox paste target |
| Strategy inbox | [docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md](../../../codex/daily-strategy-inbox.md) |
| Notebook verify discipline | [docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md](../../../codex/NOTEBOOK-PREFERENCES.md) |
| Statecraft archive | [source-archive/statecraft/](../../../source-archive/statecraft/) |
| Iran native triangulation | [docs/skill-work/work-strategy/daily-brief-iran-watch.md](../../../docs/skill-work/work-strategy/daily-brief-iran-watch.md) |
| Native-language pass (all jurisdictions) | [docs/skill-work/work-strategy/daily-brief-native-international-pass.md](../../../docs/skill-work/work-strategy/daily-brief-native-international-pass.md) |
| Persia statecraft lane | [statecraft/persia/README.md](../../../statecraft/persia/README.md) |
| Rome / Holy See (CIV-STATE) | [NEWS-VERIFY-CIV-STATE-SOURCES.md § Rome](../../../docs/skill-work/work-strategy/NEWS-VERIFY-CIV-STATE-SOURCES.md#rome-lane-civ-state) · [ROME-PASS.md](../../../docs/skill-work/work-strategy/work-strategy-rome/ROME-PASS.md) |
| America statecraft lane | [statecraft/america/README.md](../../../statecraft/america/README.md) |
| China (PRC) statecraft lane | [statecraft/china/README.md](../../../statecraft/china/README.md) |
