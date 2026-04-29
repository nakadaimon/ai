# Changelog

All notable changes to the symbiosis architecture are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Versions 2.4.0 onward were driven by blind onboarding tests — each version was tested by simulating a first-time user being bootstrapped through the manifesto, and findings were applied to the next version. Methodology details at the bottom.

## [3.0.0] — 2026-04-29

Two major changes.

First: a new top-level `projects/` layer joins character, harness, and memento. Project artifacts now have a documented home alongside the memory layer; the agent reads a project-specific `CONTEXT.md` as a local boot-loader when the user names a project. The mental model gains a fourth pillar and a few load-bearing rules around it.

Second: the release ships a working reference tree. Earlier versions shipped only the manifesto (a README that described what to build); 3.0.0 ships the manifesto *plus* the scaffold to actually run it — root `AGENTS.md`, `character/` (templates per "let the model draft yours"), `harness/` (`operations.md` and `commands.md` filled with reference content), `memento/` (domain-agent plus four sub-domains marked with `.gitkeep`), and `projects/_template/`. Clone the tree, edit the stubs, and you have a runnable symbiosis without re-deriving structure from prose.

Major version bump for the architectural addition. No existing files break.

### Added

- **Reference implementation tree.** The release ships a complete working scaffold alongside the manifesto. Root `AGENTS.md` (boots the structure, version-stamped). `character/` with stubs for `soul.md`, `identity.md`, `user.md`, `symbiosis.md` (intentionally thin — the model drafts these). `harness/` with `operations.md` (tools, retrieval, gates, review protocols) and `commands.md` (ingest + lint verbs filled out). `memento/` with the domain-agent plus four sub-domains seeded with `.gitkeep`. `projects/_template/` with the new project scaffold. Prior versions shipped only the README; this is the first release where the README is accompanied by the structure it describes.
- **`projects/` layer.** Work artifacts (code, designs, drafts, source documents) live in `projects/{name}/`, sibling to character, harness, and memento. Memento holds the memory of the work; projects hold the work itself. The split keeps the memory layer transferable across project rearrangements without rewrites.
- **`projects/_template/` scaffold.** Copy-and-adapt scaffold containing `CONTEXT.md`, opt-in `requirements.md` and `dependencies.md`, plus stub READMEs for `inbox/`, `raw/`, `assets/`, and `tokens/`. New projects start as `cp -r projects/_template projects/new-project`.
- **Project mode (root `AGENTS.md` step 5).** When a project is named (in platform instructions, env, or first message), the agent reads `projects/{name}/CONTEXT.md` and treats it as the local boot-loader. Missing `CONTEXT.md` → offer to scaffold from the template. Unknown project → confirm before creating.
- **Conditional layer precedence.** In project mode: **character > harness > project > memento** — local project context overrides general history. Outside project mode the original precedence is unchanged.
- **Pipeline concept in `CONTEXT.md` template.** `raw → tokens → exploration → build → delivery`, with calibration cycling alongside. Iteration-phase folders are domain-specific (design uses `wireframes/` + `design/`, writing uses `drafts/` + `revisions/`, code research uses `exploration/` + `implementation/`); the pattern is universal but the names follow the work.
- **Visual + brief output rule.** Each iteration phase produces both a visual artifact and a brief. Artifact without brief leaves decisions invisible; brief without artifact leaves interpretation open.
- **Canonical-source rule.** Project-relevant files are canonical in `projects/{name}/raw/` (or `assets/`), not in wiki/raw. Wiki pages reference the project path in their `sources:` frontmatter. Wiki/raw is reserved for files that aren't project-bound.
- **`ingest project` command.** Walks `projects/{name}/inbox/`, proposes destinations per file (raw, assets, or an update to CONTEXT/requirements/feature-brief), waits for confirmation, moves. Mirrors `ingest inbox` for the wiki, one layer over.
- **`lint project sources` command.** Enforces the canonical-source rule. Two checks: (1) wiki/raw leakage flagged as migration candidates, (2) dual-copy drift forces an explicit decision (discard project edit, upstream to wiki, or split into distinct files). Lint never auto-syncs.
- **Project inbox pattern.** `projects/{name}/inbox/` is the unsorted drop zone for incoming material; `ingest project` sorts it.
- **`### Projects` sub-section in README.** Explains the layer, boot rule, precedence, structure, pipeline, iteration phases, canonical-source rule, inbox flow, and bootstrapping. Includes a forward-flag for nested `AGENTS.md` per project type (not yet built).
- **"Projects emerge later" guidance** in the "If the model is the builder" section. Instructs bootstrapping agents not to pre-create `projects/` on day one; scaffold from `_template/` only when work warrants it.
- **`See also` section in `memento/AGENTS.md`.** Points to `../projects/` as a sibling layer; clarifies that an agent reading only the memento domain-agent still sees the project layer's existence.

