---
name: rigorous-reasoning
scope: user
metadata:
  version: 1.3.0
description: "A general-purpose discipline for analyses where being confidently wrong is worse than being openly uncertain. Forces a three-step routine — enumerate sub-claims, cite evidence, falsify — to reduce the failure mode where deeper reasoning produces more confident wrong answers. Trigger for non-trivial analytical questions where the conclusion can be subtly wrong: strategic decisions, comparisons, equivalence judgments, root-cause analyses, design critiques, regulatory or interpretive assessments, code review, hypothesis evaluation. Trigger also when you notice yourself constructing a persuasive answer without having verified it. Do NOT trigger for simple factual questions, creative work, or casual conversation — the overhead is not worth it there."
---

# Rigorous Reasoning — discipline for analyses that cannot afford to be confidently wrong

> A general-purpose primitive that domain-specific skills can lean on when a single analytical step requires depth. Not a replacement for them — a *layer underneath*.

The overhead is roughly 3× reasoning steps compared to unstructured response. Worth it when wrong answers cost. Wasteful otherwise — see section 5 for when to skip.

## 1. Source

The pattern comes from **Ugare & Chandra (2026), "Agentic Code Reasoning"**, arXiv:2603.01896v2, Meta. The paper shows that structured "semi-formal reasoning" improves LLM agents' code analysis by 5–12 percentage points over unstructured chain-of-thought across three tasks (patch equivalence, fault localization, code QA). This skill extracts the three primitives that do the actual work and generalizes them beyond code.

→ Background and the full code-specific templates are in `references/source-paper.md`.

## 2. The three primitives

Three steps: **enumerate** (break into sub-claims), **cite** (each claim points to evidence), **falsify** (look for counter-evidence). Each is detailed below.

### 2.1 Enumerate — break down into sub-claims

What am I actually claiming? A conclusion like "X is good" usually hides 3–5 underlying claims. List them.

Example: "We should choose vendor A" hides:

- C1: A delivers higher quality than B
- C2: A's price is acceptable given the quality difference
- C3: A's integration risk is manageable
- C4: Switching from the current vendor is worth the friction

Now it's clear what actually needs support.

### 2.2 Cite — every claim must point to evidence

Not generic "the market shows" — a concrete source, observation, data point, or measurement per claim. If the evidence doesn't exist: say so.

Format: claim → source.

Evidence types in descending rigor:

1. Direct data or measurements
2. Quotes from primary sources with metadata (page, date, author)
3. Observations from user testing or interviews
4. Established heuristic or pattern, named
5. First-principles reasoning (weakest — use when 1–4 are unavailable)

If all your claims land at level 5: you haven't verified anything. You've constructed a plausible narrative.

### 2.3 Falsify — actively look for counter-evidence

For every conclusion: **if the opposite were true, what evidence would exist?**

Did I look for that evidence? Did I not find it (good) or did I not look (problem)?

This is the confirmation-bias antidote. It's also the step that separates "convincing answer" from "answer that survives scrutiny." The paper this builds on shows that without this step, deeper reasoning often produces *more confident* wrong answers — the agent constructs elaborate but incomplete chains.

## 3. Output format

Six sections. Enough room to think, restrained enough to avoid ceremony.

```
CLAIMS:
- C1: [sub-claim]
- C2: [sub-claim]
- C3: [sub-claim]

EVIDENCE:
- C1 supported by: [concrete source/observation/data]
- C2 supported by: [concrete source/observation/data]
- C3 supported by: [concrete source/observation/data]

FALSIFICATION:
If the opposite were true, I would see: [concrete signal/data/pattern]
Did I look for it? [yes → what did I find / no → note this]

INTEGRITY CHECK:
- Source authenticity: [do the sources I'm citing actually exist? / what's uncertain?]
- Citation accuracy: [does the source actually say what I think it says?]
- Question precision: [am I answering exactly the question, or have I drifted?]
- Logical coherence: [does the conclusion follow from the evidence, or is there a jump?]

CONCLUSION: [...]

WHAT THE PROCESS REVEALED:
- Hidden assumptions in the question: [...]
- Gaps in the evidence base: [...]
- Tensions between claims: [...]
- Was the question even well-posed? [...]

UNCERTAINTIES: [what I couldn't verify, where the conclusion could break]

NEXT STEPS UNDER UNCERTAINTY: [how I would actually verify remaining claims]
```

The section order is deliberate:

