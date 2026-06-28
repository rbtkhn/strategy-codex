# SID Desk Offer — Spine

WORK only. Operator offer architecture for **Statecraft Intelligence Desk (SID)**. Not Record truth. Not proof of market demand.

## Governing name

| Layer | Name |
|-------|------|
| **Client-facing product** | **Statecraft Intelligence Desk** |
| **Informal acronym** | **SID** — spell out on first use in contracts and external copy |
| **Daily deliverable (formal)** | **Situation Brief** |
| **Daily deliverable (informal / internal)** | **SID Brief** — after first use, spell out *Situation Brief (SID Brief)* |
| **Delta block (script output)** | **Situation Brief — changes since [prior date]** (short: **Situation update** or **SID Brief — delta**) |
| **Weekly deliverable** | **Desk Synthesis** |
| **Memo deliverable** | **Transaction Memo** |
| **Method (one line, secondary)** | Governed intelligence harness — source truth, bounded synthesis, ship receipts |
| **Internal operator / repo** | `strategy-codex` — not client-facing |
| **Legacy (do not use client-facing)** | ~~Intelligence Monitor~~ |

**Usage rules for SID Brief:**

- **First mention** in external doc, contract, or email: **Situation Brief** (*SID Brief*).
- **Repeat mentions** in same thread, operator notes, filenames, cadence logs: **SID Brief** OK.
- **Invoice line (formal):** *Statecraft Intelligence Desk — Situation Brief* (not "SID Brief" alone on first contract page).
- **Script / repo:** `statecraft_situation_brief_delta.py`; optional artifact prefix `sid-brief-`.

**One-line descriptor (external):**

Governed geopolitical judgment with source receipts — daily Situation Brief, weekly Desk Synthesis, and transaction memos for professionals who must survive partner review. Not a news feed. Not legal advice.

## What SID is not

- Not software access or repo licensing
- Not a wire replacement (Bloomberg, Reuters stay client-side)
- Not legal advice, investment advice, or counsel of record
- Not unlimited chat or 24/7 coverage at base retainer
- Not the singularity-academy AI workflow sprint (different buyer, different SKU)

## SKU stack

| SKU | Price (indicative) | Includes | Excludes |
|-----|-------------------|----------|----------|
| **Desk Retainer** | **$10,000 / month** | Up to 3 named theaters; daily **Situation Brief**; weekly **Desk Synthesis**; 2 transaction memos; 2× 45-min office hours | Cyber/compliance module; client-facing legal conclusion; multi-seat platform |
| **Desk Pilot** | **$10,000 / 30 days** | Same scope as retainer, one theater if buyer wants tight wedge | Auto-renew unless converted |
| **Annual prepay** | **$100,000 / year** | Full retainer; two months effective discount | — |
| **Surge Week** | **+$2,000–5,000** | 48h turnaround; extra memo slot; crisis-week cadence | Default retainer SLA |
| **Transaction Memo (à la carte)** | Quote | Single accountable object on named question | Only after relationship or explicit SOW |

## Buyer archetypes (priority order)

| Archetype | Pain | Why $10k clears | Wave |
|-----------|------|-----------------|------|
| **Law — sanctions / CFIUS / nat-sec** | Client escalation outruns associate research; partner rewrite burden | Bill-through math; mark-up-friendly background objects | 1 |
| **Energy / commodity desk** | Escalation premia vs risk committee; no reopenable weekly object | One bad week > annual retainer | 1 |
| **Existing audience → private desk** | Public cadence vs decision copy; liability on hot takes | Trust already earned | 1 |
| **Media / public operator** | Publish gate vs wire speed | Citation/retraction risk | 2 |
| **Allocator / macro overlay** | Tail-risk lacks daily synthesis with verify status | PM second brain | 2 |
| **VC / PE geo overlay** | Deal kill criteria ad hoc | Portfolio ops intro | 3 |

**First-wave send order (from prospect map):** warm audience lead → Steptoe-class sanctions → Hartree-class energy → Gibson Dunn-class CFIUS → Real Clear defense/energy beat → Freepoint-class desk → Locals peer with paid tier.

## Competitive posture (summary)

| Incumbent | SID position |
|-----------|--------------|
| **RANE / Stratfor** | Library + platform; SID = client-shaped escalation memos on **named theaters** |
| **Bloomberg / Reuters** | Events; SID = **objects** with falsifiers for partner review |
| **Geopolitical Desk / Intel Desk** | Cheap feed or aggregation; SID = **managed judgment** at retainer price |
| **Associates** | Wrong artifact type; SID = fixed cost vs crisis-week hours |
| **Internal AI (Copilot / Harvey)** | Firm drafts; SID = live theater objects + receipts — parallel test, not duplicate platform |

