# work-strategy

## Activation — `strategy` (no Cursor skill)

The **`skill-strategy` skill is dissolved** ([SKILL-STRATEGY-DEPRECATED.md](SKILL-STRATEGY-DEPRECATED.md)). On **`strategy`**, **`strategy pass`**, or legacy **`work-strategy`** (codex pass):

1. Read [.cursor/rules/strategy-codex-pass.mdc](../../.cursor/rules/strategy-codex-pass.mdc)
2. Run [DEFAULT-PATH.md](DEFAULT-PATH.md) — three moves, then stop
3. Load other skills **only** on modifier or menu fork (table below)

**Phrases:** `strategy page`, `strategy page read`, `strategy input`, `strategy write` (compound → also skill-write), `strategy + verify`.

### Routing

| Say this | Load |
|----------|------|
| **`strategy`** / **`strategy pass`** | DEFAULT-PATH.md |
| **`recursive learning`** / **`RLJ`** / session review through RLJ | [recursive-learning skill](../../../.cursor/skills/recursive-learning/SKILL.md) → journal SSOT first |
| **`strategy page` / compose** | STRATEGY-NOTEBOOK-ARCHITECTURE.md EOD section |
| **`strategy + verify`** | wire-verify / fact-check |
| **`strategy write`** | skill-write + codex substance |
| **`strategy input`** | strategy-input-raw-ingest.mdc + codex/raw-input/ |
| **Voice / lens** | statecraft handoff or compose — VOICES-SUPERSEDE-MINDS.md; statecraft-multi-lens |
| **Live crisis / intake** | statecraft-* lanes — not DEFAULT-PATH body |
| **`tri-mind` / `tri-frame`** | Deprecated — TRI-MIND-DEPRECATED.md; statecraft-multi-lens or one voice profile |
| **Weekly brief** | weekly-brief-run |
| **Speaker shelf audit** | speaker-shelf-hygiene |

---

**Legacy status:** `docs/skill-work/work-strategy/` is now a **legacy compatibility surface**, not the canonical operator judgment owner. The active public/operator-facing successor is [statecraft/](../../../statecraft/README.md). Use [Legacy Successor Map](LEGACY-SUCCESSOR-MAP.md) when an older strategy path still exists on disk and you need the current conceptual destination.

**Naming:** `strategy-codex` remains the repo and notebook identity, but the old `work-strategy` lane terminology is obsolete as a canonical live surface. The canonical chronology corpus lives under root [`/codex`](../../../codex/README.md), while live judgment, prose, and mechanism now belong under [statecraft/](../../../statecraft/README.md). `strategy-notebook` is a deprecated compatibility namespace for old links, script aliases, fixtures, and historical logs; do not add new canonical material there.

**Current role (one sentence):** This tree is now primarily a **legacy holding surface** for still-unmigrated notebook machinery, operator doctrine, and historical strategy memos that have not yet been re-homed into `statecraft/`, `/codex`, or `singularity/`.

**Default path (fast start):** [DEFAULT-PATH.md](DEFAULT-PATH.md) � three moves for a normal **`strategy`** pass; no Cursor skill to load.

