# Example LIB corpus (grace-mar-derived) — optional reference

**Not** the default for new instances. The canonical template **`platform/template/self-library.md`** ships **governance + empty `entries:`** only.

This file preserves the previous large seed (books/stories LIB rows) from an early grace-mar-aligned export, for operators who want a **starting shelf** to trim and gate. Prefer adding rows via the pipeline when possible.

---

# self-library — Curated Lookup Sources (Template, Optional)

**Cloned from grace-mar LIBRARY (books and stories only).** Optional. Copy this structure when creating a new user directory if the instance supports a bounded lookup extension. self-library is a **query-first** list of curated sources the companion or operator may use to answer questions—without auto-merging into the Record.

Governanced by the instance. Use: lookup from these sources when answering; do not infer into self or self-evidence unless the companion approves and merges via the normal pipeline.

**Maturity levels** (difficulty / content): `1` = young / all ages (fables, fairy tales, simple retellings); `2` = middle grade (myths, adventure, classic children's novels); `3` = older / teen+ (full-length classics, drama, complex themes). Sources are public domain (e.g. Project Gutenberg); volume names refer to PD collections, not Usborne.

---

## Entries (books and stories)

```yaml
entries:
  - id: 
    title: "Greek Myths (Bulfinch, PG 22381)"
    author: "Usborne"
    isbn: "9781474986441"
    type: book
    status: deprecated
    read_status: unread
    scope: [mythology, Greek myths, ancient Greece]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/22381"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (Bulfinch 3327, Odyssey 1727)."

  - id: 
    title: "The Odyssey (Homer, PG 1727)"
    author: "Usborne"
    isbn: "9781409598930"
    type: book
    status: active
    read_status: unread
    scope: [mythology, Greek, Odyssey, Homer]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/1727"
    source: manual
    added_at: 2026-02-20
    notes: "Ordered Sept 2025."

  - id: 
    title: "Stories from India (PG 2388)"
    author: "Usborne"
    isbn: "9781409596714"
    type: book
    status: deprecated
    read_status: unread
    scope: [mythology, India, stories, folktales]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/2388"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entry  (PD 2388)."

  - id: 
    title: "Adventure classics (PG 521, 120, 829)"
    author: "Usborne"
    isbn: "9781409522300"
    type: book
    status: deprecated
    read_status: unread
    scope: [adventure, stories]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/1184"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (PD 521, 120, 829)."

  - id: 
    title: "Bible stories (KJV, PG 10)"
    author: "Usborne"
    isbn: "9781409580980"
    type: book
    status: deprecated
    read_status: unread
    scope: [Bible, stories, religion]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/10"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (KJV 10)."

  - id: 
    title: "Stories from China (PG 25240)"
    author: "Usborne"
    isbn: "9781474947077"
    type: book
    status: deprecated
    read_status: unread
    scope: [China, stories, folktales]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/25240"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entry  (PD 25240)."

  - id: 
    title: "Myths from around the world (Bulfinch, PG 3327)"
    author: "Usborne"
    isbn: "9781409596738"
    type: book
    status: deprecated
    read_status: unread
    scope: [mythology, world myths, folktales]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (Greek/Roman in 3327)."

  - id: 
    title: "Ballet stories (PG 38733)"
    author: "Usborne"
    isbn: "9781474922050"
    type: book
    status: deprecated
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to . Ordered Sept 2025."

  - id: 
    title: "The Secret Garden (PG 17396)"
    author: "Usborne"
    isbn: "9781409586562"
    type: book
    status: deprecated
    read_status: unread
    scope: [classics, Secret Garden, stories]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/17396"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entry  (Secret Garden 17396)."

  - id: 
    title: "Aesop's Fables (PG 21)"
    author: "Usborne"
    isbn: "9781409538875"
    type: book
    status: deprecated
    read_status: unread
    scope: [fables, Aesop, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/21"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (Aesop 21)."

  - id: 
    title: "Greek myths (PG 11582)"
    author: "Usborne"
    isbn: "9781409531678"
    type: book
    status: deprecated
    read_status: unread
    scope: [mythology, Greek myths, stories]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/11582"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (Bulfinch 3327)."

  - id: 
    title: "Norse myths (Guerber, PG 28497)"
    author: "Usborne"
    isbn: "9781409550723"
    type: book
    status: deprecated
    read_status: unread
    scope: [mythology, Norse, Vikings, stories]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (Guerber 28497)."

  - id: 
    title: "Andersen's Fairy Tales (PG 27200)"
    author: "Usborne"
    isbn: "9781409523390"
    type: book
    status: deprecated
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to . Ordered Sept 2025."

  - id: 
    title: "King Arthur (Malory, PG 610)"
    author: "Usborne"
    isbn: "9781409563266"
    type: book
    status: deprecated
    read_status: unread
    scope: [King Arthur, legends, stories, mythology]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/610"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entry  (Malory 610)."

  - id: 
    title: "Stories from Shakespeare (PG 100)"
    author: "Usborne"
    isbn: "9781409522232"
    type: book
    status: deprecated
    read_status: unread
    scope: [Shakespeare, plays, stories]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (Complete Works 100)."

  - id: 
    title: "Grimm's Fairy Tales (PG 2591)"
    author: "Usborne"
    isbn: "9780746098547"
    type: book
    status: deprecated
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to . Ordered Sept 2025."

  - id: 
    title: "Dickens (PG author 37)"
    author: "Usborne"
    isbn: "9781474938136"
    type: book
    status: deprecated
    read_status: unread
    scope: [Dickens, classics, literature]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/author/37"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (per-novel PD links)."

  - id: 
    title: "Arabian Nights (Lang, PG 128)"
    author: "Anna Milbourne"
    isbn: "9781409533009"
    type: book
    status: deprecated
    read_status: unread
    scope: [Arabian Nights, tales, Middle East, stories]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/128"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (Lang 128)."

  - id: 
    title: "Shakespeare, Complete Works (PG 100)"
    author: "Usborne"
    isbn: "9781409598770"
    type: book
    status: deprecated
    read_status: unread
    scope: [Shakespeare, plays, stories, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (Complete Works 100)."

  - id: 
    title: "Jane Austen (PG author 68)"
    author: "Usborne"
    isbn: "9781474938143"
    type: book
    status: deprecated
    read_status: unread
    scope: [Jane Austen, novels, classics, literature]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/author/68"
    source: manual
    added_at: 2026-02-20
    notes: "Replaced by story-level entries  to  (per-novel PD links)."

  - id: 
    title: "Snow White and Rose Red"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Little Red Riding Hood"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Rapunzel"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Sleeping Beauty"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Frog Prince"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Musicians of Bremen"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Rumpelstiltskin"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Tom Thumb"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Hansel and Gretel"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Twelve Dancing Princesses"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Bear and the Wren"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "King Thrushbeard"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Goose Girl"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Elves and the Shoemaker"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Snow White and the Seven Dwarfs"
    type: story
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: active
    read_status: unread
    scope: [fairy tales, Grimm, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Princess and the Pea"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Emperor's New Clothes"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Thumbelina"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Ugly Duckling"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Little Mermaid"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Emperor and the Nightingale"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Flying Trunk"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Brave Tin Soldier"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Wild Swans"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Little Fir Tree"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Tinderbox"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Snow Queen"
    type: story
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: active
    read_status: unread
    scope: [fairy tales, Hans Christian Andersen, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Cinderella"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Swan Lake"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Sleeping Beauty"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Don Quixote"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Coppélia"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Nutcracker"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "The Firebird"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Giselle"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Ondine"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "La Sylphide"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "La Fille Mal Gardée"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  - id: 
    title: "Romeo and Juliet"
    type: story
    volume: "Ballet stories (PG 38733)"
    status: active
    read_status: unread
    scope: [ballet, dance, stories]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    source: manual
    added_at: 2026-02-22

  # --- Greek myths (Bulfinch 3327) ---
  - id: 
    title: "Prometheus and Pandora"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Apollo and Daphne"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Phaeton"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Midas, Baucis and Philemon"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Proserpine (Persephone)"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Pygmalion and Dryope"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Cupid and Psyche"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Cadmus and the Myrmidons"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Minerva and Arachne, Niobe"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Perseus and Medusa"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Golden Fleece and Medea"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Hercules"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Theseus and the Minotaur"
    type: story
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: active
    read_status: unread
    scope: [mythology, Greek myths]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Odyssey"
    type: story
    volume: "Homer, Odyssey (PG 1727)"
    status: active
    read_status: unread
    scope: [mythology, Greek, Homer]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/1727"
    source: manual
    added_at: 2026-02-26
  # --- Stories from India (PD 2388) ---
  - id: 
    title: "Stories from India (collection)"
    type: story
    volume: "Stories from India (PG 2388)"
    status: active
    read_status: unread
    scope: [India, stories, folktales]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/2388"
    source: manual
    added_at: 2026-02-26
  # --- Adventure (PD 521, 120, 829) ---
  - id: 
    title: "Robinson Crusoe"
    type: story
    volume: "Adventure classics (PG 521, 120, 829)"
    status: active
    read_status: unread
    scope: [adventure, stories]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/521"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Treasure Island"
    type: story
    volume: "Adventure classics (PG 521, 120, 829)"
    status: active
    read_status: unread
    scope: [adventure, stories]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/120"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Gulliver's Travels"
    type: story
    volume: "Adventure classics (PG 521, 120, 829)"
    status: active
    read_status: unread
    scope: [adventure, stories]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/829"
    source: manual
    added_at: 2026-02-26
  # --- Bible stories (KJV 10) ---
  - id: 
    title: "Creation and Eden"
    type: story
    volume: "Bible, KJV (PG 10)"
    status: active
    read_status: unread
    scope: [Bible, stories, religion]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/10"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Noah and the Flood"
    type: story
    volume: "Bible, KJV (PG 10)"
    status: active
    read_status: unread
    scope: [Bible, stories, religion]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/10"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Abraham and Isaac"
    type: story
    volume: "Bible, KJV (PG 10)"
    status: active
    read_status: unread
    scope: [Bible, stories, religion]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/10"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Moses and the Exodus"
    type: story
    volume: "Bible, KJV (PG 10)"
    status: active
    read_status: unread
    scope: [Bible, stories, religion]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/10"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "David and Goliath"
    type: story
    volume: "Bible, KJV (PG 10)"
    status: active
    read_status: unread
    scope: [Bible, stories, religion]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/10"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Daniel in the Lions' Den"
    type: story
    volume: "Bible, KJV (PG 10)"
    status: active
    read_status: unread
    scope: [Bible, stories, religion]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/10"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Nativity"
    type: story
    volume: "Bible, KJV (PG 10)"
    status: active
    read_status: unread
    scope: [Bible, stories, religion]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/10"
    source: manual
    added_at: 2026-02-26
  # --- Stories from China (PD 25240) ---
  - id: 
    title: "Stories from China (collection)"
    type: story
    volume: "Stories from China (PG 25240)"
    status: active
    read_status: unread
    scope: [China, stories, folktales]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/25240"
    source: manual
    added_at: 2026-02-26
  # --- Secret Garden ---
  - id: 
    title: "The Secret Garden"
    type: story
    volume: "The Secret Garden (PG 17396)"
    status: active
    read_status: unread
    scope: [classics, Secret Garden]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/17396"
    source: manual
    added_at: 2026-02-26
  # --- Aesop fables (PD 21) ---
  - id: 
    title: "The Lion and the Mouse"
    type: story
    volume: "Aesop's Fables (PG 21)"
    status: active
    read_status: unread
    scope: [fables, Aesop]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/21"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Hare and the Tortoise"
    type: story
    volume: "Aesop's Fables (PG 21)"
    status: active
    read_status: unread
    scope: [fables, Aesop]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/21"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Wolf and the Lamb"
    type: story
    volume: "Aesop's Fables (PG 21)"
    status: active
    read_status: unread
    scope: [fables, Aesop]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/21"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Shepherd's Boy and the Wolf"
    type: story
    volume: "Aesop's Fables (PG 21)"
    status: active
    read_status: unread
    scope: [fables, Aesop]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/21"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Dog and the Shadow"
    type: story
    volume: "Aesop's Fables (PG 21)"
    status: active
    read_status: unread
    scope: [fables, Aesop]
    maturity: 1
    pd_url: "https://www.gutenberg.org/ebooks/21"
    source: manual
    added_at: 2026-02-26
  # --- Norse myths (Guerber 28497) ---
  - id: 
    title: "The Creation (Norse)"
    type: story
    volume: "Norse myths (Guerber, PG 28497)"
    status: active
    read_status: unread
    scope: [mythology, Norse, Vikings]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Odin and the Norse Gods"
    type: story
    volume: "Norse myths (Guerber, PG 28497)"
    status: active
    read_status: unread
    scope: [mythology, Norse, Vikings]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Thor and Loki"
    type: story
    volume: "Norse myths (Guerber, PG 28497)"
    status: active
    read_status: unread
    scope: [mythology, Norse, Vikings]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Death of Baldur"
    type: story
    volume: "Norse myths (Guerber, PG 28497)"
    status: active
    read_status: unread
    scope: [mythology, Norse, Vikings]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Ragnarok"
    type: story
    volume: "Norse myths (Guerber, PG 28497)"
    status: active
    read_status: unread
    scope: [mythology, Norse, Vikings]
    maturity: 2
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    source: manual
    added_at: 2026-02-26
  # --- King Arthur (Malory 610) ---
  - id: 
    title: "Tales of King Arthur (collection)"
    type: story
    volume: "Usborne Illustrated Tales of King Arthur"
    status: active
    read_status: unread
    scope: [King Arthur, legends, mythology]
    pd_url: "https://www.gutenberg.org/ebooks/610"
    source: manual
    added_at: 2026-02-26
  # --- Shakespeare plays (Complete Works 100) ---
  - id: 
    title: "Hamlet"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Macbeth"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Romeo and Juliet"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "A Midsummer Night's Dream"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Tempest"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Othello"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "King Lear"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Merchant of Venice"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Twelfth Night"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "As You Like It"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Much Ado About Nothing"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Julius Caesar"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Stories from Shakespeare (all plays)"
    type: story
    volume: "Shakespeare, Complete Works (PG 100)"
    status: active
    read_status: unread
    scope: [Shakespeare, plays]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/100"
    source: manual
    added_at: 2026-02-26
  # --- Dickens novels (per-novel PD) ---
  - id: 
    title: "Oliver Twist"
    type: story
    volume: "Dickens (PG author 37)"
    status: active
    read_status: unread
    scope: [Dickens, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/730"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "David Copperfield"
    type: story
    volume: "Dickens (PG author 37)"
    status: active
    read_status: unread
    scope: [Dickens, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/766"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Great Expectations"
    type: story
    volume: "Dickens (PG author 37)"
    status: active
    read_status: unread
    scope: [Dickens, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/1400"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "A Tale of Two Cities"
    type: story
    volume: "Dickens (PG author 37)"
    status: active
    read_status: unread
    scope: [Dickens, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/98"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Bleak House"
    type: story
    volume: "Dickens (PG author 37)"
    status: active
    read_status: unread
    scope: [Dickens, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/1023"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Dickens (other novels)"
    type: story
    volume: "Dickens (PG author 37)"
    status: active
    read_status: unread
    scope: [Dickens, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/author/37"
    source: manual
    added_at: 2026-02-26
  # --- Arabian Nights (Lang 128) ---
  - id: 
    title: "Aladdin and the Wonderful Lamp"
    type: story
    volume: "Arabian Nights (Lang, PG 128)"
    status: active
    read_status: unread
    scope: [Arabian Nights, tales]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/128"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Sindbad the Sailor"
    type: story
    volume: "Arabian Nights (Lang, PG 128)"
    status: active
    read_status: unread
    scope: [Arabian Nights, tales]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/128"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Ali Baba and the Forty Thieves"
    type: story
    volume: "Arabian Nights (Lang, PG 128)"
    status: active
    read_status: unread
    scope: [Arabian Nights, tales]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/128"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "The Fisherman and the Jinni"
    type: story
    volume: "Arabian Nights (Lang, PG 128)"
    status: active
    read_status: unread
    scope: [Arabian Nights, tales]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/128"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Arabian Nights (full collection)"
    type: story
    volume: "Arabian Nights (Lang, PG 128)"
    status: active
    read_status: unread
    scope: [Arabian Nights, tales]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/128"
    source: manual
    added_at: 2026-02-26
  # --- Jane Austen novels (per-novel PD) ---
  - id: 
    title: "Pride and Prejudice"
    type: story
    volume: "Jane Austen (PG author 68)"
    status: active
    read_status: unread
    scope: [Jane Austen, novels, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/1342"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Sense and Sensibility"
    type: story
    volume: "Jane Austen (PG author 68)"
    status: active
    read_status: unread
    scope: [Jane Austen, novels, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/161"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Emma"
    type: story
    volume: "Jane Austen (PG author 68)"
    status: active
    read_status: unread
    scope: [Jane Austen, novels, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/158"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Mansfield Park"
    type: story
    volume: "Jane Austen (PG author 68)"
    status: active
    read_status: unread
    scope: [Jane Austen, novels, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/141"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Northanger Abbey"
    type: story
    volume: "Jane Austen (PG author 68)"
    status: active
    read_status: unread
    scope: [Jane Austen, novels, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/121"
    source: manual
    added_at: 2026-02-26
  - id: 
    title: "Persuasion"
    type: story
    volume: "Jane Austen (PG author 68)"
    status: active
    read_status: unread
    scope: [Jane Austen, novels, classics]
    maturity: 3
    pd_url: "https://www.gutenberg.org/ebooks/105"
    source: manual
    added_at: 2026-02-26
```

---

## Metadata

```yaml
total_entries: 127
clone_source: grace-mar LIBRARY (books and stories only; reference and video excluded)
books_broken_into_stories: 2026-02-26
maturity_levels: "1=young/all ages, 2=middle grade, 3=older/teen+"
last_updated: 2026-02-26
```

---

## Aggregate word count (estimated)

Rough totals for PD sources that have at least one entry in each maturity tier. Same source can contribute to more than one tier. Based on standard reference word counts for the listed works; actual PG texts may vary.

| Maturity | Description        | Estimated words | Main PD sources (PG etexts) |
|----------|--------------------|-----------------|-----------------------------|
| **1**    | Young / all ages    | **~1,035,000**  | Grimm (2591), Andersen (27200), Ballet (38733), Bible KJV (10), Aesop (21) |
| **2**    | Middle grade       | **~1,060,000**  | Bulfinch Greek (3327), Odyssey (1727), India (2388), Robinson Crusoe (521), Treasure Island (120), Gulliver (829), China (25240), Secret Garden (17396), Norse (28497), King Arthur (610) |
| **3**    | Older / teen+      | **~5,400,000**  | Odyssey (1727), King Arthur (610), Shakespeare Complete (100, ~884k), Dickens novels (730, 766, 1400, 98, 1023 + author 37), Arabian Nights Lang (128), Austen novels (1342, 161, 158, 141, 121, 105) |

- **Maturity 1:** ~1.0M words (fables, fairy tales, ballet retellings, Bible, Andersen).
- **Maturity 2:** ~1.1M words (myths, adventure novels, children’s classics, Malory).
- **Maturity 3:** ~5.4M words (Shakespeare ~884k, Dickens ~2.5M across major novels, Austen ~726k, plus Odyssey, Malory, Arabian Nights).

*Totals are approximate; PG editions and word-count methods differ.*

---

*Cloned from grace-mar. All sources are public domain (e.g. Project Gutenberg); volume/title names refer to PD collections. Entries have maturity 1–3 (young → older). Copy to `<new_id>/self-library.md` in an instance; add or remove entries as needed.*
