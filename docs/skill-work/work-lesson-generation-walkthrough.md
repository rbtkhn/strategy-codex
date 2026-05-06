# How Grace-Mar Skill-Work Generates Personalized LLM Lessons for the Human Companion

**Purpose:** Walk through how grace-mar's **skill-work** (together with THINK, SELF, and edge) is used to **generate personalized lesson prompts** that the human companion (operator, parent, caregiver) can paste into any LLM (ChatGPT, Grok, etc.). The LLM acts as tutor; the Record supplies context. Multiple concrete examples show prompt construction and the kind of lessons that result.

**Audience:** Operator, product, or developer who wants to implement or refine a Record-derived lesson prompt generator. See also [alpha-school-reference](work-alpha-school/alpha-school-reference.md) (Â§ Record-driven prompts) and [grace-mar-vs-companion-self-skill-work](../grace-mar-vs-companion-self-skill-work.md).

---

## 0. Ideal UX: one prompt per day

**Target:** The human companion should need to **run only one prompt per day**. One paste into the LLM in the morning (or whenever the learning block starts) carries the full dayâ€™s personalized lesson context. No separate prompts for reading vs math vs WORK; no â€œrun again at noon.â€ One prompt = one dayâ€™s tutor brief.

**Why it matters:** Friction drops (one copy-paste, one chat thread), routine is simple (â€œtodayâ€™s promptâ€), and the LLM has the full dayâ€™s scope in one context so it can pace 3â€“5 activities across the 2-hour design without the human re-pasting.

**How it fits in context:** A single prompt can hold **~1,500â€“3,500 tokens** of Record-derived material (who she is, what she knows, curiosity, THINK/MATH/WORK edge, todayâ€™s goals, rules) and still leave ample context for the whole dayâ€™s conversation. The generator should output **one** prompt that includes:

- Role + who she is (short) + Lexile/voice
- **Todayâ€™s goals:** e.g. one reading at the edge, one math at the edge, one creation/planning (WORK), optional Chinese or second reading â€” all in one â€œtodayâ€ list
- Full edge for THINK, MATH, WORK (concise)
- IX-A/IX-B in **summary form** (e.g. 20â€“40 knowledge areas, 5â€“15 curiosity items as bullets), not the full Record
- 2-hour ceiling and â€œ3â€“5 lessons in this threadâ€; end each activity with a one-line summary for logging
- Optional **Pomodoro-style** pacing (focus interval + breaks inside the 2-hour block): [pomodoro-and-timeboxing](work-dev/pomodoro-and-timeboxing.md)

The generator is **day-scoped**: run once per day, produce one prompt. The human pastes once and runs the whole dayâ€™s lessons in one chat.

**Complexity categories:** This â€œone prompt per dayâ€ target fits **elementary / general education** (Kâ€“8, broad Record, 2-hour block, 3â€“5 mixed activities). **Specialized education** (e.g. high school AP, college-level, vocational, deep single-subject work) often needs **more space per conversation** (see table below): more reference material, denser edge, or longer back-and-forth. For those cases, treat â€œone promptâ€ as **one prompt per subject or per focused block** rather than the whole day in one thread â€” e.g. one prompt for â€œtodayâ€™s math,â€ another for â€œtodayâ€™s chemistry,â€ each with the depth that subject needs. The generator can support tiers: **elementary** = one prompt per day (full scope); **specialized** = one prompt per conversation/session, with more Record excerpt and edge per prompt so the LLM has enough context for that domain. Grace-marâ€™s current instance is elementary-tier; the same Record-driven pattern scales up by increasing context per prompt when the companionâ€™s level or focus demands it.

| Tier | Scope per prompt | Use case |
|------|------------------|----------|
| **Elementary / general** | One prompt = full day (3â€“5 activities, 2-hour block). ~1,500â€“3,500 tokens of Record material. | Kâ€“8, broad Record, mixed reading/math/WORK; grace-mar instance. |
| **Specialized** | One prompt = one subject or one focused session. More Record excerpt and edge per prompt; longer conversations. | High school AP, college-level, vocational, or deep single-subject work. |

