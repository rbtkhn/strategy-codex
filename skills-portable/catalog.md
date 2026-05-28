# Portable Skill Catalog

This catalog is a discovery layer for selected portable skills and drafts.

Canonical method still lives in:

- `skills-portable/<skill>/SKILL.md`
- `skills-portable/_drafts/<skill>/SKILL.md`
- [skill-candidates.md](skill-candidates.md)

Wrapper contract: [docs/skills/workflow-wrapper-schema.md](../docs/skills/workflow-wrapper-schema.md)

---

## ideation-engine

- **What it is**
  - Approval-first Top 3 opportunity briefs grounded in existing lanes, assets, and source-backed signals.
- **When to use it**
  - Use when you want a weekly opportunity brief, a lane-aware opportunity scan, or a concise recommendation before investing time or reputation.
- **Inputs you'll need**
  - Active lanes, recent work, source library, budget constraints, and the host approval process.
- **What you get**
  - Three scored opportunity briefs, one recommended move, and a reversible first step.
- **Boundary**
  - Proposes only. Does not execute, spend, publish, spawn lanes, or bypass human approval.
- **Current status**
  - `promoted`

Canonical method: [skills-portable/ideation-engine/SKILL.md](ideation-engine/SKILL.md)

---

## abundance-native-ventures

- **What it is**
  - A governed venture-idea and sprint-pack skill for abundance-oriented operator work.
- **When to use it**
  - Use when you want venture ideas, one-afternoon sprint plans, approval packets, or compact operator briefs from existing capabilities and evidence.
- **Inputs you'll need**
  - Operator profile, source library, skill inventory, receipts, and any lane-specific docs.
- **What you get**
  - A small venture set, a sprint package, an approval packet, or a reusable operator brief.
- **Boundary**
  - Keeps risk visible, narrows when evidence is thin, and does not rewrite identity or Record-bearing files.
- **Current status**
  - `promoted`

Canonical method: [skills-portable/abundance-native-ventures/SKILL.md](abundance-native-ventures/SKILL.md)

---

## cici-ai-daily-brief

- **What it is**
  - A bounded-source cohort brief skill for generating a private digest plus a Telegram-ready daily message.
- **When to use it**
  - Use when a beginner-heavy group needs a short operating brief that rewards proof, routes action, and ends with one concrete reply ask.
- **Inputs you'll need**
  - Community dashboard, progress lane, team-chat lane, evidence notes, and member or contributor profiles.
- **What you get**
  - An operator digest, a public five-block message, and a narrower brief when evidence is weak.
- **Boundary**
  - Does not turn self-report into proof, does not hide confidence differences, and does not replace weekly governance review.
- **Current status**
  - `draft`

Canonical method: [skills-portable/_drafts/cici-ai-daily-brief/SKILL.md](_drafts/cici-ai-daily-brief/SKILL.md)

---

## graceful-constraint-reporting

- **What it is**
  - A reporting-discipline skill that keeps a generated brief honest when sources are stale, incomplete, or mixed-confidence.
- **When to use it**
  - Use when an automated update risks sounding stronger than the evidence layer beneath it.
- **Inputs you'll need**
  - The report surface, its authority source, its digest/public split, and any freshness or evidence gaps.
- **What you get**
  - A narrowed, constraint-safe report shape with visible degradation instead of polished bluffing.
- **Boundary**
  - Preserves authority versus derived surfaces and does not let the public layer claim more than the digest allows.
- **Current status**
  - `draft`

Canonical method: [skills-portable/_drafts/graceful-constraint-reporting/SKILL.md](_drafts/graceful-constraint-reporting/SKILL.md)

---

## first-wave-service-sales

- **What it is**
  - A first-contact sales skill for turning a bounded service offer into a real shortlist, first sends, logged contact, and clean reply routing.
- **When to use it**
  - Use when the offer and package already exist and the real task is moving from planning into the first live outreach wave.
- **Inputs you'll need**
  - Offer surface, proof packet, buyer map, prospect shortlist, and pipeline sheet.
- **What you get**
  - A first-batch send plan, personalized outreach logic, logging discipline, objection capture, and call or proposal handoff rules.
- **Boundary**
  - Does not invent demand, does not treat internal demos as client proof, and does not widen a bounded service into generic consulting.
- **Current status**
  - `promoted`

Canonical method: [skills-portable/first-wave-service-sales/SKILL.md](first-wave-service-sales/SKILL.md)

