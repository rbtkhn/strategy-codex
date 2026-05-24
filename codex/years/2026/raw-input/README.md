# Strategy raw input (full retention, 7 days)
<!-- master-index: raw-input-master-index.md -->
<!-- word_count: 1720 -->

**Master index:** [`raw-input-master-index.md`](raw-input-master-index.md) is the generated corpus-wide route map for this tree, with [`raw-input-master-index.json`](raw-input-master-index.json) as its machine-readable companion. It is a maintained summary surface, not the authority itself: the dated `raw-input/` folders remain canonical.

The companion audit surface is [`raw-input-index-audit.md`](raw-input-index-audit.md), with [`raw-input-index-audit.json`](raw-input-index-audit.json) as its machine-readable companion. It is heuristic and non-gating by design: use it to spot index sprawl, weak index justification, and plausible missing benches without letting it outrank the canonical tree.

Rebuild command: `python scripts/raw_input_master_index.py --raw-root codex/years/2026/raw-input --apply` (or let `materialize_youtube_raw_input.py --apply` refresh it automatically).

**Purpose:** Store **complete** transcripts and **all** strategy-ingest source material you want kept verbatim — without bloating [daily-strategy-inbox.md](../daily-strategy-inbox.md) or hitting the **~2000 word** per-block budget on [experts/*/transcript.md](../experts/ritter/transcript.md) that **`thread`** triage targets.

**SSOT role:** This tree is the **SSOT for literal text** of each capture. **[`strategy-codex-template-raw-input.md`](../../strategy-codex-template-raw-input.md)** defines the **capture shape**, while **[`refined-page-template.md`](../refined-page-template.md)** defines the **next layer:** standalone **`experts/…/ *-page-*.md`** files carry **`### Verbatim`** (and analysis) and are the **SSOT for thread / `days.md` / strategy work** — cite those pages for judgment; use **`raw-input/`** when you must verify or edit the **exact words**.

**Expert-agnostic:** This tree is **raw material for analysis**, not only dumps tied to a [strategy-commentator-threads.md](../strategy-commentator-threads.md) **`expert_id`**. Substack essays, wire bundles, institutional statements, screenshot indexes, and mixed paste-bundles belong here even when there is **no** `thread:` lane yet (or ever). The inbox stub may use **`membrane:single`** and omit **`thread:`**; frontmatter **`thread:`** is optional (see § File template).

**Unlisted speakers / no lane yet:** If a capture is worth keeping but the speaker or outlet does **not** map to an existing expert folder, still ingest it here as source-first raw input. Leave **`thread:`** out unless you later decide to route it into an existing lane.

## Interview ownership (designated stream vs outside-channel split)

- **Direct authored material** -- essays, newsletters, signed Substack posts, official statements -- stays with the **author** stream.
- **Designated-stream interviews** -- interviews, panels, podcasts, and host-framed YouTube transcripts on a **designated cognition stream** such as Diesen, Davis, Mercouris, or Dialogue Works -- belong to the **host / interviewer cognition stream** by default.
- **Outside-channel expert captures** -- interviews on channels that are **not** designated cognition streams -- should usually be owned by the **guest / recurring expert lane** when that guest already has a real notebook lane (for example `pape`, `ritter`, `parsi`, `marandi`).
- **Guests and hosts still matter:** keep both visible in titles, body text, refined pages, `crosses:` relationships, and later synthesis.
- **Do not** create duplicate host-owned and guest-owned raw-input files by default just because both sides are notable. Only do that when the operator explicitly wants a second ownership surface.

Short version:

- **Crooke essay -> Crooke**
- **Diesen x Crooke transcript -> Diesen**
- **Davis x Crooke transcript -> Davis**
- **Mario Nawfal x Pape transcript -> Pape**
- **outside channel x Ritter transcript -> Ritter**

Implementation rule:

- for **designated host-stream interviews**, `thread:` follows the **host / interviewer stream**
- for **outside-channel expert captures**, `thread:` follows the **guest / expert lane**

The filename should teach the same rule. If the designated stream owns the capture, the host stream goes first. If the host is only an outside container, put the **expert first** and retain the outside host in `show`, `host`, `channel_slug`, and title context.

For the compact strategy-language version of this rule, see [raw-input-lane-ownership.md](../../../docs/skill-work/work-strategy/raw-input-lane-ownership.md).


**Capture-type calibration (essay / transcript / social / wire–PDF):** For **type-specific** defaults — **`kind:`**, **`thread:`**, inbox stub shape, refined-page **`### Verbatim`** expectations — see **[`CAPTURE-TYPES.md`](CAPTURE-TYPES.md)** (grep-friendly **`##`** headings). Operator + assistant ingest should align that doc with the scaffold in [strategy-codex-template-raw-input.md](../../strategy-codex-template-raw-input.md) and [refined-page-template.md](../refined-page-template.md).

When a file is a valid speaker capture, correct YAML and correct storage day are necessary but **not sufficient**. The capture is not fully integrated until it is wired into the correct host and/or speaker visibility surfaces.

**Speaker wiring doctrine:** For the speaker-side route-map version of this rule, see [codex/speakers/map/README.md](../../../speakers/map/README.md). This README is the canonical storage-side contract.

**Closure doctrine:** The governing repo-level closure line lives in [architectural-fullness.md](../../../docs/architectural-fullness.md) and its supporting [lifecycle-closure-audit.md](../../../docs/lifecycle-closure-audit.md). This README applies that doctrine to storage and routing for speaker captures.

## Index hierarchy

Use the indexing ladder sparsely and on purpose:

- `raw-input-master-index.md/json` = the only corpus-wide route map for this tree
- speaker raw-input indexes = selective retrieval benches when a speaker needs a real `non-core appearance bench`
- arc files = interpretive surfaces, not default index surfaces

Per-arc indexes are exceptional, not standard. Do not create a dedicated arc index merely because an arc has chronology, multiple pages, or month-level density. The default path is:

- global lookup through the master index
- speaker-side retrieval through an existing speaker raw-input index when one is justified
- interpretation through the arc itself

If an arc-specific index is proposed, it should satisfy the stronger speaker-map threshold: the parent arc is no longer a practical front door, the indexed items form a distinct retrieval domain rather than a chronology, and the new surface answers a different operator question than the neighboring speaker index or arc.

## Raw-Input Wiring Contract

`raw-input/` is a date-first evidence ledger, but a valid materialized speaker capture must not remain only in this tree.

Every valid materialized speaker raw-input must become visible from the correct downstream routing surface:

- a host-owned `core host lane`
- a speaker-owned `non-core appearance bench`
- both, when host ownership and speaker visibility are both required

`discovery memory` is reserved for not-yet-materialized appearances only. Once a speaker appearance is valid and materialized as raw-input, leaving it only in discovery memory is broken wiring.

If a valid raw-input exists but is absent from the correct speaker raw-input index, or absent from a required host visibility surface, treat that as an architecture defect and repair it.

Hard law:

- a valid materialized speaker capture may not be left in `raw-input/` as its terminal state
- `_aired-pending/`, `snippets/`, queue docs, verify files, and discovery-memory notes may not serve as terminal homes for valid materialized captures
- if a capture is stranded in any of those states, the ingest or routing task is still open

## Lifecycle Closure

For a valid speaker capture, storage is an intermediate state rather than the end of the lifecycle.

The lifecycle works like this:

1. discovery or intake finds the source
2. materialization creates the dated evidence unit in `raw-input/`
3. routing exposes the capture from the correct host and/or speaker surfaces
4. closure happens only when that routed visibility is real, or when review shows the item is not actually a valid speaker capture

In repo shorthand:

- materialization starts the lifecycle
- routed visibility ends it

That is why `_aired-pending/`, `snippets/`, queue docs, verify sidecars, discovery-memory notes, and similar helper layers are temporary or supporting states only. They may assist the lifecycle, but they do not complete it.

## Storage vs Routing

Two distinct architectures overlap here and should not be conflated:

- `raw-input/` = publication-day storage and literal-text SSOT
- speaker and host surfaces = routing projections over that stored evidence

That means `raw-input/` answers "what exact source text do we have, and on what publication day does it belong?" while speaker folders, host lanes, and related indexes answer "where should this capture be visible for judgment and re-entry?"

Benchmark pin:

- `raw-input/` owns provenance, publication day, capture materialization, and primary ownership
- speaker and host routing surfaces own downstream visibility, re-entry paths, and completeness checks after materialization

Helper layers may still live nearby, but they are not the same thing as primary evidence units. Day files such as `YYYY-MM-DD-speaker.md`, verify sidecars, scaffold notes, inventories, and queue docs help operators and agents work the tree; they do not replace the underlying capture file.

## Ownership And Downstream Obligations

Standardize the downstream wiring rule by capture type:

- designated host-stream interviews: raw-input ownership follows the host stream, but durable guest lanes still require speaker-side visibility
- outside-channel expert captures: when the guest already has a real lane, raw-input ownership should usually follow the guest lane; host metadata stays visible in YAML, title, and later routing context
- multi-guest captures: require at least one explicit primary ownership surface plus explicit secondary speaker visibility rules for the other durable guests

Do not allow "present in raw-input only" as a final state for a valid speaker capture.

## Conceptual Routing Manifest

The repo does not need code for this yet, but each valid speaker raw-input should be easy to classify using the same conceptual manifest shape:

- `ownership`: `host-owned` or `guest-owned`
- `speaker_targets`: which speaker surfaces must expose the capture
- `host_targets`: which host-local arc, host raw-input index, or host route surface must expose it
- `status`: `materialized`, `discovery-only`, or `pending-date`

Treat this as policy-first architecture that can later support audits or automation.

## Wiring Obligations

Once a speaker capture is valid and materialized, the architecture imposes concrete obligations:

1. `raw-input/` must hold the publication-day evidence unit with correct primary ownership.
2. The correct host and/or speaker surfaces must expose that unit for re-entry.
3. Discovery memory must either promote the item into materialized routing or release it as a discarded lead; it must not act as a parking lot for already-materialized captures.

Treat those as completion conditions, not aspirations.

If any of those obligations is unmet, do not describe the work as captured, integrated, or complete.

## Audit Questions

Use these checks whenever you materialize, backfill, or review speaker captures:

1. Does the file exist in the correct dated folder with stable publication-day placement?
2. Is primary ownership legible from filename, YAML, and surrounding context?
3. If the capture belongs to a durable speaker lane, where is its speaker-side visibility surface?
4. If the capture belongs to a durable host lane, where is its host-side visibility surface?
5. Is any discovery-memory note still carrying an item that is already materialized and should have been promoted?
6. Is any scaffold, snippet, or pending-date file pretending to be a terminal home rather than a temporary state?

If one of those questions cannot be answered cleanly, treat the capture as under-wired.

Under-wired captures are not a soft warning class. They are unresolved routing work.

## Failure Modes

The common failure is not only missing files. It is false completion.

- `stored but invisible`: the raw-input exists, but no correct speaker or host route exposes it
- `speaker-only memory drift`: a speaker note mentions the appearance, but the materialized raw-input is absent or misowned
- `discovery-memory trap`: a valid materialized capture is still described as a find rather than promoted into the bench or lane
- `pending-date freeze`: a file stays in `_aired-pending/` after publication day is knowable
- `scaffold capture confusion`: snippets, verify files, or queue docs begin to function as if they were evidence units
- `ownership / visibility collapse`: the notebook forgets that primary ownership and downstream visibility are different decisions

The contract is only healthy when those failure modes are actively checked rather than assumed away.

## Closeout Rule

A task that materializes, backfills, or normalizes speaker raw-input may close only after one of the following is true:

- the capture is visible from the correct host and/or speaker route surfaces
- the operator explicitly asked for storage-only work and the reply says the routing obligation remains open
- the item is not actually a valid materialized speaker capture after review

Absent one of those conditions, the correct status is `still open`.

## Publication vocabulary (formal pin)

- **Machine (grep / YAML / cold lines, `verify:` tails):** use **`pub_date`** and the tag **`pub_date:YYYY-MM-DD`**. **Do not** introduce new **`aired:`** tags; **`ingest_date`** remains “when the file entered this tree,” distinct from **publication**.
- **Human (preambles, spec prose):** use **Published** / “publication day” — not an “aired” block as the norm. Same calendar anchor as **`pub_date`**; see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) publication vocabulary and [refined-page-template.md](../refined-page-template.md).
- **Legacy (until bulk migration):** folder **`_aired-pending/`** and existing **`aired:`** / “aired” in older **daily-strategy-inbox.md** and captures stay on disk; new material and new edits follow this pin.

## Three capture channels (normative vs recovery)

Do **not** conflate **Cursor agent transcript JSONL** (machine-local logs of chat turns, including `<user_query>`) with **`experts/<expert_id>/transcript.md`** (rolling **in-repo** triage corpus). They are different surfaces with different roles.

| Channel | What it is | Role |
|---------|------------|------|
| **1 — Direct / assistant write** | Markdown under **`raw-input/<pub_date>/`** with YAML (`kind: paste-bundle`, `rss-item`, etc.), written in-session or by automation | **Normative** for manual strategy inputs — matches [`.cursor/rules/strategy-input-raw-ingest.mdc`](../../../../../.cursor/rules/strategy-input-raw-ingest.mdc). |
| **2 — Populate** | [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py) copies **`experts/.../transcript.md`** date sections, standalone `*verbatim*.md`, X indexes — **repo artifacts only** | **Mirror / backfill** from material already committed; **does not** read Cursor JSONL. |
| **3 — Agent JSONL scripts** | Ad hoc parsers (e.g. [`scripts/backfill_crooke_raw_input_from_transcript.py`](../../../../scripts/backfill_crooke_raw_input_from_transcript.py)) | **Salvage** when chat never wrote **`raw-input/`** — regex- and shape-dependent; **not** policy. |

**RSS / Substack API** ([`fetch_strategy_raw_input.py`](../../../../scripts/fetch_strategy_raw_input.py), [`backfill_substack_raw_input.py`](../../../../scripts/backfill_substack_raw_input.py)) write **`raw-input/`** directly — **preferred** when a feed or API path exists (zero chat overhead).

### Pruning vs recovery

**Pruning** ([§ Pruning](#pruning)) is **optional disk reclaim** (`prune_strategy_raw_input.py`), operator-triggered. It is **not** the next step after “recover missed verbatim,” and it is **not** CI-scheduled. Recovery **after** mistaken deletion uses **`git checkout`** on removed paths ([§ Pruning](#pruning) note).

Do **not** bundle “default rolling window ≈ 7 days” with **recovery**: the same **`N`** aligns expert **`transcript.md`** tooling and **`prune_strategy_raw_input.py`**, but **prune** is **hygiene**, not ingest salvage.

## Automated fetch (RSS → raw-input)

**Script:** [`scripts/fetch_strategy_raw_input.py`](../../../../scripts/fetch_strategy_raw_input.py) — pulls **RSS/Atom** items (e.g. Substack `/feed`) into **`raw-input/<pub_date>/`** as markdown with YAML frontmatter (`kind: rss-item`). When a feed sets **`"thread": "<expert_id>"`**, new items **append** into **`raw-input/<pub_date>/<pub_date>-<expert_id>.md`** (multiple ingests = multiple `---` … `---` blocks; duplicates skipped by `guid:`). **Refined pages** (operator judgment artifacts) live under **`experts/<expert_id>/`** — e.g. **`mercouris-page-YYYY-MM-DD.md`** — not in this tree. Feeds **without** `thread` still write **one markdown file per RSS item** (slug + hash basename). Optional **`thread:`** in YAML drives **`python3 scripts/strategy_thread.py`** triage: one-line RSS stubs merge into that expert’s **`experts/<id>/transcript.md`** (after inbox lines for the same date).

**Setup:**

1. Edit **`fetch-sources.json`** in this directory (default includes Simplicius, Big Serge, Greenwald with `thread` set). To add feeds, copy from [fetch-sources.example.json](fetch-sources.example.json) or append another object under `rss_feeds` (`url`, `slug_prefix`, `max_items`, `enabled`, optional `thread`).
2. Preview: `python3 scripts/fetch_strategy_raw_input.py` (dry-run by default).
3. Write: `python3 scripts/fetch_strategy_raw_input.py --apply`.

**Config path override:** set env **`FETCH_STRATEGY_SOURCES`** to an absolute path, or pass **`--config`**.

**Scheduling:** use **cron**, **launchd**, or a personal runner — e.g. daily at 06:00 local:

`0 6 * * * cd /path/to/grace-mar && /usr/bin/python3 scripts/fetch_strategy_raw_input.py --apply >> ~/logs/strategy-fetch.log 2>&1`

Optional local override file (gitignored): **`fetch-sources.local.json`** — merge story is manual (copy entries into `fetch-sources.json` or swap path via env); the repo does not auto-merge two JSON files.

**Backfill / mirror (no network):** [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py) copies **on-disk** **`experts/<id>/transcript.md`** sections and verbatim sidecars into **`raw-input/`** — **not** Cursor agent JSONL (see [§ Three capture channels](#three-capture-channels-normative-vs-recovery)). Run after local edits when you want a unified archive layout.

**Backfill source registry:** before adding another `backfill_*` wrapper, check [BACKFILL-SOURCES.md](BACKFILL-SOURCES.md). It classifies generic source families, source-specific adapters, and recovery-only scripts so the notebook can reduce wrapper sprawl without deleting useful tools prematurely.
**Short-form bundle backfill (screenshots / OCR):** [`scripts/backfill_shortform_bundle_raw_input.py`](../../../../scripts/backfill_shortform_bundle_raw_input.py) packages multiple short posts from one account or source stream into a single `kind: shortform-bundle` file. Put the OCR'd bundle body in `--body-file`, repeat `--screenshot` for provenance refs, and pin `--platform`, `--account`, and optional `--thread` as needed. Example:

```bash
python3 scripts/backfill_shortform_bundle_raw_input.py \
  --pub-date 2026-05-07 \
  --platform threads \
  --account @example \
  --profile-url https://threads.net/@example \
  --thread example \
  --body-file /path/to/ocr.md \
  --screenshot /path/to/shot-1.png \
  --screenshot /path/to/shot-2.png \
  --apply
```

For X-specific bundles, [`scripts/backfill_x_shortform_bundle_raw_input.py`](../../../../scripts/backfill_x_shortform_bundle_raw_input.py) keeps the `platform` pinned to `x` and defaults `--profile-url` to `https://x.com/<account>`, so you only need to provide the account plus bundle inputs.

**Substack year backfill (full post body):** [`scripts/backfill_substack_raw_input.py`](../../../../scripts/backfill_substack_raw_input.py) — paginates `api/v1/archive`, fetches `api/v1/posts/{slug}`, writes `raw-input/<date>/substack-*.md` with optional YAML `thread: simplicius` (or other id). Treat the archive as a discovery index, not a completeness mandate: backfill the substantial posts you want preserved, and leave light or repetitive archive-visible items out when that is the better editorial call. Example:
`python3 scripts/backfill_substack_raw_input.py --hostname simplicius76.substack.com --year 2026 --thread simplicius --apply`

**X profile backfill (best-effort public crawl):** [`scripts/backfill_x_profile_raw_input.py`](../../../../scripts/backfill_x_profile_raw_input.py) — crawls a public X profile for visible `status/` links, fetches each status page, and writes `kind: x-post-text` captures into `raw-input/<date>/`. Use this for Ritter or any other public profile when you want profile discovery plus one-file-per-post capture; pass explicit `--status-url` values when you already know the exact post URLs.

**Responsible Statecraft author crawl (public articles):** [`scripts/backfill_responsiblestatecraft_author_raw_input.py`](../../../../scripts/backfill_responsiblestatecraft_author_raw_input.py) — crawls a public author page, fetches each linked article page, and writes `kind: rss-item` captures into `raw-input/<date>/`. Use this for Parsi when the public author archive is the discovery surface; pass explicit `--article-url` values when you already know the exact article URLs.


**Crooke partial backfill (public archive discovery):** [`scripts/backfill_crooke_substack_raw_input.py`](../../../../scripts/backfill_crooke_substack_raw_input.py) â€” uses the public Conflicts Forum archive to discover 2026 posts, compares them against existing `thread: crooke` raw-input files, and writes `substack-post` stubs when a post needs a public-preview placeholder. Use this when the public archive proves the post exists but the paid body still needs manual completion.

**Compose boundary:** Automated capture writes **`raw-input/`** only; new `experts/<expert_id>/*page*.md` files are created later in a separate compose pass.
**Future extensions (not implemented yet):** authenticated/private X and wire paywall fetchers — public X profile crawl and public YouTube transcript fetches are implemented, but authenticated sessions still need their own gate (tokens, ToS, tier tags).

**YouTube transcript queue:** [`youtube-transcript-queue.md`](youtube-transcript-queue.md) — lists the canonical input channels for strategy-notebook. The generic helper is [`scripts/backfill_youtube_channel_raw_input.py`](../../../../scripts/backfill_youtube_channel_raw_input.py); thin wrappers can pin channel URL, show/host, and thread routing when needed. This queue belongs with the expert-profile backfill arc as a corpus-indexing layer; compose judgment still happens later in expert pages / `days.md`, not in the queue itself.

**Relation to other surfaces:**

| Surface | Role |
|--------|------|
| **daily-strategy-inbox.md** | Paste-ready **stubs** + grep registry; optional short excerpts only — **index before (or in the same step as)** full verbatim on disk |
| **experts/`<id>`/transcript.md** | 7-day rolling **triage** corpus from inbox `thread:` blocks (word caps per architecture); **pointers** when the same material is already under **`raw-input/`** |
| **`raw-input/` (this tree)** | **Unabridged** text and bundled inputs; **pruning is operator-initiated only** (see § Pruning). Nothing in CI auto-deletes this tree. |

**`kind:` values (YAML) and automation** — files with **`thread: <expert_id>`** and a parseable publication day (folder + front matter) participate in **`thread`** triage and the **machine layer** “Recent raw-input” list, except **index-only** kinds that would duplicate assets without adding speech text:

| `kind` | Merged into transcript (one-line stub) | Notes |
|--------|----------------------------------------|--------|
| `rss-item`, `transcript`, `paste-bundle`, `x-post-text`, `mixed`, `verbatim-sidecar`, … | **Yes** (if `thread:` set) | Default: any `kind` **except** the exclude list below. |
| `screenshot-list`, `x-screenshots-index` | **No** | Image / index rolls only; not expert speech stubs. |

**Transcript file optional (advanced):** The per-expert rolling **`experts/<id>/transcript.md`** can stay **empty or pointer-only** when **`thread`** is run regularly — the **machine layer** still gets **Recent raw-input (lane)** from on-disk + inbox. Fully **removing** `transcript.md` from the tree is a separate hygiene choice (only after the operator bakes in raw-input + inbox registry habits).

**End-of-day strategy session (notebook compose):** Default **sole** window for writing **`strategy-page`** blocks + `days.md` judgment is the **once-per-day** session you open with **`strategy page`** or **`strategy page compose`** (operator phrases — see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *End-of-day strategy session*). **Primary bulk evidence:** **this folder’s** dated files plus inbox stubs. The operator token **`weave`** is **deprecated** for that compose step.

WORK only; not Record.

## Layout

**Canonical scaffold owner:** [strategy-codex-template-raw-input.md](../../strategy-codex-template-raw-input.md) owns the narrow file-shape template for raw captures. This README stays the SSOT for routing, automation, source-family policy, and pruning.

Use **one subdirectory per publication day** — the folder name **`YYYY-MM-DD`** matches **`pub_date`** in the file’s frontmatter (when the source went public: livestream go-live, YouTube publish, Substack `pubDate`, RSS item date, etc.). This matches [`scripts/fetch_strategy_raw_input.py`](../../../../scripts/fetch_strategy_raw_input.py) (writes under **`raw-input/<pub_date>/`**) and [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py) (uses section / filename **publication** dates).

**Not** the folder for “the day I saved the file” — that belongs in **`ingest_date`** in YAML only. If **`pub_date`** is still unknown (e.g. transcript paste before the canonical `watch?v=` is pinned), use **`_aired-pending/`** for the markdown file; move it into **`raw-input/<pub_date>/`** once the air day is fixed.

```text
raw-input/
  README.md          ← this file
  _aired-pending/    ← optional: captures whose pub_date is not fixed yet (move when pinned)
  YYYY-MM-DD/        ← = pub_date / air day (e.g. 2026-04-20/)
    YYYY-MM-DD-<expert_id>.md   ← raw capture: RSS `thread:` merge target + populate mirror (append ingests)
    <slug>.md        ← other captures: verbatim sidecars, RSS without thread:, bundles, indexes
```

**Refined page (not here):** **`experts/<expert_id>/<expert_id>-page-YYYY-MM-DD.md`** — Verbatim / Reflection / Predictive Outlook; links back to **verbatim** in this tree. **Multiple refined pages for the same publication date are allowed:** **`…-page-YYYY-MM-DD-<slug>.md`** (slug from `raw-input` stem) **or** one consolidated file with **A / B / C** Verbatim blocks per [refined-page-template.md](../refined-page-template.md) (each expert’s **`*-page-template.md`** is a **compat stub** linking that canonical). Distinct from **`strategy-page`** in `thread.md` unless mirrored during EOD compose.

**Raw capture:** e.g. **`2026-04-21-mercouris-verbatim.md`** under **`2026-04-21/`** because the episode **published** ( **`pub_date`** ) on that calendar day; RSS **`thread: mercouris`** appends to **`2026-04-21-mercouris.md`** in that same folder.

**Other slugs:** `kebab-case`, unique within that day — e.g. `ritter-judging-freedom-2026-04-20.md`, `substack-simplicius-….md`, `davis-johnson-hormuz-full.md`.

**Optional:** Add non-markdown payloads next to the `.md` file in the same folder (e.g. `.txt` exports) if you truly need byte-identical dumps; keep filenames descriptive.

## Subtree semantics

Treat the special subtrees and helper files as distinct from primary capture units:

- `_aired-pending/` = unresolved `pub_date`; allowed temporarily, but the file should still carry intended routing metadata and must move into a dated folder once publication day is pinned
- `snippets/` = scaffolding only; never a terminal home for valid captures
- scaffold docs, inventories, and queue files = control surfaces; useful for coordination, but not evidence units
- day helper files such as `YYYY-MM-DD-speaker.md`, `verify-*.md`, and similar sidecars = helper layers, not equivalent to primary transcript captures unless explicitly documented otherwise

Any file graduating from scaffold or snippet status into a valid capture should be moved into a dated folder and wired downstream immediately.

## File template (recommended)

The canonical shape lives in [strategy-codex-template-raw-input.md](../../strategy-codex-template-raw-input.md). Use the summary below as a convenience reminder; keep detailed file-shape edits aligned with the template.

Each `.md` file should start with a short metadata block so greps and future tooling can link back to expert lanes and URLs:

```markdown
---
ingest_date: YYYY-MM-DD
pub_date: YYYY-MM-DD
thread: expert_id
source_url: https://...
kind: transcript | paste-bundle | screenshot-list | x-screenshots-index | x-post-text | shortform-bundle | mixed | substack-post
---

# Human-readable title

…full body…
```

`thread:` may be omitted for non-expert material (e.g. raw wire paste with no `thread:` lane yet). When **`thread:`** is present for an **interview**, it should name the **owning host / interviewer stream**, not every notable guest mentioned in the capture. **`pub_date`** is the calendar day the source went public (live, YouTube/Substack publish, RSS `pubDate`, etc.), distinct from **`ingest_date`** (when you saved or ingested the file into this tree). **On disk,** the parent folder `raw-input/YYYY-MM-DD/` **should match `pub_date`** once known (or **`_aired-pending/`** until then). The legacy key **`published_date`** is **removed** from this tree; use **`pub_date`** only. RSS triage reads **`pub_date`**, then **`ingest_date`**, then the folder name. Prefer **`kind: x-post-text`** when you paste X copy directly; legacy screenshot captures are indexed as **`x-screenshots-index`** (links to `assets/**/*.png`, no OCR).

For bundled short-form posts captured from screenshots or OCR, use **`kind: shortform-bundle`**. That is the generic daily bundle format for one source account or stream when you want one file to hold multiple short posts, with OCR text in the body and screenshots preserved as provenance. Existing `x-post-bundle` captures remain valid legacy files, but new generic bundles should use `shortform-bundle`.

## Harvest / backfill

To **populate** `raw-input/` from material already on disk (standalone `*verbatim*.md` at the strategy-notebook root, per-expert `experts/<id>/transcript.md` date sections, and `assets/**/x-*.png` grouped by date in the filename), run from repo root:

```bash
python3 scripts/populate_strategy_raw_input.py --dry-run
python3 scripts/populate_strategy_raw_input.py --apply
```

**Window:** dates **`d`** where **`d > today − 7`** local days (same as expert transcript triage and `prune_strategy_raw_input.py`). **`--days N`**, **`--today YYYY-MM-DD`** (tests), **`--force`** (overwrite changed files), and **`--notebook-root`** / **`--root`** are supported.

Idempotent: unchanged files are skipped (content hash). See [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py).

**Advisory gap hint:** [`scripts/strategy_raw_input_gap_hint.py`](../../../../scripts/strategy_raw_input_gap_hint.py) — compares **`daily-strategy-inbox.md`** URLs to **`source_url`** in **`raw-input/`** YAML (default: article-ish URLs such as Substack `/p/`, Conflicts Forum, YouTube `watch`; **`--all-urls`** for full inbox scrape — noisy). **Not** CI or policy; operator judgment only.

## Outlet inventories (tracker docs)

- **Dialogue Works** (Nima Alkhorshid): [dialogue-works-inventory.md](dialogue-works-inventory.md) — metadata-only YouTube crawl index from `2026-01-01` through the latest upload returned by the crawl, with `needs capture` markers and maintenance notes at the bottom.
- **April 2026 channel scaffolds** — month-scoped handoff docs for transcript completion and canonical URL pinning:
  - [dialogue-works-april-2026-scaffold.md](dialogue-works-april-2026-scaffold.md)
  - [glenn-diesen-april-2026-scaffold.md](glenn-diesen-april-2026-scaffold.md)
  - [daniel-davis-april-2026-scaffold.md](daniel-davis-april-2026-scaffold.md)
  - [mercouris-duran-april-2026-scaffold.md](mercouris-duran-april-2026-scaffold.md)

## Volume / Book / Chapter convention

Use the following naming ladder for scaffold work:

- **Volume** = year
- **Book** = month
- **Chapter** = day

Example:

- `Vol. 2026, Book IV, Chapter XXVIII` = the daily slice for `2026-04-28`

How to apply it here:

- the **daily Chapter files** are the substantive units of work for Cici-AI completion
- the **month scaffold files** summarize and coordinate those chapter files for a single channel
- the **volume** is the annual wrapper used when you want to speak about the full year as a whole
- keep the file system date folders unchanged; this is a naming and coordination layer, not a directory migration

Suggested scaffold file wording:

> This scaffold covers `Vol. 2026`, `Book IV` and organizes the daily Chapter files for April 2026.


## Pruning

**Policy:** There is **no** scheduled or CI-driven prune in this repo — **you** run the script when you want to reclaim disk space. A marker file **[`.pruning-suspended`](.pruning-suspended)** is committed: **`python3 scripts/prune_strategy_raw_input.py --apply`** **refuses** to delete until you either pass **`--override`** with **`--apply`** or **remove** the marker file. **`--dry-run`** (or default preview mode) **always** works so you can see what would be removed.

Retention (when you do prune) matches expert **`transcript.md`**: folders named **`YYYY-MM-DD`** are **removed** when that date is **`<= today − N`** (default **`N = 7`** via **`--days`**) — same calendar window as `scripts/strategy_expert_transcript.py`.

From repo root:

```bash
# Preview what would be deleted
python3 scripts/prune_strategy_raw_input.py --dry-run

# Apply deletion (only when not suspended, or with override)
python3 scripts/prune_strategy_raw_input.py --apply --override
```

Default root: `docs/skill-work/work-strategy/strategy-notebook/raw-input`. Override with `--root <path>` if needed.

**Note:** This does **not** replace git history. If you need recovery after prune, use `git checkout` on the removed paths.

## Assistant default

When the operator asks for **full transcript on disk**, write **verbatim** under **`raw-input/YYYY-MM-DD/<descriptive-slug>.md`** (or **`YYYY-MM-DD-<expert_id>.md`** when matching RSS merge). Place **refined pages** under **`experts/<expert_id>/<expert_id>-page-YYYY-MM-DD.md`** (and **`…-page-YYYY-MM-DD-<slug>.md`** when splitting multiple primaries on the same date — see [NOTEBOOK-CONTRACT.md](../NOTEBOOK-CONTRACT.md) § Refined pages). Keep [daily-strategy-inbox.md](../daily-strategy-inbox.md) to **stub lines** pointing at **verbatim** for `verify:` and optionally at the **expert page** for composed judgment, e.g. `verify:full-text+raw-input/2026-04-21/2026-04-21-mercouris-verbatim.md`.

**Provenance:** YAML frontmatter does not record **operator vs assistant** author by default; **git commits** carry **who / when** for audit. Optional YAML (`note:`) may name capture context.

**Paste-bundle starter:** [snippets/new-paste-bundle.md](snippets/new-paste-bundle.md) — copy headers + replace placeholders before pasting body.

Full contract: [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Split ingest model](../STRATEGY-NOTEBOOK-ARCHITECTURE.md#split-ingest-model).
