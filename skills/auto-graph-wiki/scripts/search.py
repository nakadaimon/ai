#!/usr/bin/env python3
"""
search.py — cheap retrieval over an LLM-wiki.

Returns top-k results with metadata + snippet. Designed to be cheap in
tokens — what search returns is usually enough as an answer on its own.

Auto-reindexing: by default, search checks whether the index has drifted
from the source files before running. If it has, it triggers a rebuild
silently and runs against the fresh index. Disable with --no-auto-reindex.

Usage:
    python search.py --query "DORA compliance"
    python search.py --query "..." --scope llm-wiki
    python search.py --query "..." -k 3 --pretty
    python search.py --query "..." --domain customer-journey
    python search.py --domain customer-journey            # list pages in domain
    python search.py --list-domains
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "llm_wiki_paths.json"
DEFAULT_INDEX_DIR = Path(__file__).resolve().parent.parent / "indexes"

# Keep in sync with INDEX_VERSION in index.py. Hardcoded to keep search.py
# importable without sys.path tricks.
INDEX_VERSION = 2

WORD_RE = re.compile(r"[A-Za-zÅÄÖåäöÆØæøÉéÜü][A-Za-zÅÄÖåäöÆØæøÉéÜü0-9_-]+")
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are", "was",
    "is", "of", "to", "in", "on", "at", "by", "as", "an", "or", "if",
}


def tokenize(text: str) -> list[str]:
    return [
        t.lower()
        for t in WORD_RE.findall(text)
        if t.lower() not in STOPWORDS and len(t) > 1
    ]


# --- Auto-reindex (lazy freshness fix) ------------------------------------

def resolve_path(p: str, config_dir: Path) -> Path:
    if p.startswith("~"):
        return Path(p).expanduser()
    path = Path(p)
    if not path.is_absolute():
        path = (config_dir / path).resolve()
    return path


def index_is_stale(scope: str, index_dir: Path, config_path: Path) -> bool:
    """True if the index is missing, has a stale schema version, or any
    source file is newer than the index."""
    index_path = index_dir / f"{scope}.json"
    if not index_path.exists():
        return True
    # Schema-version check: rebuild if the index was written by an older
    # version of index.py (or if the field is missing entirely — pre-v2).
    try:
        idx = json.loads(index_path.read_text(encoding="utf-8"))
        if idx.get("index_version", 1) < INDEX_VERSION:
            return True
    except (json.JSONDecodeError, OSError):
        return True
    try:
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
        scope_conf = cfg["scopes"].get(scope)
        if not scope_conf:
            return False
        vault = resolve_path(scope_conf["vault"], config_path.resolve().parent)
        if not vault.is_dir():
            return False
        index_mtime = index_path.stat().st_mtime
        for f in vault.rglob("*.md"):
            if not f.is_file():
                continue
            if any(part.startswith(".") for part in f.relative_to(vault).parts):
                continue
            if f.stat().st_mtime > index_mtime:
                return True
        return False
    except (json.JSONDecodeError, KeyError, OSError):
        return False  # if we can't tell, don't try to fix


def trigger_reindex(config_path: Path) -> None:
    """Run reindex.py silently. Errors are reported to stderr."""
    reindex = Path(__file__).parent / "reindex.py"
    result = subprocess.run(
        [sys.executable, str(reindex), "--config", str(config_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"warning: auto-reindex failed: {result.stderr}", file=sys.stderr)
    else:
        print("(auto-reindex completed — index was stale)", file=sys.stderr)


# --- Search core ----------------------------------------------------------

def load_index(scope: str, index_dir: Path) -> dict | None:
    path = index_dir / f"{scope}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def page_domain(page: dict) -> str | None:
    md = page.get("metadata", {})
    for key in ("domain", "category"):
        if key in md and md[key]:
            return str(md[key])
    return None


def domain_matches(page_dom: str | None, filter_dom: str) -> bool:
    if not page_dom:
        return False
    return filter_dom.lower() in page_dom.lower()


def search_index(index: dict, query: str, k: int, domain: str | None = None) -> list[tuple]:
    idf = index["idf"]
    q_tokens = tokenize(query) if query else []

    if not q_tokens and domain:
        out = []
        for page in index["pages"]:
            if domain_matches(page_domain(page), domain):
                first_chunk = page["chunks"][0] if page["chunks"] else {"heading": "", "text": "", "tf": {}, "norm": 1.0}
                out.append((1.0, page, first_chunk))
        return out[:k]

    if not q_tokens:
        return []

    q_tf = Counter(q_tokens)
    q_vec = {t: q_tf[t] * idf.get(t, 0) for t in q_tf}
    q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0

    results = []
    for page in index["pages"]:
        if domain and not domain_matches(page_domain(page), domain):
            continue
        for c in page["chunks"]:
            score = 0.0
            tf = c["tf"]
            for t, qv in q_vec.items():
                if t in tf:
                    score += qv * (tf[t] * idf.get(t, 0))
            score /= (q_norm * c["norm"])
            if score > 0:
                results.append((score, page, c))

    results.sort(key=lambda x: -x[0])
    return results[:k]


def list_domains(indexes: dict[str, dict]) -> dict[str, list[dict]]:
    by_domain: dict[str, list[dict]] = {}
    for scope, index in indexes.items():
        for page in index["pages"]:
            dom = page_domain(page) or "(no domain)"
            by_domain.setdefault(dom, []).append({
                "title": page["title"],
                "file": page["id"],
                "breadcrumb": page.get("breadcrumb", page["title"]),
                "scope": scope,
            })
    return dict(sorted(
        by_domain.items(),
        key=lambda x: (x[0] == "(no domain)", x[0].lower()),
    ))


def to_result(score: float, page: dict, chunk: dict, scope: str) -> dict:
    md = page.get("metadata", {})

    def first(*keys):
        for k in keys:
            if k in md and md[k]:
                return md[k]
        return None

    summary = first("summary", "description")
    keywords = first("keywords", "tags") or page.get("tags", [])
    domain = first("domain", "category")
    aliases = first("aliases", "alias")
    related = first("related", "see_also")
    updated = first("updated", "modified")

    snippet_text = chunk["text"]
    if len(snippet_text) > 400:
        snippet_text = snippet_text[:400] + "…"

    out = {
        "scope": scope,
        "file": page["id"],
        "title": page["title"],
        "breadcrumb": page.get("breadcrumb", page["title"]),
        "score": round(score, 4),
        "snippet": {
            "heading": chunk["heading"],
            "text": snippet_text,
        },
    }
    meta_out = {}
    if domain: meta_out["domain"] = domain
    if summary: meta_out["summary"] = summary
    if keywords: meta_out["keywords"] = keywords
    if aliases: meta_out["aliases"] = aliases
    if related: meta_out["related"] = related
    if updated: meta_out["updated"] = updated
    if meta_out:
        out["metadata"] = meta_out
    return out


def pretty_print(results: list[dict]) -> None:
    if not results:
        print("(no matches)")
        return
    for i, r in enumerate(results, 1):
        crumb = r.get("breadcrumb", r["title"])
        print(f"\n[{i}] {crumb}  score={r['score']}  scope={r['scope']}")
        print(f"    📄 {r['file']}")
        md = r.get("metadata", {})
        if md.get("summary"):
            print(f"    summary: {md['summary']}")
        if md.get("keywords"):
            kw = md["keywords"]
            if isinstance(kw, list):
                kw = ", ".join(str(x) for x in kw)
            print(f"    keywords: {kw}")
        if md.get("related"):
            rel = md["related"]
            if isinstance(rel, list):
                rel = ", ".join(str(x) for x in rel)
            print(f"    related: {rel}")
        h = r["snippet"]["heading"]
        if h:
            print(f"    ## {h}")
        for line in r["snippet"]["text"].split("\n"):
            print(f"    {line}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", type=str, default="all",
                        help="scope name or 'all' (default: all)")
    parser.add_argument("--query", type=str, default=None)
    parser.add_argument("--domain", type=str, default=None,
                        help="filter to pages in a specific domain (case-insensitive substring)")
    parser.add_argument("--list-domains", action="store_true",
                        help="list all domains and their pages instead of searching")
    parser.add_argument("-k", type=int, default=5)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--index-dir", type=Path, default=DEFAULT_INDEX_DIR)
    parser.add_argument("--pretty", action="store_true",
                        help="human-readable output instead of JSON")
    parser.add_argument("--no-auto-reindex", action="store_true",
                        help="disable automatic reindex when drift is detected")
    args = parser.parse_args()

    index_dir = args.index_dir.expanduser()
    config_path = args.config.expanduser()

    scopes = []
    if args.scope == "all":
        scopes = sorted(p.stem for p in index_dir.glob("*.json"))
        # If no indexes exist yet and we have a config, try a first build
        if not scopes and config_path.exists() and not args.no_auto_reindex:
            print("(no indexes found — running reindex.py for first-time setup)", file=sys.stderr)
            trigger_reindex(config_path)
            scopes = sorted(p.stem for p in index_dir.glob("*.json"))
    else:
        scopes = [args.scope]

    if not scopes:
        print(f"error: no indexes found in {index_dir}", file=sys.stderr)
        return 1

    # Lazy freshness check before searching
    if not args.no_auto_reindex and config_path.exists():
        any_stale = any(index_is_stale(s, index_dir, config_path) for s in scopes)
        if any_stale:
            trigger_reindex(config_path)

    if args.list_domains:
        indexes = {s: load_index(s, index_dir) for s in scopes if load_index(s, index_dir)}
        domains = list_domains(indexes)
        if args.pretty:
            for dom, pages in domains.items():
                print(f"\n## {dom}  ({len(pages)} pages)")
                for p in pages:
                    print(f"  · {p['breadcrumb']}  ({p['scope']}: {p['file']})")
        else:
            print(json.dumps(domains, ensure_ascii=False, indent=2))
        return 0

    if not args.query and not args.domain:
        print("error: provide --query or --domain (or --list-domains)", file=sys.stderr)
        return 2

    all_hits: list[tuple[float, dict, dict, str]] = []
    for scope in scopes:
        index = load_index(scope, index_dir)
        if index is None:
            continue
        hits = search_index(index, args.query or "", k=args.k * 2, domain=args.domain)
        for score, page, chunk in hits:
            all_hits.append((score, page, chunk, scope))

    all_hits.sort(key=lambda x: -x[0])
    top = all_hits[: args.k]
    results = [to_result(s, p, c, sc) for s, p, c, sc in top]

    if args.pretty:
        pretty_print(results)
    else:
        print(json.dumps({"query": args.query, "results": results},
                         ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
