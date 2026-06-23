# 2026-05-25 intake scaffold

WORK only; not Record.

This scaffold prepares `provenance/2026-05-25/` to receive today's captures.

Use it as a coordination surface while files are arriving. It is not a transcript, not a terminal evidence unit, and not a substitute for the actual dated raw-input files that should land beside it.

## Today

- `pub_date`: `2026-05-25`
- `ingest_date`: `2026-05-25`
- canonical folder: `codex/years/2026/provenance/2026-05-25/`

## Intake order

1. Materialize the actual transcript-bearing or source-first raw-input file into this folder.
2. Keep primary ownership visible in filename, YAML, and host/guest context.
3. If the capture is speaker-valid, route it downstream after materialization; do not leave it stranded here as a terminal state.

## Canonical YouTube channels

- Dialogue Works
- Daniel Davis Deep Dive
- Glenn Diesen
- Alex Mercouris
- The Duran / Mercouris
- Judging Freedom / Judge Napolitano

## File-shape reminders

- transcript-first captures should prefer the strongest available actual transcript or transcript-bearing raw-input
- designated host-stream interviews should keep host ownership in `thread:` and filename order
- outside-channel expert captures should usually follow the guest lane when that guest already has a real lane
- keep `pub_date` aligned with the parent folder name
- use helper/scaffold files only as temporary coordination surfaces

## Ready-to-land captures

Add rows as candidates appear during the day.

| status | source type | channel / host | guest / subject | target filename | notes |
|--------|-------------|----------------|-----------------|-----------------|-------|
| landed | youtube / operator-pasted transcript | Daniel Davis Deep Dive / Daniel Davis | Iran war cheerleaders / mixed messaging around a deal | `source-daniel-davis-iran-war-cheerleaders-mixed-messaging-surrounding-a-deal-2026-05-25.md` | Canonical `thread: davis` raw-input capture from user-pasted transcript. |
| landed | youtube / operator-pasted transcript | Alexander Mercouris / Alexander Mercouris | Oreshnik strikes / Zaporozhzhye offensive / Europe-Ukraine funding | `source-alex-mercouris-russia-plans-more-oreshnik-strikes-speeds-up-zaporozhzhye-offensive-europe-ukraine-funds-run-short-2026-05-25.md` | Canonical `thread: mercouris` raw-input capture from user-pasted transcript. |
| landed | youtube / cleaned transcript | The Duran / Alex Christoforou | Mercouris on Oreshnik / more strikes planned | `source-duran-mercouris-russia-unleashes-oreshnik-more-strikes-planned-2026-05-25.md` | Duran-hosted Mercouris object routed to `thread: mercouris`. |
| landed | youtube / cleaned transcript | Dialogue Works / Nima Alkhorshid | Larry Johnson on Hormuz / U.S.-Iran throw down | `source-alkorshid-johnson-us-iran-throw-down-over-the-strait-of-hormuz-ticking-time-bomb-2026-05-25.md` | Nima host-stream object routed to `thread: nima`. |
| landed | youtube / cleaned transcript | Dialogue Works / Nima Alkorshid | Col. Jacques Baud on Trump's last card / Israel | `source-alkorshid-baud-trumps-last-card-just-shattered-israel-2026-05-25.md` | Nima host-stream object routed to `thread: nima`. |
| landed | youtube / operator-pasted transcript | Glenn Diesen / Glenn Diesen | Chas Freeman on Israel crisis / Iranian nuclear weapons | `source-glenn-diesen-chas-freeman-crisis-in-israel-iranian-nuclear-weapons-2026-05-25.md` | Canonical `thread: diesen` raw-input capture from user-pasted transcript. |

## Closeout reminder

Before calling the day integrated:

- each valid capture should exist as a real raw-input file in this folder
- helper rows here should either point at a landed file or be removed as stale leads
- downstream routing remains a separate completion step when the capture belongs to a speaker or host lane
