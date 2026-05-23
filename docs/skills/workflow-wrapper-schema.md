# Workflow Wrapper Schema

**Purpose:** Standardize the short human-readable wrappers used to explain a governed skill or WORK workflow without replacing its canonical method.

Wrappers are a discovery and onboarding layer. They are not the source of truth for methodology, policy, or automation behavior.

## Canonical sections

Use these headings in wrapper pages when practical:

1. **Purpose**
2. **When to use**
3. **Inputs you'll need**
4. **What happens**
5. **What you get**
6. **Boundary**
7. **Related surfaces**

Compact pages may rename **Purpose** to **What this is** when the audience is beginner-heavy, but the meaning should stay the same.

## Rules

- A wrapper explains a workflow; it does not replace the canonical source surface.
- Every wrapper must point back to its authoritative source file, skill, or lane document.
- Wrappers must stay ASCII and operator-first.
- Wrappers must not imply silent merge, silent posting, or automatic authority.
- If a workflow has a public layer and a private layer, the wrapper must preserve that distinction.
- If the authoritative source changes, update the wrapper or remove it; do not let it drift into a parallel method.

## Status language

When a wrapper describes a skill, use one of these status tags:

- **draft** - lives under `skills-portable/_drafts/`
- **listed** - manifest-listed portable skill
- **promoted** - actively used, manifest-listed skill with a stable generated runtime copy

Use the narrowest honest label. If in doubt, prefer `listed` over `promoted`.

## Recommended note

Add one short note near the top or bottom:

`This wrapper is derivative. Canonical method lives in: <path>.`

That keeps the discovery layer useful without turning it into a second doctrine source.
