# strategy-codex-template-profile
<!-- word_count: concise scaffold -->


Use the profile as the compact channel index for one of the main strategy-codex lanes. A profile should orient a reader quickly: who this person or channel is, why the lane matters, and where its public output lives.

**Canonical role:**

- compact orientation for the lane
- stable identity and routing handle
- durable library-facing link hub for public source surfaces
- companion surface for thread, transcript, codex-page, strategy-page, and mind work

**Canonical location:**

- `codex/profiles/<channel>-profile.md`

Profiles are year-independent lane identity surfaces. They should not be taught as volume-bound artifacts even if some current live files still sit under year folders during migration.

**Minimal shape:**

```md
# Strategy expert - <Full name> (`<expert_id>`)


**Canonical index:** ...

---

## Introduction

Short orienting paragraph covering:
- who this person/channel is
- what kind of analysis or hosting role they provide
- why the lane matters in strategy-codex

## Identity

| Field | Value |
|-------|-------|
| **Name** | ... |
| **expert_id** | `...` |
| **Role** | ... |
| **Default grep tags** | ... |
| **Typical pairings** | ... |
| **Notebook-use tags** | ... |

## Links

### Social media

- X / YouTube / other social surfaces that are active source channels

### Substack

- active Substack URL when present
- if none is currently tracked, say so explicitly

### Other links

- main site
- institution / faculty / organization page
- podcast / publisher / archive links
- other stable public source surfaces worth citing
```

**Authoring rules:**

- `## Introduction` should be short and orienting, not a full biographical essay.
- `## Links` is a public-source hub, not a bibliography dump.
- Keep `### Social media`, `### Substack`, and `### Other links` explicit so operators can find source surfaces quickly.
- If no Substack is currently tracked, write `- None currently tracked.` rather than omitting the subsection.
- Richer sections such as **Voice pattern**, **Bias pattern**, **Style markers**, optional **Disposition**, convergence, tension, automation, ledgers, or seed mirrors may follow below the canonical profile scaffold.

**Companion surfaces:**

- thread
- transcript
- codex-page
- strategy-page
- mind
