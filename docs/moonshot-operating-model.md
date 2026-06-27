# Moonshot Operating Model (PMOS v0.1)

**Status:** Active (WORK doctrine)  
**Scope:** Grace-Mar **Personal Moonshot OS** â€” governance-first scaffold. **Not** Record; **not** medical-by-default (domain-neutral moonshots).

## North star

- **civilization_memory / external research** and **operator intent** inform moonshots.
- **Long-horizon programs** are drafted in **[self-moonshots.md](../self-moonshots.md)** as **staging only** â€” not authoritative SELF until merged via the **gated pipeline**.
- **AI / assistants** **propose** and **stage** candidates; **companions** approve merges â€” same invariant as [AGENTS.md](AGENTS.md).

## v0.1 deliverables

| Deliverable | Path |
|-------------|------|
| Staging surface | `self-moonshots.md` |
| Template | [docs/skill-work/work-moonshots/moonshot-template.md](skill-work/work-moonshots/moonshot-template.md) |
| Lane README | [docs/skill-work/work-moonshots/README.md](skill-work/work-moonshots/README.md) |

**Out of v0.1:** Bot/CLI commands, data-ingestion connectors, HTML dashboards, â€œagent swarmâ€ automation.

## Edit authority

| Actor | `self-moonshots.md` | Merge to `self.md` / EVIDENCE |
|-------|---------------------|--------------------------------|
| Companion / operator | Yes | Only via `process_approved_candidates.py` after approval |
| Assistant | **Do not** treat staging as merge authority â€” **stage** `CANDIDATE-*` in `recursion-gate.md` | Same as today |

## Promotion mapping (after approval)

| Content | Destination |
|---------|-------------|
| Durable **why** / values / identity-relevant commitments | `self.md` museum knowledge section B / museum knowledge section C (or museum knowledge section A if factual), with provenance |
| **Dated outcomes** (milestones, launches) | `self-archive.md` (ACT / CREATE / structured evidence per instance conventions) |
| Running experiments / next steps | Stay in `self-moonshots.md` or **memory** until promoted |

**EVIDENCE in v0.1:** Optional habit when a milestone is merged â€” **not** required to ship the scaffold.

## Voice / prompt / benchmarks (deferred)

- **v0.1** does **not** change [archive/grace-mar-instance/bot/prompt.py](../archive/grace-mar-instance/bot/prompt.py).
- After a gate merge touches profile text, use existing **identity delta** / voice checks per [instance-doctrine.md](../instance-doctrine.md) if applicable.

## Life portfolio / cross-moonshot synthesis (deferred)

- Overlaps between moonshots may be noted in **memory** (continuity) or a future **WORK** index â€” **not** a parallel Record.

## Example: recursion-gate block (moonshot promotion)

Use the same **`### CANDIDATE-XXXX`** + **```yaml** shape as [recursion-gate.md](../archive/grace-mar-instance/recursion-gate.md). Fields consumed by `process_approved_candidates.py` include **`summary`**, **`mind_category`**, **`profile_target`**, **`status`**, **`channel_key`**, **`source`**, and optional **`suggested_entry`**.

**Illustrative only** â€” use a new `### CANDIDATE-XXXX` heading in `recursion-gate.md`, then a fenced **`yaml`** block **below** it (same pattern as existing candidates). Assign a fresh id; keep the block **above** `## Processed` while **pending**. YAML body example:

```yaml
mind_category: curiosity
signal_type: moonshot_promotion
profile_target: museum knowledge section B. CURIOSITY
status: pending
channel_key: operator:cursor
source: self-moonshots.md
summary: "Promote active moonshot <moonshot-id> â€” durable curiosity line from staging"
suggested_entry: "(paste proposed IX line; companion edits before approve)"
```

**Align to live schema:** When staging real candidates, copy field names from the most recent approved block in `recursion-gate.md` and from [process_approved_candidates.py](../scripts/process_approved_candidates.py) YAML parsing.

## Security

- No secrets in `self-moonshots.md` or templates.
- No unfounded legal / medical / financial claims as Record facts; professional context belongs outside LLM inference.

## Related

- **Partner / audit (optional):** `python3 scripts/report_governance_posture.py -u <id>` emits [runtime/artifacts/governance-posture.md](../runtime/artifacts/governance-posture.md) â€” a **generated** one-pager on triad, gated merge, inspectable audit files, and verification commands for external conversations. Operational narrative only, not legal or regulatory certification; see [safety-story-ux.md](skill-work/work-dev/safety-story-ux.md).
- [Canonical paths â€” self-moonshots](canonical-paths.md) (staging row)
- [Id taxonomy â€” self-moonshots](id-taxonomy.md#standard-location-labels)
- [Identity fork protocol](identity-fork-protocol.md)
- [Promotion ladder](skill-work/work-strategy/promotion-ladder.md) (optional cross-link for long arcs)

