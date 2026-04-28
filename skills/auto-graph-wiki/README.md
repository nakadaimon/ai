![ Auto Graph Wiki](autographwiki.jpeg)

# Auto Graph Wiki

A retrieval layer for an LLM-wiki. Adds a TF-IDF index over markdown frontmatter and body, plus a search interface that returns relevant snippets at a fraction of the token cost of full-file reads.

Built on top of the LLM-wiki paradigm — curated markdown notes the agent reads for context. The pattern was introduced by Andrej Karpathy ([gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)). **If you don't have an LLM-wiki yet, start there.** This skill assumes you are already running one. If you are, augmenting it with cheap retrieval typically reduces query cost by ~20×.

## How you run it

The skill is a folder of Python scripts. **You point your agent at the folder and let it run the right script when you ask.** Drop the folder into your host's skills directory (Claude Code, Cursor, Cowork — anything that reads `SKILL.md`); the host parses `SKILL.md`, learns the triggers, and dispatches scripts on your behalf.

You never type a script name. You ask in natural language; the agent runs the right thing:

| You say | Agent runs |
|---|---|
| "What did I say about X?" | `scripts/search.py --query "X"` |
| "Everything about [domain]?" | `scripts/search.py --domain ... --query "..."` |
| "What links to page X?" / "What does X point to?" | `scripts/links.py --page "X"` |
| "Which wiki-links are broken?" | `scripts/broken.py` |
| "Is the index up to date?" | `scripts/freshness.py` |
| (you just edited the wiki) | nothing — `search.py` auto-reindexes on the next query |

If you don't have an agent host, every script also runs directly: `python3 scripts/search.py --query "..."`. But the design intent is natural language → agent → script.

**Requirements.** Python 3.10+, standard library only. No `pip install` for runtime.

## Quick start

```bash
# 1. Configure your wiki path in llm_wiki_paths.json
#    (defaults to the bundled examples/ directory)

# 2. Build the initial index (one-time)
python3 scripts/reindex.py

# 3. Search
python3 scripts/search.py --query "sourdough hydration" --pretty
```

That's the whole loop. **Edit your wiki freely from this point on.** Every `search.py` call re-checks freshness and rebuilds if needed — you won't run `reindex.py` again unless you opt out of auto-reindex with `--no-auto-reindex`. The "auto" in the name means *you don't think about indexing*.

Optional follow-ups:

```bash
# Generate a derived overview page (frontmatter table grouped by domain)
python3 scripts/generate_index.py --scope llm-wiki --out indexes/llm-wiki-index.md

# Find broken wiki-links (pages that don't resolve)
python3 scripts/broken.py --pretty

# Check freshness manually (mtime + schema-version drift)
python3 scripts/freshness.py --pretty
```

## File layout

```
auto-graph-wiki/
├── SKILL.md                  # Natural-language instructions for an agent
├── README.md                 # This file
├── llm_wiki_paths.json       # Configuration: scope name, vault path
├── indexes/                  # Generated JSON indexes (one per scope)
├── examples/
│   ├── llm-wiki/             # A small example wiki you can run against
│   └── edge-cases/           # Edge-case test vault (code blocks, escapes, unicode)
├── tests/
│   └── test_edge_cases.py    # Pytest suite for the extractor
└── scripts/
    ├── index.py              # Build a single scope's index
    ├── reindex.py            # Rebuild every configured scope
    ├── search.py             # Top-k retrieval with auto-reindex
    ├── links.py              # Wiki-link graph traversal
    ├── broken.py             # List broken wiki-links per scope
    ├── freshness.py          # Drift detection (for lint pipelines)
    └── generate_index.py     # Auto-generate a markdown overview
```

## Configuration

Edit `llm_wiki_paths.json` to point at your own wiki:

```json
{
  "index_dir": "./indexes",
  "scopes": {
    "llm-wiki": {
      "vault": "~/path/to/your/wiki"
    }
  }
}
```

Vault paths can be absolute, `~/` for home directory, or relative to the config file. Multiple scopes are supported — add as many as you have separate wikis.

## Frontmatter that makes the graph sharp

The skill works on any markdown with frontmatter, but quality goes up sharply when notes carry the right metadata. The fields below are what `search.py`, `links.py`, `broken.py`, and `generate_index.py` actually read. Add what serves you; skip what doesn't fit.

| Field | Why it matters |
|---|---|
| `title` | First H1 is used as fallback. Explicit `title` lets you decouple display name from filename. |
| `summary` | Shown in every search result. Often answers the user's question on its own. |
| `keywords` | Boosts search recall when the body uses different vocabulary than the query. |
| `aliases` | Names this page can be referenced by from `[[wiki-links]]`. Crucial for graph resolution. |
| `related` | Curated outgoing links beyond the body's `[[wiki-links]]`. Used by `links.py` and `broken.py`. |
| `domain` | Enables domain-scoped search (`search.py --domain ...`) and grouping in `generate_index.py`. |
| `updated` | Surfaces in index views; supports staleness-tracking in your lint pipeline. |