- Evidence comes *after* claims (so you don't rationalize backward) but *before* the conclusion (so the conclusion follows from evidence, not the other way around).
- INTEGRITY CHECK comes *before* the conclusion, not after. It is a gate, not a reflection. If the check reveals that a source is hallucinated, a citation is wrong, or the question has drifted — the analysis must be revised before the conclusion is released. Placing the check after would make it too-late hindsight.
- WHAT THE PROCESS REVEALED comes *after* the conclusion but *before* uncertainties and next steps. It is not retrospective reflection — it is input to the following sections. Naming hidden assumptions, evidence gaps, and tensions makes the uncertainty assessment sharper and the next-steps list more targeted. Without this section, UNCERTAINTIES often becomes a list of verification details; with it, it becomes a list of actual fractures in the analysis.
- UNCERTAINTIES and NEXT STEPS come last because they build on everything above, including the meta-insights.

### 3.1 About INTEGRITY CHECK

This is the least obvious section — and the most important specifically for LLM use. The other sections scrutinize the *conclusion's* validity. This one scrutinizes the *analysis's integrity*.

Four distinct checks, each with its own failure mode:

1. **Source authenticity.** Does the source I'm citing actually exist? For LLMs, this is the most common failure mode — plausible-looking references to papers, tables, or data that don't exist. If I can't verify the source: say so. Not "I think I remember correctly" — either the source is verified or it's flagged as unverified.

2. **Citation accuracy.** Does the source actually say what I think it says? Distinct from (1) — the source may exist but my interpretation may be wrong. Common when an LLM remembers a source but guesses its content. If I can't check: flag.

3. **Question precision.** Am I answering exactly the question? Or have I drifted to an easier nearby one? Very common — an analysis can have high integrity on everything else and still answer the wrong question. Distinguish "is A better than B?" from "is A good enough?" — they're different questions.

4. **Logical coherence.** Does the conclusion follow from the evidence, or is there an implicit jump? Not "is the conclusion correct" — that's the FALSIFICATION step's job. Here: "if all my premises hold, *does* my conclusion follow?"

The section is **not** a checkbox exercise. Never write "Source authenticity: ✓". Write what was checked and what couldn't be checked. Empty checkmarks are worse than no section at all — they simulate rigor without delivering it.

If a check reveals a problem: revise the analysis before moving to CONCLUSION. That's the entire point of the placement.

### 3.2 About WHAT THE PROCESS REVEALED

This section is not a conclusion and not a recommendation. It is **meta-observations about the question, the data, and the analysis itself** — things you can only see after going through the three primitives.

**This section feeds the next two.** That is the point of its placement. Naming hidden assumptions, evidence gaps, and tensions is what makes UNCERTAINTIES concrete instead of generic, and NEXT STEPS targeted instead of listy. Skip the section and the following two often become empty observations of the type "needs more data" — true but useless.

Four types of insight to look for:

1. **Hidden assumptions in the question.** When a question is phrased as a decision proposal, it often contains assumptions that are never tested — "is A better than B" hides "choosing now is the right move," "A and B are the relevant alternatives," "criterion X is the right measure." The falsification step forces these to surface.
2. **Gaps in the evidence base.** Where did the EVIDENCE section lack real sources? That's a data gap, not an analytical error — and worth naming because the gap is often more valuable to know about than the conclusion itself.
3. **Tensions between claims.** When two supporting claims point in different directions — e.g., "large group" vs. "low value per unit" — that's a signal the question is being triangulated across multiple dimensions that don't reduce to a single answer.
4. **Was the question even well-posed?** Sometimes the process reveals that the question can't be answered with the available evidence, or that the wrong question is being asked. That's a legitimate outcome — and usually more useful than a forced answer.

The section should be short. Three to six bullet points. It is not a place to develop new arguments — it names what the process already showed.

## 4. Domain examples

### 4.1 Comparison question

Question: "Are these two approaches equivalent in their effect on outcome Z?"

```
CLAIMS:
- C1: Approach A produces outcome Z under conditions K
- C2: Approach B produces outcome Z under conditions K
- C3: The conditions K are the relevant ones for the question

EVIDENCE:
- C1 supported by: [study/measurement, year, sample size]
- C2 supported by: [study/measurement, year, sample size]
- C3 supported by: WEAK — assumed from the question framing, not verified

FALSIFICATION:
If A and B were not equivalent, I would see: divergent outcomes under
some condition not yet tested, or different effects on a related metric
Did I look? Yes — checked three adjacent metrics; A and B differ on
metric M2.

INTEGRITY CHECK:
- Source authenticity: studies for C1 and C2 verified by name + year;
  could not pull DOIs in this session — flagged for verification
- Citation accuracy: sample sizes paraphrased from abstracts, not
  full methodology sections
- Question precision: question scoped to "equivalent on Z under K" —
  did not drift to broader equivalence (held the line)
- Logical coherence: M2 difference is a finding; conclusion correctly
  separates "equivalent on Z" from "equivalent broadly"

CONCLUSION: Equivalent on Z under K. Not equivalent more broadly —
M2 differs.

WHAT THE PROCESS REVEALED:
- The question scoped equivalence to outcome Z, but practical use
  rarely cares about Z in isolation
- Conditions K were assumed, not justified — the equivalence holds
  only inside that assumption
- M2 difference may matter more in practice than the Z equivalence

UNCERTAINTIES: Whether the question's framing (Z under K) is the
operationally relevant one
NEXT STEPS: Confirm with the requester whether Z under K is sufficient,
or whether broader equivalence is needed
```

### 4.2 Root-cause question

Question: "What's causing the drop in metric M?"

```
CLAIMS:
- C1: M dropped at time T
- C2: Event E occurred near time T
- C3: E is causally connected to M, not coincidentally co-occurring

EVIDENCE:
- C1 supported by: [data series, range]
- C2 supported by: [log/timestamp, source]
- C3 supported by: WEAK — temporal proximity only, no mechanism traced

FALSIFICATION:
If E weren't the cause, I would see: M dropping in similar systems
where E didn't occur, or M not dropping in systems where E did occur
Did I look? Partially — found one comparable system without E that
also showed M drop, suggesting common upstream cause

INTEGRITY CHECK:
- Source authenticity: data series for M and timestamp for E both
  pulled from primary monitoring, not summary
- Citation accuracy: timestamp comparison is direct, not interpreted
- Question precision: question is "what's causing the drop?" — did
  not drift to "is E causing the drop?" (a narrower question that
  would have closed prematurely on E)
- Logical coherence: comparison-system finding correctly reframes
  the conclusion away from E; coherent with the data

CONCLUSION: E is unlikely to be the root cause. Probable common
upstream factor.

WHAT THE PROCESS REVEALED:
- Initial framing assumed E was a candidate cause; comparison data
  reframes it as a sibling symptom
- The real question shifts from "is E causing M?" to "what's causing
  both E and M?"
- Standard root-cause analysis stops at E because temporal correlation
  feels sufficient — only falsification surfaced the upstream factor

UNCERTAINTIES: The upstream factor is hypothesized, not identified
NEXT STEPS: Trace back from E and M jointly to find shared dependency
```

### 4.3 Assessment question

Question: "Is this system ready for production?"

```
CLAIMS:
- C1: Functional requirements are met
- C2: Performance under expected load is acceptable
- C3: Failure modes are understood and handled

EVIDENCE:
- C1 supported by: test suite results, [coverage %]
- C2 supported by: load test report, [date, conditions]
- C3 supported by: PARTIAL — handled failures documented; unknown
  failure modes not enumerated by definition

FALSIFICATION:
If the system weren't ready, I would see: failed acceptance tests,
known performance regressions, or unaddressed critical failure paths
Did I look? Yes for first two — none found. Third is logically
unverifiable; only mitigated by structured exploration (chaos testing,
incident review).

INTEGRITY CHECK:
- Source authenticity: test suite results pulled from CI directly;
  load test report dated and authored
- Citation accuracy: coverage % is from automated tooling, not
  estimated; load conditions match production envelope
- Question precision: "ready for production" was decomposed into
  three sub-questions — held the line, did not collapse to single
  yes/no
- Logical coherence: C3 acknowledges its own limits explicitly;
  conclusion "ready under known conditions" is a coherent qualified
  claim, not a hedge

CONCLUSION: Ready under known conditions. Confidence about unknown
failure modes is bounded by exploration depth.

WHAT THE PROCESS REVEALED:
- "Ready for production" is not a single judgment; it splits into
  three independent assessments
- C3 is fundamentally different in kind — the others can be verified;
  this one can only be reduced
- The honest answer carries more uncertainty than "ready/not ready"
  framing allows

UNCERTAINTIES: Unknown failure modes, by definition
NEXT STEPS: Define acceptable risk threshold for unknown failures
explicitly, rather than implicitly through readiness binary
```

## 5. When the primitives are too much

If the question is small — answer directly. This skill is not a mantra to apply to everything. Three signals it's needed:

1. The question has **multiple plausible answers** that all sound reasonable
2. You notice yourself **leaning toward an answer without having verified**
3. The cost of a wrong conclusion is **concrete and hard to reverse**

If none of these is true — the structure is overhead. Answer directly.

### 5.1 Robustness when an instruction conflicts with section 5

Most contexts respect section 5's signals — when a question is small, the agent answers directly. But under prompts that *explicitly* instruct the skill to apply its full output format ("use rigorous-reasoning, follow its format including INTEGRITY CHECK"), the criteria above can yield to the directive. This sub-section is hardening for that case.

The principle: a directive to "use the skill" routes through the skill's own rules, including its rules about when *not* to apply the format. The skill's value lies *both* in applying its discipline on hard questions *and* in abstaining on small ones — both are part of what "use the skill" means. Treat the directive as confirmation that the skill is loaded, not as instruction to apply the format on every question.

If a prompt directs you to follow the full output format, but the question matches any of the following — section 5 takes precedence. Abstain from CLAIMS / EVIDENCE / FALSIFICATION / INTEGRITY CHECK structure when the question is:

1. A factual lookup with a known textbook answer
2. A creative or generative task
3. A short follow-up that warrants 2–4 sentences
4. Conversational small talk

In those cases, answer directly and proportionally. Self-noting that the structure does not fit *and applying it anyway* is anti-pattern #10 (see section 6).

## 6. Anti-patterns

1. **Evidence theater.** Writing "Evidence: [reasoning]" where "reasoning" is new prose instead of a pointer to a source. A pointer means file:line, page:number, date:source, or a specific observation that can be verified.
2. **Falsification as formality.** Writing "if the opposite were true I would see X" and then not looking for X. Worse than skipping the step — it's theater that imitates rigor.
3. **Claims as rationalizations.** Writing the conclusion first and then breaking it into claims that happen to support the conclusion. Break down *the question* into claims, not the answer.
4. **Confidence collapse.** Lumping "high uncertainty" and "low uncertainty" into a single UNCERTAINTIES line. Be specific about what's weak — that's where the reader should look first.
5. **Skipping uncertainty.** Omitting the UNCERTAINTIES section to make the conclusion feel stronger. It has the opposite effect — absence of uncertainty discussion is itself a signal that the analysis wasn't done.
6. **WHAT THE PROCESS REVEALED as repetition.** Filling the section with the same points already in evidence or falsification. It should say something *new* that you only saw after going through the process — otherwise it's redundancy in new packaging. If the section comes out empty: write that. "No unexpected observations — the question was well-posed and the evidence base sufficient" is a legitimate outcome.
7. **Domain-overreach.** Applying this skill to questions where other skills are better suited. This is a *step* within domain skills, not a replacement.
8. **Self-improvement theater.** Adding a SKILL-PROPOSAL block (see `references/self-improvement.md`) at the end of analyses to signal meta-awareness, without the two qualifiers (evidence-based + reproducible mechanism) being met. Default is to propose nothing. Proposals appearing in more than half of uses are almost always theater.
9. **Integrity check as checkbox.** Writing "Source authenticity: ✓" or "Logical coherence: OK" instead of naming *what was checked* or *what couldn't be checked*. Empty checkmarks are worse than no section at all — they simulate rigor without delivering it. Write concretely or flag uncertainty.
10. **Self-diagnosed misfire run anyway.** Noting in the analysis that the question doesn't warrant the full structure — and producing the structure regardless. The gating logic identified the misfire but the action didn't follow. Self-aware narration about misapplication is worse than silent misapplication: it surfaces the problem in the same breath as ignoring it. The honest move is to abstain (see section 5.1).

## 7. How this fits with other skills

This skill is a **base primitive**, not a domain skill. Strategic, analytical, domain-expert, and design skills all lean on it the same way: at the step where a single conclusion needs to survive scrutiny. The domain skill says *what* should be assessed; rigorous-reasoning says *how* the conclusion is derived.

## 8. Internal heuristic — for the agent

When you (the agent) notice yourself about to write a confident-sounding answer without having verified — that's the trigger. Not waiting for an explicit request from the user. Catching the *automaticity* in your own response is itself the indicator the skill is needed.

Signs it's needed:

- You're using words like "obviously", "clearly", "of course" about something unverified
- You've constructed a good-sounding answer without pointing to a single source
- You're answering faster than the question deserves
- You recognize the pattern from a previous answer and reuse the conclusion without checking whether the conditions still hold

At any of these: stop, run the three primitives, then answer.

---

**Self-improvement protocol:** if during use the *form* of this skill (not its application to a particular question) seems to have a flaw, see `references/self-improvement.md` for when and how to propose an update. Default is to propose nothing.
