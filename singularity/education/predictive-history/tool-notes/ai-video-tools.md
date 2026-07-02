# AI video tools — asset-class reference

**SSOT for vendor prose:** [`../STRATEGIC-PLAN.md`](../STRATEGIC-PLAN.md) (asset classes). This note is operational quick-reference only.

---

## Asset-class matrix

| Asset class | Role in PH pipeline | Example tools (replaceable) | Dependency level |
| --- | --- | --- | --- |
| Lesson / script drafting | Source-grounded briefs | LLM + repo context | Low |
| Slide / deck | Structured teaching visuals | NotebookLM, presentation export | Low |
| Diagrams / maps | Evidence, timelines, geography | Image models + manual edit | Medium |
| Short B-roll | Atmosphere, transitions | Veo, Runway, Firefly | Medium |
| Talking-head explainer | Scale narration on camera | Synthesia, HeyGen | Medium |
| Full composite video | Final long-form | Editor + assembled layers | High |

**Do not depend on Sora** — platform discontinued; treat as non-operational.

---

## Selection rules

1. **Evidence visuals** — prefer diagrams, maps, timelines; label reconstructions.
2. **Atmosphere B-roll** — never substitute for sourced evidence.
3. **Store prompts and scripts** in `media-packs/prompts/` separately from rendered video.
4. **Vendor swap** — if a tool changes ToS or quality, replace asset class only; lesson architecture unchanged.

---

## Related

- [`voice-avatar-tools.md`](voice-avatar-tools.md)
- [`rights-and-disclosure.md`](rights-and-disclosure.md)
- [`../media-packs/media-pack-template.md`](../media-packs/media-pack-template.md)
