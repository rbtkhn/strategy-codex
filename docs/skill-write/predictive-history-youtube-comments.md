# Predictive History YouTube comments

**Purpose:** Shape Predictive History YouTube comments for trust-first influence. The comment should feel like a useful companion to the lecture, not a hijack of the thread or a growth-hack pitch.

## Wave One Pilot Exception

For the local `civ-01` to `civ-06` pilot, use a different profile.

That wave is a **statecraft proof-object pilot**, not a chapter-doorway campaign. Its purpose is to publicly demonstrate unusually strong civilizational analysis in one compressed paragraph. For that pilot:

- no repo link
- no paste-into-LLM instruction
- no `ph-civ` signature requirement
- each comment must contain **at least two concrete historical examples**
- each example must help reason toward the thesis, not just decorate it
- each comment should sound compressed, formidable, and human

Repo-local skill for this mode: [`.cursor/skills/ph-civ-comment-proof-objects/SKILL.md`](../../.cursor/skills/ph-civ-comment-proof-objects/SKILL.md)

Treat the older doorway profile below as the default general rollout unless the operator explicitly invokes the Wave One proof-object pilot.

## Preference profile

- **Primary audience:** curious lurkers who might use a concrete reader packet.
- **Posture:** helpful artifact, not self-promotion.
- **Conversion action:** paste the GitHub chapter-folder link into an LLM chat.
- **Hook strength:** quietly useful and grounded in the lecture.
- **Cadence:** one tailored top-level comment per video.
- **Project identity:** light `ph-civ` signature, not heavy branding.
- **Primary win:** quality readers who open the repo and study.
- **Risk boundary:** avoid hype, spam, overclaiming, or repeated boilerplate.
- **Template style:** stable skeleton with a video-specific first sentence and prompt.

## Comment shape

Use this repeatable structure:

1. A video-specific first sentence naming what the lecture is doing.
2. One sentence offering the public reader packet.
3. The exact GitHub chapter-folder link.
4. One sentence telling readers to paste the link into ChatGPT, Claude, or Grok and ask for a guided study path.
5. A light signature: "part of ph-civ, a public LLM-native Predictive History reader."

## Rollout scope

The full public rollout uses **Phase 1 only**: the chapter-folder doorway comment described above.

The retired `ph-mus` exhibit follow-up phase was removed from the mirror vision. Do not invent museum or exhibit links.

## Drafting rules

- The first sentence should be about the lecture, not the repo.
- Make the link useful before making the project memorable.
- Keep the tone quiet, concrete, and generous.
- Use one tailored top-level comment per video unless the operator asks for a reply strategy.
- Vary the video-specific sentence and prompt; do not reuse identical comments across videos.
- Do not use urgency, growth-hack language, or inflated claims such as "must read," "ultimate guide," or "this changes everything."
- Do not imply transcript fidelity, commentary depth, or scholarly review is complete when the chapter is provisional.
- For `gt-23` through `gt-26`, use source-first language until transcript fidelity and claims have been reviewed.
- For application or live-crisis chapters, preserve the guardrail: public orientation and study only, not live operational analysis.

For the `civ-01` to `civ-06` Wave One pilot, replace the default shape with this compressed proof-object structure:

1. State the lecture's governing inversion.
2. Name at least two concrete historical examples.
3. Show why those examples support the lecture thesis, then compress them into one higher-order civilizational claim.

Do not let the evidence turn into a mini-essay. The point is density, not exhaustiveness.

## Folder readiness

Do not draft a comment around a chapter-folder link until the folder has enough local context for a curious reader or LLM:

- `README.md`
- transcript
- commentary canvas
- orientation/card link
- review status
- suggested LLM prompt

If a folder is provisional, say so plainly in the comment or prompt. A provisional packet can still be useful, but it should not masquerade as a finished edition.

## Draft storage boundary

Store rollout drafts only inside `strategy-codex`, not in the public `ph-civ` repo.

- canonical workflow state belongs in the local rollout queue
- readable local review copies may be rendered as Markdown under the rollout folder
- `ph-civ` remains the source of packet URLs, readiness context, and public study materials
- posted YouTube comments are public outputs; the drafting workspace remains local

## Example skeleton

```text
This lecture is doing [video-specific thing], and I made a public reader packet for following it without losing the thread.

[exact GitHub chapter-folder URL]

Paste the folder link into ChatGPT, Claude, or Grok and ask it to guide you through the chapter using the transcript, commentary canvas, and guardrails. It is part of ph-civ, a public LLM-native Predictive History reader.
```

## Acceptance checks

- A reader can understand the value of the link without knowing `ph-civ`.
- The comment feels like a companion to the lecture, not a takeover of the thread.
- The action is clear: paste the folder URL into an LLM and ask for a guided study path.
- The `ph-civ` identity is memorable but secondary to immediate chapter usefulness.
