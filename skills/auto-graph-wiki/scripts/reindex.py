#!/usr/bin/env python3
"""
reindex.py — rebuild every scope listed in llm_wiki_paths.json.

Cheap to run — fully rebuilds in seconds for hundreds of pages.
Couple this to your ingest pipeline so the index never drifts.

Usage:
    python reindex.py
    python reindex.py --config path/to/llm_wiki_paths.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "llm_wiki_paths.json"


def resolve_path(p: str, config_dir: Path) -> Path:
    """Support absolute paths, ~/foo (home), and ./foo or ../foo (relative to config)."""
    if p.startswith("~"):
        return Path(p).expanduser()
    path = Path(p)
    if not path.is_absolute():
        path = (config_dir / path).resolve()
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    config_dir = args.config.resolve().parent

    index_dir = resolve_path(cfg.get("index_dir") or "./indexes", config_dir)
    index_dir.mkdir(parents=True, exist_ok=True)

    indexer = Path(__file__).parent / "index.py"
    failed: list[str] = []

    for scope, conf in cfg["scopes"].items():
        vault = resolve_path(conf["vault"], config_dir)
        out = index_dir / f"{scope}.json"
        print(f"\n[{scope}] {vault}")
        if not vault.is_dir():
            print(f"  SKIP — vault not found: {vault}", file=sys.stderr)
            failed.append(scope)
            continue
        rc = subprocess.call([
            sys.executable, str(indexer),
            "--vault", str(vault),
            "--scope", scope,
            "--out", str(out),
        ])
        if rc != 0:
            failed.append(scope)

    if failed:
        print(f"\nfailed scopes: {failed}", file=sys.stderr)
        return 1
    print("\nall scopes indexed ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
