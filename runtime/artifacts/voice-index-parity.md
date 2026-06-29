# Voice Index Parity Dashboard

Do not edit by hand. Regenerate:

```bash
python3 scripts/build_voice_index_registry.py
```

Terminology: [`voice-index-registry.md`](../../statecraft/voices/voice-index-registry.md).

_Generated at 2026-06-29T13:21:14Z_

## Summary

| Metric | Count |
| --- | ---: |
| Voices discovered | 33 |
| Listed in voices router | 33 |
| With primary voice index | 33 |
| With rebuild script | 26 |
| Parity pass | 26 |
| Parity warn | 7 |
| Parity fail | 0 |
| Broken links (total) | 0 |
| Documented exceptions | 10 |

## Voice registry

| Voice | Primary index | Builder | Eligible | Indexed | Parity | Exceptions | Status |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| aguilar | `statecraft/voices/aguilar/aguilar-index.md` | `scripts/build_aguilar_index.py` | 17 | 17 | pass | — | canonical |
| alkhorshid | `statecraft/voices/alkhorshid/alkhorshid-index.md` | `scripts/build_alkhorshid_guest_index.py` | 1 | 1 | pass | dialogue-works host channel (channel_slug dialogue-works, source-dialogue-works-*) excluded from guest-index parity; cross-host guest captures only (Nima on other hosts) | canonical |
| barnes | `statecraft/voices/barnes/barnes-index.md` | `scripts/build_barnes_index.py` | 23 | 23 | pass | — | canonical |
| baud | `statecraft/voices/baud/baud-index.md` | `scripts/build_baud_index.py` | 34 | 34 | pass | — | canonical |
| blumenthal | `statecraft/voices/blumenthal/blumenthal-index.md` | `scripts/build_blumenthal_index.py` | 8 | 8 | pass | — | canonical |
| crooke | `statecraft/voices/crooke/crooke-index.md` | — | 65 | 65 | warn | legacy YYYY-MM-DD-crooke.md dated filenames excluded; transcript-crooke.md and verify-crooke-* stubs excluded | canonical |
| davis | `statecraft/voices/davis/davis-index.md` | `scripts/build_davis_guest_index.py` | 6 | 6 | pass | daniel-davis host channel (channel_slug daniel-davis, source-daniel-davis-*) excluded from guest-index parity; guest-index eligible set mirrors build_davis_guest_index.is_guest() | canonical |
| diesen | `statecraft/voices/diesen/diesen-index.md` | `scripts/build_diesen_guest_index.py` | 3 | 3 | pass | glenn-diesen host channel (channel_slug glenn-diesen, source-glenn-diesen-*, source-diesen-*) excluded from guest-index parity; cross-host guest captures only (Glenn Diesen on other hosts) | canonical |
| freeman | `statecraft/voices/freeman/freeman-index.md` | `scripts/build_freeman_index.py` | 148 | 150 | pass | — | canonical |
| helmer | `statecraft/voices/helmer/helmer-index.md` | `scripts/build_helmer_index.py` | 16 | 18 | pass | — | canonical |
| hoh | `statecraft/voices/hoh/hoh-index.md` | `scripts/build_hoh_index.py` | 13 | 13 | pass | — | canonical |
| jermy | `statecraft/voices/jermy/jermy-index.md` | — | 12 | 15 | warn | — | canonical |
| jiang | `statecraft/voices/jiang/jiang-index.md` | `scripts/build_jiang_index.py` | 6 | 6 | pass | PH-owned filenames (source-game-theory-, source-gb-, source-predictive-history-, source-interviews-* except Sneako dual-index); Dialogue Works host rows about Jiang excluded (+1) | canonical |
| johnson | `statecraft/voices/johnson/johnson-index.md` | `scripts/build_johnson_index.py` | 110 | 110 | pass | — | canonical |
| karaganov | `statecraft/voices/karaganov/karaganov-index.md` | — | 7 | 10 | warn | reaction-tier source-ritter-* captures citing Karaganov token are not guest appearances | canonical |
| kent | `statecraft/voices/kent/kent-index.md` | `scripts/build_kent_index.py` | 15 | 15 | pass | support-tier panel rows may appear in index but are not primary guest corpus for parity warnings | canonical |
| krainer | `statecraft/voices/krainer/krainer-index.md` | `scripts/build_krainer_index.py` | 14 | 14 | pass | — | canonical |
| krapivnik | `statecraft/voices/krapivnik/krapivnik-index.md` | `scripts/build_krapivnik_index.py` | 10 | 10 | pass | — | canonical |
| macgregor | `statecraft/voices/macgregor/macgregor-index.md` | `scripts/build_macgregor_index.py` | 90 | 90 | pass | — | canonical |
| marandi | `statecraft/voices/marandi/marandi-index.md` | `scripts/build_marandi_index.py` | 72 | 72 | pass | — | canonical |
| martyanov | `statecraft/voices/martyanov/martyanov-index.md` | `scripts/build_martyanov_index.py` | 34 | 34 | pass | — | canonical |
| mate | `statecraft/voices/mate/mate-index.md` | — | 2 | 3 | warn | — | canonical |
| matlock | `statecraft/voices/matlock/matlock-index.md` | `scripts/build_matlock_index.py` | 5 | 5 | pass | — | canonical |
| mcgovern | `statecraft/voices/mcgovern/mcgovern-index.md` | — | 27 | 27 | warn | — | canonical |
| mearsheimer | `statecraft/voices/mearsheimer/mearsheimer-index.md` | `scripts/build_mearsheimer_index.py` | 95 | 95 | pass | — | canonical |
| mercouris | `statecraft/voices/mercouris/mercouris-index.md` | `scripts/build_mercouris_guest_index.py` | 44 | 45 | pass | alexander-mercouris host channel and source-alexander-mercouris-* excluded from guest-index parity; guest-index eligible set mirrors build_mercouris_guest_index.is_guest() | canonical |
| pape | `statecraft/voices/pape/pape-index.md` | `scripts/build_pape_index.py` | 72 | 72 | pass | verify-pape-* and x-pape-* stub captures excluded from guest parity; date-only source-pape-YYYY-MM-DD stubs unless Cyrus Janssen studio lane (+1) | canonical |
| parsi | `statecraft/voices/parsi/parsi-index.md` | — | 51 | 51 | warn | — | canonical |
| postol | `statecraft/voices/postol/postol-index.md` | `scripts/build_postol_index.py` | 5 | 5 | pass | — | canonical |
| ritter | `statecraft/voices/ritter/ritter-index.md` | — | 99 | 99 | warn | date-only source-ritter-YYYY-MM-DD stubs excluded from index parity; verify-ritter-* and ritter-rant-* prefixes excluded | canonical |
| sachs | `statecraft/voices/sachs/sachs-index.md` | `scripts/build_sachs_index.py` | 92 | 92 | pass | — | canonical |
| weichert | `statecraft/voices/weichert/weichert-index.md` | `scripts/build_weichert_index.py` | 14 | 14 | pass | — | canonical |
| wilkerson | `statecraft/voices/wilkerson/wilkerson-index.md` | `scripts/build_wilkerson_index.py` | 95 | 95 | pass | — | canonical |
