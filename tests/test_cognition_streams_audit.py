from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import cognition_streams_audit as csa  # noqa: E402


def _receipt(channel_key: str, channel_name: str, rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "channel_key": channel_key,
        "channel_name": channel_name,
        "window": {"start": "2026-05-11", "end": "2026-05-13"},
        "sources_attempted": ["uploads_playlist"],
        "source_used": "uploads_playlist",
        "errors": [],
        "items": rows,
    }


def _write_raw(path: Path, *, source_url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\nsource_url: \"{source_url}\"\n---\nbody\n", encoding="utf-8")


def test_may_regression_classifications_and_queue(tmp_path: Path) -> None:
    receipts = tmp_path / "receipts" / "2026-05-11_to_2026-05-13"
    out_dir = tmp_path / "artifacts"
    notebook = tmp_path / "codex" / "2026"
    raw_root = notebook / "raw-input"

    _write_raw(
        raw_root / "2026-05-12" / "davis-barnes-companion.md",
        source_url="https://www.youtube.com/watch?v=22cOVLIatOw",
    )
    _write_raw(
        raw_root / "2026-05-12" / "glenn-chas.md",
        source_url="https://www.youtube.com/watch?v=YKvzjkOfyWQ",
    )
    _write_raw(
        raw_root / "2026-05-12" / "glenn-sachs.md",
        source_url="https://www.youtube.com/watch?v=D8WeTG3rAFs",
    )

    glenn_rows = [
        {
            "id": "YKvzjkOfyWQ",
            "title": "Chas Freeman: Trump Goes to Beijing After Historic Defeat in Iran",
            "url": "https://www.youtube.com/watch?v=YKvzjkOfyWQ",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 3620,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "D8WeTG3rAFs",
            "title": "Jeffrey Sachs: New European Military Bloc for War Against Russia",
            "url": "https://www.youtube.com/watch?v=D8WeTG3rAFs",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 3440,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "Z1TQNvoUhTk",
            "title": "Douglas Macgregor on Glenn Diesen podcast",
            "url": "https://www.youtube.com/watch?v=Z1TQNvoUhTk",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 61,
            "discovery_source": "uploads_playlist",
        },
    ]
    davis_rows = [
        {
            "id": "M_0XZf3qdQI",
            "title": "Trump v. Xi: Battle for Strategic Advantage",
            "url": "https://www.youtube.com/watch?v=M_0XZf3qdQI",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 3500,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "F96pMYCZK84",
            "title": "Iran War Both Sides Declaring Victory",
            "url": "https://www.youtube.com/watch?v=F96pMYCZK84",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 3000,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "ntHXdIvOcIk",
            "title": "Col Douglas Macgregor: IF WE Go Back To BOMBING IRAN",
            "url": "https://www.youtube.com/watch?v=ntHXdIvOcIk",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 2400,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "S3bPrYf1w40",
            "title": "Trump & American's Pocketbooks (Iran War)",
            "url": "https://www.youtube.com/watch?v=S3bPrYf1w40",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 27,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "8mMvRD0bYb8",
            "title": "Trump & American's Pocketbooks (Does He Care?)",
            "url": "https://www.youtube.com/watch?v=8mMvRD0bYb8",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 27,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "WmG-x4BFd00",
            "title": "Trump's most confrontational foreign policy...",
            "url": "https://www.youtube.com/watch?v=WmG-x4BFd00",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 45,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "22cOVLIatOw",
            "title": "Iran War Plans on the Table/ Robert Barnes & Lt Col Daniel Davis",
            "url": "https://www.youtube.com/watch?v=22cOVLIatOw",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 980,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "tfgfSubAEJM",
            "title": "Col Doug Macgregor: Trump Visits China",
            "url": "https://www.youtube.com/watch?v=tfgfSubAEJM",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 540,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "klvztvA37b8",
            "title": "Iran's Power Is a Fact, Not a Debate / Lt Col Daniel Davis",
            "url": "https://www.youtube.com/watch?v=klvztvA37b8",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 1150,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "QCUzMPfGuZY",
            "title": "Prof John Mearsheimer LIVE TODAY 2:00p et",
            "url": "https://www.youtube.com/watch?v=QCUzMPfGuZY",
            "upload_date": "2026-05-13",
            "date": "2026-05-13",
            "duration_seconds": 0,
            "discovery_source": "uploads_playlist",
            "live_status": "is_upcoming",
        },
    ]
    dialogue_rows = [
        {
            "id": "vmCvNogL8PU",
            "title": "Col. Larry Wilkerson: Iran WIPES OUT Trump's Proposal & INSISTS on Its Own Terms",
            "url": "https://www.youtube.com/watch?v=vmCvNogL8PU",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 3569,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "Uhgd6vRsPxA",
            "title": "Seyed M. Marandi: Hezbollah's FPV Drones HUMILIATE Israeli Air Defenses",
            "url": "https://www.youtube.com/watch?v=Uhgd6vRsPxA",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 3320,
            "discovery_source": "uploads_playlist",
        },
        {
            "id": "rTmm2b60yNM",
            "title": "John Helmer: Iran Just Did the Unthinkable - China's Response to Trump Changes EVERYTHING",
            "url": "https://www.youtube.com/watch?v=rTmm2b60yNM",
            "upload_date": "2026-05-12",
            "date": "2026-05-12",
            "duration_seconds": 4010,
            "discovery_source": "uploads_playlist",
        },
    ]

    receipts.mkdir(parents=True)
    (receipts / "glenn-diesen.discovery.json").write_text(
        json.dumps(_receipt("glenn-diesen", "Glenn Diesen", glenn_rows), indent=2),
        encoding="utf-8",
    )
    (receipts / "daniel-davis-deep-dive.discovery.json").write_text(
        json.dumps(_receipt("daniel-davis-deep-dive", "Daniel Davis / Deep Dive", davis_rows), indent=2),
        encoding="utf-8",
    )
    (receipts / "dialogue-works.discovery.json").write_text(
        json.dumps(_receipt("dialogue-works", "Dialogue Works", dialogue_rows), indent=2),
        encoding="utf-8",
    )

    watchlist = tmp_path / "watchlist.json"
    watchlist.write_text(
        json.dumps(
            {
                "channels": [
                    {
                        "channel_key": "glenn-diesen",
                        "channel_name": "Glenn Diesen",
                        "channel_id": "UCZFCDIHTe9HGxtIuVDpBz7g",
                        "uploads_playlist_id": "UUZFCDIHTe9HGxtIuVDpBz7g",
                        "handle_url": "https://www.youtube.com/@GDiesen1",
                        "show": "Glenn Diesen",
                        "host": "Glenn Diesen",
                        "thread": "diesen",
                        "file_prefix": "youtube-glenn-diesen",
                        "discovery_priority": csa.DISCOVERY_SOURCE_ORDER,
                    },
                    {
                        "channel_key": "daniel-davis-deep-dive",
                        "channel_name": "Daniel Davis / Deep Dive",
                        "channel_id": "UCWDN5zr5ttctoIAhZwW6tcQ",
                        "uploads_playlist_id": "UUWDN5zr5ttctoIAhZwW6tcQ",
                        "handle_url": "https://www.youtube.com/@DanielDavisDeepDive",
                        "show": "Daniel Davis Deep Dive",
                        "host": "Daniel Davis",
                        "thread": "davis",
                        "file_prefix": "youtube-daniel-davis-deep-dive",
                        "discovery_priority": csa.DISCOVERY_SOURCE_ORDER,
                    },
                    {
                        "channel_key": "dialogue-works",
                        "channel_name": "Dialogue Works",
                        "channel_id": "UCkF-6h_Zgf9zXNUmUB-MzTw",
                        "uploads_playlist_id": "UUkF-6h_Zgf9zXNUmUB-MzTw",
                        "handle_url": "https://www.youtube.com/@dialogueworks01",
                        "show": "Dialogue Works",
                        "host": "Nima Alkhorshid",
                        "thread": "alkorshid",
                        "file_prefix": "transcript-dialogue-works",
                        "discovery_priority": csa.DISCOVERY_SOURCE_ORDER,
                    },
                ]
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = csa.run_audit(
        start=csa._parse_date("2026-05-11"),
        end=csa._parse_date("2026-05-13"),
        recent_start=csa._parse_date("2026-05-12"),
        channel_keys=None,
        out_dir=out_dir,
        notebook_root=notebook,
        fmt="jsonl",
        offline=True,
        receipt_root=tmp_path / "receipts",
        watchlist_path=watchlist,
    )

    ledger_path = Path(result["ledger_paths"]["jsonl"])
    rows = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    by_id = {row["youtube_id"]: row for row in rows}

    assert by_id["M_0XZf3qdQI"]["classification"] == "uncaptured-main"
    assert by_id["F96pMYCZK84"]["classification"] == "uncaptured-main"
    assert by_id["ntHXdIvOcIk"]["classification"] == "uncaptured-main"
    assert by_id["S3bPrYf1w40"]["classification"] == "hidden-short"
    assert by_id["8mMvRD0bYb8"]["classification"] == "hidden-short"
    assert by_id["WmG-x4BFd00"]["classification"] == "hidden-short"
    assert by_id["22cOVLIatOw"]["classification"] == "hidden-companion"
    assert by_id["22cOVLIatOw"]["captured"] == 1
    assert by_id["tfgfSubAEJM"]["classification"] == "hidden-companion"
    assert by_id["klvztvA37b8"]["classification"] == "hidden-companion"
    assert by_id["vmCvNogL8PU"]["classification"] == "uncaptured-main"
    assert by_id["Uhgd6vRsPxA"]["classification"] == "uncaptured-main"
    assert by_id["rTmm2b60yNM"]["classification"] == "uncaptured-main"
    assert by_id["QCUzMPfGuZY"]["classification"] == "upcoming"
    assert by_id["YKvzjkOfyWQ"]["classification"] == "captured-main"
    assert by_id["D8WeTG3rAFs"]["classification"] == "captured-main"
    assert by_id["Z1TQNvoUhTk"]["classification"] == "hidden-short"

    summary = result["summary"]
    assert summary["main_total"] == 8
    assert summary["captured_main"] == 2
    assert summary["must_capture_remaining"] == 6
    assert summary["overall_pct"] == 0.25
    assert summary["recent_main_total"] == 8
    assert summary["recent_captured_main"] == 2
    assert summary["status"] == "below-threshold"

    queue = result["queue_groups"]
    assert sorted(row["youtube_id"] for row in queue["must-capture"]) == sorted(
        [
            "vmCvNogL8PU",
            "Uhgd6vRsPxA",
            "rTmm2b60yNM",
            "F96pMYCZK84",
            "M_0XZf3qdQI",
            "ntHXdIvOcIk",
        ]
    )
    assert queue["probably-capture"] == []
    queue_md = (out_dir / "2026-05-11_to_2026-05-13" / "repair-queue.md").read_text(encoding="utf-8")
    assert "hidden-short" not in queue_md
    assert "hidden-companion" not in queue_md


def test_offline_rerun_is_stable(tmp_path: Path) -> None:
    receipts = tmp_path / "receipts" / "2026-05-12_to_2026-05-12"
    notebook = tmp_path / "codex" / "2026"
    watchlist = tmp_path / "watchlist.json"
    out_a = tmp_path / "out-a"
    out_b = tmp_path / "out-b"

    receipts.mkdir(parents=True)
    (receipts / "glenn-diesen.discovery.json").write_text(
        json.dumps(
            _receipt(
                "glenn-diesen",
                "Glenn Diesen",
                [
                    {
                        "id": "YKvzjkOfyWQ",
                        "title": "Chas Freeman: Trump Goes to Beijing After Historic Defeat in Iran",
                        "url": "https://www.youtube.com/watch?v=YKvzjkOfyWQ",
                        "upload_date": "2026-05-12",
                        "date": "2026-05-12",
                        "duration_seconds": 3620,
                        "discovery_source": "uploads_playlist",
                    }
                ],
            ),
            indent=2,
        ),
        encoding="utf-8",
    )
    _write_raw(
        notebook / "raw-input" / "2026-05-12" / "glenn.md",
        source_url="https://www.youtube.com/watch?v=YKvzjkOfyWQ",
    )
    watchlist.write_text(
        json.dumps(
            {
                "channels": [
                    {
                        "channel_key": "glenn-diesen",
                        "channel_name": "Glenn Diesen",
                        "channel_id": "UCZFCDIHTe9HGxtIuVDpBz7g",
                        "uploads_playlist_id": "UUZFCDIHTe9HGxtIuVDpBz7g",
                        "handle_url": "https://www.youtube.com/@GDiesen1",
                        "show": "Glenn Diesen",
                        "host": "Glenn Diesen",
                        "thread": "diesen",
                        "file_prefix": "youtube-glenn-diesen",
                        "discovery_priority": csa.DISCOVERY_SOURCE_ORDER,
                    }
                ]
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result_a = csa.run_audit(
        start=csa._parse_date("2026-05-12"),
        end=csa._parse_date("2026-05-12"),
        recent_start=csa._parse_date("2026-05-12"),
        channel_keys=None,
        out_dir=out_a,
        notebook_root=notebook,
        fmt="jsonl",
        offline=True,
        receipt_root=tmp_path / "receipts",
        watchlist_path=watchlist,
    )
    result_b = csa.run_audit(
        start=csa._parse_date("2026-05-12"),
        end=csa._parse_date("2026-05-12"),
        recent_start=csa._parse_date("2026-05-12"),
        channel_keys=None,
        out_dir=out_b,
        notebook_root=notebook,
        fmt="jsonl",
        offline=True,
        receipt_root=tmp_path / "receipts",
        watchlist_path=watchlist,
    )

    assert result_a["summary"] == result_b["summary"]
    assert result_a["queue_groups"] == result_b["queue_groups"]


def test_fetch_metadata_falls_back_to_module(monkeypatch) -> None:
    calls: list[str] = []

    def fake_import(video_id: str, *, max_attempts=4):
        calls.append("import")
        raise RuntimeError("import mode unavailable")

    def fake_fetch(video_id: str, *, mode: str = "binary", cwd=None, python_cmd=None):
        calls.append(mode)
        if mode == "binary":
            raise RuntimeError("yt-dlp executable not found")
        return {
            "title": "Example title",
            "upload_date": "20260412",
            "duration": 1234,
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
            "live_status": "",
        }

    monkeypatch.setattr(csa, "fetch_video_metadata_import", fake_import)
    monkeypatch.setattr(csa, "fetch_video_metadata_subprocess", fake_fetch)
    row = csa._fetch_metadata("abc123def45")

    assert calls == ["import", "binary", "module"]
    assert row["upload_date"] == "2026-04-12"
    assert row["duration_seconds"] == 1234
    assert row["url"] == "https://www.youtube.com/watch?v=abc123def45"
