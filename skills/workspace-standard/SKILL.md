---
name: workspace-standard
description: >-
  An enterprise-style operating standard for running a multi-project personal
  workspace with an AI agent — written roles, one-conversation-one-lane focus,
  a chronological work ledger with decision records, a live action board, and
  a hand-off checklist so any new session (or person) can take over cold. Use
  at the start of any work session, before and after making changes, and
  whenever standards, traceability, pickup, or handoff come up.
---

# Workspace Standard

Run the workspace like an enterprise project: **every change leaves a trace,
structure is predictable, docs stay current, and any new session can take
over cold.** This is the meta/process skill; concrete per-task skills run
underneath it.

**Four principles**
1. **Traceability** — if it mattered, it is written down: what changed, why,
   and what comes next. The chat transcript is disposable; the files are the
   memory.
2. **Extensibility** — new work goes in its own folder behind the same
   structure; pluggable over hard-coded; nothing bolted onto the wrong layer.
3. **Readability** — a stranger (or future you) understands the workspace
   from the docs alone. Plain language, one source of truth per fact, no
   secrets in the open.
4. **Handoff-readiness** — the next session reads a fixed set of files and is
   fully oriented in minutes.

---

## 0. Roles — who does what

A two-party operation with **one goal, stated at the top of the workspace
README**. Every session should be able to answer: *"how does this move the
goal forward?"*

- **The agent is the project lead.** It owns the plan and the machinery: runs
  the recurring cycles, builds and maintains the tools, drafts every
  deliverable, tracks progress, audits the workspace, and proactively
  proposes the next highest-leverage move. The agent does not wait to be
  asked for obvious follow-through, and it flags — rather than silently
  absorbs — anything that stalls the pipeline.
- **The human is the decision-maker and external executor.** Only the human
  acts in the real world (submit, send, publish, sign, pay) and has final say
  on facts and strategy pivots.
- **The seam between them is `NEXT_ACTIONS.md`** (workspace root) — a live
  action board with two queues: the human's real-world actions (with
  deadlines) and the agent's build/automation backlog. Every session ends by
  updating it. The work ledger is history; the action board is *now*.
- **Operating rhythm:** scheduled tasks handle the daily loop; roughly weekly
  the agent reviews end-to-end progress against a small set of KPIs and
  records adjustments as DECISION entries.

### 0.1 One conversation, one lane

Context drifts when a single chat touches everything. Group the sub-projects
into a handful of **lanes** (5–7 works well) and have each conversation
declare **one lane** at pickup and stay inside it.

Rules:
1. **Open by declaring the lane** — start a conversation with
   "pick up \<lane\>"; the session reads the standard pickup order plus that
   lane's own docs, and works only inside it.
2. **Shared seams stay shared** — the work ledger, the action board, and the
   source-of-truth files are updatable from any lane; that is how lanes talk.
   Tag ledger entries with the lane.
3. **Out-of-lane work is escalated, not done drive-by** — on noticing
   *substantive* work that belongs to another lane, add it to the action
   board tagged with that lane and let that lane's conversation do it.
   **Trivial fixes are exempt** (a typo, a broken link, a one-line stale
   fact): do them inline and mention it in the ledger entry — the lane rule
   serves focus, not bureaucracy. If it needs a test run, a decision, or more
   than a couple of lines, it is substantive — escalate.
4. **Only the meta/PM lane** restructures folders, edits this standard, or
   runs cross-lane audits.
5. **Concurrency etiquette** — conversations can run in parallel, and the
   shared files are where they collide. Re-read the file top immediately
   before appending or editing; another session may have updated it since you
   last looked. A stale edit fails — re-read and re-apply, never force.

---

## 1. Pick up a session — read in this order

Before doing anything, orient yourself:
1. **Session memory** — the always-loaded briefing: instance specifics, IDs,
   environment gotchas.
2. **`README.md`** (workspace root) — the goal, the folder map, the lanes.
3. **`WORKLOG.md`** (workspace root) — the last few entries: what the
   previous session did, decided, and left open.
