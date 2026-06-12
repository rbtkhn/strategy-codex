#!/usr/bin/env python3
"""Smoke benchmark: Barnes source-index discovery — wrong surfaces vs routing path."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from yaml_compat import safe_load_path

TARGET_REL = Path("statecraft/civ-lens/barnes/barnes-source-index.md")
TARGET_NAME = TARGET_REL.name
CANONICAL = TARGET_REL.as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def wrong_surface_search() -> list[str]:
    """Barnes failure path: library/dashboard surfaces agents opened first."""
    hits: list[str] = []
    for rel in (
        "artifacts/library-index.md",
        "self-library.md",
        "self-library",
    ):
        path = REPO_ROOT / rel
        if path.is_file() and TARGET_NAME in _read_text(path):
            hits.append(rel)
    return hits


def llm_routing_table() -> str | None:
    """Routing path step 1: LLM-ROUTING dispatch row for Barnes."""
    routing = REPO_ROOT / "LLM-ROUTING.md"
    if not routing.is_file():
        return None
    text = _read_text(routing)
    routed = (
        "barnes/barnes-source-index" in text
        or CANONICAL in text
        or "civ-lens/barnes/" in text
    )
    if not routed:
        return None
    target = REPO_ROOT / CANONICAL
    return CANONICAL if target.is_file() else None


def civ_lens_index() -> str | None:
    """Routing path step 2: civ-lens INDEX table."""
    index = REPO_ROOT / "statecraft/civ-lens/INDEX.md"
    if not index.is_file():
        return None
    text = _read_text(index)
    if TARGET_NAME not in text and "barnes/barnes-source-index" not in text:
        return None
    target = REPO_ROOT / CANONICAL
    return CANONICAL if target.is_file() else None


def repo_map_route() -> str | None:
    """Routing path via machine-readable registry."""
    repo_map = REPO_ROOT / "repo-map.yaml"
    if not repo_map.is_file():
        return None
    data = safe_load_path(repo_map, feature="benchmark_routing_discovery.py")
    for route in data.get("routes", []):
        if route.get("id") == "barnes-source-index":
            rel = str(route.get("path", "")).replace("\\", "/")
            target = REPO_ROOT / rel
            if target.is_file():
                return rel
    return None


def rg_repo_search() -> list[str]:
    """Unrouted full-repo text search (may return many paths)."""
    rg = shutil.which("rg")
    if rg:
        proc = subprocess.run(
            [rg, "-l", "--fixed-strings", TARGET_NAME, str(REPO_ROOT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode in (0, 1):
            return [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return [
        p.relative_to(REPO_ROOT).as_posix()
        for p in REPO_ROOT.rglob(TARGET_NAME)
    ]


def timed(name: str, fn: Callable[[], Any], *, rounds: int) -> dict[str, Any]:
    samples: list[float] = []
    result: Any = None
    for _ in range(rounds):
        start = time.perf_counter()
        result = fn()
        samples.append(time.perf_counter() - start)
    return {
        "name": name,
        "rounds": rounds,
        "min_ms": round(min(samples) * 1000, 2),
        "mean_ms": round(sum(samples) / len(samples) * 1000, 2),
        "result": result,
    }


def run_benchmark(*, rounds: int) -> list[dict[str, Any]]:
    return [
        timed("wrong_surface (library-index + self-library)", wrong_surface_search, rounds=rounds),
        timed("rg full-repo filename search", rg_repo_search, rounds=rounds),
        timed("LLM-ROUTING dispatch", llm_routing_table, rounds=rounds),
        timed("civ-lens INDEX", civ_lens_index, rounds=rounds),
        timed("repo-map barnes-source-index", repo_map_route, rounds=rounds),
    ]


def format_report(rows: list[dict[str, Any]]) -> str:
    lines = [
        "## Barnes index discovery benchmark",
        "",
        f"Target: `{CANONICAL}`",
        "",
        "| Path | min ms | mean ms | found |",
        "| --- | ---: | ---: | --- |",
    ]
    for row in rows:
        result = row["result"]
        if isinstance(result, list):
            found = "yes" if CANONICAL in result else f"{len(result)} hit(s), not canonical"
            if not result:
                found = "no"
        else:
            found = "yes" if result == CANONICAL else "no"
        lines.append(
            f"| {row['name']} | {row['min_ms']} | {row['mean_ms']} | {found} |"
        )
    routed = [r for r in rows if r["name"].startswith(("LLM-ROUTING", "civ-lens", "repo-map"))]
    wrong = [r for r in rows if r["name"].startswith("wrong_surface")][0]
    best_routed = min(r["min_ms"] for r in routed)
    lines.extend(
        [
            "",
            f"- Wrong-surface min: {wrong['min_ms']} ms (found: {bool(wrong['result'])})",
            f"- Best routed path min: {best_routed} ms",
        ]
    )
    if wrong["min_ms"] > 0 and best_routed > 0:
        ratio = wrong["min_ms"] / best_routed if best_routed else 0
        lines.append(
            f"- Routed path is ~{ratio:.1f}x faster when wrong surface misses (latency only; "
            "correctness gain is finding the canonical index at all)."
        )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="Timing rounds per scenario (default: 5)",
    )
    args = ap.parse_args()
    rows = run_benchmark(rounds=max(1, args.rounds))
    print(format_report(rows))
    routed_ok = any(
        row["result"] == CANONICAL
        for row in rows
        if row["name"] in {
            "LLM-ROUTING dispatch",
            "civ-lens INDEX",
            "repo-map barnes-source-index",
        }
    )
    return 0 if routed_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
