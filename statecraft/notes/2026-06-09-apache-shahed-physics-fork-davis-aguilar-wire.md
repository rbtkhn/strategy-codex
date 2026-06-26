WORK only; not Record.

# Apache × Shahed-136 — physics fork (Davis · Aguilar · Krapivnik vs wire) — 2026-06-09

**Parent:** [2026-06-09 daily](statecraft/synthesis/day/2026-06-09.md) · [news-verify matrix](statecraft/notes/wire/2026-06-08-09-news-verify-matrix.md) (**S2** contested) · **Sources:** [Davis breaking Qeshm/Apache](https://www.youtube.com/watch?v=TlcHuoC86JQ) · [Aguilar × Nima](https://www.youtube.com/watch?v=4wfVXkp9eGs) (Nawfal Pape same Apache bench) · [Krapivnik × Nima breaking interrupt](https://www.youtube.com/watch?v=Cg-cFVQ55S8) · [Davis × Marandi morning](https://www.youtube.com/watch?v=xP9lW4aYJx8)

## Purpose

Compress the **Apache down / cause unclear** seam into one physics-grounded fork before it floors **CENTCOM Qeshm strikes** (5 p.m. ET 9 Jun) or daily synthesis.

**Question:** Given reported outcomes (aircraft lost, **two crew safe**, sea-drone rescue), what do **kinematics + energetics + Apache sensor fit** allow for a **Shahed-136 ↔ AH-64** encounter?

**Not in scope:** Proving mechanical failure, proving Iranian denial, or adjudicating CENTCOM credibility — only **what collision physics permits**.

---

## A. Closure worksheet (order-of-magnitude)

**Constants (public specs):**

| Parameter | Shahed-136 | AH-64 Apache |
|-----------|------------|--------------|
| Cruise speed **v** | **51 m/s** (185 km/h) | **74 m/s** (~143 kt cruise) |
| Body scale | 3.5 m × 2.5 m | Rotor **Ø 14.6 m**; fuselage ~15 m |
| Guidance | INS/GNSS → **fixed coordinates**; ~10–50 m CEP vs **static** targets | Piloted; agile; can hover / turn |
| Warhead | **30–50 kg** HE (nose) | — |

**Time of flight τ = range / 51 m/s → Apache displacement ≈ 74 m/s × τ** (straight-line upper bound; maneuver increases miss):

| Slant range (km) | τ (s) | τ (min) | Apache displacement (km) | GNSS fixed-target CEP (m) | Physics read |
|------------------|-------|---------|--------------------------|---------------------------|--------------|
| **1** | 20 | 0.3 | **1.5** | 10–50 | Still needs **live track**; hover-only target |
| **2** | 39 | 0.7 | **2.9** | 10–50 | Point-launch **miss** unless stationary |
| **5** | 98 | 1.6 | **7.3** | 10–50 | **Not** coordinate-guided anti-air |
| **10** | 196 | 3.3 | **14.5** | 10–50 | Absurd for moving helicopter |
| **30** | 588 | 9.8 | **43.5** | 10–50 | Cruise-missile role only |

**Capture geometry (contact scale):**

| Aspect | Effective radius (order) | Contact scale **R₁+R₂** |
|--------|--------------------------|-------------------------|
| Apache broadside (rotor normal) | ~7 m | **~9 m** |
| Apache side fuselage | ~3 m | **~5 m** |
| Shahed body | ~1–2 m | — |

**Encounter probability (sketch):**

| Scenario | Order-of-magnitude **P** per sortie | Notes |
|----------|-------------------------------------|-------|
| **Accidental** intersection (uncorrelated paths) | **10⁻⁷ – 10⁻⁹** | Shared theatre ≠ shared 10 m tube |
| **Deliberate** Shahed-136 vs maneuvering Apache (no seeker) | **10⁻⁴ – 10⁻²** | Bad vs SAM/AAA; luck / hover only |
| **Full terminal hit + 50 kg HE + crew uninjured** | **Low conditional P** | Energetics–outcome tension |

**Short rule:** Shahed-136 is a **slow coordinate cruiser** (~51 m/s); Apache on patrol is a **large moving target** (~74 m/s+). Without a **seeker or continuous retarget**, closure math produces **kilometer-class miss** over flyout times that matter.

---

## Apache sensors vs Shahed approach

**Question:** Would an AH-64’s radar or other sensors **reliably detect** a slow inbound Shahed-136 in time to treat the official kill story as plausible?

**Short answer:** Apache carries **serious attack-helicopter sensors**, not an **air-defense search-and-cue chain** for small slow drones. **Detection is possible** (visual/IR); **reliable early warning is not the design center.** Shahed-136’s **passive INS/GNSS** guidance gives **no radar-warning trip**.

### Sensor inventory (variant-dependent; AH-64D/E typical)

| System | Primary role | vs Shahed-136 inbound |
|--------|--------------|------------------------|
| **TADS / PNVS** (day TV + **FLIR**) | Crew **visual–IR** search & track | **Best chance** — if crew scans sector, range/weather/contrast permit; **not** auto “drone inbound” cue |
| **AN/APG-78 Longbow** (mast radar; **not** on every Apache) | **Ground** MTI / fire control; limited **air** tracks | Some helicopter/fixed-wing detection; **small slow low-signature UAV** = hard class; **not** drone-detection radar |
| **RWR / EW** (block-dependent) | Hostile **radar** illumination warning | **Null vs Shahed** — no target-tracking radar on helo required |
| **Laser warn / designator chain** | Designation & some threat cues | **Not relevant** to coordinate cruiser |

### Implications for the fork

| Claim | Sensor read |
|-------|-------------|
| “Apache would have seen it and dodged” | **Overstated** — see ≠ defeat; no dedicated anti-drone air-search pipeline |
| “Shahed could approach without any electronic warning” | **Supported** — passive guidance → **no RWR** |
| “FLIR/visual makes deliberate intercept easy” | **Weak** — crew-dependent; does **not** fix **km-class miss** without seeker/retarget |
| “Sensor failure required for official story” | **Not required** — **mechanical (IV)** branch is sensor-agnostic |
| “Deliberate kill needs physics + energetics + aim” | **Unchanged** — sensors do **not** rescue **joint hit × survive ~10⁻⁵** |

**Iran planning read:** Even **if** FLIR occasionally spots a drone, **coordinate Shahed-136** still lacks **closing solution** on a maneuvering Apache. Sensors do **not** make deliberate Shahed anti-helo a rational expenditure.

**Configuration note:** Lost-airframe block (**D vs E**, Longbow fitted or not) marginally affects **radar limb only**; **RWR null** and **FLIR crew-dependence** hold across typical U.S. theater fits. **`fact-check`** tail number / unit ORBAT if configuration becomes load-bearing.

---

## Joint probability (hit × survival)

**Wire claim bundle:** Shahed-136 **hits** a maneuvering Apache **and** both crew **survive** (ditch + sea-drone rescue).

\[
P(\text{story}) \approx P(\text{hit}) \times P(\text{survive} \mid \text{hit})
\]

Treat as **conditional chain**, not independent miracles: a full terminal hit largely **determines** survival odds.

### Factor 1 — P(hit)

| Scenario | Order of magnitude |
|----------|-------------------|
| Deliberate Shahed-136 vs maneuvering Apache (no seeker) | **10⁻⁴ – 10⁻²** |
| Accidental path intersection | **10⁻⁷ – 10⁻⁹** |

Mid-range deliberate sortie: **~10⁻³**.

### Factor 2 — P(survive | hit)

Apache: **no ejection seats**. Reported bench = **controlled loss + rescue**, not inflight disintegration.

| Hit class | P(survive \| hit) | Notes |
|-----------|-------------------|-------|
| Full terminal + warhead function (~30–50 kg HE) | **~10⁻² – 10⁻¹** (generous) | Direct coupling usually destroys rotor / transmission / fuel |
| Graze / rotor strike / partial coupling / dud | **~10⁻¹ – 10⁰** | Wreck may still be ditchable over water |
| Mechanical / pilot ditch (no Iranian ordnance) | **~0.5 – 0.9** | Best fit to “aircraft lost, crew safe” |

Mid-range for **“Shahed killed it” + “crew fine”**: **~10⁻²** conditional on a **real** Shahed-scale terminal event.

### Multiplication table

| P(hit) | P(survive \| hit) | **Joint P** | Per-million sorties |
|--------|-------------------|-------------|---------------------|
| **10⁻³** (deliberate mid) | **10⁻²** (terminal, generous) | **~10⁻⁵** | ~10 / 1M |
| **10⁻⁴** (deliberate low) | **10⁻²** | **~10⁻⁶** | ~1 / 1M |
| **10⁻²** (deliberate high) | **10⁻²** | **~10⁻⁴** | ~100 / 1M |
| **10⁻⁸** (accidental) | **10⁻¹** (graze) | **~10⁻⁹** | negligible |
| **10⁻³** | **10⁻¹** (graze-only) | **~10⁻⁴** | still rare |

### Versus competing class (no hit penalty)

| Story | Joint P (order) |
|-------|-----------------|
| **Shahed terminal kill + safe crew** | **~10⁻⁵ – 10⁻⁶** |
| **Mechanical / controlled ditch** | **~10⁻¹ – 10⁰** |

**Disproportion:** Survival is **cheap** under ditch stories and **expensive** under 50 kg HE terminal stories. Multiplying forces **graze / mislabel / non-Shahed** — not the clean Pentagon “Shahed downed Apache” headline.

**Iran resource read:** A state that understands closure math would **not** budget Shahed-136 sorties for **~10⁻⁵** joint outcomes when the same asset hits **fixed** infrastructure at far higher P. Iranian **denial + non-deliberate** line is **strategically consistent** with that calculus.

**Daily floor (joint):** Apache down **supported**; **Shahed-136 terminal intercept with uninjured crew** is **joint-improbable (~10⁻⁵ per sortie, generous)** — pending ordnance, blast pattern, engagement geometry.

---

## B. Bayesian fork — class priors and posteriors

WORK interpretive weights only; **not** Record truth. Update when wreckage / CENTCOM geometry lands.

**Observed evidence E (8–9 Jun bench):**

- Aircraft **lost**; **two crew safe** / uninjured; sea-drone rescue.
- Trump: Iran **shot down** Apache (escalation permission).
- Pentagon leak tier: **Shahed** (CNN/CBS).
- Iran: **not deliberate** / deny (Araghchi; Marandi military sources).
- Physics: joint **~10⁻⁵** for deliberate Shahed terminal + safe crew.
- Sensors: Shahed **no RWR trip**; FLIR/Longbow **possible but not reliable** drone-detection chain.

### Hypothesis classes

| Class | Mechanism | Prior **P(H)** | **P(E \| H)** (likelihood) |
|-------|-----------|----------------|----------------------------|
| **IV** | Mechanical / pilot-controlled ditch | **0.30** | **0.85** — best match to safe crew + lost airframe |
| **III** | SAM / AAA / MANPAD / **FPV** (not Shahed-136) | **0.25** | **0.35** — kill possible; survival varies by hit |
| **II** | Graze / partial Shahed coupling / mislabel / dud | **0.20** | **0.40** — reconciles “Shahed” leak with survivors |
| **V** | Accidental Shahed path intersection | **0.17** | **0.15** — rare hit; graze survival possible |
| **I** | Deliberate Shahed-136 terminal + warhead function | **0.08** | **~0.005** — joint hit × survive from table above |

Priors reflect **pre-audit** theatre base rates (helo ops risk, mixed ordnance environment, low Iranian incentive to waste coordinate cruisers on Apaches). **I** is non-zero only for **leak + Trump** tail — physics keeps it small.

### Posterior sketch (unnormalized → normalized)

| Class | Prior × likelihood | **Posterior (approx.)** |
|-------|-------------------|-------------------------|
| **IV** Mechanical | 0.30 × 0.85 = **0.255** | **~57%** |
| **III** SAM / FPV / other | 0.25 × 0.35 = **0.088** | **~20%** |
| **II** Graze / mislabel Shahed | 0.20 × 0.40 = **0.080** | **~18%** |
| **V** Accidental Shahed path | 0.17 × 0.15 = **0.026** | **~6%** |
| **I** Deliberate Shahed terminal | 0.08 × 0.005 = **0.0004** | **~0.1%** |

Normalizer ≈ **0.449** → posteriors sum to 1.

**Read:** Conditioning on **safe crew** + physics joint test collapses **I** to **rounding error**. Residual mass sits on **IV**, then **III** / **II** (reconciles Pentagon “Shahed” shorthand with outcomes). **Trump attribution** moves **policy** and **Qeshm timing**; it does **not**, by itself, move posterior mass into **I** without ordnance proof.

### What moves posteriors (evidence hooks)

| New evidence | Class gain |
|--------------|------------|
| Shahed fragments + terminal blast pattern on wreckage | **I** or **II** ↑ |
| Confirmed SAM/AAA/FPV engagement geometry | **III** ↑ |
| Pilot / maintenance mechanical statement | **IV** ↑ |
| CENTCOM names weapon + intercept vs collision | Resolves **II** vs **I** vs **V** |
| Iranian track + launch point showing hover trap | **I** ↑ (still faces energetics test) |

---

## Pretext chain (mechanical ditch → attribution → strikes)

**Leading hypothesis (WORK; not Record):** Two linked bundles — keep **causal** and **political** separable.

### Causal bundle (what likely happened)

| Step | Bench | Confidence |
|------|-------|------------|
| Apache **lost** on Hormuz/Gulf patrol | CENTCOM; crew rescued via sea drone | **Supported** |
| **Semi-controlled ditch** after mechanical or pilot-induced failure | Outcome shape (safe crew); Davis in-voice | **Leading** — **IV ~57%** posterior |
| **Not** deliberate Shahed-136 terminal kill | Joint P **~10⁻⁵**; **I ~0.1%** posterior | **Strong skepticism** |

Davis breaking: evidence described sounds **most plausible** as **mechanical error**; Shahed point-to-point vs maneuvering A64 **implausible**; pilots safe **inconsistent** with large warhead terminal hit. **Krapivnik** (ex-guard Apache attack battalion): same energetics — **no eject**, brick-fall, canopy-only egress; **“bull crap”** on uninjured crew after real terminal hit; **stronger** guest line that event may be **fabricated** — **overruns wire** (CENTCOM down + rescue **supported**); keep as **tier-4 mechanism stress-test**, not causal floor.

### Political bundle (how the event was used)

| Step | Bench | Confidence |
|------|-------|------------|
| Cause lane left **contested** (investigation → Pentagon leak tier → presidential line) | WaPo / CNN-CBS / Axios seam | **Supported** |
| Trump: Iran **shot down** Apache; **response as we speak** (Carl ABC readout) | Davis breaking transcript | **Supported** (attribution **choice**, not ordnance proof) |
| CENTCOM evening strikes — **proportional response** to Apache down | Davis: Qeshm, Sir Port, Bandar Jask, Bandar Abbas area, Minab — up to **five** base areas | **Supported** at reporting tier; **disproportion** read open |
| MOU / Hormuz reopen path **at risk** | Marandi + admin voices in same tape | **Developing** |

**Mechanism (compressed):**

```
Mechanical ditch (outcome-favored)
  → ambiguous morning cause lane
  → presidential reframe (Iran shot it down)
  → CENTCOM strike package with “proportional response” wrapper
  → diplomacy / deal floor further stressed
```

### Why Iran denial fits both layers

Araghchi / Marandi military sources: forces did **not deliberately** target the U.S. helicopter. Consistent if **(a)** no Iranian anti-helo engagement occurred, and **(b)** Tehran refuses to own a casus belli it did not plan.

### What “pretext” means here (limits)

- **Does not** require proved conscious lie — may be leak consensus, genuine belief, or institutional momentum.
- **Does** mean **attribution sufficiency for strikes** may have been **lower** than ordnance proof would require.
- **Not settled** without wreckage, blast pattern, pilot statement, CENTCOM weapon + geometry readout.

**Daily floor:** **Physics favors accident; politics favored retaliation anyway.** Do not write “Iran shot down Apache” as settled fact.

### Falsifiers (pretext-specific)

| Observation | Effect |
|-------------|--------|
| Shahed fragments + terminal blast on airframe | Causal bundle shifts off **IV**; pretext may still have operated on thin evidence |
| Pilot / maintenance mechanical statement | **IV** ↑; strengthens full two-bundle read |
| CENTCOM documents intercept geometry + ordnance | Resolves causal class; tests whether strikes tracked proof or narrative |
| Strike list judged proportional on damage/aimpoints | Weakens **disproportion** limb of political bundle |

---

## C. Speaker / wire fork

**Shared observable bench (wire-partial, 8–9 Jun):**

- Apache down near Hormuz / Gulf of Oman — **supported** (CENTCOM; 2 pilots rescued, sea drone).
- Cause — **unclear** (WaPo investigation → Trump shootdown → CNN/CBS Pentagon **Shahed** → Axios **collision** framing; CBS: intent **not established**).
- Iranian official line — **non-deliberate** / deny (Araghchi; Gharibabadi; Marandi morning military sources).
- Outcome — **ditch + rescue**, Trump **safe and uninjured**.
- **9 Jun evening strikes** — CENTCOM **self-defense** 5 p.m. ET; **Sirik, Qeshm, Jask, Bandar Abbas** area — **supported** ([CBS live](https://www.cbsnews.com/live-updates/iran-war-trump-peace-deal-israel/) · [Xinhua](https://english.news.cn/20260610/2e6492ae896148b88558018001867614/c.html)); Fox **3b** mid-strike “ongoing” on radars vs later **completed** read — **timeline partial**.

| Lane | Strongest claim | Physics fit | Load-bearing |
|------|-----------------|-------------|--------------|
| **Davis** (breaking) | Shahed **cannot** pursue; **not navigable** for air targets; **50 kg HE** ⇒ no survivors; **mechanical** more plausible | **Strong** on energetics; **overstates** “cannot intersect path” (collision ≠ chase) | **Outcome vs warhead** |
| **Aguilar** (Nima) | If Shahed hit, **“nothing left”**; but **FPV precision** one-way drone **upping game** | **Agrees** on lethality; **conflates** Shahed-136 with **FPV** class | Lethality yes; platform ID shaky |
| **Krapivnik** (Nima, ex-guard Apache battalion) | Apache **no glide / no eject**; Shahed in Hormuz patrol = **“past stupid”**; pilots safe after hit = **“bull crap”**; **does not believe Apache happened** | **Strongest** on **crew-survival vs terminal HE**; **MANPAD vs Shahed** swap plausible in guest voice; **event-denial** line **contradicts** CENTCOM down row | **Energetics + pretext skepticism** |
| **CNN/CBS** (via Davis cite) | Pentagon sources: **Shahed** downed Apache | **Poor** vs survivors unless graze / mislabel / no detonation | **Wire-partial** (intent open) |
| **Trump** | Iranians **shot down** Apache; must respond | Policy trigger, not physics proof | Escalation **permission** |
| **Araghchi / Marandi** | **Not deliberate** / deny | Consistent with **low P** deliberate Shahed intercept | Diplomatic seam |

### Krapivnik guard-battalion fork (third voice)

**Credential (in-voice):** enlisted **Apache attack battalion**, U.S. Army Guard — not forensic ordnance proof, but **platform survival grammar** load-bearing.

| Krapivnik claim | Physics / wire read |
|-----------------|---------------------|
| Main rotor stop ⇒ **brick fall**; no side doors; **canopy pop** only egress | **Supported** vs AH-64 design — tightens **P(survive \| terminal hit)** |
| **~500 ft** controlled collapse with **uninjured** crew after Shahed warhead | **Contradicted** at guest certainty — aligns **IV / graze** not **I** |
| Shahed-136 too **slow** for anti-helo; **Stinger/MANPAD** class more plausible than coordinate cruiser | **Aligns** with closure worksheet; guest **rejects** CNN Shahed without naming alternative ordnance |
| Patrol Apache in Hormuz = **tactically absurd** (terrain-masked Hellfire role) | **Mechanism context** — supports **pretext / misplacement** read; does not disprove **down** |
| **“Don’t believe Apache even happened”** | **Overreach** vs **wire-supported** loss + rescue — treat as **rhetorical escalation**, not bench fact |
| Trump **sixth** deal-walkaway; strike list Sirri/Jask/Bandar Abbas at interrupt | **Policy bundle** — matches CENTCOM package; reinforces **political** half of pretext chain |

**Compression:** **Physics + outcomes** favor **skepticism of “Shahed terminal kill”** (**Davis · Aguilar · Krapivnik** agree on lethality; Krapivnik adds **strongest crew-survival impossibility** and **casus-belli fabrication suspicion**). **Aguilar** and **CNN** still disagree on **platform class** (FPV vs Shahed). **Wire** has not closed **ordnance + geometry + blast**; **strikes package** is **settled**, **Fox “over”** is **timeline-partial**.

---

## Outcome classes (physics-allowed)

| Class | Mechanism | P(rough) | Fits “crew safe”? |
|-------|-----------|----------|-------------------|
| **I** | Full Shahed terminal + warhead function on airframe | Very low per sortie | **Poor** |
| **II** | Graze / rotor strike / partial coupling / dud | Low | **Maybe** |
| **III** | Different weapon (SAM, AAA, MANPAD, FPV) | Unknown | Varies |
| **IV** | Mechanical / pilot ditch | Independent of Iran | **Yes** |
| **V** | Accidental path intersection (no warhead intent) | ~10⁻⁷–10⁻⁹ | Possible without HE kill |

**Daily floor rule:** Do **not** write “Shahed shot down Apache” as settled without **wreckage / ordnance ID / engagement geometry**. Safe label: **Apache down; cause contested; joint P(Shahed terminal hit ∧ crew safe) ~10⁻⁵ (generous); Bayesian posterior on deliberate Shahed terminal ~0.1% given current bench.**

---

## Falsifiers

| Observation | Effect |
|-------------|--------|
| Shahed fragments + blast pattern on airframe | **I** or **II** rises; Davis skepticism weakens |
| Confirmed SAM/AAA/FPV class | Fork shifts off Shahed-136 |
| Pilot/maintenance statement (mechanical) | **IV** rises |
| Track + launch point + time → closure <100 m with hover | Deliberate intercept **possible** but still energetics test |
| CENTCOM names weapon + geometry (collision vs intercept) | Wire can close **S2** |

---

## Best next moves

1. **`fact-check`** — Apache cause only (ordnance, CENTCOM readout, satellite).
2. Update [news-verify matrix](statecraft/notes/wire/2026-06-08-09-news-verify-matrix.md) **S2** when receipts land.
3. Hold **Qeshm proportional-strike** synthesis on **S2** until cause or damage row firms.

---

## Receipt

| Field | Value |
|-------|-------|
| **Physics fork** | Shahed-136 anti-Apache intercept **low P**; **joint hit × survive ~10⁻⁵** (generous) |
| **Sensors** | **RWR null** (passive guidance); FLIR/Longbow **possible see, not air-defense cueing** |
| **Bayesian fork** | **IV ~57%** · **III ~20%** · **II ~18%** · **I ~0.1%** (WORK priors; update on ordnance) |
| **Leading hypothesis** | Mechanical ditch → attribution pretext → Qeshm evening strikes — **not settled** |
| **Bench agreement** | Davis + Aguilar + Krapivnik on **lethality / survival tension**; split on **platform** (FPV vs Shahed vs MANPAD); Krapivnik adds **event-skeptic** pole (fence vs CENTCOM) |
| **Wire** | **S2 contested** (cause) · **9 Jun strike package supported** (Sirri/Qeshm/Jask/Bandar Abbas) |
| **News-verify sub-hook** | 2026-06-10 — Krapivnik interrupt strikes; see chat receipt |
