**strategy-codex instance notes**

- Canonical archive root for this skill: [source-archive/statecraft](/C:/dev/strategy-codex/source-archive/statecraft)
- Primary manual activation: **`source-intake`**
- Batch invocation phrases this host should recognize:
  - `source-intake`
  - `statecraft source intake`
  - `statecraft daily intake`
  - `statecraft daily intake / source-archive first`
- Deprecated compatibility surfaces that must **not** receive new captures:
  - [codex/raw-input/README.md](/C:/dev/strategy-codex/codex/raw-input/README.md) — [RAW-INPUT-DEPRECATED.md](/C:/dev/strategy-codex/docs/skill-work/work-strategy/RAW-INPUT-DEPRECATED.md)
  - [codex/years/2026/raw-input](/C:/dev/strategy-codex/codex/years/2026/raw-input)
  - [codex/years/2026/provenance](/C:/dev/strategy-codex/codex/years/2026/provenance)
- Primary neighboring families this skill should check before writing:
  - `Dialogue Works / Nima`
  - `Judging Freedom / Napolitano`
  - `Glenn Diesen`
  - `The Duran / Mercouris`

**Current live examples**

- Nima / Dialogue Works:
  - [source-archive/statecraft/2026-05-26/source-alkorshid-marandi-iran-opens-fire-on-american-fighter-jets-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/source-alkorshid-marandi-iran-opens-fire-on-american-fighter-jets-2026-05-26.md)
- Napolitano / Judging Freedom:
  - [source-archive/statecraft/2026-05-26/source-napolitano-freeman-israel-humiliates-itself-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/source-napolitano-freeman-israel-humiliates-itself-2026-05-26.md)
  - [source-archive/statecraft/2026-05-26/source-napolitano-mearsheimer-neocons-want-more-war-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/source-napolitano-mearsheimer-neocons-want-more-war-2026-05-26.md)
  - [source-archive/statecraft/2026-05-26/source-napolitano-crooke-fear-as-a-deterrent-to-war-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/source-napolitano-crooke-fear-as-a-deterrent-to-war-2026-05-26.md)
- Glenn Diesen:
  - [source-archive/statecraft/2026-05-26/source-glenn-diesen-lawrence-wilkerson-failing-to-adjust-to-a-multipolar-world-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/source-glenn-diesen-lawrence-wilkerson-failing-to-adjust-to-a-multipolar-world-2026-05-26.md)
- The Duran / Mercouris:
  - [source-archive/statecraft/2026-05-26/source-duran-mercouris-pressure-to-walk-away-from-a-good-iran-deal-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/source-duran-mercouris-pressure-to-walk-away-from-a-good-iran-deal-2026-05-26.md)

**Repo notes**

- `statecraft/` is downstream interpretation and control, not archive storage.
- Daily synthesis belongs on the `statecraft/` side, not in `source-archive/statecraft/`.
- For manual file creation or edits, use `apply_patch` for **small** captures; for large operator-pasted transcript bodies and **Mercouris solo** lands, prefer **`python scripts/land_statecraft_intake.py`** (one-command header + chunked merge + post-land). Manual fallback when the header is already built: **`python scripts/land_statecraft_source_body.py`** (§ Large transcript body land in the portable core).
- Prefer the closest same-family recent file as the pattern authority.
- When a transcript is already supplied in chat, this skill can proceed without YouTube fetching.
- **Post-land optional:** [wire-verify](../wire-verify/SKILL.md) — **`wire verify`** on breaking wire hooks; land **`verify:`** tails in `source_note` / `editorial_note` when operator ships receipts.
- In same-day batch mode, the minimum expected rebuild set is:
  - `source-archive/statecraft/YYYY-MM-DD/day-index.md` (+ README stub via `build_statecraft_day_indices.py --day`)
  - `source-archive/statecraft/YYYY-MM.md`
  - `source-archive/statecraft/thread-index.md`
  - `source-archive/statecraft/stale-index-audit.md` only if the navigation builder touches it

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill statecraft-source-intake
python scripts/sync_portable_skills.py --verify --skill statecraft-source-intake
python scripts/validate_skills.py
```
