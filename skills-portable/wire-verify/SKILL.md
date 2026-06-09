---
name: wire-verify
preferred_activation: wire verify
description: "Triage wire- and desk-reported facts in ingests and briefs before synthesis: extract media hooks, fence interpretation, score developing-story claims (supported/contradicted/unclear/contested), optional verify receipts. Triggers: wire verify, verify wires, verify tier, strategy + verify on breaking seams. Complements fact-check."
portable: true
version: 1.0.0
tags:
  - verification
  - statecraft
  - strategy
  - provenance
---

# Wire verify

**Preferred activation:** **`wire verify`**, **`wire-verify`**, **`verify wires`**, or **`verify tier`** on a named ingest / brief / transcript batch.

**Scope:** Fast external check on **claims that entered through news wires, live desks, or attributed media** — especially when **second-hand inside a transcript** ("according to the New York Times…", "Axios says…", "Hebrew media reports…").

**Not in scope (label, do not score as wire facts):**

- Analyst **interpretation**, forecasting, or doctrine (escalation dominance, decoupling arcs, "what Iran wants").
- Operator opinion, predictions, moral frames.
- **Primary-source acquisition** (full MFA readout, court filing, official PDF) — escalate to **`fact check deep`** or lane-specific primary skills.

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

## Wire hook detection

Scan for:

1. **Named outlets** — NYT, WSJ, Reuters, AP, Axios, BBC, CNN, NBC, CBS, Times of Israel, Haaretz, Ynet, Anadolu, Al-Monitor, etc.
2. **Institution quotes** — IDF, CENTCOM, Pentagon, IAEA, UNIFIL, IRNA-class (English syndication ≠ primary; see below).
3. **Transcript attribution** — "according to…", "reports say…", "my sources…", "we don't have confirmation yet."
4. **Developing-story markers** — "under investigation," "allegedly," "preliminary," "Hebrew media," conflicting US officials.

**High misstatement risk (prioritize):** casualty counts, **who** did **what**, **when**, **how many**, delegation **rosters/titles**, **mechanism** (SAM vs drone vs malfunction), **affiliation** (Hezbollah vs unknown terrorist), **first time since** claims.

## Procedure

1. **Inventory hooks** — List discrete wire-attributed claims (merge near-duplicates). One row per checkable fact.
2. **Fence interpretation** — Move speaker/analyst frames to an **Interpretation** block (max three bullets). Do not verdict-score them as Supported/Contradicted.
3. **Classify story state**
   - **Developing** — cause/mechanism/count still moving; note **interview/publication time** if transcript predates later wires.
   - **Settled** — multiple independents align; official statement landed.
   - **Contested** — credible outlets disagree (e.g. "did not intercept" vs "fired interceptors in self-defense").
4. **Search (triage)** — One solid cite per claim; second cite when **contested** or **high-stakes**. Prefer: official readout > wire > syndicated blog. For **regime wording disputes**, prefer native-language primaries when discoverable (see fact-check § native primaries); otherwise **Unclear** + Escalate.
5. **Verdict table**

   | Claim (short) | Wire source cited | Verdict | Cite (title + URL) |
   |---------------|-------------------|---------|---------------------|
   | … | NYT / Axios / … | **Supported** / **Contradicted** / **Unclear** / **Contested** / **Out of scope** | … |

   **Contested** = two credible lines disagree; state both in one row or split sub-rows.

6. **Developing-story caveat** — One line under the table when timing matters ("Nawfal aired while cause **under investigation**; later Trump/Axios pointed to **drone**.").
7. **Confidence** — One line: low / medium / high + what would raise it (CENTCOM release, IDF Spokesperson Hebrew, primary Houthi Arabic statement).
8. **Escalate (if needed)** — Primary pull list; say **`fact check deep`** when beyond triage.

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

```markdown
## Wire verify — <subject> (<date context>)

**Hooks checked:** N · **Developing:** yes/no · **Confidence:** medium

| Claim | Verdict | Cite |
|-------|---------|------|

**Developing-story caveat:** …

**Interpretation (not wire-verified):**
- …

**Escalate:** …
```

## Guardrails

- Assistant + web output is **not** Record truth. Cite what you found and where.
- Do not upgrade **commentator monologue** or **analyst essays** to wire grade without tagged sources.
- Do not collapse **Hebrew-media speculation** into confirmed IDF fact without Spokesperson alignment.
- **Abstain** honestly; **Unclear** beats false precision on fast-moving desks.

## Related

- **fact-check** (host skill) — general triage; native-primary discipline; **`fact check deep`** escalation.
- Host appendix — repo paths for inbox tokens, statecraft `source_note`, `strategy + verify` gate (Cursor install only).