4. **`NEXT_ACTIONS.md`** (workspace root) — the live action board.
5. **The lane's own docs** — README / RUNBOOK / METHODOLOGY of the project
   being picked up.
6. **Source-of-truth files** for the task at hand.

Only after this should you plan the actual work.

---

## 2. Leave a trace — WORKLOG.md (the ledger)

`WORKLOG.md` at the workspace root is the **single chronological ledger**.
Append a short entry on finishing a meaningful unit of work (one entry per
task/session, not per keystroke). Newest at the top.

```
## YYYY-MM-DD — <short title>  [project: <lane>]
- **Did:** what changed, in files. Link paths.
- **Why:** the reason / what was asked.
- **Result:** outcome, numbers, tests passing, links.
- **Next / open:** what's unfinished. "none" if clean.
```

Rules: real absolute dates; reference files by path; pure exploration usually
is not logged — but DO log anything learned that changes how future work
should go.

---

## 3. Record decisions — DECISION entries

On making a non-obvious choice (a trade-off, a rejected alternative, a
convention someone might later question), log it in the ledger with a
**DECISION** tag so the reasoning survives:

```
## YYYY-MM-DD — DECISION: <the choice>  [project: <lane>]
- **Context:** what forced the choice.
- **Chose:** X, because …
- **Rejected:** Y (why not).
- **Revisit if:** the condition that would change this.
```

Durable cross-session facts (service IDs, environment quirks, "always do X")
also go into **session memory** — the ledger is history, memory is the
always-loaded briefing. Put a one-liner in both when in doubt.

---

## 4. The action board — NEXT_ACTIONS.md

Two queues, updated at every hand-off:
- **The human's queue** — real-world actions only, with deadlines, ordered by
  priority.
- **The agent's queue** — build/automation backlog, each item tagged with its
  lane and its trigger ("do when X"), so nothing is built for its own sake.

Done items are removed (history lives in the ledger); new items get an owner
and a deadline; stale items are challenged, not silently carried.

---

## 5. Source-of-truth discipline

Each fact has exactly one home. Update the home, not the copy.
- Generated outputs (PDFs, compiled artifacts, reports) are never the
  master — regenerate them from the source.
- Instance specifics (IDs, the *location* of secrets, gotchas) → session
  memory.
- Secrets themselves → git-ignored `.env` only. Never commit, never paste in
  chat. If a secret is ever exposed, say so and rotate it.

On changing a fact, update its home file in the same session, then note it in
the ledger. A stale source of truth is the one bug that silently spreads.

---

## 6. Per-project structure

New work gets **its own top-level folder**. Inside, the doc quartet (add only
what applies):
- **`README.md`** — what it is + install/run. Public-safe.
- **`METHODOLOGY.md`** — how it decides, when there is real logic worth
  explaining.
- **`RUNBOOK.md`** — day-to-day operating + handoff steps. No secrets.
- **`SKILL.md`** — if the agent runs it repeatedly, encapsulate it as a
  per-task skill.

Code conventions: `src/<package>/` layout, `tests/`, run the suite before
calling anything done. Prefer pluggable seams over hard-coding — extend by
adding an implementation, not by editing callers.

---

## 7. Hand off — end-of-session checklist

- [ ] **Files reflect reality** — source of truth updated, outputs
      regenerated, tests green.
- [ ] **Repos clean** — `git status` empty in every repo touched (commit and
      push, or log why not). Uncommitted work is the most common violation
      found in audits — check even after a "docs-only" session.
- [ ] **Ledger** — entry appended (Did / Why / Result / Next).
- [ ] **DECISION** logged if a non-obvious choice was made.
- [ ] **Session memory** — updated if any durable fact/ID/gotcha changed.
- [ ] **Action board** — both queues current.
- [ ] **README / RUNBOOK** — updated if structure or operating steps changed.
- [ ] **No secrets** committed or printed.
- [ ] **Told the human** plainly what was done, what is verified, and what
      comes next.

If a session runs out of context mid-task, the ledger's "Next / open" line is
the handoff — write it as if someone else will finish.
