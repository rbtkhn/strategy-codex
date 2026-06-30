from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STATECRAFT_ROOT = REPO_ROOT / "codex" / "academy" / "statecraft"
MIGRATION_ROOT = STATECRAFT_ROOT / "civ-emp" / "migration"
LANES = {
    "america": {
        "folder": "AMERICA",
        "title": "America",
        "lane_root": STATECRAFT_ROOT / "america",
    },
    "russia": {
        "folder": "RUSSIA",
        "title": "Russia",
        "lane_root": STATECRAFT_ROOT / "russia",
    },
    "china": {
        "folder": "CHINA",
        "title": "China",
        "lane_root": STATECRAFT_ROOT / "china",
    },
    "iran": {
        "folder": "PERSIA",
        "title": "Iran",
        "lane_root": STATECRAFT_ROOT / "iran",
    },
}
FIRST_WAVE_CLASSES = ("state-memory", "geo", "war", "peace", "empire-instrument")
FIRST_WAVE_FAMILIES = [
    {
        "id": 1,
        "family": "what makes a settlement real rather than theatrical",
        "civilization_reading": "legitimacy, memory, identity, recognition, continuity",
        "empire_reading": "guarantor structure, enforcement carrier, instrument durability",
        "hinge_reading": "settlement design must pair civilizational recognition with a governable enforcement carrier",
    },
    {
        "id": 2,
        "family": "when does a pressured hegemon misread its own power, limits, or durability",
        "civilization_reading": "self-image, legitimacy narrative, inherited mission",
        "empire_reading": "overextension, amplification trap, decaying instrument set",
        "hinge_reading": "restoration requires trimming instrument reach before civilizational self-image turns brittle",
    },
    {
        "id": 3,
        "family": "when do older strategic memories continue to constrain present actors",
        "civilization_reading": "living memory, sacred grammar, civilizational continuity",
        "empire_reading": "how those memories alter deterrence, corridors, alliance, and coercive behavior",
        "hinge_reading": "active policy must read memory as a live strategic carrier rather than as inert heritage",
    },
    {
        "id": 4,
        "family": "when does coercion fail to convert into the political outcome it claims to serve",
        "civilization_reading": "what political legitimacy or social acceptance coercion cannot generate",
        "empire_reading": "instrument failure, escalation without settlement, amplification without control",
        "hinge_reading": "statecraft must reattach force to a bounded political end before entropy outruns control",
    },
    {
        "id": 5,
        "family": "when do broken contact regimes and arms-control inheritances make escalation more dangerous than the proxy-war script admits",
        "civilization_reading": "memory of danger, successor fear, procedural caution",
        "empire_reading": "command channels, deterrence architecture, escalation thresholds",
        "hinge_reading": "restoration means rebuilding contact procedure before rivalry management collapses",
    },
    {
        "id": 6,
        "family": "how does remembered exclusion shape the politics of direct great-power settlement",
        "civilization_reading": "status memory, humiliation, exclusion anxiety",
        "empire_reading": "bargaining geography, corridor access, and outer-power settlement mechanics",
        "hinge_reading": "durable bargaining must answer symbolic inclusion and actual geographic access together",
    },
]
PRIMARY_FAMILY_BY_CLASS = {
    "state-memory": FIRST_WAVE_FAMILIES[2]["family"],
    "geo": FIRST_WAVE_FAMILIES[5]["family"],
    "war": FIRST_WAVE_FAMILIES[3]["family"],
    "peace": FIRST_WAVE_FAMILIES[0]["family"],
    "empire-instrument": FIRST_WAVE_FAMILIES[1]["family"],
}
SECONDARY_FAMILY_BY_CLASS = {
    "state-memory": FIRST_WAVE_FAMILIES[1]["family"],
    "geo": FIRST_WAVE_FAMILIES[2]["family"],
    "war": FIRST_WAVE_FAMILIES[4]["family"],
    "peace": FIRST_WAVE_FAMILIES[5]["family"],
    "empire-instrument": FIRST_WAVE_FAMILIES[3]["family"],
}
WORD_BANDS = {
    "state-memory": "3500-4500",
    "geo": "2500-3500",
    "war": "3000-4000",
    "peace": "3000-4000",
    "empire-instrument": "2500-3500",
}
PILOT_PAIR_DEFAULTS = {
    "america-state-memory": {
        "status": "cut_over",
        "counterweight_present": "yes",
        "transaction_hook_present": "yes",
        "notes": "phase-one pilot pair materialized; America README routing now prefers the pair and legacy civ-mem remains explicit provenance inside the object",
    },
    "america-empire-instrument": {
        "status": "cut_over",
        "counterweight_present": "yes",
        "transaction_hook_present": "yes",
        "notes": "phase-one pilot pair materialized; existing seed path now carries the active empire object and America README routing prefers it as the empire-side opening",
    },
}
CORPUS_BUDGET = {
    "v1_target": 150000,
    "v1_band": [120000, 180000],
    "hard_ceiling": 180000,
    "phase2_active_proving_cases": ["America", "Russia", "China", "Iran"],
    "volume_targets": {
        "civilization": {"target": 90000, "band": [70000, 100000]},
        "empire": {"target": 60000, "band": [50000, 80000]},
    },
    "first_wave_core_minimum": [60000, 90000],
    "first_wave_object_core": [58000, 78000],
    "hinge_budget": [8000, 12000],
    "first_wave_practical_target": [66000, 90000],
    "v1_remainder": {
        "cross_lane_canonical_family_synthesis": [18000, 25000],
        "volume_level_orientation_and_retrieval": [6000, 10000],
        "second_wave_depth_reserve": [20000, 35000],
    },
    "symmetry_rule": {
        "minimum_empire_share_of_civilization": 0.6,
        "maximum_civilization_to_empire_ratio": 2.0,
        "max_single_lane_share_of_v1_total": 0.30,
    },
    "phase2_tracking": {
        "helix_object_words": "track per-lane helix surface growth without replacing the historical strand scaffold",
        "strand_subtotals": "track first-wave strand words by lane beneath the helix layer",
        "canonical_family_synthesis_surfaces": "track future cross-lane family synthesis notes once they exist",
        "orientation_and_retrieval_surfaces": "track future top-layer orientation and retrieval surfaces once they exist",
    },
}
REF_RE = re.compile(
    r"research/repos/civilization_memory/content/civilizations/[A-Z]+/[^`\s]+\.md"
)
TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")
STATUS_VALUES = {"unstarted", "in_progress", "materialized", "cut_over", "verified"}
YES_NO_VALUES = {"yes", "no"}

