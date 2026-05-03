#!/usr/bin/env bash
# Compare imported civ-mem provenance to docs/ci/civilization_memory_upstream.env.
# Exit 0: match. Exit 1: mismatch. Exit 2: malformed or missing required files.
# Usage: bash scripts/check_civ_mem_upstream_pin.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${ROOT}/docs/ci/civilization_memory_upstream.env"
PROVENANCE_FILE="${ROOT}/research/repos/civilization_memory/STRATEGY-CODEX-PROVENANCE.md"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "error: missing ${ENV_FILE}" >&2
  exit 2
fi

if [[ ! -f "${PROVENANCE_FILE}" ]]; then
  echo "error: missing ${PROVENANCE_FILE}" >&2
  exit 2
fi

PIN_LINE="$(grep -E '^CIV_MEM_UPSTREAM_SHA=' "${ENV_FILE}" | head -1 || true)"
PIN="${PIN_LINE#CIV_MEM_UPSTREAM_SHA=}"
PIN="$(echo "${PIN}" | tr -d '\r' | tr -d ' ')"

IMPORTED_LINE="$(grep -E '^- Imported upstream commit:' "${PROVENANCE_FILE}" | head -1 || true)"
IMPORTED_SHA="${IMPORTED_LINE#- Imported upstream commit: }"
IMPORTED_SHA="$(echo "${IMPORTED_SHA}" | tr -d '\r' | tr -d ' ' | tr -d '`')"

if [[ -z "${PIN}" || -z "${IMPORTED_SHA}" ]]; then
  echo "error: could not parse civ-mem pin or imported SHA" >&2
  exit 2
fi

if [[ "${PIN}" == "${IMPORTED_SHA}" ]]; then
  echo "civ-mem pin check: OK (provenance matches docs/ci pin ${PIN:0:12}...)"
  exit 0
fi

echo "civ-mem pin check: MISMATCH - imported snapshot ${IMPORTED_SHA}" >&2
echo "  expected pin: ${PIN} (from docs/ci/civilization_memory_upstream.env)" >&2
echo "  run: bash scripts/ci/clone_civilization_memory.sh" >&2
exit 1
