---
name: auto-graph-wiki
metadata:
  version: 2.1.0
description: Cheap retrieval over an LLM-wiki — TF-IDF index with automatic refresh, structured wiki-link graph (target/heading/alias), and broken-link reporting. Built on top of the LLM-wiki paradigm (curated markdown notes with frontmatter). Use when an agent needs to find specific information without paying the token cost of full-file reads, traverse backlinks, or detect graph drift. Returns top-k snippets with metadata in ~500 tokens instead of ~10 000 for a full-file read.
---

# auto-graph-wiki

A retrieval layer for an LLM-wiki. Adds a TF-IDF index over markdown frontmatter and body, plus a search interface that returns relevant snippets to an agent in a fraction of the tokens a `Read` would cost. Indexing is automatic — wired into ingest, lint, and search so the index never drifts from the source.

## Philosophy

This skill assumes you're already running an LLM-wiki — a curated set of markdown notes the agent reads for context. The pattern was introduced by Andrej Karpathy ([gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)). **Don't have an LLM-wiki yet? Start there before installing this skill.**

The wiki pattern works, but it scales poorly: the index file gets heavy, every specific question pulls in whole files, and token budgets balloon.

The augmentation is small. Build a TF-IDF index over the same wiki. When the agent needs something specific, search instead of read. Top-k snippets with metadata, ~500 tokens, twenty times cheaper.

Four principles run through the design:

- **Search first, read second.** A search returns relevant snippets in seconds. Only open a full file if the snippets do not answer the question.
- **Metadata is free context.** Frontmatter (summary, keywords, related) ships with every search result. Often it is enough on its own.
- **Derived artifacts follow the source.** The TF-IDF index is generated from the wiki. When the wiki changes, the index updates automatically — at ingest, at lint, or lazily at search time.
- **Drift is detectable.** Broken links, missing pages, schema-version mismatches — all surface through `broken.py` and `freshness.py`. The graph reports its own gaps.

## Scopes

The wiki is divided into one or more *scopes* — independently indexed sets of markdown files. By default a single `llm-wiki` scope is configured. Add more scopes (e.g. `personal`, `work`) by extending `llm_wiki_paths.json`.

Indexes live in `indexes/<scope>.json` next to the skill.

## When to index

The skill ships with three automation points:

- **At ingest.** When the host agent runs an ingest pipeline that writes new pages to the wiki, the same pipeline runs `reindex.py` as a final step. Documented in the host's command file.
- **At lint.** When the host agent runs a lint pass, it calls `freshness.py`. If drift is detected, lint may either report or auto-fix by triggering reindex. Configurable.
- **At search (lazy).** Each search call checks the index mtime against the wiki mtime. If the index is stale, it is rebuilt before returning results. This is on by default and can be disabled with `--no-auto-reindex`.

A user who installs this skill correctly should never have to type "reindex" by hand.

## Commands

The skill exposes the following scripts. All are runnable directly with `python3 scripts/<name>.py`.

| Script | Purpose |
|--------|---------|
| `index.py` | Build a single scope's index from frontmatter + body. Usually called by `reindex.py`. |
| `reindex.py` | Rebuild every scope listed in `llm_wiki_paths.json`. Cheap — runs in seconds for hundreds of pages. |
| `search.py` | Top-k retrieval. Returns JSON or pretty-printed snippets with metadata. Auto-reindexes if stale or schema-versioned out of date. |
| `links.py` | Traverse wiki-link graph: backlinks and outgoing links for a given page. Path-aware matching. |
| `broken.py` | List wiki-links whose targets don't exist in the index. Includes frontmatter `related` lists. |
| `freshness.py` | Compare index mtimes and schema versions against the source. Exit 0 if fresh, 1 if drift. Used by host's lint pipeline. |
| `generate_index.py` | Render an `index.md` from frontmatter — a derived overview of every page in a scope, grouped by domain. |

## When to reach for which command

Use these triggers to choose the right tool:

| User signal | Command | Why |
|---|---|---|
| "What did I say about X?" / "Find information on Y" | `search.py --query "..."` | Cheap retrieval, top-k snippets with metadata |
| "Everything about [domain]" / domain-bounded question | `search.py --domain ... --query "..."` | Tighter scope, higher precision |
| "What links to page X?" / "What does X point to?" | `links.py --page "..."` | Backlinks + outgoing graph traversal |
| "Which links are broken?" / `lint wiki` work | `broken.py --pretty` | List wiki-links that don't resolve. External file refs (`.pdf`, `.xlsx`, etc) are filtered out automatically |
| "Is the index current?" / lint pass | `freshness.py --pretty` | Drift detection — mtime drift *and* schema-version drift |
| Wiki was just edited and you need to query right after | (no command) | Search auto-reindexes on stale or version-mismatched indexes — just query |
| User installed v1 of the skill and upgraded the code | (no command) | First query after upgrade triggers transparent rebuild — no manual migration |

