# Local read-only directory index adapter

**Status:** Narrow **metadata-plane** step â€” **`scripts/mcp_local_index.py`** walks repo directories under **[`platform/config/mcp-local-read-allowlist.yaml`](../../platform/config/mcp-local-read-allowlist.yaml)** only. It emits **paths, kinds, sizes**, and optional **line counts / SHA256** with **`max_file_bytes`** caps â€” **never file contents or excerpts**. **No MCP servers**, **no credentials**, **no network**, **no shell**.

**Related:** [`schemas/mcp-local-index-request.v1.json`](../../schemas/mcp-local-index-request.v1.json), [`docs/mcp/governed-mcp-layer.md`](governed-mcp-layer.md), capability **`filesystem_readonly`** in [`platform/config/mcp-capabilities.yaml`](../../platform/config/mcp-capabilities.yaml).

---

## Companion to the local read-only file adapter

| Aspect | File read ([`mcp_local_readonly.py`](../../scripts/mcp_local_readonly.py)) | Directory index (`mcp_local_index.py`) |
|--------|---------------------------------------------------------------------------|----------------------------------------|
| Operation | Read **one file** as UTF-8 (bounded excerpt optional) | **List** files and directories under a root |
| Emitted body | Metrics + optional excerpt | **Metadata table only** â€” no excerpts |
| Receipt **`capability.id`** | **`filesystem_readonly`** | **`filesystem_readonly`** |
| Banner | `LOCAL READ-ONLY MCP-SHAPED RUN Â· â€¦` | `LOCAL READ-ONLY DIRECTORY INDEX Â· â€¦` |

Both scripts share the **same allowlist**, **`filesystem_readonly`** receipts with **`access.resources_written: []`**, and **`result.artifacts`** for packet + receipt paths.

---

## How this differs from the mock harness

| Aspect | Mock harness ([`mcp_mock_harness.py`](../../scripts/mcp_mock_harness.py)) | Directory index (`mcp_local_index.py`) |
|--------|---------------------------------------------------------------------------|----------------------------------------|
| Data source | Declared **`mock_request`** / **`mock_response`** JSON only | Actual **`path`** traversal on disk |
| Receipt **`capability.id`** | **`mcp_mock_harness`** | **`filesystem_readonly`** |
| Purpose | Simulate posture vs registry | Enumerate allowlisted tree metadata |

---

## How this differs from general MCP

- **No MCP host/server**: invocation is **`python scripts/mcp_local_index.py`** reading JSON + YAML â€” no IDE MCP process graph.
- **No remote identifiers**: paths resolve inside **`repo-root`** after containment checks; traversal **does not follow symlinks** (entries skipped safely).

---

## Allowlist model

[`platform/config/mcp-local-read-allowlist.yaml`](../../platform/config/mcp-local-read-allowlist.yaml) defines:

- **`allowed_roots`** â€” repo-relative prefixes permitted for indexing (e.g. **`docs/`**, **`schemas/`**, named **`runtime/artifacts/â€¦`** buckets).
- **`blocked_roots`** â€” hard deny prefixes (**``**, **`venv/`**, **`.git/`**, â€¦).
- **`blocked_files`** / **`blocked_name_patterns`** â€” basename skips during traversal (**skipped**, increment skip count; root path failure still fails closed before indexing).
- **`max_file_bytes`** â€” caps optional line-count and hash reads per file (oversize shows placeholder in table; entries still listed).

Rejected **request root** paths fail closed (**exit 1**) **before** receipt emission.

---

## Traversal semantics

- **`recursive: false`** â€” direct children of the indexed directory only; **`max_depth`** is not applied.
- **`recursive: true`** â€” descend into subdirectories; **`max_depth`** is the number of **levels below** the indexed directory to recurse ( **`0`** lists immediate children only â€” same surface as non-recursive one-shot list, but recursive mode still honors symlink/block skips consistently).
- **`max_entries`** â€” cap on emitted rows (deterministic sort by name at each level).
- **Symlinks** â€” not followed; symlink entries are **skipped** (counted).

---

## Receipt behavior

- Receipt **`capability.id`** = **`filesystem_readonly`** (registry **`output_lane`:** **`runtime_only`**).
- Registry **`writes: []`** â‡’ **`access.resources_written`** must be **empty** for validated receipts â€” packet paths appear under **`result.artifacts`** only.
- **`access.resources_read`** lists **request JSON path** and **indexed directory path** (not every file visited).

See packet **`## Receipt note`** under **`runtime/artifacts/mcp-local-index/`**.

---

## Forbidden paths (high level)

- Absolute paths, **`..`**, **``**, blocked roots/files/globs. Request roots outside **`allowed_roots`** fail closed.

Passing this adapter does **not** approve wider live MCP integration or Record merges â€” **[`AGENTS.md`](../../AGENTS.md)** gate rules are unchanged.

