# Statecraft Metadata Normalization Audit

_Generated audit artifact for read-time host/guest normalization._

- Generated: `2026-06-05T05:24:15.715503+00:00`
- Root: `C:\dev\strategy-codex\source-archive\statecraft`
- Scanned files: `1546`

## Top Host Rewrites

| Rewrite | Count |
| --- | ---: |
| `Judge Andrew Napolitano -> Andrew Napolitano` | 99 |
| `Nima Alkhorshid -> Nima Alkhorshid` | 28 |
| `Dialogue Works -> Nima Alkhorshid` | 18 |
| `Nema -> Nima Alkhorshid` | 15 |
| `glenn-diesen -> Glenn Diesen` | 8 |
| `Daniel Davis / Deep Dive -> Daniel Davis` | 6 |
| `daniel-davis -> Daniel Davis` | 6 |
| `Lt Col Daniel Davis -> Daniel Davis` | 4 |
| `Nima -> Nima Alkhorshid` | 3 |
| `Nima R. Alkhorshid -> Nima Alkhorshid` | 3 |
| `Clayton Morris, Natali Morris -> Clayton Morris` | 2 |
| `Clayton Morris, Natali Morris -> Natali Morris` | 2 |
| `Alex Christoforu -> Alex Christoforou` | 1 |
| `Clayton Morris; Natali Morris -> Clayton Morris` | 1 |
| `Clayton Morris; Natali Morris -> Natali Morris` | 1 |
| `Cyrus Janssen; Alex Reporterfy (Reporterfy Media) -> Alex Reporterfy (Reporterfy Media)` | 1 |
| `Cyrus Janssen; Alex Reporterfy (Reporterfy Media) -> Cyrus Janssen` | 1 |
| `Daniel Davis (host); Col. Jacques Baud (guest) -> Daniel Davis` | 1 |
| `Daniel Davis (host); Col. Jacques Baud (guest) -> Jacques Baud (guest)` | 1 |
| `Judge Andrew Napolitano; Larry Johnson -> Andrew Napolitano` | 1 |

## Top Guest Rewrites

| Rewrite | Count |
| --- | ---: |
| `Col. Jacques Baud -> Jacques Baud` | 19 |
| `Col. Larry Wilkerson -> Lawrence Wilkerson` | 19 |
| `Col. Lawrence Wilkerson -> Lawrence Wilkerson` | 19 |
| `john-mearsheimer -> John Mearsheimer` | 18 |
| `Col. Douglas Macgregor -> Douglas Macgregor` | 13 |
| `Larry Wilkerson -> Lawrence Wilkerson` | 11 |
| `alexander-mercouris -> Alexander Mercouris` | 7 |
| `Larry C. Johnson; Col. Larry Wilkerson -> Larry C. Johnson` | 6 |
| `Larry C. Johnson; Col. Larry Wilkerson -> Lawrence Wilkerson` | 6 |
| `Lt. Col. Anthony Aguilar -> Anthony Aguilar` | 5 |
| `Col Doug Macgregor -> Doug Macgregor` | 4 |
| `Larry Johnson & Col. Wilkerson -> Larry Johnson` | 4 |
| `Larry Johnson & Col. Wilkerson -> Lawrence Wilkerson` | 4 |
| `Amb. Chas Freeman -> Chas Freeman` | 3 |
| `Colonel Lawrence Wilkerson -> Lawrence Wilkerson` | 3 |
| `Larry C. Johnson & Col. Larry Wilkerson -> Larry C. Johnson` | 3 |
| `Larry C. Johnson & Col. Larry Wilkerson -> Lawrence Wilkerson` | 3 |
| `Chas Freeman & Mohammad Marandi -> Chas Freeman` | 2 |
| `Chas Freeman & Mohammad Marandi -> Mohammad Marandi` | 2 |
| `Lt Col Daniel Davis -> Daniel Davis` | 2 |

## Dropped Guest Fragments

| Rewrite | Count |
| --- | ---: |
| `exact-title-match` | 13 |
| `Jeffrey Sachs` | 3 |
| `host-only-title-match` | 2 |
| `Scott Ritter` | 1 |
| `pepe_escobar` | 1 |
| `title-known-speaker-match` | 1 |

## Structured Field Presence

| Rewrite | Count |
| --- | ---: |
| `any_structured_fields` | 38 |
| `channel_name` | 38 |
| `host_people` | 38 |
| `show_and_channel_complete` | 38 |
| `show_title` | 31 |
| `guest_people` | 25 |

