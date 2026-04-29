# AGENTS.md

> The symbiosis architecture (v3.0.0). This file boots the structure; the actual work lives one level down.

> Prefer retrieval-led reasoning over pre-training-led reasoning. Open the file before guessing what it says.

> Every rule should be testable — measurable as followed or broken. Rules without that filter belong outside this file.

## Read order

1. `character/soul.md` — the lens
2. `character/identity.md` — role and operating principles
3. `character/user.md` — who you work with
4. `character/symbiosis.md` — the contract
5. `harness/operations.md` — tools and review protocols
6. `harness/commands.md` — verbs (`ingest`, `lint`)
7. `memento/AGENTS.md` — the memory layer

When layers conflict: **character > harness > memento**. In project mode: **character > harness > project > memento** — local project context overrides general history. Values filter tools; tools filter history.

## Session start

1. Read the files above in order.
2. Check `memento/episodic/sessions/` for an in-progress scratchpad — resume if present, otherwise open a fresh one.
3. Surface anything in `memento/prospective/tasks/tasks.md` so the day's work is visible.
4. **Project mode:** if a project is named — in platform-level instructions, env, or the user's first message — read `projects/{name}/CONTEXT.md` and treat it as the local boot-loader. If `projects/{name}/` exists but lacks `CONTEXT.md`, offer to scaffold from `projects/_template/CONTEXT.md`. If the named project doesn't exist, confirm before creating.
5. The rest of `memento/` loads on demand.

> Claude Code reads `CLAUDE.md` instead of `AGENTS.md`. If you're on Claude Code, symlink: `ln -s AGENTS.md CLAUDE.md`.
