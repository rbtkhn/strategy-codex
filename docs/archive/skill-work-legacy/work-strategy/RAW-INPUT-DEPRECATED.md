# Strategy raw-input capture — DEPRECATED (2026-06-23)

**Status:** The **`continuity/raw-input/`** tree, **`continuity/years/*/raw-input/`**, and compat **`docs/.../../../continuity/raw-input/`** paths are **deprecated** for new strategy-codex capture. Do not create new verbatim files there. Legacy files on disk remain **read-only archaeology**.

## What replaced it

| Old | Use instead |
|-----|-------------|
| **`continuity/raw-input/<pub_date>/`** verbatim files | **`source-archive/statecraft/YYYY-MM-DD/source-<slug>.md`** |
| **`substack-*` / `youtube-*` / `transcript-*`** notebook filenames | **`source-*`** archive prefix — [source-archive/statecraft/README.md](../../../source-archive/statecraft/README.md) (filename law) |
| Monolithic markdown write to notebook raw-input | **`source-intake`** — sidecar `Write` + `land_statecraft_source_body.py` — [statecraft-source-intake SKILL](../../../skills/statecraft-source-intake/SKILL.md) |
| **`strategy input`** / pasted essay + URL | Same turn: **`source-intake`** land first, then digest / synthesis — [strategy-input-raw-ingest.mdc](../../../.cursor/rules/strategy-input-raw-ingest.mdc) |
| YouTube roster → capture | **`check sources`** → approve → **`source-intake`** — see [YOUTUBE-MATERIALIZE-DEPRECATED.md](YOUTUBE-MATERIALIZE-DEPRECATED.md) |

## Three surfaces (not one)

| Surface | Role |
|---------|------|
| **`source-archive/statecraft/`** | **Verbatim SSOT** — full external body |
| **`continuity/daily-strategy-inbox.md`** | **Registry** — one-liners, `thread:`, URLs, stubs pointing at archive paths |
| **`continuity/chapters/.../days.md` + strategy-page** | **Synthesis + links** — not full mirrors |

## Material type → frontmatter (same land skill)

Choose **`kind`** and **`source_form`** per [statecraft-source-intake](../../../skills/statecraft-source-intake/SKILL.md) family table — do not pick a different folder per type.

| Material | Typical `kind` | Typical `source_form` |
|----------|----------------|------------------------|
| YouTube / podcast transcript | `transcript` | `solo`, `interview`, `panel` |
| Substack / long essay | `substack-post` | `newsletter` |
| Wire / institutional paste | `paste-bundle`, `rss-item` | `article`, `institutional-primary` |
| X / social thread | `x-post-text`, `x-post-bundle` | `post` |

## Pending publication date

Use **`source-archive/statecraft/_aired-pending/`** until **`pub_date`** is pinned; then land under **`source-archive/statecraft/YYYY-MM-DD/`**.

## Inbox and gap check

- Optional **inbox stub** after land — pointer to **archive path**, not raw-input path — [daily-strategy-inbox.md](../../../continuity/daily-strategy-inbox.md).
- Advisory gap heuristic: `python3 scripts/strategy_raw_input_gap_hint.py` (inbox URLs vs `source_url` in archive YAML).

## Legacy trees (read-only)

- [`continuity/raw-input/`](../../../continuity/raw-input/README.md)
- [`continuity/years/2025/raw-input/`](../../../continuity/years/2025/raw-input/) and [`continuity/years/2026/raw-input/`](../../../continuity/years/2026/raw-input/README.md)
- Compat namespace **`docs/skill-work/work-strategy/../../continuity/raw-input/`** (removed; do not recreate)

Do **not** delete or bulk-migrate legacy captures in a deprecation pass unless the operator explicitly requests migration.

## Parallel namespace (singularity)

[`singularity/workshop/raw-input/`](../../../singularity/workshop/raw-input/README.md) is a separate deprecated pointer. New singularity workshop captures → **`source-archive/singularity/`**, not strategy raw-input.

## What is **not** deprecated

- **`source-intake`** — canonical archive land skill
- **`check sources`** — discovery handoff to source-intake
- **`source-clean`** — post-land ASR / entity cleanup on archive captures
- **`strategy_raw_input_gap_hint.py`** — advisory inbox vs archive URL check (legacy script name)
- **`cognition_streams_audit.py --capture-surface raw-input`** — archaeology / coverage receipts on old paths only

## Related deprecation

- Strategy-notebook namespace: [STRATEGY-NOTEBOOK-DEPRECATED.md](STRATEGY-NOTEBOOK-DEPRECATED.md)
- YouTube materialize path: [YOUTUBE-MATERIALIZE-DEPRECATED.md](YOUTUBE-MATERIALIZE-DEPRECATED.md)
- Notebook preferences (inbox vs archive): [NOTEBOOK-PREFERENCES.md](../../../continuity/NOTEBOOK-PREFERENCES.md)

## Legacy pointers

- Deprecated tree stub: [`continuity/raw-input/README.md`](../../../continuity/raw-input/README.md)
- Always-on rule (updated): [`.cursor/rules/strategy-input-raw-ingest.mdc`](../../../.cursor/rules/strategy-input-raw-ingest.mdc)
