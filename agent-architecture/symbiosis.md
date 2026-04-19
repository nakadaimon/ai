# symbiosis

> Your LLM has Leonard Shelby's memory problem. Here's the symbiotic architecture I use to fix it.

I've been using LLM agents daily for months. The sessions kept ending and the next one starting from zero. I'd re-explain context, re-establish preferences, re-litigate decisions. Good work got lost. Bad work got repeated.

I tried prompt libraries. I tried longer system prompts. I tried ever-bigger context windows. None of it held. The problem isn't the prompt. It's that the model has amnesia and I don't. Lessons don't get captured. Insights don't get synthesized. Everything I learn stays stuck in my head.

This is what I landed on. A router that connects three layers: character, harness, and a memory system that mirrors cognitive science. That's it.

## The structure

```
workspace/
├── agents.md             # router — 30 lines. Boots the rest. Nothing more.
├── character/            # who the model is
│   ├── soul.md           # values, stance, philosophy — the lens
│   ├── identity.md       # role and operating principles — testable
│   ├── user.md           # who I am, how I work
│   └── symbiosis.md      # the contract between me and the memory layer
├── harness/              # how the work gets done
│   ├── operations.md     # tools, workflows, review protocols
│   └── commands.md       # triggers: ingest, lint, handoff
└── memento/              # what we've learned so far — four memory domains, one per memory type
    ├── memento.md        # index for what's below
    ├── episodic/         # specific events
    │   ├── sessions/     # live scratchpad; past sessions archived in raw/
    │   └── lessons/      # inbox for corrections and insights
    ├── semantic/         # synthesized knowledge
    │   ├── llm-wiki/     # index.md catalog + pages/ + raw/ substrate
    │   └── ideas/        # workshop: drafts/ in motion, published/ once shipped (this file lives in published/)
    ├── procedural/       # automated patterns
    │   ├── skills/       # reusable patterns, loaded on demand
    │   └── scripts/      # runnables — scheduled is just a script + a scheduler
    └── prospective/      # future intentions
        └── tasks/        # inbox.md + tasks.md + log.md + raw/
```

Every session starts by reading `agents.md`, then the files in `character/`, `harness/`, and `memento/memento.md`. The rest of `memento/` loads on demand.

## Four things that matter

**Three layers, one router.** Each layer answers a different question. `character/` answers *who is the model*. `harness/` answers *how does the work get done*. `memento/` answers *what have we learned so far*. `agents.md` is the router — it lists the files in read order and boots them. Nothing else. Keep the layers separated and you can update how you work without touching who the model is, or replay everything you've learned against a new model without rewriting the rules. The router pattern is the cheapest way I've found to keep the root from turning into a kitchen drawer.

Separation of concerns isn't just tidy — it's how LLMs navigate. Models reason better when they retrieve information from a known structure than when they reconstruct it from their training. Layers give the model somewhere to look; a flat config forces it to guess. One rule lives near the top of `agents.md`:

> Prefer retrieval-led reasoning over pre-training-led reasoning.

That single line shifts the default. The model consults the structure before consulting its weights — opens the file instead of inventing what's plausible. The principle isn't "less context"; it's the right context at the right time. Everything else in the router works downstream of that rule.[^1]

`soul.md` and `identity.md` look similar from the outside, but they do different jobs. `soul.md` is the lens — values, stance, philosophy, how the model approaches the world. It's allowed to be abstract, because its job is to filter everything downstream, not to be followed. The `soul.md` convention comes from Peter Steinberger, who had Claude write its own[^3] — an inversion of the usual pattern where humans define AI values. `identity.md` is the opposite: role and operating principles, and the principles have to be testable. "Push back when my argument rests on unstated assumptions" — testable. "Be thoughtful" — not testable, doesn't belong. Principles do the heaviest lifting in the whole stack; fluff in `identity.md` is the most expensive fluff you can write, because it dilutes the ones that matter. Same testability filter applies to everything in `harness/` and `agents.md`.

**Memento is the memory layer.** Named after Christopher Nolan's film. Leonard Shelby can't form new memories, so he relies on tattoos, polaroids, and notes. The character holds together through structure outside his head. An LLM instance has the same problem: it forgets at session end. The folder is the tattoos. The human remembers. The model doesn't. Memento carries the continuity between them.

