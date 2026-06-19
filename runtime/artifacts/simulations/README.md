# Simulation Artifacts

This directory stores WORK-layer simulation outputs.

These files are:

- derived
- advisory
- rebuildable
- non-Record
- not approval receipts

Recommended contents:

- one run folder per scenario
- one `manifest.jsonl` row per run
- optional Markdown visualization or bundle-ready outputs

Suggested layout:

```text
runtime/artifacts/simulations/
  manifest.jsonl
  <scenario-slug>/
    packet.json
    packet.md
    raw-scenario-lab-output.json
    report.json
    report.md
    visualization.md
```

Rule: simulation artifacts may support singularity, strategy, or forecasting work, but they do not update Record surfaces directly.

See:

- [work-forecast lane](../../docs/skill-work/work-forecast/README.md)
- [Counterfactual Fork Simulator](../../docs/counterfactual-fork-simulator.md)

