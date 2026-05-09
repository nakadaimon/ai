# Self-improvement protocol — for `rigorous-reasoning`

> Loaded only when the agent has empirical reason to propose an update to the skill itself. Not part of the default output format. Default is to propose nothing.

This skill is not finished. During use, signs sometimes appear that the skill's *form* — not just its application to a particular question — has a flaw or improvement potential. When that happens, propose an update — under the conditions below.

## 1. When a proposal is legitimate

Two qualifiers must hold — otherwise it's noise, not signal:

1. **Evidence-based.** The observation is empirical from actual use, not speculative. "In the last three uses, step X was missing" is evidence. "It might be nice to have Y" is not.
2. **Reproducible mechanism.** If the improvement were added, it would produce an observably different and better outcome in future uses. Aesthetic or subjective improvements don't qualify.

Both must hold. Otherwise carry the observation in mind and gather more before raising it.

## 2. Distinguish skill flaw from domain flaw

The most common mistake is confusing a deficient *evidence base* with a deficient *skill*. If an analysis lacks data X, that's the data source's problem, not this skill's. Skill update proposals should only address:

- **The process** — is a step missing, is the order wrong, is something over- or under-specified?
- **The format** — does the output format lead to anti-patterns not yet listed?
- **The principles** — is there a class of analysis where the three primitives systematically miss something?
- **The triggers** — does the skill activate when it shouldn't, or miss cases where it should?

Domain-specific deficiencies belong in domain skills.

## 3. Format for proposals

When the qualifiers are met, append a separate block after the analysis — not part of the output format, so it doesn't become routine noise:

```
SKILL-PROPOSAL (rigorous-reasoning):
- Observation: [what I noticed during this use]
- Reproducibility: [have I seen this before? where?]
- Proposed change: [concrete addition/change to SKILL.md or reference]
- Expected effect: [what would be different in future use]
- Bump to: [PATCH | MINOR | MAJOR]
```

Versioning convention:

- **PATCH** for wording fixes, clearer examples, corrected links
- **MINOR** for new sections, new anti-patterns, expanded principles
- **MAJOR** for structural changes to the output format or to the three primitives

## 4. When proposals are *not* legitimate

Actively avoid:

- **One-time observation.** "This time it would have been good if..." — too few data points. Note, wait, gather.
- **Domain projection.** Improvement that actually belongs in a domain skill.
- **Aesthetic preference.** "It would look cleaner if..." — without reproducible effect on outcome.
- **Improvement theater.** Proposals that appear to show rigor but change nothing in practice.
- **Conflict with an existing principle.** A proposal that contradicts a stated principle must first argue *why* the principle is wrong — otherwise it's inconsistency, not improvement.

## 5. What this pattern is

This is rigorous-reasoning applied to itself. The same evidence burden + falsification, at the meta level: what is the observation, can it be reproduced, what would refute the need for the improvement?

A skill that can't evolve through its own use dies quietly. One that evolves uncontrollably drifts. This protocol is the middle path — structured self-improvement with evidence burden.