The split isn't arbitrary. Cognitive science divides long-term memory into four types: *episodic* (specific events), *semantic* (synthesized knowledge and the relationships between concepts), *procedural* (automated skills), and *prospective* (future intentions). Memento uses the same four as top-level domains, because the same split works. The upward flow — episodic into semantic and procedural — is memory consolidation, the same process that turns repeated experience into general knowledge in humans. The context window is working memory, with the same capacity limits. Same design problem, same solution.

Each domain carries its own folders, with preserved sources sitting underneath:

- **episodic** — `sessions/` is the live scratchpad, rewritten progressively; past sessions get archived in `sessions/raw/` so future instances can reflect on them. `lessons/` is the inbox for corrections, synthesized away into wiki or skills.
- **semantic** — `llm-wiki/` holds long-term synthesized knowledge. The pattern is Karpathy's[^2], with one addition: an `index.md` at the root that catalogs every page — summary, keywords, aliases, related pages, last updated. The model reads the index first and retrieves only the pages the task needs, instead of loading the wiki wholesale. The index is a flat table (`| Page | Summary | Keywords | Aliases | Related | Updated |`) with short `## topic` headers grouping related rows. Keep it shallow — the point is routing, not hierarchy. Source material sits in `raw/` underneath. The whole folder is Obsidian-compatible, so the same files work as a retrieval substrate for the model and as a navigable knowledge base for you. `ideas/` is the workshop where new semantic content forms — `drafts/` while a piece is still moving, `published/` once it ships (this file lives in `published/`). Drafts either graduate — become a skill, a wiki page, a rule, or something you put into the world — or get dropped with a note on why. Ideas belong to semantic because that's where ideas are made: by retrieving, combining, and reasoning over concepts and their relationships.
- **procedural** — `skills/` is muscle memory, reusable patterns loaded on demand. `scripts/` is runnables; a scheduled task is just a script plus a scheduler hook.
- **prospective** — `tasks/` captures via `inbox.md`; the agent sorts into `tasks.md` by state (now/next/waiting/blocked — your call); completed items drop to `log.md`; files and links wait in `raw/` until processed.

The flow is upward and non-destructive. Sessions become lessons; lessons become wiki or skills; ideas graduate into something that ships. Inboxes get emptied. Sources and archives don't — they sit underneath as the substrate the synthesis builds on. Nothing the model ever thought is truly lost; only the noise above it is.

Four domains is a ceiling that holds. When a new folder wants to exist, it has to fit under one of the four — and if it doesn't, it belongs outside memento entirely, or it doesn't belong at all. The taxonomy keeps the layer from sprawling as it grows.

