#!/usr/bin/env python3
"""
generate_index.py — auto-generate an index.md from frontmatter.

Reads a scope's index (built by index.py) and produces a markdown file
with a table per top-level domain. The truth lives in frontmatter on each
page; index.md is a derived view.

Usage:
    python generate_index.py --scope llm-wiki --out index-auto.md
    python generate_index.py --scope llm-wiki --out path/to/index.md \\
                              --title "My Wiki — Index"
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

DEFAULT_INDEX_DIR = Path(__file__).resolve().parent.parent / "indexes"


def _first(md: dict, *keys) -> Any:
    for k in keys:
        if k in md and md[k]:
            return md[k]
    return None


def _to_list(v) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    return [str(v)]


def _to_csv(v) -> str:
    return ", ".join(_to_list(v))


def page_summary(page: dict) -> str:
    """Get summary from frontmatter. Fallback: first paragraph of body."""
    md = page.get("metadata", {})
    val = _first(md, "summary", "description")
    if val:
        return str(val)
    for c in page.get("chunks", []):
        text = c.get("text", "").strip()
        if not text or text.startswith(">"):
            continue
        first_line = text.split("\n")[0]
        if len(first_line) > 140:
            first_line = first_line[:137] + "…"
        return first_line + "  _(from body)_"
    return ""


def page_keywords(page: dict) -> str:
    md = page.get("metadata", {})
    kw = _first(md, "keywords")
    if kw is None:
        kw = page.get("tags", [])
    return _to_csv(kw)


def page_aliases(page: dict) -> str:
    md = page.get("metadata", {})
    return _to_csv(_first(md, "aliases", "alias"))


def page_related(page: dict) -> str:
    md = page.get("metadata", {})
    val = _first(md, "related", "see_also")
    if val:
        return _to_csv(val)
    links = page.get("wiki_links", [])
    if not links:
        return ""
    # v2: wiki_links is list[dict]; v1 fallback: list[str]
    targets = [(l["target"] if isinstance(l, dict) else l) for l in links[:5]]
    short = [t.split("/")[-1].split("|")[0].strip() for t in targets]
    return ", ".join(short)


def page_updated(page: dict) -> str:
    md = page.get("metadata", {})
    val = _first(md, "updated", "modified")
    return str(val) if val else ""


def page_domain_full(page: dict) -> str:
    md = page.get("metadata", {})
    return _first(md, "domain", "category") or ""


def page_domain_top(page: dict) -> str:
    full = page_domain_full(page)
    return full.split("/", 1)[0] if full else ""


def page_basename(page: dict) -> str:
    return Path(page["id"]).stem


def _updated_to_sortable(s: str) -> int:
    if not s:
        return 0
    try:
        return int(s.replace("-", "")[:8])
    except ValueError:
        return 0


def find_overview_description(domain: str, pages: list[dict]) -> str:
    for p in pages:
        if page_basename(p) == domain:
            md = p.get("metadata", {})
            return _first(md, "description", "summary") or ""
    return ""


def render_table(pages: list[dict]) -> list[str]:
    if not pages:
        return ["| _No pages yet_ | | | | | |"]

    pages = sorted(pages, key=lambda p: (
        page_domain_full(p).count("/"),
        -_updated_to_sortable(page_updated(p)),
        page_basename(p),
    ))

    lines = []
    for p in pages:
        link = f"[{page_basename(p)}]({p['id']})"
        cells = [
            link,
            page_summary(p).replace("|", "\\|").replace("\n", " "),
            page_keywords(p).replace("|", "\\|"),
            page_aliases(p).replace("|", "\\|"),
            page_related(p).replace("|", "\\|"),
            page_updated(p),
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def render_index(index: dict, title: str, intro: str | None) -> str:
    pages_by_domain: dict[str, list[dict]] = defaultdict(list)
    for p in index["pages"]:
        if p["id"].startswith("raw/"):
            continue
        basename = page_basename(p)
        if basename in {"schema", "log", "index"} and "/" not in p["id"]:
            continue
        top = page_domain_top(p) or "(uncategorized)"
        pages_by_domain[top].append(p)

    out: list[str] = []
    out.append(f"# {title}")
    out.append("")
    if intro:
        for line in intro.split("\n"):
            out.append(f"> {line}" if line.strip() else ">")
        out.append("")
    out.append("> *Auto-generated from frontmatter. Truth lives on each page — do not edit here.*")
    out.append("")
    out.append("---")
    out.append("")

    for domain in sorted(pages_by_domain.keys()):
        pages = pages_by_domain[domain]
        intro_text = find_overview_description(domain, pages)

        out.append(f"## {domain}")
        if intro_text:
            out.append(f"_{intro_text}_")
        out.append("")
        out.append("| Page | Summary | Keywords | Aliases | Related | Updated |")
        out.append("|------|---------|----------|---------|---------|---------|")
        out.extend(render_table(pages))
        out.append("")

    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", type=str, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--title", type=str, default=None)
    parser.add_argument("--intro", type=str, default=None)
    parser.add_argument("--index-dir", type=Path, default=DEFAULT_INDEX_DIR)
    args = parser.parse_args()

    index_path = args.index_dir / f"{args.scope}.json"
    if not index_path.exists():
        print(f"error: index for '{args.scope}' not found: {index_path}\n"
              f"run python scripts/reindex.py first.", file=sys.stderr)
        return 1

    index = json.loads(index_path.read_text(encoding="utf-8"))
    title = args.title or f"{args.scope} — Index"

    md = render_index(index, title=title, intro=args.intro)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(md, encoding="utf-8")

    print(f"generated index for '{args.scope}': {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
