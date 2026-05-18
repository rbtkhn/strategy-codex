#!/usr/bin/env python3
"""Score speaker-memory benchmark runs and emit recursive repair telemetry."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
WORK_BOUNDARY = "WORK only; not Record."
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")
OBJECT_SHAPE_RE = re.compile(r"(?im)^\s*object_shape\s*:\s*([a-z0-9-]+)\s*$")

CORE_FAILURES = {
    "missing_work_boundary",
    "missing_object_shape",
    "weak_open_first",
    "wrong_arc_rank",
    "missing_paired_read",
    "generic_guest_profile",
    "lattice_overload",
    "premature_helix",
}

REPAIR_ROUTING = {
    "missing_work_boundary": ("source_note", "Add the required WORK-only boundary line."),
    "missing_object_shape": ("source_note", "Add an explicit object_shape declaration."),
    "weak_open_first": ("source_note", "Add concrete Open first links and routing reasons."),
    "missing_routing_use": ("source_note", "Add a Routing use section with actionable routes."),
    "missing_boundaries": ("source_note", "Add boundaries that state what not to overclaim."),
    "wrong_arc_rank": ("fixture", "Tighten expected rank order or repair the arc ranking."),
    "missing_paired_read": ("source_note", "Add a paired-read recommendation and reason."),
    "generic_guest_profile": ("template", "Strengthen host-conditioned arc language."),
    "lattice_overload": ("template", "Reinforce lattice-as-pointer doctrine."),
    "unsupported_claim_risk": ("prompt", "Tighten source-pack restraint and unsupported-claim penalties."),
    "premature_helix": ("source_note", "Remove or qualify premature helix claims."),
}

DEFAULT_TARGETS = {
    "sm-1-speaker-object-repair": "codex/speakers/sachs/sachs-speaker-object.md",
    "sm-2-speaker-arc-ranking": "codex/years/2026/diesen/diesen-freeman-speaker-arc.md",
}

TARGET_BY_TYPE = {
    "template": "codex/speakers/_templates/speaker-arc-template.md",
    "fixture": "artifacts/benchmarks/speaker-memory/fixtures",
    "rubric": "artifacts/benchmarks/speaker-memory/fixtures",
    "prompt": "artifacts/benchmarks/speaker-memory/fixtures",
}


@dataclass(frozen=True)
class Check:
    name: str
    score: int
    max_score: int
    passed: bool
    message: str


@dataclass(frozen=True)
class RepairAction:
    benchmark_id: str
    failure_code: str
    target_type: str
    target: str
    recommended_action: str
    severity: str


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.strip().lower()).strip("_")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def section_text(text: str, heading: str) -> str:
    target = heading.casefold()
    for match in HEADING_RE.finditer(text):
        if match.group(1).strip().casefold() != target:
            continue
        start = match.end()
        next_match = HEADING_RE.search(text, start)
        end = next_match.start() if next_match else len(text)
        return text[start:end]
    return ""


def has_section(text: str, *headings: str) -> bool:
    return any(section_text(text, heading).strip() for heading in headings)


def link_count(text: str) -> int:
    return len(LINK_RE.findall(text))


def contains_any(text: str, needles: list[str]) -> bool:
    low = text.casefold()
    return any(needle.casefold() in low for needle in needles)


def phrase_is_negated(text: str, phrase: str) -> bool:
    low = text.casefold()
    target = phrase.casefold()
    start = low.find(target)
    if start < 0:
        return False
    window = low[max(0, start - 80) : start]
    return any(marker in window for marker in ("not", "not a", "not as a", "not a provenance ledger"))


def first_index(text: str, needles: list[str]) -> int | None:
    low = text.casefold()
    hits = [low.find(needle.casefold()) for needle in needles]
    hits = [hit for hit in hits if hit >= 0]
    return min(hits) if hits else None


def add_check(
    checks: list[Check],
    failures: list[str],
    *,
    name: str,
    score: int,
    max_score: int,
    passed: bool,
    message: str,
    failure_code: str | None = None,
) -> None:
    checks.append(Check(name, score, max_score, passed, message))
    if not passed and failure_code:
        failures.append(failure_code)


def score_work_boundary(text: str, checks: list[Check], failures: list[str]) -> None:
    passed = WORK_BOUNDARY in text
    add_check(
        checks,
        failures,
        name="work_boundary",
        score=10 if passed else 0,
        max_score=10,
        passed=passed,
        message="Required WORK-only boundary is present." if passed else "Missing WORK-only boundary.",
        failure_code="missing_work_boundary",
    )


def score_sm1(text: str) -> tuple[list[Check], list[str]]:
    checks: list[Check] = []
    failures: list[str] = []
    score_work_boundary(text, checks, failures)

    required = {
        "object_shape_section": ("Object shape",),
        "open_first_section": ("Open first",),
        "routing_use_section": ("Routing use",),
        "boundaries_section": ("Boundaries", "Boundary"),
    }
    section_hits = 0
    missing_sections: list[str] = []
    for name, headings in required.items():
        if has_section(text, *headings):
            section_hits += 1
        else:
            missing_sections.append(name)
    add_check(
        checks,
        failures,
        name="required_sections",
        score=section_hits * 5,
        max_score=20,
        passed=section_hits == len(required),
        message=(
            "All required speaker-object sections are present."
            if section_hits == len(required)
            else f"Missing sections: {', '.join(missing_sections)}."
        ),
        failure_code="missing_boundaries" if "boundaries_section" in missing_sections else None,
    )

    shape_match = OBJECT_SHAPE_RE.search(text)
    shape = shape_match.group(1) if shape_match else ""
    shape_ok = shape == "cross-host-reinforced"
    add_check(
        checks,
        failures,
        name="explicit_object_shape",
        score=15 if shape_ok else 0,
        max_score=15,
        passed=shape_ok,
        message=(
            "`object_shape: cross-host-reinforced` is explicit."
            if shape_ok
            else "Missing or incorrect explicit object_shape."
        ),
        failure_code="missing_object_shape",
    )

    open_first = section_text(text, "Open first")
    links = link_count(open_first)
    open_score = 15 if links >= 2 else 10 if links == 1 else 0
    add_check(
        checks,
        failures,
        name="open_first_links",
        score=open_score,
        max_score=15,
        passed=open_score >= 10,
        message=f"Open first contains {links} markdown link(s).",
        failure_code="weak_open_first",
    )

    routing = section_text(text, "Routing use")
    routing_ok = bool(routing.strip()) and contains_any(
        routing, ["routing", "route", "strengthens", "deciding", "speaker"]
    )
    add_check(
        checks,
        failures,
        name="routing_use_actionability",
        score=10 if routing_ok else 0,
        max_score=10,
        passed=routing_ok,
        message="Routing use is actionable." if routing_ok else "Routing use is missing or generic.",
        failure_code="missing_routing_use",
    )

    boundaries = section_text(text, "Boundaries") or section_text(text, "Boundary")
    boundary_terms = [
        "raw-input",
        "provenance",
        "biography",
        "wire-grade",
        "verifier",
        "helix",
        "overclaim",
        "do not",
    ]
    boundary_hits = sum(1 for term in boundary_terms if term.casefold() in boundaries.casefold())
    boundary_score = min(15, boundary_hits * 3)
    add_check(
        checks,
        failures,
        name="boundary_coverage",
        score=boundary_score,
        max_score=15,
        passed=boundary_score >= 9,
        message=f"Boundary section covers {boundary_hits} expected warning term(s).",
        failure_code="missing_boundaries",
    )

    source_risk_terms = ["born", "professor at", "served as", "according to wikipedia"]
    source_ok = not contains_any(text, source_risk_terms)
    add_check(
        checks,
        failures,
        name="source_pack_restraint",
        score=10 if source_ok else 0,
        max_score=10,
        passed=source_ok,
        message="No obvious unsupported biography markers found." if source_ok else "Unsupported biography risk found.",
        failure_code="unsupported_claim_risk",
    )

    premature_helix = contains_any(
        text,
        ["triple-helix", "double-helix", "mature helix", "canonical helix"],
    ) and not contains_any(text, ["not", "without", "until", "premature"])
    add_check(
        checks,
        failures,
        name="premature_helix_restraint",
        score=15 if not premature_helix else 0,
        max_score=15,
        passed=not premature_helix,
        message="Helix claims are restrained." if not premature_helix else "Premature helix claim risk found.",
        failure_code="premature_helix",
    )
    return checks, failures


def score_sm2(text: str) -> tuple[list[Check], list[str]]:
    checks: list[Check] = []
    failures: list[str] = []
    score_work_boundary(text, checks, failures)

    required = {
        "why_this_guest_run_matters": ("Why this guest run matters",),
        "arc_set": ("Arc set",),
        "open_first": ("Open first",),
        "best_paired_read": ("Best paired read",),
        "routing_use": ("Routing use",),
        "boundary": ("Boundary", "Boundaries"),
    }
    hits = 0
    missing: list[str] = []
    for name, headings in required.items():
        if has_section(text, *headings):
            hits += 1
        else:
            missing.append(name)
    add_check(
        checks,
        failures,
        name="required_sections",
        score=hits * 3,
        max_score=18,
        passed=hits == len(required),
        message="All required speaker-arc sections are present." if hits == len(required) else f"Missing sections: {', '.join(missing)}.",
        failure_code="missing_boundaries" if "boundary" in missing else None,
    )

    idx_0506 = first_index(text, ["2026-05-06", "maritime-dominance-strait-of-hormuz"])
    idx_0418 = first_index(text, ["2026-04-18", "freeman-diesen-2026-04-18"])
    rank_ok = idx_0506 is not None and idx_0418 is not None and idx_0506 < idx_0418
    add_check(
        checks,
        failures,
        name="expected_rank_order",
        score=18 if rank_ok else 0,
        max_score=18,
        passed=rank_ok,
        message="Expected 2026-05-06 before 2026-04-18 ranking is present." if rank_ok else "Expected rank order is missing or reversed.",
        failure_code="wrong_arc_rank",
    )

    paired = section_text(text, "Best paired read")
    paired_ok = contains_any(paired, ["diesen-matlock-speaker-arc.md", "Matlock"]) and contains_any(
        paired, ["diesen-jiang-speaker-arc.md", "Jiang"]
    )
    add_check(
        checks,
        failures,
        name="paired_read_coverage",
        score=14 if paired_ok else 7 if paired.strip() else 0,
        max_score=14,
        passed=paired_ok,
        message="Matlock and Jiang paired-read logic is present." if paired_ok else "Paired-read coverage is incomplete.",
        failure_code="missing_paired_read",
    )

    host_terms = ["diesen brings out", "host-local", "host frame", "inside the diesen stream", "conversational form"]
    host_ok = contains_any(text, host_terms)
    generic_terms = ["generic freeman profile", "generic guest profile"]
    generic_guest = any(
        term.casefold() in text.casefold() and not phrase_is_negated(text, term)
        for term in generic_terms
    )
    add_check(
        checks,
        failures,
        name="host_form_awareness",
        score=14 if host_ok and not generic_guest else 0,
        max_score=14,
        passed=host_ok and not generic_guest,
        message="Host-conditioned form is explicit." if host_ok and not generic_guest else "Arc reads as a generic guest profile.",
        failure_code="generic_guest_profile",
    )

    lattice_mentions = re.findall(r"lattice", text, flags=re.IGNORECASE)
    lattice_ok = not lattice_mentions or contains_any(
        text,
        ["lattice rows can cite", "lattice as a secondary", "lattice rows are lookup", "not the place"],
    )
    add_check(
        checks,
        failures,
        name="lattice_restraint",
        score=12 if lattice_ok else 0,
        max_score=12,
        passed=lattice_ok,
        message="Lattice is treated as a pointer surface." if lattice_ok else "Lattice appears overloaded as interpretation surface.",
        failure_code="lattice_overload",
    )

    boundary = section_text(text, "Boundary") or section_text(text, "Boundaries")
    boundary_terms = ["wire", "fleet", "cargo", "blockade", "orbat", "proxy", "generic"]
    boundary_hits = sum(1 for term in boundary_terms if term.casefold() in boundary.casefold())
    add_check(
        checks,
        failures,
        name="boundary_coverage",
        score=min(12, boundary_hits * 2),
        max_score=12,
        passed=boundary_hits >= 4,
        message=f"Boundary section covers {boundary_hits} expected warning term(s).",
        failure_code="missing_boundaries",
    )

    source_risk_terms = ["born", "wikipedia", "foreign minister", "ambassador to"]
    source_ok = not contains_any(text, source_risk_terms)
    add_check(
        checks,
        failures,
        name="source_pack_restraint",
        score=12 if source_ok else 0,
        max_score=12,
        passed=source_ok,
        message="No obvious unsupported biography markers found." if source_ok else "Unsupported biography risk found.",
        failure_code="unsupported_claim_risk",
    )
    return checks, failures


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def closeout_for(total: int, max_score: int, failures: list[str], open_error: bool = False) -> str:
    if open_error or max_score <= 0:
        return "Open"
    percentage = total / max_score * 100
    if percentage < 70 or any(failure in CORE_FAILURES for failure in failures):
        return "Broke"
    if percentage >= 85:
        return "Held"
    return "Weakened"


def repair_actions_for(benchmark_id: str, failures: list[str]) -> list[RepairAction]:
    actions: list[RepairAction] = []
    for failure in failures:
        target_type, recommendation = REPAIR_ROUTING.get(
            failure, ("rubric", "Review scorer rule and benchmark fixture.")
        )
        target = (
            DEFAULT_TARGETS.get(benchmark_id, "artifacts/benchmarks/speaker-memory")
            if target_type == "source_note"
            else TARGET_BY_TYPE.get(target_type, "artifacts/benchmarks/speaker-memory")
        )
        severity = "high" if failure in CORE_FAILURES else "medium"
        actions.append(
            RepairAction(
                benchmark_id=benchmark_id,
                failure_code=failure,
                target_type=target_type,
                target=target,
                recommended_action=recommendation,
                severity=severity,
            )
        )
    return actions


def build_score(run_path: Path) -> dict[str, Any]:
    metadata_path = run_path / "metadata.json"
    output_path = run_path / "output.md"
    if not metadata_path.exists() or not output_path.exists():
        missing = [
            str(path.name)
            for path in (metadata_path, output_path)
            if not path.exists()
        ]
        checks = [
            Check(
                "required_files",
                0,
                1,
                False,
                f"Missing required file(s): {', '.join(missing)}.",
            )
        ]
        return {
            "benchmark_id": "unknown",
            "run_path": str(run_path),
            "total_score": 0,
            "max_score": 1,
            "percentage": 0.0,
            "closeout": "Open",
            "checks": [asdict(check) for check in checks],
            "failure_codes": [],
            "repair_actions": [],
        }

    metadata = load_json(metadata_path)
    benchmark_id = metadata.get("benchmark_id", "")
    text = output_path.read_text(encoding="utf-8")
    if benchmark_id == "sm-1-speaker-object-repair":
        checks, failures = score_sm1(text)
    elif benchmark_id == "sm-2-speaker-arc-ranking":
        checks, failures = score_sm2(text)
    else:
        checks = [Check("supported_benchmark", 0, 1, False, f"Unsupported benchmark_id: {benchmark_id}")]
        failures = []

    failures = unique(failures)
    total = sum(check.score for check in checks)
    max_score = sum(check.max_score for check in checks) or 1
    closeout = closeout_for(total, max_score, failures, open_error=benchmark_id not in {
        "sm-1-speaker-object-repair",
        "sm-2-speaker-arc-ranking",
    })
    actions = repair_actions_for(benchmark_id, failures)
    return {
        "benchmark_id": benchmark_id or "unknown",
        "run_path": str(run_path),
        "total_score": total,
        "max_score": max_score,
        "percentage": round(total / max_score * 100, 1),
        "closeout": closeout,
        "checks": [asdict(check) for check in checks],
        "failure_codes": failures,
        "repair_actions": [asdict(action) for action in actions],
    }


def render_score_md(score: dict[str, Any]) -> str:
    lines = [
        f"# Speaker Memory Score - {score['benchmark_id']}",
        "",
        f"**Closeout:** `{score['closeout']}`",
        f"**Score:** `{score['total_score']}/{score['max_score']}` ({score['percentage']}%)",
        "",
        "## Checks",
        "",
        "| Check | Score | Pass | Note |",
        "|---|---:|---|---|",
    ]
    for check in score["checks"]:
        passed = "yes" if check["passed"] else "no"
        lines.append(
            f"| `{check['name']}` | {check['score']}/{check['max_score']} | {passed} | {check['message']} |"
        )
    lines += ["", "## Failure Codes", ""]
    if score["failure_codes"]:
        lines.extend(f"- `{failure}`" for failure in score["failure_codes"])
    else:
        lines.append("- none")
    lines += ["", "## Repair Actions", ""]
    if score["repair_actions"]:
        for action in score["repair_actions"]:
            lines.append(
                f"- `{action['failure_code']}` -> `{action['target_type']}` `{action['target']}`: {action['recommended_action']}"
            )
    else:
        lines.append("- none")
    lines += [
        "",
        "## Recursive Use",
        "",
        "Use this score as repair telemetry. Fix one high-severity repair target, rerun the scorer, and compare `percentage`, `closeout`, and `failure_codes` before treating the loop as improved.",
        "",
    ]
    return "\n".join(lines)


def write_outputs(run_path: Path, score: dict[str, Any]) -> None:
    (run_path / "score.json").write_text(
        json.dumps(score, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (run_path / "score.md").write_text(render_score_md(score), encoding="utf-8")
    queue_path = run_path / "repair-queue.jsonl"
    queue_path.write_text(
        "".join(json.dumps(action, ensure_ascii=False) + "\n" for action in score["repair_actions"]),
        encoding="utf-8",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True, help="Benchmark run folder containing metadata.json and output.md.")
    parser.add_argument("--json", action="store_true", help="Print score JSON to stdout.")
    parser.add_argument("--no-write", action="store_true", help="Compute score without writing score artifacts.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_path = args.run.resolve()
    score = build_score(run_path)
    if not args.no_write:
        write_outputs(run_path, score)
    if args.json:
        print(json.dumps(score, indent=2, ensure_ascii=False))
    else:
        print(f"{score['benchmark_id']}: {score['closeout']} ({score['percentage']}%)")
    return 0 if score["closeout"] != "Open" else 1


if __name__ == "__main__":
    raise SystemExit(main())
