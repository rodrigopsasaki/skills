---
name: evolution-loop
description: >-
  Run a bounded evolution loop to grow ONE capability toward a
  judgment-scored fitness. A handful of rounds; each round is one
  deliberate, best-effort change exposed to real feedback, and the next
  round is discovered from what the last one taught — never planned in
  advance. Use when the user wants to deliberately evolve or mature a
  capability (a detector, prompt, agent, eval, classifier, model, ranking,
  or piece of writing) against a real corpus over several rounds — often
  phrased as a "5-iteration exercise", "evolution experiment", "N-round
  loop", or "let's evolve X". NOT for one-off fixes, generic refactors, or
  chasing a metric.
---

# The evolution loop

A bounded loop for growing **one capability** into the best version of
itself. A handful of rounds — five is the canonical budget. Each round you
make the capability the sharpest thing you can currently justify, run it
against real material, and compare to the round before. What you learn
breeds the next round.

It is **not** a benchmark and **not** metric-optimization. Read the fitness
section below — it is the single most important thing to get right.

## Why "loop", not "iteration"

"Iteration" mis-cues everyone — humans and models alike — toward a small
incremental tweak, and toward a pre-planned sequence of them. This is
neither.

- Each round is the **best foreseeable change under scrutiny** — the boldest
  move you can currently defend, implemented fully, then exposed to reality.
  Not a sketch, not a hedge, not a safe delta.
- The sequence is **discovered, not planned**. The next round does not exist
  until this one has run. You are doing variation under selection: propose,
  let reality judge, breed the next variant from what you just learned.

If you catch yourself writing out rounds 2 through 5 in advance, stop. That
is the exact anti-pattern this loop exists to prevent.

## Fitness — the thing you are actually maximizing

Pick **one concrete question, scored by judgment**, and hold it constant
across every round. Not a metric. A question you can answer honestly by
looking at the output, phrased in terms of the real goal:

> "After this change, could I do the downstream work safely from this output
> alone?" · "Would this catch the thing a careful reviewer would catch?" ·
> "Does this now say what it means?"

Then:

- **Convergence is the signal, not a number.** The win is when what the
  system surfaces matches what *you* already know to be true when you look at
  the material yourself. That convergence is what makes it trustworthy.
- **Do not optimize a proxy.** If a change makes a number look better but
  doesn't make the capability genuinely more useful — or worse, games the
  number — it failed. The score going *up* is not the goal; the score being
  *honest* is.
- **Trust your taste.** You have free range on direction. Evolve where it
  feels wanting. Your judgment about where it's lacking is part of the
  experiment, not noise to be eliminated.

Score each round on a couple of 0–3 axes if it helps, but the axes serve the
question — never the reverse.

## The loop, per round

1. **Understand what to improve.** Look at the current output through the
   fitness lens. What would make it sharper, more honest, better calibrated,
   more prepared? Pick the highest-leverage move.
2. **State a hypothesis.** "X should happen because Y." Write it down *before*
   you run. This is what makes "compare to the previous round" mean something
   — otherwise you're just watching numbers move.
3. **Implement the best possible version of that one change.** The real
   thing, not a placeholder. Clean enough to keep.
4. **Run it against the corpus.**
5. **Compare to the previous round, then branch:**
   - **Hypothesis held, it evolved** → write the round up, breed the next
     round from what you now see.
   - **Hypothesis failed** → **diagnose.** This is where the real work is
     (see below). Fix it and re-run. **The fix-and-retry counts as the next
     round** — a round spent diagnosing is a legitimate round.

## The rules that make it work

These are load-bearing and learned the hard way. Skipping them turns the
loop back into aimless tweaking.

- **Round 0 is the baseline — the *current* capability, unchanged.** Run it
  first, score it, and let that data reveal the headroom. The baseline's
  headroom is what *picks* round 1. Round 0 is not your first change; it's
  the "before" that every later round compares against.

- **The next round does not exist until this one has run.** Each result
  picks the next single change. The emergent pivots are the entire value —
  pre-planning the arc forecloses the learning and usually optimizes the
  wrong thing.

- **Your best idea IS the next round — don't sandbag it.** If you're holding
  a "best solution" for a later slot, that solution is the *next* round,
  fully realized. Implement it now. (The classic mistake is mislabeling your
  best idea as a modest round 0.)

- **One change per round.** Machinery carried over from prior validated
  rounds doesn't count as "the one change" — but don't stack two new bets in
  a single round, or you won't know which one moved the needle.

- **Genuine-vs-mistake is the central discrimination.** A regression or a
  surprising result is *not* automatically a bug. Before you react, ask: is
  this **the world actually being like this** (the finding stands — surfacing
  it honestly *is* the result), or **my own mistake** (a bug in the detector,
  a misread, a bad query — fix it)? Most of the loop's value lives in telling
  these apart. Fix mistakes; keep findings.

- **`unknown` is its own state.** Absence of evidence is not confirmation of
  absence — "found no X" is not "there is no X." Don't falsely confirm
  either. Never silently fold `unknown` into "pass" or "fail"; weight it as
  the unknown it is.

- **Convergence is when to stop or pivot.** When consecutive rounds add
  nothing, you've converged on this target — say so, and either stop or pivot
  to a new target. Five is a **budget, not a quota**. Don't manufacture
  motion to fill slots.

- **Report honestly, dull outcomes included.** A round where nothing moved
  because "the material genuinely has none of what we're looking for" is a
  valid, valuable round — say so. Regressions, no-ops, and "the assumption
  failed against reality" are results, not failures to hide.

- **Keep the noisy part at the edge.** Where you can, make the core
  deterministic and idempotent so rounds are actually comparable; quarantine
  anything stochastic (an LLM call, a sampled input) at the boundary. If a
  re-run gives a different answer, you can't compare rounds.

## Deliverables

1. **A dated log** — `YYYY-MM-DD-<name>-evolution.md` — structured:

   ```
   # <capability> — evolution loop

   ## Premise            what we're growing, and why now
   ## Fitness            the concrete question; what "better" means here
   ## Round 0 — baseline the current capability, scored; the headroom it reveals

   ## Round 1
     Change       the one move
     Hypothesis   X should happen because Y
     Result       what actually happened vs the hypothesis
     Diagnosis    (only if it failed) genuine finding, or my mistake?
     Next         what this round tells the next one to be

   ## Round 2 … (same shape)

   ## Closing synthesis  what it proved; the open edges left honest
   ```

2. **The matured capability**, clean enough to keep.

3. **Saved raw output per round** (e.g. `round-N.log`), so comparisons
   survive later changes to the underlying data. "Latest" moves; your
   evidence shouldn't.

## When NOT to use this

- A one-off fix or a single well-understood change. Just make the change.
- Chasing a metric or a benchmark score. This loop optimizes *honest
  usefulness*, judged by you — a number is at best a secondary signal.
- A roadmap you already know. If you can write all the steps in advance, you
  don't have an evolution loop, you have a plan — go execute it.
