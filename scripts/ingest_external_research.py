#!/usr/bin/env python3
"""Ingest pasted external research into a lane-scoped artifact with optional derived outputs.

This script deliberately separates three responsibilities:

1. normalize pasted research into a validated external artifact
2. render optional WORK-layer derivatives such as academy briefs or offer memos
3. emit a derived self-proposal draft only when explicitly requested

It never writes directly to recursion-gate.md or other Record-bound surfaces.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema-registry" / "external-research-artifact.v1.json"

try:
    import jsonschema
except Exception:  # pragma: no cover - surfaced explicitly at runtime
    jsonschema = None

LANE_ROOTS = {
    "singularity-academy": REPO_ROOT / "research" / "external" / "singularity-academy",
    "work-dev": REPO_ROOT / "research" / "external" / "work-dev" / "external-research",
    "work-strategy": REPO_ROOT / "research" / "external" / "work-strategy" / "external-research",
    "work-business": REPO_ROOT / "research" / "external" / "work-business" / "external-research",
}

DEFAULT_SOURCE = "sci-bot.ru"
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)>]+", re.IGNORECASE)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


@dataclass
class OutputPaths:
    artifact_path: Path
    workshop_brief_path: Path | None = None
    offer_memo_path: Path | None = None
    self_proposal_path: Path | None = None


@dataclass
class DerivedOutputs:
    workshop_brief: str | None = None
    offer_memo: str | None = None
    self_proposal_draft: dict[str, Any] | None = None


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "research-topic"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_text(path_arg: str) -> str:
    if path_arg == "-":
        return sys.stdin.read()
    return Path(path_arg).read_text(encoding="utf-8")


def split_paragraphs(text: str) -> list[str]:
    chunks = re.split(r"\n\s*\n", text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def infer_summary(text: str) -> str:
    paragraphs = split_paragraphs(text)
    if not paragraphs:
        return "No summary could be inferred from the pasted research."
    summary = paragraphs[0].replace("\n", " ").strip()
    return summary[:600]


def extract_bullet_candidate(line: str) -> str | None:
    stripped = line.strip()
    for prefix in ("- ", "* "):
        if stripped.startswith(prefix):
            candidate = stripped[len(prefix):].strip()
            return candidate or None
    return None


def clean_labeled_value(text: str) -> str:
    cleaned = re.sub(r"^(citation|reference|paper)\s*:\s*", "", text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"[\s.]*doi(?:\s*:)?\s*$", "", cleaned, flags=re.IGNORECASE).strip(" -:;,.")
    return cleaned.strip()


def validate_artifact_fallback(artifact: dict[str, Any], schema: dict[str, Any]) -> None:
    required = set(schema.get("required", []))
    properties = schema.get("properties", {})

    missing = sorted(key for key in required if key not in artifact)
    if missing:
        raise ValueError(f"Artifact missing required fields: {', '.join(missing)}")

    unexpected = sorted(key for key in artifact if key not in properties)
    if unexpected:
        raise ValueError(f"Artifact has unexpected fields: {', '.join(unexpected)}")

    lane_enum = properties["lane"]["enum"]
    record_impact_enum = properties["record_impact"]["enum"]
    ingest_mode_enum = properties["ingest_mode"]["enum"]
    citation_status_enum = properties["citations"]["items"]["properties"]["resolution_status"]["enum"]

    if artifact["artifact_schema_version"] != 1:
        raise ValueError("artifact_schema_version must equal 1")
    if artifact["lane"] not in lane_enum:
        raise ValueError(f"Unsupported lane: {artifact['lane']}")
    if artifact["record_impact"] not in record_impact_enum:
        raise ValueError(f"Unsupported record_impact: {artifact['record_impact']}")
    if artifact["ingest_mode"] not in ingest_mode_enum:
        raise ValueError(f"Unsupported ingest_mode: {artifact['ingest_mode']}")
    if not re.fullmatch(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", artifact["topic_slug"]):
        raise ValueError("topic_slug must be lowercase kebab-case")

    for key in ("source", "query", "raw_capture", "summary"):
        if not isinstance(artifact[key], str) or not artifact[key].strip():
            raise ValueError(f"{key} must be a non-empty string")

    for key in ("key_claims", "citations", "tensions", "open_questions", "proposed_ix_updates", "proposed_skill_updates", "prepared_context_tags"):
        if not isinstance(artifact[key], list):
            raise ValueError(f"{key} must be a list")

    for claim in artifact["key_claims"]:
        if not isinstance(claim, dict):
            raise ValueError("Each key_claim must be an object")
        if set(claim) - {"claim", "citations", "evidence_strength", "notes"}:
            raise ValueError("Each key_claim may only contain claim, citations, evidence_strength, and notes")
        if not isinstance(claim.get("claim"), str) or not claim["claim"].strip():
            raise ValueError("Each key_claim.claim must be a non-empty string")
        if not isinstance(claim.get("citations"), list):
            raise ValueError("Each key_claim.citations must be a list")

    for citation in artifact["citations"]:
        if not isinstance(citation, dict):
            raise ValueError("Each citation must be an object")
        if set(citation) - {"id", "title", "authors", "year", "doi", "url", "pdf_url", "relevance", "snippet", "raw_text", "resolution_status"}:
            raise ValueError("Each citation contains unsupported fields")
        if not re.fullmatch(r"^cit-[0-9]{3}$", str(citation.get("id", ""))):
            raise ValueError("Each citation id must match cit-000 format")
        if not isinstance(citation.get("raw_text"), str) or not citation["raw_text"].strip():
            raise ValueError("Each citation.raw_text must be a non-empty string")
        if citation.get("resolution_status") not in citation_status_enum:
            raise ValueError("Each citation.resolution_status must be resolved, partial, or unresolved")


def infer_list_items(text: str, *, labels: tuple[str, ...]) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if any(label in lowered for label in labels):
            after_colon = stripped.split(":", 1)
            if len(after_colon) == 2 and after_colon[1].strip():
                items.append(after_colon[1].strip())
    return items


def infer_claims(text: str) -> list[dict[str, Any]]:
    claims: list[str] = []
    for line in text.splitlines():
        candidate = extract_bullet_candidate(line)
        if candidate and not DOI_RE.search(candidate) and not URL_RE.search(candidate):
            claims.append(candidate)
    if not claims:
        claims = [p.replace("\n", " ") for p in split_paragraphs(text)[:3]]
    out: list[dict[str, Any]] = []
    for claim in claims[:5]:
        out.append(
            {
                "claim": claim[:800],
                "citations": [],
                "evidence_strength": None,
                "notes": None,
            }
        )
    return out


def infer_citations(text: str) -> list[dict[str, Any]]:
    citations: list[dict[str, Any]] = []
    seen_keys: set[tuple[str | None, str | None, str | None]] = set()
    candidate_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if DOI_RE.search(stripped) or URL_RE.search(stripped):
            candidate_lines.append(stripped)
        elif any(token in stripped.lower() for token in ("citation", "reference", "paper", "doi")):
            candidate_lines.append(stripped)

    for idx, line in enumerate(candidate_lines, start=1):
        lowered = line.lower()
        urls = URL_RE.findall(line)
        if lowered.startswith("pdf:") and urls and citations:
            if citations[-1]["pdf_url"] is None:
                citations[-1]["pdf_url"] = urls[0]
                if citations[-1]["url"] is None:
                    citations[-1]["url"] = urls[0]
                if citations[-1]["resolution_status"] == "partial":
                    citations[-1]["resolution_status"] = "resolved"
            continue

        doi_match = DOI_RE.search(line)
        pdf_url = next((url for url in urls if ".pdf" in url.lower()), None)
        url = urls[0] if urls else None
        year_match = YEAR_RE.search(line)
        title_guess = line
        if url:
            title_guess = title_guess.replace(url, "").strip(" -:;,.")
        if doi_match:
            title_guess = title_guess.replace(doi_match.group(0), "").strip(" -:;,.")
        title = clean_labeled_value(title_guess) or None
        status = "resolved" if (doi_match or url) and title else "partial" if (doi_match or url) else "unresolved"
        key = (title, doi_match.group(0) if doi_match else None, url)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        citations.append(
            {
                "id": f"cit-{idx:03d}",
                "title": title,
                "authors": [],
                "year": int(year_match.group(0)) if year_match else None,
                "doi": doi_match.group(0) if doi_match else None,
                "url": url,
                "pdf_url": pdf_url,
                "relevance": None,
                "snippet": None,
                "raw_text": line[:1200],
                "resolution_status": status,
            }
        )
    return citations


def build_artifact(args: argparse.Namespace, raw_capture: str) -> dict[str, Any]:
    artifact: dict[str, Any] = {
        "artifact_schema_version": 1,
        "source": args.source,
        "source_url": args.source_url,
        "lane": args.lane,
        "topic_slug": slugify(args.topic),
        "captured_at": utc_now_iso(),
        "ingest_mode": "paste",
        "record_impact": args.record_impact,
        "query": args.query,
        "raw_capture": raw_capture.strip(),
        "summary": args.summary.strip() if args.summary else infer_summary(raw_capture),
        "key_claims": infer_claims(raw_capture),
        "citations": infer_citations(raw_capture),
        "tensions": infer_list_items(raw_capture, labels=("tension", "counter", "tradeoff")),
        "open_questions": infer_list_items(raw_capture, labels=("open question", "unknown", "unclear", "needs verification")),
        "proposed_ix_updates": list(args.ix_update),
        "proposed_skill_updates": list(args.skill_update),
        "prepared_context_tags": list(args.prepared_context_tag),
        "academy_surface": args.academy_surface,
        "acceleration_vector": args.acceleration_vector,
        "agent_type": args.agent_type,
        "alignment_risk": args.alignment_risk,
        "substrate_notes": args.substrate_notes,
        "displacement_notes": args.displacement_notes,
        "commercial_relevance": args.commercial_relevance,
        "reuse_output": args.reuse_output,
    }
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> None:
    if not SCHEMA_PATH.is_file():
        raise FileNotFoundError(f"Missing schema: {SCHEMA_PATH}")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if jsonschema is not None:
        jsonschema.validate(artifact, schema)
        return
    validate_artifact_fallback(artifact, schema)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def artifact_root_for_lane(lane: str) -> Path:
    return LANE_ROOTS[lane]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def artifact_relpath(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT.resolve())).replace("\\", "/")


def first_claim(artifact: dict[str, Any]) -> str:
    claims = artifact.get("key_claims") or []
    if claims:
        return str(claims[0].get("claim") or "").strip()
    return artifact["summary"]


def render_workshop_brief(artifact: dict[str, Any], artifact_path: Path) -> str:
    acceleration = artifact.get("acceleration_vector") or "Needs operator naming from the source artifact."
    agent = artifact.get("agent_type") or "Needs operator naming from the source artifact."
    alignment = artifact.get("alignment_risk") or "Clarify what objective is being optimized and who set it."
    substrate = artifact.get("substrate_notes") or "Clarify where authority, memory, and rollback live."
    displacement = artifact.get("displacement_notes") or "Clarify what human role or office is being weakened or strengthened."
    reuse = artifact.get("reuse_output") or "Derive one reusable agency map, warning, or bridge question."
    return "\n".join(
        [
            f"# Academy Brief - {artifact['topic_slug']}",
            "",
            "WORK only; upstream external research, not workshop truth.",
            "",
            f"- Source artifact: `{artifact_relpath(artifact_path)}`",
            f"- Source: `{artifact['source']}`",
            f"- Query: {artifact['query']}",
            "",
            "## Summary",
            artifact["summary"],
            "",
            "## Name the acceleration",
            acceleration,
            "",
            "## Name the agent",
            agent,
            "",
            "## Test alignment",
            alignment,
            "",
            "## Test substrate",
            substrate,
            "",
            "## Test displacement",
            displacement,
            "",
            "## Produce reuse",
            reuse,
            "",
            "## Source-bound notes",
            f"- Lead claim: {first_claim(artifact)}",
            f"- Tensions: {', '.join(artifact['tensions']) if artifact['tensions'] else 'None extracted; verify manually.'}",
            f"- Open questions: {', '.join(artifact['open_questions']) if artifact['open_questions'] else 'None extracted; verify manually.'}",
        ]
    ) + "\n"


def render_offer_memo(artifact: dict[str, Any], artifact_path: Path) -> str:
    commercial = artifact.get("commercial_relevance") or "Translate the research into buyer pain and proof discipline before reuse."
    return "\n".join(
        [
            f"# Singularity-Academy Offer Memo - {artifact['topic_slug']}",
            "",
            "WORK only; source-bound business memo derived from external research.",
            "",
            f"- Source artifact: `{artifact_relpath(artifact_path)}`",
            f"- Query: {artifact['query']}",
            "",
            "## Workflow pain evidenced",
            commercial,
            "",
            "## Reusable control-plane lesson",
            artifact.get("substrate_notes") or "Clarify where review, authority, and rollback have to remain human-owned.",
            "",
            "## Proof claim strengthened",
            artifact.get("reuse_output") or "Name the narrow claim this research makes safer for the AI Operating System Sprint.",
            "",
            "## Outreach language to sharpen carefully",
            artifact.get("alignment_risk") or "Convert the research into bounded, non-hyped language before client-facing reuse.",
            "",
            "## Source-bound notes",
            f"- Summary: {artifact['summary']}",
            f"- Lead claim: {first_claim(artifact)}",
        ]
    ) + "\n"


def build_self_proposal_draft(artifact: dict[str, Any], artifact_path: Path) -> dict[str, Any]:
    suggested_entry = artifact["proposed_ix_updates"][0] if artifact["proposed_ix_updates"] else first_claim(artifact)
    prompt_addition = artifact["proposed_skill_updates"][0] if artifact["proposed_skill_updates"] else artifact["summary"]
    grounding_excerpt = artifact["raw_capture"][:1200].strip()
    return {
        "hypothesis": f"External research on {artifact['topic_slug']} contains a durable self-facing insight worth review.",
        "expected_delta": 0.02,
        "grounding_mode": "strict",
        "proposal_type": "recursion_gate_candidate",
        "target_surface": "self",
        "candidate_bundle": {
            "title": f"External research draft - {artifact['topic_slug']}",
            "summary": artifact["summary"],
            "source": "operator - external research ingest",
            "source_exchange": {
                "operator": grounding_excerpt,
                "artifact": f"Derived from {artifact_relpath(artifact_path)}",
            },
            "mind_category": "knowledge",
            "signal_type": "external_research_proposal",
            "priority_score": 2,
            "profile_target": "IX-A. KNOWLEDGE",
            "suggested_entry": suggested_entry,
            "prompt_section": "YOUR KNOWLEDGE",
            "prompt_addition": prompt_addition,
            "new_vs_record": f"Derived draft only; review against current Record before any promotion. Source artifact: {artifact_relpath(artifact_path)}",
            "suggested_followup": "Review whether this is truly a durable self-facing claim before using any self-proposals promotion flow.",
        },
        "evaluation_notes": "Derived from WORK-only external research. Not gate-ready until explicitly reviewed.",
    }


def validate_requested_outputs(args: argparse.Namespace) -> None:
    if args.emit_workshop_brief and args.lane != "singularity-academy":
        raise ValueError("--emit-workshop-brief is only valid with --lane singularity-academy")
    if args.emit_offer_memo and args.lane != "singularity-academy":
        raise ValueError("--emit-offer-memo is only valid with --lane singularity-academy")


def default_output_paths(args: argparse.Namespace, artifact: dict[str, Any]) -> OutputPaths:
    topic_slug = artifact["topic_slug"]
    date_prefix = artifact["captured_at"][:10]
    root = artifact_root_for_lane(args.lane)
    if args.lane == "singularity-academy":
        artifact_path = root / "queries" / f"{date_prefix}-{topic_slug}.json"
        workshop_path = root / "briefs" / f"{date_prefix}-{topic_slug}-academy-brief.md" if args.emit_workshop_brief else None
    else:
        artifact_path = root / f"{date_prefix}-{topic_slug}.json"
        workshop_path = None
    offer_path = (
        REPO_ROOT / "docs" / "skill-work" / "work-business" / "singularity-academy-research-memos" / f"{date_prefix}-{topic_slug}-offer-memo.md"
        if args.emit_offer_memo
        else None
    )
    self_proposal_path = (
        REPO_ROOT / "auto-research" / "self-proposals" / "derived" / f"{date_prefix}-{topic_slug}.json"
        if args.emit_self_proposal
        else None
    )
    return OutputPaths(
        artifact_path=artifact_path,
        workshop_brief_path=workshop_path,
        offer_memo_path=offer_path,
        self_proposal_path=self_proposal_path,
    )


def build_derived_outputs(args: argparse.Namespace, artifact: dict[str, Any], artifact_path: Path) -> DerivedOutputs:
    return DerivedOutputs(
        workshop_brief=render_workshop_brief(artifact, artifact_path) if args.emit_workshop_brief else None,
        offer_memo=render_offer_memo(artifact, artifact_path) if args.emit_offer_memo else None,
        self_proposal_draft=build_self_proposal_draft(artifact, artifact_path) if args.emit_self_proposal else None,
    )


def write_outputs(args: argparse.Namespace, artifact: dict[str, Any]) -> OutputPaths:
    paths = default_output_paths(args, artifact)
    write_json(paths.artifact_path, artifact)
    derived = build_derived_outputs(args, artifact, paths.artifact_path)

    if paths.workshop_brief_path is not None and derived.workshop_brief is not None:
        ensure_dir(paths.workshop_brief_path.parent)
        paths.workshop_brief_path.write_text(derived.workshop_brief, encoding="utf-8")
    if paths.offer_memo_path is not None and derived.offer_memo is not None:
        ensure_dir(paths.offer_memo_path.parent)
        paths.offer_memo_path.write_text(derived.offer_memo, encoding="utf-8")
    if paths.self_proposal_path is not None and derived.self_proposal_draft is not None:
        write_json(paths.self_proposal_path, derived.self_proposal_draft)
    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest pasted external research into a lane-scoped artifact.",
        epilog=(
            "Example:\n"
            "  python scripts/ingest_external_research.py --lane singularity-academy "
            '--topic "AI workflow authority" '
            '--query "How should review-gated AI workflow research be applied to singularity academy?" '
            "--input sample.txt --emit-workshop-brief --emit-offer-memo"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--lane", required=True, choices=sorted(LANE_ROOTS))
    parser.add_argument("--topic", required=True, help="Human-readable topic; will be slugified for filenames.")
    parser.add_argument("--query", required=True, help="Original research query used to obtain the source material.")
    parser.add_argument("--input", required=True, help="Path to pasted raw research text, or '-' for stdin.")
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--source-url")
    parser.add_argument("--summary")
    parser.add_argument("--record-impact", default="none", choices=("none", "possible", "proposed"))
    parser.add_argument("--academy-surface")
    parser.add_argument("--acceleration-vector")
    parser.add_argument("--agent-type")
    parser.add_argument("--alignment-risk")
    parser.add_argument("--substrate-notes")
    parser.add_argument("--displacement-notes")
    parser.add_argument("--commercial-relevance")
    parser.add_argument("--reuse-output")
    parser.add_argument("--prepared-context-tag", action="append", default=[])
    parser.add_argument("--ix-update", action="append", default=[])
    parser.add_argument("--skill-update", action="append", default=[])
    parser.add_argument("--emit-workshop-brief", action="store_true")
    parser.add_argument("--emit-offer-memo", action="store_true")
    parser.add_argument("--emit-self-proposal", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        validate_requested_outputs(args)
    except ValueError as exc:
        parser.error(str(exc))
    raw_capture = load_text(args.input)
    if not raw_capture.strip():
        parser.error("input was empty")
    artifact = build_artifact(args, raw_capture)
    validate_artifact(artifact)
    paths = write_outputs(args, artifact)
    payload = {
        "artifact_path": artifact_relpath(paths.artifact_path),
        "workshop_brief_path": artifact_relpath(paths.workshop_brief_path) if paths.workshop_brief_path else None,
        "offer_memo_path": artifact_relpath(paths.offer_memo_path) if paths.offer_memo_path else None,
        "self_proposal_path": artifact_relpath(paths.self_proposal_path) if paths.self_proposal_path else None,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
