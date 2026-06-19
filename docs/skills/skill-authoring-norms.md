# Skill authoring — agent behavior norms

**Purpose:** Optional **social contract** text for **agent-facing** portable skills — not a substitute for [skills/_schema.md](../../skills/_schema.md) (frontmatter, portable vs appendix).

**When to add:** Skills that drive tools, staging, or communication with maintainers (e.g. feedback prompts, harness rituals). Skip for purely mechanical skills if norms add no signal.

---

## Where norms live

| Content | Location |
|---------|----------|
| **Vendor-neutral** defaults (brevity, respect user-owned text, abstain when uncertain) | Portable **`SKILL.md` body** — optional `## Agent behavior norms` |
| **Grace-Mar paths, merge scripts, instance policy** | `.cursor/skills/<skill>/CURSOR_APPENDIX.md` only |

Forbidden substrings in the portable **core** still apply ([manifest](../../skills/manifest.yaml) `verify_forbidden_substrings`).

---

## Minimal paste-in example

Use under `## Agent behavior norms` in a new portable core:

```markdown
## Agent behavior norms

- **Human authority** — Assist; do not overwrite companion-owned or user-owned text without explicit consent.
- **Brevity** — Default to short outputs unless the operator asks for depth.
- **Abstention** — When upstream docs already answer a claim, do not invent gaps.
- **Leakage** — Do not tie external projects to private instance names unless the operator asks.
```

Tune bullets per skill; keep the block **short**.

---

## See also

- [skills/_schema.md](../../skills/_schema.md) — schema and optional norms heading  
- [trust-layers.md](../trust-layers.md) — reliability vs adversarial trust for tools  
- [skills/README.md](../../skills/README.md) — portable ladder and sync
