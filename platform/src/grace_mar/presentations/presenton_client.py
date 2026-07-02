from __future__ import annotations

import json
import os
import uuid
from typing import Any
from urllib import error, request

class PresentonClientError(RuntimeError):
    """Raised when Presenton generation fails."""

def _encode_multipart(fields: dict[str, str]) -> tuple[bytes, str]:
    boundary = f"----grace-mar-presenton-{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for key, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8")
        )
        chunks.append(str(value).encode("utf-8"))
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), boundary

class PresentonClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("PRESENTON_API_URL", "http://127.0.0.1:5000")).rstrip("/")
        self.api_key = api_key or os.getenv("PRESENTON_AUTH", "").strip()

    def generate_presentation(
        self,
        *,
        content: str,
        template: str,
        n_slides: int,
        language: str = "English",
        export_as: str = "pptx",
    ) -> dict[str, Any]:
        body, boundary = _encode_multipart(
            {
                "content": content,
                "template": template,
                "n_slides": str(n_slides),
                "language": language,
                "export_as": export_as,
            }
        )
        url = f"{self.base_url}/api/v1/ppt/presentation/generate"
        headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = request.Request(url, method="POST", data=body, headers=headers)
        try:
            with request.urlopen(req, timeout=120) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise PresentonClientError(f"Presenton HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise PresentonClientError(f"Presenton unavailable: {exc.reason}") from exc

        for key in ("presentation_id", "path", "edit_path"):
            if key not in payload or not str(payload[key]).strip():
                raise PresentonClientError(f"Presenton response missing {key}")
        return payload
