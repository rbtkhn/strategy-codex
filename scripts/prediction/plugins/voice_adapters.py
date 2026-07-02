"""Voice adapter plugins — annotate without touching core inference."""

from __future__ import annotations

from typing import Any

from prediction.plugins.base import EpistemicPlugin

VOICE_PROFILES: dict[str, str] = {
    "mearsheimer": "structural_realist",
    "mercouris": "civilizational_analyst",
    "freeman": "diplomatic_realist",
    "macgregor": "military_operational",
}

class MearsheimerAdapter(EpistemicPlugin):
    """Stub voice adapter — maps known voices to profile annotations."""

    def name(self) -> str:
        return "mearsheimer_adapter_v0"

    def version(self) -> str:
        return "0.1.0"

    def plugin_type(self) -> str:
        return "voice"

    def apply(self, core_input: dict[str, Any]) -> dict[str, Any]:
        voice = str(core_input.get("voice") or "").lower()
        profile = VOICE_PROFILES.get(voice, "generalist")
        if voice == "mearsheimer":
            profile = "structural_realist"
        return {
            "plugin_name": self.name(),
            "modifications": {
                "signals": {},
                "regime_adjustments": {},
                "annotations": {"voice_profile": profile},
            },
            "confidence": 0.15,
        }
