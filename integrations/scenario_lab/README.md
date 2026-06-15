# Scenario Lab Pilot Integration

This directory holds a **bounded Scenario Lab pilot** for `strategy-codex`.

## Scope

Use this pilot for:

- singularity-academy questions that need structured future branching
- actor-pressure and scenario-family work
- one readable simulation artifact plus one Presenton-ready visualization path

Do **not** use this pilot as:

- a recursion-gate path
- governed-state truth
- a replacement for ordinary forecasting, strategy notes, or technical implementation work

## Local Shape

- Scenario Lab stays outside this repo as a **neighbor checkout**
- the bridge path is configurable through `SCENARIO_LAB_ROOT` and `SCENARIO_LAB_CMD`
- `.forecast/` is a local WORK-layer run root, not canonical truth

## Pilot Commands

Build an intake packet from local evidence:

```bash
python -m integrations.scenario_lab.export_to_scenario \
  --scenario "Compute sovereignty and agent control over the next 12 months" \
  --domain company-action \
  --evidence-path essays/agent-control-plane.md \
  --evidence-path essays/sovereignty-under-acceleration.md \
  --assumption "External checkout is configured locally" \
  --output compute-sovereignty/packet.json \
  --markdown-output compute-sovereignty/packet.md
```

Run one bounded simulation:

```bash
python -m integrations.scenario_lab.run_gated_simulation \
  --scenario "Compute sovereignty and agent control over the next 12 months" \
  --domain company-action \
  --evidence-path singularity/workshop/sheets/agent-control-plane.md \
  --evidence-path singularity/workshop/sheets/sovereignty-under-acceleration.md
```

Convert a run into Markdown plus an optional presentation bundle:

```bash
python -m integrations.scenario_lab.visualize_simulation \
  --input artifacts/simulations/compute-sovereignty/report.json \
  --output artifacts/simulations/compute-sovereignty/visualization.md \
  --bundle-output artifacts/presentations/scenario-lab-compute-sovereignty.bundle.json
```

## Notes

- All outputs are **WORK-only** and **simulation-only** by default.
- Failure artifacts are part of the pilot: missing checkout, invalid domain, or weak runner behavior should write a bounded report instead of faking success.
- Presenton reuse is intentional: the pilot emits the existing presentation bundle contract instead of creating a separate Scenario Lab deck schema.