**Don't reach for `Read` on a wiki file when you could `search`.** The cost asymmetry is ~20x. Even partial-match queries usually return enough.

**Don't reach for `reindex.py` manually unless freshness reports drift that auto-reindex won't fix.** Reindex is idempotent but unnecessary when the freshness check already triggers it.

## Wiki-link extraction (v2)

Wiki-links in the body are extracted as structured records:

```json
{
  "target": "page-name",
  "heading": "Section A",
  "alias": "display name",
  "raw": "[[page-name#Section A|display name]]"
}
```

`target` is lowercased and trimmed; `heading` and `alias` preserve original casing.

The extractor masks code spans before scanning, so `[[link]]` inside fenced code (` ``` `, `~~~`), inline code (`` ` ``), HTML comments (`<!-- ... -->`), and indented code blocks is ignored. Escaped `\[[...]]` is also skipped.

**Relative paths supported.** Obsidian-style links like `[[../folder/page]]` and `[[./page]]` resolve the same as plain forms (`[[folder/page]]`, `[[page]]`). Both `find_page` and `backlinks` strip leading `../` and `./` segments before matching.

Frontmatter `related: [[A]], [[B]]` lists remain in `metadata.related` as a string list — they're not folded into `wiki_links`.

## Schema versioning

Each index carries `index_version: 2`. When `search.py` or `freshness.py` reads an index without the field (or with a lower version), the index is rebuilt transparently before serving the request. Users never run a manual migration command.

## Frontmatter the skill consumes

These fields actively shape search results, graph navigation, and filtering. Pages that carry them rank higher and link more usefully. Other frontmatter fields are preserved in the index and shown alongside results, but only the ones below influence the skill's behavior directly.

| Field | Used by | Why it matters |
|---|---|---|
| `title` | All | Display name. Falls back to first H1 if absent. |
| `summary` | `search.py`, `generate_index.py` | Shown in every search result. Often the answer on its own. |
| `keywords` | `search.py` | Boosts recall when the body uses different vocabulary than the query. |
| `aliases` | `links.py`, `broken.py` | Names the page can be referenced by from `[[wiki-links]]`. Critical for graph resolution — Obsidian uses the same field for the same purpose, so this comes free. |
| `related` | `links.py`, `broken.py`, `generate_index.py` | Curated outgoing links beyond the body's `[[wiki-links]]`. Treated as graph edges. |
| `domain` | `search.py --domain`, `generate_index.py` | Enables domain-scoped search and grouping in derived index views. |
| `updated` | `generate_index.py` | Surfaces page age in derived views; supports staleness-tracking when you wire it into your lint pipeline. |

The parser accepts a few common English synonyms (`description` for `summary`, `category` for `domain`, `modified` for `updated`). See `index.py` and `generate_index.py` for the full list. **Pick one form and use it consistently** across the vault — mixed vocabulary makes the wiki harder to maintain, not the index.

When you create or edit a wiki page, prompt the user for these fields if they're missing — especially `aliases` and `summary`, which produce the largest improvement in retrieval quality.

## How to integrate with a host harness

Three couplings make the skill function as designed:

**Ingest coupling.** Add `python3 scripts/reindex.py` as the final step of any ingest command that writes to the wiki.

**Lint coupling.** Add `python3 scripts/freshness.py` to the host's lint pipeline. Exit code 1 means drift — either report it or auto-fix by running `reindex.py`.

**Search routing.** Tell the host agent (via its command file or skill instructions) to prefer `python3 scripts/search.py --query "..."` over `Read` on wiki files. The cost asymmetry makes this nearly always correct.

## Trade-offs

**TF-IDF is keyword-based.** A query for "compliance" will not match a wiki that uses "regulation". The augmentation rewards consistent vocabulary in the source. Consider it a feature: it makes you write more carefully.

**Indexes are rebuilt from scratch.** Not incremental. For wikis up to a few thousand pages this is fine — full reindex completes in a couple of seconds. For larger wikis, incremental indexing would need to be added.

**JSON indexes are not for humans.** They are fuel for `search.py`. Do not open them in a markdown editor.

## What this is not

This skill is a retrieval layer for *already-curated* knowledge. If the wiki is unstructured — no frontmatter, inconsistent terminology, no manual organization — the augmentation will not save you. The discipline of writing the wiki is what makes the cheap retrieval possible.

This skill is also not a knowledge graph extractor. If you have unfamiliar material (a codebase you didn't write, papers you haven't read), you need extraction tools, not retrieval tools. They are different problems.
