---
name: strategy-notebook-lane-split
description: Archived strategy-codex multi-expert refined-page workflow. Use codex templates and raw-input SSOT for new work.
preferred_activation: lane split
activation: lane split
category: domain-pack
status: archived
scope_class: repo-governed
review_date: 2026-12-31
tags:
  - operator
  - archived
  - work-strategy
  - strategy-codex
---
# Archived — strategy-notebook-lane-split

**Status:** Archived. Do not invoke this skill for new work.

**Use instead (strategy-codex / codex SSOT):**

- [`codex/refined-page-template.md`](../../../codex/refined-page-template.md) — refined page contract, verbatim budget, appendix order
- [`codex/raw-input/README.md`](../../../codex/raw-input/README.md) — multi-expert raw capture, `threads:` YAML
- [`strategy-notebook-guest-canon-note`](../strategy-notebook-guest-canon-note/SKILL.md) or [`strategy-notebook-expert-cross-weave`](../strategy-notebook-expert-cross-weave/SKILL.md) — EOD weave / guest canon when folding seams

**Machine checks (unchanged):** `python3 scripts/strategy/audit_refined_pages.py`; lane-split guest pages — set **`skip_assembly: true`** on manifest rows so verbatim assemblers do not overwrite compressed guest Verbatim.

## Legacy activation

When the operator says **`lane split`** or **`two-lane refined page`**, follow codex templates above for host/guest (or A/B) refined pairs from one multi-`expert_id` raw-input file — shared slug, lane-distinct Verbatim, sibling cross-links.

## No independent entry surface

Full workflow doctrine lives in codex notebook surfaces, not this stub.
