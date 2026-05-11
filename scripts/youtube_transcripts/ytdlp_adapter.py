from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

try:
    import yt_dlp
except ImportError:
    yt_dlp = None  # type: ignore

from youtube_transcripts.retry import retry_call


class YtDlpError(RuntimeError):
    """Normalized yt-dlp execution error."""


def watch_url(video_id: str) -> str:
    vid = video_id.strip()
    if not vid:
        raise YtDlpError("missing video id")
    return f"https://www.youtube.com/watch?v={vid}"


def normalize_upload_date(raw: str | None) -> str | None:
    text = (raw or "").strip()
    if not text:
        return None
    if re.fullmatch(r"\d{8}", text):
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def compact_upload_date(raw: str | None) -> str:
    normalized = normalize_upload_date(raw)
    if not normalized:
        return (raw or "").strip()
    return normalized.replace("-", "")


def normalize_title(value: object, *, fallback: str = "") -> str:
    text = str(value or "").strip()
    return text or fallback


def normalize_duration_seconds(value: object) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def caption_language_fields(info: dict[str, object], *, limit: int = 40) -> dict[str, list[str]]:
    manual = info.get("subtitles") or {}
    auto = info.get("automatic_captions") or {}
    manual_langs = list(manual.keys()) if isinstance(manual, dict) else []
    auto_langs = list(auto.keys()) if isinstance(auto, dict) else []
    return {
        "caption_manual_langs": manual_langs[:limit],
        "caption_auto_langs": auto_langs[:limit],
    }


def normalize_video_fields(info: dict[str, object], *, fallback_id: str = "") -> dict[str, str]:
    video_id = normalize_title(info.get("id"), fallback=fallback_id)
    duration = normalize_duration_seconds(info.get("duration"))
    raw_url = normalize_title(info.get("webpage_url") or info.get("url"))
    if raw_url and "://" not in raw_url:
        raw_url = ""
    return {
        "id": video_id,
        "title": normalize_title(info.get("title"), fallback=video_id),
        "upload_date": normalize_title(info.get("upload_date")),
        "duration": str(duration) if duration is not None else "",
        "url": raw_url or (watch_url(video_id) if video_id else ""),
    }


def _require_import_mode() -> None:
    if yt_dlp is None:
        raise YtDlpError("yt-dlp not installed")


def _run_import_extract(
    url: str,
    *,
    options: dict[str, Any],
    download: bool,
) -> Any:
    _require_import_mode()
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)
    except Exception as exc:  # pragma: no cover - exercised through callers
        raise YtDlpError(str(exc) or "yt-dlp failed") from exc


def _parse_json_output(stdout: str) -> dict[str, Any]:
    lines = stdout.strip().splitlines()
    payload = lines[-1] if lines else ""
    if not payload.startswith("{"):
        raise YtDlpError("yt-dlp did not return JSON")
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise YtDlpError("yt-dlp returned invalid JSON") from exc
    if not isinstance(data, dict):
        raise YtDlpError("yt-dlp returned non-object JSON")
    return data


def _subprocess_command(
    *args: str,
    mode: str,
    python_cmd: str | None = None,
) -> list[str]:
    if mode == "binary":
        return ["yt-dlp", *args]
    if mode == "module":
        return [python_cmd or sys.executable, "-m", "yt_dlp", *args]
    raise ValueError(f"unsupported yt-dlp mode: {mode}")


def _run_json_subprocess(
    url: str,
    *,
    mode: str,
    args: list[str],
    cwd: Path | None = None,
    python_cmd: str | None = None,
) -> dict[str, Any]:
    cmd = _subprocess_command(*args, url, mode=mode, python_cmd=python_cmd)
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise YtDlpError("yt-dlp executable not found") from exc
    if proc.returncode != 0:
        raise YtDlpError(proc.stderr.strip() or proc.stdout.strip() or "yt-dlp failed")
    return _parse_json_output(proc.stdout)


def get_version(*, mode: str = "binary", python_cmd: str | None = None) -> str:
    cmd = _subprocess_command("--version", mode=mode, python_cmd=python_cmd)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        return "unknown"
    if proc.returncode == 0:
        return proc.stdout.strip() or "unknown"
    return "unknown"