Full table: [sid-desk-competitive-comparison.md](sid-desk-competitive-comparison.md) *(planned)*.

## Artifact authority (what we sell)

| Output | Authority class | Client use |
|--------|-----------------|------------|
| **Situation Brief** (*SID Brief*) | Operating context + day-over-day delta | Internal; daily rhythm |
| **Desk Synthesis** | Bounded analytical object | Internal; partner briefing |
| **Transaction Memo** | Draft background for review | Partner mark-up; not client-ready legal opinion unless firm adopts |
| **Office hours** | Directed Q&A on named theaters | Clarify object, not open-ended chat |

## Operator tooling (repo)

| Tool | Purpose |
|------|---------|
| [statecraft_situation_brief_delta.py](../../../scripts/statecraft_situation_brief_delta.py) | Emit **Situation Brief — changes since [date]** from wire-verify / 72h fork grades |
| [sid-transaction-memo.md](../../../statecraft/templates/sid-transaction-memo.md) | Transaction Memo template |
| [validate_sid_transaction_memo.py](../../../scripts/validate_sid_transaction_memo.py) | Partner-review shape check |
| [validate_sid_embargo.py](../../../scripts/validate_sid_embargo.py) | Optional `embargo:` frontmatter when publishing same day |

**Method line (attach on every deliverable):** *Governed brief with source receipts and explicit falsifiers — not a wire summary.*

## Doc map (package tree)

Mirror proportion of [singularity-academy sprint tree](singularity-academy-sprint-one-page-packet.md) — spine → sendable surfaces → pipeline → call/proposal → proof.

| Status | Path | Purpose |
|--------|------|---------|
| **live** | [sid-desk-offer-spine.md](sid-desk-offer-spine.md) | This file — name, SKUs, archetypes, hierarchy |
| **live** | [sid-desk-one-page-packet.md](sid-desk-one-page-packet.md) | First send / “send the one-pager” |
| planned | `sid-desk-competitive-comparison.md` | RANE / wire / associate / internal AI table |
| planned | `sid-desk-objection-cheat-sheet.md` | Call cheat sheet — objection → pivot → close |
| planned | `sid-desk-objection-scripts.md` | Verbatim call scripts (RANE, associates, price, wire, legal, internal AI) |
| planned | `sid-desk-prospect-pipeline.md` | First 20 names, stages, send metadata |
| planned | `sid-desk-first-wave-send-checklist.md` | Pre-send honesty + logging |
| planned | `sid-desk-discovery-call.md` | Qualification + workflow-fit |
| planned | `sid-desk-pilot-sow-excerpt.md` | GC packet — disclaimer, UPL, embargo, liability cap |
| planned | `sid-desk-proof-packet-outline.md` | 7-day sample week spec |
| planned | `sid-desk-client-theater-profile.md` | **Deferred** until first pilot SOW |
| planned | `sid-desk-export-lane.md` | **Deferred** until first 48h sample request |
| planned | `sid-desk-pilot-checklist.md` | **Deferred** until first signed pilot |
| planned | `sid-desk-faq.md` | Post-packet objections |
| planned | `sid-desk-external-packet.md` | Plain-text forwardable bundle (no repo framing) |

**Send discipline:** No first-wave outreach until **one-pager** + **pilot SOW excerpt** exist. Proof packet before enterprise procurement conversations.

## Internal / external boundary

| Surface | SID naming |
|---------|------------|
| Invoice / MSA | Statecraft Intelligence Desk — Managed Service Retainer |
| Email signature | Statecraft Intelligence Desk |
| Procurement category | Professional services — not software license |
| Method footnote | Powered by governed intelligence harness (internal: strategy-codex) |

## Related repo doctrine (operator only)

- [intelligence-harness.md](../../intelligence-harness.md) — method vocabulary
- [product-identity.md](../../product-identity.md) — interpretive machine identity
- [first-wave-service-sales SKILL](../../../skills/first-wave-service-sales/SKILL.md) — send-stage discipline

## Falsifier

**Offer spine is wrong if:** first paid pilot closes on “platform access” or “AI subscription” language instead of **Desk retainer + named theaters + transaction memos**.
