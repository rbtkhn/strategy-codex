"""Epistemic plugin layer — bounded extension around frozen core."""

from prediction.plugins.base import EpistemicPlugin, MAX_PLUGIN_INFLUENCE
from prediction.plugins.registry import load_plugins

__all__ = ["EpistemicPlugin", "MAX_PLUGIN_INFLUENCE", "load_plugins"]