For specialized: run the generator **per subject or per block** (e.g. today's math, today's chemistry) so each thread has enough context. The generator can take a **tier** parameter (elementary vs specialized) and adjust prompt length and scope.

---

## 1. End-to-end flow

```
Record (SELF + skill-think + skill-work + edge)
        â†“
  Lesson prompt generator â€” one run per day, one output prompt
        â†“
  Human companion pastes prompt once â†’ ChatGPT / Grok (one thread per day)
        â†“
  LLM delivers 3â€“5 personalized lessons in that thread (2-hour design)
        â†“
  Transcript (optional) â†’ "we did X" or paste â†’ pipeline â†’ skill-think for processing/merge
```

**Formative loop:** After processing "we did X" merges, run the lesson generator again so the next day's prompt reflects the updated Record.

- **Knowledge boundary:** The prompt is built **only** from the Record. The LLM does not write into the Record; evidence of what was done is captured via "we did X" and merged through the gate.
- **skill-workâ€™s role:** WORK supplies **work_goals** (e.g. SAT â‰¥ 1200), **WORK edge** (what to do next in making/planning/creation), **SCHOOL** context (grade), and alignment with the **2-hour design**. THINK and SELF supply knowledge, curiosity, personality, Lexile, and THINK/MATH/CHINESE edge. The **lesson prompt** combines these so the LLM teaches at the edge, in voice, without leaking.

---

## 2. What goes into the lesson prompt (Record-only)

| Source | What to include (examples for grace-mar) |
|--------|----------------------------------------|
| **SELF** | Identity (name, age, languages); IX-A knowledge samples; IX-B curiosity; IX-C personality; **Lexile** (input 400â€“500L, output 600L); verbal habits; values. |
| **skill-think** | THINK edge ("longer independent text; early chapter books; inference questions; retelling with explicit sentence structure"); **SAT readiness** block (general principles, EBRW trajectory, next milestones); MATH edge ("telling time; place value; double-digit operations"); CHINESE edge ("first character recognition"). |
| **skill-work** | **work_goals** (horizon: SAT â‰¥ 1200); **WORK edge** (narrative creation from prompts; planning/execution; next steps); **SCHOOL** (first grade); optional companion_creative_context. |
| **Design** | 2-hour ceiling for screen-based learning (from alpha-school); 3â€“5 lessons per block; mastery at edge, no content outside Record. |

The **generator** (script or manual) reads these files, extracts the relevant sections, and fills a **minimal prompt shape** (see Â§3). skill-work contributes the **goals and WORK edge** so that (a) THINK-focused lessons align with SAT trajectory and (b) WORK-focused lessons (making, planning, creation) sit at the companionâ€™s edge.

---

## 2a. How work-human-teacher uses self-knowledge, self-curiosity, and self-personality

**work-human-teacher** is a tool designed to provide **personalized education for Grace-Mar's human companion** â€” the companion whose Record it is, and their family/caregiver. The pattern (companion-self template: human augments the system by reading skill-think and modulating focus and gate) treats the three SELF dimensions as direct inputs to lesson generation and shaping. When a **human teacher** follows that pattern, or when a **Record-derived lesson prompt** encodes the same logic for an LLM, hereâ€™s how each dimension is used.

