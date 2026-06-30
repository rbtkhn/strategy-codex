# Strategy-notebook namespace — DEPRECATED (2026-06-23)


**Status:** The phrase **`strategy-notebook`** and the compat tree **`docs/skill-work/work-strategy/../../continuity/`** are **deprecated** for new strategy-codex work. Do not add new canonical artifacts under that namespace. Legacy files and script aliases may remain **read-only compatibility** until explicitly migrated.

## What to say instead

| Old phrase / path | Use instead |
|-------------------|-------------|
| **`strategy-notebook`** (operator) | **`strategy-codex`** or **`/codex`** |
| **`docs/.../../../continuity/`** | **`continuity/`** at repo root |
| Notebook architecture doc | [`continuity/STRATEGY-NOTEBOOK-ARCHITECTURE.md`](../../../continuity/STRATEGY-NOTEBOOK-ARCHITECTURE.md) — **filename is legacy**; content governs **`continuity/`** continuity |
| Operator preferences | [`continuity/NOTEBOOK-PREFERENCES.md`](../../../continuity/NOTEBOOK-PREFERENCES.md) |
| Daily scratch | [`continuity/daily-strategy-inbox.md`](../../../continuity/daily-strategy-inbox.md) |
| Verbatim capture | **`source-archive/statecraft/`** via **`source-intake`** — [RAW-INPUT-DEPRECATED.md](RAW-INPUT-DEPRECATED.md) |
| Live judgment / mechanism | [`statecraft/`](../../../statecraft/README.md) |

## Three layers (current model)

```text
source-archive/statecraft/   verbatim SSOT (source-intake)
continuity/                       chronology, inbox, days.md, thread/page machinery
statecraft/                  live judgment, lanes, synthesis, prose outputs
```

**`strategy-notebook`** was an intermediate packaging name for what is now **`strategy-codex`** (`continuity/`). The architecture doc title **`STRATEGY-NOTEBOOK-ARCHITECTURE.md`** remains the SSOT for EOD compose and page shape — it lives under **`continuity/`**, not under the deprecated compat folder.

## Compat tree (do not extend)

- [`docs/skill-work/work-strategy/../../continuity/`](../../../README.md) — redirect stub only
- Historical links, fixtures, and script path aliases may still mention **`strategy-notebook`** — treat as archaeology unless a script is actively maintained

Do **not** recreate removed subtrees such as **`../../continuity/raw-input/`** — see [RAW-INPUT-DEPRECATED.md](RAW-INPUT-DEPRECATED.md).

## Mind / voice paths (named expert)

**Legacy mind files (compatibility):** `continuity/strategy-expert-<id>-mind.md` (redirects to voice profiles).

**New work:** [`statecraft/voices/`](../../../statecraft/voices/README.md) voice profiles — [VOICES-SUPERSEDE-MINDS.md](VOICES-SUPERSEDE-MINDS.md).

Do **not** resolve expert voice from missing **`docs/.../../../continuity/strategy-expert-*`** paths.

## What is **not** deprecated

- **`strategy-codex`** — repo and operator notebook identity
- **`continuity/`** — canonical chronology corpus
- **`STRATEGY-NOTEBOOK-ARCHITECTURE.md`** — architecture SSOT (under `continuity/`)
- **`strategy`** / **`strategy pass`** — [DEFAULT-PATH.md](DEFAULT-PATH.md) + [strategy-codex-pass.mdc](../../../.cursor/rules/strategy-codex-pass.mdc)
- **`strategy page` / compose** — EOD session per architecture doc
- Deprecated **`skill-strategy`** skill — [SKILL-STRATEGY-DEPRECATED.md](SKILL-STRATEGY-DEPRECATED.md)

## Related deprecation

- Raw-input capture: [RAW-INPUT-DEPRECATED.md](RAW-INPUT-DEPRECATED.md)
- YouTube materialize: [YOUTUBE-MATERIALIZE-DEPRECATED.md](YOUTUBE-MATERIALIZE-DEPRECATED.md)
- Legacy lane map: [LEGACY-SUCCESSOR-MAP.md](LEGACY-SUCCESSOR-MAP.md)

## Legacy pointers

- Compat redirect: [`../../continuity/README.md`](../../../README.md)
- Books routing: [`.cursor/rules/operator-books-routing.mdc`](../../../.cursor/rules/operator-books-routing.mdc)