### Changed

- **Root `AGENTS.md` opening blockquote.** "The symbiosis layer" → "The symbiosis architecture (v3.0.0)". Architecture is more accurate than layer — the four pillars (character, harness, memento, projects) are layers; symbiosis is the architecture that holds them.
- **Bootstrap paste prompt** in README. "symbiosis layer" → "symbiosis architecture" for consistency with the new framing.
- **`harness/operations.md`.** `Project context` bullet replaced with `Project mode` bullet — defers to root `AGENTS.md` as the canonical rule, references `projects/_template/` for scaffolding, and documents project-mode precedence.
- **README "How to start".** Adds a sentence about `projects/`: added when work starts, template at `projects/_template/`.
- **README structure tree.** Now includes `projects/_template/` as sibling of `memento/`.
- **README Memento section.** Project-artifacts paragraph collapsed into a brief forward-reference to the new Projects sub-section, since the new section covers the same ground in more detail.

### Removed

- **`projects/example-project/`.** Replaced by the more functionally-named `projects/_template/`. The old folder was a minimal stub; the new folder is a complete copy-and-adapt scaffold.

## [2.8.0] — 2026-04-25

### Added

- **Day-in-the-life paragraph** ("What you actually do") in *How to start*, after Maintenance budget. Three cases when the user touches a file (correction, preference update, quarterly subtraction). The continuity comes from the agent reading the structure, not from the user maintaining it. Closes 2.7.0 P2 — the load-bearing reassurance the framework's value depends on.
- **Delivery surface for `ingest`/`lint`** — sentence appended to the vocabulary block stating these are conversational verbs said to the model, not scripts. Day one all manual; some can be wired up as scheduled tasks where the runtime supports it. Closes 2.7.0 P1.

## [2.7.0] — 2026-04-25

### Added

- **`memento/AGENTS.md` scaffold** as a markdown code block, alongside the existing harness file shapes. Every other bootstrap file now has a scaffold; the memory-layer router is no longer the exception. Closes 2.6.0 P6.
- **Stance-to-principle rewriting recipe** in the `identity.md` scaffold guidance — three steps (state stance → ask "what would violate this?" → make violation the rule), with worked example. Gives the agent a documented move when a user proposes an untestable principle. Closes 2.6.0 P2.
- **Per-file minimum shippable floors** before the *Done* line — concrete content checklist for `user.md`/`identity.md`/`symbiosis.md`/`soul.md`. "Thin is fine; missing sections is not." Closes 2.6.0 P3.
- **Confirm maintenance ceiling** step before declaring done — the agent asks the user for their actual weekly budget and writes the agreed number into the symbiosis stub as a soft commitment. Closes 2.6.0 P8.

### Changed

- **`symbiosis.md` negotiation** rewritten from "surface user's stance with three prompts" to "draft a stub during bootstrap, defer real negotiation to session 2 or 3". The three prompts are kept but explicitly marked as belonging to the later session. Common commitment areas listed: externalizing lessons, correcting drift, **maintenance budget** (soft guideline, not hard rule), revising the contract. Closes 2.6.0 P1, the highest-friction moment in the previous run.

### Skipped

- 2.6.0 P7 (start-minimal vs build-full contradiction): kept build-full at bootstrap so all folders are guaranteed to exist and don't get forgotten later. Did not surface as friction in the 2.7.0 run.

## [2.6.0] — 2026-04-25

### Added

