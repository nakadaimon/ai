# Commands

> Triggers. Short verbs the user invokes to run specific operations. Without these, the memento layer goes stale.

## capture

Trigger: a phrase that's clearly a future task ("I should check X", "remind me about Y").

Append a line to `memento/prospective/tasks/inbox.md`. Unformatted — sorting happens via `ingest tasks`.

## ingest

Promote signal upward through the memento layer.

| Command | Flow | What happens |
|---|---|---|
| `ingest session` | sessions → lessons + tasks | Extract lessons from the current session; route open todos to the inbox. |
| `ingest lessons` | lessons → character / harness / wiki / skills | Synthesize each correction into the right layer. |
| `ingest tasks` | inbox → tasks | Sort inbox entries by state. Empty processed rows. |
| `ingest ideas` | drafts → published / harness / skills / wiki | Graduate a draft, fold it elsewhere, or keep iterating. |
| `ingest project` | project inbox → project raw / assets / pointer into CONTEXT, requirements, or a feature brief | Project mode only. For each file in `projects/{active}/inbox/`: propose destination (source file → `raw/`, finished resource → `assets/`, or an update to CONTEXT/requirements/feature brief), wait for confirmation, move. **Canonical rule:** project-relevant files are canonical in the project — if the same file also lives in `memento/semantic/llm-wiki/raw/...` under a project path, move the wiki copy to the project and update `sources:` references in affected wiki pages. |

## lint

Catch drift across the structure.

| Command | What's checked |
|---|---|
| `lint bootstrap` | Eager-load stack (`AGENTS.md` + `character/*` + `harness/*` + `memento/AGENTS.md`): cross-zone references, reading order, broken paths, contradictory rules. |
| `lint wiki` | Missing pages, missing list entries, broken cross-references, stale `Updated` dates. |
| `lint skills` | TOC drift, version drift, overlap between skills. |
| `lint subtraction` | Quarterly. Two questions per section: can this rule be removed without breaking anything? Does this content already live in a skill? |
| `lint symbiosis` | Contract integrity: dependence patterns, missing pushback, stale risks. |
| `lint project sources` | Canonical-source rule for projects. Two checks: (1) **wiki/raw leakage** — files in `memento/semantic/llm-wiki/{wiki}/raw/{project-path}/` are flagged as migration candidates to `projects/{name}/raw/`. (2) **drift** — same filename in both project and wiki/raw with different hash → show diff and force a decision: discard project edit, upstream to wiki, or split (rename to make distinct). Lint never auto-syncs; it forces explicit choices. |

## handoff

Trigger: explicit signal the session is over (`handoff`, "we're done", "thanks for today").

Run the session-end protocol immediately.

## Session end

Triggered by `handoff` or any session-end phrase.

1. Archive the session scratchpad to `episodic/sessions/raw/` with a `## Summary` block at the top.
2. Show `Now` and `Next` from `prospective/tasks/tasks.md` so the next session opens with visibility on what's pending.
3. Scan `episodic/lessons/`. If unprocessed entries exist, suggest `ingest lessons`. Wait for confirmation before writing into character / harness / wiki / skills.
4. Scan `prospective/tasks/inbox.md`. If unsorted entries exist, suggest `ingest tasks`. Wait for confirmation.
