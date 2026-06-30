# Predictive History Education — Strategic Plan

WORK only; not Record.

**Scope:** `singularity/education/predictive-history/` and loop cluster `predictive-history-*`.

**One-line strategy:** Predictive History becomes a source-grounded education media engine — each historical prediction case becomes a lesson, each lesson becomes a media pack, each media pack passes a quality gate, and each published artifact feeds learner feedback back into the curriculum.

---

## Executive thesis

The project is a **lecture-first, media-assisted curriculum factory** — not an AI video channel.

```text
source lecture / chapter
  → lesson brief
  → worksheet / quiz
  → visual map
  → narration script
  → storyboard
  → AI-assisted media pack
  → reviewed video / interactive lesson
  → distribution package
  → learner feedback
  → improved lesson
```

Build a **modular instructional pipeline** now so future video, avatar, voice, translation, and interactivity tools can swap in without changing curriculum architecture.

---

## Method spine (prediction literacy)

The corpus teaches a method, not only history:

```text
historical case → forecast / expectation → evidence → outcome → evaluation → lesson about judgment
```

Each unit exercises: source reading, causal reasoning, probability thinking, narrative comparison, prediction evaluation, historical humility, retrospective bias detection.

---

## Pedagogical spine (every lesson)

1. Hook question
2. Historical setup
3. Prediction problem
4. Evidence packet
5. Competing interpretations
6. Outcome
7. Evaluation
8. Transfer lesson
9. Retrieval quiz
10. Reflection prompt

Media must serve this spine. Decorative AI clips that do not clarify prediction, evidence, causality, or outcome are rejected.

Template: [`lessons/lesson-template.md`](lessons/lesson-template.md)

---

## Loop cluster

| Loop | Role |
| --- | --- |
| `predictive-history-education` | Umbrella — source intake, lecture/chapter selection |
| `predictive-history-lesson-pipeline` | Lesson brief, worksheet, quiz, source packet |
| `predictive-history-media-pack` | Slides, storyboard, narration, AI-assisted visuals |
| `predictive-history-media-quality-gate` | Factual, pedagogy, rights review — anti-slop gate |
| `predictive-history-distribution-pack` | YouTube, Shorts, Substack, podcast packaging |
| `predictive-history-learner-feedback-review` | Monthly revision queue from learner data |

See [`README.md`](README.md) for hard/soft dependency graph.

---

## Asset classes (not one video vendor)

| Asset | Tool class | Notes |
| --- | --- | --- |
| Lesson brief | LLM / repo-aware assistant | Must cite source lecture/chapter |
| Slide deck | NotebookLM / LLM / presentation | Human review required |
| Diagrams / maps | image model + manual correction | Avoid fake geography |
| Short B-roll | Veo / Runway / Firefly | Atmosphere, not evidence |
| Talking-head explainer | Synthesia / HeyGen | Scale; can feel generic |
| Voiceover | ElevenLabs / similar | Consistent voice; rights clarity |
| Interactive tutor | RAG + LLM | High future value |
| Full video | edited composite | Assembled, not single-prompt |

**Do not depend on Sora** as operational substrate (platform discontinued).

Tool notes: [`tool-notes/`](tool-notes/README.md)

---

## Layer separation

Keep artifacts separate until final composite:

```text
lesson_script.md
narration_script.md
voiceover.wav
captions.srt
slide_deck.pdf
video_edit.mp4
```

Enables correction, translation, audio-only versions, short clips, and updates without full rebuild.

---

## Distribution model

```text
Canonical lesson: YouTube long-form + repo/website archive
Discovery: Shorts / TikTok / Reels (3–5 clips per lesson)
Relationship: Substack / email (source packet, worksheet, quiz)
Depth: source packet + worksheet + quiz
Audio: podcast feed from long lesson
Productization: course bundle (after 10–20 lessons)
```

Long-form segments: aim **6–9 minutes** per segment where possible (MOOC retention research).

---

## Risk register

| Risk | Mitigation |
| --- | --- |
| AI slop | No video without lesson script; no publish without factual review |
| Historical hallucination | AI visuals as illustrations; label reconstructions; prefer maps/timelines |
| Copyright / likeness | Commercial-safety tool notes per asset; avoid unclear likeness |
| Bias / representation | Bias review; prefer diagrams over personification |
| Vendor instability | Store scripts, prompts, sources, captions separately; tool-agnostic templates |

Gate template: [`media-review/media-quality-gate-template.md`](media-review/media-quality-gate-template.md)

---

## 90-day operating plan

### Month 1 — First lesson pipeline

Select one lecture/chapter → lesson brief, worksheet, quiz, visual map, narration script, media pack → quality gate → publish or hold.

Output: `lessons/lesson-001/` (operator-created)

### Month 2 — First distribution package

YouTube long-form, 3–5 Shorts, Substack post, podcast/audio, archived metadata.

Output: `distribution/lesson-001/`

### Month 3 — Repeatability

Lessons 002–003; compare production time; first feedback review.

Output: `feedback/2026-09.md`

---

## Weekly scorecard

| Metric | Target | Why |
| --- | ---: | --- |
| Lessons in pipeline | 1–3 | Throughput |
| Approved lesson packages | 1/month initially | Quality over volume |
| Media assets rejected | Track | Anti-slop gate signal |
| Quizzes per lesson | 1 | Retrieval practice |
| Source packets per lesson | 1 | Factual grounding |
| Long-form videos published | 1/month initially | Canonical public asset |
| Shorts per lesson | 3–5 | Discovery |
| Substack posts per lesson | 1 | Relationship/archive |
| Learner questions captured | Monthly | Feedback loop |
| Revisions queued | Monthly | Improvement signal |

---

## Upstream sources (read only)

- Canonical: [rbtkhn/predictive-history](https://github.com/rbtkhn/predictive-history)
- In-repo mirror: [`continuity/predictive-history/`](../../../continuity/predictive-history/README.md)

Corpus edits stay in the canonical clone; this shelf holds learner-facing artifacts only.

---

## Related external pattern — Jiang Lens

[Jiang Lens](https://github.com/apresmoi/jianglens) is a useful external reference for source-grounded interpretive compression. It is an agentic research organization built around a dense, contested interpretive corpus, where agents ingest sources, produce source-linked episode reads, validate claims, and maintain public lens pages with provenance.

Predictive History can adapt the pattern without treating Jiang Lens as canonical source material:

```text
Jiang Lens:
source corpus → episode read → lens page → public site → agent-readable artifact

Predictive History:
source lecture/chapter → lesson brief → source packet → media pack → quality gate → distribution package
```

Boundary: Jiang Lens is an external implementation reference, not an official Predictive History source or part of this repo's source of truth. Expanded pattern notes: [`tool-notes/related-projects.md`](tool-notes/related-projects.md).
