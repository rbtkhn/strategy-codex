#!/usr/bin/env python3
"""
Generate domain-pack triage artifacts from skill inventory + disposition SSOT.

Usage:
  python3 scripts/generate_skill_inventory.py   # refresh inventory first
  python3 scripts/generate_domain_pack_triage.py
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
REPO_ROOT = _SCRIPTS.parent

INVENTORY_JSON = REPO_ROOT / "runtime" / "artifacts" / "skill-inventory.json"
DISPOSITIONS_YAML = _SCRIPTS / "domain_pack_dispositions.yaml"
OUTPUT_MD = REPO_ROOT / "runtime" / "artifacts" / "domain-pack-triage.md"
OUTPUT_JSON = REPO_ROOT / "runtime" / "artifacts" / "domain-pack-triage.json"

CLUSTER_ORDER = [
    "civ-state",
    "portable-domain",
    "state-lane",
    "country-culture",
    "domain-helpers",
    "speaker-shelf",
    "work-lane",
    "other-cursor",
    "drafts",
    "_unclustered",
]

CLUSTER_TITLES = {
    "civ-state": "CIV-STATE family",
    "portable-domain": "Portable domain skills (manifest-listed)",
    "state-lane": "State-lane openers",
    "country-culture": "Country culture (art / lit / god)",
    "domain-helpers": "General domain helpers",
    "speaker-shelf": "Speaker / intake / bridge",
    "work-lane": "Work-lane cursor skills",
    "other-cursor": "Other cursor-only domain-pack",
    "drafts": "Drafts (domain-pack)",
    "_unclustered": "Unclustered",
}

RUNBOOK_REF = [
    ("civ-state-primary-text", "exists", "skills/runbooks/civ-state-primary-text.runbook.md"),
    ("civ-state-volume-hardening", "exists", "skills/runbooks/civ-state-volume-hardening.runbook.md"),
    ("domain-lane-survey", "exists", "skills/runbooks/domain-lane-survey.runbook.md"),
    ("speaker-shelf-maintenance", "exists", "skills/runbooks/speaker-shelf-maintenance.runbook.md"),
]


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("PyYAML required: pip install pyyaml") from exc
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise SystemExit(f"Invalid YAML root in {path}")
    return raw


def _load_inventory() -> tuple[list[dict[str, Any]], str]:
    if not INVENTORY_JSON.is_file():
        raise SystemExit(
            f"Missing {INVENTORY_JSON.relative_to(REPO_ROOT)} — run "
            "python3 scripts/generate_skill_inventory.py first"
        )
    payload = json.loads(INVENTORY_JSON.read_text(encoding="utf-8"))
    skills = payload.get("skills")
    if not isinstance(skills, list):
        raise SystemExit(f"Invalid inventory JSON: expected skills list in {INVENTORY_JSON}")
    generated_at = str(payload.get("generated_at", ""))
    return skills, generated_at


def _skill_path(row: dict[str, Any]) -> str:
    if row.get("cursor_target"):
        return str(row["cursor_target"])
    if row.get("portable_source"):
        return f"skills/{row['portable_source']}"
    if row.get("location") == "draft":
        return f"skills/_drafts/{row['name']}/SKILL.md"
    return ""


def _merge_row(row: dict[str, Any], disp_cfg: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    name = row["name"]
    skill_disp = disp_cfg.get(name, {})
    merged = {
        "name": name,
        "location": row.get("location", ""),
        "manifest_listed": bool(row.get("manifest_listed")),
        "cursor_only": row.get("location") in ("cursor-only", "draft"),
        "skill_path": _skill_path(row),
        "category": row.get("category", ""),
        "status": row.get("status", ""),
        "proof_standard": row.get("proof_standard", ""),
        "current_trigger": row.get("activation_trigger", ""),
        "inventory_notes": row.get("notes", ""),
        "proposed_disposition": skill_disp.get(
            "proposed_disposition", defaults.get("proposed_disposition", "REVIEW_WITH_OPERATOR")
        ),
        "post_disposition": skill_disp.get("post_disposition", ""),
        "replacement_or_runbook": skill_disp.get("replacement_or_runbook") or "",
        "reason": skill_disp.get("reason", defaults.get("reason", "")),
        "risk": skill_disp.get("risk", defaults.get("risk", "")),
        "cluster": skill_disp.get("cluster", "_unclustered"),
    }
    if merged["replacement_or_runbook"] is None:
        merged["replacement_or_runbook"] = ""
    return merged


def _summary_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    disp_counter = Counter(r["proposed_disposition"] for r in rows)
    active_missing_proof = sum(
        1
        for r in rows
        if r["status"] == "active" and r["proof_standard"] == "missing"
    )
    return {
        "total_domain_pack_rows": len(rows),
        "by_disposition": dict(sorted(disp_counter.items())),
        "active_proof_missing": active_missing_proof,
    }


def _md_table(rows: list[dict[str, Any]]) -> str:
    headers = [
        "name",
        "location",
        "manifest_listed",
        "cursor_only",
        "status",
        "proof_standard",
        "current_trigger",
        "proposed_disposition",
        "replacement_or_runbook",
        "reason",
        "risk",
    ]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        cells = [str(row.get(h, "")).replace("|", "\\|") for h in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _build_markdown(
    rows: list[dict[str, Any]],
    summary: dict[str, Any],
    inventory_generated_at: str,
    missing_dispositions: list[str],
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    disp_line = " | ".join(f"{k}: {v}" for k, v in summary["by_disposition"].items())
    lines = [
        "# Domain-pack triage (generated)",
        "",
        f"Generated: `{now}`",
        "",
        f"Inventory source: `{INVENTORY_JSON.relative_to(REPO_ROOT).as_posix()}` "
        f"(generated `{inventory_generated_at[:19]}Z`)" if inventory_generated_at else "",
        "",
        "Regenerate:",
        "",
        "```bash",
        "python3 scripts/generate_skill_inventory.py",
        "python3 scripts/generate_domain_pack_triage.py",
        "```",
        "",
        "Disposition SSOT: [`scripts/domain_pack_dispositions.yaml`](../scripts/domain_pack_dispositions.yaml)",
        "",
        "## Summary",
        "",
        f"- **Total domain-pack rows:** {summary['total_domain_pack_rows']}",
        f"- **By disposition:** {disp_line}",
        f"- **Active + proof_standard missing:** {summary['active_proof_missing']} "
        "(target after full pass: 0–3)",
        "",
    ]
    if missing_dispositions:
        lines.extend([
            f"- **WARNING:** {len(missing_dispositions)} skill(s) missing curated disposition "
            f"in YAML: `{', '.join(missing_dispositions)}`",
            "",
        ])

    lines.extend([
        "> **Note:** `civ-state-volume-architect` is **not** domain-pack — it is "
        "`legacy-redirect` → `civ-state` in the skill inventory.",
        "",
    ])

    by_cluster: dict[str, list[dict[str, Any]]] = {c: [] for c in CLUSTER_ORDER}
    for row in rows:
        cluster = row.get("cluster") or "_unclustered"
        if cluster not in by_cluster:
            cluster = "_unclustered"
        by_cluster[cluster].append(row)

    for cluster_key in CLUSTER_ORDER:
        cluster_rows = sorted(by_cluster.get(cluster_key, []), key=lambda r: r["name"])
        if not cluster_rows:
            continue
        title = CLUSTER_TITLES.get(cluster_key, cluster_key)
        lines.extend([f"## {title}", "", _md_table(cluster_rows), ""])

    lines.extend([
        "## Runbook cross-reference",
        "",
        "| Runbook | Status | Path |",
        "| --- | --- | --- |",
    ])
    for name, status, path in RUNBOOK_REF:
        lines.append(f"| `{name}` | **{status}** | `{path}` |")
    lines.append("")
    return "\n".join(lines)


def build_triage() -> tuple[list[dict[str, Any]], dict[str, Any], str, list[str]]:
    inventory_rows, inventory_generated_at = _load_inventory()
    domain_rows = [r for r in inventory_rows if r.get("category") == "domain-pack"]
    if not domain_rows:
        raise SystemExit("No domain-pack rows found in skill inventory")

    disp_root = _load_yaml(DISPOSITIONS_YAML)
    defaults = disp_root.get("defaults") or {}
    disp_cfg = disp_root.get("skills") or {}
    if not isinstance(disp_cfg, dict):
        raise SystemExit("domain_pack_dispositions.yaml: skills must be a mapping")

    merged = [_merge_row(r, disp_cfg, defaults) for r in domain_rows]
    merged.sort(key=lambda r: (CLUSTER_ORDER.index(r["cluster"]) if r["cluster"] in CLUSTER_ORDER else 99, r["name"]))

    inventory_names = {r["name"] for r in domain_rows}
    yaml_names = set(disp_cfg.keys())
    missing_in_yaml = sorted(inventory_names - yaml_names)
    extra_in_yaml = sorted(yaml_names - inventory_names)
    if extra_in_yaml:
        print(
            f"WARN: disposition YAML has {len(extra_in_yaml)} name(s) not in domain-pack inventory: "
            + ", ".join(extra_in_yaml[:5])
            + ("..." if len(extra_in_yaml) > 5 else ""),
            file=sys.stderr,
        )

    summary = _summary_counts(merged)
    return merged, summary, inventory_generated_at, missing_in_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate domain-pack triage artifacts.")
    parser.add_argument(
        "--require-full-yaml",
        action="store_true",
        help="Exit 1 if any domain-pack row lacks an explicit skills: entry in YAML",
    )
    args = parser.parse_args()

    merged, summary, inventory_generated_at, missing_in_yaml = build_triage()

    if args.require_full_yaml and missing_in_yaml:
        print(
            f"ERROR: {len(missing_in_yaml)} domain-pack row(s) missing from domain_pack_dispositions.yaml:",
            ", ".join(missing_in_yaml),
            file=sys.stderr,
        )
        return 1

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inventory_generated_at": inventory_generated_at,
        "dispositions_source": str(DISPOSITIONS_YAML.relative_to(REPO_ROOT).as_posix()),
        "summary": summary,
        "missing_yaml_entries": missing_in_yaml,
        "skills": merged,
        "runbooks": [
            {"name": n, "status": s, "path": p} for n, s, p in RUNBOOK_REF
        ],
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(
        _build_markdown(merged, summary, inventory_generated_at, missing_in_yaml),
        encoding="utf-8",
    )

    print(f"Wrote {OUTPUT_MD.relative_to(REPO_ROOT)} ({len(merged)} rows)")
    print(f"Wrote {OUTPUT_JSON.relative_to(REPO_ROOT)}")
    print(f"Summary: {summary['by_disposition']}")
    if missing_in_yaml:
        print(f"WARN: {len(missing_in_yaml)} row(s) used YAML defaults", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