- **Project mapping clarification** in `### Memento` — projects with their own folder structure (code repositories, design files, large source documents) live outside `memento/` in a `projects/` folder alongside. Memento holds raw research and distilled knowledge, not project work itself. The structure is agnostic about where the actual project work lives. Closes 2.3.0 P5 (which had persisted into 2.5.0).
- **Maintenance budget** in *How to start* — concrete ~30 min/week guideline with quarterly `lint subtraction` (30–60 min) and a scheduled-task hint. Smell rule: if maintenance climbs past 30 min/week sustained, run subtraction early. Closes 2.5.0 P2 (the highest-leverage gap in the 2.5.0 run).
- **File scaffolds for character/** in *If the model is the builder* — markdown templates for `user.md`, `identity.md`, `symbiosis.md`, `soul.md`. Section names in English; users can rename to whatever language the file lives in. The `soul.md` scaffold includes a conceptual framing paragraph (a soul document defines who an AI is — the layer that emerges from relationship, not what the model can do) as the file's own intro, so the model has scaffolding to draft against even with thin bootstrap context. Closes 2.5.0 P1 and P3 (replacing the ambiguous category checklist and thin negotiation cue).
- **Done criteria** at end of *If the model is the builder* — bootstrap is complete when the four character files plus harness/memento scaffolds are written and the user is ready to start ingesting. "Don't push past that — the second session is where the actual work begins."

### Removed

- **Principle categories list** (the "pushback intensity, hedging tolerance..." checklist from 2.4.0) — replaced by the explicit 8-section `identity.md` scaffold (Role / Mission / Language / Expertise / Philosophy / Core principles / Working principles / Communication style). The 2.4.0 categories were ambiguous between "internal scaffold" and "questions for the user"; the 8-section file scaffold removes the ambiguity.
- **Slow-down-at-`symbiosis.md`** cue (from 2.4.0) — replaced by the symbiosis.md scaffold and three negotiation prompts (refuse / over-reliance / archive triggers).

## [2.5.0] — 2026-04-25

### Added

- **Conceptual framing** at the top of `## The architecture` — three short paragraphs framing the four pieces (three structural — layers, memento, routers; one contractual — `symbiosis.md`) and explaining why the architecture is named after the contract. Sets up the argument before the user meets the structure, addressing the latent "why is it called symbiosis when it's a folder full of files?" question.

## [2.4.0] — 2026-04-25

### Added

- **Glossary** at the top of *How to start* — inline paragraph with bolded terms covering `AGENTS.md`, `soul.md`, `identity.md`, `user.md`, `symbiosis.md`, `memento`, `ingest`, `lint`. The bootstrap agent can paste from it; users can skim it. Closes 2.3.0 P1 (jargon dump in early bootstrap turns).
- **Project example crossing memento domains** in `### Memento` — concrete worked example showing how a single project lands across `prospective/tasks/`, `semantic/ideas/drafts/`, `semantic/llm-wiki/raw/`, `episodic/lessons/`. "Projects don't get folders; memory does." Closes 2.3.0 P5 partially (full closure came in 2.6.0 with the project-mapping clarification).
- **Two-pass architecture pacing** in *If the model is the builder* — first pass draws directory tree + root `AGENTS.md`, pause for orientation, second pass adds harness + memento scaffolds. Don't draft `user.md`, `identity.md`, `symbiosis.md`, or `soul.md` yet. Closes 2.3.0 P4 (single-turn scaffold dump).
- **`soul.md` Steinberger procedure** in *If the model is the builder* — model drafts last, reflecting on the bootstrap conversation; user edits, doesn't dictate. A bootstrap that ends without `soul.md` boots fine but ships without the lens — fine for one session, not fine long-term. Closes 2.3.0 P3.
- **Signal types** in *The two loops* — state-based (scratchpad over ~2k tokens, corrected mistake worth keeping, draft that has stopped moving, retrieval that returns a stale fact) vs calendar-based (`lint subtraction` quarterly), preserving "mixed cadence" nuance. Resolves the latent contradiction between "on signal, not calendar" and `lint subtraction`'s explicit quarterly cadence. Closes 2.3.0 P7.
- **`.gitkeep` conditional** in *How to start* — added "if you're using git" qualifier. Non-git users no longer told to drop placeholder files they don't need. Closes 2.3.0 P6.
- **`llm-wiki/` sub-catalog scaling** in `### Memento` — when the central `llm-wiki/AGENTS.md` gets too long to skim in one pass, give each topic-domain its own catalog-agent (`llm-wiki/pricing/AGENTS.md`, `llm-wiki/customers/AGENTS.md`, etc.); root `AGENTS.md` becomes a router pointing at sub-catalogs. Same routers-list-and-catalogs-tabulate rule, one level deeper.
- **Principle categories** for `identity.md` in *If the model is the builder* — six categories (pushback intensity, hedging tolerance, language, tone, decision authority, output format). *Removed in 2.6.0* in favor of the explicit 8-section scaffold.
- **Slow-down at `symbiosis.md`** cue in *If the model is the builder*. *Removed in 2.6.0* in favor of the symbiosis.md scaffold and three negotiation prompts.

### Changed

- **`## Four things that matter` → `## The architecture`** — section restructured into six `###` subsections: *Three layers, one router* / *Routers, domains, catalogs* / *Separation of concerns* / *Character* / *Harness* / *Memento*. The umbrella heading no longer describes "four things" since the section now expands into six subsections covering the architectural pattern (three) and the three layers in detail.
- **Symbiosis-is-the-contract content moved into `### Character`** — `symbiosis.md` is now framed as the fourth character file alongside `soul.md`/`identity.md`/`user.md`, instead of standing as one of "Four things that matter". The transition reads naturally via "The fourth character file is `symbiosis.md` — the contract."
- **`### Harness` paragraph written from scratch** — new prose covering `commands.md` (verbs, `ingest` and `lint` load-bearing), `operations.md` (tools + review protocols), and a reference to *Operational extensions* below. Replaces the implicit harness coverage that was scattered across the original "Four things that matter".
- **`## The engine is replaceable`** moved out of "Four things" and promoted to its own top-level section, positioned between *The two loops* and *Exit criteria*. Sets up the engine metaphor (motor / chassis / navigation / driver) before *Exit criteria* references "the engine metaphor holds".
- **`Soul.md` → `soul.md`** in *Three layers, one router* — typography normalized to match the rest of the manifesto (lowercase + backticks).

## [2.3.0] — pre-iteration baseline

The starting point of this iteration. Compared to an earlier unversioned manifesto, v2.3.0 introduced:

### Added

- **Vocabulary normalization to AGENTS.md standard**:
  - `agents.md` → `AGENTS.md`
  - `memento/memento.md` → `memento/AGENTS.md`
  - `llm-wiki/index.md` → `llm-wiki/AGENTS.md`
- **`## How retrieval scales`** — new section with three-level escalation (level 1: AGENTS.md tree; level 2: nearest local AGENTS.md; level 3: programmatic search + sub-agents).
- **`## Operational extensions (examples)`** — new section with six optional patterns: supersedes-link for wiki contradictions, auto-load handoff summary at boot, plan mode for build tasks, multi-agent validation, 70% context-budget gate, `lint ablate` for individual rules, `lint staleness` against the Updated column.
- **Routers, domains, catalogs subsection** inside *Four things that matter* — introduced the Root-agent / Domain-agent / Catalog-agent triad and the "auto-load nearest AGENTS.md" mechanic.
- **AGENTS.md cross-references and YAML frontmatter** paragraph — `Related: harness/operations.md, character/identity.md` pattern as search hints; reserve frontmatter for structured cases.
- **File shapes for harness/** in *If the model is the builder* — markdown skeleton examples for `commands.md` and `operations.md`, two entries each.
- **Boot order detail** — boot also checks `episodic/sessions/` for an in-progress session and surfaces `prospective/tasks/` so the day's work is visible.
- **10 new footnotes**: AGENTS.md standard ([Agentic AI Foundation](https://agents.md/)), cognitive science taxonomy (Tulving 1985, Squire & Zola 1996, Einstein & McDaniel 1990), GTD (Allen 2001), AGM belief revision, Anthropic context engineering, plan-mode community benchmark, verifier-and-judge pattern, Vercel skills eval, Atlan freshness scoring, Recursive Language Models (MIT OASYS). Footnote numbering renumbered accordingly.

### Changed

- **`commands.md`** vocabulary: removed `handoff`; added `lint subtraction` and other lint variants.
- **Symbiosis-is-the-contract paragraph** expanded — added "And the contract makes the human more necessary, not less... Symbiosis lowers the threshold so you can explore more, decide more, write more, with continuity that doesn't depend on memory."
- **Version footer added** (`Version: 2.3.0`).

## Methodology

Versions 2.5.0 onward were validated via a blind onboarding test:

1. Spawn an orchestrator agent with orchestrator instructions.
2. Orchestrator simulates two roles in alternation: a **Bootstrap Agent** (using the manifesto under test as its sole reference) and a **Simulated User** (a senior PM persona with ~9 months of LLM use, comfortable with markdown but not engineering, with a 30-min/week maintenance ceiling). Roles are isolated by discipline; both are played by the same model — a documented caveat that likely makes friction findings conservative.
3. The conversation runs up to 30 turns or until natural stop conditions (user satisfaction, declared done, or loop detection).
4. The orchestrator writes a structured report following the same eight-section template: run summary, what worked, pain points (ranked by severity), gaps in the manifesto, sequence problems, recommendations, meta-notes, full transcript.
5. Findings are reviewed; recommendations applied to the next version; repeat.

### Run progression

| Version | Turns | Outcome | Headline finding |
|---|---|---|---|
| 2.3.0 | 22 | User-satisfied, 7 of 8 files drafted | Vocabulary-heavy friction; jargon dump in early turns |
| 2.5.0 | 22 | Full functional bootstrap | Three high-severity findings; two persisted from 2.3.0 in different form |
| 2.6.0 | 24 | Partial — user disengaged at symbiosis prompts | Friction shifted from missing content to wrong sequencing |
| 2.7.0 | 28 | Full clean run — user said "Done" without prompting | Remaining friction was user-facing reassurances (small, scoped, high-leverage) |
| 2.8.0 | not retested | — | — |
| 3.0.0 | not retested | — | architectural addition (projects layer) — onboarding flow unchanged through 2.8.0 path |

(2.4.0 was not separately tested; it served as the foundation that the architecture restructure was applied to before testing 2.5.0.)

### Pattern across the iteration

> **Missing pieces → wrong order → missing crib-sheets.**

Each fix exposed the next layer of friction. By 2.7.0 the bootstrap mechanics worked end-to-end; the only remaining gaps were small user-reassurance paragraphs and one-line agent crib-sheets. 2.8.0 closed the two highest-leverage of those.
