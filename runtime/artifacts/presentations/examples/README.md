# Presentation Packet Examples

These examples make the `family + subsurface + intent` taxonomy concrete.

- `ce-mus-hormuz.packet.json`: WORK-safe museum packet for the `civ-emp` family
- `ph-mus-gt16.packet.json`: **legacy** public museum packet (retired subsurface; kept for archaeology)

Use them to sanity-check packet shape, adapter expectations, and the product story:

- `ce-mus` turns strategic object sequences into operator-facing exhibit decks
- `ph-mus` adapter support was removed; see [`public/predictive-history/docs/archive/ph-mus-retired.md`](../../../../public/predictive-history/docs/archive/ph-mus-retired.md)

Example bundle command:

```bash
python scripts/build_civ_emp_presentation_bundle.py \
  --subsurface ce-mus \
  --intent summary \
  --title "Hormuz Exhibit Summary" \
  --audience Operators \
  --packet-json runtime/artifacts/presentations/examples/ce-mus-hormuz.packet.json \
  --output runtime/artifacts/presentations/examples/ce-mus-hormuz.bundle.json
```
