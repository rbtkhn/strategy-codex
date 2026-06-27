# speaker-routing (terminated output root)

Historical voice-routing queue artifacts live here from runs before the 2026-06 rename.

**New runs:** [`../voice-routing/`](../voice-routing/) — `voice-routing-queue.jsonl` / `voice-routing-queue.md`.

**Script:** `python scripts/build_voice_routing_queue.py` (deprecated shim: `build_speaker_routing_queue.py`).

Legacy JSONL rows may use `existing-speaker-*` route types; loaders normalize to `existing-voice-*`.
