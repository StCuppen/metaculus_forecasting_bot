# Agent Memory

Shared knowledge base for all coding agents working on this repo (Claude Code, Codex, Cursor, Copilot, etc.).

## How Agents Should Use This Folder

### On session start — read these files first
1. **`current_state.md`** — **volatile, dated** facts: active season/tournament, model roster, keys,
   search provider, caps. Read this first and check its `Last verified` date.
2. **`architecture.md`** — project structure, pipelines, key file paths (durable)
3. **`conventions.md`** — coding patterns, prompt rules (durable)
4. **`lessons.md`** — hard-won debugging insights and gotchas (durable)

These are the "always-relevant" context. Read them before making changes.

### During a session
- **`changelog.md`** — rolling log of recent sessions. Skim for context on what changed recently, but don't treat old entries as current truth. Architecture/conventions/lessons files are the source of truth.

### After a session — update what you learned
- **Stable facts** (project structure changed, new pipeline added, model swapped) → update `architecture.md` or `conventions.md`
- **Debugging insight or gotcha** confirmed across multiple instances → add to `lessons.md`
- **Session summary** (what was built/fixed/tested) → append to `changelog.md`

### Rules
1. **Durable vs volatile — the staleness rule.** Facts that *expire* (model versions, active
   season/tournament, keys, caps, cost defaults) live **only** in `current_state.md`, each line
   dated `(as of YYYY-MM-DD)`, under a file-level `Last verified` date. Durable invariants (pipeline
   structure, gating rules, lessons) go in the topical files and stay **undated** except for a single
   `Last reviewed: YYYY-MM-DD` footer per file. This makes old-vs-new visible at a glance instead of
   letting stale facts hide among durable ones.
2. **Topical, not chronological.** Architecture, conventions, and lessons are organized by topic. Don't append timestamped entries to them — edit the relevant section (then bump its `Last reviewed`).
3. **Keep it concise.** These files are injected into agent context windows. Every line costs tokens. If a fact is no longer true, delete it.
4. **Absolute dates only.** Convert relative terms ("next month", "last week") to explicit dates.
5. **Changelog gets trimmed.** Keep only the last ~5 sessions. Older entries should be deleted — their durable lessons belong in `lessons.md`, not in the log. The changelog is the *one* place chronological/dated entries belong.
6. **Don't duplicate.** If a fact is in `architecture.md`, don't also put it in `lessons.md`. Each file has a clear scope.
7. **Verify before writing.** Don't add speculative conclusions from a single file read. Confirm against project code/docs first.

## Legacy Files (root directory)
- **`MEMORY.md`** and **`codingagentmemory.md`** in the repo root are **legacy** files. They are kept for reference but are no longer the active memory. All new memory updates should go into this `memory/` folder.

## File Overview

```
memory/
├── README.md          # This file — usage instructions
├── current_state.md   # VOLATILE dated facts: season, roster, keys, search, caps
├── architecture.md    # Project structure, pipelines, key files (durable)
├── conventions.md     # Coding patterns, prompt rules (durable)
├── lessons.md         # Debugging insights, gotchas (durable)
└── changelog.md       # Rolling session log (last ~5 sessions)
```