---

## statecraft-source-intake

- **What it is**
  - A statecraft archive-intake skill for landing full transcript-bearing source objects into the canonical `source-archive/statecraft` tree with the correct family pattern.
- **When to use it**
  - Use when the operator already has a pasted transcript or transcript-bearing source object and the main job is placing it correctly, honestly, and without summary/stub drift.
- **Inputs you'll need**
  - Source URL, transcript body, publication date if known, and the nearest existing family examples.
- **What you get**
  - A real full-source archive object with the right filename/frontmatter family, truthful provenance, and archive-only placement.
- **Boundary**
  - Does not fetch YouTube captions, does not clean to study-grade derivative form, and does not route, summarize, or synthesize in `statecraft/`.
- **Current status**
  - `promoted`

Canonical method: [skills-portable/statecraft-source-intake/SKILL.md](statecraft-source-intake/SKILL.md)

---

## monthly-deepening

- **What it is**
  - A month-by-month corpus deepening skill for inventory, missing-item selection, transcript classification, and bounded archive materialization.
- **When to use it**
  - Use when you want a monthly split for a speaker or stream, a truthful list of present versus missing entries, or a repeatable deepening pass after transcript uploads.
- **Inputs you'll need**
  - Month scope, speaker scope, local archive evidence, local receipts, and any pasted transcript bodies.
- **What you get**
  - A scoped month inventory, an honest missing list, bounded materialization of pasted transcripts, and month-slice commit discipline when requested.
- **Boundary**
  - Keeps `speaker-only` separate from `speaker-adjacent`, does not guess unrecovered URLs, and treats transcript uploads as materialization requests unless reporting-only was explicit.
- **Current status**
  - `promoted`

Canonical method: [skills-portable/monthly-deepening/SKILL.md](monthly-deepening/SKILL.md)

---

## strategy-notebook-expert-cross-weave

- **What it is**
  - A WORK-only cross-expert seam skill that folds two expert-thread ingests into one dated notebook judgment surface.
- **When to use it**
  - Use when two expert lines should become one explicit seam without collapsing their evidence chains or pretending false convergence.
- **Inputs you'll need**
  - Expert roster, daily inbox, calendar notebook, month meta, and a status or recent-work receipt surface.
- **What you get**
  - A dated seam with signal, judgment, links, and open hooks, plus optional batch-analysis grep anchors.
- **Boundary**
  - WORK only; not SELF, not EVIDENCE, and not Record staging.
- **Current status**
  - `promoted`

Canonical method: [skills-portable/strategy-notebook-expert-cross-weave/SKILL.md](strategy-notebook-expert-cross-weave/SKILL.md)

---

## statecraft-helix-synthesis

- **What it is**
  - A helix-first statecraft synthesis skill for building canonical-family notes, retrieval surfaces, and meta-synthesis layers above mature lane objects.
- **When to use it**
  - Use when academy-statecraft has already reached a real lane layer and the next move is cross-lane synthesis, orientation/routing, or architecture-class comparison.
- **Inputs you'll need**
  - Lane helixes, first-wave strand objects, migration control-plane notes, and the inventory generator.
- **What you get**
  - A new family, routing, or meta-surface artifact plus synchronized control-plane metrics and a clearer next wedge.
- **Boundary**
  - WORK only; not Record, not PH-CIV authoring, and not raw CIV-MEM backfill.
- **Current status**
  - `promoted`

Canonical method: [skills-portable/statecraft-helix-synthesis/SKILL.md](statecraft-helix-synthesis/SKILL.md)

---

## arc-to-chapter-seeds

- **What it is**
  - An upstream extraction skill for turning a speaker arc, lane arc, or cross-host arc into additive chapter-seed ideas with clean attribution.
- **When to use it**
  - Use when the operator wants chapter ideas harvested from an arc without letting that arc silently govern the destination volume or lane architecture.
- **Inputs you'll need**
  - A real arc on disk, its strongest raw-input or theme support, and the upstream seed surface that will receive the harvested ideas.
- **What you get**
  - A detailed bridge note, an additive seed-list section, or an attribution-correction pass that preserves chapter-generating ideas.
- **Boundary**
  - WORK only; not Record, not destination-corpus doctrine, and not a substitute for full chapter writing.
- **Current status**
  - `promoted`

Canonical method: [skills-portable/arc-to-chapter-seeds/SKILL.md](arc-to-chapter-seeds/SKILL.md)
