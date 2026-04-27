"""Edge-case tests for wiki-link extraction (v2).

Tests cover:
  - Code blocks (fenced backticks, fenced tildes, indented) — links inside masked
  - Inline code — links inside masked
  - HTML comments — links inside masked
  - Escaped brackets — not extracted
  - Heading + alias preserved per link
  - Unicode targets and aliases
  - Frontmatter related list — separate from wiki_links
  - Index version stamped

Run from skill root:
    python -m pytest tests/ -v
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from index import index_vault  # noqa: E402

VAULT = Path(__file__).resolve().parent.parent / "examples" / "edge-cases"


# --- helpers ---------------------------------------------------------------

def _index():
    return index_vault(VAULT, scope="edge-cases")


def _page(idx, filename: str):
    for p in idx["pages"]:
        if p["id"] == filename or p["id"].endswith("/" + filename):
            return p
    raise AssertionError(f"page '{filename}' not in index. Available: {[p['id'] for p in idx['pages']]}")


def _targets(page) -> set[str]:
    return {link["target"] for link in page["wiki_links"]}


# --- tests -----------------------------------------------------------------

def test_index_version_stamped():
    idx = _index()
    assert idx.get("index_version") == 2, f"expected index_version=2, got {idx.get('index_version')}"


def test_wiki_links_are_dicts():
    idx = _index()
    page = _page(idx, "alias-heavy.md")
    assert page["wiki_links"], "expected wiki_links to be non-empty"
    for link in page["wiki_links"]:
        assert isinstance(link, dict), f"expected dict, got {type(link).__name__}: {link}"
        assert "target" in link
        assert "heading" in link
        assert "alias" in link
        assert "raw" in link


def test_code_heavy_excludes_fenced_and_inline_code():
    idx = _index()
    page = _page(idx, "code-heavy.md")
    assert _targets(page) == {"real-target", "real-target-two"}, \
        f"expected only real targets, got {_targets(page)}"


def test_tilde_fences_excluded():
    idx = _index()
    page = _page(idx, "tilde-fences.md")
    assert _targets(page) == {"real-tilde-target", "real-after-tilde"}, \
        f"got {_targets(page)}"


def test_indented_code_excluded_but_lists_kept():
    idx = _index()
    page = _page(idx, "indented-code.md")
    assert _targets(page) == {
        "real-indented-target",
        "real-list-link",
        "another-real-list-link",
        "real-after-indent",
    }, f"got {_targets(page)}"


def test_html_comments_excluded():
    idx = _index()
    page = _page(idx, "html-comments.md")
    assert _targets(page) == {"real-comment-target", "real-after-comment"}, \
        f"got {_targets(page)}"


def test_escaped_brackets_excluded():
    idx = _index()
    page = _page(idx, "escaped.md")
    assert _targets(page) == {"real-escaped-target", "real-after-escape"}, \
        f"got {_targets(page)}"


def test_alias_preserved_per_link():
    idx = _index()
    page = _page(idx, "alias-heavy.md")
    aliases_by_target = {}
    for link in page["wiki_links"]:
        aliases_by_target.setdefault(link["target"], []).append(link["alias"])
    assert "first display name" in aliases_by_target.get("target-one", [])
    assert "different alias for same target" in aliases_by_target.get("target-one", [])
    assert aliases_by_target.get("target-two") == ["second display"]
    assert aliases_by_target.get("plain-target") == [None]


def test_heading_preserved_per_link():
    idx = _index()
    page = _page(idx, "heading-heavy.md")
    headings_by_target = {}
    for link in page["wiki_links"]:
        headings_by_target.setdefault(link["target"], []).append(link["heading"])
    assert "section-a" in headings_by_target.get("target-doc", [])
    assert "section-b" in headings_by_target.get("target-doc", [])
    assert "deep nested heading with spaces" in headings_by_target.get("target-doc", [])
    assert headings_by_target.get("plain-target") == [None]


def test_combined_heading_and_alias():
    idx = _index()
    page = _page(idx, "combined.md")
    found = {(l["target"], l["heading"], l["alias"]) for l in page["wiki_links"]}
    assert ("target-doc", "section-a", "the first section") in found
    assert ("target-doc", "section-b", "second part") in found
    assert ("plain-target", None, None) in found
    assert ("target-doc", "section-c", None) in found
    assert ("target-doc", None, "just an alias") in found


def test_unicode_targets_and_aliases():
    idx = _index()
    page = _page(idx, "unicode.md")
    found = {(l["target"], l["alias"]) for l in page["wiki_links"]}
    assert ("größe-page", "Größe overview") in found
    assert ("résumé", "résumé") in found
    assert ("mañana", None) in found
    assert ("café", "café au lait") in found
    assert ("日本語-page", "Japanese reference") in found


def test_frontmatter_related_in_metadata_not_wiki_links():
    idx = _index()
    page = _page(idx, "frontmatter-related.md")
    related = page["metadata"].get("related", [])
    assert "A" in related
    assert "B" in related
    assert "C" in related
    # body link is in wiki_links (not in metadata.related)
    assert _targets(page) == {"body-target"}


def test_raw_field_preserves_original():
    idx = _index()
    page = _page(idx, "combined.md")
    raws = {l["raw"] for l in page["wiki_links"]}
    assert "[[target-doc#section-a|the first section]]" in raws
    assert "[[plain-target]]" in raws


def test_target_normalized_lowercase():
    idx = _index()
    # All targets in our test files are already lowercase, so we test
    # that normalization is consistent (no surprise capitalization).
    for page in idx["pages"]:
        for link in page["wiki_links"]:
            assert link["target"] == link["target"].lower(), \
                f"target not normalized: {link['target']}"


def test_find_page_resolves_relative_paths():
    """Obsidian-style [[../foo/bar]] should resolve like [[foo/bar]]."""
    from links import find_page  # noqa: E402

    fake_index = {
        "pages": [
            {
                "id": "pages/folder-a/page-one.md",
                "title": "Page One",
                "path_no_ext": "pages/folder-a/page-one",
                "metadata": {},
            },
            {
                "id": "pages/folder-b/subfolder/page-two.md",
                "title": "Page Two",
                "path_no_ext": "pages/folder-b/subfolder/page-two",
                "metadata": {},
            },
        ]
    }

    # Various relative-path forms should all resolve to page-one
    for query in [
        "../folder-a/page-one",
        "../../folder-a/page-one",
        "./folder-a/page-one",
        "folder-a/page-one",  # plain form should still work
    ]:
        result = find_page(fake_index, query)
        assert result is not None, f"failed to resolve: {query}"
        assert result["title"] == "Page One", f"wrong page for {query}: {result['title']}"

    # Deep relative path
    result = find_page(fake_index, "../../folder-b/subfolder/page-two")
    assert result is not None
    assert result["title"] == "Page Two"


def test_backlinks_resolve_relative_paths():
    """backlinks() must also normalize relative-path targets, otherwise
    Obsidian-style [[../foo]] links don't show up as backlinks."""
    from links import backlinks  # noqa: E402

    fake_index = {
        "pages": [
            {
                "id": "pages/folder-a/page-one.md",
                "title": "Page One",
                "path_no_ext": "pages/folder-a/page-one",
                "breadcrumb": "folder-a › Page One",
                "metadata": {},
                "wiki_links": [],
            },
            {
                "id": "pages/folder-b/page-two.md",
                "title": "Page Two",
                "path_no_ext": "pages/folder-b/page-two",
                "breadcrumb": "folder-b › Page Two",
                "metadata": {},
                "wiki_links": [
                    {
                        "target": "../folder-a/page-one",
                        "heading": None,
                        "alias": "page one",
                        "raw": "[[../folder-a/page-one|page one]]",
                    }
                ],
            },
        ]
    }

    target_page = fake_index["pages"][0]
    bl = backlinks(fake_index, target_page)
    assert len(bl) == 1, f"expected 1 backlink, got {len(bl)}: {bl}"
    assert bl[0]["from_file"] == "pages/folder-b/page-two.md"
