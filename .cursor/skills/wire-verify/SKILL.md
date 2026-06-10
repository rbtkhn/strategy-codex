---
name: "wire-verify"
preferred_activation: "wire verify"
description: "Triage wire- and desk-reported facts in ingests and briefs before synthesis: extract media hooks, fence interpretation, score developing-story claims (supported/contradicted/unclear/contested), optional verify receipts. Triggers: wire verify, verify wires, verify tier, strategy + verify on breaking seams. Complements fact-check."
portable: true
version: "1.5.1"
tags:
  - "verification"
  - "statecraft"
  - "strategy"
  - "provenance"
portable_source: "skills-portable/wire-verify/SKILL.md"
synced_by: "sync_portable_skills.py"
---
# Wire verify

**Preferred activation:** **`wire verify`**, **`wire-verify`**, **`verify wires`**, or **`verify tier`** on a named ingest / brief / transcript batch.

**Scope:** Fast external check on **claims that entered through news wires, live desks, or attributed media** — especially when **second-hand inside a transcript** ("according to the New York Times…", "Axios says…", "Hebrew media reports…").

**Corpus tier (source-lattice):** Wire-verify grades **corpus tier 3 only** — current-events news / official. SSOT: [source-lattice § statecraft corpus tiers](../../../docs/source-lattice-beyond-the-repo.md#statecraft-corpus-tiers-strategy-codex) · registry [§ placement](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md#source-lattice-placement).

| Tier | Scope |
|------|--------|
| **1** Historical primary | Out of scope — civ-state primary-text acquisition |
| **2** Historical secondary | Out of scope — Durant, Gibbon, CIV-MEM, etc. |
| **3** Current-events news | **This skill** — sub-tiers **3a** (official), **3b** (major wire), **3c** (syndicated/social) |
| **4** Current-events commentary | Out of scope for wire grade — Mercouris, Diesen, Davis, landed transcripts |

**Not in scope (label, do not score as wire facts):**

- **Corpus tier 4** analyst **interpretation**, forecasting, or doctrine (escalation dominance, decoupling arcs, "what Iran wants").
- Operator opinion, predictions, moral frames.
- **Corpus tier 1–2** historical claims cited inside commentary.
- **Deep 3a pull** (full MFA readout, court filing, official PDF) beyond triage — escalate to **`fact check deep`** or lane-specific primary skills.

## Relationship to fact-check

| Skill | Role |
|-------|------|
| **fact-check** (host skill) | General triage on **any** checkable claim the operator names. |
| **wire-verify** (this skill) | **Scoped child:** auto-extract **wire hooks** from ingests/briefs, apply fact-check verdict discipline, add **developing-story** and **contested-wire** handling, optional **verify receipt** for archive/inbox. |

When the operator says **`fact check`** on wire-only material, you may run **either** skill; prefer **wire-verify** when the input is a **full ingest** or **live-desk batch** and the job is "grade the hooks before synthesis."

**Not a substitute for** campaign/newsletter lanes (**politics-massie**, **skill-write**). Stay **claim-neutral**.

## Lane

- Default **Think:** verdict table in chat; **no** repo edits unless the operator switches to **Ship** and names files.
- **Ship (explicit):** append **`verify:`** tails, **`editorial_note`** / **`source_note`** receipts on landed captures, or inbox lines — still **not** Record merge.

## When to invoke

- After **statecraft source intake** or **strategy ingest** on a **breaking** or **same-week** seam.
- Before **`statecraft daily synthesis`**, **`strategy` EOD compose**, or promoting a claim into **`days.md` Judgment**.
- When **`strategy + verify`** is named and the load-bearing rows are **wire-sourced**.
- When the operator asks to **wire-verify** specific seams (Apache, infiltration, Houthi statement, non-intercept, roster, counts).

## Pass modes (batch vs sub-hook)

| Mode | When | Hooks | Five-lane sweep |
|------|------|-------|-----------------|
| **Batch** (default) | Full ingest, day batch, matrix gate, pre-**`statecraft daily synthesis`** | Inventory all wire hooks in scope | **Full** — all five lanes; cite or **`-absent`** each |
| **Sub-hook** | Operator names **one claim** or narrow fork (e.g. "Iran intentional credit?", "America refute denial?") | 1–5 rows only; merge near-duplicates | **Combatant lanes required** (America · Persia when hook is bilateral); **PRC · Russia · Rome** = mesh-if-spoke — still run registry search, honest **`-absent`** + "searched, silent" note |

**Sub-hook law:** Do not skip the mesh line or **Confidence** / **Escalate** blocks because the question is narrow. Do not claim **full sweep** without the [execution checklist](#sweep-execution-checklist) below.

**Operator shorthand:** `wire verify — full mesh` = batch sweep on named seam; `wire verify — intent only` (or similar) = sub-hook; default to **sub-hook** when the message is a single yes/no fork.

## Wire hook detection

Scan for:

1. **Named outlets** — NYT, WSJ, Reuters, AP, Axios, BBC, CNN, NBC, CBS, Times of Israel, Haaretz, Ynet, Anadolu, Al-Monitor, etc.
2. **Institution quotes** — IDF, CENTCOM, Pentagon, IAEA, UNIFIL, IRNA-class (English syndication ≠ primary; see below).
3. **Transcript attribution** — "according to…", "reports say…", "my sources…", "we don't have confirmation yet."
4. **Developing-story markers** — "under investigation," "allegedly," "preliminary," "Hebrew media," conflicting US officials.

**High misstatement risk (prioritize):** casualty counts, **who** did **what**, **when**, **how many**, delegation **rosters/titles**, **mechanism** (SAM vs drone vs malfunction), **affiliation** (Hezbollah vs unknown terrorist), **first time since** claims.

## CIV-STATE sweep (every pass)

**Do not** close wire-verify on **English-only Western wires** alone when hooks are **regime- or institution-attributed**.

**Source registry (SSOT):** [WIRE-VERIFY-CIV-STATE-SOURCES.md](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md) — **corpus tier 3** per-lane outlet tables (**3a/3b/3c**; legacy T1/T2/T3), URLs, native-lang law, and verify tokens. **Do not** maintain parallel outlet lists in chat; extend the registry when a lane gains a new stable **3a**.

**Fixed lanes — search all five on every `wire verify` pass** (same story window as the hooks; **no topic triggers**):

| Lane | Repo surface | Registry | If lane silent in window |
|------|--------------|----------|---------------------------|
| **America** | `statecraft/america/` | [§ America](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md#america-lane) | `verify:america-lane-absent` |
| **Persia** | `statecraft/persia/` | [§ Persia](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md#persia-lane) | `verify:persia-lane-absent` |
| **China (PRC)** | `statecraft/china/` | [§ China](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md#china-lane-prc) | `verify:prc-lane-absent` |
| **Russia** | `statecraft/russia/` | [§ Russia](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md#russia-lane) | `verify:russia-lane-absent` |
| **Rome (Holy See)** | `work-strategy-rome/` | [§ Rome](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md#rome-lane-civ-state) | `verify:rome-lane-absent` |

**Daily-brief companions** (48h scan — not duplicate registries): [jd-vance-watch](../../../docs/skill-work/work-strategy/daily-brief-jd-vance-watch.md) · [iran-watch](../../../docs/skill-work/work-strategy/daily-brief-iran-watch.md) · [prc-watch](../../../docs/skill-work/work-strategy/daily-brief-prc-watch.md) · [putin-watch](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md) · [native-international-pass](../../../docs/skill-work/work-strategy/daily-brief-native-international-pass.md).

**Sweep law:**

- **All five lanes** every pass — cite **≥1** **3a/3b** when that lane commented on the seam; else **`-absent`** receipt + one-line note. **Silent skip forbidden** → `verify:triangulation-incomplete`.
- **Attribution:** facts attributed to a lane are **blocked at Supported** without that lane's receipt. Native lang when wording disputes: **`fa`** (Persia), **`zh`** (PRC), **`ru`** (Russia), **`it` / `es` / `fr` / `pt`** (Rome per registry).
- **Mesh:** non-combatant lanes (**PRC**, **Rome**) inform **framing** when combatant lanes contest; they **do not** override America/Persia attribution.
- **Lanes disagree** → **`Contested`** or **`Unclear`** — never flatten to one wire.
- **Commentator transcript** = **interpretation** unless paired to lane primaries.
- **Adjacent** (Israel, Oman): [registry § Adjacent](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md#adjacent-israel) — **outside** the five-lane sweep; add only when the hook names IDF/Oman/mediation.

Extended outlet names may appear in `research/repos/civilization_memory/.../IRAN–WAR–CHRONICLE.md`; the **registry** is the operator wire-verify SSOT.

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
| Commentator transcript | — | **tier 4** | Interpretation fence only — not wire grade |

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
4. **CIV-STATE sweep** — Per [pass mode](#pass-modes-batch-vs-sub-hook): run registry searches; complete [execution checklist](#sweep-execution-checklist). Record **lane** + **lang** on each cite. Lane absent → **`-absent`** token. If native primary not found in triage time on a wording row → **Unclear** + **Escalate** (`fact check deep` or operator native pull). Apply [attribution duel](#attribution-duel-subroutine) when denial/intent load-bears.
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
## Wire verify — <subject> (<date context>)

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
- Do not upgrade **commentator monologue** or **analyst essays** to wire grade without tagged sources.
- Do not collapse **Hebrew-media speculation** into confirmed IDF fact without Spokesperson alignment.
- Do not close a **batch** without the **five-lane CIV-STATE sweep** — cite or **`-absent`** per lane with [checklist](#sweep-execution-checklist) evidence.
- Do not mark **5/5 sweep** on a **sub-hook** pass unless all five lanes were actually searched; use **combatant+mesh** honestly.
- Do not satisfy **Persia-lane** receipt with **Araghchi X** or foreign-wire denial alone — escalate **`fa`** per registry.
- Do not grade **lane-attributed** facts from **another lane's** outlets alone (e.g. Tehran from CNN only; CENTCOM from IRNA only).
- Do not treat **PRC** or **Rome** as tie-breakers for combatant attribution.
- **Abstain** honestly; **Unclear** beats false precision on fast-moving desks.

## Related

- **[source-lattice-beyond-the-repo.md](../../../docs/source-lattice-beyond-the-repo.md#statecraft-corpus-tiers-strategy-codex)** — corpus tiers **1–4** (wire-verify = tier **3** only).
- **[WIRE-VERIFY-CIV-STATE-SOURCES.md](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md)** — per-lane wire source SSOT (America, Persia, China, Russia, Rome; **3a–3c**).
- **fact-check** (host skill) — general triage; native-primary discipline; **`fact check deep`** escalation.
- Host appendix — repo paths for inbox tokens, statecraft `source_note`, `strategy + verify` gate (Cursor install only).


## Cursor / grace-mar instance

# Wire verify — strategy-codex appendix

| Topic | Path |
|-------|------|
| **Corpus tiers 1–4** (wire-verify = tier **3** only) | [docs/source-lattice-beyond-the-repo.md § statecraft corpus tiers](../../../docs/source-lattice-beyond-the-repo.md#statecraft-corpus-tiers-strategy-codex) |
| **CIV-STATE wire source registry (SSOT)** | [docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md) — sub-tiers **3a/3b/3c** |
| Portable core | [skills-portable/wire-verify/SKILL.md](../../../skills-portable/wire-verify/SKILL.md) |
| General fact triage | [.cursor/skills/fact-check/SKILL.md](../fact-check/SKILL.md) |
| Strategy + verify gate | [.cursor/skills/skill-strategy/SKILL.md](../skill-strategy/SKILL.md) (Modes → **+ verify**) |
| Statecraft intake | [.cursor/skills/statecraft-source-intake/SKILL.md](../statecraft-source-intake/SKILL.md) |
| Daily brief verify tokens | [docs/skill-work/work-strategy/daily-brief-template.md](../../../docs/skill-work/work-strategy/daily-brief-template.md) § Inbox paste target |
| Strategy inbox | [docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) |
| Notebook verify discipline | [docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md](../../../docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md) |
| Statecraft archive | [source-archive/statecraft/](../../../source-archive/statecraft/) |
| Iran native triangulation | [docs/skill-work/work-strategy/daily-brief-iran-watch.md](../../../docs/skill-work/work-strategy/daily-brief-iran-watch.md) |
| Native-language pass (all jurisdictions) | [docs/skill-work/work-strategy/daily-brief-native-international-pass.md](../../../docs/skill-work/work-strategy/daily-brief-native-international-pass.md) |
| Persia statecraft lane | [statecraft/persia/README.md](../../../statecraft/persia/README.md) |
| Rome / Holy See (CIV-STATE) | [WIRE-VERIFY-CIV-STATE-SOURCES.md § Rome](../../../docs/skill-work/work-strategy/WIRE-VERIFY-CIV-STATE-SOURCES.md#rome-lane-civ-state) · [ROME-PASS.md](../../../docs/skill-work/work-strategy/work-strategy-rome/ROME-PASS.md) |
| America statecraft lane | [statecraft/america/README.md](../../../statecraft/america/README.md) |
| China (PRC) statecraft lane | [statecraft/china/README.md](../../../statecraft/china/README.md) |
| PRC 48h watch (neutral Iran-war triangulation) | [docs/skill-work/work-strategy/daily-brief-prc-watch.md](../../../docs/skill-work/work-strategy/daily-brief-prc-watch.md) |
| U.S. executive / VP watch | [docs/skill-work/work-strategy/daily-brief-jd-vance-watch.md](../../../docs/skill-work/work-strategy/daily-brief-jd-vance-watch.md) |
| Iran war source hierarchy (research) | [research/repos/civilization_memory/content/civilizations/PERSIA/IRAN–WAR–CHRONICLE.md](../../../research/repos/civilization_memory/content/civilizations/PERSIA/IRAN–WAR–CHRONICLE.md) |
| Work menu conventions | [docs/skill-work/work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md) |

## Repo defaults

- **Default lane:** Think (chat table). **Ship** only when the operator names files (`source_note`, `editorial_note`, inbox line, `days.md` **Links** — not **Judgment** without dated URLs).
- Run **after** transcript lands, **before** `statecraft daily synthesis` or EOD compose when breaking seams load-bear.
- Pair with **`strategy + verify`** when folding wire hooks into codex / strategy-notebook layers.
- **Every batch:** run the **five-lane CIV-STATE sweep** (America · Persia · PRC · Russia · Rome — cite or **`-absent`** per lane) per portable core § *CIV-STATE sweep (every pass)* — before `statecraft daily synthesis` or matrix promotion.
- **Sub-hook passes** (v1.5.0+): single-fork operator questions — combatant lanes + mesh; still emit minimum chat block + [sweep execution checklist](../../../skills-portable/wire-verify/SKILL.md#sweep-execution-checklist); do not fake 5/5 without searching.
- **Corpus tier law** (v1.5.1): grade **tier 3** only (**3a** official · **3b** wire · **3c** syndicated/social); **tier 4** commentary (archive transcripts, Mercouris/Diesen benches) = interpretation fence — not wire facts.

## `verify:` token vocabulary (extend daily-brief defaults)

Use on inbox lines, brief §1f rows, or archive YAML tails:

| Token | Meaning |
|-------|---------|
| `verify:wire-RSS` | RSS / live-desk wire; not state primary |
| `verify:wire-supported` | Wire-verify triage: supported |
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

Existing thread weaves use **wire-verify** informally for roster/title checks (e.g. delegation head misnames). This skill formalizes that habit: run **`wire verify`** on roster lines before promoting to **Links**.

## Escalation routes

| Need | Next skill / action |
|------|---------------------|
| Non-wire claim | **`fact check`** |
| Deeper primary pull | **`fact check deep`** (operator phrase) |
| Any wire hook (batch) | **Five-lane CIV-STATE sweep** per portable core — America · Persia · PRC · Russia · Rome (`fa`/`zh`/`ru`/Romance when wording load-bearing) |
| Narrow fork (sub-hook) | Portable core § *Pass modes* + *Attribution duel* — combatant lanes required; mesh lanes searched or **`-absent`** with registry note |
| Iran/PRC/Russia wording | Native primary per **fact-check** + `daily-brief-*-watch.md` |
| Full day batch | **`statecraft daily synthesis`** with verify column |
| Public copy | **`skill-write`** after verify — do not skip |

## Sync

After editing the portable core:

```bash
python3 scripts/sync_portable_skills.py --verify
python3 scripts/validate_skills.py
```
