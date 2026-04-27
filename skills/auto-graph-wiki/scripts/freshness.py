#!/usr/bin/env python3
"""
freshness.py — verify that every scope's index is newer than its source files.

Implements the rule "derived artifacts follow their source". For each scope,
compares index mtime to the most recent wiki file mtime. If any wiki file is
newer than the index, the index has drifted and a reindex is needed.

Exit code:
  0 — all indexes fresh
  1 — drift detected in one or more scopes

Output is JSON by default, or human-readable with --pretty.

Usage:
    python freshness.py
    python freshness.py --pretty
    python freshness.py --auto-fix    # run reindex if drift detected
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "llm_wiki_paths.json"

# Keep in sync with INDEX_VERSION in index.py.
INDEX_VERSION = 2


def resolve_path(p: str, config_dir: Path) -> Path:
    if p.startswith("~"):
        return Path(p).expanduser()
    path = Path(p)
    if not path.is_absolute():
        path = (config_dir / path).resolve()
    return path


def newest_mtime(folder: Path, pattern: str = "*.md") -> tuple[float, Path | None]:
    """Find the newest mtime among matching files in folder, recursively."""
    newest = 0.0
    newest_file: Path | None = None
    for f in folder.rglob(pattern):
        if not f.is_file():
            continue
        if any(part.startswith(".") for part in f.relative_to(folder).parts):
            continue
        mt = f.stat().st_mtime
        if mt > newest:
            newest = mt
            newest_file = f
    return newest, newest_file


def check(config_path: Path) -> dict:
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    config_dir = config_path.resolve().parent
    index_dir = resolve_path(cfg.get("index_dir", "./indexes"), config_dir)

    out: dict = {"fresh": True, "scopes": {}}

    for scope, conf in cfg["scopes"].items():
        vault = resolve_path(conf["vault"], config_dir)
        index_path = index_dir / f"{scope}.json"
        result: dict = {"fresh": False}

        if not index_path.exists():
            result["error"] = "index missing — run reindex.py"
            out["fresh"] = False
            out["scopes"][scope] = result
            continue

        if not vault.is_dir():
            result["error"] = f"vault not found: {vault}"
            out["fresh"] = False
            out["scopes"][scope] = result
            continue

        # Schema-version check — drift here means the index was written by
        # an older index.py and must be rebuilt regardless of mtime.
        try:
            idx_version = json.loads(index_path.read_text(encoding="utf-8")).get("index_version", 1)
        except (json.JSONDecodeError, OSError):
            idx_version = 0
        result["index_version"] = idx_version
        if idx_version < INDEX_VERSION:
            result["fresh"] = False
            result["message"] = (
                f"schema version {idx_version} < {INDEX_VERSION} — run reindex"
            )
            out["fresh"] = False
            out["scopes"][scope] = result
            continue

        index_mtime = index_path.stat().st_mtime
        source_mtime, source_file = newest_mtime(vault)

        result["index_mtime"] = round(index_mtime, 2)
        result["newest_source_mtime"] = round(source_mtime, 2)
        if source_file:
            result["newest_source_file"] = str(source_file.relative_to(vault))

        drift = source_mtime - index_mtime
        result["drift_seconds"] = round(drift, 2)

        if drift > 0:
            result["fresh"] = False
            result["message"] = f"index is {drift:.0f}s older than newest wiki file — run reindex"
            out["fresh"] = False
        else:
            result["fresh"] = True
            result["message"] = "index is fresh"

        out["scopes"][scope] = result

    return out


def auto_fix() -> int:
    """Run reindex.py to refresh stale indexes."""
    reindex = Path(__file__).parent / "reindex.py"
    print("auto-fix: running reindex.py", file=sys.stderr)
    return subprocess.call([sys.executable, str(reindex)])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--pretty", action="store_true",
                        help="Human-readable output instead of JSON")
    parser.add_argument("--auto-fix", action="store_true",
                        help="Run reindex if drift is detected")
    args = parser.parse_args()

    out = check(args.config)

    if args.pretty:
        print(f"\n{'✓' if out['fresh'] else '✗'} freshness check {'PASS' if out['fresh'] else 'FAIL'}")
        for scope, r in out["scopes"].items():
            mark = "✓" if r.get("fresh") else "✗"
            print(f"\n  {mark} {scope}")
            if "error" in r:
                print(f"      ERROR: {r['error']}")
                continue
            idx_dt = datetime.fromtimestamp(r["index_mtime"]).isoformat(timespec="seconds")
            src_dt = datetime.fromtimestamp(r["newest_source_mtime"]).isoformat(timespec="seconds")
            print(f"      index:    {idx_dt}")
            print(f"      newest:   {src_dt}  ({r.get('newest_source_file', '?')})")
            print(f"      {r['message']}")
    else:
        print(json.dumps(out, ensure_ascii=False, indent=2))

    if not out["fresh"] and args.auto_fix:
        rc = auto_fix()
        if rc == 0:
            print("\n✓ auto-fix succeeded — index is now fresh", file=sys.stderr)
            return 0
        print("\n✗ auto-fix failed", file=sys.stderr)
        return rc

    return 0 if out["fresh"] else 1


if __name__ == "__main__":
    sys.exit(main())
