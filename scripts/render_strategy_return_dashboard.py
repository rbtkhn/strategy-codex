#!/usr/bin/env python3
"""Render a derived HTML dashboard for the explicit Strategy return hint.

The dashboard is an operator view only. It reads Strategy-codex work-layer
sources, renders static HTML, and does not mutate canonical notebook or Record
surfaces.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

try:
    from strategy_return_hint import (
        DEFAULT_INBOX,
        DEFAULT_RAW_ROOT,
        DEFAULT_STATUS,
        REPO_ROOT,
        StrategyReturnHint,
        accumulator_drift_days,
        build_strategy_return_hint,
        read_text,
    )
except ImportError:
    from scripts.strategy_return_hint import (
        DEFAULT_INBOX,
        DEFAULT_RAW_ROOT,
        DEFAULT_STATUS,
        REPO_ROOT,
        StrategyReturnHint,
        accumulator_drift_days,
        build_strategy_return_hint,
        read_text,
    )

DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "work-strategy" / "strategy-return-dashboard.html"
ACCUMULATOR_RE = re.compile(r"\*\*Accumulator for:\*\*\s*(\d{4}-\d{2}-\d{2})")


@dataclass(frozen=True)
class DashboardContext:
    hint: StrategyReturnHint
    generated_at: str
    source_paths: tuple[str, ...]
    accumulator_date: str | None
    accumulator_status: str
    accumulator_drift_days: int | None


def configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def accumulator_date_from_inbox(inbox_text: str) -> str | None:
    match = ACCUMULATOR_RE.search(inbox_text)
    if not match:
        return None
    return match.group(1)


def accumulator_status(accumulator_date: str | None, *, today: date | None = None) -> str:
    if accumulator_date is None:
        return "unknown - no Accumulator for line found"
    today = today or date.today()
    try:
        parsed = date.fromisoformat(accumulator_date)
    except ValueError:
        return "unknown - accumulator date is malformed"
    drift = (today - parsed).days
    if drift == 0:
        return "fresh - accumulator date matches today"
    if drift > 0:
        return f"stale - accumulator is {drift} day(s) behind today"
    return f"future-dated - accumulator is {abs(drift)} day(s) ahead of today"


def accumulator_drift_label(drift_days: int | None) -> str:
    if drift_days is None:
        return "unknown"
    if drift_days == 0:
        return "0d"
    sign = "+" if drift_days > 0 else "-"
    return f"{sign}{abs(drift_days)}d"


def build_dashboard_context(
    repo_root: Path = REPO_ROOT,
    *,
    generated_at: str | None = None,
    today: date | None = None,
) -> DashboardContext:
    hint = build_strategy_return_hint(repo_root)
    inbox_path = repo_root / "codex" / "daily-strategy-inbox.md"
    status_path = repo_root / "codex" / "STATUS.md"
    raw_root = repo_root / "source-archive" / "statecraft"
    inbox_text = read_text(inbox_path)
    acc_date = accumulator_date_from_inbox(inbox_text)
    drift_days = accumulator_drift_days(acc_date, today=today)
    sources = [
        rel(inbox_path, repo_root),
        rel(status_path, repo_root),
        rel(raw_root, repo_root),
        "scripts/strategy_return_hint.py",
    ]
    if hint.active_days_path:
        sources.append(hint.active_days_path)
    return DashboardContext(
        hint=hint,
        generated_at=generated_at or datetime.now().astimezone().isoformat(timespec="seconds"),
        source_paths=tuple(sources),
        accumulator_date=acc_date,
        accumulator_status=accumulator_status(acc_date, today=today),
        accumulator_drift_days=drift_days,
    )


def card(label: str, value: str | int, detail: str, class_name: str = "") -> str:
    klass = f' class="card {html.escape(class_name)}"' if class_name else ' class="card"'
    return (
        f"<article{klass}>"
        f"<span>{html.escape(label)}</span>"
        f"<strong>{html.escape(str(value))}</strong>"
        f"<p>{html.escape(detail)}</p>"
        "</article>"
    )


def render_dashboard_html(ctx: DashboardContext) -> str:
    h = ctx.hint
    source_items = "\n".join(f"<li><code>{html.escape(path)}</code></li>" for path in ctx.source_paths)
    gap_items = ""
    if h.raw_input_gap_urls:
        gap_items = "\n".join(
            f"<li><code>{html.escape(url)}</code></li>" for url in h.raw_input_gap_urls
        )
    source_panel = ""
    if h.raw_input_gap:
        source_panel = f"""
        <section class="panel warning">
          <h2>Source Hygiene Panel</h2>
          <p><strong>{h.raw_input_gap}</strong> possible source-archive gap(s) remain after ignoring placeholder YouTube IDs and rows with same-line source pointers.</p>
          <ul class="source-list">
            {gap_items}
          </ul>
          <p>Use explicit source hygiene before page or chapter composition. Coffee C is Statecraft.</p>
        </section>
        """
    else:
        source_panel = """
        <section class="panel calm">
          <h2>Source Hygiene Panel</h2>
          <p>No source-archive gaps detected by the current heuristic. Keep treating this as advisory, not proof of complete sourcing.</p>
        </section>
        """

    cards = "\n".join(
        [
            card("Ready", h.ready, "Synthesis-ready clusters: batch-analysis, page-ready, strategy-page, compose-read, or weave.", "ready"),
            card("Verify", h.verify, "Lines carrying verify pressure or pending-primary language.", "verify"),
            card("Source-archive gap", h.raw_input_gap, "Article-like URLs not matched to source-archive `source_url` or same-row source pointer.", "gap"),
            card("Carry", h.carry, "Open loop, revisit, falsifier, carry, or live-tension signals.", "carry"),
            card("Active chapter", h.active_chapter or "unknown", h.active_days_path or "No active days.md path resolved.", "chapter"),
            card("Accumulator drift", accumulator_drift_label(ctx.accumulator_drift_days), ctx.accumulator_status, "freshness"),
            card("Accumulator", ctx.accumulator_date or "unknown", ctx.accumulator_status, "freshness"),
        ]
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Strategy Return Dashboard</title>
  <style>
    :root {{
      --ink: #1f2523;
      --muted: #66716c;
      --paper: #f6f0e5;
      --panel: #fffaf0;
      --line: #d7c9b2;
      --accent: #b4512a;
      --accent-2: #255f6b;
      --warn: #8a3d22;
      --ok: #496c45;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(180, 81, 42, 0.16), transparent 32rem),
        linear-gradient(135deg, #f9f4ea 0%, var(--paper) 48%, #ebe1d0 100%);
      font-family: Georgia, "Times New Roman", serif;
      line-height: 1.5;
    }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 40px 22px 60px; }}
    header {{
      display: grid;
      gap: 18px;
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: rgba(255, 250, 240, 0.86);
      box-shadow: 0 24px 80px rgba(77, 55, 34, 0.14);
    }}
    .eyebrow {{ color: var(--accent); font: 700 0.78rem/1.2 ui-monospace, "SFMono-Regular", Consolas, monospace; letter-spacing: 0.12em; text-transform: uppercase; }}
    h1 {{ margin: 0; font-size: clamp(2.2rem, 7vw, 5.5rem); line-height: 0.94; letter-spacing: -0.055em; }}
    h2 {{ margin: 0 0 10px; font-size: 1.18rem; }}
    .lede {{ max-width: 850px; margin: 0; color: #3d4642; font-size: 1.08rem; }}
    .warning-strip {{
      padding: 12px 14px;
      border-radius: 14px;
      background: #ffe8d8;
      color: #6a2e1a;
      font-weight: 700;
    }}
    .move {{
      margin: 24px 0;
      padding: 22px;
      border-left: 8px solid var(--accent);
      border-radius: 18px;
      background: var(--panel);
    }}
    .move p {{ margin: 0; font-size: clamp(1.2rem, 3vw, 2rem); font-weight: 700; }}
    .grid {{ display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 14px; margin: 22px 0; }}
    .card {{
      grid-column: span 2;
      min-height: 155px;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: rgba(255, 250, 240, 0.9);
    }}
    .card span {{ display: block; color: var(--muted); font: 700 0.75rem/1.2 ui-monospace, Consolas, monospace; text-transform: uppercase; letter-spacing: 0.1em; }}
    .card strong {{ display: block; margin: 8px 0; font-size: clamp(2rem, 5vw, 4rem); line-height: 0.95; color: var(--accent-2); }}
    .card p {{ margin: 0; color: var(--muted); }}
    .gap strong, .warning strong {{ color: var(--warn); }}
    .panel {{
      margin-top: 18px;
      padding: 22px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: rgba(255, 250, 240, 0.88);
    }}
    .panel.warning {{ border-color: #d2997d; background: #fff2e9; }}
    .panel.calm {{ border-color: #b7c9ad; background: #f2f7ec; }}
    code {{
      padding: 0.1rem 0.28rem;
      border-radius: 0.35rem;
      background: rgba(31, 37, 35, 0.08);
      font-family: ui-monospace, "SFMono-Regular", Consolas, monospace;
      font-size: 0.9em;
    }}
    .source-list {{ columns: 2; padding-left: 1.2rem; }}
    footer {{ margin-top: 28px; color: var(--muted); font-size: 0.92rem; }}
    @media (max-width: 760px) {{
      main {{ padding: 20px 14px 40px; }}
      header {{ padding: 20px; }}
      .grid {{ grid-template-columns: 1fr; }}
      .card {{ grid-column: span 1; }}
      .source-list {{ columns: 1; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="eyebrow">Derived Strategy-codex Operator View</div>
      <h1>Strategy Return Dashboard</h1>
      <p class="lede">A static HTML reading layer for the Strategy return hint. It does not replace Markdown, source-archive, strategy pages, chapters, Coffee C Statecraft, or governed Record surfaces.</p>
      <div class="warning-strip">Non-canonical / derived / rebuildable. No files were mutated by this dashboard.</div>
    </header>

    <section class="move">
      <h2>Suggested Strategy Move</h2>
      <p>{html.escape(h.suggested_move)}</p>
    </section>

    <section class="panel">
      <h2>Live Seam</h2>
      <p>{html.escape(h.live_seam)}</p>
    </section>

    <section class="grid" aria-label="Strategy return cards">
      {cards}
    </section>

    {source_panel}

    <section class="panel">
      <h2>Provenance</h2>
      <p><strong>Generated:</strong> {html.escape(ctx.generated_at)}</p>
      <p><strong>Active chapter:</strong> {html.escape(h.active_chapter or "unknown")}</p>
      <p><strong>Sources read:</strong></p>
      <ul class="source-list">
        {source_items}
      </ul>
    </section>

    <footer>
      <p>Regenerate with <code>python scripts/render_strategy_return_dashboard.py</code>. This artifact is a view, not the score.</p>
    </footer>
  </main>
</body>
</html>
"""


def write_dashboard(repo_root: Path = REPO_ROOT, output: Path = DEFAULT_OUTPUT) -> Path:
    ctx = build_dashboard_context(repo_root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_dashboard_html(ctx), encoding="utf-8")
    return output


def main() -> int:
    configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Render the derived Strategy return HTML dashboard.")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    path = write_dashboard(args.repo_root, args.output)
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
