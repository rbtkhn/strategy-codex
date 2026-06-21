# Contributor checklist — generated surfaces

1. Authority: **generated** — rebuildable, non-authoritative.
2. Regenerate via documented script; add header comment when introducing new generators.
3. Do not hand-edit drift-prone indexes (`thread-index.md`, hybrid `LLM-ROUTING.md`, etc.) — run generator `--check` in CI.
4. Future manifest: `generated-manifest.yaml` (Sprint 6).
5. Preflight: `python3 scripts/generate_llm_routing.py --check` when touching routing inputs.
