# memento

> The memory layer. Loads `episodic/` files on boot; the rest load on demand.

## episodic/

Live scratchpad (`sessions/`) and inbox for corrections (`lessons/`).

## semantic/

Synthesized knowledge: `llm-wiki/` (catalog + pages + raw), `ideas/` (drafts/published).

## procedural/

Reusable patterns: `skills/` (loaded on demand), `scripts/` (runnables). Opt-in as they earn their place: `recipes/` (delegation briefs — Discovery → Gate → Plan → Execute packages another actor runs), `prompts/` (reusable prompt templates that recipes and skills reference), `schematics/` (technical blueprints for agents that build — architecture, data models, API specs).

## prospective/

Future intentions: `tasks/` (inbox, tasks, log, raw).

## See also

- `../projects/` — work artifacts (one folder per project, sibling to `memento/`). The agent reads `projects/{name}/CONTEXT.md` as a local boot-loader in project mode (see root `AGENTS.md`).
