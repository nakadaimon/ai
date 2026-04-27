#!/usr/bin/env python3
"""
broken.py — list wiki-links whose target does not exist in the index.

Walks every page's `wiki_links`, resolves each target against the index
using the same matching rules as links.py, and reports those that don't
resolve. Frontmatter `related` lists are also checked.

Usage:
    python broken.py                       # all scopes
    python broken.py --scope my-vault
    python broken.py --pretty              # human-readable
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from links import find_page  # noqa: E402

DEFAULT_INDEX_DIR = Path(__file__).resolve().parent.parent / "indexes"

# Suffixes that indicate the link points to a raw file, not a wiki page.
# Such links are *external references* (e.g. into a vault's `raw/` mirror)
# and are not considered broken even if no markdown page resolves them.
_EXTERNAL_FILE_SUFFIXES = {
    ".pdf", ".xlsx", ".xls", ".docx", ".doc", ".pptx", ".ppt",
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
    ".csv", ".tsv", ".json", ".yaml", ".yml",
    ".zip", ".tar", ".gz",
    ".mp3", ".mp4", ".wav", ".mov",
}


def _is_external_file_link(target: str) -> bool:
    """True if `target` looks like a path to a non-markdown file (raw/-mirror,
    binary asset, etc)."""
    if not target:
        return False
    suffix = Path(target).suffix.lower()
    return suffix in _EXTERNAL_FILE_SUFFIXES


def find_broken(index: dict) -> list[dict]:
    """Return all wiki-links and frontmatter related-entries that don't resolve.

    External file references (links to .pdf, .xlsx, etc — typically into a
    vault's `raw/` mirror) are skipped. They're not broken wiki-links;
    they're intentional references to source documents on disk.
    """
    broken: list[dict] = []
    for page in index["pages"]:
        for link in page.get("wiki_links", []):
            # v2: dict; v1 fallback: string
            if isinstance(link, dict):
                target = link["target"]
                raw = link["raw"]
                heading = link.get("heading")
                alias = link.get("alias")
            else:
                target = link
                raw = f"[[{link}]]"
                heading = None
                alias = None

            if _is_external_file_link(target):
                continue

            if find_page(index, target) is None:
                broken.append({
                    "from_file": page["id"],
                    "from_title": page["title"],
                    "from_breadcrumb": page.get("breadcrumb", page["title"]),
                    "normalized_target": target,
                    "heading": heading,
                    "alias": alias,
                    "raw": raw,
                    "via": "body",
                })

        # Frontmatter related (still list[str] in v2)
        related = page.get("metadata", {}).get("related") or []
        if isinstance(related, str):
            related = [related]
        for r in related:
            if _is_external_file_link(str(r)):
                continue
            if find_page(index, r) is None:
                broken.append({
                    "from_file": page["id"],
                    "from_title": page["title"],
                    "from_breadcrumb": page.get("breadcrumb", page["title"]),
                    "normalized_target": str(r).lower().strip(),
                    "heading": None,
                    "alias": None,
                    "raw": str(r),
                    "via": "frontmatter.related",
                })
    return broken


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", type=str, default="all",
                        help="scope to check, or 'all' (default)")
    parser.add_argument("--index-dir", type=Path, default=DEFAULT_INDEX_DIR)
    parser.add_argument("--pretty", action="store_true",
                        help="human-readable output instead of JSON")
    args = parser.parse_args()

    index_dir = args.index_dir.expanduser()

    if args.scope == "all":
        scopes = sorted(p.stem for p in index_dir.glob("*.json"))
    else:
        scopes = [args.scope]

    results: dict = {"scopes": {}, "total": 0}

    for scope in scopes:
        idx_path = index_dir / f"{scope}.json"
        if not idx_path.exists():
            results["scopes"][scope] = {"error": f"index not found: {idx_path}"}
            continue
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        broken = find_broken(idx)
        results["scopes"][scope] = {
            "broken_links": broken,
            "total": len(broken),
        }
        results["total"] += len(broken)

    if args.pretty:
        print(f"\nbroken-links report — {results['total']} total")
        for scope, r in results["scopes"].items():
            if "error" in r:
                print(f"\n  {scope}: ERROR — {r['error']}")
                continue
            print(f"\n  [{scope}] {r['total']} broken")
            for b in r["broken_links"]:
                detail = b["normalized_target"]
                if b["heading"]:
                    detail += f"#{b['heading']}"
                if b["alias"]:
                    detail += f" (alias: {b['alias']})"
                print(f"      {b['from_breadcrumb']} → {detail}  [{b['via']}]")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))

    return 0 if results["total"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
