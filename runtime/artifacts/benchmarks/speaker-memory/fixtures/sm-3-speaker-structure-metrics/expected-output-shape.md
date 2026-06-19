# SM-3 Expected Output Shape

A strong answer should produce:

- a named target speaker
- a visible four-part score vector:
  - `density`
  - `completeness`
  - `coherence`
  - `maturity`
- an optional composite placed after the vector
- an evidence section with concrete support such as:
  - host lane count
  - materialized transcript count or evidence count
  - host-local arc count
  - helix or cross-host note presence
  - cross-year continuity note
  - watch URL coverage state
- a short note on the main limiting factor

Weak answers:

- treat volume as maturity
- skip completeness gaps
- collapse all judgment into one adjective
- overstate a shelf as a mature helix without evidence