The parser also accepts a few common English synonyms for each field (e.g. `description` for `summary`, `category` for `domain`, `modified` for `updated`). See `index.py` and `generate_index.py` for the full list. **Pick one form and use it consistently** — the skill normalizes either way, but mixed vocabulary makes the vault harder for *you* to maintain.

Example minimum frontmatter:

```yaml
---
title: Quarterly revenue by segment
summary: Revenue breakdown across the four reporting segments, with quarter-over-quarter deltas and the methodology used to compute them.
keywords: [revenue, segments, reporting, quarterly]
domain: finance
aliases: [quarterly-revenue, segment-revenue]
related: [[reporting-methodology]], [[segment-definitions]]
updated: 2026-01-15
---
```

Three principles when adopting frontmatter at scale:

- **Consistency beats completeness.** A wiki where every page has `summary`, `keywords`, and `aliases` filled in — even minimally — outperforms one where some pages have rich frontmatter and others have none. The graph is only as good as its sparsest section.
- **Aliases are how the graph knows what your pages are called.** A page named `quarterly-revenue-by-segment` won't backlink from `[[Quarterly revenue]]` in prose unless `Quarterly revenue` is listed in its `aliases`. Add aliases for the words you actually use when referring to the page.
- **`related:` is curated graph context.** Inline `[[wiki-links]]` in the body capture intention at a moment. Frontmatter `related:` captures *the page's permanent neighbors*. Both end up in the graph; both add value; they are not the same.

Indexes regenerate automatically when frontmatter changes — there's no migration step.

## How retrieval works

Given a query, search runs through this pipeline:

1. **Tokenize** the query — lowercase, drop stopwords, keep meaningful terms.
2. **Load** the JSON index for the relevant scope.
3. **Score** each chunk using cosine similarity between the query's TF-IDF vector and the chunk's. Common words contribute almost nothing because their inverse document frequency is low; rare, specific terms dominate the score.
4. **Sort** and return the top *k* — typically five.
5. **Decorate** each result with metadata from the page's frontmatter: title, breadcrumb, summary, keywords, aliases, related pages, last-updated date.

Total cost of a typical query: ~500 tokens of context, returned in milliseconds. Compare to ~10 000 tokens for reading whole files.

## Auto-reindexing

The skill name is "auto" because indexing is automatic at three points:

- **Lazy at search.** Every `search.py` call checks index freshness. If any wiki file is newer than the index, search rebuilds before returning. Disable with `--no-auto-reindex` if you prefer manual control.
- **Active at lint.** `freshness.py --auto-fix` rebuilds stale indexes on demand. Wire this into your host harness's lint pipeline.
- **Coupled at ingest.** Whatever pipeline writes new pages to the wiki should run `reindex.py` as a final step. Documented in your host's command file.

A correctly integrated install means you never type "reindex" by hand.

## Trade-offs

**TF-IDF is keyword-based.** A query for "compliance" will not match a wiki that uses "regulation". The augmentation rewards consistent vocabulary in the source — consider it a feature.

**Indexes are rebuilt from scratch.** Not incremental. For wikis up to a few thousand pages this is fine — full reindex completes in a couple of seconds. For larger wikis, incremental indexing would need to be added.

**JSON indexes are not for humans.** They are fuel for `search.py`. Do not open them in a markdown editor.

## Wiki-link extraction

Wiki-links in the body — `[[target]]`, `[[target#heading]]`, `[[target|alias]]`, `[[target#heading|alias]]` — are extracted as structured records. Each link in the index has `target` (lowercased), `heading`, `alias`, and the original `raw` form.

The extractor masks code spans before scanning, so links inside fenced code (` ``` `, `~~~`), inline code (`` ` ``), HTML comments, indented code blocks, and escaped `\[[...]]` are correctly ignored.

`broken.py` walks the graph and lists links whose targets don't exist:

```bash
python3 scripts/broken.py --pretty
python3 scripts/broken.py --scope my-vault
```

## Schema versioning

Each generated index carries `index_version: 2`. When `search.py` or `freshness.py` encounters an older or missing version, the index is rebuilt transparently before the request is served. Users never run a manual migration command.

## Trade-offs

**Regex-based extraction.** The wiki-link parser is regex with masking, not a full Markdown AST. It handles 99% of cases (kafe blocks, inline code, comments, escapes, unicode) but is not full CommonMark-compliant. If your wiki uses exotic markdown patterns, file an issue.

## For contributors

Run the test suite:

```bash
pip install pytest --break-system-packages
python3 -m pytest tests/ -v
```

Tests cover the edge-case vault under `examples/edge-cases/`. Pytest is a test-time dependency only — the runtime is Python-standalone with no third-party packages.

## What this is not

This is a retrieval layer for *already-curated* knowledge. If your wiki is unstructured — no frontmatter, inconsistent terminology, no manual organization — the augmentation will not save you. The discipline of writing the wiki is what makes the cheap retrieval possible.

This is also not a knowledge graph extractor. If you have unfamiliar material (a codebase you didn't write, papers you haven't read), you need extraction tools, not retrieval tools. Those are different problems.

## License

MIT.
