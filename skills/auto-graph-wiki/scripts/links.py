#!/usr/bin/env python3
"""
links.py — traverse the wiki-link graph (no LLM).

Given a page (title, path, or alias), show what links to it (backlinks)
and what it links to (outgoing).

Usage:
    python links.py --page "Page Title"
    python links.py --page "folder/sub/page-slug"
    python links.py --page "alias-from-frontmatter"
    python links.py --page "..." --scope llm-wiki
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_INDEX_DIR = Path(__file__).resolve().parent.parent / "indexes"


def _strip_relative_prefix(s: str) -> str:
    """Strip leading '../' and './' segments. Obsidian-style relative-path
    links should resolve the same as plain paths."""
    while s.startswith("../"):
        s = s[3:]
    while s.startswith("./"):
        s = s[2:]
    return s


def find_page(index: dict, query: str) -> dict | None:
    """Match a page on title, path, basename, or alias.

    Tries in order of specificity:
      1. Exact title
      2. Exact path (with or without `pages/` prefix, with or without .md)
      3. Path-suffix match (Obsidian-style short links)
      4. Alias from frontmatter
      5. Filename basename
      6. Substring fallback
    """
    q = query.lower().strip()
    q_no_ext = q[:-3] if q.endswith(".md") else q
    q_no_ext = _strip_relative_prefix(q_no_ext)

    # Exact title
    for p in index["pages"]:
        if p["title"].lower() == q:
            return p

    # Exact path
    for p in index["pages"]:
        path = p.get("path_no_ext", p["id"].replace(".md", "")).lower()
        if path == q_no_ext:
            return p
        if path.startswith("pages/") and path[len("pages/"):] == q_no_ext:
            return p

    # Path suffix
    for p in index["pages"]:
        path = p.get("path_no_ext", p["id"].replace(".md", "")).lower()
        if path.endswith("/" + q_no_ext) or path.endswith(q_no_ext):
            return p

    # Alias
    for p in index["pages"]:
        aliases = p.get("metadata", {}).get("alias") or p.get("metadata", {}).get("aliases") or []
        if isinstance(aliases, str):
            aliases = [aliases]
        if any(a.lower() == q for a in aliases):
            return p

    # Basename
    for p in index["pages"]:
        path = p.get("path_no_ext", p["id"].replace(".md", "")).lower()
        if path.split("/")[-1] == q_no_ext:
            return p

    # Substring fallback
    for p in index["pages"]:
        if q in p["title"].lower() or q in p["id"].lower():
            return p

    return None


def backlinks(index: dict, page: dict) -> list[dict]:
    """Find pages that link TO this one. Path-aware: matches on title,
    all path variants, and aliases."""
    target_names: set[str] = {page["title"].lower()}
    aliases = page.get("metadata", {}).get("alias") or page.get("metadata", {}).get("aliases") or []
    if isinstance(aliases, str):
        aliases = [aliases]
    for a in aliases:
        target_names.add(a.lower())

    path = page.get("path_no_ext", page["id"].replace(".md", "")).lower()
    target_names.add(path)
    if path.startswith("pages/"):
        target_names.add(path[len("pages/"):])
    target_names.add(path.split("/")[-1])

    out = []
    for other in index["pages"]:
        if other["id"] == page["id"]:
            continue
        for link in other.get("wiki_links", []):
            # v2: link is a dict {target, heading, alias, raw}.
            # v1 fallback: link is a string.
            target = link["target"] if isinstance(link, dict) else link.lower()
            target = _strip_relative_prefix(target)
            if target in target_names:
                out.append({
                    "from_file": other["id"],
                    "from_title": other["title"],
                    "from_breadcrumb": other.get("breadcrumb", other["title"]),
                    "via_link": link,
                })
                break
    return out


def outgoing(index: dict, page: dict) -> list[dict]:
    """Find pages this page links to."""
    out = []
    for link in page.get("wiki_links", []):
        # v2: link is a dict; v1 fallback: link is a string.
        if isinstance(link, dict):
            query = link["target"]
            link_repr = link
        else:
            query = link
            link_repr = link
        target = find_page(index, query)
        out.append({
            "link": link_repr,
            "resolved_file": target["id"] if target else None,
            "resolved_title": target["title"] if target else None,
        })
    related = page.get("metadata", {}).get("related") or []
    if isinstance(related, str):
        related = [related]
    for r in related:
        target = find_page(index, r)
        out.append({
            "link": r,
            "via": "frontmatter.related",
            "resolved_file": target["id"] if target else None,
            "resolved_title": target["title"] if target else None,
        })
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", type=str, default="all")
    parser.add_argument("--page", type=str, required=True)
    parser.add_argument("--index-dir", type=Path, default=DEFAULT_INDEX_DIR)
    args = parser.parse_args()

    index_dir = args.index_dir.expanduser()

    if args.scope == "all":
        scopes = sorted(p.stem for p in index_dir.glob("*.json"))
    else:
        scopes = [args.scope]

    found_in = None
    page = None
    index = None
    for scope in scopes:
        idx_path = index_dir / f"{scope}.json"
        if not idx_path.exists():
            continue
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        p = find_page(idx, args.page)
        if p:
            found_in = scope
            page = p
            index = idx
            break

    if not page:
        print(json.dumps({
            "error": f"no page matches '{args.page}'",
            "searched_scopes": scopes,
        }, ensure_ascii=False, indent=2))
        return 2

    out = {
        "scope": found_in,
        "page": {
            "title": page["title"],
            "file": page["id"],
            "metadata": page.get("metadata", {}),
        },
        "backlinks": backlinks(index, page),
        "outgoing": outgoing(index, page),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
