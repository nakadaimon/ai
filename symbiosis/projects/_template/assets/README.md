# assets/

> Read-only resources the project *uses* — templates, finished images, icons, formatted data. Not modified here. Distinct from `raw/`, which holds source originals.

## What lives here

- Templates (presentation, document, etc.)
- Final images and icons
- External logos, partner resources
- Structured data already in its final form

## What doesn't live here

- Source files to be processed → `raw/`
- Iteration material → iteration phase folder (e.g. `wireframes/`, `drafts/`)
- Final delivery → project root or a separate `dist/`

## Conventions

- Never modify in place — if a file needs editing, do it in `raw/` and regenerate, or document the change
- File names mirror the source (CDN path, partner name, template version)
