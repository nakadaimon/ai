# inbox/

> Unsorted incoming material for the project. Source files, screenshots, exports, notes — drop them here first. `ingest project` moves each item to its right place.

## Convention

Mirrors the wiki-inbox pattern (`memento/semantic/llm-wiki/{wiki}/inbox/` → `raw/{domain}/` via `ingest inbox`):

```
inbox/  →  raw/                  (source files — Excel, Word, data, exports)
       →  assets/                (finished resources — design exports, screenshots, logos)
       →  CONTEXT.md             (if the material updates status, structure, or links)
       →  requirements.md        (if the material changes scope or success criteria)
       →  {iteration-phase}/     (if the material is input to ongoing exploration or build)
```

## When to use inbox

- An email arrived with a file — drop in `inbox/`, ingest later.
- Exported a frame, took a screenshot — `inbox/`, ingest to `assets/`.
- A colleague sent a spec — `inbox/`, ingest to `raw/` plus update `requirements.md`.
- A note from a meeting — `inbox/`, ingest to either CONTEXT.md (status) or a feature brief (input to exploration).

## Conventions

- File names retained from source when possible — traceability.
- Inbox is *transient*. If something sits there unprocessed for long, surface it in CONTEXT.md `Next` or create a task.
- If the file is clearly a `raw/` or `assets/` file from the start, skip inbox and place it directly. Inbox is for *uncertainty*: "worth keeping, but I don't know where yet".

## Relationship to wiki-inbox

The wiki-inbox (`memento/semantic/llm-wiki/{wiki}/inbox/`) is for material that becomes wiki knowledge without project binding. The project inbox is for material that becomes project artifacts. Same pattern, different layer.

**Canonical rule.** Project-relevant files live in the project — `projects/{name}/raw/` or `projects/{name}/assets/` is canonical. Wiki pages that need the source reference the project path in their `sources:`. The lint command `lint project sources` flags drift when the same file ends up in both. Wiki/raw is reserved for files that aren't project-bound.
