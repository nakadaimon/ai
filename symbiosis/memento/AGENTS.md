# memento

> The memory layer. Loads `episodic/` files on boot; the rest load on demand.

## episodic/

Live scratchpad (`sessions/`) and inbox for corrections (`lessons/`).

## semantic/

Synthesized knowledge: `llm-wiki/` (catalog + pages + raw), `ideas/` (drafts/published).

## procedural/

Reusable patterns: `skills/` (loaded on demand), `scripts/` (runnables).

## prospective/

Future intentions: `tasks/` (inbox, tasks, log, raw).

## See also

- `../projects/` — work artifacts (one folder per project, sibling to `memento/`). The agent reads `projects/{name}/CONTEXT.md` as a local boot-loader in project mode (see root `AGENTS.md`).