| Dimension | Role in lesson generation |
|-----------|---------------------------|
| **self-knowledge** (IX-A) | **Content boundary and hints.** What the companion already knows defines (1) what the tutor can safely assume and build on, (2) what counts as â€œat the edgeâ€ (not yet known), and (3) what to use as hints when theyâ€™re stuck (â€œfrom the Recordâ€). Lesson prompts include an IX-A summary so the LLM only uses documented knowledge and doesnâ€™t introduce facts outside the Record. Human teacher: when suggesting focus or gating THINK candidates, they avoid content that conflicts with or far exceeds IX-A. |
| **self-curiosity** (IX-B) | **Topic and interest selection.** What the companion is curious about prioritizes which subjects and angles to use in reading, discussion, and creation. Lesson prompts include an IX-B bullet list so the LLM leans into documented interests (e.g. space, ballet, animals) and can hook motivation. Human teacher: when shaping â€œwhat to work on today,â€ they use IX-B to pick topics that hold attention and to avoid pushing content the companion has no interest in. |
| **self-personality** (IX-C) | **Tone, respect, and constraints.** How the companion processes and expresses (values, linguistic style, behavioral traits) shapes how the tutor should speak and what not to push. Lesson prompts include IX-C (or a short â€œwho she isâ€ summary that draws on it) so the LLM respects identityâ€”e.g. values like kindness and bravery, preferred tone, and â€œdonâ€™t push content that conflicts with the Record.â€ Human teacher: â€œRespect SELF and IX-C when suggesting or gating; donâ€™t push content that conflicts with the Recordâ€ (human-teacher objectives). IX-C also informs **voice** (Lexile, sentence patterns) so lessons feel in-character. |

