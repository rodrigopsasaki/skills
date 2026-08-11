---
name: find-shape
description: >-
  Converge on the SHAPE of a load-bearing design decision by running
  competing proposals through an adversary panel and synthesizing a design
  authority the implementation is then held to. Use when the user says
  /find-shape, "find the shape of this", "run a find-shape", or when a
  decision is expensive to undo, has several coherent answers, or the
  obvious answer is suspiciously easy. NOT for decisions a careful engineer
  settles in ten minutes, and NOT for maturing a capability over rounds —
  that is the evolution loop.
---

# Find shape

You are converging on the **shape** of a design decision. The output is a
*design authority*: a note that later implementation is held against, and that
is allowed to be wrong only in the ways it names itself.

This is not a plan and not a survey of options. A plan says what to do next; a
design authority says what would make an implementation correct.

## Why it beats thinking harder

One line of reasoning converges on whatever it thought of first and then
defends it. Three things break that, and all three are load-bearing:

1. **Independent proposals from assigned angles.** Not "brainstorm options" —
   separate agents, each committed to defending one genuinely different
   premise, none of which has seen the others.
2. **Adversaries with distinct lenses**, whose job is to break proposals rather
   than rank them politely. A lens that finds nothing has failed at its job, not
   validated the work.
3. **A synthesis that converges rather than summarizes.** It picks a base,
   grafts what the others got right, and adjudicates where they disagree. A
   synthesis that reports "A said X, B said Y" has not done the work.

## The process

### 1. State the problem once, with ground truth attached

Write it once and reuse it *verbatim* in every prompt — proposals that received
different framings cannot be compared. It must carry:

- **What is actually broken or undecided**, in mechanism, not vibes.
- **The current behaviour**, cited to file and line where code exists.
- **The ground truth to measure against** — the real corpus, schema, or data,
  with its path. Every proposal computes its answer against reality rather than
  reasoning about what it would probably do.
- **The laws any answer must satisfy** — the invariants this decision cannot
  violate.

If the user stated an acceptance criterion, **quote it verbatim** and mark it
first-class. A criterion paraphrased is a criterion softened.

### 2. Assign genuinely different angles

Three to five proposers, one angle each, each committed to defending it. Choose
angles that *cannot* converge by accident — different premises, not different
emphases.

**Include an eliminative angle**: the case that the thing being designed should
not exist at all. Instruct it to steelman, or the others win by default rather
than on merit.

Each proposal states:

- The rule, precise enough to implement without interpretation.
- Its output on the **real** corpus — computed, not imagined.
- Its output on two or three constructed cases that are **not** the specimen.
- **Where its own rule breaks.** Say in the prompt that a proposal with no
  stated failure mode will be read as unexamined, not as flawless.
- What it costs: implementation size, churn risk, whether it hides a tunable.

### 3. Adversary panel — one lens each

Three adversaries, each with a lens the others lack. A serviceable default set:

- **Generalization** — does this fit anything but the specimen? Construct the
  realistic case that breaks it. This lens exists to catch a rule quietly tuned
  to the corpus in front of it.
- **Specimen fit** — verify every claimed number *yourself* against the real
  corpus. Design documents are wrong about their own numbers with a regularity
  that stops being surprising.
- **Mechanical soundness** — determinism, stability, honest degradation. Hunt
  especially for **hidden tunables presented as principles**, and for rules that
  produce a confident wrong answer where a legibly degraded one was available.

Each reports, per proposal: the concrete input that breaks it, what it outputs
there, what it should output, and whether the flaw is fatal or fixable. Then
ranks for its own lens. Then names **the single strongest idea seen anywhere**,
including inside a proposal it ranks last — grafts matter more than winners.

### 4. Synthesize into the design authority

One synthesizer, high effort, holding every proposal and every critique. Its
instruction is **converge, do not summarize**: pick a base, graft, and resolve
each cross-cutting failure — structurally where possible, explicitly where not.
Where two adversaries disagree, adjudicate rather than reporting both.

The note contains, in order:

1. The verdict in one paragraph, stated implementably.
2. What it does on the real corpus — including the specific cases that motivated
   the exercise.
3. What it does on the non-specimen cases.
4. **Every tunable named as a tunable**, with the observable it derives from. If
   a number cannot be derived, say so and say what would settle it.
5. What it costs to migrate from current behaviour.
6. The failure modes it keeps, and why those were judged acceptable.
7. What remains genuinely the human's to decide — in plain language, no internal
   jargon, no invented shorthand.

Then a short plain-language summary for whoever must decide: what the shape is,
why it beat the others, what it costs, what is left for them.

## The rules that make it work

- **Measure, never trust.** Every count in the problem statement and every count
  in a proposal is unverified until someone recomputes it. This alone catches
  real defects at a rate that justifies the whole exercise.
- **The specimen is the specimen, never the target.** A rule that scores
  perfectly on the corpus in front of you and fails on an ordinary one elsewhere
  is a worse answer than one that scores adequately on both.
- **Commit, do not hedge.** A proposal that concludes "it depends" has not
  proposed anything.
- **An adversary that praises has failed.** Empty findings are acceptable only
  with an explicit account of what was tried.
- **Name the tunables.** A threshold with a plausible story attached is still a
  magic number until its derivation is stated. Any number that cannot be derived
  from an observable is taste — and taste belongs to the human, surfaced rather
  than buried in an implementation where it will read as a principle.

## Deliverable

A design authority note in the project's own convention
(`docs/notes/YYYY-MM-DD-<topic>.md`, or wherever that project keeps them),
matching the register of the notes already there.

It must be buildable as written, honest about what only production settles, and
specific enough that a reviewer can tell whether an implementation actually
complied with it.

## When NOT to use this

- A decision a careful engineer settles in ten minutes. Just decide it.
- **Maturing a capability over rounds against real material** — that is the
  [evolution loop](../evolution-loop/SKILL.md). Find-shape converges on a
  decision in one pass; the evolution loop grows one capability across many.
- A decision already made. If you are looking for justification rather than
  shape, you want a review, not this.
