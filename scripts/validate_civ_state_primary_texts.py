#!/usr/bin/env python3
"""
Validate CIV-STATE primary-text records, excerpts, and sidecar manifests.

Usage:
  python scripts/validate_civ_state_primary_texts.py
  python scripts/validate_civ_state_primary_texts.py --json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CIV_STATE_DIR = REPO_ROOT / "statecraft" / "states"
SOURCE_RECORDS_DIR = CIV_STATE_DIR / "source-records"
SOURCE_EXCERPTS_DIR = CIV_STATE_DIR / "source-excerpts"
SOURCE_SIDECAR_DIR = CIV_STATE_DIR / "source-sidecar"

RECORD_INDEX = SOURCE_RECORDS_DIR / "index.json"
SIDECAR_INDEX = SOURCE_SIDECAR_DIR / "index.json"

ALLOWED_RIGHTS = {
    "public_domain",
    "official_government_text",
    "operator_authored_transcription",
    "modern_translation_restricted",
    "unclear",
}
ALLOWED_STORAGE = {"metadata_only", "excerpt_only", "full_text_sidecar"}
ALLOWED_WITNESS = {"official_text", "public_domain_text", "academic_text", "scan_ocr", "manual_transcription"}
ALLOWED_VALIDATION = {"unvalidated", "spot_checked", "verified"}
FULLTEXT_RIGHTS = {"public_domain", "official_government_text", "operator_authored_transcription"}
REQUIRED_RECORD_FIELDS = {
    "source_id",
    "civilization",
    "era",
    "branch",
    "title",
    "author_or_body",
    "source_type",
    "date_or_range",
    "original_language",
    "target_language",
    "witness_type",
    "canonical_witness",
    "rights_class",
    "storage_class",
    "acquisition_method",
    "witness_locator",
    "sidecar_locator",
    "canonical_excerpt_available",
    "full_text_available",
    "validation_status",
    "notes",
}
REQUIRED_EXCERPT_TOP = {"excerpt_collection_id", "civilization", "era_focus", "entries"}
REQUIRED_EXCERPT_FIELDS = {"excerpt_id", "source_id", "excerpt_role", "witness_basis", "location", "text", "notes"}
REQUIRED_SIDECAR_FIELDS = {"source_id", "stored_representation", "text_path", "witness_locator", "rights_class", "validation_status"}

def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))

def add_issue(issues: list[dict[str, str]], path: Path, level: str, message: str) -> None:
    issues.append({"path": str(path.relative_to(REPO_ROOT)), "level": level, "message": message})

def validate() -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    record_index = read_json(RECORD_INDEX)
    if not isinstance(record_index, dict) or "records" not in record_index or not isinstance(record_index["records"], list):
        add_issue(issues, RECORD_INDEX, "error", "Record index must define a records list")
        return issues

    record_paths: list[Path] = []
    source_ids: dict[str, Path] = {}
    for rel in record_index["records"]:
        record_path = REPO_ROOT / "statecraft" / "states" / "source-records" / rel
        record_paths.append(record_path)
        if not record_path.exists():
            add_issue(issues, RECORD_INDEX, "error", f"Indexed source record missing: {rel}")
            continue

        data = read_json(record_path)
        if not isinstance(data, dict):
            add_issue(issues, record_path, "error", "Source record must be a JSON object")
            continue

        missing = sorted(REQUIRED_RECORD_FIELDS - set(data.keys()))
        if missing:
            add_issue(issues, record_path, "error", f"Missing required fields: {', '.join(missing)}")
            continue

        source_id = str(data["source_id"])
        if source_id in source_ids:
            add_issue(issues, record_path, "error", f"Duplicate source_id also used by {source_ids[source_id].relative_to(REPO_ROOT)}")
        source_ids[source_id] = record_path

        if data["rights_class"] not in ALLOWED_RIGHTS:
            add_issue(issues, record_path, "error", f"Invalid rights_class: {data['rights_class']}")
        if data["storage_class"] not in ALLOWED_STORAGE:
            add_issue(issues, record_path, "error", f"Invalid storage_class: {data['storage_class']}")
        if data["witness_type"] not in ALLOWED_WITNESS:
            add_issue(issues, record_path, "error", f"Invalid witness_type: {data['witness_type']}")
        if data["validation_status"] not in ALLOWED_VALIDATION:
            add_issue(issues, record_path, "error", f"Invalid validation_status: {data['validation_status']}")

        canonical = data.get("canonical_witness")
        if not isinstance(canonical, dict) or not canonical.get("label") or not canonical.get("locator"):
            add_issue(issues, record_path, "error", "canonical_witness must include label and locator")

        if data["target_language"] != data["original_language"] and not data.get("working_translation"):
            add_issue(issues, record_path, "error", "Translated working witness requires working_translation metadata")

        if data["storage_class"] == "full_text_sidecar":
            if data["rights_class"] not in FULLTEXT_RIGHTS:
                add_issue(issues, record_path, "error", "full_text_sidecar requires a lawful full-text rights_class")
            if not data["sidecar_locator"]:
                add_issue(issues, record_path, "error", "full_text_sidecar requires sidecar_locator")
            if data["full_text_available"] is not True:
                add_issue(issues, record_path, "error", "full_text_sidecar requires full_text_available=true")

        if data["full_text_available"] and not data["witness_locator"]:
            add_issue(issues, record_path, "error", "full_text_available=true requires witness_locator")

    for excerpt_path in sorted(SOURCE_EXCERPTS_DIR.rglob("*.json")):
        if excerpt_path.name == "index.json":
            continue
        data = read_json(excerpt_path)
        if not isinstance(data, dict):
            add_issue(issues, excerpt_path, "error", "Excerpt file must be a JSON object")
            continue
        missing = sorted(REQUIRED_EXCERPT_TOP - set(data.keys()))
        if missing:
            add_issue(issues, excerpt_path, "error", f"Missing excerpt top-level fields: {', '.join(missing)}")
            continue
        if not isinstance(data["entries"], list) or not data["entries"]:
            add_issue(issues, excerpt_path, "error", "Excerpt file must contain a non-empty entries list")
            continue
        for entry in data["entries"]:
            if not isinstance(entry, dict):
                add_issue(issues, excerpt_path, "error", "Excerpt entry must be an object")
                continue
            missing_entry = sorted(REQUIRED_EXCERPT_FIELDS - set(entry.keys()))
            if missing_entry:
                add_issue(issues, excerpt_path, "error", f"Excerpt entry missing fields: {', '.join(missing_entry)}")
                continue
            if entry["source_id"] not in source_ids:
                add_issue(issues, excerpt_path, "error", f"Excerpt entry references unknown source_id: {entry['source_id']}")

    sidecar_index = read_json(SIDECAR_INDEX)
    if not isinstance(sidecar_index, dict) or "manifests" not in sidecar_index or not isinstance(sidecar_index["manifests"], list):
        add_issue(issues, SIDECAR_INDEX, "error", "Sidecar index must define a manifests list")
        return issues

    for rel in sidecar_index["manifests"]:
        manifest_path = REPO_ROOT / "statecraft" / "states" / "source-sidecar" / rel
        if not manifest_path.exists():
            add_issue(issues, SIDECAR_INDEX, "error", f"Indexed sidecar manifest missing: {rel}")
            continue
        data = read_json(manifest_path)
        if not isinstance(data, dict):
            add_issue(issues, manifest_path, "error", "Sidecar manifest must be a JSON object")
            continue
        missing = sorted(REQUIRED_SIDECAR_FIELDS - set(data.keys()))
        if missing:
            add_issue(issues, manifest_path, "error", f"Missing sidecar manifest fields: {', '.join(missing)}")
            continue
        if data["source_id"] not in source_ids:
            add_issue(issues, manifest_path, "error", f"Sidecar manifest references unknown source_id: {data['source_id']}")
            continue
        text_path = REPO_ROOT / Path(data["text_path"])
        if not text_path.exists():
            add_issue(issues, manifest_path, "error", f"Sidecar text missing: {data['text_path']}")
        record = read_json(source_ids[data["source_id"]])
        if record["sidecar_locator"] != data["text_path"]:
            add_issue(issues, manifest_path, "error", "Sidecar manifest text_path does not match record sidecar_locator")

    return issues

def format_text(issues: list[dict[str, str]]) -> str:
    if not issues:
        return "CIV-STATE primary-text layer valid."
    lines: list[str] = []
    for issue in issues:
        marker = "ERROR" if issue["level"] == "error" else "WARN"
        lines.append(f"[{marker}] {issue['path']}: {issue['message']}")
    lines.append(f"\n{len(issues)} issue(s) found.")
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CIV-STATE primary-text records and sidecar state.")
    parser.add_argument("--json", action="store_true", help="Output issues as JSON")
    args = parser.parse_args()

    issues = validate()
    if args.json:
        print(json.dumps(issues, indent=2))
    else:
        print(format_text(issues))
    return 1 if any(issue["level"] == "error" for issue in issues) else 0

if __name__ == "__main__":
    raise SystemExit(main())
