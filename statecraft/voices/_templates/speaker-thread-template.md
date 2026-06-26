# Speaker thread template

WORK only; not Record.

Purpose: define the canonical scaffold for **topical threads** in the `speakers/` taxonomy.

System grammar:

- **Person arc:** `<speaker>-arc.md` for the speaker across hosts, contexts, and time.
- **Relational arc:** `<host>-<speaker>-arc.md` for what a specific host repeatedly elicits from that speaker.
- **Topical thread:** `<speaker>-thread-<topic>.md` for a compact topic-centered continuity surface inside a larger speaker corpus.

Ownership rule:

- Choose an **arc** when the question is "whose continuity is this?"
- Choose a **thread** when the question is "which recurring topic or strand inside that arc needs its own reusable surface?"

Orthogonality rule:

- Threads inside one arc should be as **mutually orthogonal** as the material allows.
- A new thread must isolate a distinct recurring object, mechanism, or retrieval use, not merely restate a neighboring thread with slightly different labels.
- If two proposed threads share the same source spine, same causal grammar, and same operator use, they probably belong in one thread or back in the parent arc.

## Topical thread

# Speaker topical thread — `<speaker>-thread-<topic>`

WORK only; not Record.

Use a topical thread only when one recurring subject materially deserves its own reusable surface inside a person arc or relational arc.

**Naming rule:**

- Keep the topic name concrete and reusable, for example `international-law`, `deterrence`, or `domestic-legitimacy`.

**Recommended shape:**

- `Orthogonality guide`
- `Purpose`
- `Boundary`
- `Core thesis`
- `Current source spine`
- `Recurring claims`
- `Best-use cases`
- `Do-not-flatten rules`

**Topical-thread rules:**

- Treat the topical thread as a support surface beneath an arc, never as a replacement for the arc itself.
- Start with an explicit `Orthogonality guide` that says what this thread isolates, what neighboring surface it should not be confused with, and when to route back upward into the parent arc.
- Favor boundary, core thesis, current source spine, recurring claims, best-use cases, and do-not-flatten rules over month-by-month machinery.
- Link upward to the governing person arc or relational arc and sideways to neighboring arcs or topic lanes when those distinctions matter.
- Preserve the thread's distinctness by naming what it sees that neighboring threads do not.

Use a topical thread when the notebook needs:

- one recurring topic cut cleanly out of a larger speaker corpus
- reuse across multiple weeks without reopening the whole arc
- a topic-centered bridge into neighboring arcs or lanes
- a named strand that can be cited as one component of a larger arc

Quick distinctness tests:

- **Object test** - is the thread about a different thing?
- **Mechanism test** - does it explain recurrence differently?
- **Use test** - would an operator open it for a different reason?

### Orthogonality guide

Every canonical topical thread should open with a short guide in this shape:

- state the thread's distinct recurring strand in one sentence
- give a quick separation rule against the nearest neighboring surfaces
- include a `Distinct from:` block that names the adjacent thread, parent arc, or host-local arc most likely to be confused with it
- tell the operator when to route back to the parent arc instead of forcing more into the topical thread

Minimum contract:

- `this thread = {its narrow recurring strand}`
- `{neighboring surface} = {what that surface does instead}`
- `Distinct from:` followed by 2-4 concrete neighboring surfaces

If a proposed thread cannot fill this section cleanly, it probably does not deserve its own surface yet.

## Boundary

Do not use a thread template for:

- a person-centered cross-host surface that should be `{speaker}-arc.md`
- a host-pair surface that should be `{host}-{speaker}-arc.md`
- a cross-speaker disagreement note that should be a `speaker-a-vs-speaker-b-<window>.md` tension note
- a standalone speaker-level continuity file that pretends to exist outside any arc
- a file whose main value is ranking one host-local guest run
- a raw-input ledger or transcript sink
- a profile or speaker object
