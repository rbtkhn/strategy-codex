# Capture-type calibration (statecraft source archive)

<!-- word_count: 2200 -->

**When to open this doc:** You are about to create or review a source-bearing file in the canonical `source-archive/statecraft/` tree and need **type-specific** defaults for YAML **`kind:`**, **`thread:`**, inbox **stub shape**, and refined-page **Selected Passages** handling — use **§ Essay**, **§ Transcript**, **§ Social**, or **§ Wire and institutional PDF** below. For directory layout and formal **`pub_date`** rules, see [README.md](README.md) and [refined-page-template.md](../../../codex/refined-page-template.md).

WORK only; not Record.

---

## Shared spine (all types)

| Layer | Role |
|--------|------|
| **`source-archive/statecraft/<pub_date>/<slug>.md`** | **Literal SSOT** — full text (or defined bundle), YAML front matter. See [README.md — File template](README.md#file-template-recommended). |
| **[`daily-strategy-inbox.md`](../../../codex/daily-strategy-inbox.md)** | **Registry** — one-line stubs, **`thread:`**, relative link to source file, **`source_url`**, **`verify:`** tail. No megabyte pastes here for heavy captures. |
| **`experts/<id>/<id>-page-*.md`** | **Notebook handle** — **`### Selected Passages`** (excerpt or condensed from raw), **`### Reflection` / `### Predictive Outlook`**, **`### Appendix`**. Not a second verbatim archive; [refined-page-template.md](../../../codex/refined-page-template.md) § SSOT hierarchy. |

**Dates:** **`pub_date`** = calendar day the source went public (essay publish, stream air, post time). **`ingest_date`** = day the file landed in this tree. Folder **`source-archive/statecraft/YYYY-MM-DD/`** should match **`pub_date`** when known; else use the repo's documented pending / unresolved convention until pinned ([README.md](README.md)). Older `provenance/` wording is historical compatibility language only.

**`kind:` vocabulary:** Use only values recognized in-repo (see README kinds table): e.g. **`rss-item`**, **`transcript`**, **`paste-bundle`**, **`x-post-text`**, **`mixed`**, **`verbatim-sidecar`**, **`screenshot-list`**, **`x-screenshots-index`**. Do **not** invent new **`kind:`** strings that tooling must parse unless README/scripts are updated.

---

## Essay

Long-form prose from a **single primary author** or outlet voice: Substack posts, newsletter HTML, magazine essays, static web articles (often ingested via RSS as **`rss-item`**).

| Axis | Guidance |
|------|----------|
| **Typical sources** | Substack, Responsible Statecraft author pages, Ghost, Medium, HTML paste, RSS **`fetch_strategy_raw_input`** pulls. |
| **`kind:`** | Prefer **`rss-item`** when automated from feed; manual paste → **`paste-bundle`** or **`mixed`** if bundling multiple snippets. |
| **`thread:`** | Set when a [strategy-commentator-threads.md](../strategy-commentator-threads.md) **`expert_id`** applies (e.g. named columnist). Else omit **`thread:`** or use inbox **`membrane:single`** until routed — see [README.md — Expert-agnostic](README.md). |
| **Raw body** | Full article text under YAML; preserve headings for navigation; if **paywalled / partial**, state in YAML **`note:`** or inbox (**`partial`**). Public archive / API backfills may only yield the preview body; label that clearly instead of pretending it is a full capture. |
| **Backfill judgment** | Archive discovery is a starting point, not a requirement to ingest every item. Capture the substantial posts you want to keep; leave lighter archive-visible items out when they do not merit preservation. |
| **Mechanical inbox stub** | Title + outlet + **`pub_date`** + **`SS \| cold`** or **`YT`** only if video-shaped — usually **`SS`** / **`notebook`** lane for essays. Tail: **`verify:full-text`** or **`verify:operator-partial`** + **`pub_date:`** + **`opinion-essay-tier`** + **`not-Record`**. **`grep:`** line: author slug + short title tokens + **`YYYY-MM-DD`**. |
| **Refined `### Selected Passages`** | Often **exceeds** ~3k word budget — **excerpt** key sections; full text stays in **`source-archive/statecraft/`**; note omissions in **`### Appendix`** ([refined-page-template.md](../../../codex/refined-page-template.md) § Length). |
| **Pitfalls** | Mistaking **RSS duplicate** for manual paste (dedupe by `guid` when using fetch); **canonical URL** vs tracking params; tiering **fact claims** inside opinion prose (`verify:`). |

**`grep:` keywords (optional tail):** `substack`, `essay`, `paste-bundle`, `rss-item`, `thread:<expert>`.

---

## Transcript

**Speaker-turn** media: YouTube, podcast transcripts, TV segments, broadcast interviews — structured as host/guest blocks or monologue.

| Axis | Guidance |
|------|----------|
| **Typical sources** | YouTube **`watch?v=`**, podcast pages, operator-cleaned transcripts (session paste). |
| **`kind:`** | **`transcript`** (default for speech capture). |
| **`thread:`** | Map the **owning stream** to the **host / interviewer** slug for host-led interviews (e.g. **`thread:diesen`** for a Glenn Diesen interview, even when the guest is Marandi). Use a guest slug only when the guest is the actual owner of the capture. Multi-guest shows: inbox may use **`thread:a`** × **`thread:b`** style (see existing [daily-strategy-inbox.md](../../../codex/daily-strategy-inbox.md) rows). |
| **Raw body** | **Unabridged** cleaned transcript as SSOT; YAML **`show`**, **`host`**, **`guest`** when helpful; **`source_url`** canonical episode URL. Keep **source-faithful** names in `channel_slug`, quoted titles, and `Channel:` lines, but keep **editorial** names consistent in assistant-added fields such as `author`, `host`, `interviewer`, `slug`, and speaker labels. |
| **Mechanical inbox stub** | **`YT \| cold`** (or platform label) + episode title + **aired / publication** **`YYYY-MM-DD`** + theme bullets + **`hook:`** + **`thread:<expert_id>`** + **`full`** link to the canonical `source-archive/statecraft/...md` file + canonical URL + **`verify:operator-cleaned-transcript`** + **`pub_date:`** + tier tags (`opinion-analytic-tier`, etc.) + **`grep:`** host + guest + short slug + date. |
| **Refined `### Selected Passages`** | Often **lane-specific** (guest-only, or expert monologue) or **head + tail + omission line** per [refined-page-template.md](../../../codex/refined-page-template.md) § Length; drop host filler if budget forces. |
| **Pitfalls** | **`pub_date`** = upload vs live air mismatch; chunk merges dropping blank lines between speakers; on-air **numbers** need **`verify:`** before load-bearing use in **`days.md`**; editorial name drift where assistant-added speaker tags or metadata use a different naming style than the lane. |

**Downstream wiring obligation:**

- designated host-stream interviews are host-owned in the canonical statecraft archive
- durable guest lanes still need downstream visibility on the correct speaker surface
- outside-channel guest captures should not remain archive-only; they must land in the guest speaker surface once materialized
- multi-guest captures need an explicit primary ownership surface plus explicit secondary speaker visibility where the guests have real lanes

Closeout law:

- do not call a transcript capture complete merely because the transcript body is on disk
- if the item is materialized but still lacks the required host or speaker visibility surface, the work is still open

**Transcript naming rule (explicit):**

- If the field is preserving the source's public identity, keep the source form exactly.
- If the field is the notebook's own editorial layer, follow the lane's local naming convention consistently.
- For `Diesen`-owned transcript captures, default editorial shorthand is **`Diesen`**, not `Glenn`, unless the source itself is being quoted.

**`grep:` keywords (optional tail):** `transcript`, `YT`, `watch?v=`, `thread:<expert>`, `cleaned-transcript`.

---

## Social

Short-form or **threaded** social text: X/Twitter, Bluesky, **Locals**, Truth Social, Threads, etc. May include **screenshot indexes** when OCR text is unavailable.

| Axis | Guidance |
|------|----------|
| **Typical sources** | Copy-paste posts; thread exports; Locals HTML paste; **public profile crawl** / explicit status URLs; **screenshot rolls** with filenames under **`assets/`**. |
| **`kind:`** | Prefer **`x-post-text`** for a single direct X post paste; prefer **`shortform-bundle`** for multiple short posts from one account or source stream in a day; use **`paste-bundle`** for mixed clips; **`mixed`** for hybrid; **`screenshot-list`** / **`x-screenshots-index`** when **no** extractable speech text ([README.md — kinds table](README.md)). |
| **`thread:`** | Often **topic- or operator-routed** rather than classic commentator; set **`thread:`** when a named lane applies; else omit / **`membrane:single`**. |
| **Raw body** | Ordered posts with separators (`---` or **`Post N`**) for bundles; **stable URL per post** when available; for `shortform-bundle`, keep OCR text as the main body and preserve screenshot provenance in a manifest or appendix section. Capture **time of snapshot** in **`note:`** if deletion risk. |
| **Mechanical inbox stub** | Platform + handle + **`pub_date`** (post day) + **`partial`** vs **`full`** + **`verify:`** for breaking claims + **`not-Record`**. Flag **`screenshot-capture-tier`** or **`operator-pasted-transcript`** as appropriate. For `shortform-bundle`, include the source platform and bundle count in the stub. **`grep:`** handle + first distinctive phrase + date. |
| **Refined `### Selected Passages`** | Short posts may **fit full** Selected Passages; long threads → **selected posts** + Appendix pointer to raw bundle. |
| **Pitfalls** | **Deleted posts** (SSOT is “what we captured”); character-limit noise; mixing **hot takes** with wire facts without tier tags. |

**Downstream wiring obligation:**

- when a social capture clearly belongs to a durable speaker lane, materialization should make it visible from that speaker surface
- if the capture is only a screenshot roll or unresolved mention, keep it out of the bench and treat it as discovery-only until it becomes a real source-archive unit

Closeout law:

- a social capture with real speaker-lane significance may not close as `source-archive only`
- screenshot rolls, unresolved mentions, and discovery placeholders may remain unresolved, but they must not be described as fully routed captures

**`grep:` keywords (optional tail):** `x-post`, `shortform-bundle`, `Locals`, `thread`, `screenshot`, `partial`.

---

## Wire and institutional PDF

**Light bucket** — not the same as **Essay**: multi-outlet **wire** clips, terminal **headline stacks**, **government / central bank / IO PDFs**, institutional PDFs, and **paste-bundles** where **datelines, outlet labels, and attributed facts** matter more than single-author argument arc.

- **Vs essay:** Institutional or **wire-service voice**; **datelines** (LOCATION, Day Month); multiple outlets in one paste; **PDF page references** — use this section, not **§ Essay**.
- **`kind:`** Usually **`paste-bundle`** or **`mixed`**; add YAML **`note:`** for **outlet list**, **tier** (wire vs opinion desk), or **PDF filename** if text is sidecar to a binary.
- **Attribution:** Keep outlet / byline visible in title or first body lines; **`verify:`** **heavy** on numbers, ranks, and **time-sensitive** claims before **`days.md`** load-bearing use.
- **Partial bundles:** OK — state **`partial`** in inbox; refined **`### Appendix`** links the full canonical archive path.
- **Automation:** **Automated wire / paywall fetchers are not implemented** in-repo; manual paste or export remains normative ([README.md — Future extensions](README.md)). Do not assume network fetch in assistant workflows unless the operator authorizes a documented script.

WORK only; not Record.

---

## See also

- [README.md](README.md) — layout, pruning, **`fetch_strategy_raw_input`**, **`populate_strategy_raw_input`**
- [refined-page-template.md](../../../codex/refined-page-template.md) — Selected Passages budget, Appendix bullet order
- [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) — split ingest model
- [`.cursor/rules/strategy-input-raw-ingest.mdc`](../../../../../.cursor/rules/strategy-input-raw-ingest.mdc) — mandatory verbatim capture rule
