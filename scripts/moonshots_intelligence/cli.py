"""CLI orchestration for Moonshots intelligence compiler."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from moonshots_intelligence.assemble import assemble_document  # noqa: E402
from moonshots_intelligence.evidence import extract_evidence  # noqa: E402
from moonshots_intelligence.generate import generate_document  # noqa: E402
from moonshots_intelligence.ingest import default_out_dir, ingest_archive  # noqa: E402
from moonshots_intelligence.nst_map import apply_nst_mapping  # noqa: E402
from moonshots_intelligence.render import render_markdown  # noqa: E402
from moonshots_intelligence.segment import segment_body, segments_lossless  # noqa: E402


def compile_archive(
    archive_path: Path,
    *,
    out_dir: Path,
    strict: bool = False,
    nst: bool = False,
    dry_run: bool = False,
    bullets_json: Path | None = None,
    model: str | None = None,
    write: bool = True,
) -> dict[str, Any]:
    ingested = ingest_archive(archive_path)
    segments = segment_body(ingested.body)
    if not segments_lossless(ingested.body, segments):
        raise ValueError("segmentation is not lossless")

    evidence_blocks = extract_evidence(segments)
    result: dict[str, Any] = {
        "evidence_count": len(evidence_blocks),
        "evidence": [
            {
                "evidence_id": b.evidence_id,
                "source_location": b.source_location,
                "word_count": b.word_count,
            }
            for b in evidence_blocks
        ],
    }

    if dry_run:
        result["dry_run"] = True
        return result

    if not evidence_blocks:
        raise ValueError("no evidence blocks >= 30 words")

    draft, receipt = generate_document(
        evidence_blocks,
        bullets_json_path=bullets_json,
        model=model,
    )
    document = assemble_document(
        archive_path=ingested.archive_path,
        meta=ingested.meta,
        archive_body=ingested.body,
        evidence_blocks=evidence_blocks,
        draft=draft,
        receipt=receipt,
        strict=strict,
    )
    if nst:
        document = apply_nst_mapping(document)

    basename = document["provenance"]["output_basename"]
    json_path = out_dir / f"{basename}.json"
    md_path = out_dir / f"{basename}.md"

    if write:
        out_dir.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(document, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        md_path.write_text(render_markdown(document), encoding="utf-8")

    result["output_json"] = str(json_path)
    result["output_md"] = str(md_path)
    result["bullet_count"] = len(document.get("bullets") or [])
    return result


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Compile Moonshots archive to intelligence document")
    parser.add_argument("--archive", type=Path, required=True, help="Path to archive .md capture")
    parser.add_argument("--out", type=Path, default=default_out_dir(), help="Output directory")
    parser.add_argument("--strict", action="store_true", help="Require >= 10 validated bullets")
    parser.add_argument("--nst", action="store_true", help="Add NST mapping layer")
    parser.add_argument("--dry-run", action="store_true", help="Evidence extraction only")
    parser.add_argument("--bullets-json", type=Path, help="Inject/replay bullet document JSON")
    parser.add_argument("--model", type=str, default=None, help="OpenAI model override")
    args = parser.parse_args(argv)

    try:
        result = compile_archive(
            args.archive.resolve(),
            out_dir=args.out.resolve(),
            strict=args.strict,
            nst=args.nst,
            dry_run=args.dry_run,
            bullets_json=args.bullets_json,
            model=args.model,
        )
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
