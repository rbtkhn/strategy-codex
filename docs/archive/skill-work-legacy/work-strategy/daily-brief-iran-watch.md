# IRI - last 48 hours (Islamic Republic of Iran) (explicit daily brief route)

**Purpose:** Standing **operator WORK** slice for the daily brief: **Tehran's public lines and visible Iranian state activity** (presidency, **foreign ministry**, **IRNA** / major state-adjacent wires) in a **rolling 48-hour** window (not Record truth, not Voice knowledge).

**Relation to Islamabad lane:** [islamabad-operator-index.md](islamabad-operator-index.md), gap matrices, and `islamabad-framework*.md` capture **bargaining structure** and **U.S.-Iran** trade space. This hub is the **Iranian-state voice** pass, not a substitute for those frameworks; use **both** when the day is load-bearing on **pause**, **Hormuz**, **Lebanon**, or **nuclear** terms.

**News-verify SSOT:** Per-lane source tables for **`wire verify`** triangulation live in [WIRE-VERIFY-CIV-STATE-SOURCES.md](WIRE-VERIFY-CIV-STATE-SOURCES.md#persia-lane) (Persia lane); this watch is the **48h scan** companion, not a duplicate registry.

**When:** When the operator explicitly requests the **daily brief** or a **daily-brief refresh** in the [coffee skill](../../../.cursor/skills/coffee/SKILL.md) ecosystem (legacy **hey** still works): run the **web scan**, then write the **compact block** (bullets + URLs) into **section 1h** (`## 1h. IRI - last 48 hours (Islamic Republic of Iran)`) **in the daily brief file** after `generate_work_politics_daily_brief.py` (or when refreshing an existing today's file). Step 1 **coffee** does **not** run this scan automatically.

---

## What to cover

- **Foreign Ministry** statements, **readouts**, **calls**, and **summit** lines with **date/time (UTC if possible)**.
- **President's office** / **Supreme Leader**-channel statements when they move **negotiation**, **sanctions**, **regional**, or **maritime** framing in the window.
- **IRNA** / **Mehr** / **Tasnim** (attribute **state** versus **state-adjacent**) when they carry the **first** Iranian wording on a story Western wires summarize.
- If **nothing material** in 48h: one line - `"No major new IRI/MFA statements located in window; see ministry feed for minor items."`

## Canonical surfaces (bookmark)

| Surface | URL | Notes |
|--------|-----|-------|
| MFA - English | [en.mfa.ir](https://en.mfa.ir/) | Diplomatic wording; cross-check Persian root when terms matter |
| President (English) | [president.ir/en](https://president.ir/en) | Executive readouts |
| IRNA - English | [en.irna.ir](https://en.irna.ir/) | State news; label as such |
| Tasnim | [tasnimnews.com](https://www.tasnimnews.com/en) | Often faster on security/military lines; state-adjacent, tag tier |
| Reuters - Iran | [reuters.com/world/middle-east](https://www.reuters.com/world/middle-east/) | Cross-check time and paraphrase |

**Native-language triangulation:** When the **Iran** thread is load-bearing, add **at least one Persian (`fa`) primary line** (IRNA root, Tasnim FA, Fars, MFA Persian) per [daily-brief-native-international-pass.md](daily-brief-native-international-pass.md). This is not optional on active **Islamabad**, **Hormuz**, or **nuclear** crisis days.

## Guardrails

- **Cite URLs** for each bullet used in client-facing or posted material.
- **Do not** merge into SELF, EVIDENCE, or `archive/grace-mar-instance/bot/prompt.py` without the gated pipeline.
- **RSS section 2** of the daily brief may surface Iran-adjacent headlines; it **does not** replace this pass (timing, full quotes, Persian check).
- **Do not** treat Western "Iran" analysis or exile narratives as Tehran's position without **MFA / IRNA-class** alignment.

---

**Last procedure refresh:** 2026-04-12
