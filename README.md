# Claude Workspace Standard

An enterprise-style operating standard for running a **multi-project personal
workspace with an AI agent** (Claude Code), distilled from running a real
job-search operation this way — 7 sub-projects, 3 repos, ~150 tests, a daily
automation cycle, and dozens of agent sessions that all pick up cold and hand
off clean.

The whole standard fits in one file: **[`SKILL.md`](SKILL.md)**.

## The problem it solves

Agent conversations are disposable; your work isn't. Without a standard,
every new chat re-derives context, drive-by edits pile up, decisions evaporate
with the transcript, and nobody knows what the human still owes the pipeline.

## The core ideas (核心要领)

| Idea | Mechanism |
|---|---|
| **处处留痕** — every change leaves a trace | `WORKLOG.md`: one chronological ledger, one entry per unit of work (Did / Why / Result / Next), newest on top. Non-obvious choices get a **DECISION** record (Context / Chose / Rejected / Revisit-if). |
| **Roles are written down** | Agent = project lead (plan, build, draft, track, propose). Human = decision-maker + external executor (submit, send, publish, pay). The goal sits at the top of the README. |
| **一会话一线** — one conversation, one lane | Group sub-projects into 5–7 lanes; each chat declares one lane at pickup ("接手 <lane>") and stays in it. Out-of-lane work is escalated to the board, not done drive-by. |
| **The board is the seam** | `NEXT_ACTIONS.md`: two live queues (human's real-world actions with deadlines / agent's build backlog with triggers), updated at every hand-off. WORKLOG is history; the board is *now*. |
| **One source of truth per fact** | Update the home file, never the copy; generated outputs are never the master; secrets only in git-ignored `.env`. |
| **可接手** — take over cold | Fixed pickup read-order (memory → README → WORKLOG → board → lane docs) and a hard hand-off checklist, including "git status clean in every repo touched". |

## Install

Copy the skill into any workspace you run with Claude Code:

```
your-workspace/
├── .claude/skills/workspace-standard/SKILL.md   ← SKILL.md from this repo
├── README.md            ← add your goal + folder map + lane table
├── WORKLOG.md           ← start from templates/WORKLOG.md
└── NEXT_ACTIONS.md      ← start from templates/NEXT_ACTIONS.md
```

Then open every conversation with "接手 <lane>" (pick up \<lane\>) and end it
against the §7 checklist.

## Templates

- [`templates/WORKLOG.md`](templates/WORKLOG.md) — the ledger, with entry + DECISION formats.
- [`templates/NEXT_ACTIONS.md`](templates/NEXT_ACTIONS.md) — the two-queue action board.

## License

MIT.
