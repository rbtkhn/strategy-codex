# CI pins

- **`civilization_memory_upstream.env`** - URL + commit SHA for the civ-mem
  snapshot vendored into `research/repos/civilization_memory`. Use it as
  provenance and as the refresh pin for
  `scripts/ci/clone_civilization_memory.sh`.
- **`scripts/test_civmem_tri_frame_routing.py`** - With no arguments, runs
  **RUSSIA** (full spine + sample MEMs) then **ROME** (partial spine if
  `MEM-RELEVANCE-ROME.md` is absent; Barnes-oriented MEM paths). Tools that
  rely on `MEM-RELEVANCE-<X>.md` and `content/civilizations/<X>/` layout
  should re-run this after snapshot pin bumps.
- **Snapshot vs pin** - Optional: `bash scripts/check_civ_mem_upstream_pin.sh`
  compares the imported SHA recorded in
  `research/repos/civilization_memory/STRATEGY-CODEX-PROVENANCE.md` to the env
  pin (exit `1` on mismatch). Use after a manual civ-mem refresh or before a
  strategy/dream closeout when tri-frame routing depends on the local snapshot.
