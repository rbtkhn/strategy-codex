**strategy-codex instance notes**

- Canonical archive root for this skill: [source-archive/statecraft](/C:/dev/strategy-codex/source-archive/statecraft)
- Batch invocation phrases this host should recognize:
  - `statecraft daily intake`
  - `statecraft daily intake / source-archive first`
- Deprecated compatibility surfaces that must **not** receive new captures:
  - [codex/years/2026/raw-input](/C:/dev/strategy-codex/codex/years/2026/raw-input)
  - [codex/years/2026/provenance](/C:/dev/strategy-codex/codex/years/2026/provenance)
- Primary neighboring families this skill should check before writing:
  - `Dialogue Works / Nima`
  - `Judging Freedom / Napolitano`
  - `Glenn Diesen`
  - `The Duran / Mercouris`

**Current live examples**

- Nima / Dialogue Works:
  - [source-archive/statecraft/2026-05-26/transcript-alkorshid-marandi-iran-opens-fire-on-american-fighter-jets-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-alkorshid-marandi-iran-opens-fire-on-american-fighter-jets-2026-05-26.md)
- Napolitano / Judging Freedom:
  - [source-archive/statecraft/2026-05-26/transcript-napolitano-freeman-israel-humiliates-itself-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-napolitano-freeman-israel-humiliates-itself-2026-05-26.md)
  - [source-archive/statecraft/2026-05-26/transcript-napolitano-mearsheimer-neocons-want-more-war-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-napolitano-mearsheimer-neocons-want-more-war-2026-05-26.md)
  - [source-archive/statecraft/2026-05-26/transcript-napolitano-crooke-fear-as-a-deterrent-to-war-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-napolitano-crooke-fear-as-a-deterrent-to-war-2026-05-26.md)
- Glenn Diesen:
  - [source-archive/statecraft/2026-05-26/youtube-glenn-diesen-lawrence-wilkerson-failing-to-adjust-to-a-multipolar-world-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/youtube-glenn-diesen-lawrence-wilkerson-failing-to-adjust-to-a-multipolar-world-2026-05-26.md)
- The Duran / Mercouris:
  - [source-archive/statecraft/2026-05-26/transcript-duran-mercouris-pressure-to-walk-away-from-a-good-iran-deal-2026-05-26.md](/C:/dev/strategy-codex/source-archive/statecraft/2026-05-26/transcript-duran-mercouris-pressure-to-walk-away-from-a-good-iran-deal-2026-05-26.md)

**Repo notes**

- `statecraft/` is downstream interpretation and control, not archive storage.
- Daily synthesis belongs on the `statecraft/` side, not in `source-archive/statecraft/`.
- For manual file creation or edits, use `apply_patch`.
- Prefer the closest same-family recent file as the pattern authority.
- When a transcript is already supplied in chat, this skill can proceed without YouTube fetching.
- In same-day batch mode, the minimum expected rebuild set is:
  - `source-archive/statecraft/YYYY-MM-DD/README.md`
  - `source-archive/statecraft/YYYY-MM.md`
  - `source-archive/statecraft/thread-index.md`
  - `source-archive/statecraft/stale-index-audit.md` only if the navigation builder touches it

**Preferred maintenance commands after skill edits**

```powershell
python scripts/sync_portable_skills.py --skill statecraft-source-intake
python scripts/sync_portable_skills.py --verify --skill statecraft-source-intake
python scripts/validate_skills.py
```
