# CodeGraph Pilot Benchmark - CodeGraph Lane

## Frame

CodeGraph lane used the bounded pilot surfaces:

- [export_code_context.py](C:/dev/strategy-codex/integrations/codegraph/export_code_context.py)
- [generate_architecture_bundle.py](C:/dev/strategy-codex/integrations/codegraph/generate_architecture_bundle.py)
- prior same-day export artifacts already present in `artifacts/codegraph/`

Important constraint:

- a fresh rerun of `npx @colbymchenry/codegraph` on this Windows setup failed during the benchmark because the spawned CodeGraph binary returned `EINVAL`
- a repo-local npm cache avoided the first cache-permission error but did **not** fix the later spawn failure
- because of that, today's codegraph lane is partly evaluated from an already-generated same-day export plus a fresh bundle regeneration

## Task A - Presentation service architecture

Question:

`What are the key entry points, call relationships, and source files for the presentation service path?`

Result: `usable`

Usable artifact:

- [service-architecture.md](C:/dev/strategy-codex/artifacts/codegraph/service-architecture.md)

What it did well:

- produced one compact summary plus a Mermaid relationship graph
- surfaced `create_app`, `_presentation_store_root`, and `PresentonClient::generate_presentation` quickly
- bundled related files and code blocks into one artifact

What it did poorly:

- the top-ranked result set also pulled in unrelated-but-lexically-near nodes like `service_worker` from `apps/miniapp_server.py`
- the symbol query inside the stored export targeted `PresentationService`, which was not the most useful symbol for this path

Measures:

| Measure | Value |
|---|---|
| `wall_minutes` | `1` |
| `tool_calls` | `2` |
| `output_path` | `artifacts/codegraph/service-architecture.md` |
| `answer_quality` | `usable` |
| `notes` | Faster than baseline to scan, but slightly noisier; summary plus graph are the main win. |

## Task B - Presentation service impact review

Question:

`If we change src/grace_mar/presentations/service.py, what other files and likely test surfaces should we inspect first?`

Result: `weak`

Usable artifact:

- [service-architecture.json](C:/dev/strategy-codex/artifacts/codegraph/service-architecture.json)

Observed problem:

- the stored `affected` output returned only the changed file and no tests
- that makes the impact result materially weaker than the baseline grep/read pass for this repo slice

Measures:

| Measure | Value |
|---|---|
| `wall_minutes` | `1` |
| `tool_calls` | `1` |
| `output_path` | `artifacts/codegraph/service-architecture.json` |
| `answer_quality` | `weak` |
| `notes` | The impact result under-reported the obvious test and script surfaces, so speed did not translate into enough trust. |

## Task C - Architecture bundle prep

Question:

`Can we produce a more legible, traceable architecture bundle for the presentation path with less prep time than the ordinary manual route?`

Result: `strong`

Usable artifact:

- [benchmark-codegraph-service-architecture.bundle.json](C:/dev/strategy-codex/artifacts/presentations/benchmark-codegraph-service-architecture.bundle.json)

Observed strengths:

- fresh bundle regeneration from the prior export took about `0.19` seconds
- the bundle is fully traceable back to the export and source files
- relationship graph plus code-block selection made the architecture story legible with very little operator effort

Observed weakness:

- this task only completed because a prior export already existed; a fresh export rerun failed on the Windows `npx` spawn path

Measures:

| Measure | Value |
|---|---|
| `wall_minutes` | `1` |
| `tool_calls` | `3` |
| `output_path` | `artifacts/presentations/benchmark-codegraph-service-architecture.bundle.json` |
| `answer_quality` | `strong` |
| `notes` | The bundle path is excellent once an export exists, but the current rerun path is not yet dependable. |

## Fresh Rerun Failure

Fresh benchmark rerun attempts failed in two stages:

1. default npm cache path raised a permission error outside the workspace
2. repo-local cache then reached package install but failed with `spawnSync ... codegraph.cmd EINVAL`

That means today's lane cannot be judged as a clean local rerunnable workflow yet.
