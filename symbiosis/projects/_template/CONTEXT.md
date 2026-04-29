# [Project name]

> [One-paragraph framing: what this is, who it's for, what done looks like.]

> _Projects live in `projects/` — sibling to `character/`, `harness/`, and `memento/`. Project artifacts (code, files, source documents) live here; the memory of the work — raw research, distilled knowledge, lessons — lives in `memento/`._

## Structure

Standard folders — remove what isn't used, add project-specific ones as needed:

```
project-name/
├── CONTEXT.md            # this document — the project brief
├── requirements.md       # business requirements, scope, success criteria (opt-in)
├── dependencies.md       # technical dependencies, tools, libs (opt-in)
├── inbox/                # unsorted incoming material — `ingest project` sorts
├── raw/                  # source files (Excel, Word, data, unmodified)
├── assets/               # finished resources used by the project
└── tokens/               # translation layer between sources and delivery (opt-in)
```

**Iteration phases are domain-specific.** Add folders that match the work — examples:

- Design: `wireframes/` (cheap exploration) + `design/` (build phase)
- Writing: `drafts/` + `revisions/`
- Code research: `exploration/` + `implementation/`
- Calibration of instructions: `training/`

The pattern is universal — cheap exploration → commit → ship — but the names follow the work. Each phase produces both a visual artifact and a brief.

**Other paths that matter:**

- `harness/commands.md` — ...
- `memento/semantic/llm-wiki/...` — ...

## Pipeline

```
raw  →  tokens  →  exploration  →  build  →  delivery
                       ↕
                 calibration (optional)
```

`raw` feeds `tokens`. `tokens` translate sources into substrate (typography, color, data, parameters) the project consumes. Exploration phase produces variants and locks a brief. Build phase iterates against the brief to a master. Calibration loops alongside when instructions or process need sharpening — each iteration is a learning cycle that lands in `tokens/`, a brief, or a type-level rule.

Not every project needs every phase. Lightweight projects skip `tokens/` and calibration. Production-heavy projects run the full chain.

## Glossary

[Project-specific terms, names, acronyms, domain concepts the agent should know.]

- **[term]** — ...
- **[term]** — ...

## Conventions

[Naming, formatting, project-specific rules. Things to honor, things to never do.]

- ...
- ...

## Status

[Where the work stands. A quick state list, or a multi-axis tracking table for projects with tracked artifacts.]

- ...
- ...

## Next

[Open threads, planned work, pending decisions.]

- ...
- ...

## Working here

[Optional. Project-specific rules for how the agent approaches work in this project. Diverge from general harness only when there's a real reason — path conventions, domain-specific iteration style, what to read first.]

- ...
- ...
