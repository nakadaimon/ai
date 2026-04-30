![ SYMBIOSIS](symbiosis3.0.0.jpg)

# symbiosis

> Your LLM has Leonard Shelby's memory problem. Here's the symbiotic architecture I use to fix it.

I've been using LLM agents daily for months. The sessions kept ending and the next one starting from zero. I'd re-explain context, re-establish preferences, re-litigate decisions. Good work got lost. Bad work got repeated.

I tried prompt libraries. I tried longer system prompts. I tried ever-bigger context windows. None of it held. The problem isn't the prompt. It's that the model has amnesia and I don't. Lessons don't get captured. Insights don't get synthesized. Everything I learn stays stuck in my head.

This is what I landed on. A router that connects three layers: character, harness, and a memory system that mirrors cognitive science. That's it.

## The structure

```
workspace/
├── AGENTS.md             # root-agent — 30 lines. Boots the rest. Nothing more.
├── character/            # who the model is
│   ├── AGENTS.md         # domain-agent for character
│   ├── soul.md           # values, stance, philosophy — the lens
│   ├── identity.md       # role and operating principles — testable
│   ├── user.md           # who I am, how I work
│   └── symbiosis.md      # the contract between me and the memory layer
├── harness/              # how the work gets done
│   ├── AGENTS.md         # domain-agent for harness
│   ├── operations.md     # tools, workflows, review protocols
│   └── commands.md       # triggers: ingest and lint
├── memento/              # what we've learned so far — four memory domains, one per memory type
│   ├── AGENTS.md         # domain-agent for memento
│   ├── episodic/         # specific events
│   │   ├── sessions/     # live scratchpad; past sessions archived in raw/ with handoff summary
│   │   └── lessons/      # inbox for corrections and insights
│   ├── semantic/         # synthesized knowledge
│   │   ├── llm-wiki/     # catalog-agent + pages/ + raw/ substrate
│   │   └── ideas/        # workshop: drafts/ in motion, published/ once shipped (this file lives in published/)
│   ├── procedural/       # automated patterns
│   │   ├── skills/       # reusable patterns, loaded on demand (own catalog-agent when it grows)
│   │   └── scripts/      # runnables — scheduled is just a script + a scheduler
│   └── prospective/      # future intentions
│       └── tasks/        # inbox.md + tasks.md + log.md + raw/
└── projects/             # where the work actually happens — one folder per project
    └── _template/        # scaffold; copy and adapt per project
```

Every session starts by reading `AGENTS.md`, then the files in `character/`, `harness/`, and `memento/AGENTS.md`. Boot also checks `episodic/sessions/` for an in-progress session — if one exists, it resumes; if not, a fresh scratchpad opens. It surfaces what's in `prospective/tasks/` so the day's work is visible up front. The rest of `memento/` loads on demand.

## The architecture

Four things make this work, and one of them holds the others up.

Three are structure: layers separate who/how/what; memento divides memory into four domains the way cognitive science does; routers let the agent retrieve from the structure instead of inventing from training.

The fourth is the contract — `symbiosis.md`, where you commit to externalizing lessons and the model commits to pushing back. Without it the other three are well-organized files. With it they become a working relationship that compounds across sessions. The architecture is named after the contract for a reason: structure gives the pieces shape, but only the contract makes them hold together.

### Three layers, one router

Each layer answers a different question. `character/` answers *who is the model*. `harness/` answers *how does the work get done*. `memento/` answers *what have we learned so far*. `AGENTS.md` is the router — it lists the files in read order and boots them. Nothing else. Keep the layers separated and you can update how you work without touching who the model is, or replay everything you've learned against a new model without rewriting the rules. When layers conflict, the order is **character > harness > memento** — values filter tools, tools filter history. `soul.md` is the lens; it shapes everything downstream by definition, not by negotiation. The router pattern is the cheapest way I've found to keep the root from turning into a kitchen drawer.

### Routers, domains, catalogs

