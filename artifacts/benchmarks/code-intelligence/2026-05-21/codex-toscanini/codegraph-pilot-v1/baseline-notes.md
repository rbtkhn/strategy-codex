# CodeGraph Pilot Benchmark - Baseline Lane

## Frame

Baseline lane used ordinary repo methods only:

- `rg` for call sites and route surfaces
- direct file reads for `service.py`, `presenton_client.py`, `contract.py`, `intents.py`, and presentation helper docs
- no CodeGraph export or graph tooling

## Task A - Presentation service architecture

Question:

`What are the key entry points, call relationships, and source files for the presentation service path?`

Result: `usable`

- Primary entry point is [`create_app`](C:/dev/strategy-codex/src/grace_mar/presentations/service.py), which exposes `POST /v1/bundles/render` and owns bundle validation, Presenton render dispatch, record write, and manifest append.
- Main downstream dependency is [`PresentonClient.generate_presentation`](C:/dev/strategy-codex/src/grace_mar/presentations/presenton_client.py), which builds multipart form data and POSTs to the external Presenton service.
- Supporting architecture files surfaced cleanly:
  - [contract.py](C:/dev/strategy-codex/src/grace_mar/presentations/contract.py)
  - [intents.py](C:/dev/strategy-codex/src/grace_mar/presentations/intents.py)
  - [scripts/presentations_service.py](C:/dev/strategy-codex/scripts/presentations_service.py)
  - [scripts/render_presentation_bundle.py](C:/dev/strategy-codex/scripts/render_presentation_bundle.py)
  - [test_presentations_service.py](C:/dev/strategy-codex/tests/test_presentations_service.py)

Measures:

| Measure | Value |
|---|---|
| `wall_minutes` | `3` |
| `tool_calls` | `4` |
| `output_path` | `artifacts/benchmarks/code-intelligence/2026-05-21/codex-toscanini/codegraph-pilot-v1/baseline-notes.md` |
| `answer_quality` | `usable` |
| `notes` | Clean enough to answer the architecture question, but manual reading was needed to distinguish the Flask entry point from contract and client helpers. |

## Task B - Presentation service impact review

Question:

`If we change src/grace_mar/presentations/service.py, what other files and likely test surfaces should we inspect first?`

Result: `strong`

First inspection set:

- [presenton_client.py](C:/dev/strategy-codex/src/grace_mar/presentations/presenton_client.py) because `create_app` instantiates and calls `PresentonClient.generate_presentation`
- [contract.py](C:/dev/strategy-codex/src/grace_mar/presentations/contract.py) because `render_bundle` validates and hashes bundles
- [intents.py](C:/dev/strategy-codex/src/grace_mar/presentations/intents.py) because template resolution and markdown generation happen there
- [scripts/presentations_service.py](C:/dev/strategy-codex/scripts/presentations_service.py) because it imports `create_app`
- [scripts/render_presentation_bundle.py](C:/dev/strategy-codex/scripts/render_presentation_bundle.py) because it targets `/v1/bundles/render`
- [test_presentations_service.py](C:/dev/strategy-codex/tests/test_presentations_service.py) as the obvious test surface

Measures:

| Measure | Value |
|---|---|
| `wall_minutes` | `2` |
| `tool_calls` | `2` |
| `output_path` | `artifacts/benchmarks/code-intelligence/2026-05-21/codex-toscanini/codegraph-pilot-v1/baseline-notes.md` |
| `answer_quality` | `strong` |
| `notes` | The impact surface is small enough that grep plus one read pass gave a trustworthy first-inspection list. |

## Task C - Architecture bundle prep

Question:

`Can we produce a more legible, traceable architecture bundle for the presentation path with less prep time than the ordinary manual route?`

Result: `weak`

- Baseline lane did not produce a fresh manual presentation bundle during this pass.
- Manual preparation was enough to describe the likely source items, but not enough to count as a clean bundle-prep win.

Measures:

| Measure | Value |
|---|---|
| `wall_minutes` | `4` |
| `tool_calls` | `3` |
| `output_path` | `artifacts/benchmarks/code-intelligence/2026-05-21/codex-toscanini/codegraph-pilot-v1/baseline-notes.md` |
| `answer_quality` | `weak` |
| `notes` | Manual route is understandable, but bundle assembly is still mostly a hand-crafted operator move rather than a compact repeatable workflow. |