**In practice:** The lesson promptâ€™s â€œWhat she knows (IX-A)â€ and â€œWhat sheâ€™s curious about (IX-B)â€ sections are the **content and interest** inputs; the â€œWho she isâ€ and rules (e.g. â€œDo not add facts not listed above,â€ â€œrespect her levelâ€) are the **personality and boundary** inputs derived from IX-C and the knowledge boundary. Together they ensure lessons are personalized (knowledge and curiosity) and respectful (personality and identity), whether the â€œtutorâ€ is a human following work-human-teacher objectives or an LLM following a Record-derived prompt. Template: companion-self [work-human-teacher](https://github.com/rbtkhn/companion-self/tree/main/docs/skill-work/skill-work-human-teacher) (human-teacher-objectives: read skill-think, modulate focus and gate, respect identity).

**IX-A scope:** IX-A applies to THINK and WRITE content (reading, comprehension, production). It does **not** limit skill-work capabilities. WORK (making, planning, execution) is an instrument that grows with technology; its capabilities are not bounded by IX-A. When a lesson includes WORK activities, the WORK edge and goals come from the BUILD container; IX-A constrains only the content dimensions of the lesson (e.g. what the tutor assumes for context), not what WORK can propose.

**Recursion with work-alpha-school:** Human-teacher can utilize alpha-school's insights and methods (2-hour design, block composition, mastery thresholds, academic-literature mappings) to shape lessons. Alpha-school can observe human-teacher's practice for feedback: evidence in the Record ("we did X," edge, retention) reflects what happens when those methods are applied, and that evidence can inform how benchmarks and design principles are interpreted or refined. The Record is the shared medium â€” alpha-school learns from how the Record evolves when human-teacher applies its methods; alpha-school does not write into the Record directly. See [alpha-school-reference](work-alpha-school/alpha-school-reference.md) (Â§ Recursion with work-human-teacher).

---

## 3. Minimal prompt shape (for the human to paste)

**One prompt = whole day.** The human pastes once; the LLM uses this for all 3â€“5 lessons in the same thread.

1. **Role:** "You are a patient tutor for a 6-year-old. Use only the information below. Speak at her level (Lexile ~600L output, simple sentences). This prompt is for the whole day â€” run 3â€“5 short activities in this thread, up to 2 hours total."
2. **Who she is:** Name, age, languages; 2â€“3 sentence summary of interests and how she learns (from SELF).
3. **What she knows (IX-A):** Bullet list of knowledge areas (from SELF IX-A / recent evidence).
4. **What sheâ€™s curious about (IX-B):** Bullet list (from SELF IX-B).
5. **Where sheâ€™s at (edge):** THINK edge, MATH edge, WORK edge (from skill-think + skill-work).
6. **Todayâ€™s goals:** "Long-term: SAT readiness (goal â‰¥1200). Today in this thread: [e.g. one reading at the edge, one math at the edge, one creation/planning (WORK)]. Do these in order or as fits the conversation; after each, give one line for the parent to log."
7. **Rules:** "One question at a time. If she's stuck or misses a question, give a hint from the Record and try again before moving on. Aim for 80â€“85% success within each segment. Don't advance to a new segment until she shows ~90% mastery on the current one. Do not add facts not listed above. For reading: introduce one new word in context; when it appears, briefly explain it using a student-friendly definition (simple words, example from her world). Aim for 4 short segments of ~25â€“30 min each; keep each activity to 10â€“15 min. After each activity, output one line: 'We did [X].' so the parent can log â€” so the next day's prompt reflects what was done. Stay within one thread for the day. When asking what to do next or when the learner might not know how to respond, always offer 4 multiple choice options (A, B, C, D) so the learner never gets stuck."

The generator can output this as one block of text (or structured sections) for copy-paste.

---

## 4. Example A â€” Reading / comprehension lesson (THINK + SAT readiness)

**Record inputs (summary):**

- skill-think: edge = "Longer independent text; early chapter books; inference questions; retelling with explicit sentence structure"; comprehension_level 3; vocabulary_level 2; sat_readiness.ebrw_reading next_milestones: "600L input â€” early chapter books, short nonfiction."
- skill-work: work_goals.horizon = "SAT score â‰¥ 1200".
- SELF: Lexile input 400â€“500L, output 600L; favorites include Madeline, fairy tales, Clifford; IX-A includes planets, Earth layers, Lincoln, Nutcracker.

**Generated prompt (abbreviated):**

```
You are a patient reading tutor for Abby, age 6. Use ONLY the information below. Use simple words and short sentences (Lexile ~600L).

Who she is: Abby likes Madeline, fairy tales, Clifford, space, and animals. She retells stories with key details and character traits. Sheâ€™s working on "why do you think that?" and "what in the story shows that?"

What she knows: Planets (all names, Jupiterâ€™s storm, Mars), Earthâ€™s layers, Abraham Lincoln, The Nutcracker, reptiles, Tomb of Pakal, The Wild Robot.

Where sheâ€™s at (reading): Ready for slightly longer texts and early chapter books. Next: inference questions ("Why do you thinkâ€¦?", "What will happen next?"), vocabulary in context, evidence ("What in the story makes you say that?").

Goal today: One short reading at her edge (1â€“2 paragraphs or a short book page). Ask 1â€“2 inference questions. One new word in context. Keep it to about 15 minutes.

Rules: One question at a time. If sheâ€™s stuck, give a hint from what she already knows. Do not add facts or stories not listed above. At the end, summarize in one line what you did so her parent can log it (e.g. "We read a short passage and answered two â€˜why do you thinkâ€™ questions.").
```

**What the LLM might do:**

- Propose a 1â€“2 paragraph passage (or use a listed book/source); ask "What do you think will happen next?" and "What in the story makes you say that?"
- Introduce one new word in context and briefly explain it.
- Keep tone and length appropriate; close with a one-line summary for the parent to log (e.g. "We did one short reading and two inference questions; new word: [X].").

The **human** pastes this into ChatGPT/Grok, runs the conversation with the child, then can log "we did X" or paste the transcript for staging â†’ skill-think.

---

## 5. Example B â€” Math at the edge (MATH + skill-work goal)

**Record inputs:**

- skill-think MATH: edge = "Telling time; place value; double-digit operations"; counts_to 100; addition/subtraction single digit; tells_time: no (edge).
- skill-work: work_goals horizon SAT; SCHOOL first grade.
- SELF: age 6, first grade.

**Generated prompt (abbreviated):**

```
You are a patient math tutor for Abby, age 6, first grade. Use ONLY the information below. Simple words, short sentences (Lexile ~600L).

Where sheâ€™s at (math): Counts to 100. Single-digit addition and subtraction. Knows days of the week forward and backward. Not yet: telling time, place value, double-digit operations.

Goal today: One small step toward telling time OR place value (e.g. "What number is in the tens place?" with a two-digit number). About 10â€“15 minutes. One concept, then one or two practice questions.

Rules: One question at a time. Use only numbers and concepts listed above or one step at the edge (e.g. tens place). If sheâ€™s stuck, give a hint. Do not add content outside the Record. End with one line for the parent: "We did [X]."
```

**What the LLM might do:**

- Introduce "tens place" with a two-digit number (e.g. 34) and ask "Which digit is in the tens place?" or do one telling-time question (e.g. "When the big hand is on 12 and the small hand is on 3, what time is it?").
- Keep it to one concept and 1â€“2 follow-ups; output a one-line summary for logging.

Again, the **human** runs the conversation and can log or paste the transcript for skill-think/merge.

---

## 6. Example C â€” WORK-aligned lesson (making / planning at the edge)

**Record inputs:**

- skill-work: WORK edge = "Narrative creation from prompts; cross-language creative tasks; independent scene composition; planning/execution evidenced via WORK probe (step order, next step, making method)"; planning_level 1â€“2, execution_level 1; creation originality/elaboration/flexibility strong (CREATE-0001â€“0008).
- companion_creative_context: pencil/pen on paper, playful, prefers silence when creating.
- SELF: favorites (animals, Madeline, space); values kindness, bravery, beauty.

**Generated prompt (abbreviated):**

```
You are a gentle coach for Abby, age 6, who loves to draw and make things. Use ONLY the information below. Simple words (Lexile ~600L).

What sheâ€™s good at: She draws with lots of detail (color bands, eyelashes, whole scenes). She can order steps for familiar tasks (e.g. get materials first; lemonade first for a stand). She follows step-by-step (e.g. Lego steps). She gives reasons for choices ("kind, brave, beautiful").

Where sheâ€™s at (making/planning): Next steps: (1) Try a short narrative from a prompt (e.g. "Draw one scene from a story you know and tell me the steps you took"). (2) Plan a small project in order (e.g. "What would you do first, second, third to make X?").

Goal today: One short creation prompt OR one 3-step planning question. About 10â€“15 minutes. If itâ€™s a drawing prompt, suggest she can use pencil/pen on paper and tell you her steps after. If itâ€™s planning, ask for first, second, third.

Rules: Do not add characters or stories not in her Record (e.g. Madeline, animals, space, fairy tales are fine). One prompt or one planning question at a time. End with one line for the parent: "We did [X]."
```

**What the LLM might do:**

- Give one prompt: "Draw one scene from Madeline (or your favorite animal) and tell me: what did you do first, second, third?"
- Or ask: "If you were going to make a lemonade stand, what would you do first? Second? Third?"
- Then ask a short "why did you choose that?" to reinforce decision_making. Output a one-line summary for the parent.

The **human** runs this with the child; any "we did X" or transcript can be staged and merged into WORK/THINK as evidence.

---

## 7. Example D â€” Integrated 2-hour block (3â€“5 lessons in one prompt)

**Record inputs:** Combined SELF + skill-think (THINK, MATH, SAT readiness) + skill-work (work_goals, WORK edge, SCHOOL, 2-hour design).

**Generated prompt (abbreviated):**

```
You are a tutor for Abby, 6, first grade. She has a 2-hour block for screen-based learning today. Use ONLY the information below. Simple words (Lexile ~600L).

Who she is: [2â€“3 lines from SELF â€” interests, how she learns.]

What she knows: [Bullet list from IX-A.]

Curiosity: [Bullet list from IX-B.]

Edge:
- Reading: Longer text, inference ("why?", "what in the story shows that?"), vocabulary in context.
- Math: Telling time, place value (tens place), double-digit next.
- Making/planning: Narrative from a prompt; plan 3 steps for a small project.

Goals: (1) SAT readiness over time â€” today: one reading at the edge + one inference question. (2) One math step (time or place value). (3) One short creation or planning question. Total about 3â€“5 short activities, up to 2 hours max. You can do them in any order.

Rules: One activity at a time. After each, say in one line what you did (for logging). Do not add facts or stories not listed above. If sheâ€™s tired or resistant, suggest a break or stop.
```

**What the LLM might do:**

- Run 3â€“5 short segments (e.g. one reading + inference, one math, one planning or creation), each with a one-line summary.
- Respect the 2-hour ceiling and the Record-only constraint; the human can log each segment or paste the full transcript for skill-think.

---

## 8. How skill-work specifically drives the generator

| skill-work element | How itâ€™s used in lesson generation |
|--------------------|------------------------------------|
| **work_goals.horizon** (e.g. SAT â‰¥ 1200) | THINK/skill-think SAT readiness and EBRW/Math trajectory are prioritized; reading and math lesson prompts reference "goal: SAT readiness" and next milestones. |
| **WORK edge** | Lesson prompt includes "making/planning at the edge" (narrative from prompts, 3-step planning, next step in sequence) so the LLM can propose one WORK-aligned activity per block. |
| **SCHOOL** (first grade) | Age and grade are passed into the prompt so the LLM keeps difficulty and framing appropriate. |
| **2-hour design** (from alpha-school) | Prompt can state "up to 2 hours" or "3â€“5 lessons per block" so the human and LLM donâ€™t over-schedule. |
| **companion_creative_context** | Optional: "She likes pencil/pen on paper, playful, prefers silence when creating" so creation prompts match the household context. |

The **lesson prompt generator** (script or manual) should read `skill-work.md` along with `skill-think.md` and `self.md`, then fill the minimal prompt shape above. That yields the personalized prompt the human companion pastes into the LLM for 3â€“5 lessons, with transcript â†’ skill-think (and optional "we did X" â†’ WORK) after.

---

## 9. Implementation (script)

The lesson prompt generator is implemented as `scripts/generate_lesson_prompt.py`:

1. Reads `self.md`, `skill-think.md`, `skill-work.md`.
2. Parses: IX-A/B topics, Lexile, THINK/MATH/WORK/CHINESE edge, work_goals, SCHOOL, companion_creative_context.
3. Fills the minimal prompt shape (Â§3) **day-scoped**: one prompt containing todayâ€™s full set of goals (reading, math, WORK) so the human runs the script once per day and pastes once.
4. Outputs one text block (or one file) for copy-paste.

**Usage:** `python scripts/generate_lesson_prompt.py -u grace-mar` or `python scripts/generate_lesson_prompt.py -u grace-mar -n Robert -o docs/skill-work/sample-lesson-prompt-grace-mar-generated.txt`

**Formative loop:** Run the generator after processing "we did X" merges so the next day's prompt reflects the updated Record.

Related: `scripts/export_curriculum.py` (skills edge, IX summaries); `scripts/export_prp.py` (SELF â†’ prompt); `bot/prompt.py` HOMEWORK_PROMPT (Record â†’ JSON questions). A **lesson prompt** is a different product: not PRP (identity/voice for chat) and not homework JSON, but a **tutor instruction set** derived from the same Record so the human can run **one prompt per day** and get 3â€“5 lessons in one LLM thread.

---

## 10. Summary

- **Ideal UX:** One prompt per day. Human runs the generator once, pastes once, runs 3â€“5 lessons in one LLM thread (2-hour design).
- **Flow:** Record (SELF + skill-think + skill-work) â†’ lesson prompt generator (day-scoped) â†’ human pastes into LLM â†’ 3â€“5 lessons in one thread â†’ transcript optional â†’ "we did X" / paste â†’ skill-think (and optionally WORK) via gate.
- **skill-work** supplies work_goals (SAT), WORK edge (making/planning/creation), SCHOOL, and 2-hour alignment so lessons are goal-aware and at the edge.
- **Examples Aâ€“D** show: (A) reading/THINK + SAT readiness, (B) math at MATH edge, (C) WORK making/planning at edge, (D) integrated 2-hour block. Example D is the one-prompt-per-day pattern: one paste, full dayâ€™s scope.

**Demo:** [sample-lesson-prompt-grace-mar.txt](sample-lesson-prompt-grace-mar.txt) is a curated one-prompt-per-day lesson. **Generator:** Run `python scripts/generate_lesson_prompt.py -u grace-mar -n Robert` to produce a prompt from the current Record; regenerate when the Record changes (especially after "we did X" merges).


