![ Rigorous Reasoning](rigorous-reasoning.jpeg)

# rigorous-reasoning

A general-purpose discipline for analyses where being confidently wrong is worse than being openly uncertain.

The skill forces a three-step routine — **enumerate → cite → falsify** — that closes a specific failure mode: deeper reasoning producing *more confident* wrong answers because the agent constructs elaborate but incomplete chains. Overhead is roughly 3× the steps of an unstructured response. Worth it when wrong answers cost; wasteful otherwise.

## How you run it

The skill is a folder of markdown — there are no scripts. **You point your agent at the folder and let it dispatch the discipline when a question needs it.** Drop the folder into your host's skills directory (Claude Code, Cursor, Cowork — anything that reads `SKILL.md`); the host parses `SKILL.md`, learns the triggers, and applies the routine when an analytical question warrants it.

You never invoke the skill by name. You ask in natural language; the agent recognizes the question type and runs the routine:

| You ask | Agent runs |
|---|---|
| "Are these two approaches equivalent?" | Three primitives + full output format |
| "What's causing the drop in M?" | Three primitives + full output format |
| "Is this system ready for production?" | Three primitives + full output format |
| "What's the capital of France?" | Direct answer (skill abstains — see §5) |
| "Write me a haiku about latency." | Direct answer (skill abstains) |

The skill's value lies *both* in applying its discipline on hard questions *and* in abstaining on small ones. Both are part of what "use the skill" means.

## When it triggers

Trigger for non-trivial analytical questions where the conclusion can be subtly wrong: strategic decisions, comparisons, equivalence judgments, root-cause analyses, design critiques, regulatory or interpretive assessments, code review, hypothesis evaluation. Trigger also when you notice yourself constructing a persuasive answer without having verified it — catching the *automaticity* in your own response is itself the indicator.

Three signals it's needed:

1. The question has multiple plausible answers that all sound reasonable.
2. You notice yourself leaning toward an answer without having verified.
3. The cost of a wrong conclusion is concrete and hard to reverse.

If none of these holds, the structure is overhead. Answer directly.

## The three primitives

**Enumerate** — break the question into sub-claims. A conclusion like "X is good" usually hides 3–5 underlying claims. List them, so it's clear what actually needs support.

**Cite** — every claim points to evidence. Not "the market shows" — a concrete source, observation, data point, or measurement per claim. If the evidence doesn't exist, say so. Evidence types in descending rigor: direct data → primary-source quotes → user observations → named heuristic → first-principles reasoning. If everything lands at the bottom of that ladder, you haven't verified anything; you've constructed a plausible narrative.

**Falsify** — actively look for counter-evidence. *If the opposite were true, what evidence would exist?* Did you look for it? This is the confirmation-bias antidote, and the step that separates "convincing answer" from "answer that survives scrutiny."

## Output format

Six sections. Enough room to think, restrained enough to avoid ceremony:

```
CLAIMS:
- C1, C2, C3, ...

EVIDENCE:
- C1 supported by: [concrete source/observation/data]
- ...

FALSIFICATION:
If the opposite were true, I would see: [...]
Did I look? [yes → what I found / no → flag it]

INTEGRITY CHECK:
- Source authenticity: [...]
- Citation accuracy: [...]
- Question precision: [...]
- Logical coherence: [...]

CONCLUSION: [...]

WHAT THE PROCESS REVEALED:
- Hidden assumptions, evidence gaps, tensions, was the question well-posed

UNCERTAINTIES: [what couldn't be verified, where the conclusion could break]

NEXT STEPS UNDER UNCERTAINTY: [how to actually verify the rest]
```

The order is deliberate, not cosmetic:

- **Evidence before conclusion** — so the conclusion follows from the evidence, not the other way around.
- **Integrity check before conclusion** — it is a gate, not a reflection. If the check reveals a hallucinated source, a misread citation, or that the question has drifted, the analysis is revised before the conclusion is released.
- **What the process revealed before uncertainties** — meta-observations feed the next two sections and turn them from generic ("needs more data") into concrete and targeted.

Full templates with worked examples (comparison, root-cause, assessment) live in `SKILL.md` §3–4.

## Integrity check — four distinct checks

The least obvious section, and the most important specifically for LLM use. The other sections scrutinize the *conclusion's* validity. This one scrutinizes the *analysis's integrity*.

| Check | Failure mode it catches |
|---|---|
| Source authenticity | The cited source doesn't exist. Most common LLM failure. |
| Citation accuracy | The source exists, but doesn't say what you think. |
| Question precision | You answered an easier nearby question instead of the one asked. |
| Logical coherence | The conclusion doesn't follow from the premises, even if both are sound. |

Never write "Source authenticity: ✓". Write what was checked and what couldn't be checked. Empty checkmarks are worse than no section at all — they simulate rigor without delivering it.

## Anti-patterns

The full list is in `SKILL.md` §6; the ones worth flagging up front:

- **Evidence theater** — writing "Evidence: [reasoning]" where "reasoning" is new prose instead of a pointer to a source.
- **Falsification as formality** — writing "if the opposite were true I would see X" and then not looking for X.
- **Claims as rationalizations** — writing the conclusion first and breaking it into supporting claims. Break down the *question*, not the answer.
- **Integrity check as checkbox** — empty marks instead of named checks.
- **Self-diagnosed misfire run anyway** — noting in the analysis that the question doesn't warrant the structure and producing the structure regardless. The honest move is to abstain.

## File layout

```
rigorous-reasoning/
├── SKILL.md                    # Natural-language instructions for the agent
├── README.md                   # This file
└── references/
    ├── source-paper.md         # The Ugare & Chandra paper + code-specific templates
    └── self-improvement.md     # Protocol for when the skill may propose updates to itself
```

## Source

The pattern comes from **Ugare & Chandra (2026), "Agentic Code Reasoning"** (arXiv:2603.01896v2, Meta). The paper shows that structured "semi-formal reasoning" improves LLM agents' code analysis by 5–12 percentage points over unstructured chain-of-thought across three tasks (patch equivalence, fault localization, code QA). This skill extracts the three primitives that do the actual work and generalizes them beyond code.

Background and the full code-specific templates are in `references/source-paper.md`.

## What this is not

This is a discipline for analyses, not a workflow engine and not a planning framework. If the question is small, the right move is to answer it directly — applying the structure anyway is the worst of both worlds. The discipline earns its overhead only when a wrong conclusion is concrete and hard to reverse.

This is also not a hallucination filter. The integrity check surfaces what the agent could and couldn't verify; it doesn't replace verification. If you need ground truth, fetch the source.

## License

MIT.
