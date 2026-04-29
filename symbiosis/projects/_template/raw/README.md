# raw/

> Source files — Excel, Word, data exports, raw notes. This is where the project *derives* other artifacts (tokens, requirements, content, summaries) from. Distinct from `assets/`, which holds finished resources.

## What lives here

- Spreadsheets from business systems, partners, external sources
- Word documents from meetings, interviews, vendors
- Raw data files (CSV, JSON exports, dumps)
- Scanned documents, screenshots from other systems

## Conventions

- Files are not modified in place — diff against original must hold
- Derived artifacts (tokens, summaries, requirements) live in their proper place; `raw/` is the source
- File names retain their original when possible — traceability to source
- Files no longer in active use → move to `_archive/` or document what they were for

## Canonical-source rule

Project-relevant files are canonical here, not in `memento/semantic/llm-wiki/raw/`. Wiki pages that need a file reference the project path in their `sources:` frontmatter. If the same filename ends up in both `projects/{name}/raw/` and `memento/semantic/llm-wiki/{wiki}/raw/`, that's drift — `lint project sources` catches it and forces a decision.

## Relationship to other folders

- `raw/` feeds `tokens/` (translation to substrate)
- `raw/` feeds `requirements.md` and CONTEXT.md (when requirements are derived from documentation)
- `raw/` feeds iteration phases (when design or build choices are informed by source files)
