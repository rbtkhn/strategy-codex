# Future Of Ingestion Obsolescence

This note is about what parts of the current cognition-streams ingest stack are likely to age badly within the next 24 months, and what parts are worth hardening because they should survive the transition.

The key distinction is simple:

- the fragile layer is **how we reach the field**
- the durable layer is **how we describe, score, and trust what we reached**

Current ingest pain has exposed that difference clearly. The April 2026 benchmark failure was not mainly a failure of ledger math, repair queues, or provenance logic. It was a failure of one specific access assumption: that unauthenticated YouTube metadata could be relied on for month-scale historical dating.

That matters because the likely frontier trajectory is not "no ingestion," but **less brittle ingestion**:

- authenticated browser-use agents
- multimodal video understanding
- longer-context models that can reason over larger raw windows directly
- connector / MCP-style direct access to systems of record
- better advisory ranking of what matters most

Under that trajectory, the repo should stop treating today's extraction method as the center of gravity.

## What to stop investing in

- Heavy dependence on unofficial handle-page scraping.
- Filename-led retrospective reconstruction.
- Deep refinement of title/runtime heuristics as though they are a stable foundation.
- Month-audit machinery that still depends on hostile unauthenticated per-video enrichment for every item.
- Treating transcript capture as the main bottleneck.

These may remain temporarily useful, but they are poor candidates for heavy doctrinal or engineering investment.

## What to keep building

These look durable even if the access layer changes:

- canonical watchlist / registry discipline
- row-level ledger schema
- stable classifications such as `captured-main`, `uncaptured-main`, `hidden-companion`, `hidden-short`, and `upcoming`
- provenance-first matching by stable ids and frontmatter `source_url`
- numeric thresholds such as `overall_pct`, `recent_pct`, and `must_capture_remaining`
- repair-queue generation
- offline rerun from saved receipts
- explicit separation between visibility automation and judgment automation

These are good investments because they describe the **governance of trust**, not the quirks of one current extractor.

## What to wait for frontier tooling to solve

The repo should be cautious about overbuilding local substitutes for areas where frontier systems are already advancing quickly:

- authenticated browsing of hostile web surfaces
- reliable historical recovery from browser state or first-party interfaces
- direct multimodal understanding of videos without transcript-first workflows
- better significance ranking of missed items
- standard connector-based access where platforms permit it

The likely pattern is that local systems will still need thin adapters, but should avoid becoming overcommitted to today's brittle workaround stack.

## Practical rule

Build around **portable visibility contracts**, not around today's extraction method.

That means:

- keep extraction adapters thin and replaceable
- keep investing in ledgers, receipts, scoring, repair queues, and provenance
- assume the discovery layer will be swapped or supplemented within 24 months

## Strategic bet

The durable asset is not "our scraper."

The durable assets are:

- our classification language
- our evidence thresholds
- our operator trust model
- our local provenance spine

Those should survive a transition from scraping toward agentic access, multimodal understanding, and connector-mediated retrieval.

## Design law

When a capability is likely to be obsoleted by better access technology, invest in the **trust contract** above it rather than the brittle workaround beneath it.