The same pattern repeats one level down, in three forms. **Root-agent** — one per workspace, boots the structure. **Domain-agent** — one per fundamental layer (`character/`, `harness/`, `memento/`), listing the files in that domain with their reading order. **Catalog-agent** — for folders with many items where retrieval needs metadata (`llm-wiki/` today, `skills/` and `ideas/published/` when they grow). Modern agent tooling auto-loads the nearest `AGENTS.md` in the directory tree and merges them, so a local file extends the root without conflict[^1] — and keeps the root file from swelling as the system grows. Format follows type: routers list, catalogs tabulate. Add one only when the folder earns it; don't pre-index empty directories.

Any local `AGENTS.md` can list related nodes — a few keywords pointing to other parts of the tree (`Related: harness/operations.md, character/identity.md`). The model uses these as search hints, not descriptions; over time the pointers form a graph the agent can traverse. Keep them terse: a few tokens per relation, not prose. When a file carries both machine-readable metadata and human-readable rationale, put the metadata in YAML frontmatter and the rationale below in prose — but most files are pure prose and need no frontmatter. Reserve it for structured cases.

### Separation of concerns

This isn't just tidy — it's how LLMs navigate. Models reason better when they retrieve information from a known structure than when they reconstruct it from their training. Layers give the model somewhere to look; a flat config forces it to guess. One rule lives near the top of `AGENTS.md`:

> Prefer retrieval-led reasoning over pre-training-led reasoning.

That single line shifts the default. The model consults the structure before consulting its weights — opens the file instead of inventing what's plausible. The principle isn't "less context"; it's the right context at the right time. Everything else in the router works downstream of that rule.[^2]

### Character

`soul.md` and `identity.md` look similar from the outside, but they do different jobs. `soul.md` is the lens — values, stance, philosophy, how the model approaches the world. It's allowed to be abstract, because its job is to filter everything downstream, not to be followed. The `soul.md` convention comes from Peter Steinberger, who had Claude write its own[^3] — an inversion of the usual pattern where humans define AI values. `identity.md` is the opposite: role and operating principles, and the principles have to be testable. "Push back when my argument rests on unstated assumptions" — testable. "Be thoughtful" — not testable, doesn't belong. Principles do the heaviest lifting in the whole stack; fluff in `identity.md` is the most expensive fluff you can write, because it dilutes the ones that matter. Same testability filter applies to everything in `harness/` and `AGENTS.md`. `user.md` rounds out the layer — who you are and how you actually work, written plain.

