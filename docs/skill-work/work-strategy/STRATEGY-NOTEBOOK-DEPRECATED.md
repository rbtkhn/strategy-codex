# Strategy-notebook namespace — DEPRECATED (2026-06-23)

WORK only; not Record.

**Status:** The phrase **`strategy-notebook`** and the compat tree **`docs/skill-work/work-strategy/strategy-notebook/`** are **deprecated** for new strategy-codex work. Do not add new canonical artifacts under that namespace. Legacy files and script aliases may remain **read-only compatibility** until explicitly migrated.

## What to say instead

| Old phrase / path | Use instead |
|-------------------|-------------|
| **`strategy-notebook`** (operator) | **`strategy-codex`** or **`/codex`** |
| **`docs/.../strategy-notebook/`** | **`codex/`** at repo root |
| Notebook architecture doc | [`codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md`](../../../codex/STRATEGY-NOTEBOOK-ARCHITECTURE.md) — **filename is legacy**; content governs **`codex/`** continuity |
| Operator preferences | [`codex/NOTEBOOK-PREFERENCES.md`](../../../codex/NOTEBOOK-PREFERENCES.md) |
| Daily scratch | [`codex/daily-strategy-inbox.md`](../../../codex/daily-strategy-inbox.md) |
| Verbatim capture | **`source-archive/statecraft/`** via **`source-intake`** — [RAW-INPUT-DEPRECATED.md](RAW-INPUT-DEPRECATED.md) |
| Live judgment / mechanism | [`statecraft/`](../../../statecraft/README.md) |

## Three layers (current model)

```text
source-archive/statecraft/   verbatim SSOT (source-intake)
codex/                       chronology, inbox, days.md, thread/page machinery
statecraft/                  live judgment, lanes, synthesis, prose outputs
```

**`strategy-notebook`** was an intermediate packaging name for what is now **`strategy-codex`** (`codex/`). The architecture doc title **`STRATEGY-NOTEBOOK-ARCHITECTURE.md`** remains the SSOT for EOD compose and page shape — it lives under **`codex/`**, not under the deprecated compat folder.

## Compat tree (do not extend)

- [`docs/skill-work/work-strategy/strategy-notebook/`](strategy-notebook/README.md) — redirect stub only
- Historical links, fixtures, and script path aliases may still mention **`strategy-notebook`** — treat as archaeology unless a script is actively maintained

Do **not** recreate removed subtrees such as **`strategy-notebook/raw-input/`** — see [RAW-INPUT-DEPRECATED.md](RAW-INPUT-DEPRECATED.md).

## Mind / voice paths (named expert)

**Legacy mind files (compatibility):** `codex/strategy-expert-<id>-mind.md` (redirects to voice profiles).

**New work:** [`statecraft/voices/`](../../../statecraft/voices/README.md) voice profiles — [VOICES-SUPERSEDE-MINDS.md](VOICES-SUPERSEDE-MINDS.md).

Do **not** resolve expert voice from missing **`docs/.../strategy-notebook/strategy-expert-*`** paths.

## What is **not** deprecated

- **`strategy-codex`** — repo and operator notebook identity
- **`codex/`** — canonical chronology corpus
- **`STRATEGY-NOTEBOOK-ARCHITECTURE.md`** — architecture SSOT (under `codex/`)
- **`strategy`** / **`strategy pass`** — [DEFAULT-PATH.md](DEFAULT-PATH.md) + [strategy-codex-pass.mdc](../../../.cursor/rules/strategy-codex-pass.mdc)
- **`strategy page` / compose** — EOD session per architecture doc
- Deprecated **`skill-strategy`** skill — [SKILL-STRATEGY-DEPRECATED.md](SKILL-STRATEGY-DEPRECATED.md)

## Related deprecation

- Raw-input capture: [RAW-INPUT-DEPRECATED.md](RAW-INPUT-DEPRECATED.md)
- YouTube materialize: [YOUTUBE-MATERIALIZE-DEPRECATED.md](YOUTUBE-MATERIALIZE-DEPRECATED.md)
- Legacy lane map: [LEGACY-SUCCESSOR-MAP.md](LEGACY-SUCCESSOR-MAP.md)

## Legacy pointers

- Compat redirect: [`strategy-notebook/README.md`](strategy-notebook/README.md)
- Books routing: [`.cursor/rules/operator-books-routing.mdc`](../../../.cursor/rules/operator-books-routing.mdc)