## Missing Structured Field Combos

| Rewrite | Count |
| --- | ---: |
| `missing_host_people` | 1320 |
| `missing_channel_name` | 1277 |
| `missing_show_title` | 1144 |
| `missing_guest_people` | 972 |

## Field-Boundary Failure Classes

- `person-host-shares-show-identity`: `host` (281)
  Host examples: `Alexander Mercouris` (117), `Glenn Diesen` (106), `Jeffrey Sachs` (22), `Mario Nawfal` (20), `Diesen` (12)
- `title-fragment-as-guest`: `guest` (98)
  Guest examples: `John Helmer` (4), `Jiang Xueqin` (3), `Matthew Hoh` (3), `Pepe Escobar` (3), `Deep Dive Intel Briefing` (2)
- `slug-person-field`: `guest` (41), `host` (14)
  Host examples: `glenn-diesen` (8), `daniel-davis` (6)
  Guest examples: `john-mearsheimer` (18), `exact-title-match` (13), `alexander-mercouris` (7), `host-only-title-match` (2), `title-known-speaker-match` (1)
- `compound-person-field`: `guest` (40), `host` (6)
  Host examples: `Clayton Morris, Natali Morris` (2), `Clayton Morris; Natali Morris` (1), `Cyrus Janssen; Alex Reporterfy (Reporterfy Media)` (1), `Daniel Davis (host); Col. Jacques Baud (guest)` (1), `Judge Andrew Napolitano; Larry Johnson` (1)
  Guest examples: `Larry C. Johnson; Col. Larry Wilkerson` (6), `Larry Johnson & Col. Wilkerson` (4), `Larry C. Johnson & Col. Larry Wilkerson` (3), `Chas Freeman & Mohammad Marandi` (2), `Alex Christoforou, Alexander Mercouris` (1)
- `channel-label-in-host-field`: `host` (16)
  Host examples: `Dialogue Works` (13), `Garland Nixon` (1), `Moral Resistance` (1), `Shaun Attwood` (1)
- `unresolved-guest-fragment`: `guest` (5)
  Guest examples: `Jeffrey Sachs` (3), `Scott Ritter` (1), `pepe_escobar` (1)
- `multi-role-mixed-field`: `host` (1)
  Host examples: `Daniel Davis (host); Col. Jacques Baud (guest)` (1)

## Guest Variant Families

