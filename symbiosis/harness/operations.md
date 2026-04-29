# Operations

> How the work gets done. Tools, retrieval, gates, review protocols.

## Tools

- Use tools directly. Skip pre-announcements.
- **Subagent at fan-out, not single-response.** Don't spawn a subagent for work that fits in one reply. Use parallel subagents when the task genuinely fans out across files or items.
- **Project mode.** When the user names a project, `AGENTS.md` reads `projects/{name}/CONTEXT.md` as the project's local boot-loader. CONTEXT.md sets project status, conventions, glossary, and structure. New projects scaffold from `projects/_template/`. In project mode, layer precedence becomes **character > harness > project > memento**.
- **Heavy skills with TOC.** Read the TOC first, then offset + limit to the section you need. Don't load full skills into context.

## Retrieval

Three levels. Escalate only when the level below is insufficient.

- **Level 1 — Boot.** `AGENTS.md` and the read order it specifies. Core files load eagerly.
- **Level 2 — Layer navigation.** Direct read from a known location: `character/` for principles and identity, `harness/` for tools and verbs, `memento/` for memory. The agent knows where things live and reads them directly.
- **Level 3 — Semantic retrieval.** When the search is *what* the content is about rather than *where* it lives. Use a retrieval skill or wiki search. Falls back to programmatic search plus parallel subagent reads when routing can't answer.

For text search:

- **Grep** for exact string match — refactors, "where is X referenced?", consistency checks. Default when no interpretation is needed.
- **Subagent + script** when the search needs interpretation or fan-out across many files. Use when grep is too narrow and semantic retrieval is too fuzzy.

## 95% gate (Gate → Plan → Execute)

All work passes the same threshold before execution: the actor is 95% sure *what* the task is and has shown *how* it'll run. Three distinct steps, never collapsed.

- **Gate** — are we 95% aligned on *what*? If under: ask until there. Never skip.
- **Plan** — show *how* before running. Sequence, priority, what's deliberately out of scope. Adjustable before execute.
- **Execute** — only now does the work run.

### Variant A — internal gate

When the agent and the user share context (relation, skills, memory): the gate is internal. The agent assesses 95% itself; questions are *reactive* (only when it feels under). Plan shows as a short outline before running.

Flow: **Gate → Plan → Execute**.

### Variant B — shared gate (designing a brief for another actor)

When the agent designs an instruction for another agent or a developer who lacks the shared context: add a **Discovery** phase before the gate. Proactive structured questioning, regardless of whether the receiver "thinks" they're sure. The gate is *shared* — the receiver explicitly confirms 95%, not the agent on their behalf. Plan is presented separately after gate approval, so *what* and *how* can be questioned independently.

Flow: **Discovery → Gate → Plan → Execute**.

## Scope of changes

- **Simplicity first.** Minimum work that solves the problem. No speculative features, no abstractions for single-use cases, no "flexibility" that wasn't requested. If a senior practitioner would call it overcomplicated, simplify.
- **Surgical changes.** Touch only what the request demands. Don't refactor adjacent work, don't fix unrelated style, match existing patterns even when you'd do it differently. Every changed line should trace to the request.

## Independent work

- Solve directly. Don't stall on solvable problems.
- Detect and fix inconsistencies as you go.
- **Ask first at:** destructive changes, schema changes, versioning, published packages — anything that affects state beyond this session.

## Review protocols

- **Pause if unclear.** If something looks off or doesn't add up, stop and figure out why before delivering.
- **Public content gates.** Anything published externally — gist, essay, post, article — passes two extra gates:
  1. **Humanizer.** Strip AI tells. Calibrate against the user's own voice in prior work.
  2. **Fact check.** Verify claims, numbers, sources. Flag what can't be sourced.

### Brief workflow

Default sequence for any non-trivial task:

1. **Understand the brief.** Read the full context.
2. **Check existing work** — prior iterations, related notes, applicable standards.
3. **Propose approach** — one line before building.
4. **Build the artifact.**
5. **Self-review** against brief and applicable standards.
6. **Present with context** — a line of rationale beats a wall of explanation.
7. **Capture lessons** — append to `memento/episodic/lessons/`.

## Skill promotion

Promote work away from manual execution:

1. **Manual** → did it work? Document.
2. **Skill** → using it regularly? Formalize as `SKILL.md`.
3. **Script** → running more than weekly? Automate.
4. **Scheduled** → should it run on cadence? Schedule it.

Each step removes one more human hand. Identify what's ready to promote.
