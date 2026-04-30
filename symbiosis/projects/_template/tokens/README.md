# tokens/

> Translation layer between source files and delivery format or schema. If the project has distinct sources (design-system CSS, requirements Excel, data dump) that need translation into structured substrate before consumption — that's what lives here.

## The concept

```
raw sources  →  tokens (translated substrate)  →  iteration phases consume
```

`tokens/` isn't truth — truth lives in `raw/` or external sources. `tokens/` is the *translation* into a form the project's build can consume directly.

The pattern is generic; the shape varies by domain:

- **Report projects:** Spreadsheet of metrics → typed markdown/yaml ready for report generation
- **UI projects:** Figma variables → CSS/TS tokens

## When the folder is needed — and not

**Needed when** the project has a clear translation task between source and delivery, complex enough to document rather than handle ad hoc.

**Not needed when** the project writes directly in the delivery format without sources, or source and delivery are the same format.

If not needed — remove the folder. An empty folder without function pollutes the structure.

## Conventions

- A `README.md` (or `tokens.md`) at the root documents the bridge convention and what files live here
- Files are generated when possible; keep the generation script alongside when worth it
- Drift between source and delivery is flagged visibly — never silent