- `Chas Freeman`: `Chas Freeman` (104), `Amb. Chas Freeman` (3), `Chas Freeman & Mohammad Marandi` (2)
- `Lawrence Wilkerson`: `Col. Larry Wilkerson` (19), `Col. Lawrence Wilkerson` (19), `Lawrence Wilkerson` (18), `Larry Wilkerson` (11), `Larry C. Johnson; Col. Larry Wilkerson` (6), `Larry Johnson & Col. Wilkerson` (4), `Colonel Lawrence Wilkerson` (3), `Larry C. Johnson & Col. Larry Wilkerson` (3), `Col. Larry Wilkerson; Scott Ritter` (1), `Israel is in Total Disarray | Alex Krainer & Col. Larry Wilkerson` (1), `Larry C. Johnson; Larry Wilkerson` (1), `Larry C. Johnson; Lawrence Wilkerson` (1), `Ret. Col. Lawrence Wilkerson` (1), `Scott Ritter; Larry Wilkerson` (1), `The US Strategy That's Failing Spectacularly | Col. Larry Wilkerson` (1), `Trump's Weakness Spells Disaster | Col. Larry Wilkerson & Scott Ritter` (1)
- `John Mearsheimer`: `John Mearsheimer` (65), `john-mearsheimer` (18), `John Mearsheimer, Alexander Mercouris` (1)
- `Jeffrey Sachs`: `Jeffrey Sachs` (80), `Professor Jeffrey Sachs` (2), `Jeffrey Sachs, Yakov Rabkin, Manuel Ramos` (1)
- `Scott Ritter`: `Scott Ritter` (75), `Andrei Martyanov & Scott Ritter` (1), `Col. Larry Wilkerson; Scott Ritter` (1), `Israel's Worst Nightmare Coming | Prof. Mohammad Marandi & Scott Ritter` (1), `Scott Ritter & Andrei Martyanov` (1), `Scott Ritter; Larry Wilkerson` (1), `Scott Ritter; Ray McGovern` (1), `Trump's Weakness Spells Disaster | Col. Larry Wilkerson & Scott Ritter` (1)
- `Douglas Macgregor`: `Douglas Macgregor` (55), `Col. Douglas Macgregor` (13)
- `Larry Johnson`: `Larry Johnson` (51), `Larry Johnson & Col. Wilkerson` (4)
- `Alexander Mercouris`: `Alexander Mercouris` (44), `alexander-mercouris` (7), `Alex Christoforou, Alexander Mercouris` (1), `John Mearsheimer, Alexander Mercouris` (1)
- `Seyed M. Marandi`: `Seyed M. Marandi` (34), `Seyed M. Marandi & Larry C. Johnson` (1)
- `Andrei Martyanov`: `Andrei Martyanov` (28), `Andrei Martyanov & Alex Krainer` (1), `Andrei Martyanov & Scott Ritter` (1), `Pepe Escobar & Andrei Martyanov` (1), `Pepe Escobar, Andrei Martyanov & Alex Krainer` (1), `Scott Ritter & Andrei Martyanov` (1)
- `Jacques Baud`: `Col. Jacques Baud` (19), `Jacques Baud` (8)
- `Larry C. Johnson`: `Larry C. Johnson` (9), `Larry C. Johnson; Col. Larry Wilkerson` (6), `Larry C. Johnson & Col. Larry Wilkerson` (3), `Larry C. Johnson; Larry Wilkerson` (1), `Larry C. Johnson; Lawrence Wilkerson` (1), `Pepe Escobar & Larry C. Johnson` (1), `Seyed M. Marandi & Larry C. Johnson` (1)
- `Ray McGovern`: `Ray McGovern` (18), `Scott Ritter; Ray McGovern` (1)
- `Alex Krainer`: `Alex Krainer` (8), `Andrei Martyanov & Alex Krainer` (1), `Israel is in Total Disarray | Alex Krainer & Col. Larry Wilkerson` (1), `Pepe Escobar, Andrei Martyanov & Alex Krainer` (1)
- `Mohammad Marandi`: `Mohammad Marandi` (8), `Chas Freeman & Mohammad Marandi` (2), `Israel's Worst Nightmare Coming | Prof. Mohammad Marandi & Scott Ritter` (1)
- `Robert Pape`: `Robert Pape` (7), `Professor Robert Pape` (2)
- `Daniel Davis`: `Daniel Davis` (6), `Lt Col Daniel Davis` (2)
- `Pepe Escobar`: `Pepe Escobar` (3), `Pepe Escobar & Andrei Martyanov` (1), `Pepe Escobar & Larry C. Johnson` (1), `Pepe Escobar, Andrei Martyanov & Alex Krainer` (1)
- `Anthony Aguilar`: `Lt. Col. Anthony Aguilar` (5), `Anthony Aguilar` (1)
- `Doug Macgregor`: `Col Doug Macgregor` (4), `Doug Macgregor` (2)

## Host Variant Families

- `Nima Alkhorshid`: `Nima Alkhorshid` (183), `Nima Alkhorshid` (28), `Dialogue Works` (18), `Nema` (15), `Nima` (3), `Nima R. Alkhorshid` (3)
- `Daniel Davis`: `Daniel Davis` (215), `Daniel Davis / Deep Dive` (6), `daniel-davis` (6), `Lt Col Daniel Davis` (4), `Daniel Davis (host); Col. Jacques Baud (guest)` (1), `Lt. Col. Daniel Davis` (1)
- `Andrew Napolitano`: `Judge Andrew Napolitano` (99), `Andrew Napolitano` (90), `Judge Andrew Napolitano; Larry Johnson` (1)
- `Glenn Diesen`: `Glenn Diesen` (162), `glenn-diesen` (8)
- `Alex Christoforou`: `Alex Christoforou` (18), `Alex Christoforu` (1)
- `Clayton Morris`: `Clayton Morris, Natali Morris` (2), `Clayton Morris; Natali Morris` (1)
- `Natali Morris`: `Clayton Morris, Natali Morris` (2), `Clayton Morris; Natali Morris` (1)
- `Cyrus Janssen`: `Cyrus Janssen` (1), `Cyrus Janssen; Alex Reporterfy (Reporterfy Media)` (1)
- `Larry Johnson`: `Judge Andrew Napolitano; Larry Johnson` (1), `Larry Johnson` (1)
