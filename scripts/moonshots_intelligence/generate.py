"""LLM-assisted document generation from evidence blocks."""

from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from moonshots_intelligence import MIN_BULLETS_STRICT, PROMPT_ID
from moonshots_intelligence.evidence import EvidenceBlock

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "dual_layer_v1.md"

def prompt_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def load_prompt_template() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")

def build_prompt(evidence_blocks: list[EvidenceBlock], *, min_bullets: int) -> str:
    template = load_prompt_template()
    payload = [
        {
            "evidence_id": block.evidence_id,
            "text": block.text,
            "source_location": block.source_location,
            "word_count": block.word_count,
        }
        for block in evidence_blocks
    ]
    return (
        template.replace("{{min_bullets}}", str(min_bullets))
        .replace("{{evidence_json}}", json.dumps(payload, indent=2, ensure_ascii=False))
    )

def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            text = text[start : end + 1]
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("LLM response is not a JSON object")
    return data

def call_openai_json(prompt: str, *, model: str | None = None) -> tuple[dict[str, Any], str]:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set; use --bullets-json or set API key")
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are an epistemic compiler. Output only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {detail}") from exc
    content = body["choices"][0]["message"]["content"]
    return _extract_json_object(content), model_name

def load_bullets_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("--bullets-json must be a JSON object")
    return data

def generate_document(
    evidence_blocks: list[EvidenceBlock],
    *,
    bullets_json_path: Path | None = None,
    model: str | None = None,
    min_bullets: int = MIN_BULLETS_STRICT,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if bullets_json_path is not None:
        doc = load_bullets_json(bullets_json_path)
        receipt = {
            "prompt_id": PROMPT_ID,
            "prompt_hash": None,
            "model": "bullets-json",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        return doc, receipt

    prompt = build_prompt(evidence_blocks, min_bullets=min_bullets)
    phash = prompt_hash(prompt)
    doc, model_name = call_openai_json(prompt, model=model)
    receipt = {
        "prompt_id": PROMPT_ID,
        "prompt_hash": phash,
        "model": model_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    return doc, receipt
