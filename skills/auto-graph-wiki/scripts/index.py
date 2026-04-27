#!/usr/bin/env python3
"""
index.py — build a TF-IDF search index over an LLM-wiki.

Parses:
  - YAML frontmatter (all fields preserved as metadata)
  - Section-based chunks (heading-delimited)
  - Wiki-links [[Other Note]] and [[path/to/note|alias]]
  - Tags #tag

Produces a JSON index that search.py and links.py can query.
No LLM, no network, fully deterministic.

Usage:
    python index.py --vault path/to/wiki --scope llm-wiki --out indexes/llm-wiki.json
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

# --- Tokenizer (handles common Latin scripts including Nordic letters) -----

INDEX_VERSION = 2

WORD_RE = re.compile(r"[A-Za-zÅÄÖåäöÆØæøÉéÜü][A-Za-zÅÄÖåäöÆØæøÉéÜü0-9_-]+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
# Wiki-link regex with three capture groups:
#   group 1 = target (required)
#   group 2 = heading (optional, after #)
#   group 3 = alias   (optional, after |)
WIKI_LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]")
TAG_RE = re.compile(r"(?:^|\s)#([A-Za-z][A-Za-z0-9_/-]*)")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Minimal stopword list — extend in your own copy if you need locale-specific tuning
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are", "was",
    "were", "been", "have", "has", "had", "but", "not", "can", "will",
    "all", "one", "two", "any", "you", "we", "they", "them", "their",
    "is", "of", "to", "in", "on", "at", "by", "as", "an", "or", "if",
}


def tokenize(text: str) -> list[str]:
    return [
        t.lower()
        for t in WORD_RE.findall(text)
        if t.lower() not in STOPWORDS and len(t) > 1
    ]


# --- Frontmatter parser (minimal YAML, no external deps) ------------------

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Return (frontmatter_dict, body_text). Empty dict if no frontmatter."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    yaml_block = m.group(1)
    body = text[m.end():]
    fm = parse_simple_yaml(yaml_block)
    return fm, body


def parse_simple_yaml(yaml_text: str) -> dict[str, Any]:
    """Handles the common cases:
       - key: value
       - key: [a, b, c]
       - key:
           - a
           - b
       Plus Obsidian-style wiki-link lists: 'related: [[A]], [[B]], [[C]]'
       Skips PyYAML dependency to keep the skill standalone."""
    out: dict[str, Any] = {}
    lines = yaml_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest == "":
            # Multi-line list or block
            items: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].startswith("- ") or lines[i].startswith("\t")):
                v = lines[i].strip()
                if v.startswith("- "):
                    items.append(_strip_quotes(v[2:].strip()))
                i += 1
            out[key] = items if items else ""
            continue
        # Obsidian: 'related: [[A]], [[B]]' — multiple wiki-links without YAML list syntax
        wiki_list = _maybe_parse_wiki_links(rest)
        if wiki_list is not None:
            out[key] = wiki_list
        elif rest.startswith("[") and rest.endswith("]") and not rest.startswith("[["):
            inner = rest[1:-1].strip()
            if not inner:
                out[key] = []
            else:
                out[key] = [_strip_quotes(x.strip()) for x in inner.split(",")]
        else:
            out[key] = _strip_quotes(rest)
        i += 1
    return out


def _extract_wiki_target(s: str) -> str | None:
    """If `s` is exactly '[[target]]' or '[[target#h|alias]]', return the target name."""
    m = WIKI_LINK_RE.fullmatch(s.strip())
    return m.group(1).strip() if m else None


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    target = _extract_wiki_target(s)
    if target is not None:
        return target
    return s


def _maybe_parse_wiki_links(s: str) -> list[str] | None:
    """If the string looks like '[[A]], [[B]], [[C]]', return ['A','B','C']."""
    targets = [m.group(1).strip() for m in WIKI_LINK_RE.finditer(s)]
    if not targets:
        return None
    rest = WIKI_LINK_RE.sub("", s)
    rest_clean = re.sub(r"[\s,;]+", "", rest)
    if rest_clean:
        return None
    return targets


# --- Code/comment masking (preserves positions) ----------------------------

# Order matters: inline code first, otherwise fenced regex would greedily
# match across `~~~` or ``` characters that appear inside inline spans.
_CODE_AND_COMMENT_PATTERNS = [
    re.compile(r"`[^`\n]+`"),                           # 1. inline code (single line)
    re.compile(r"<!--.*?-->", re.DOTALL),               # 2. HTML comments
    re.compile(r"```.*?```", re.DOTALL),                # 3. fenced backticks
    re.compile(r"~~~.*?~~~", re.DOTALL),                # 4. fenced tildes
    re.compile(r"^(?: {4,}|\t).*$", re.MULTILINE),      # 5. indented code
]


def mask_code_and_comments(body: str) -> str:
    """Replace code spans and HTML comments with whitespace of equal length,
    preserving offsets so downstream regex positions remain stable."""
    masked = body
    for pattern in _CODE_AND_COMMENT_PATTERNS:
        masked = pattern.sub(lambda m: " " * (m.end() - m.start()), masked)
    return masked


def extract_wiki_links(body: str) -> list[dict]:
    """Extract structured wiki-links from body, masking code blocks first.

    Returns a list of dicts with target/heading/alias/raw. Targets are
    lowercased and trimmed; heading and alias preserve original casing.
    Escaped '\\[[...]]' is skipped. Duplicates (same target+heading+alias)
    are dropped while preserving first-occurrence order.
    """
    masked = mask_code_and_comments(body)
    out: list[dict] = []
    seen: set[tuple[str, str | None, str | None]] = set()
    for m in WIKI_LINK_RE.finditer(masked):
        if m.start() > 0 and body[m.start() - 1] == "\\":
            continue
        target = m.group(1).strip().lower()
        heading = m.group(2).strip() if m.group(2) else None
        alias = m.group(3).strip() if m.group(3) else None
        key = (target, heading, alias)
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "target": target,
            "heading": heading,
            "alias": alias,
            "raw": m.group(0),
        })
    return out


# --- Chunking --------------------------------------------------------------

def chunk_by_headings(body: str, max_chars: int = 1000) -> list[dict]:
    chunks: list[dict] = []
    matches = list(HEADING_RE.finditer(body))
    if not matches:
        text = body.strip()
        if text:
            chunks.append({"heading": "", "text": text[:max_chars]})
        return chunks

    if matches[0].start() > 0:
        pre = body[: matches[0].start()].strip()
        if pre:
            chunks.append({"heading": "", "text": pre[:max_chars]})

    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        text = body[start:end].strip()
        if text:
            chunks.append({"heading": m.group(2).strip(), "text": text[:max_chars]})
    return chunks


# --- Indexing --------------------------------------------------------------

def index_vault(vault: Path, scope: str) -> dict[str, Any]:
    """Index every .md file in a vault, skipping hidden folders and node_modules."""
    md_files = [
        p for p in vault.rglob("*.md")
        if not any(part.startswith(".") or part in {".obsidian", ".trash", "node_modules"}
                   for part in p.relative_to(vault).parts)
    ]

    print(f"  found {len(md_files)} markdown files in {vault}", file=sys.stderr)

    pages: list[dict[str, Any]] = []

    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        rel = str(f.relative_to(vault))
        page_id = rel.replace("\\", "/")
        frontmatter, body = parse_frontmatter(text)

        h1 = HEADING_RE.search(body)
        title = h1.group(2).strip() if (h1 and h1.group(1) == "#") else f.stem

        # Path information for breadcrumb and disambiguation
        rel_path = Path(page_id)
        path_parts = list(rel_path.parts[:-1])
        path_no_ext = page_id[:-3] if page_id.endswith(".md") else page_id
        crumb_parts = [p for p in path_parts if p != "pages"]
        breadcrumb = " › ".join(crumb_parts + [title]) if crumb_parts else title

        wiki_links = extract_wiki_links(body)
        tags = list(set(TAG_RE.findall(body)))
        chunks = chunk_by_headings(body)

        for c in chunks:
            heading_tokens = tokenize(c["heading"])
            text_tokens = tokenize(c["text"])
            # Heading counts twice — small relevance boost for headings that match
            chunk_tokens = heading_tokens + heading_tokens + text_tokens
            c["tf"] = dict(Counter(chunk_tokens))

        pages.append({
            "id": page_id,
            "scope": scope,
            "title": title,
            "path_parts": path_parts,
            "path_no_ext": path_no_ext,
            "breadcrumb": breadcrumb,
            "metadata": frontmatter,
            "chunks": chunks,
            "wiki_links": wiki_links,
            "tags": tags,
            "mtime": f.stat().st_mtime,
        })

    # IDF over chunks
    n_chunks = sum(len(p["chunks"]) for p in pages) or 1
    df: Counter[str] = Counter()
    for p in pages:
        for c in p["chunks"]:
            for tok in c["tf"]:
                df[tok] += 1
    idf = {t: math.log((n_chunks + 1) / (cnt + 1)) + 1 for t, cnt in df.items()}

    for p in pages:
        for c in p["chunks"]:
            tf = c["tf"]
            c["norm"] = math.sqrt(sum((tf[t] * idf.get(t, 0)) ** 2 for t in tf)) or 1.0

    return {
        "index_version": INDEX_VERSION,
        "scope": scope,
        "vault": str(vault),
        "indexed_at": datetime.now().isoformat(),
        "pages": pages,
        "idf": idf,
        "stats": {
            "page_count": len(pages),
            "chunk_count": n_chunks,
            "vocab_size": len(idf),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--scope", type=str, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    vault = args.vault.expanduser().resolve()
    out = args.out.expanduser()

    if not vault.is_dir():
        print(f"error: vault is not a directory: {vault}", file=sys.stderr)
        return 1

    print(f"indexing scope='{args.scope}' from {vault}", file=sys.stderr)
    index = index_vault(vault, scope=args.scope)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")

    s = index["stats"]
    print(f"  → {s['page_count']} pages, {s['chunk_count']} chunks, "
          f"{s['vocab_size']} unique tokens", file=sys.stderr)
    print(f"  written to {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
