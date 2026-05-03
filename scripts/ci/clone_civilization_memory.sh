#!/usr/bin/env bash
# Refresh the vendored civilization_memory snapshot at the pinned commit.
# This is a manual refresh helper for strategy-codex, not a default CI bootstrap.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

PIN="${ROOT}/docs/ci/civilization_memory_upstream.env"
if [[ ! -f "$PIN" ]]; then
  echo "clone_civilization_memory.sh: missing ${PIN}" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$PIN"
set +a

: "${CIV_MEM_UPSTREAM_URL:?set in docs/ci/civilization_memory_upstream.env}"
: "${CIV_MEM_UPSTREAM_SHA:?set in docs/ci/civilization_memory_upstream.env}"

TARGET="${ROOT}/research/repos/civilization_memory"
TMP_DIR="${ROOT}/.codex-tmp/civmem-refresh"

rm -rf "$TMP_DIR"
mkdir -p "$(dirname "$TMP_DIR")"

git clone "$CIV_MEM_UPSTREAM_URL" "$TMP_DIR"
git -C "$TMP_DIR" checkout "$CIV_MEM_UPSTREAM_SHA"

rm -rf "$TARGET"
mkdir -p "$(dirname "$TARGET")"
cp -R "$TMP_DIR" "$TARGET"
rm -rf "${TARGET}/.git"

cat > "${TARGET}/STRATEGY-CODEX-PROVENANCE.md" <<EOF
## Strategy-Codex Provenance

- Source repository: \`${CIV_MEM_UPSTREAM_URL}\`
- Imported upstream commit: \`${CIV_MEM_UPSTREAM_SHA}\`
- Imported into \`strategy-codex\`: \`$(date +%F)\`

This directory is a \`strategy-codex\`-tracked snapshot of civ-mem kept at
\`research/repos/civilization_memory\` so strategy workflows can rely on a local,
repo-native corpus.

The upstream repository remains a historical reference for provenance and manual
refreshes. Normal strategy work should treat this in-repo snapshot as the
canonical working corpus in this workspace.
EOF

rm -rf "$TMP_DIR"
echo "civilization_memory vendored at ${CIV_MEM_UPSTREAM_SHA}"
