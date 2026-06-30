#!/usr/bin/env python3
"""Build longitudinal views over Innermost Loop raw captures.

Reads full local captures from the singularity-academy workshop and writes:
  - workshop/longitudinal/innermost-loop.md
  - workshop/longitudinal/innermost-loop-signals.json
This is deterministic rule extraction, not LLM synthesis.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timedelta
import json
from pathlib import Path
import re
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORKSHOP = REPO_ROOT / "singularity/workshop"
DEFAULT_RAW_ROOT = DEFAULT_WORKSHOP / "raw-input/innermost-loop"
DEFAULT_OUT_DIR = DEFAULT_WORKSHOP / "longitudinal"
DEFAULT_README = DEFAULT_WORKSHOP / "README.md"

BOILERPLATE_PATTERNS = [
    r"thanks for reading the innermost loop! subscribe for free to receive new posts and support my work\.",
    r"_backfilled by `scripts/backfill_innermost_loop_academy_raw\.py`; local work copy, not record\._",
]

FRONTS = [
    {
        "slug": "frontier-models-and-benchmarks",
        "label": "Frontier models and benchmarks",
        "terms": [
            "frontier model",
            "model",
            "models",
            "benchmark",
            "eval",
            "metr",
            "claude",
            "openai",
            "gpt",
            "gemini",
            "anthropic",
            "reasoning",
            "sota",
            "superexponential",
        ],
    },
    {
        "slug": "agents-and-autonomy",
        "label": "Agents and autonomy",
        "terms": [
            "agent",
            "agentic",
            "autonomy",
            "autonomous",
            "workflow",
            "tool use",
            "assistant",
            "codex",
            "scaffolding",
            "self-improv",
        ],
    },
    {
        "slug": "compute-chips-and-energy",
        "label": "Compute, chips, and energy",
        "terms": [
            "compute",
            "chip",
            "gpu",
            "silicon",
            "datacenter",
            "data center",
            "nvidia",
            "amd",
            "intel",
            "micron",
            "tsmc",
            "ssd",
            "energy",
            "power",
            "grid",
        ],
    },
    {
        "slug": "cyber-capability",
        "label": "Cyber capability",
        "terms": [
            "cyber",
            "vulnerability",
            "exploit",
            "malware",
            "ctf",
            "penetration",
            "pen testing",
            "security",
            "defense",
        ],
    },
    {
        "slug": "robotics-and-embodiment",
        "label": "Robotics and embodiment",
        "terms": [
            "roarchive/grace-mar-instance/bot",
            "robotics",
            "humanoid",
            "autonomous vehicle",
            "vehicle",
            "drone",
            "tesla",
            "figure",
            "embodied",
            "physical",
        ],
    },
    {
        "slug": "biotech-and-medicine",
        "label": "Biotech and medicine",
        "terms": [
            "bio",
            "biology",
            "biotech",
            "medicine",
            "medical",
            "doctor",
            "drug",
            "therapy",
            "cell",
            "genetic",
            "protein",
            "isomorphic",
        ],
    },
    {
        "slug": "memory-world-models-and-synthetic-reality",
        "label": "Memory, world models, and synthetic reality",
        "terms": [
            "memory",
            "world model",
            "simulation",
            "synthetic",
            "hallucination",
            "video",
            "audio",
            "voice",
            "context",
            "provenance",
            "forecast",
        ],
    },
    {
        "slug": "markets-labor-and-productization",
        "label": "Markets, labor, and productization",
        "terms": [
            "market",
            "labor",
            "job",
            "workforce",
            "product",
            "revenue",
            "valuation",
            "startup",
            "enterprise",
            "business",
            "customer",
            "pricing",
            "commerce",
        ],
    },
    {
        "slug": "institutions-statecraft-and-regulation",
        "label": "Institutions, statecraft, and regulation",
        "terms": [
            "white house",
            "government",
            "state",
            "regulation",
            "executive order",
            "law",
            "lawsuit",
            "policy",
            "national",
            "china",
            "defense",
            "military",
            "university",
            "institution",
        ],
    },
    {
        "slug": "trust-provenance-and-human-meaning",
        "label": "Trust, provenance, and human meaning",
        "terms": [
            "trust",
            "provenance",
            "truth",
            "fake",
            "deception",
            "impersonating",
            "dignity",
            "meaning",
            "religion",
            "monk",
            "buddhist",
            "human",
            "attention",
        ],
    },
]

@dataclass(frozen=True)
class RawCapture:
    day: date
    title: str
    source_url: str
    path: Path
    body: str

def _relative(path: Path, root: Path = REPO_ROOT) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")

def _parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out

def _extract_newsletter_text(text: str) -> str:
    marker = "## Newsletter Text"
    if marker not in text:
        return text
    body = text.split(marker, 1)[1]
    body = re.split(r"\n_Backfilled by ", body, maxsplit=1)[0]
    return _strip_boilerplate(body)

def _strip_boilerplate(text: str) -> str:
    cleaned = text
    for pattern in BOILERPLATE_PATTERNS:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.I)
    lines = []
    for line in cleaned.splitlines():
        stripped = line.strip()
        if stripped in {"", "-", "- -"}:
            lines.append("")
            continue
        lines.append(stripped)
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"[ \t\r\f\v]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()

def _load_capture(path: Path) -> RawCapture:
    text = path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(text)
    day_text = fm.get("title_date") or re.search(r"(\d{4}-\d{2}-\d{2})", path.name).group(1)
    day = datetime.strptime(day_text, "%Y-%m-%d").date()
    title = ""
    for line in text.splitlines():
        if line.startswith("- Title: "):
            title = line.removeprefix("- Title: ").strip()
            break
    if not title:
        title = f"The Innermost Loop - {day.isoformat()}"
    return RawCapture(
        day=day,
        title=title,
        source_url=fm.get("source_url", ""),
        path=path,
        body=_extract_newsletter_text(text),
    )

def _term_count(text: str, term: str) -> int:
    escaped = re.escape(term.lower()).replace(r"\ ", r"[\s\-]+")
    pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
    return len(re.findall(pattern, text.lower()))

def _confidence(score: int) -> str:
    if score >= 4:
        return "high"
    if score >= 2:
        return "medium"
    if score == 1:
        return "low"
    return "none"

def _front_note(label: str, confidence: str) -> str:
    if confidence == "high":
        return f"Strong deterministic signal for {label.lower()} in this issue."
    if confidence == "medium":
        return f"Moderate deterministic signal for {label.lower()}; review before synthesis."
    return f"Weak deterministic signal for {label.lower()}; needs review."

def classify_capture(capture: RawCapture) -> list[dict[str, object]]:
    detected = []
    for front in FRONTS:
        matches: dict[str, int] = {}
        for term in front["terms"]:
            count = _term_count(capture.body, term)
            if count:
                matches[term] = count
        score = sum(matches.values())
        if not score:
            continue
        confidence = _confidence(score)
        detected.append(
            {
                "slug": front["slug"],
                "label": front["label"],
                "score": score,
                "confidence": confidence,
                "matched_terms": matches,
                "needs_review": confidence == "low",
                "note": _front_note(str(front["label"]), confidence),
            }
        )
    return sorted(detected, key=lambda x: (-int(x["score"]), str(x["label"])))

def _date_range_gaps(days: list[date]) -> list[date]:
    if not days:
        return []
    present = set(days)
    out = []
    cur = min(days)
    end = max(days)
    while cur <= end:
        if cur not in present:
            out.append(cur)
        cur += timedelta(days=1)
    return out

def build_index(raw_root: Path) -> dict[str, object]:
    captures = [_load_capture(path) for path in sorted(raw_root.glob("innermost-loop-*.md"))]
    items = []
    front_timelines: dict[str, list[str]] = {str(front["slug"]): [] for front in FRONTS}
    for capture in captures:
        fronts = classify_capture(capture)
        for front in fronts:
            if not bool(front["needs_review"]):
                front_timelines[str(front["slug"])].append(capture.day.isoformat())
        confidence = "none"
        if fronts:
            confidence = str(fronts[0]["confidence"])
        items.append(
            {
                "date": capture.day.isoformat(),
                "title": capture.title,
                "source_url": capture.source_url,
                "raw_path": _relative(capture.path),
                "confidence_tier": confidence,
                "needs_review": (not fronts) or any(bool(front["needs_review"]) for front in fronts),
                "detected_fronts": fronts,
            }
        )
    days = [capture.day for capture in captures]
    return {
        "schema_version": 1,
        "source": "the-innermost-loop",
        "generated_by": "scripts/build_innermost_loop_longitudinal.py",
        "raw_root": _relative(raw_root),
        "fronts": [
            {"slug": front["slug"], "label": front["label"], "terms": front["terms"]}
            for front in FRONTS
        ],
        "coverage": {
            "first_date": min(days).isoformat() if days else None,
            "last_date": max(days).isoformat() if days else None,
            "issue_count": len(days),
            "gaps": [day.isoformat() for day in _date_range_gaps(days)],
        },
        "items": items,
        "front_timelines": front_timelines,
    }

def _md_link_from_out(raw_path: str) -> str:
    filename = Path(raw_path).name
    return f"../../../source-archive/singularity/innermost-loop/{filename}"

def _format_fronts(fronts: list[dict[str, object]], limit: int = 4) -> str:
    if not fronts:
        return "_none_"
    labels = [str(front["label"]) for front in fronts[:limit]]
    if len(fronts) > limit:
        labels.append(f"+{len(fronts) - limit} more")
    return "; ".join(labels)

def _stable_fronts(fronts: list[dict[str, object]]) -> list[dict[str, object]]:
    return [front for front in fronts if not bool(front["needs_review"])]

def render_markdown(index: dict[str, object]) -> str:
    coverage = dict(index["coverage"])  # type: ignore[arg-type]
    items = list(index["items"])  # type: ignore[arg-type]
    gaps = list(coverage.get("gaps") or [])
    lines = [
        "# The Innermost Loop Longitudinal Spine",
        "",
                "",
        "Deterministic v1 view over local raw captures. Fronts are keyword/rule signals for review, not settled interpretation.",
        "",
        "## Coverage",
        "",
        f"- First issue: {coverage.get('first_date') or 'none'}",
        f"- Last issue: {coverage.get('last_date') or 'none'}",
        f"- Captured issues: {coverage.get('issue_count')}",
        f"- Gaps: {', '.join(gaps) if gaps else 'none'}",
        "",
        "## Date-by-Date",
        "",
        "| Date | Fronts | Review | Raw |",
        "| --- | --- | --- | --- |",
    ]
    for item in items:
        fronts = list(item["detected_fronts"])  # type: ignore[index]
        stable = _stable_fronts(fronts)
        review = "needs review" if item.get("needs_review") else "ok"
        raw_link = _md_link_from_out(str(item["raw_path"]))
        front_text = _format_fronts(stable)
        weak_count = len(fronts) - len(stable)
        if weak_count and stable:
            front_text = f"{front_text}; +{weak_count} weak review"
        lines.append(
            f"| {item['date']} | {front_text} | {review} | [raw]({raw_link}) |"
        )

    lines.extend(["", "## Front Timelines", ""])
    front_lookup = {front["slug"]: front["label"] for front in index["fronts"]}  # type: ignore[index]
    timelines = dict(index["front_timelines"])  # type: ignore[arg-type]
    for slug, dates in timelines.items():
        label = front_lookup.get(slug, slug)
        if dates:
            lines.append(f"- **{label}:** {', '.join(dates)}")
        else:
            lines.append(f"- **{label}:** no signal")

    recurring = [
        (front_lookup.get(slug, slug), dates)
        for slug, dates in timelines.items()
        if len(dates) >= 2
    ]
    lines.extend(["", "## Recurring Fronts", ""])
    if recurring:
        for label, dates in sorted(recurring, key=lambda x: (-len(x[1]), str(x[0]))):
            lines.append(f"- **{label}:** {len(dates)} issue(s), {dates[0]} through {dates[-1]}")
    else:
        lines.append("- No recurring fronts detected.")

    first_seen: dict[str, list[str]] = {}
    for slug, dates in timelines.items():
        if dates:
            first_seen.setdefault(dates[0], []).append(str(front_lookup.get(slug, slug)))
    lines.extend(["", "## Newly Appearing Fronts", ""])
    for day in sorted(first_seen):
        lines.append(f"- **{day}:** {', '.join(sorted(first_seen[day]))}")

    needs_review = [item for item in items if item.get("needs_review")]
    lines.extend(["", "## Needs Review", ""])
    if needs_review:
        for item in needs_review:
            weak = [
                str(front["label"])
                for front in item["detected_fronts"]  # type: ignore[index]
                if front.get("needs_review")
            ]
            reason = ", ".join(weak) if weak else "no deterministic front"
            lines.append(f"- **{item['date']}:** {reason}")
    else:
        lines.append("- No low-confidence deterministic front signals.")

    lines.extend(
        [
            "",
            "## Method",
            "",
            "- Reads only `## Newsletter Text` from each raw capture.",
            "- Removes repeated subscription and backfill boilerplate before scoring.",
            "- Scores fronts by exact deterministic term matches.",
            "- Marks low-confidence single-hit fronts as review items.",
            "- Rebuild with `python scripts/build_innermost_loop_longitudinal.py --apply`.",
            "",
        ]
    )
    return "\n".join(lines)

def _replace_or_insert_section(text: str, heading: str, body: str, *, before_heading: str | None = None) -> str:
    pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\n.*?(?=^## |\Z)")
    replacement = f"## {heading}\n\n{body.rstrip()}\n\n"
    if pattern.search(text):
        return pattern.sub(replacement, text)
    if before_heading and f"## {before_heading}" in text:
        idx = text.index(f"## {before_heading}")
        return (text[:idx].rstrip() + "\n\n" + replacement + text[idx:].lstrip()).rstrip() + "\n"
    return text.rstrip() + "\n\n" + replacement

def update_readme(readme: Path, *, apply: bool) -> None:
    if not readme.is_file():
        return
    body = (
        "- [The Innermost Loop longitudinal spine](longitudinal/innermost-loop.md) - dated front-by-front trend view.\n"
        "- [The Innermost Loop signals JSON](longitudinal/innermost-loop-signals.json) - structured deterministic front index.\n"
        "- [Spine Health Checklist](longitudinal/spine-health-checklist.md) - quick QA pass for coverage, review load, bridge isolation, and rebuild sanity."
    )
    text = readme.read_text(encoding="utf-8")
    new_text = _replace_or_insert_section(text, "Longitudinal Views", body, before_heading="First Instruments To Build")
    if new_text == text:
        return
    if apply:
        readme.write_text(new_text, encoding="utf-8")
        print(f"updated: {_relative(readme)}")
    else:
        print(f"would update: {_relative(readme)}")

def write_outputs(index: dict[str, object], out_dir: Path, *, apply: bool) -> None:
    md_path = out_dir / "innermost-loop.md"
    json_path = out_dir / "innermost-loop-signals.json"
    md_text = render_markdown(index)
    json_text = json.dumps(index, indent=2, sort_keys=True) + "\n"
    for path, content in [(md_path, md_text), (json_path, json_text)]:
        existed_before = path.is_file()
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            print(f"skip unchanged: {_relative(path)}")
            continue
        if not apply:
            print(f"{'would update' if path.is_file() else 'would write'}: {_relative(path)}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"{'updated' if existed_before else 'wrote'}: {_relative(path)}")

def run(*, raw_root: Path, out_dir: Path, readme: Path, apply: bool) -> int:
    index = build_index(raw_root)
    write_outputs(index, out_dir, apply=apply)
    update_readme(readme, apply=apply)
    if not apply:
        print("\nDry-run only. Pass --apply to write longitudinal artifacts.")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--readme", type=Path, default=DEFAULT_README)
    ap.add_argument("--apply", action="store_true", help="write files; default is dry-run")
    args = ap.parse_args()
    return run(
        raw_root=args.raw_root,
        out_dir=args.out_dir,
        readme=args.readme,
        apply=args.apply,
    )

if __name__ == "__main__":
    raise SystemExit(main())