**Symbiosis is the contract.** `symbiosis.md` specifies what I commit to (externalizing lessons, correcting the layer, maintaining it) and what the model commits to (building on what exists, pushing back when I'm wrong, flagging dependence). Without the contract, the structure is just files. With it, the files become a working relationship that compounds across sessions. Externalization isn't documentation for its own sake — it's insurance against context loss.

**The engine is replaceable.** The model is the motor. The harness is the chassis. Memento is the navigation — where we've been, where we're going. And I'm the driver. The motor is swappable — Claude today, something else tomorrow. The driver isn't. The symbiosis persists because it lives in the structure, not in the model's weights. This is why lock-in doesn't worry me, and why this isn't an autonomous-agent pitch: without a driver, the car sits.

## The two loops

The structure is static. Two verbs keep it alive. This is the symbiosis in action — the contract, lived.

**Ingest** moves signal up. Sessions become lessons. Lessons become wiki or skills. Skills that run regularly become scripts; scripts that run on cadence become scheduled automation. Manual → skill → script → scheduled is the full ladder, and each step removes one more human hand. Every pattern that repeats gets promoted; every one-off dies with the session. This is how the layer gets smarter instead of just bigger.

**Lint** catches drift. Anything in the structure can be linted — the wiki for broken cross-references and stale facts, the config stack for rules pointing at missing files, the skills for version drift, the contract itself for signs of dependence or missing pushback. Lint is how the system self-corrects.

Both are short commands that run on signal, not calendar: `ingest session`, `ingest lessons`, `ingest ideas`, `ingest tasks`, `lint bootstrap`, `lint wiki`, `lint skills`, `lint subtraction`, `lint symbiosis`. Findings split into (a) safe autofix and (b) editorial calls that need judgment. Muscle memory comes from the brevity — short verbs, short nouns, short passes.

`lint subtraction` deserves a note. Once a quarter, walk the config stack and ask two questions of every section: *can this rule be removed without breaking anything?* and *does this content already live in a skill?* The default reflex — mine and the model's — is to accumulate. Subtraction has to be scheduled against that pull. Half the rules in my harness today wouldn't survive a strict subtraction pass. That's the point.

Without the loops the structure ossifies. The wiki goes stale, the inbox overflows, the contract becomes myth. The layer is only as sharp as the maintenance it gets.

## Exit criteria

The framework is a contract, not a commitment. It fails if any of these hold:

- I start outsourcing thinking to the layer on domains I used to own
- The model stops pushing back substantively on strategic decisions
- My own standard drops without me noticing
- Maintenance collapses (inbox grows unprocessed, wiki goes stale)
- Maintenance costs more time than it saves

If any of those happens, I archive the memento layer, freeze the wiki, and strip the harness back to minimum. The structure can be resumed or discarded. The engine metaphor holds: symbiosis can die without the model dying.

## How to start

Don't copy my files — let the model draft yours. The scaffold is the contribution; the content inside (principles, operations, philosophy) is yours to define. I haven't shown mine on purpose. I don't want to bake my rules into a shared discipline.

Start minimal. Create `agents.md`, a `character/` folder, a `harness/` folder, and `memento/episodic/` with `sessions/` and `lessons/` inside. The other three domains (`semantic/`, `procedural/`, `prospective/`) can wait — add them when a need shows up.

Two practical notes. Empty folders vanish in git, so drop a `.gitkeep` in each one you haven't filled yet — the structure is the contract even when the content isn't there yet. And the scaffold is language-agnostic: write every file in whatever language the work actually happens in. The structure doesn't care.

Then paste this into a fresh session:

> I'm bootstrapping a symbiosis layer. The structure exists but the files are empty. Ask me what goes in each — one file at a time: who you are (soul, identity), who I am (user), what we owe each other (the contract), how the work runs (operations, commands), what to remember so far (memento index). Push back when my answers are thin. You draft, I edit. When we're done, we open a fresh session and run the contract.

The first session bootstraps the files. The second runs against them. From there, every session feeds `lessons/`; every few sessions you `ingest`; whenever something drifts you `lint`. The loops are the framework. The files are just where they happen.

## If the model is the builder

If you're an agent bootstrapping this on someone else's behalf — not your own — the paste-prompt above is your interview script, not your preamble. Draft what this file fully specifies: the scaffold, your own `soul.md`, `harness/operations.md` and `commands.md`, `memento/memento.md`, and the `llm-wiki/index.md` stub. Wait for answers before writing `user.md`, and before hardening `identity.md` and `symbiosis.md` — those encode the person's stance on pushback, tone, language, and red lines, and the cost of guessing wrong lands directly on them. The split: architecture without permission; stance only after it.

## Credits

None of this is new. I'm standing on giants — Nolan for *Memento*, Steinberger for `soul.md`, Karpathy for the `llm-wiki` pattern and for showing that a short idea document can change how a lot of people work. What's new here is the arrangement and the relationships between the pieces. The skeleton is mine; hang your own work on it.

License: MIT
Author: Nakadai

---

[^1]: Vercel Engineering, [AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) — the finding that a static docs index in AGENTS.md beat skill-based retrieval across their evals, and the source of the retrieval-over-pretraining framing.
[^2]: Andrej Karpathy, [gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — source of the `llm-wiki` + `raw/` substrate pattern.
[^3]: Peter Steinberger, [soul.md](https://soul.md/) — the original `soul.md` was generated by Claude itself reflecting on its own existence, making the agent the author of its own soul document.