**Full sequence (SSOT):** [STRATEGY-NOTEBOOK-ARCHITECTURE.md â€” Default operating path](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md#default-operating-path-ssot) â€” inbox-first numbered path (weave, optional escalation markers, STRATEGY promotion when stable, no Record). **Conductor / cadence â†’ durable /codex anchor:** [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../codex/CONDUCTOR-IMPROVEMENT-LOOP.md) (optional close template: [CONDUCTOR-CLOSE-TEMPLATE.md](../../../codex/CONDUCTOR-CLOSE-TEMPLATE.md)).

**Strategy run wrapper (optional):** [STRATEGY-RUN-OPERATOR.md](STRATEGY-RUN-OPERATOR.md) â€” session-scoped `run_id`, derived `state.json` + receipts under `artifacts/`; does not replace or auto-edit /codex files. Shared vocabulary: [run-contract.md](../../run-contract.md).

**Carry harness (optional):** [carry-harness.md](carry-harness.md) â€” derived JSON receipts for task-level intake â†’ artifact presence checks (`scripts/work_strategy/run_carry_harness.py`); not strategic truth.

**Packet validators (optional):** [validator-contract.md](validator-contract.md) â€” structural integrity JSON reports (`scripts/work_strategy/validate_strategy_packet.py`); pre-review hygiene only; can nest under carry harness via `--run-validators`.

**Task-shape routing (optional):** [task-shape-routing.md](task-shape-routing.md) â€” deterministic classification of strategy job kind (`scripts/work_strategy/classify_task_shape.py`); optional `--classify-task-shape` on the carry harness; not model routing.

**Review packet (optional):** [review-packet-template.md](review-packet-template.md) â€” derived handoff JSON/Markdown (`scripts/work_strategy/build_review_packet.py`); consolidates task paths, optional validation/task-shape reports, and review readiness; not Record truth.

**Source-hygiene packets (optional):** [source-hygiene-packets.md](source-hygiene-packets.md) â€” compact operator recipe for turning a live seam into a refined page + hygiene companion before heavier notebook composition.

**Packet-before-synthesis doctrine (optional):** [packet-before-synthesis-doctrine.md](packet-before-synthesis-doctrine.md) â€” slower strategist rule for when mixed seams should be packeted before synthesis, including the dual-register maturity sequence for official-primary lines and attributed gloss.

**Packet crosswalk (optional):** [packet-crosswalk.md](packet-crosswalk.md) â€” quick chooser linking mechanism / process / register packets and dual-register maturity to their actual notebook moves.

**Best re-entry point for half-remembered packet work:** [packet-crosswalk.md](packet-crosswalk.md) â€” start here if you remember the packet-first idea but not which file you need; it routes quickly to the recipe, doctrine, or philosophy layer without rereading the whole stack.

**When elegance becomes dangerous (optional):** [when-elegance-becomes-dangerous.md](when-elegance-becomes-dangerous.md) â€” notebook-philosophy note on when smooth synthesis starts distorting layered seams and packet-first discipline should interrupt it.

**Statecraft workflow retrospective (optional):** [statecraft-root-workflow-retrospective-2026-05-25.md](statecraft-root-workflow-retrospective-2026-05-25.md) â€” operator memo on how the repo-root `statecraft/` kernel would have improved the immediately preceding seven-day build/use cycle, with ten concrete workflow gains.

**Conductor recursive-improvement benchmark (optional):** [conductor-recursive-improvement-benchmark.md](conductor-recursive-improvement-benchmark.md) â€” scorecard and formulas for testing whether named conductor stances plus the four-movement arc are increasing recursive self-improvement power.

**Conductor arc impact journal (optional):** [conductor-arc-impact-journal.md](conductor-arc-impact-journal.md) â€” append-only narrative ledger for benchmark windows, provisional scores, and what changed.

**Conductor novelty claim ladder (optional):** [conductor-novelty-claim-ladder.md](conductor-novelty-claim-ladder.md) â€” safe claims, overclaim boundaries, and the evidence needed to upgrade novelty claims over time.

**Speaker arc / thread / lattice boundaries (optional):** [speaker-arc-thread-lattice-boundaries.md](speaker-arc-thread-lattice-boundaries.md) â€” compact distinction between ranked host × guest lane notes, `thread:<expert_id>` continuity joins, and roster-level lattice rows.

**yt-dlp effectiveness layers (optional):** [ytdlp-effectiveness-layers.md](ytdlp-effectiveness-layers.md) â€” separates extractor success, wrapper success, and inventory failure when auditing YouTube ingest.

**yt-dlp ingest quality rubric (optional):** [ytdlp-ingest-quality-rubric.md](ytdlp-ingest-quality-rubric.md) â€” compact four-part scorecard for discovery, subtitle extraction, provenance wrapper quality, and index sync.

**Repo self-perception (optional):** [repo-self-perception.md](repo-self-perception.md) â€” distinguishes absent corpus, partial corpus, and unrecognized corpus, and treats inventory drift as one case of broader self-description lag.

**Predictive History CIV-MEM context transfer package (optional):** [predictive-history-civmem-context/README.md](predictive-history-civmem-context/README.md) â€” transfer-ready doctrine, templates, voice rules, calibration examples, and a consolidated [implementation handoff](predictive-history-civmem-context/implementation-handoff.md) for later application in the external PH repo.

**Predictive History comment rollout (optional):** [predictive-history-comment-rollout/README.md](predictive-history-comment-rollout/README.md) â€” two-phase public YouTube comment pipeline: chapter-folder doorway first, then `ph-mus` exhibit follow-up when the route exists.

**Carry-stack observability (optional):** [observability.md](observability.md#carry-stack-observability-pr-5) â€” regenerable JSON/Markdown aggregate over runtime receipts/reports (`scripts/work_strategy/summarize_carry_receipts.py`); process metrics only.

**Bottom line:** this tree remains useful as a legacy doctrine and machinery shelf, but it should no longer be taught as the live canonical owner of operator judgment. In the current topology:

- `statecraft/` owns live operator judgment, analytical prose, mechanism, recursive learning, and downstream strategic use
- `/codex` owns chronology, daily continuity, thread/page accumulation, and notebook memory
- `docs/skill-work/work-strategy/` owns compatibility residue until later bounded migrations re-home material more precisely

**Purpose:** preserve the older cross-territory strategy machinery while the repo is re-centered around `statecraft/`. The **[/codex](../../../codex/README.md)** remains the primary chronology artifact where daily continuity is captured; `statecraft/` is now the canonical interpretive and prose-bearing surface above it; this tree supports compatibility, older frameworks, and still-unmigrated machinery.

**Not** a replacement for territory READMEs. **Not** Record truth. Companion gate and knowledge boundary rules still apply.

Predictive History is the public corpus name for the slow transcript spine; `work-jiang` remains only as a legacy compatibility label in older paths and wrappers.

**Check streams / cognition streams coverage ledger (optional):** [cognition-streams-coverage-ledger.md](cognition-streams-coverage-ledger.md) - machine-shaped row schema, formulas, and thresholds for automating month or date-window completeness across the five tracked channels. Use **`check streams`** for the daily operator skill; treat **`cognition streams`** as the broader conceptual/audit namespace and legacy alias.

**Cognition streams audit command (optional):** [cognition-streams-watchlist.json](cognition-streams-watchlist.json) plus `python scripts/cognition_streams_audit.py --start YYYY-MM-DD --end YYYY-MM-DD --recent-start YYYY-MM-DD` - advisory automation that emits discovery receipts, coverage ledgers, summary JSON, and a ranked repair queue without performing ingest.

**Advisory automation maturity classes (optional):** [advisory-automation-visibility-vs-judgment.md](advisory-automation-visibility-vs-judgment.md) - visibility-first doctrine for automation that should illuminate the field and expose repair before attempting stronger judgment.

**Future of ingestion obsolescence (optional):** [future-of-ingestion-obsolescence.md](future-of-ingestion-obsolescence.md) - what parts of today's cognition-streams ingest stack are likely to age badly within 24 months, and what trust/provenance layers are worth building because they should survive the shift to agentic access.

## Forecast integration

Forecast artifacts from [`docs/skill-work/work-forecast/`](../work-forecast/README.md) may be referenced inside work-strategy as planning inputs.

Allowed uses:

- active watch support
- threshold monitoring
- timing judgments
- decision-point framing

Disallowed uses:

- direct Record updates
- converting a forecast into a fact claim
- bypassing proposal and review workflow

Recommended flow:

1. run forecast
2. save artifact
3. write receipt
4. review summary
5. reference in [forecast-watch-log](../../../codex/forecast-watch-log.md) or a [decision point](decision-points/forecast-informed-decision-point-template.md) if useful
6. stage any durable downstream claim separately if needed

**GitHub / gate CI:** [LANE-CI.md](LANE-CI.md) â€” label **`lane/work-strategy`**, gate paste convention (`territory: work-politics` + `channel_key: operator:work-strategy` when using the work-politics **`operator:pol:`** channel bucket), paste-snippet CLI.

### Cursor skills â€” disambiguation

| Intended use | Typical trigger | What it does | Primary artifacts / scripts |
|--------------|-----------------|--------------|-----------------------------|
| **Work-politics territory pulse** | _(no skill â€” run script)_ | Stale docs, brief blockers, gate rhythm, content queue, campaign-facing next actions. | `python3 scripts/operator_work_politics_pulse.py -u grace-mar` (legacy: `operator_wap_pulse.py`) |
| **Weekly brief workflow** | `weekly brief` | **Weekly** brief **readiness**, blockers, optional scaffold generation (not the daily generator). | [weekly-brief-run SKILL](../../.cursor/skills/weekly-brief-run/SKILL.md); `operator_weekly_brief_run.py` |
| **Strategy pass** (`skill-strategy`) | **`strategy`**, **`strategy pass`**, **`work-strategy`** | Cross-territory **judgment** slice: **[../../../codex/](../../../codex/README.md)** first (daily/monthly blocks), then [STRATEGY.md](STRATEGY.md) when promoting watches/log; Islamabad / Rome threads, weak-signal and [analogy-audit](analogy-audit-template.md) flags â€” **not** the pulse script or weekly brief runner. | [../../../codex/](../../../codex/README.md), [STRATEGY.md](STRATEGY.md); [skill-strategy SKILL](../../.cursor/skills/skill-strategy/SKILL.md) |

**Coffee** [Compass](../../.cursor/skills/coffee/SKILL.md) (**C**) can include **work-strategy-rome** (ROME-PASS) but is a **session hub**, not a full strategy pass.

### Strategy session helpers (`skill-strategy`)

Quick index for **Capture**-adjacent surfaces: **narrative register**, **Grok-style prose**, **long-arc placement**, and **standing hypothesis logs** â€” WORK only; weave into knots per [STRATEGY-NOTEBOOK-ARCHITECTURE](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md).

**`strategy-context` (CLI):** Cold-thread re-entry â€” one bounded paragraph (default **â‰¤120 words**) from notebook `days.md` **Open**, inbox accumulator, `daily-brief-YYYY-MM-DD.md` Â§1b, STRATEGY + promotion ladder + commentator index presence â€” or **`--compact`** paths/status only. **`--meta`** adds `chapters/YYYY-MM/meta.md` (month **Theme** excerpt); **`--minds`** adds `minds/README.md` + `minds/outputs` filenames for the date or recent month scaffolds. **`--log`** appends a **`WORK-choice`** receipt to `session-transcript.md` via `log_operator_choice.py` (pointer, not full stdout). **`--recent N`** (or **`--history`** for N=20) appends a **lightweight recent-activity** block after state: merges `strategy-fold-events.jsonl`, **strategy-filtered** `### [WORK-choice]` lines from `session-transcript.md`, and optionally **`--recent-git K`** commits under `docs/skill-work/work-strategy` (merged, sorted by time, truncated to N; omitted if no events). `python3 scripts/strategy_context.py -u grace-mar` Â· `--date YYYY-MM-DD` Â· `--max-words N`

**`strategy_thread` (CLI):** Operator **`thread`** â€” rebuild **`strategy-expert-<expert_id>.md`** rolling ingest blocks from [daily-strategy-inbox.md](../../../codex/daily-strategy-inbox.md) lines that carry **`thread:<expert_id>`**; delegates to `strategy_expert_corpus.py` (**same** `--inbox`, `--threads`, `--out`, `--days`, `--today`, `--dry-run`). **Not** a **`weave`** (no `days.md` / knots). Spec: [STRATEGY-NOTEBOOK-ARCHITECTURE.md Â§ Thread (terminology)](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology). `python3 scripts/strategy_thread.py`

| File | Role |
|------|------|
| [grok-daily-brief.md](grok-daily-brief.md) | Headings-only **magazine layer** on top of generated `daily-brief-YYYY-MM-DD.md`. |
| [../../../codex/trump-religion-papacy-arc.md](../../../codex/trump-religion-papacy-arc.md) | **Trump â†” Christianity / papacy / religion** arc (anchor 2016â†’); placement for **Trumpâ€“Leo** / **`narrative-escalation`** ingests. |
| [../../../codex/rome-persia-legitimacy-signal-check.md](../../../codex/rome-persia-legitimacy-signal-check.md) | Append-only **legitimacy-plane** falsifiers (Romeâ€“Tehran wedge); orthogonal to Hormuz/Islamabad **hard security**. |
| [../../../codex/narrative-escalation-trump-timeline.md](../../../codex/narrative-escalation-trump-timeline.md) | **Stub** â€” canonical content moved to [trump-religion-papacy-arc.md](../../../codex/trump-religion-papacy-arc.md). |
| [skill-strategy / SKILL](../../../.cursor/skills/skill-strategy/SKILL.md) | Â§ **Narrative escalation**, optional **retroactive spine**, **Modes** (Capture / Weave / Promote). |

---

## Contents

| Artifact | Role |
|----------|------|
| **[Strategy session helpers (`skill-strategy`)](#strategy-session-helpers-skill-strategy)** | Compact index subsection **above** (`strategy-context`, **`strategy_thread`** / operator **`thread`**, Grok layer, Trump arc, Romeâ€“Persia signal check, narrative stub, skill-strategy SKILL). |
| **[common-inputs.md](common-inputs.md)** | Shared inputs into work-politics and work-strategy (event ingest, RSS, neutral fact summary, three lenses, gate, operator). |
| **Transcript ingest** | [research/external/work-strategy/transcripts/README.md](../../../research/external/work-strategy/transcripts/README.md) â€” raw or digest `.md`/`.txt` for Perceiver / current-events / LEARN MODE. **Predictive History:** use external-canonical material plus bounded review packets/snapshots; the local [predictive-history/README.md](../../../research/external/youtube-channels/predictive-history/README.md) is a frozen historical reference, not an active sync target. |
| **[external-tech-scan.md](external-tech-scan.md)** | Curated **themes** from long-form tech/business discourse (e.g. GTC, podcasts) â€” strategy vs work-politics angles; **work-dev integration lens:** [../work-dev/external-signals.md](../work-dev/external-signals.md). **Not** canonical news. |
| **[daily-brief-config.json](daily-brief-config.json)** | Feeds (`locale` per feed) + global + per-locale keyword lists (`pol_keyword_phrases_by_locale`, legacy `wap_keyword_phrases_by_locale`, and `strategy_keyword_phrases_by_locale`) for `generate_work_politics_daily_brief.py` â€” **W+S** scoring only; no translation API. **`ingest_caps`** + per-feed **`tier`** (1â€“3) and optional **`max_items`** cap each feed **before** ranking (newest first), so one noisy RSS does not dominate. Optional **`story_dedupe`** clusters headlines that share enough `story_anchor_phrases` overlap (Jaccard + shared anchors) so the same crisis in EN/FR/DE/ES/AR does not flood Â§2; tune thresholds or pass `--no-story-dedupe` for a flat list. CLI **`--max-per-feed N`** overrides every feedâ€™s cap. |
| **[daily-brief-focus.md](daily-brief-focus.md)** | Operator-maintained bullets: what the strategy lane is watching (product, partners, policy). |
| **[daily-brief-native-international-pass.md](daily-brief-native-international-pass.md)** | **Native-language triangulation** for international load-bearing stories (Â§1d / Â§1e / Â§1g / Â§1h + coffee C); one native bullet per jurisdiction alongside wires. |
| **[daily-brief-jiang-layer.md](daily-brief-jiang-layer.md)** | **Slow layer** pointers for external Predictive History review and historical Jiang references embedded in the daily brief as **Â§1c** â€” not breaking news and not a signal to restart local PH production. |
| **[daily-brief-template.md](daily-brief-template.md)** | Spec for the combined daily brief output. |
| **[daily-brief-minds-config.json](daily-brief-minds-config.json)** | Optional Tri-Frame **scaffold** overlays after the daily brief (Barnes / Mearsheimer / Mercouris); strategy-expert **`-mind.md`** paths (SSOT); outputs under [minds/outputs](minds/outputs). See [minds/DAILY-BRIEF-MINDS-WORKFLOW.md](minds/DAILY-BRIEF-MINDS-WORKFLOW.md). |
| **[daily-brief-minds-menu.md](daily-brief-minds-menu.md)** | Human-readable Aâ€“D menus per mind (program order B â†’ M â†’ M). |
| **[brief-source-registry.md](brief-source-registry.md)** | Human-readable source-governance layer for work-strategy: 6 source classes, artifact-by-artifact usage policy (Â§6), corroboration expectations by claim strength (Â§9), transcript discipline (Â§10), historical/civilizational use policy (Â§7), weak-signal source bounds (Â§11), promotion eligibility (Â§8). Complements (does not duplicate) the [work-politics weekly-brief registry](../work-politics/brief-source-registry.md). WORK only. |
| **[weak-signals.md](weak-signals.md)** | Weak-signal discipline: **Â§1f** block, promotion to STRATEGY **Â§II-A / Â§III-A / Â§IV**, analogy audit before overclaiming (WORK only). |
| **[weak-signal-template.md](weak-signal-template.md)** | Markdown stub for **Â§1f** in the daily brief. |
| **[analogy-audit-template.md](analogy-audit-template.md)** | Short form when a historical parallel is proposed (current-events + brief). |
| **[civilizational-strategy-surface.md](civilizational-strategy-surface.md)** | Thin bridge from civilization_memory to strategy-grade objects: 9 lenses, 12 reusable case families, fit/mismatch/falsifier discipline, promotion targets. WORK only. |
| **[faith-science-legitimacy-capability.md](faith-science-legitimacy-capability.md)** | Refines the "faith vs science" intuition into a strategy-grade "legitimacy vs capability" lens, with America / China / Russia / Persia comparison and AI-age implications. WORK only. |
| **[case-index.md](case-index.md)** | Thin local index of reusable strategy-grade historical and civilizational cases (15 initial entries, required template, fit/mismatch/falsifier per case, compression and review protocol). Companion to civilizational-strategy-surface. WORK only. |
| **[decision-point-template.md](decision-point-template.md)** | Structured options when an escalating watch needs a recommendation before promotion. Three-minds perspectives default. |
| **[context-efficiency-layer.md](../context-efficiency-layer.md)** | Cross-lane: hot/warm/cold operator context, recovery links, budgets â€” pairs with [context-compaction-protocol.md](../context-compaction-protocol.md). |
| **[promotion-ladder.md](promotion-ladder.md)** | 7-stage promotion path for civilizational, historical, and strategy-relevant material into reusable work-strategy artifacts (case hit â†’ resonance note â†’ analogy audit â†’ watch support â†’ decision point â†’ doctrine note â†’ optional gate candidate); shortcut, demotion, and compression rules; minimum reasoning standard. **WORK-only**. |
| **[watch-promotion-rules.md](watch-promotion-rules.md)** | When to promote watches and open decision points. |
| **[decision-points/](decision-points/README.md)** | Instance files (`YYYY-MM-DD-slug.md`). |
| **[promotion-policy.json](promotion-policy.json)** | Machine-readable stage ids (v0). |
| **[authorized-sources.yaml](authorized-sources.yaml)** | Machine-readable source registry: 6 source classes, artifact eligibility per source, trust tiers (1â€“4), review rules, maintenance policy. 16 sources (primary, data, reporting, analyst, transcript, operator note). Pairs with [brief-source-registry.md](brief-source-registry.md) (human policy) and [work-strategy-sources.md](work-strategy-sources.md) (URL catalog). |
| **[source-tiers.md](source-tiers.md)** | Trust tier meanings + phased enforcement. |
| **[source-hygiene-packets.md](source-hygiene-packets.md)** | Recipe for refined-page + source-hygiene-note packet pairs; use when a seam is strategically useful but still mixed in evidence quality. |
| **[packet-before-synthesis-doctrine.md](packet-before-synthesis-doctrine.md)** | Durable doctrine note for slower packet-first strategist tempo: mechanism / process / register reuse, anti-flattening discipline, and the dual-register maturity rule. |
| **[packet-crosswalk.md](packet-crosswalk.md)** | **Best re-entry point** for this family: compact chooser mapping packet type to notebook move, then routing to the recipe, doctrine, or philosophy note as needed. |
| **[when-elegance-becomes-dangerous.md](when-elegance-becomes-dangerous.md)** | Philosophy note for seam-first writing: when attractive synthesis becomes smoother than reality and should be interrupted by packet-first discipline. |
| **[conductor-recursive-improvement-benchmark.md](conductor-recursive-improvement-benchmark.md)** | Benchmark spec for measuring whether conductor stances plus the four-movement arc are increasing recursive self-improvement power over time. |
| **[dopamine-flow-agency-benchmark.md](dopamine-flow-agency-benchmark.md)** | Benchmark spec for measuring whether an AI-assisted session improves orientation, momentum, taste, selection pressure, falsifiability, afterglow, and human agency. |
| **[conductor-arc-impact-journal.md](conductor-arc-impact-journal.md)** | Narrative benchmark ledger for conductor-wave, monthly, and quarterly impact reviews. |
| **[conductor-novelty-claim-ladder.md](conductor-novelty-claim-ladder.md)** | Claim-discipline note distinguishing old ingredients, distinctive recombination, plausible implementation novelty, and what evidence would justify stronger public claims. |
| **[observability.md](observability.md)** | Notebook hygiene metrics (`build_strategy_observability.py`) **and** carry-stack runtime summaries (`summarize_carry_receipts.py`). |
| **[strategy-health.md](strategy-health.md)** | How to read observability numbers. |
| **[../WORK-LAYER-HARDENING-ROADMAP.md](../WORK-LAYER-HARDENING-ROADMAP.md)** | Full work-layer sequencing (strategy â†’ dev â†’ cadence â†’ dashboard). |
| **[current-events-analysis.md](current-events-analysis.md)** | Standard workflow for converting live events into disciplined strategy judgment: Perceiver (neutral fact summary) â†’ verify seam â†’ event classification â†’ case-index check â†’ energy-chokepoint hook â†’ analyst (structured breakdown) â†’ resonance note or analogy audit â†’ watch-support decision â†’ decision-point trigger â†’ three minds â†’ synthesis â†’ optional deliberation receipt. 11 sections including failure modes and operator checklist. **WORK only**. |
| **[STRATEGY.md](STRATEGY.md)** | WORK-only ledger: CORE / **Â§II-A active watches** / SCHOLAR / **Â§III-A analogy watchlist** / **Â§IV operator strategy log** (additive notes in-file; not CMC `MEMâ€“*` shards); not Record. |
| **[../../../codex/](../../../codex/README.md)** | **Page-first operator notebook** for strategy judgment â€” knots are atomic pages; `days.md` = chronology; PH-style month chapters (`chapters/YYYY-MM/`), [architecture](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md), [STATUS](../../../codex/STATUS.md); **`### History resonance`** wires [history-notebook](history-notebook/README.md) chapter ids into knots. Not [work-strategy-history](work-strategy-history.md). WORK only. |
| **[theology-notebook/](theology-notebook/README.md)** | **Theology** â€” define the operatorâ€™s own beliefs through **writing** the book; [LIB-0159](../../../self-library.md#operator-analytical-books); [research](theology-notebook/research/), [ideas](theology-notebook/ideas/); **not** a substitute for governed theology entries in the library surface (legacy path: `self-library.md`). WORK only. |
| **[../../../codex/daily-strategy-inbox.md](../../../codex/daily-strategy-inbox.md)** | **SSOT** for **X / strategy ingest** scratch: cadence, **paste-ready one-liner** shape, default assistant target. Weave at **dream** â†’ `days.md` ([architecture](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md) Â§ *Daily strategy inbox*). |
| **[LEARN_MODE_RULES.md](LEARN_MODE_RULES.md)** | LEARN MODE adapter: Tri-Frame protocol, extraction format, governance aligned with STRATEGY Â§VI. |
| **[LEARN_MODE_OPERATOR_PROMPT.md](LEARN_MODE_OPERATOR_PROMPT.md)** | Copy-paste operator / Composer prompt for work-strategy sessions and LEARN MODE. |
| **[minds/](minds/README.md)** | Tri-Frame entry stubs (Mercouris, Mearsheimer, Barnes) â†’ `CIVâ€“MINDâ€“*.md` in civilization_memory. Advisory patterns: [minds/MINDS-SKILL-STRATEGY-PATTERNS.md](minds/MINDS-SKILL-STRATEGY-PATTERNS.md). |
| **[manifest-principles.md](manifest-principles.md)** | Operator principles (truth > persuasion, triangulation, energy-chokepoint mandatory, etc.). |
| **[persuasive-content-pipeline.md](persuasive-content-pipeline.md)** | Ingest â†’ energy-chokepoint flags â†’ Council â†’ Triangulation â†’ Draft; staged for approval. |
| **[synthesis-engine.md](synthesis-engine.md)** | Spec for mind-synthesis after three lenses; prototype: `research/prototypes/mind-synthesis.py`. |
| **[multi-agent-fork-generator.md](multi-agent-fork-generator.md)** | Experimental two-pass / subagent richer WORK menus; token budget; human still picks one branch. |
| **[../work-menu-conventions.md](../work-menu-conventions.md)** | Cursor WORK multiple-choice shape (evidence links, tags, choice log to `session-transcript`). |
| **[modules/energy-chokepoint/](modules/energy-chokepoint/manifest.md)** | Energy-chokepoint monitoring (manifest + perceiver-hook); mandatory for energy-related events. |
| **[modules/economic-blowback/](modules/economic-blowback/guardrail-test.md)** | Guardrail checklist for inflation/gas/oil content (everyday impact, CIV-MEM, tone). |
| **[modules/verifiable-personal-ai/](modules/verifiable-personal-ai/manifest.md)** | Operator deliberation receipts â€” auditable pipeline trace (WORK only; not crypto proof). |
| **[modules/moonshot-orchestration/](modules/moonshot-orchestration/README.md)** | WORK-only moonshot mapping module: source-tier assessment, contribution maps, boundary checks, dashboard entries, and optional gated proposals. Not Record truth; not a canonical skill. |
| **[work-moonshots/](../work-moonshots/README.md)** | **work-moonshots** lane â€” PMOS templates + [Moonshot Orchestration](../work-moonshots/moonshot-orchestration/README.md) (maps, source tiers, dashboard, optional gated proposals). Not Record. |
| **[work-strategy-rome/](work-strategy-rome/README.md)** | WORK project: Vatican / papal soft power and moral-diplomatic signals vs multipolar and Western-legitimacy themes ([manifest](work-strategy-rome/manifest.md), pre-skill [ROME-PASS](work-strategy-rome/ROME-PASS.md)). |
| **[founding-influences-graeco-roman-vs-english.md](founding-influences-graeco-roman-vs-english.md)** | Working paper: classical-republic vs English constitutional idiom on a 32-unit founding corpus (rubric + lexical methods; `scripts/founding_lexical_compare.py`). Not Record. |
| **[islamabad-operator-index.md](islamabad-operator-index.md)** | **Islamabad bundle â€” operator index:** single bookmark listing all Islamabad artifacts (this lane + [Predictive History intake](../../../codex/predictive-history/intake/Islamabad-5-point-reconciliation-plan-with-jiang-commentary.md)). **Not** work-cici. WORK only. |
| **[islamabad-framework.md](islamabad-framework.md)** | **Islamabad Framework** â€” diplomatic working document (not treaty): six sections, formal register, Â§6 implementation sequence, dual-audience architecture. WORK only. |
| **[islamabad-framework-summary.md](islamabad-framework-summary.md)** | **Islamabad Framework â€” summary**: short cover note (~150 words) for social media, email, and channel propagation. Preserves the Leo XIV named reference. WORK only. |
| **[islamabad-framework-operator-edition.md](islamabad-framework-operator-edition.md)** | Same framework â€” **operator edition**: annexes, Jiang commentary block, Leo XIV rhetoric blend, rubric / phase notes, distribution checklist. See [us-framed-five-point-gulf-peace-framework-2026-04-08.md](us-framed-five-point-gulf-peace-framework-2026-04-08.md) and [Predictive History intake](../../../codex/predictive-history/intake/Islamabad-5-point-reconciliation-plan-with-jiang-commentary.md). WORK only. |

---

## Daily brief

**Output name:** `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (example: `daily-brief-2026-03-29.md`). See [daily-brief-template.md](daily-brief-template.md).

**Template SSOT (single source of truth):** [daily-brief-template.md](daily-brief-template.md) is the **authoritative** spec for the combined generator output. [work-politics/daily-brief-template.md](../work-politics/daily-brief-template.md) is a **compatibility pointer** (same content as a stubâ€”do not duplicate the full spec there). [work-template/daily-brief-template.md](../work-template/daily-brief-template.md) is the **cross-lane semantic** scaffold; its numbered mapping points back here.

### Regenerate a dated brief without losing post-process tails

When you have already written a **`## 2c. Narrative layer retrofit`** tail (and optional **`## 8. Quality rubric footer`** bundled after it), use the merge helper so a regen does not erase operator work:

```bash
python3 scripts/merge_daily_brief_postprocess.py -u grace-mar --date YYYY-MM-DD --no-fetch
```

- **`--no-fetch`** is the safer default for â€œtemplate/config changed, re-render spineâ€ work; omit it only when you intentionally want a fresh RSS pull (expect headline drift vs the original capture day).
- **`--force`** strips any duplicate **`## 2c. Narrative layer retrofit`** tail from the freshly generated base before splicing the preserved post-process material.
- **Tail cleanup (built-in):** if an older brief accidentally folded **`## 3`â€“`## 7`** stubs after **`## 2c`** (before **`## 8`**), the merge script removes that duplicate outline from the preserved tail and drops a **trailing** duplicate `_Generated by â€¦ daily-brief-config.json` signature when present (the regenerated base already emits the signature once before **`## 2c`**).
- Generator detail flag: **`--brief-date YYYY-MM-DD`** on `scripts/generate_work_politics_daily_brief.py` (see [daily-brief-template.md](daily-brief-template.md) **Generate** section).

Portable draft skill: [`skills-portable/_drafts/daily-brief-regen-merge/SKILL.md`](../../skills-portable/_drafts/daily-brief-regen-merge/SKILL.md).

**Brief source registry:** Weekly-brief source readiness is tracked in [work-politics/brief-source-registry.md](../work-politics/brief-source-registry.md) (operator WPC rhythm). The [work-strategy brief-source-registry](brief-source-registry.md) governs how sources are used inside this lane â€” source classes, artifact-level usage policy, corroboration expectations, transcript discipline, and historical/civilizational use bounds.

One script covers **work-politics + work-strategy**:

```bash
python scripts/generate_work_politics_daily_brief.py -u grace-mar \
  -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md
```

Default config path: `docs/skill-work/work-strategy/daily-brief-config.json`.

**Ranked morning forks (gate + memory signals):** `python3 scripts/suggest_morning_forks.py -u grace-mar` (see `--markdown`, `--llm`). **Menu evolution:** `python3 scripts/menu_choice_evolution.py -u grace-mar --days 30`.

**Foreign-language feeds:** Each feed may set `"locale": "fr"` (etc.). Phrases in `pol_keyword_phrases_by_locale` (legacy `wap_*`) / `strategy_keyword_phrases_by_locale` are **added** to the global lists when scoring that feedâ€™s items (substring match on the original headline). Non-`en` locales are shown in the headline line (`Â· _fr_`). Tuning those lists is the **zero-API** way to align ranking with non-English copy; a future optional path could add translated-title scratch for scoring only.

**Ingest volume:** `ingest_caps.default_max_items_per_feed` and `max_items_by_tier` apply when a feed has no explicit `max_items`. Tier **1** = core US/congress feeds; **2** = international language feeds; **3** = long-tail (e.g. HN). Explicit `max_items` on a feed wins over tier.

**Same-story grouping:** After ranking, items can be clustered by anchor overlap on `title + link` (default anchor list in the script; optional `story_anchor_phrases` in JSON extends it). This is **not** semantic dedupeâ€”raise `jaccard_min` / `min_shared_anchors` if clusters feel loose; disable via config `story_dedupe.enabled: false` or CLI `--no-story-dedupe`.

**Operator habit:** Starting Cursor with **`coffee`** runs warmup in [.cursor/skills/coffee/SKILL.md](../../.cursor/skills/coffee/SKILL.md) (see bootstrap); legacy **`hey`** still works. **Generating** today's daily brief to `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` is **coffee menu C â€” Strategy (daily brief)** â€” Step 1 does **not** run the generator.

### Daily brief mind overlays

After `daily-brief-YYYY-MM-DD.md` exists, the operator may run optional **Tri-Frame mind scaffolds** (same generator; **scaffold-only** â€” no LLM inside the script):

- **Config:** [daily-brief-minds-config.json](daily-brief-minds-config.json)
- **Mind fingerprints (SSOT):** `strategy-expert-barnes-mind.md`, `strategy-expert-mearsheimer-mind.md`, `strategy-expert-mercouris-mind.md` under [`../../../codex/`](../../../codex/) â€” [`../../../codex/minds/CIV-MIND-*.md`](../../../codex/minds/) redirect to the same bodies (see [minds/README.md](minds/README.md))
- **Outputs:** `docs/skill-work/work-strategy/minds/outputs/` â€” dated sidecar files; complete analysis in Cursor or a **`strategy`** pass
- **CLI:** `scripts/generate_wap_daily_brief.py` â€” `--offer-minds`, `--mind`, `--mind-option`, `--mind-all`, `--brief-path`, `--skip-brief` (see [minds/DAILY-BRIEF-MINDS-WORKFLOW.md](minds/DAILY-BRIEF-MINDS-WORKFLOW.md))

### X post strategy ingest

Cadence, **paste-ready** micro-format, and default on-disk target for chat ingests: **[../../../codex/daily-strategy-inbox.md](../../../codex/daily-strategy-inbox.md)** (SSOT). Optional session receipt: [work-menu-conventions Â§ Auditing picks](../work-menu-conventions.md#6-auditing-picks-choice-journal).

---

## Boundaries

- **WORK only** â€” drafts, briefs, commercial context.
- **Generic pattern library** (tiers, ledger shape, mapping): [work-template/README.md](../work-template/README.md).
- **Triangulation** for political copy stays under [work-politics/analytical-lenses](../work-politics/analytical-lenses/manifest.md).
- **Merge to Record** only via RECURSION-GATE + companion approval.

