---
name: gate-review-pass
preferred_activation: gate review
activation: gate review
description: DEPRECATED default — fork revive only. Redirect to gated merge pipeline.
category: legacy-redirect
status: redirect
replacement: fork-revive
scope_class: repo-governed
review_date: 2026-12-31
---
# Gate review pass (legacy alias) — DEPRECATED

**Record frozen by default.** Merge only after explicit **`fork revive`** and companion approval.

**Superseded by:** fork-revive + `process_approved_candidates.py --apply` — [`docs/agent-rules/deep-rules.md`](../../../docs/agent-rules/deep-rules.md).

**Activation:** `gate review`, `gate-review-pass` — redirect; do not stage candidates unless operator invoked fork revive.

**Preferred name (new work):** **`fork revive`** then approved candidate merge script.
