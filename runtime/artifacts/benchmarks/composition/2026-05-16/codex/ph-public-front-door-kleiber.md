---
benchmark_id: kleiber-ph-public-front-door
prompt_version: composition-benchmark-v1-kleiber-front-door-adapter
rubric_version: composition-rubric-v1-adapted-front-door
model: GPT-5 Codex
provider: OpenAI
model_version: unavailable
run_date: 2026-05-16
temperature: unknown
seed: unavailable
source_mode: live_lookup
evaluator: Codex agent
target_repo: rbtkhn/predictive-history
conductor: kleiber
closeout: Held
notes: "Adapter benchmark requested by operator: score the PH public front door, not one of the standard V1 prose-generation tasks. Sources retrieved through GitHub connector on 2026-05-16."
---

# PH Public Front Door - Kleiber Composition Benchmark

## Scope

Score only the public front door of `rbtkhn/predictive-history`: README, `llms.txt`, series roadmap, chapter manifest/index routing, one `civ-01` route canary, and maintainer next-actions. Refuse full corpus audit, prose rewrite, or chapter deepening in this pass.

## Sources Checked

- `README.md`
- `llms.txt`
- `docs/series-roadmap.md`
- `docs/chapter-index.md`
- `chapter-manifest.yaml`
- `corpus/civilization/civ-01.md`
- `book/volume-ii/civ-01/civ-01-transcript.md`
- `book/volume-ii/civ-01/civ-01-commentary.md`
- `corpus/civ-ph/civ-01.md`
- `book/volume-ii/civ-01/civ-01-orientation.yaml`
- `reports/next-actions.md`

## Verified Evidence vs Interpretation

Verified evidence: the public front door names the project purpose, rights/status limits, machine entry path, one-chapter load contract, major public surfaces, current series status, and next-action queue. The `civ-01` route resolves across manifest, index, corpus pointer, transcript, commentary, civ-ph card, and orientation YAML.

Interpretation: the front door is compositionally strong because it gives humans and agents a bounded path into a large corpus without inviting whole-repo ingestion or overclaiming completed analysis.

## Weakest Factual Link

The benchmark only canaried one chapter route (`civ-01`). It did not validate all manifest rows, all generated links, or every report count against repository contents.

## Scores

| Dimension | Score | Rationale |
| --- | ---: | --- |
| Template/front-door fit | 5 | README, `llms.txt`, roadmap, manifest, and reports each have a distinct role and do not collapse into one overloaded index. |
| Strategic judgment | 5 | The front door makes a clear strategic choice: one chapter at a time, source discipline first, broad corpus second. |
| Falsifiability | 4 | Status vocabulary, review limits, `reports/next-actions.md`, and routeable artifacts make failure visible, though full link validation was not run here. |
| Tension preservation | 5 | The repo keeps representation separate from endorsement, public surface separate from private notes, and routed spines separate from final commentary. |
| Voice and memorability | 4 | The public prose is clear and sober; it is less vivid than a reader-facing essay, but that restraint suits a front door. |

## Result

**Held.**

No dimension is below 4. The front door is coherent enough for public readers and coding agents: it states what the project is, where to start, what is included, what is unfinished, and how to load one chapter without swallowing the whole corpus.

## Falsifier

This result fails if a fresh route audit finds that a nontrivial share of `chapter-manifest.yaml` rows point to missing transcript, commentary, civ-ph, or orientation files, or if README / `llms.txt` / roadmap drift back into conflicting names for the second semester or review state.

## Revisit

Revisit after the next batch of review hardening, especially if `reports/next-actions.md` changes from audit queue to completed review receipts.

## Next Operator Action

Park this as calibration residue until a full manifest route audit is available, then rerun only if the route audit changes the front-door confidence.