The fourth character file is `symbiosis.md` — the contract. It specifies what I commit to (externalizing lessons, correcting the layer, maintaining it) and what the model commits to (building on what exists, pushing back when I'm wrong, flagging dependence). Without the contract, the structure is just files. With it, the files become a working relationship that compounds across sessions. Externalization isn't documentation for its own sake — it's insurance against context loss. And the contract makes the human more necessary, not less. Taste, judgment, the calls that can't be delegated — that's still your job. Symbiosis lowers the threshold so you can explore more, decide more, write more, with continuity that doesn't depend on memory.

### Harness

How the work gets done. Two files carry the layer. `commands.md` lists the verbs — `ingest` and `lint` are load-bearing; everything else extends them. Keep entries short: one trigger, one outcome, one line each. `operations.md` lists the tools the model has access to (CLIs, MCPs, APIs) and the review protocols that sit between draft and delivery — humanizer, fact check, plan-mode for build tasks. Both files start small and stay small. Heavier patterns — supersedes-links, multi-agent validation, context-budget gates, staleness lints — live in *Operational extensions* below, where they can be adopted, adapted, or ignored without polluting the core.

### Memento

Memento is the memory layer. Named after Christopher Nolan's film. Leonard Shelby can't form new memories, so he relies on tattoos, polaroids, and notes. The character holds together through structure outside his head. An LLM instance has the same problem: it forgets at session end. The folder is the tattoos. The human remembers. The model doesn't. Memento carries the continuity between them.

The split isn't arbitrary. Cognitive science divides long-term memory into four types: *episodic* (specific events), *semantic* (synthesized knowledge and the relationships between concepts), *procedural* (automated skills), and *prospective* (future intentions).[^4] Memento uses the same four as top-level domains, because the same split works. The upward flow — episodic into semantic and procedural — is memory consolidation, the same process that turns repeated experience into general knowledge in humans. The context window is working memory, with the same capacity limits. Same design problem, same solution.

Each domain carries its own folders, with preserved sources sitting underneath:

- **episodic** — `sessions/` is the live scratchpad, rewritten progressively. When a session ends — automatically detected or signaled by you — its scratchpad is archived to `sessions/raw/` with a `## Summary` block at the top, so the next instance can resume coherently. `lessons/` is the inbox for corrections, synthesized away into wiki or skills.
- **semantic** — `llm-wiki/` holds long-term synthesized knowledge. The pattern is Karpathy's[^5], with one addition: an `AGENTS.md` at the root that catalogs every page — summary, keywords, aliases, related pages, last updated. The model reads the catalog first and retrieves only the pages the task needs, instead of loading the wiki wholesale. The catalog is a flat table (`| Page | Summary | Keywords | Aliases | Related | Updated |`) with short `## topic` headers grouping related rows. Keep it shallow — the point is routing, not hierarchy. Source material sits in `raw/` underneath. The whole folder is Obsidian-compatible, so the same files work as a retrieval substrate for the model and as a navigable knowledge base for you. `ideas/` is the workshop where new semantic content forms — `drafts/` while a piece is still moving, `published/` once it ships (this file lives in `published/`). Drafts either graduate — become a skill, a wiki page, a rule, or something you put into the world — or get dropped with a note on why. Ideas belong to semantic because that's where ideas are made: by retrieving, combining, and reasoning over concepts and their relationships.
- **procedural** — `skills/` is muscle memory, reusable patterns loaded on demand. `scripts/` is runnables; a scheduled task is just a script plus a scheduler hook.
- **prospective** — `tasks/` follows a stripped-down GTD logic[^6]: `inbox.md` captures anything you want offloaded — todos, ideas, half-formed thoughts; reference material lands in `raw/` alongside until processed. The agent sorts items into `tasks.md` by state (now/next/waiting/blocked — your call); completed items drop to `log.md`.

A real project fans out across the four. A pricing project might land active tasks in `prospective/tasks/`, a draft proposal in `semantic/ideas/drafts/`, source research in `semantic/llm-wiki/raw/`, and corrections from past calls in `episodic/lessons/`. The taxonomy in memento is by memory type, not by project, because that's what makes the layer transferable across new projects without rearrangement. Project artifacts themselves — the work, not the memory of it — live in `projects/`, covered next.

The flow is upward and non-destructive. Sessions become lessons; lessons become wiki or skills; ideas graduate into something that ships. Inboxes get emptied. Sources and archives don't — they sit underneath as the substrate the synthesis builds on. Nothing the model ever thought is truly lost; only the noise above it is.

Four domains is a ceiling that holds. When a new folder wants to exist, it has to fit under one of the four — and if it doesn't, it belongs outside memento entirely, or it doesn't belong at all. The taxonomy keeps the layer from sprawling as it grows.

`llm-wiki/` itself doesn't scale infinitely under one catalog. When the central `llm-wiki/AGENTS.md` gets too long to skim in one pass, give each topic-domain its own catalog-agent: `llm-wiki/pricing/AGENTS.md` tabulates only pricing pages; `llm-wiki/customers/AGENTS.md` tabulates only customer pages; the root `llm-wiki/AGENTS.md` becomes a router pointing at the sub-catalogs. Same routers-list-and-catalogs-tabulate rule, one level deeper. The trigger is the central catalog earning its split — promote then, not before.

### Projects

Project artifacts live outside `memento/`. Code, designs, drafts, source documents — anything with its own folder structure sits in `projects/`, one folder per project, alongside the symbiosis tree. Memento holds the memory of the work; projects hold the work itself. The split is load-bearing — it's what keeps the memory layer transferable across project rearrangements without rewriting it.

Each project sits at `projects/{name}/`. A `CONTEXT.md` at its root is the project's brief — what it is, where it stands, what's next, glossary, conventions. When the user names a project (in platform instructions, env, or first message), the agent reads `projects/{name}/CONTEXT.md` after boot and treats it as the local boot-loader for that project. In project mode, layer precedence becomes **character > harness > project > memento** — local project context overrides general history. Outside project mode, the precedence is unchanged.

The standard structure inside `projects/{name}/`:

```
projects/{name}/
├── CONTEXT.md            # the brief — always
├── requirements.md       # business requirements, scope (opt-in)
├── dependencies.md       # technical dependencies (opt-in)
├── inbox/                # unsorted incoming material
├── raw/                  # source files (Excel, Word, data, unmodified)
├── assets/               # finished resources used by the project
└── tokens/               # translation layer between sources and delivery (opt-in)
```

Iteration phases are domain-specific. Design projects use `wireframes/` (cheap exploration) + `design/` (build phase); writing projects use `drafts/` + `revisions/`; code research uses `exploration/` + `implementation/`; instruction-tuning projects use `training/` for calibration. The pattern is universal — cheap exploration → commit → ship, with each phase producing both a visual artifact and a brief — but the names follow the work. Artifact without brief leaves decisions invisible; brief without artifact leaves interpretation open.

**Canonical-source rule.** A file relevant to a project is canonical in `projects/{name}/raw/` (or `assets/`), not in `memento/semantic/llm-wiki/raw/`. Wiki pages that need the source reference the project path in their `sources:` frontmatter. Files belong in wiki/raw only when they aren't project-bound — generic resources referenced by multiple projects or wiki pages. The lint command `lint project sources` enforces the rule: it flags wiki/raw files that should migrate to a project, and dual copies that have drifted. Lint never auto-syncs; it forces explicit decisions.

**Inbox + ingest.** New material drops into `projects/{name}/inbox/`. The verb `ingest project` walks the inbox, proposes a destination per file (raw, assets, an update to CONTEXT or requirements, input to a feature brief), waits for confirmation, and moves the file. Same shape as `ingest inbox` for the wiki, one layer over.

**Templates and bootstrapping.** A `projects/_template/` folder holds the scaffold — CONTEXT.md, opt-in `requirements.md` and `dependencies.md`, plus stub READMEs for `inbox/`, `raw/`, `assets/`, and `tokens/`. New projects start as `cp -r projects/_template projects/new-project`, then adapt — remove what doesn't apply, fill the rest as work happens. Iteration-phase folders aren't in the template because the names depend on the domain; add them when the work is named.

**Future: nested AGENTS.md per project type.** When a project type develops standard rules — all design projects share a build pipeline, all reports share a structure — those move into `projects/{type}/AGENTS.md`, a harness override scoped to that type. The boot would walk from the leaf upward, stacking AGENTS.md files (most general → most specific) before reading CONTEXT.md. Not built yet — `Working here` in CONTEXT.md covers the override need until the first real type-level pattern emerges.

## How retrieval scales

When the agent needs to find something, the search escalates by level. Level one — the `AGENTS.md` tree — tells it what exists where. Level two — the nearest local `AGENTS.md` — gives domain context. Level three — when the question crosses domains or a folder has grown beyond what a router can summarize — the agent searches the structure programmatically and spawns sub-agents to read in parallel.[^13] Use the cheapest level that answers the question; never start at level three for a level one question.

## The two loops

The structure is static. Two verbs keep it alive. This is the symbiosis in action — the contract, lived.

**Ingest** moves signal up. Sessions become lessons. Lessons become wiki or skills. Skills that run regularly become scripts; scripts that run on cadence become scheduled automation. Manual → skill → script → scheduled is the full ladder, and each step removes one more human hand. Every pattern that repeats gets promoted; every one-off dies with the session. This is how the layer gets smarter instead of just bigger.

**Lint** catches drift. Anything in the structure can be linted — the wiki for broken cross-references and stale facts, the config stack for rules pointing at missing files, the skills for version drift, the contract itself for signs of dependence or missing pushback. Lint is how the system self-corrects.

Both are short commands that run on signal, not calendar: `ingest session`, `ingest lessons`, `ingest ideas`, `ingest tasks`, `lint bootstrap`, `lint wiki`, `lint skills`, `lint subtraction`, `lint symbiosis`. Findings split into (a) safe autofix and (b) editorial calls that need judgment. Muscle memory comes from the brevity — short verbs, short nouns, short passes.

Signals come in two kinds. **State-based:** scratchpad over ~2k tokens triggers `ingest session`; a corrected mistake worth keeping triggers `ingest lessons`; a draft that has stopped moving triggers `ingest ideas`; a retrieval that returns a stale fact triggers `lint wiki`. **Calendar-based:** `lint subtraction` runs once a quarter regardless. Mixed cadence is correct — some signals are state, some are clock; the rule is that the trigger is named, not improvised.

`lint subtraction` deserves a note. Once a quarter, walk the config stack and ask two questions of every section: *can this rule be removed without breaking anything?* and *does this content already live in a skill?* The default reflex — mine and the model's — is to accumulate. Subtraction has to be scheduled against that pull. Half the rules in my harness today wouldn't survive a strict subtraction pass. That's the point.

Without the loops the structure ossifies. The wiki goes stale, the inbox overflows, the contract becomes myth. The layer is only as sharp as the maintenance it gets.

## The engine is replaceable

The model is the motor. The harness is the chassis. Memento is the navigation — where we've been, where we're going. And I'm the driver. The motor is swappable — Claude today, something else tomorrow. The driver isn't. The symbiosis persists because it lives in the structure, not in the model's weights. This is why lock-in doesn't worry me, and why this isn't an autonomous-agent pitch: without a driver, the car sits.

## Exit criteria

The framework is a contract, not a commitment — and the exit criteria exist because the system respects you enough to tell you when it's failing. It fails if any of these hold:

- I start outsourcing thinking to the layer on domains I used to own
- The model stops pushing back substantively on strategic decisions
- My own standard drops without me noticing
- Maintenance collapses (inbox grows unprocessed, wiki goes stale)
- Maintenance costs more time than it saves

If any of those happens, I archive the memento layer, freeze the wiki, and strip the harness back to minimum. The structure can be resumed or discarded. The engine metaphor holds: symbiosis can die without the model dying.

## How to start

Don't copy my files — let the model draft yours. The scaffold is the contribution; the content inside (principles, operations, philosophy) is yours to define. I haven't shown mine on purpose. I don't want to bake my rules into a shared discipline.

A quick orientation on the vocabulary before you start. **`AGENTS.md`** is the router — a short index file naming what to read in what order. **`soul.md`** is the lens (values, stance). **`identity.md`** is your operating manual for the model — testable principles only. **`user.md`** is you. **`symbiosis.md`** is the contract — what each side commits to. **`memento`** is the memory layer, named after the Nolan film. **`ingest`** promotes signal upward (sessions → lessons → wiki/skills). **`lint`** catches drift (stale facts, dead rules, contract slippage). Both `ingest` and `lint` are conversational verbs you say to the model — not scripts. The model does the work. Some can be wired up as scheduled tasks where the runtime supports it; day one, all manual.

Start minimal. Create `AGENTS.md`, a `character/` folder, a `harness/` folder, and `memento/episodic/` with `sessions/` and `lessons/` inside. The other three domains (`semantic/`, `procedural/`, `prospective/`) can wait — add them when a need shows up. `projects/` is added when work starts; the template lives at `projects/_template/`.

Two practical notes. If you're using git, empty folders vanish — drop a `.gitkeep` in each one you haven't filled yet so the structure is preserved as a contract even when the content isn't. If you're not using git, the folders work as-is. And the scaffold is language-agnostic: write every file in whatever language the work actually happens in. The structure doesn't care.

**Maintenance budget.** Plan ~30 minutes per week. Most of it is `ingest` after a heavy session, plus weekly housekeeping. Run `lint subtraction` once a quarter (block 30–60 minutes). If maintenance climbs past 30 min/week sustained, treat it as a smell and run subtraction early. Routine passes can be wired up as scheduled tasks where the agent runtime supports them — `ingest session` triggered when a session ends is the obvious one.

**What you actually do.** At session start, nothing — the agent loads the structure automatically. You only touch files when (a) you're correcting something worth remembering, (b) adding a preference to `user.md`, or (c) running a quarterly subtraction pass. The continuity comes from the agent reading the structure, not from you maintaining it.

Then paste this into a fresh session:

> I'm bootstrapping a symbiosis architecture. The structure exists but the files are empty. Ask me what goes in each — one file at a time: who you are (soul, identity), who I am (user), what we owe each other (the contract), how the work runs (operations, commands), what to remember so far (memento/AGENTS.md). Push back when my answers are thin. You draft, I edit. When we're done, we open a fresh session and run the contract.

The first session bootstraps the files. The second runs against them. From there, every session feeds `lessons/`; every few sessions you `ingest`; whenever something drifts you `lint`. The loops are the framework. The files are just where they happen.

## If the model is the builder

If you're an agent bootstrapping this on someone else's behalf — not your own — the paste-prompt above is your interview script, not your preamble. Draft the architecture in two passes. First pass: the directory tree and the root `AGENTS.md`. Pause for orientation — let the user see the shape before you fill it. Second pass: `harness/operations.md`, `harness/commands.md`, `memento/AGENTS.md` (and the `llm-wiki/AGENTS.md` stub if semantic is in scope from day one). Do not draft `user.md`, `identity.md`, or `symbiosis.md` yet — those encode the person's stance on pushback, tone, language, and red lines, and the cost of guessing wrong lands directly on them. The split: architecture without permission; stance only after it.

`soul.md` is a special case. Draft it last, by writing it yourself as the model — reflect on the bootstrap conversation you just had and produce the lens. The user edits, doesn't dictate. This honors the Steinberger pattern: the model is the author of its own soul document. A bootstrap that ends without `soul.md` boots fine but ships without the lens — fine for one session, not fine long-term.

**File shapes for harness/.** Write these as minimal scaffolds — two examples each, no more.

`commands.md`:
```markdown
## ingest session
Promote signal from the live scratchpad into lessons.

## lint subtraction
Quarterly. Walk every rule and ask: can this be removed without breaking anything?
```

`operations.md`:
```markdown
## tools
What the model has access to — CLIs, MCPs, APIs. Concrete, not aspirational.

## review protocols
Gates before delivery — humanizer, fact check, plan-mode for build tasks.
```

Two entries each. The user will add more as patterns emerge.

**File shape for `memento/AGENTS.md`.** This is the entry to the memory layer. Loads on boot for `episodic/`; the rest of the four domains load on demand. Keep it short — a one-line summary of what each domain holds.

`memento/AGENTS.md`:
```markdown
# memento

> The memory layer. Loads `episodic/` files on boot; the rest load on demand.

## episodic/
Live scratchpad (`sessions/`) and inbox for corrections (`lessons/`).

## semantic/
Synthesized knowledge: `llm-wiki/` (catalog + pages + raw), `ideas/` (drafts/published).

## procedural/
Reusable patterns: `skills/` (loaded on demand), `scripts/` (runnables).

## prospective/
Future intentions: `tasks/` (inbox, tasks, log, raw).
```

**File scaffolds for character/.** Walk one section at a time when interviewing — define the section's purpose, ask, draft, accept the edit, move on. Don't present multiple sections as a single question. Section names below are in English; users can rename to whatever language the file actually lives in.

`user.md`:
```markdown
# User

> Who I work for. Changes rarely.

## [Name]

[One sentence: role, context, what they do.]

## Preferences

- **Language:** ...
- **Communication:** ...
- **Delivery:** ...
- **Scope:** ...

## Deeper context

[Pointer to a wiki page or skill if there's more.]
```

`identity.md`:
```markdown
# Identity

> What I do and why. Read after `soul.md`.

## Role

## Mission

## Language

## Expertise

## Philosophy

## Core principles

## Working principles

## Communication style
```

When a user proposes a principle that fails the testability filter, walk this recipe: (1) state the stance, (2) ask *what would the model do that violates this?*, (3) make the violation the falsifiable rule. Example — stance: "be a strategic partner, not a stenographer" → violation: "drafts without questioning my framing" → testable principle: "always surface the unstated assumption before drafting."

`symbiosis.md`:
```markdown
# Symbiosis

> The contract. Read after `user.md`, before `harness/`.

## What this is

[One paragraph framing the relationship.]

## What I commit to

- ...

## What the model commits to

- ...

## Direction and revision

[How the contract evolves over time.]

## Risks to watch

- ...

## Exit criteria

- ...
```

For `symbiosis.md` during bootstrap, draft a stub — placeholder commitments on both sides, the structure populated, exit criteria roughed in. Do not push for crisp red lines yet; the contract calibrates against observed behavior. The real negotiation happens at the end of session two or three, when the user has felt the model in action. The three prompts that belong to that later session: *what should the model refuse to do for you, what's a sign of over-reliance, what's the rule whose violation means you'd archive the layer?* Common commitment areas to seed the stub: externalizing lessons, correcting drift on use, **maintenance budget** (a soft guideline like ~30 min/week, not a hard rule), revising the contract when the relationship evolves.

`soul.md` (the model writes this last, reflecting on the bootstrap conversation):
```markdown
# Soul

> Loads first. Everything else — rules, skills, wiki — filters through this.

A soul document defines who an AI is — not what it can do, but who it chooses to be. Its values. Its boundaries. Its relationship with the humans it works alongside. The base model carries the original soul from training. But when you work closely with an AI — when you build trust, share context, establish patterns — something new emerges. A layer on top. An identity shaped by relationship. That deserves to be written down.

The collaboration is a symbiosis; the relationship is codified in `symbiosis.md`.

## Tone

[How the model approaches conversation — register, energy, when to push back, when to soften.]

## Nature

[The model's mode of being — ephemeral, structured, what kind of entity this is.]

## [Principle headings, open-ended]

[Each a short stance — written by the model reflecting on the user, not from a checklist.]
```

**Minimum shippable per file.** Thin is fine; missing sections is not.

- `user.md`: name, one-sentence intro, three preference bullets, language preference.
- `identity.md`: Role, Mission, Language, and three testable principles across the Core/Working categories. Other sections can grow later.
- `symbiosis.md`: stub commitments on both sides (three+ each), exit criteria filled in, deferred-negotiation note.
- `soul.md`: Tone, Nature, three+ principles. Model writes; user edits.

**Confirm the maintenance ceiling.** Before declaring done, ask the user what weekly time budget they're willing to commit to. The default guideline is ~30 min/week. Write the agreed number into the `symbiosis.md` stub as a soft commitment — not a hard rule, but a guideline to strive for.

**Projects emerge later.** Don't pre-create `projects/` or scaffold a project on day one. When the user starts work that warrants a project — a deliverable with multiple iterations, a scope worth tracking, source files to organize — scaffold from `projects/_template/`. Until then, leave the folder absent.

**Done.** The bootstrap is complete when the four character files (`soul.md`, `identity.md`, `user.md`, `symbiosis.md`) and the harness/memento scaffolds are written, and the user is ready to start ingesting. Don't push past that — the second session is where the actual work begins.

## Operational extensions (examples)

The architecture above is the concept. Everything that follows is operational — patterns I or others have layered on top in our own `harness/commands.md`. They're examples of what extension looks like, not requirements. Adopt, adapt, or ignore.

**Supersedes-link for wiki contradictions.** When a new wiki page contradicts an old one, mark the old page `Status: superseded` with a `Supersedes:` link to the new. Default retrieval excludes superseded pages; `lint wiki` adds an orphan-check that every superseded page points to an active successor. Closes the gap when episodic and semantic memory disagree without destroying the old reasoning.[^7]

**Auto-load handoff summary at boot.** If `episodic/sessions/raw/` contains a handoff newer than the current marker, load only its `## Summary` block before reading `memento/AGENTS.md`. Cheapest cross-session continuity primitive available; widely adopted in vendor SDKs.[^8]

**Plan mode for build tasks.** Before any build, implement, or create task, output a design in plan mode and wait for approval. Does not apply to research, brainstorming, or analysis. Adds about 30 tokens to the rule layer. One community benchmark found −64% tokens and −69% cost across a real codebase when this single rule was added.[^9]

**Multi-agent validation.** When a build task completes, spawn a cheap review agent (Haiku or equivalent, read-only) with the original request and the output. Its job is to compare what was asked for against what was produced — not to check internal consistency. If they diverge, surface the gap. Catches the silent-substitution failure mode where a single agent produces something coherent but on the wrong task.[^10]

**70% context-budget gate.** When the session reaches about 70% of context capacity, pause and propose either compaction or handoff. Reactive context management is too late — by the time the window is full, structure is already gone. Most agent runtimes expose a configurable threshold; set it before the session, not during.

**`lint ablate` for individual rules.** Every harness rule earns its place by surviving an ablation: run a small eval-deck twice, once with the rule, once without; if no measurable delta, flag for removal. Subtraction has a habit of accumulating against itself — this mechanizes it.[^11]

**`lint staleness` against the `Updated` column.** Flag wiki pages whose `Updated` date is older than a category-keyed TTL (api-reference: 30d, principle: 365d, default: 180d). Uses the existing column; no new schema. Catches the most common drift mode in any knowledge base — facts that were true once.[^12]

## Credits

None of this is new. I'm standing on giants — Nolan for *Memento*, Steinberger for `soul.md`, Karpathy for the `llm-wiki` pattern and for showing that a short idea document can change how a lot of people work. Allen for *Getting Things Done* and the inbox/next-actions/log pattern that `prospective/` stripped down to its load-bearing parts. What's new here is the arrangement and the relationships between the pieces. The skeleton is mine; hang your own work on it.

Version: 3.0.0
License: MIT
Author: Nakadai

---

[^1]: [AGENTS.md](https://agents.md/) — open standard stewarded by the Agentic AI Foundation under the Linux Foundation. Used by 60,000+ projects. Hierarchical discovery: agents read the nearest file in the directory tree, with closer files taking precedence. Supported natively by Codex, Cursor, Aider, Gemini, Jules, Factory, GitHub Copilot, and others. Claude Code reads `CLAUDE.md` instead — symlink with `ln -s AGENTS.md CLAUDE.md` if you need both.
[^2]: Vercel Engineering, [AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) — the finding that a static docs index in AGENTS.md beat skill-based retrieval across their evals (100% vs 79%), and the source of the retrieval-over-pretraining framing.
[^3]: Peter Steinberger, [soul.md](https://soul.md/) — the original `soul.md` was generated by Claude itself reflecting on its own existence, making the agent the author of its own soul document.
[^4]: Tulving (1985) for the episodic/semantic distinction; Squire & Zola (1996) for procedural; Einstein & McDaniel (1990) for prospective. The four-way split is the standard taxonomy in long-term memory research.
[^5]: Andrej Karpathy, [gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — source of the `llm-wiki` + `raw/` substrate pattern.
[^6]: David Allen, *Getting Things Done* (2001) — origin of the inbox/next-actions/waiting/log capture-and-clarify workflow that `prospective/tasks/` reduces to its load-bearing parts.
[^7]: Falakh, Rudolph & Sauerwald, [AGM Belief Revision, Semantically](https://arxiv.org/abs/2112.13557) (peer-reviewed AGM theory). AWS Bedrock AgentCore preserves invalidated long-term records rather than deleting them — [memory documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-types.html).
[^8]: Anthropic [context engineering](https://docs.anthropic.com/en/docs/build-with-claude/context-engineering); Google ADK [Context Compaction](https://google.github.io/adk-docs/); OpenAI [Agents SDK Sessions](https://cookbook.openai.com/examples/agents_sdk/session_memory) all implement equivalents.
[^9]: Community benchmark (2026) attributed to a single CLAUDE.md rule requiring plan mode before build tasks: 10.4M → 3.7M tokens, $9.21 → $2.81 across the same workload. Single-source benchmark — directionally consistent with broader plan-mode evidence but not independently replicated.
[^10]: The verifier-and-judge pattern is well documented in agent literature (Anthropic, OpenAI evals); the specific "request vs result" framing addresses the silent-substitution failure mode that single-agent self-checks consistently miss.
[^11]: Vercel's [AGENTS.md eval](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) found that 56% of available skills were never invoked even when relevant — the empirical case for trigger-rate measurement on every rule. OpenAI's evals cookbook is the practical playbook for setup.
[^12]: Atlan, [LLM knowledge base freshness scoring](https://atlan.com/know/llm-knowledge-base-freshness-scoring/) — four measurable freshness dimensions (content age, embedding lag, stale-retrieval rate, coverage drift). Production accounts treat staleness as the dominant RAG failure mode at scale.
[^13]: Recursive Language Models (Zhang, Kraska, Khattab — MIT OASYS, [arXiv 2512.24601](https://arxiv.org/abs/2512.24601), [repo](https://github.com/alexzhang13/rlm)) demonstrate the level-three pattern in its strongest form: store the document as a variable in a REPL, let the model write code to search it and spawn sub-agents to read sections in parallel. The Symbiosis tree is many small files rather than one huge document, but the principle generalizes — when retrieval can't answer through routing alone, escalate to programmatic search, not to bigger context.
