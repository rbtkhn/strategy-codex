"""Tests for scripts/validate_sid_transaction_memo.py."""

from __future__ import annotations

import sys
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_sid_transaction_memo import validate_memo_file  # noqa: E402

VALID_MEMO = """---
title: Gulf shipping escalation
sid_deliverable: transaction-memo
embargo: client-only
theater: Gulf shipping / Hormuz
matter_date: 2026-06-16
---

## Matter Question

Can the firm advise a charter client that Hormuz toll-free language is binding for 60 days?

## Executive Read

- MOU electronic sign landed 16 Jun; formal Geneva sign 19 Jun still open.
- Toll-free vs fee lane **contested** on wire (ABC vs Mehr draft).

## Escalation Ladder

| Tier | Trigger | Implication for client matter |
| --- | --- | --- |
| 1 — Baseline | Electronic MOU only | Monitor charter clauses |
| 2 — Elevated | Geneva slip | Reopen force majeure memo |
| 3 — Crisis | Kinetic Hormuz incident | Client call same day |

## Pin-Cites (receipts)

| Claim | Grade | Source | URL or archive path |
| --- | --- | --- | --- |
| 60-day toll-free carry | contested | ABC Jun 16 | https://example.com/abc |

## Falsifiers

- **F1:** Signed MOU text publishes fee lane — downgrade toll-free read.
- **F2:** IDF Lebanon ops breach MOU clause — escalate tier 2 for Gulf-adjacent routes.

## Off-Ramp / Review Trigger

Revisit after Geneva signing or 2026-06-19 wire close.

## Disclaimer

*Statecraft Intelligence Desk provides geopolitical intelligence support and draft background memoranda for the Firm's internal professional use. Vendor is not legal counsel to the Firm or its clients. The Firm is solely responsible for all legal advice, compliance determinations, and client communications. Deliverables are judgment support, not investment advice.*
"""

def _scratch_path(name: str) -> Path:
    scratch = REPO_ROOT / ".codex-tmp" / "pytest-scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    return scratch / f"{name}-{uuid.uuid4().hex}.md"

def test_valid_memo_passes() -> None:
    path = _scratch_path("memo")
    path.write_text(VALID_MEMO, encoding="utf-8")
    assert validate_memo_file(path) == []

def test_missing_falsifiers_fails() -> None:
    path = _scratch_path("memo-broken")
    broken = VALID_MEMO.replace(
        "## Falsifiers\n\n- **F1:** Signed MOU text publishes fee lane — downgrade toll-free read.\n- **F2:** IDF Lebanon ops breach MOU clause — escalate tier 2 for Gulf-adjacent routes.\n\n",
        "## Falsifiers\n\n",
    )
    path.write_text(broken, encoding="utf-8")
    errors = validate_memo_file(path)
    assert any("Falsifiers" in e for e in errors)

def test_template_documents_embargo_values() -> None:
    template = REPO_ROOT / "statecraft" / "templates" / "sid-transaction-memo.md"
    text = template.read_text(encoding="utf-8")
    assert "embargo: client-only" in text
    assert "validate_sid_transaction_memo.py" in text
