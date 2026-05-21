# Presentation Packet Examples

These examples make the `family + subsurface + intent` taxonomy concrete.

- `ph-mus-gt16.packet.json`: public museum packet for the `ph-civ` family
- `ce-mus-hormuz.packet.json`: WORK-safe museum packet for the `civ-emp` family

Use them to sanity-check packet shape, adapter expectations, and the product story:

- `ph-mus` turns public exhibit routes into reader-facing museum decks
- `ce-mus` turns strategic object sequences into operator-facing exhibit decks

Example bundle commands:

```bash
python scripts/build_ph_civ_presentation_bundle.py \
  --subsurface ph-mus \
  --intent lesson \
  --title "GT-16 Museum Lesson" \
  --audience Readers \
  --packet-json artifacts/presentations/examples/ph-mus-gt16.packet.json \
  --output artifacts/presentations/examples/ph-mus-gt16.bundle.json
```

```bash
python scripts/build_civ_emp_presentation_bundle.py \
  --subsurface ce-mus \
  --intent summary \
  --title "Hormuz Exhibit Summary" \
  --audience Operators \
  --packet-json artifacts/presentations/examples/ce-mus-hormuz.packet.json \
  --output artifacts/presentations/examples/ce-mus-hormuz.bundle.json
```
