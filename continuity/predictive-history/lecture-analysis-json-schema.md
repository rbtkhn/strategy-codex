# Lecture analysis JSON schema (Predictive History)
<!-- word_count: 532 -->

Operator research only - not Voice knowledge until merged through the gate. See [README.md](./README.md) for corpus boundaries.

## File location

Sidecar next to the Markdown memo, same stem:

- `analysis/<video_id>-<slug>-analysis.md` -> `analysis/<video_id>-<slug>-analysis.json`

Optional front-matter key: `analysis_json_path` if the JSON lives elsewhere.

## Version fields

| Field | Where |
|-------|------|
| `schema_version` | Root of JSON (for example `1.0`) |
| `memo_format_version` | YAML front matter on `.md` (for example `1`) |
| `analysis_json_version` | Optional; if set, must match `schema_version` |

## Root object (required keys)

| Key | Type | Description |
|-----|------|-------------|
| `schema_version` | string | Schema version for migrations |
| `summary` | string | Short synthesis of the lecture |
| `key_claims` | array | See below |
| `predictions` | array | Forecast-like rows (map to prediction registry) |
| `divergences_from_prior` | array | Contrasts vs earlier lectures or named mainstream |
| `open_questions` | array of string | Unresolved questions |
| `cross_links` | array | Links to other sources or memos |

Optional:

| Key | Type | Description |
|-----|------|-------------|
| `source` | object | `video_id`, `source_id`, `model_id` |
| `civ_mem` | object | Structured civ-mem bridge fields; see below |

## `key_claims[]` objects

| Key | Type | Required |
|-----|------|----------|
| `claim_text` | string | yes |
| `claim_type` | string | yes - for example `observation`, `interpretation`, `forecast`, `normative` |
| `confidence` | string | no - for example `low`, `medium`, `high` |
| `evidence_quote_ref` | string | no - pointer into transcript or timestamp |

## `predictions[]` objects (align with JSONL)

| Key | Type | Required |
|-----|------|----------|
| `claim_summary` | string | yes |
| `claim_type` | string | yes |
| `excerpt` | string | no |
| `evaluation_window` | object or null | `{ "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" }` |
| `resolution_status` | string | default `pending` for new extractions |

## `divergences_from_prior[]` objects

| Key | Type | Required |
|-----|------|----------|
| `jiang_claim` | string | yes |
| `mainstream_anchor` | string | no |
| `mainstream_summary` | string | no |
| `divergence_type` | string | no - `empirical`, `interpretive`, etc. |
| `strength` | string | no |

## `cross_links[]` objects

| Key | Type | Required |
|-----|------|----------|
| `target` | string | yes - slug, `video_id`, or URL |
| `relation` | string | no - for example `supports`, `contradicts`, `extends` |
| `note` | string | no |

## `civ_mem` object

Use this object for the civ-mem reference spine. Keep it short and operator-written.

| Key | Type | Description |
|-----|------|-------------|
| `paths` | array of string | Exact civ-mem or CMC paths used as references |
| `case_families` | array of string | Historical family labels |
| `alignment_notes` | string | Why the lecture and civ-mem overlap |
| `mismatch_notes` | string | Where the analogy breaks or overreaches |
| `bridge_paragraph` | string | Short bridge from lecture to civ-mem |
| `confidence` | string | `low`, `medium`, or `high` |

If the bridge is weak, set `confidence` to `low` and say so instead of forcing a match.

## Example (minimal)

```json
{
  "schema_version": "1.0",
  "summary": "Lecture argues X; predicts Y under conditions Z.",
  "key_claims": [
    {
      "claim_text": "Alliance seams open under electoral cycles.",
      "claim_type": "interpretation",
      "confidence": "medium",
      "evidence_quote_ref": "~12:00"
    }
  ],
  "predictions": [
    {
      "claim_summary": "Event E within two years.",
      "claim_type": "time_bounded",
      "excerpt": "verbatim hint",
      "evaluation_window": { "start": "2026-01-01", "end": "2028-12-31" },
      "resolution_status": "pending"
    }
  ],
  "divergences_from_prior": [],
  "open_questions": ["What metric for 'popular'?"],
  "cross_links": [
    { "target": "geo-strategy-01-iran-strategy-matrix-2024-04-24.md", "relation": "extends", "note": "Iran matrix" }
  ],
  "civ_mem": {
    "paths": ["docs/civilization-memory/..."],
    "case_families": ["Rome", "Persia"],
    "alignment_notes": "Seam and institution framing aligns with the lecture.",
    "mismatch_notes": "No strong support for a single civilizational collapse timeline.",
    "bridge_paragraph": "CIV-MEM treats this as a seam-and-institution problem with a long horizon, not just a short news-cycle event.",
    "confidence": "medium"
  },
  "source": { "video_id": "xEEpOxqdU5E", "source_id": "geo-01" }
}
```

Validation: `python3 scripts/work_jiang/validate_lecture_analysis_json.py path/to/file.json`
