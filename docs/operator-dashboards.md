# Operator dashboards (derived Markdown)

Grace-Mar can emit **compact, regeneratable Markdown â€œdashboardsâ€** for operator navigation. They borrow the *visibility* idea from Dataview-style vault tools without making the repo an Obsidian-style truth system.

## Dashboard anti-sprawl rule

Prefer **extending** an existing dashboard, **adding a registry entry**, or **adding a report, receipt, packet, or machine feed** before adding a **new** dashboard. Any new operator dashboard must be **registered** in [operator-surface-registry.md](operator-surface-registry.md) with **authority status**, **source inputs**, **operator use**, and **relationship** to existing surfaces (see Â§5â€“7 there). The full policy and preferred alternatives live in that fileâ€”not duplicated here.

**Operator dashboard consolidation (Phases 0–4):** Repo Surgeon, Statecraft War Room, Operator Command Deck, and Operator Dashboard umbrella — [operator-dashboard-consolidation-phase0.md](skill-work/work-dev/operator-dashboard-consolidation-phase0.md). **When to use (agent nudge):** [operator-dashboard-when-to-use.md](operator-dashboard-when-to-use.md). **`coffee`** Step 1 includes a mandatory Dashboard nudge — [coffee SKILL](../.cursor/skills/coffee/SKILL.md).

Dashboards are a **stable scripted subclass** of the [Interface Artifact Protocol](skill-work/work-dev/interface-runtime/artifacts/README.md): generated operator-facing views that remain **derived** and **non-canonical** even when they become reliable enough to script and regenerate routinely.

## Dashboard staleness

Dashboards are **derived views** and can become **stale** when **source inputs** (e.g. `self-library.md`, `recursion-gate.md`, runtime indexes) change without a **regen**. For time-sensitive decisions, **confirm** against the **authoritative source** when freshness matters. Levels, a standard note format, and the rule that staleness does **not** change authority: [operator-surface-staleness.md](operator-surface-staleness.md).

## What these are

- **Derived artifacts** under [`runtime/artifacts/`](../runtime/artifacts/README.md), produced by scripts:
  - `python3 scripts/build_library_index.py` â†’ [`runtime/artifacts/library-index.md`](../runtime/artifacts/library-index.md)
  - `python3 scripts/build_lane_dashboards.py` â†’ [`runtime/artifacts/lane-dashboards/README.md`](../runtime/artifacts/lane-dashboards/README.md) (optionally after `python3 scripts/build_work_lanes_dashboard.py` for JSON inputs)
  - `python3 scripts/build_review_dashboard.py` â†’ [`runtime/artifacts/review-dashboard.md`](../runtime/artifacts/review-dashboard.md)
  - `python3 scripts/build_gate_board.py` â†’ [`runtime/artifacts/gate-board.md`](../runtime/artifacts/gate-board.md) (Kanban-style; see [gate-board.md](gate-board.md))

## What they are not

- **Not** canonical Record surfaces (not SELF, SELF-LIBRARY, SKILLS, or EVIDENCE).
- **Not** a replacement for [`recursion-gate.md`](../recursion-gate.md) or structured review-queue JSON â€” they **summarize** and **link**, they do not hold merge authority.
- **Not** runtime truth â€” [`runtime/observations/`](../runtime/observations/README.md) remains non-canonical; dashboards may quote it as **hints** only.

## How to regenerate

From repo root (typical order):

```bash
python3 scripts/build_work_lanes_dashboard.py   # optional JSON feed for lane dashboard
python3 scripts/build_library_index.py
python3 scripts/build_lane_dashboards.py
python3 scripts/build_review_dashboard.py
python3 scripts/build_gate_board.py

# Phase 4 umbrella — all three aggregators + stitched index (gitignored latest.*)
python3 scripts/operator_dashboard.py

# Phase 1–3 aggregators individually
python3 scripts/operator_command_deck.py --max-next-actions 5
python3 scripts/statecraft_war_room.py --latest-days 7 --max-objects 12
python3 scripts/repo_surgeon.py --scope docs
```

Use `-u grace-mar` where scripts support it (default user is usually `grace-mar`).

When several derived surfaces may have drifted at once, use the repo-owned regeneration entrypoint first:

```bash
python3 scripts/regenerate_all_derived.py --changed --dry-run
```

Covered dashboard outputs also gain sibling rebuild-provenance sidecars such as
`runtime/artifacts/review-dashboard.md.derived-rationale.json`. Those sidecars are derived metadata only;
they do not add authority beyond the dashboard itself.

**CI:** On push and pull requests to `main`, [`.github/workflows/library-index.yml`](../.github/workflows/library-index.yml) runs `build_library_index.py` and fails if `runtime/artifacts/library-index.md` is out of date â€” regenerate locally and commit with `self-library.md` changes.

## Design notes

- **Library index** parses the `entries:` YAML block in `self-library.md` (first `## Entries` fence); emitted Markdown is **dashboard-ordered** (summary â†’ Start here â†’ recent â†’ compact lanes â†’ appendix full inventory).
- **Review dashboard** uses [`scripts/gate_block_parser.py`](../scripts/gate_block_parser.py) for fenced `### CANDIDATE-*` blocks; pending rows are any block with `status: pending` (even if misplaced relative to `## Processed` â€” fix the gate file when possible).
- **Lane dashboards** aggregate `runtime/observations/index.jsonl` (when present) and embed or reference `runtime/artifacts/work-lanes-dashboard.json`.

See also: [runtime vs Record](runtime-vs-record.md), [claude-surface-contract.md](claude-surface-contract.md) (invocation / mutation language).

