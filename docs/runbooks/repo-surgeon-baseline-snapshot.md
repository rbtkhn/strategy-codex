# Repo Surgeon baseline snapshot (count-only)

**** Regenerate via [repo-surgeon.md](repo-surgeon.md).

| Date | Scope | Blocking | Warnings | Notes |
| --- | --- | --- | --- | --- |
| 2026-06-26 (pre-closure) | `all` | 12 | ~14,136 | Pre–Pass 4; legacy `continuity/years` + repo-root absolute links |
| 2026-06-26 (post batch Pass 4) | `all` | 0 | ~7,698 | After `fix_repo_surgeon_link_batch.py` v1 |
| 2026-06-26 (Pass 4 continued) | `routing-ssot` | 0 | **0** | SSOT slice clean (regenerate via `generate_llm_routing.py`) |
| 2026-06-26 (Pass 4 continued) | `all` | 0 | ~2,094 | Voice-thread machine layer + skills depth; strict gate pending |

**Category mix (latest `all` scan):** predominantly `broken_link`; residual `absolute_path` (~28) in example paths and operator receipts.

**Next tranche:** statecraft `*-thread.md` machine-layer legacy targets; `.cursor/skills` depth to `skills/runbooks/`; missing `work-cici` placeholder paths → `singularity/work-cici/README.md`.
