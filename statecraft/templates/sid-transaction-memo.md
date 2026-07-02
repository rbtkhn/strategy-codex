# SID Transaction Memo Template

Use for **Statecraft Intelligence Desk (SID)** crisis-week or retainer **Transaction Memo** deliverables — lighter than the full [statecraft-transaction](statecraft-transaction.md) instrument. Partner-review shape: pin-cites, escalation ladder, explicit falsifiers.

**Formal name:** Transaction Memo · **Retainer context:** included in Desk Retainer (2/month) or à la carte.

---

```yaml
---
title: ""
sid_deliverable: transaction-memo
embargo: client-only  # public-ok | client-only | internal-only
theater: ""           # e.g. Iran escalation / Gulf shipping / CFIUS China exposure
matter_date: YYYY-MM-DD
---
```

## Matter Question

One sentence: what decision or client escalation does this memo support?

## Executive Read

Three to five bullets — load-bearing judgment only. No wire recap.

## Escalation Ladder

| Tier | Trigger | Implication for client matter |
| --- | --- | --- |
| 1 — Baseline | | |
| 2 — Elevated | | |
| 3 — Crisis | | |

## Pin-Cites (receipts)

| Claim | Grade | Source | URL or archive path |
| --- | --- | --- | --- |
| 1 | supported / contested / partial | | |

## Falsifiers

- **F1:** … — if true, downgrade executive read to …
- **F2:** … — if true, reopen tier …

## Off-Ramp / Review Trigger

When to revisit (date, event, or wire hook).

## Disclaimer

*Statecraft Intelligence Desk provides geopolitical intelligence support and draft background memoranda for the Firm's internal professional use. Vendor is not legal counsel to the Firm or its clients. The Firm is solely responsible for all legal advice, compliance determinations, and client communications. Deliverables are judgment support, not investment advice.*

---

**Method line (attach on send):** *Governed brief with source receipts and explicit falsifiers — not a wire summary.*

**Validate:** `python scripts/validate_sid_transaction_memo.py --path <file>`
