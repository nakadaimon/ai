# Hooks

> Triggers the agent detects and fires automatically during work. Mirrors `commands.md` — there the user is the subject, here the agent is. Loads eagerly: hooks fire mid-work without explicit invocation, so lazy-loading defeats the point.

A hook is a deterministic *if-X-then-Y* rule where:

- The **trigger** is a concrete observable state (file timestamp, command failure, phrase pattern, session signal) — not a filter or a principle.
- The **action** is a specific operation — a tool call, a command, a file edit.

Softer rules (push back, dependence checks, self-review, ask-first before destructive changes) are general behavior and belong in `character/` or `harness/operations.md`. They are not hooks. The split is testable: a hook trigger must be expressible as a state the agent can observe; a principle filters every action without a discrete trigger.

Each hook carries a **detection surface** — what kind of runtime can observe the trigger. Phrase detection works in conversational agents but not in non-interactive scripts; filesystem triggers work everywhere; session signals depend on what the runtime exposes. Mark the surface so adopters know what their runtime supports.

## Hook table

| Hook | Trigger | Action | Surface |
|---|---|---|---|
| `session-end-detect` | The user signals the session is over ("bye", "thanks for today", "that's all") | Run the session-end protocol in `commands.md` | phrase |
| `capture-detect` | A phrase that is clearly a future task ("I should check X", "remind me about Y") | Run `capture` | phrase |
| `derived-follow-source` | A write to a source file whose derived artifacts (index, catalog, generated view) are now older than the source | Regenerate the derived artifact as the last step of the task | filesystem |

These three are the generic starters. Your own hooks emerge from your work — add them as their triggers become observable, and keep the table the single home for implicit triggers: no trigger should live in `operations.md` or `commands.md` simultaneously.

## Details

### session-end-detect

The hook is the *detection*; the procedure lives in `commands.md` (Session end). The `handoff` command is the explicit equivalent the user can trigger manually.

### capture-detect

Fuzzier than the others. Sharp form: the phrase contains future-action markers ("I should", "need to", "remember to check") *and* the agent judges it a task rather than conversational context — fire directly when unambiguous, otherwise propose `capture` first.

### derived-follow-source

The generic form of "derived artifacts follow their source." After any write to a file that feeds a derived artifact — a catalog row, a generated index, a summary view — the derived artifact's timestamp must end up newer than the source's. If it doesn't, the task isn't complete.

## Promotion pressure

Hooks sit one rung below scripts on the promotion ladder. A hook deterministic enough to need no judgment — pure filesystem trigger, single-line action — should become a script or scheduled task; the prose stage is for hooks that still need the agent's eyes. `lint hooks` (see `commands.md`) names the candidates.