def list_videos_flat(
    url: str,
    *,
    limit: int | None,
    playlist_items: str | None = None,
    stop_before_date: date | None = None,
    max_attempts: int = 4,
) -> list[dict[str, str]]:
    def _extract() -> list[dict[str, str]]:
        opts: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "skip_download": True,
            "ignoreerrors": True,
        }
        if playlist_items:
            opts["playlist_items"] = playlist_items
        if limit is not None and limit > 0:
            opts["playlistend"] = limit
        info = _run_import_extract(url, options=opts, download=False)
        entries = info.get("entries") if isinstance(info, dict) else None
        if entries is None:
            entries = []
        if not entries and isinstance(info, dict) and info.get("id"):
            entries = [info]

        rows: list[dict[str, str]] = []
        cutoff = stop_before_date.isoformat() if stop_before_date else None
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            row = normalize_video_fields(entry)
            if not row["id"]:
                continue
            normalized = normalize_upload_date(row["upload_date"])
            if cutoff and normalized and normalized < cutoff:
                break
            rows.append(row)
        return rows

    return retry_call(_extract, max_attempts=max_attempts)


def list_channel_entries_subprocess(
    channel_url: str,
    *,
    limit: int,
    cwd: Path | None = None,
    python_cmd: str | None = None,
) -> list[dict[str, str]]:
    payload = _run_json_subprocess(
        channel_url,
        mode="module",
        python_cmd=python_cmd,
        cwd=cwd,
        args=[
            "--flat-playlist",
            "--skip-download",
            "--dump-single-json",
            "--playlist-end",
            str(max(1, limit)),
        ],
    )
    entries = payload.get("entries") or []
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        row = normalize_video_fields(entry)
        if not row["id"] or row["id"] in seen:
            continue
        seen.add(row["id"])
        rows.append(row)
    return rows


def fetch_video_metadata_import(video_id: str, *, max_attempts: int = 4) -> dict[str, object]:
    url = watch_url(video_id)

    def _extract() -> dict[str, object]:
        info = _run_import_extract(
            url,
            options={
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "ignoreerrors": False,
            },
            download=False,
        )
        return info if isinstance(info, dict) else {}

    return retry_call(_extract, max_attempts=max_attempts)


def fetch_video_metadata_subprocess(
    url_or_video_id: str,
    *,
    mode: str = "binary",
    cwd: Path | None = None,
    python_cmd: str | None = None,
) -> dict[str, Any]:
    url = url_or_video_id if "://" in url_or_video_id else watch_url(url_or_video_id)
    return _run_json_subprocess(
        url,
        mode=mode,
        cwd=cwd,
        python_cmd=python_cmd,
        args=[
            "--quiet",
            "--no-warnings",
            "--skip-download",
            "--no-write-comments",
            "--dump-single-json",
        ],
    )


def download_subtitles(
    video_id: str,
    languages: list[str],
    *,
    prefer_manual: bool = True,
) -> tuple[str | None, str | None, str | None]:
    url = watch_url(video_id)
    langs = languages[:8] if languages else ["en", "en-US", "zh-Hans", "zh-CN"]

    with TemporaryDirectory(prefix="ytsub_") as tmp:
        tmp_path = Path(tmp)
        opts: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": langs,
            "outtmpl": str(tmp_path / "%(id)s"),
            "ignoreerrors": False,
        }
        _require_import_mode()
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as exc:
            raise YtDlpError(str(exc) or "yt-dlp subtitle download failed") from exc

        all_vtt = sorted(tmp_path.glob("*.vtt"))
        if not all_vtt:
            raise YtDlpError("no vtt subtitle file produced")
        manual_files = [
            path for path in all_vtt if ".auto." not in path.name and "auto-generated" not in path.name.lower()
        ]
        auto_files = [path for path in all_vtt if path not in manual_files]

        if prefer_manual and manual_files:
            chosen = manual_files[0]
            kind = "manual"
        elif auto_files:
            chosen = auto_files[0]
            kind = "auto"
        else:
            chosen = all_vtt[0]
            kind = "manual"

        text = chosen.read_text(encoding="utf-8", errors="replace")
        lang = chosen.stem.replace(video_id, "").strip(".-_") or "unknown"
        return text, kind, lang


def download_audio_wav(video_id: str, out_wav: Path) -> None:
    out_dir = out_wav.parent
    stem = out_wav.stem
    opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / f"{stem}.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "ignoreerrors": False,
    }
    _run_import_extract(watch_url(video_id), options=opts, download=True)