@dataclass(frozen=True)
class Occurrence:
    lane: str
    lane_title: str
    file_path: str
    object_class: str
    upstream_ref: str
    upstream_folder: str
    line_number: int
    line_text: str

def normalize_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        value = value[1:-1]
    return value.strip()

def parse_markdown_table(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    rows: dict[str, list[str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = TABLE_ROW_RE.match(line)
        if not match:
            continue
        cells = [normalize_cell(cell) for cell in match.group(1).split("|")]
        if not cells or cells[0] in {"---", "Target object id", "Target object"}:
            continue
        if set(cells[0]) == {"-"}:
            continue
        rows[cells[0]] = cells
    return rows

def get_existing_ledger_value(
    row: list[str], index: int, allowed: set[str] | None = None, default: str = ""
) -> str:
    if len(row) <= index:
        return default
    value = row[index]
    if allowed is not None and value not in allowed:
        return default
    return value

def get_existing_note(row: list[str], default: str) -> str:
    value = get_existing_ledger_value(row, 15, None, default)
    if value in YES_NO_VALUES or value in STATUS_VALUES or not value:
        return default
    return value

def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))

def file_word_count(path: Path) -> int:
    return word_count(path.read_text(encoding="utf-8"))

def infer_object_class(rel_path: Path) -> str:
    parts = rel_path.parts
    filename = rel_path.name
    if "civilization" in parts:
        if "objects" in parts and filename == "state-memory.md":
            return "state-memory"
        stem = rel_path.stem
        if stem in {"geo", "war", "peace", "god", "lit", "art"}:
            return stem
        if stem == "seed-patterns":
            return "seed-patterns"
        return "civilization-other"
    if "empire" in parts:
        if filename == "seed-instruments.md":
            return "empire-instrument"
        return "empire-other"
    if "state" in parts:
        return "state"
    if "transactions" in parts:
        return "transaction"
    if filename == "helix.md":
        return "helix"
    return "other"

def collect_occurrences() -> list[Occurrence]:
    occurrences: list[Occurrence] = []
    for lane, lane_meta in LANES.items():
        lane_root = lane_meta["lane_root"]
        for file_path in sorted(lane_root.rglob("*.md")):
            rel_path = file_path.relative_to(REPO_ROOT)
            text = file_path.read_text(encoding="utf-8")
            object_class = infer_object_class(file_path.relative_to(lane_root))
            for line_number, line in enumerate(text.splitlines(), start=1):
                refs = REF_RE.findall(line)
                for ref in refs:
                    upstream_folder = Path(ref).parts[-2]
                    occurrences.append(
                        Occurrence(
                            lane=lane,
                            lane_title=lane_meta["title"],
                            file_path=rel_path.as_posix(),
                            object_class=object_class,
                            upstream_ref=ref,
                            upstream_folder=upstream_folder,
                            line_number=line_number,
                            line_text=line.strip(),
                        )
                    )
    return occurrences

def target_surface_for(lane: str, object_class: str) -> str:
    base = f"continuity/academy/statecraft/{lane}"
    if object_class == "state-memory":
        return f"{base}/civilization/objects/state-memory.md"
    if object_class in {"geo", "war", "peace"}:
        return f"{base}/civilization/{object_class}.md"
    if object_class == "empire-instrument":
        return f"{base}/empire/seed-instruments.md"
    raise ValueError(f"Unexpected first-wave object class: {object_class}")

def compute_word_metrics() -> dict:
    lane_totals = {}
    first_wave_totals_by_lane = {}
    helix_totals_by_lane = {}
    civ_emp_total = 0
    civ_emp_file_count = 0
    target_word_counts: dict[str, int] = {}
    family_word_counts = Counter()
    first_wave_core_total = 0

    civ_emp_files = list((STATECRAFT_ROOT / "civ-emp").rglob("*.md"))
    civ_emp_total = sum(file_word_count(path) for path in civ_emp_files)
    civ_emp_file_count = len(civ_emp_files)

    for lane, lane_meta in LANES.items():
        lane_root = lane_meta["lane_root"]
        lane_files = list(lane_root.rglob("*.md"))
        lane_total = sum(file_word_count(path) for path in lane_files)
        lane_totals[lane_meta["title"]] = {"words": lane_total, "file_count": len(lane_files)}

        hinge_path = lane_root / "helix.md"
        hinge_words = file_word_count(hinge_path) if hinge_path.exists() else 0
        civ_words = 0
        emp_words = 0
        pilot_civ_words = 0
        pilot_emp_words = 0
        target_ids = []
        for object_class in FIRST_WAVE_CLASSES:
            target_id = f"{lane}-{object_class}"
            path = REPO_ROOT / target_surface_for(lane, object_class)
            words = file_word_count(path) if path.exists() else 0
            target_word_counts[target_id] = words
            first_wave_core_total += words
            family_word_counts[PRIMARY_FAMILY_BY_CLASS[object_class]] += words
            secondary_family = SECONDARY_FAMILY_BY_CLASS[object_class]
            if secondary_family != PRIMARY_FAMILY_BY_CLASS[object_class]:
                family_word_counts[secondary_family] += words
            target_ids.append(target_id)
            if object_class == "empire-instrument":
                emp_words += words
                pilot_emp_words += words
            else:
                civ_words += words
                if object_class == "state-memory":
                    pilot_civ_words += words
        ratio = round(civ_words / emp_words, 2) if emp_words else None
        share = round(emp_words / civ_words, 2) if civ_words else None
        pilot_ratio = round(pilot_civ_words / pilot_emp_words, 2) if pilot_emp_words else None
        pilot_share = round(pilot_emp_words / pilot_civ_words, 2) if pilot_civ_words else None
        helix_totals_by_lane[lane_meta["title"]] = {
            "path": hinge_path.relative_to(REPO_ROOT).as_posix() if hinge_path.exists() else "",
            "words": hinge_words,
        }
        first_wave_totals_by_lane[lane_meta["title"]] = {
            "target_ids": target_ids,
            "civilization_words": civ_words,
            "empire_words": emp_words,
            "hinge_words": hinge_words,
            "strand_words": civ_words + emp_words,
            "civilization_to_empire_ratio": ratio,
            "empire_share_of_civilization": share,
            "pilot_civilization_words": pilot_civ_words,
            "pilot_empire_words": pilot_emp_words,
            "pilot_civilization_to_empire_ratio": pilot_ratio,
            "pilot_empire_share_of_civilization": pilot_share,
        }

    canonical_family_synthesis_files = sorted(MIGRATION_ROOT.glob("canonical-family-*.md"))
    orientation_and_retrieval_files = sorted(MIGRATION_ROOT.glob("orientation-*.md")) + sorted(
        MIGRATION_ROOT.glob("retrieval-*.md")
    )

    phase2_metrics = {
        "helix_objects": {
            "active_proving_cases": CORPUS_BUDGET["phase2_active_proving_cases"],
            "total_words": sum(item["words"] for item in helix_totals_by_lane.values()),
            "by_lane": helix_totals_by_lane,
        },
        "strand_subtotals_by_lane": {
            lane: {
                "words": item["strand_words"],
                "object_count": len(FIRST_WAVE_CLASSES),
            }
            for lane, item in first_wave_totals_by_lane.items()
        },
        "canonical_family_synthesis_surfaces": {
            "surface_count": len(canonical_family_synthesis_files),
            "current_words": sum(file_word_count(path) for path in canonical_family_synthesis_files),
            "surfaces": [
                {
                    "path": path.relative_to(REPO_ROOT).as_posix(),
                    "words": file_word_count(path),
                }
                for path in canonical_family_synthesis_files
            ],
        },
        "orientation_and_retrieval_surfaces": {
            "surface_count": len(orientation_and_retrieval_files),
            "current_words": sum(file_word_count(path) for path in orientation_and_retrieval_files),
            "surfaces": [
                {
                    "path": path.relative_to(REPO_ROOT).as_posix(),
                    "words": file_word_count(path),
                }
                for path in orientation_and_retrieval_files
            ],
        },
    }

    return {
        "lane_totals": lane_totals,
        "civ_emp_total_words": civ_emp_total,
        "civ_emp_file_count": civ_emp_file_count,
        "target_word_counts": target_word_counts,
        "first_wave_core_total_words": first_wave_core_total,
        "first_wave_lane_totals": first_wave_totals_by_lane,
        "canonical_family_word_counts": dict(family_word_counts),
        "phase2_metrics": phase2_metrics,
    }

def compute_inventory(occurrences: list[Occurrence], word_metrics: dict) -> dict:
    by_lane = Counter(o.lane_title for o in occurrences)
    by_object_class = Counter(o.object_class for o in occurrences)
    by_upstream_folder = Counter(o.upstream_folder for o in occurrences)
    files_by_lane: dict[str, set[str]] = defaultdict(set)
    refs_by_file: dict[str, set[str]] = defaultdict(set)
    duplicate_refs: dict[str, set[str]] = defaultdict(set)
    target_consumers: dict[tuple[str, str], set[str]] = defaultdict(set)
    target_ref_counts: Counter[tuple[str, str]] = Counter()

    existing_ledger_rows = parse_markdown_table(MIGRATION_ROOT / "migration-ledger.md")
    existing_manifest_rows = parse_markdown_table(MIGRATION_ROOT / "source-map-manifest.md")

    for o in occurrences:
        files_by_lane[o.lane_title].add(o.file_path)
        refs_by_file[o.file_path].add(o.upstream_ref)
        duplicate_refs[o.upstream_ref].add(o.file_path)
        if o.object_class in FIRST_WAVE_CLASSES:
            target_consumers[(o.lane, o.object_class)].add(o.file_path)
            target_ref_counts[(o.lane, o.object_class)] += 1

    duplicate_entries = []
    for upstream_ref, files in duplicate_refs.items():
        if len(files) > 1:
            duplicate_entries.append(
                {
                    "upstream_ref": upstream_ref,
                    "consumer_count": len(files),
                    "consumer_files": sorted(files),
                }
            )
    duplicate_entries.sort(key=lambda item: (-item["consumer_count"], item["upstream_ref"]))

    default_note = (
        "phase-one symmetric target; cut over only when lane-local citation order prefers civ-emp and legacy civ-mem remains provenance only"
    )
    first_wave_targets = []
    for lane, lane_meta in LANES.items():
        empire_id = f"{lane}-empire-instrument"
        lane_budget = word_metrics["first_wave_lane_totals"][lane_meta["title"]]
        for object_class in FIRST_WAVE_CLASSES:
            object_id = f"{lane}-{object_class}"
            target_surface = target_surface_for(lane, object_class)
            consumers = sorted(target_consumers[(lane, object_class)])
            direct_ref_count = target_ref_counts[(lane, object_class)]
            existing_ledger = existing_ledger_rows.get(object_id, [])
            existing_manifest = existing_manifest_rows.get(object_id, [])
            pilot_defaults = PILOT_PAIR_DEFAULTS.get(object_id, {})
            if object_class == "empire-instrument":
                symmetry_partner_id = f"{lane}-state-memory"
                current_consumers = consumers or [f"{lane_meta['lane_root'].relative_to(REPO_ROOT).as_posix()}/empire/seed-instruments.md"]
                current_consumer_note = (
                    "no direct CIV-MEM dependency found; seed-instruments is the phase-one destination"
                    if not consumers
                    else "direct CIV-MEM dependency already present"
                )
                volume_side = "empire"
            else:
                symmetry_partner_id = empire_id
                current_consumers = consumers or [target_surface]
                current_consumer_note = (
                    "no direct CIV-MEM dependency found yet; target surface still participates in symmetric first-wave build"
                    if not consumers
                    else "direct CIV-MEM dependency already present"
                )
                volume_side = "civilization"

            first_wave_targets.append(
                {
                    "target_object_id": object_id,
                    "lane": lane_meta["title"],
                    "lane_slug": lane,
                    "volume_side": volume_side,
                    "object_class": object_class,
                    "canonical_question_family": PRIMARY_FAMILY_BY_CLASS[object_class],
                    "secondary_canonical_family": SECONDARY_FAMILY_BY_CLASS[object_class],
                    "upstream_civ_mem_sources": [lane_meta["folder"]],
                    "current_lane_local_consumers": current_consumers,
                    "current_consumer_note": current_consumer_note,
                    "status": get_existing_ledger_value(
                        existing_ledger,
                        10,
                        STATUS_VALUES,
                        pilot_defaults.get("status", "unstarted"),
                    ),
                    "counterweight_present": get_existing_ledger_value(
                        existing_ledger,
                        11,
                        YES_NO_VALUES,
                        pilot_defaults.get("counterweight_present", "no"),
                    ),
                    "transaction_hook_present": get_existing_ledger_value(
                        existing_ledger,
                        12,
                        YES_NO_VALUES,
                        pilot_defaults.get("transaction_hook_present", "no"),
                    ),
                    "symmetry_partner_id": symmetry_partner_id,
                    "target_surface": target_surface,
                    "direct_civ_mem_reference_count": direct_ref_count,
                    "current_word_count": word_metrics["target_word_counts"].get(object_id, 0),
                    "target_word_band": WORD_BANDS[object_class],
                    "symmetry_partner_status": "unstarted",
                    "lane_civilization_words": lane_budget["civilization_words"],
                    "lane_empire_words": lane_budget["empire_words"],
                    "lane_hinge_words": lane_budget["hinge_words"],
                    "lane_civilization_to_empire_ratio": lane_budget["civilization_to_empire_ratio"],
                    "lane_empire_share_of_civilization": lane_budget["empire_share_of_civilization"],
                    "provenance_rule": existing_manifest[4]
                    if len(existing_manifest) > 4
                    else "retain explicit Source basis naming upstream civ-mem files; after cutover use civ-mem only as provenance or gap fallback",
                    "notes": get_existing_note(
                        existing_ledger,
                        pilot_defaults.get(
                            "notes",
                            default_note,
                        ),
                    ),
                }
            )

    target_status_map = {
        target["target_object_id"]: target["status"] for target in first_wave_targets
    }
    for target in first_wave_targets:
        target["symmetry_partner_status"] = target_status_map.get(
            target["symmetry_partner_id"], "unstarted"
        )

    current_total_words = sum(item["words"] for item in word_metrics["lane_totals"].values())
    return {
        "summary": {
            "generated_from": "scripts/build_civ_emp_migration_inventory.py",
            "occurrence_count": len(occurrences),
            "files_with_direct_refs": len(refs_by_file),
            "unique_upstream_refs": len(duplicate_refs),
            "active_lanes": [meta["title"] for meta in LANES.values()],
            "first_wave_target_count": len(first_wave_targets),
            "canonical_question_families": [item["family"] for item in FIRST_WAVE_FAMILIES],
            "current_lane_surface_words": current_total_words,
            "current_civ_emp_words": word_metrics["civ_emp_total_words"],
            "first_wave_core_current_words": word_metrics["first_wave_core_total_words"],
        },
        "direct_ref_occurrences": [o.__dict__ for o in occurrences],
        "by_lane": dict(sorted(by_lane.items())),
        "by_object_class": dict(sorted(by_object_class.items())),
        "by_upstream_folder": dict(sorted(by_upstream_folder.items())),
        "duplicate_upstream_usage": duplicate_entries,
        "first_wave_targets": first_wave_targets,
        "canonical_family_translation": FIRST_WAVE_FAMILIES,
        "word_metrics": word_metrics,
        "corpus_budget": CORPUS_BUDGET,
    }

def write_json(data: dict) -> None:
    path = MIGRATION_ROOT / "dependency-inventory.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def write_dependency_inventory_md(data: dict) -> None:
    lines = [
                "",
        "# CIV-EMP Dependency Inventory",
        "",
        "This report inventories direct legacy `civ-mem` references inside the four active statecraft lanes. It is inventory-only and does not perform semantic migration.",
        "",
        "## Summary",
        "",
        f"- Direct legacy reference occurrences: `{data['summary']['occurrence_count']}`",
        f"- Files with direct references: `{data['summary']['files_with_direct_refs']}`",
        f"- Unique upstream `civ-mem` files referenced: `{data['summary']['unique_upstream_refs']}`",
        f"- First-wave symmetric targets: `{data['summary']['first_wave_target_count']}`",
        f"- Current active-lane words: `{data['summary']['current_lane_surface_words']}`",
        f"- Current `civ-emp` subtree words: `{data['summary']['current_civ_emp_words']}`",
        "",
        "## Direct References By Lane",
        "",
        "| Lane | Direct reference occurrences | Files with direct references |",
        "| --- | ---: | ---: |",
    ]
    lane_file_counts = defaultdict(set)
    for item in data["direct_ref_occurrences"]:
        lane_file_counts[item["lane_title"]].add(item["file_path"])
    for lane, count in data["by_lane"].items():
        lines.append(f"| {lane} | {count} | {len(lane_file_counts[lane])} |")

    lines.extend(
        [
            "",
            "## Direct References By Object Class",
            "",
            "| Object class | Direct reference occurrences |",
            "| --- | ---: |",
        ]
    )
    for object_class, count in data["by_object_class"].items():
        lines.append(f"| `{object_class}` | {count} |")

    lines.extend(
        [
            "",
            "## Direct References By Upstream Civilization Folder",
            "",
            "| Upstream folder | Direct reference occurrences |",
            "| --- | ---: |",
        ]
    )
    for folder, count in data["by_upstream_folder"].items():
        lines.append(f"| `{folder}` | {count} |")

    lines.extend(
        [
            "",
            "## Duplicate Upstream Source Usage",
            "",
            "| Upstream `civ-mem` source | Consumer files | Notes |",
            "| --- | --- | --- |",
        ]
    )
    duplicates = data["duplicate_upstream_usage"]
    if duplicates:
        for item in duplicates[:50]:
            consumers = "<br>".join(item["consumer_files"])
            lines.append(
                f"| `{item['upstream_ref']}` | {consumers} | used by `{item['consumer_count']}` lane-local files |"
            )
    else:
        lines.append("| none | none | no duplicate upstream usage detected |")

    lines.extend(
        [
            "",
            "## Candidate First-Wave Objects Implied By Current Dependency Surface",
            "",
            "| Target object | Volume side | Current lane-local consumers | Direct reference count | Current words | Target band | Current note |",
            "| --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for target in data["first_wave_targets"]:
        consumers = "<br>".join(target["current_lane_local_consumers"])
        lines.append(
            f"| `{target['target_object_id']}` | `{target['volume_side']}` | {consumers} | {target['direct_civ_mem_reference_count']} | {target['current_word_count']} | `{target['target_word_band']}` | {target['current_consumer_note']} |"
        )

    (MIGRATION_ROOT / "dependency-inventory.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

def write_pair_map_md(data: dict) -> None:
    lines = [
                "",
        "# First-Wave Pair Map",
        "",
        "This pair-map locks the first symmetric migration slice: four active lanes times five first-wave objects for a total of twenty targets.",
        "",
        "| Target object | Lane | Volume side | Object class | Symmetry partner | Primary family | Secondary family | Current words | Target band | Target surface |",
        "| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for target in data["first_wave_targets"]:
        lines.append(
            f"| `{target['target_object_id']}` | {target['lane']} | `{target['volume_side']}` | `{target['object_class']}` | `{target['symmetry_partner_id']}` | {target['canonical_question_family']} | {target['secondary_canonical_family']} | {target['current_word_count']} | `{target['target_word_band']}` | `{target['target_surface']}` |"
        )
    (MIGRATION_ROOT / "first-wave-pair-map.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

def write_ledger_md(data: dict) -> None:
    lines = [
                "",
        "# Migration Ledger",
        "",
        "Status vocabulary: `unstarted`, `in_progress`, `materialized`, `cut_over`, `verified`.",
        "",
        "| Target object id | Lane | Volume side | Object class | Primary family | Secondary family | Current words | Target band | Upstream `civ-mem` sources | Current lane-local consumers | Status | Counterweight present | Transaction hook present | Symmetry partner id | Symmetry partner status | Notes |",
        "| --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for target in data["first_wave_targets"]:
        sources = ", ".join(target["upstream_civ_mem_sources"])
        consumers = "<br>".join(target["current_lane_local_consumers"])
        lines.append(
            f"| `{target['target_object_id']}` | {target['lane']} | `{target['volume_side']}` | `{target['object_class']}` | {target['canonical_question_family']} | {target['secondary_canonical_family']} | {target['current_word_count']} | `{target['target_word_band']}` | `{sources}` | {consumers} | `{target['status']}` | `{target['counterweight_present']}` | `{target['transaction_hook_present']}` | `{target['symmetry_partner_id']}` | `{target['symmetry_partner_status']}` | {target['notes']} |"
        )
    (MIGRATION_ROOT / "migration-ledger.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

def write_source_map_manifest_md(data: dict) -> None:
    lines = [
                "",
        "# Source-Map Manifest",
        "",
        "This manifest links each first-wave target to its upstream legacy memory bucket, its current lane-local consumers, and its phase-one migration destination.",
        "",
        "| Target object | Upstream folder | Current consumers | Migration destination | Provenance rule |",
        "| --- | --- | --- | --- | --- |",
    ]
    for target in data["first_wave_targets"]:
        consumers = "<br>".join(target["current_lane_local_consumers"])
        lines.append(
            f"| `{target['target_object_id']}` | `{target['upstream_civ_mem_sources'][0]}` | {consumers} | `{target['target_surface']}` | {target['provenance_rule']} |"
        )
    (MIGRATION_ROOT / "source-map-manifest.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

def write_corpus_budget_json(data: dict) -> None:
    budget_data = {
        "summary": data["summary"],
        "corpus_budget": data["corpus_budget"],
        "word_metrics": data["word_metrics"],
        "phase2_metrics": data["word_metrics"]["phase2_metrics"],
        "first_wave_targets": [
            {
                "target_object_id": target["target_object_id"],
                "lane": target["lane"],
                "volume_side": target["volume_side"],
                "object_class": target["object_class"],
                "current_word_count": target["current_word_count"],
                "target_word_band": target["target_word_band"],
                "canonical_question_family": target["canonical_question_family"],
                "secondary_canonical_family": target["secondary_canonical_family"],
                "status": target["status"],
                "counterweight_present": target["counterweight_present"],
                "transaction_hook_present": target["transaction_hook_present"],
                "symmetry_partner_id": target["symmetry_partner_id"],
                "symmetry_partner_status": target["symmetry_partner_status"],
            }
            for target in data["first_wave_targets"]
        ],
    }
    (MIGRATION_ROOT / "corpus-budget.json").write_text(
        json.dumps(budget_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

def write_corpus_budget_md(data: dict) -> None:
    budget = data["corpus_budget"]
    phase2_metrics = data["word_metrics"]["phase2_metrics"]
    lines = [
                "",
        "# CIV-EMP Corpus Budget",
        "",
        "This note locks the v1 two-volume materialization target and ties it to the live first-wave object grid, lane totals, and current subtree counts. It now also reports Phase 2 helix-first proving-case metrics alongside the historical strand scaffold metrics rather than replacing them.",
        "",
        "## Locked Targets",
        "",
        f"- Full v1 target: `{budget['v1_target']}` words",
        f"- Acceptable v1 band: `{budget['v1_band'][0]}` to `{budget['v1_band'][1]}`",
        f"- Hard ceiling: `{budget['hard_ceiling']}`",
        f"- Phase 2 active proving cases: `{', '.join(budget['phase2_active_proving_cases'])}`",
        f"- Volume I: Civilization target `{budget['volume_targets']['civilization']['target']}`, band `{budget['volume_targets']['civilization']['band'][0]}` to `{budget['volume_targets']['civilization']['band'][1]}`",
        f"- Volume II: Empire target `{budget['volume_targets']['empire']['target']}`, band `{budget['volume_targets']['empire']['band'][0]}` to `{budget['volume_targets']['empire']['band'][1]}`",
        f"- First-wave core minimum: `{budget['first_wave_core_minimum'][0]}` to `{budget['first_wave_core_minimum'][1]}`",
        f"- First-wave practical target: `{budget['first_wave_practical_target'][0]}` to `{budget['first_wave_practical_target'][1]}`",
        "",
        "## Current Baseline",
        "",
        f"- Current active-lane words across America, Russia, China, and Iran: `{data['summary']['current_lane_surface_words']}`",
        f"- Current `civ-emp` subtree words: `{data['summary']['current_civ_emp_words']}`",
        f"- Current first-wave core words on the 20 target surfaces: `{data['summary']['first_wave_core_current_words']}`",
        "",
        "| Surface | Current words | File count |",
        "| --- | ---: | ---: |",
    ]
    for lane, item in data["word_metrics"]["lane_totals"].items():
        lines.append(f"| {lane} lane | {item['words']} | {item['file_count']} |")
    lines.append(
        f"| `civ-emp` subtree | {data['word_metrics']['civ_emp_total_words']} | {data['word_metrics']['civ_emp_file_count']} |"
    )

    lines.extend(
        [
            "",
            "## First-Wave Object Targets",
            "",
            "| Target object | Current words | Target band | Status | Counterweight | Transaction hook | Symmetry partner status |",
            "| --- | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for target in data["first_wave_targets"]:
        lines.append(
            f"| `{target['target_object_id']}` | {target['current_word_count']} | `{target['target_word_band']}` | `{target['status']}` | `{target['counterweight_present']}` | `{target['transaction_hook_present']}` | `{target['symmetry_partner_status']}` |"
        )

    lines.extend(
        [
            "",
            "## Pilot Pair Symmetry Budget",
            "",
            "These rows measure the proving-case pair only: `state-memory` versus `empire-instrument`. This is the scope where the `60%` empire-share floor and `2.0:1` ceiling apply.",
            "",
            "| Lane | Pilot civilization words | Pilot empire words | Pilot ratio | Pilot empire share |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for lane, item in data["word_metrics"]["first_wave_lane_totals"].items():
        ratio = item["pilot_civilization_to_empire_ratio"]
        share = item["pilot_empire_share_of_civilization"]
        ratio_text = f"{ratio:.2f}" if ratio is not None else "n/a"
        share_text = f"{share:.2f}" if share is not None else "n/a"
        lines.append(
            f"| {lane} | {item['pilot_civilization_words']} | {item['pilot_empire_words']} | {ratio_text} | {share_text} |"
        )

    lines.extend(
        [
            "",
            "## First-Wave Grid Balance",
            "",
            "These rows measure the broader first-wave civilization grid against the single phase-one empire object. They are useful for maturity tracking, but they are not governed by the pilot-pair `60%` / `2.0:1` template rule because the grid intentionally contains four civilization classes and one empire class.",
            "",
            "| Lane | Civilization words | Empire words | Hinge words | Civilization:Empire ratio | Empire share of civilization |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for lane, item in data["word_metrics"]["first_wave_lane_totals"].items():
        ratio = item["civilization_to_empire_ratio"]
        share = item["empire_share_of_civilization"]
        ratio_text = f"{ratio:.2f}" if ratio is not None else "n/a"
        share_text = f"{share:.2f}" if share is not None else "n/a"
        lines.append(
            f"| {lane} | {item['civilization_words']} | {item['empire_words']} | {item['hinge_words']} | {ratio_text} | {share_text} |"
        )

    lines.extend(
        [
            "",
            "## Phase 2 Helix-First Metrics",
            "",
            "These rows are additive. They describe the active helix-first proving cases and the underlying strand totals without discarding the historical two-volume scaffold metrics above. America, Russia, China, and Iran are now the current proving cases in this phase.",
            "",
            "### Helix Objects",
            "",
            "| Lane | Helix words | Path |",
            "| --- | ---: | --- |",
        ]
    )
    for lane, item in phase2_metrics["helix_objects"]["by_lane"].items():
        lines.append(f"| {lane} | {item['words']} | `{item['path']}` |")

    lines.extend(
        [
            "",
            f"- Total helix-object words across active lanes: `{phase2_metrics['helix_objects']['total_words']}`",
            "",
            "### Strand Subtotals By Lane",
            "",
            "| Lane | First-wave strand words | Strand object count |",
            "| --- | ---: | ---: |",
        ]
    )
    for lane, item in phase2_metrics["strand_subtotals_by_lane"].items():
        lines.append(f"| {lane} | {item['words']} | {item['object_count']} |")

    lines.extend(
        [
            "",
            "### Future Phase 2 Surface Classes",
            "",
            "| Surface class | Current surfaces | Current words | Notes |",
            "| --- | ---: | ---: | --- |",
            f"| Canonical-family synthesis | {phase2_metrics['canonical_family_synthesis_surfaces']['surface_count']} | {phase2_metrics['canonical_family_synthesis_surfaces']['current_words']} | {'active first synthesis surfaces now exist in the control plane' if phase2_metrics['canonical_family_synthesis_surfaces']['surface_count'] else 'not yet instantiated in the control plane'} |",
            f"| Orientation / retrieval | {phase2_metrics['orientation_and_retrieval_surfaces']['surface_count']} | {phase2_metrics['orientation_and_retrieval_surfaces']['current_words']} | {'active orientation or retrieval surfaces now exist in the control plane' if phase2_metrics['orientation_and_retrieval_surfaces']['surface_count'] else 'not yet instantiated as distinct Phase 2 surfaces'} |",
            "",
            "## Canonical Family Coverage",
            "",
            "Counts below are family-served first-wave words. A target contributes to a family when that family is named as either its primary or secondary linkage, so these rows measure answer-capacity rather than partitioned word totals.",
            "",
            "| Canonical family | Current mapped first-wave words |",
            "| --- | ---: |",
        ]
    )
    for family in data["summary"]["canonical_question_families"]:
        lines.append(
            f"| {family} | {data['word_metrics']['canonical_family_word_counts'].get(family, 0)} |"
        )

    lines.extend(
        [
            "",
            "## V1 Remainder Allocation",
            "",
            f"- Cross-lane canonical family synthesis: `{budget['v1_remainder']['cross_lane_canonical_family_synthesis'][0]}` to `{budget['v1_remainder']['cross_lane_canonical_family_synthesis'][1]}`",
            f"- Volume-level orientation and retrieval surfaces: `{budget['v1_remainder']['volume_level_orientation_and_retrieval'][0]}` to `{budget['v1_remainder']['volume_level_orientation_and_retrieval'][1]}`",
            f"- Second-wave depth reserve: `{budget['v1_remainder']['second_wave_depth_reserve'][0]}` to `{budget['v1_remainder']['second_wave_depth_reserve'][1]}`",
            "",
            "## Budget Rules",
            "",
            f"- The pilot pair (`state-memory` / `empire-instrument`) must hold at least `{int(budget['symmetry_rule']['minimum_empire_share_of_civilization'] * 100)}`%` empire share and remain below a `{budget['symmetry_rule']['maximum_civilization_to_empire_ratio']}:1` ratio once a lane is mature enough to cut over.",
            "- The broader first-wave grid uses those pilot-pair metrics as a template-readiness test, not as a class-completion requirement.",
            f"- No single lane should consume more than `{int(budget['symmetry_rule']['max_single_lane_share_of_v1_total'] * 100)}`%` of the v1 total unless a later corpus audit justifies it.",
        ]
    )
    (MIGRATION_ROOT / "corpus-budget.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

def main() -> None:
    MIGRATION_ROOT.mkdir(parents=True, exist_ok=True)
    occurrences = collect_occurrences()
    word_metrics = compute_word_metrics()
    data = compute_inventory(occurrences, word_metrics)
    write_json(data)
    write_dependency_inventory_md(data)
    write_pair_map_md(data)
    write_ledger_md(data)
    write_source_map_manifest_md(data)
    write_corpus_budget_json(data)
    write_corpus_budget_md(data)

if __name__ == "__main__":
    main()
