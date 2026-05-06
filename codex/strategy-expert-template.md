# Strategy cognition stream templates (WORK only)
<!-- word_count: concise bundle -->

**Single source** for the six on-disk surfaces each cognition-stream routing handle uses:
profile, thread, transcript, codex-page, strategy page, and mind.

**Notebook contract:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md)  
**Thread contract:** [THREAD-CONTRACT.md](THREAD-CONTRACT.md)

**Jump:** [Profile](#profile-template) · [Thread](#thread-template) · [Transcript](#transcript-template) · [codex-page](#codex-page-template) · [Strategy page](#strategy-page-template) · [Mind](#mind-template)

---

<a id="profile-template"></a>

## Profile -> `strategy-expert-<expert_id>.md`

# Strategy cognition stream profile - <Stream / full name> (`<expert_id>`)

WORK only; not Record.

This section is now a compatibility redirect.

**Canonical scaffold:** [strategy-codex-template-profile.md](strategy-codex-template-profile.md)

Use the canonical profile template for the actual profile shape, including:

- `## Introduction`
- `## Identity`
- `## Links`
- optional downstream voice, automation, ledger, and seed sections

Profiles are durable lane surfaces, not year-volume artifacts. Teach the canonical profile as year-independent even if some live files still exist under `2026/<channel>/` during migration.

Companion files: thread, transcript, codex-page, strategy page, mind.

---

<a id="thread-template"></a>

## Thread -> `experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`

# Cognition stream thread handle - `<expert_id>`

WORK only; not Record.

The thread file is the month-bounded continuity surface for a cognition stream. It keeps:

- the narrative journal for the month
- the page index for that month
- the machine extraction block

**Thread contract:** [THREAD-CONTRACT.md](THREAD-CONTRACT.md)

**Core rules:**

- Compose the month from that month's `strategy-page` set.
- Keep the journal above the machine block.
- Keep one file per month when possible; legacy `thread.md` only while migrating.
- Use `thread-page` links to track continuity, not to duplicate page prose.

Companion files: profile, transcript, mind, and page surfaces.

---

### Thread-embedded `strategy-page` blocks

Use the `strategy-page` fence in the monthly thread file for the month's main analytical pages. The canonical scaffold for the fence is the `Strategy page` section below.

Machine extraction lives between the `<!-- strategy-expert-thread:start -->` and `<!-- strategy-expert-thread:end -->` comments.

---

<a id="transcript-template"></a>

## Transcript -> `experts/<expert_id>/transcript.md`

# Cognition stream transcript - `<expert_id>`

WORK only; not Record.

The transcript is the 7-day rolling triage sink, not the long-form SSOT.
It may contain:

- one-line `thread:` registry entries
- short continuation paragraphs
- pointers to `raw-input/`

When the full capture already lives in `raw-input/`, the transcript can stay empty or pointer-only.

Companion files: profile, thread, mind, and codex-pages.

---

<a id="codex-page-template"></a>

## codex-page -> `codex/<year>/<channel>/<expert_id>-page-YYYY-MM-DD.md`

# Cognition stream codex-page - `<expert_id>`

WORK only; not Record.

This section is now a compatibility redirect.

**Canonical scaffold:** [strategy-codex-template-page.md#codex-page---codexyearchannelexpert_id-page-yyyy-mm-ddmd](strategy-codex-template-page.md#codex-page---codexyearchannelexpert_id-page-yyyy-mm-ddmd)

Use the canonical page template for the actual codex-page shape.

---

<a id="strategy-page-template"></a>

## Strategy page -> thread-fence page

# Cognition stream strategy page - `<expert_id>`

WORK only; not Record.

This section is now a compatibility redirect.

**Canonical scaffold:** [strategy-codex-template-page.md#strategy-page---thread-fence-page](strategy-codex-template-page.md#strategy-page---thread-fence-page)

Use the canonical page template for the actual strategy-page fence shape.

---

<a id="mind-template"></a>

## Mind -> `strategy-expert-<expert_id>-mind.md`

# Cognition stream mind - `<expert_id>`

WORK only; not Record.

The mind file is the long-form voice fingerprint / style map. Keep it separate from the transcript and the thread.

**Use it for:**

- longer register notes
- transcript-derived style fingerprints
- durable voice patterns

**Do not use it for:**

- literal transcript replacement
- page prose
- thread prose

Companion files: profile, thread, transcript, and page surfaces.
