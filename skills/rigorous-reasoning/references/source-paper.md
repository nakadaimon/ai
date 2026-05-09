# Source — Agentic Code Reasoning

> Background and traceability for `rigorous-reasoning`. Loaded only when verifying the primitive's origin or examining the original code-specific templates.

## 1. The paper

**Title:** Agentic Code Reasoning
**Authors:** Shubham Ugare, Satish Chandra (Meta)
**arXiv:** 2603.01896v2
**Date:** 4 March 2026
**URL:** https://arxiv.org/html/2603.01896v2

## 2. The paper's core claim

LLM agents can do meaningful semantic code analysis without executing the code — but only if forced into a structured proof template. The technique is called **semi-formal reasoning**.

Measured results across three tasks:

| Task | Standard CoT | Semi-formal | Δ |
|---|---|---|---|
| Patch equivalence (curated) | 78.2% | 88.8% | +10.6pp |
| Patch equivalence (real-world, Opus-4.5) | 87% | 93% | +6pp |
| Code QA (RubberDuckBench, Opus-4.5) | 78.3% | 87.0% | +8.7pp |
| Fault localization (Defects4J Top-5) | 60.5% | 72.1% | +11.6pp |

Cost: ~2.8× more reasoning steps.

## 3. What rigorous-reasoning extracts

The paper describes three **task-specific** templates (patch equivalence, fault localization, code QA). Each template is detailed and code-oriented. Across them, three **shared primitives** do the actual work:

1. **Forced enumeration of sub-claims** — `Comparison: [SAME/DIFFERENT]` per test case, `Claim D1, D2, ...` per divergence, etc. The agent cannot summarize its way out.
2. **Evidence burden per claim** — each claim must cite file:line. Plausibility doesn't count.
3. **Alternative-hypothesis check** — explicit in the code QA template, implicit in the others through the requirement of a counterexample or a proof that no counterexample exists.

`rigorous-reasoning` generalizes these three to domains beyond code by letting "file:line" become "concrete source," "test case" become "sub-claim," and "counterexample" become "falsifying evidence."

## 4. The central example (django-13670)

To understand *why* the structure works — this is the motivating example in the paper.

Two patches for 2-digit year formatting:

```python
# Patch 1
return format(self.data.year, "04d")[-2:]

# Patch 2
return '%02d' % (self.data.year % 100)
```

**Standard CoT:** "Both produce '76' for year 476. Equivalent." Wrong.

**Semi-formal:** The template forces the agent to *trace the `format` call*. It discovers that Django has a module-level function named `format` in `dateformat.py` that shadows Python's builtin. Patch 1 raises `AttributeError`. Not equivalent.

The lesson: structure forces the agent to read, not guess. The same principle generalizes — in strategy, it forces verification rather than assumption.

## 5. The original code templates (reference)

Preserved here for traceability. `rigorous-reasoning` does *not* use these directly — it uses the abstracted three-step form. These are here for anyone who wants to see where the primitives came from.

### 5.1 Patch equivalence (simplified)

```
DEFINITIONS:
D1: Two patches are EQUIVALENT MODULO TESTS iff
    the test suite produces identical pass/fail outcomes.

PREMISES:
P1: Patch 1 modifies [file] by [change]
P2: Patch 2 modifies [file] by [change]

ANALYSIS OF TEST BEHAVIOR:
For each test:
  Claim: With Patch 1, test [name] will [PASS/FAIL] because [trace]
  Claim: With Patch 2, test [name] will [PASS/FAIL] because [trace]
  Comparison: [SAME/DIFFERENT]

COUNTEREXAMPLE (if NOT EQUIVALENT):
  Test [name] produces different outcomes because [evidence]

FORMAL CONCLUSION:
By D1, since outcomes are [IDENTICAL/DIFFERENT],
patches are [EQUIVALENT/NOT EQUIVALENT].
```

### 5.2 Fault localization (four phases)

1. Test semantics analysis — premises about what the test requires
2. Code path tracing — call sequence with file:line documentation
3. Divergence analysis — claims with reference to premise + code location
4. Ranked predictions — each prediction cites supporting claims

### 5.3 Code QA template

```
FUNCTION TRACE TABLE:
| Function | File:Line | Params | Return | Behavior (VERIFIED) |

DATA FLOW ANALYSIS:
Variable: [name]
- Created at: [file:line]
- Modified at: [file:line(s) or NEVER MODIFIED]
- Used at: [file:line(s)]

SEMANTIC PROPERTIES:
Property 1: [...]
- Evidence: [file:line]

ALTERNATIVE HYPOTHESIS CHECK:
If the opposite answer were true, what evidence would exist?
- Searched for: [...]
- Found: [...]
- Conclusion: [REFUTED / SUPPORTED]
```

`ALTERNATIVE HYPOTHESIS CHECK` is the direct equivalent of `rigorous-reasoning`'s falsification step.

## 6. Failure modes the paper reports

Worth keeping in mind — structured rigor doesn't solve everything:

1. **Confident wrong answers.** Semi-formal can make the conclusion *worse* when the agent constructs elaborate but incomplete chains. The paper's `py_5` example: the agent traced five functions and found a real edge case, but missed that downstream code already handled it. Deeper reasoning → more conviction → wrong answer.
2. **Third-party libraries.** When the agent doesn't have access to source, it has to guess. Structure exposes the guess but doesn't solve it.
3. **Domain expertise.** Algorithmic or numerical problems requiring specialized knowledge exceed the model's capacity regardless of structure.
4. **Multi-file or multi-region bugs.** The more locations that need to be held simultaneously, the harder it gets.

Generalized to other domains: rigorous-reasoning improves median quality but can shift some failures from "obviously wrong" to "subtly wrong with elaborate justification." The latter is harder to catch in review. It requires the reader to run the falsification step on the produced analysis.

## 7. Other works referenced in the paper

Worth knowing if you want to dig deeper:

- **SWE-RM** (Shum et al., 2025) — execution-free reward models for agents
- **Agentic Rubrics** (Raghavendra et al., 2025) — rubric-based LLM verification
- **CodeJudge** (Tong et al., 2024) — LLM-as-judge for code
- **Sultan et al. (2026)** — LLMs vs Halting Problem, showing that LLMs can predict termination properties but often fail to provide valid proofs. This is the theoretical ground for why "semi-formal" is interesting — LLMs are good at *intuition* about programs, weaker at formal *proofs*. The middle path is where the value lies.

## 8. Translation table (code → general analysis)

To see how the primitives map:

| Paper term | General equivalent in `rigorous-reasoning` |
|---|---|
| Premise | Assumption / precondition |
| Claim | Sub-claim |
| Trace through code behavior | Cite source / observation |
| Counterexample | Falsifying evidence |
| Test outcome | Verifiable consequence |
| File:line | Concrete reference (page, date, measurement) |
| Alternative hypothesis check | Falsification step |
| Formal conclusion | Conclusion follows from evidence |
| (implicit in the paper: error analysis) | What the process revealed |

The mapping isn't perfect — code has formal execution semantics that strategy doesn't. But the three primitives (enumerate, cite, falsify) carry over.
