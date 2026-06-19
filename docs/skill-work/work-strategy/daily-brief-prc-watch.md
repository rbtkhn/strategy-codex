# PRC - last 48 hours (People's Republic of China) (explicit daily brief route)

**Purpose:** Standing **operator WORK** slice for the daily brief: **Beijing's public lines and visible PRC state activity** (party-state leadership, **MFA**, major ministries when relevant) in a **rolling 48-hour** window (not Record truth, not Voice knowledge).

**Wire-verify SSOT:** Per-lane source tables for **`wire verify`** triangulation live in [WIRE-VERIFY-CIV-STATE-SOURCES.md](WIRE-VERIFY-CIV-STATE-SOURCES.md#china-lane-prc) (PRC neutral lane); this watch is the **48h scan** companion, not a duplicate registry.

**When:** When the operator explicitly requests the **daily brief** or a **daily-brief refresh** in the [coffee skill](../../../.cursor/skills/coffee/SKILL.md) ecosystem (legacy **hey** still works): run the **web scan**, then write the **compact block** (bullets + URLs) into **section 1g** (`## 1g. PRC - last 48 hours (People's Republic of China)`) **in the daily brief file** after `generate_work_politics_daily_brief.py` (or when refreshing an existing today's file). Step 1 **coffee** does **not** run this scan automatically.

---

## What to cover

- **Foreign Ministry (MFA)** regular briefings, **readouts**, and **summits / calls** with **date/time (UTC if possible)**.
- **State Council / NDRC / commerce** lines when they move **trade**, **sanctions**, or **regional** framing in the window.
- **Cross-strait**, **South China Sea**, or **Russia-Iran-U.S.** stories only when **PRC** is a **named** party in the day's strategy thread; attribute to **official** text or **wire quoting MFA**.
- If **nothing material** in 48h: one line - `"No major new PRC/MFA statements located in window; see MFA regular briefing index for minor items."`

## Canonical surfaces (bookmark)

| Surface | URL | Notes |
|--------|-----|-------|
| MFA - press conferences / spokes | [fmprc.gov.cn](https://www.fmprc.gov.cn/) | Primary for diplomatic wording (EN / Chinese) |
| Xinhua (English) | [english.news.cn](http://www.news.cn/english/) | State news; label as such |
| PRC embassy / mission (when U.S.-China day) | mission-specific | Readouts, statements |
| Reuters - China | [reuters.com/world/china](https://www.reuters.com/world/china/) | Cross-check time and phrasing |
| Caixin Global / SCMP | independent HK/region English | Use with independence note versus state wire |

**Native-language triangulation:** When the **PRC** thread is load-bearing, add **at least one Mandarin-primary line** (MFA Chinese, Xinhua Chinese, People's Daily as needed) per [daily-brief-native-international-pass.md](daily-brief-native-international-pass.md); this is not optional for full section 1g passes on active **U.S.-China**, **cross-strait**, or **Indo-Pacific** crisis days.

## Guardrails

- **Cite URLs** for each bullet used in client-facing or posted material.
- **Do not** merge into SELF, EVIDENCE, or `archive/grace-mar-instance/bot/prompt.py` without the gated pipeline.
- **RSS section 2** of the daily brief may surface China-adjacent headlines; it **does not** replace this pass (timing, full MFA quotes, bilingual check).
- **Do not** treat Western "China hawk" analysis as Beijing's position without **MFA / state** alignment.

---

**Last procedure refresh:** 2026-04-12
