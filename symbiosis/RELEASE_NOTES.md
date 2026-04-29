# Release Notes — 3.0.0

Symbiosis 3.0 ships two things — a working reference tree, and a new top-level layer for project artifacts.

Before, the published version was a manifesto: a README describing what to build. Adopters had to read the prose and derive their own scaffold. With 3.0, the manifesto is paired with the structure it describes. Root `AGENTS.md`, character templates, filled-out harness files, the memento domain-agent with seeded sub-domains, and a project template. Clone the tree, fill in the stubs, run it. The cost of starting drops to copying files rather than re-deriving them.

Second: the architecture grows a fourth pillar. Where 2.x had character, harness, and memento as the three top-level layers, 3.0 adds `projects/` alongside them. Memento still holds the *memory* of work — raw research, distilled knowledge, sessions, lessons — but the *work itself* — code, designs, drafts, source documents — now has a documented home in `projects/{name}/`. Each project carries a `CONTEXT.md` that the agent reads as a local boot-loader when you name the project, plus opt-in folders for source files, finished resources, an inbox, and a translation layer between sources and delivery.

The change is structural; the disciplines that follow are practical. A canonical-source rule keeps files from duplicating between project and wiki. A new `ingest project` verb sorts incoming material from a project inbox. A new `lint project sources` verb catches leakage and drift between the layers. In project mode, layer precedence becomes **character > harness > project > memento** — local project context overrides general history, so the agent doesn't drag a stale wiki entry into work governed by a fresher project brief.

Upgrading from 2.8 is non-breaking. The existing three layers work as before; `projects/` is added when work starts, not on day one. Bootstrap agents are explicitly told not to pre-create projects — they emerge as the work names them.

For new adopters, 3.0 is the easier entry point. Clone the tree, follow the bootstrap interview, and you have a running symbiosis instead of a list of folders to build.
