---
name: fact-check
preferred_activation: fact check
description: >-
  Triage-first fact check: fast web pass on operator-pasted claims with lean verdicts (supported / contradicted / unclear / out of scope),
  one solid cite per claim when possible, high abstention; include native/foreign-language official sources (e.g. Persian, Chinese, Russian) when claims are regime- or institution-attributed. Escalation flags when deeper audit is needed. Not Record merge unless gated.
---

# Fact check (operator)

**Preferred activation (operator):** say the exact phrase **`fact check`**. **Aliases:** **`verify this`**, **`check this claim`**.

**Default mode — triage (v1):** **fast pre-flight**, not a research memo. Prefer **one good source** + honest **Unclear** when the web is thin or noisy. When triage is insufficient, escalate to **[Deep pass](#fact-check-deep-pass)** (`fact check deep`) — do not stretch triage into a memo.

Use when the operator wants a **quick external sanity check** on something **they paste or name** — a sentence, stat, quote attribution, URL summary, or draft line — before shipping, teaching, or archiving.

**Not a substitute for** [politics-massie](../politics-massie/SKILL.md) (breaking-news hooks + `@usa_first_ky` drafts). Use **fact check** for **neutral verification**; use **massie x** when the goal is **campaign-shaped** copy from today's news.

<a id="verification-routing-shared"></a>

## Verification routing (shared — fact-check ↔ wire-verify)

**SSOT:** identical block in this file and [wire-verify](../wire-verify/SKILL.md#verification-routing-shared). Update **both** when routing law changes.

Use this table **before** choosing a pass. Bare **`verify`** is ambiguous — ask once or infer from **input shape**.

| Operator input | Route | Why |
| --- | --- | --- |
| **One claim** pasted or named (sentence, stat, quote, URL summary, draft line) | **`fact check`** (this skill) | Discrete triage; operator supplies the claim |
| **Full ingest**, day archive, daily brief, or **wire matrix** | **[wire-verify](../wire-verify/SKILL.md)** | Auto-extract tier-**3** hooks; five-lane sweep; optional `verify:` receipts |
| **`fact check`** on a **wire-heavy capture** but job is "grade hooks before synthesis" | **wire-verify** (prefer) | Batch hook inventory + developing-story handling |
| **Single fork** from a matrix row ("is J17-7 supported?") | **wire-verify** sub-hook **or** **fact check** | Sub-hook when lane-sweep context matters; fact-check when the claim is isolated |
| **Analyst voice** (Mercouris, Diesen, Davis, landed commentary) stating mechanism, forecast, or doctrine | **Label tier 4 / interpretation** — **do not score as wire fact** | Corpus tier 4; synthesis may use; verification does not grade |
| **Historical** primary/secondary cited inside commentary | **Out of scope** for wire-verify; **fact check** only if operator names the historical claim | Corpus tiers 1–2 |
| **Primary doc** needed (full MFA readout, court filing, official PDF) beyond triage | **[fact check deep](#fact-check-deep-pass)** (or lane primary skill) | Escalate from wire-verify or thin fact-check triage |
| **Campaign / Massie-shaped** copy from today's news | **[politics-massie](../politics-massie/SKILL.md)** | Not neutral verification |
| **Before** `state synthesis` or promoting into Judgment on a **same-week** seam | **wire-verify** (batch mode) | Pre-synthesis gate on wire hooks |

**Verdict vocabulary (align across skills):**

| fact-check | wire-verify | Meaning |
| --- | --- | --- |
| Supported | supported | Corroborated within pass budget |
| Contradicted | contradicted | Clear counter-evidence |
| Unclear | unclear | Thin, noisy, or not locatable in triage time |
| Out of scope | *(label only)* | Prediction, opinion, tier 4 — not a wire row |
| — | contested | Credible sources conflict |
| — | partial | Some elements supported; hook incomplete |

**Ambiguity rule:** If both a **named claim** and a **full ingest path** appear, prefer **wire-verify** when the ingest is the primary object; prefer **fact check** when only the claim matters and archive context is optional.

## Lane

- Default **Think**: answer in the thread with **citations**; **no** repo edits, merge, stage, or gate writes unless the operator switches to **Ship** and names files.
- If the operator asks to **draft a gate candidate** or **edit a doc**, treat that as explicit **Ship** scope for that turn only.

## Procedure (triage)

1. **Isolate claims** — List **discrete** checkable statements (who / what / when / how many). Merge near-duplicates. If the prompt is vague, ask **one** narrowing question **or** state your assumption in one line — do not block on back-and-forth.
2. **Classify each claim**
   - **Factual** (empirically checkable).
   - **Interpretive** — label **interpretation**; do not score as Supported/Contradicted without marking it as inference.
   - **Out of scope** — prediction, pure opinion, privileged access — **Out of scope**; no fake certainty.
3. **Search and cite (light)** — One **credible** source per factual claim is enough for **triage** (reputable outlet, official page, or primary doc if it surfaces quickly). Add a **second** source **only** if the claim is **obviously contested**, **high-stakes** (election / legal / medical / financial / attribution of a quote), or the first source is weak/unclear.

**Native / foreign-language primaries (strategy-adjacent — when claims are about non-U.S. governments or multilateral institutions):** Do **not** rely on **English-only** syndication if the verdict turns on **what Tehran, Beijing, Moscow, or the Holy See actually said**. Prefer, when discoverable in triage time: **official MFA / presidency / IRNA-class** pages in **Persian (fa)** for Iran; **MFA / state** readouts in **Chinese (zh)** for PRC; **Kremlin** / key ministries in **Russian (ru)** for Russia; **Vatican** / **Holy See** primaries per [ROME-PASS.md](../../../docs/skill-work/work-strategy/work-strategy-rome/ROME-PASS.md) for Rome-dependent claims. Use **reputable wire English summaries** as **supporting** evidence, not automatic substitutes for the native line when the dispute is **wording** or **scope**. If you cannot read the language, say so — **machine translation + official URL** is still better than guessing; flag **Unclear** and **Escalate** when only partisan secondary sources appear. Repo guardrails: [daily-brief-iran-watch.md](../../../docs/skill-work/work-strategy/daily-brief-iran-watch.md) (Persian triangulation), [daily-brief-prc-watch.md](../../../docs/skill-work/work-strategy/daily-brief-prc-watch.md), [daily-brief-putin-watch.md](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md).
4. **Verdict table (lean)** — For each **factual** claim:

   | Claim (short) | Verdict | Source (title + URL) |
   |---------------|---------|----------------------|
   | … | **Supported** / **Contradicted** / **Unclear** / **Out of scope** | … |

   One-line **caveat** under the table if dates, geography, or "developing story" matter.

5. **Interpretations** (if any) — **Three bullets max** — what is **speculation** vs what the cited material **actually says**.
6. **Confidence** — **One line** after the table: **low / medium / high** for triage purposes only, plus **one** phrase on what would raise it (e.g. "pull roll-call vote," "original press release").
7. **Escalation (required when applicable)** — If triage is **insufficient**, append a short **Escalate** block: **why** (stakes, conflict, no primary found) + **offer or run** [Deep pass](#fact-check-deep-pass) when the operator agrees or said **`fact check deep`**. Do **not** pretend triage was enough when it was not.

<a id="fact-check-deep-pass"></a>

## Procedure (deep pass)

**Activation:** **`fact check deep`**, **`deep fact check`**, or explicit acceptance after a triage **Escalate** block. **wire-verify** routes here for **tier-3a primary** pulls (full MFA readout, court filing, official PDF, treaty text) that exceed wire triage budget — see [wire-verify capture-gap](../wire-verify/SKILL.md#capture-gap-pre-pass) when the blocker is **missing archive body**, not missing sources.

### When to use deep pass

| Use deep | Stay on triage or route elsewhere |
| --- | --- |
| Wording/scope turns on **official primary** (MFA, Kremlin, Vatican, OFAC bulletin) | Tier-4 **analyst interpretation** — label only |
| Triage returned **Unclear** but claim is **high-stakes** (attribution, legal, election, casualty count, treaty clause) | **Capture-gap** — complete archive first; deep cannot score absent transcript |
| **Two credible wires conflict** and primary would break tie | Full ingest hook inventory — **wire-verify** batch/sub-hook |
| Operator names **one claim** and wants **primary + one independent** | Campaign copy — **politics-massie** |
| **Historical primary** (tier 1–2) — operator names the document/period | Open-ended research with no named claim |

### Depth budget (operator time)

Deep pass is **bounded audit**, not unlimited investigation.

- **Default ceiling:** up to **~15 minutes** agent time; **≤3 factual claims** per pass unless operator expands scope.
- **Source ladder per claim:** (1) **primary** official or filing when discoverable → (2) **second independent** reputable line → (3) reputable wire **supporting only**.
- **Stop rule:** If primary is not locatable after reasonable search, verdict stays **Unclear** with **documented search path** — do not fabricate certainty.

### Procedure

1. **Inherit or isolate** — Carry forward triage claim list **or** restate the operator's named claim in one line each. Merge near-duplicates.
2. **Classify stakes** — One line: why triage failed (wording dispute, conflict, no primary, developing story).
3. **Primary pull (required when regime-attributed)** — Same native-language law as triage: **fa / zh / ru / Vatican** primaries when the dispute is **what the institution said**. Cite **URL + date + excerpt anchor** (heading, paragraph, or PDF page). Machine translation allowed with **flag**.
4. **Independent second line** — Different institution or outlet family than the first; not two syndications of the same pool.
5. **Verdict table (deep)** — Extend triage columns:

   | Claim | Verdict | Primary | Supporting | Residual risk |
   | --- | --- | --- | --- | --- |
   | … | Supported / Contradicted / Unclear / Out of scope | … | … | one line |

   Use **Contested** in prose when primaries conflict and tie is not broken.

6. **Interpretations** — Separate block; still **not** scored as Supported without label.
7. **Confidence** — **low / medium / high** with explicit **what would falsify** or **what doc is still missing**.
8. **Handoff** — If result should live on archive: offer **Ship** footnote (`verify:` tail, matrix row upgrade) — **not** automatic repo edit.

### Relationship to wire-verify

| From | To deep when |
| --- | --- |
| **wire-verify** triage | Hook needs **3a primary** beyond desk sweep |
| **wire-verify** capture-gap | **Archive completion** first — not deep |
| **wire-verify** sub-hook | Operator wants primary on **one matrix fork** — deep OK if claim isolated |

Deep pass **does not** replace wire-verify's **five-lane sweep** on a full day batch unless the operator narrows to named claim(s).

### Related skills (do not duplicate)

- **[wire-verify](../wire-verify/SKILL.md)** — batch/sub-hook on ingests and matrices.
- **[civ-state-primary-text-acquisition](../civ-state-primary-text-acquisition/SKILL.md)** — sustained tier-1–2 corpus work, not same-week wire hooks.
- Lane watches — [iran-watch](../../../docs/skill-work/work-strategy/daily-brief-iran-watch.md), [prc-watch](../../../docs/skill-work/work-strategy/daily-brief-prc-watch.md), [putin-watch](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md).

### Guardrails (deep)

- Still **not Record** — citations in thread or named doc footnotes only unless gated.
- **No leakage** — training-data recall is not a primary.
- Legal / medical / financial: deep may still end **Unclear** — name **human professional** when appropriate.

## Guardrails (Grace-Mar)

- **Knowledge boundary:** Assistant + web output is **not** [Record](../../../self.md) truth. Nothing here **enters** SELF, EVIDENCE, or `bot/prompt.py` without companion approval through **RECURSION-GATE** and `process_approved_candidates.py`. See [AGENTS.md](../../../AGENTS.md) and [knowledge-boundary-framework.md](../../../docs/knowledge-boundary-framework.md).
- **No leakage:** Do not present training-data "facts" as checks. Cite **what you found** and **where**.
- **Lexile / Voice:** If output is **for the Voice** or **child-facing**, stay within instance **Lexile** (grace-mar: **600L** unless raised with evidence) and **no** undocumented biographical claims.
- **Election / legal / medical / financial:** Default **Unclear** or **Escalate** unless a **strong** primary or two clear independents surfaced quickly — say when a **human professional** is the right next step.

## WORK lane

If the thread is clearly **WORK** and the operator did not say **no menu**, end with **3–5 labeled next-step options** (e.g. run a deeper pass later, tighten one sentence for posting, pivot to **massie x**, add a doc footnote under **Ship**). Otherwise skip the menu.

## Related

- [wire-verify](../wire-verify/SKILL.md) — scoped pass on **wire/desk hooks** inside ingests and briefs before synthesis; escalates **3a primary** work to [Deep pass](#fact-check-deep-pass). Routing: [Verification routing (shared)](#verification-routing-shared).
- [politics-massie](../politics-massie/SKILL.md) — news hooks + X drafts for the Massie analysis lane.
- **Massie news hooks:** If your Cursor install includes **massie-x-news-search-draft** (optional user skill), use it for **today's** KY-4 / Massie-relevant cited briefs; **fact check** stays **claim-neutral**.
- [pros-and-cons](../pros-and-cons/SKILL.md) — tradeoffs when the question is **should we**, not **is it true**.

