# Claude Workspace Standard — an agent-operations skill suite

An operating standard for running a **multi-project personal workspace with
an AI agent** (Claude Code), plus the playbook skills distilled from its
first production use: a fully agent-operated job search — 7 sub-projects,
4 repos, ~150 tests, a scheduled daily pipeline, and dozens of agent
sessions that all pick up cold and hand off clean.

## The problem

Agent conversations are disposable; your work isn't. Without a standard,
every new chat re-derives context, drive-by edits pile up, decisions
evaporate with the transcript, and nobody knows what the human still owes
the pipeline.

## The architecture

Two written-down roles — the **agent as project lead** (plans, builds,
drafts, tracks, proposes) and the **human as decision-maker and executor**
(submits, sends, publishes, has final say) — collaborating through a shared
file layer that any conversation reads and writes:

| File | Role |
|---|---|
| `README.md` | The goal, the folder map, the lanes. |
| `WORKLOG.md` | History — one chronological ledger (Did / Why / Result / Next) plus DECISION records (Context / Chose / Rejected / Revisit-if). |
| `NEXT_ACTIONS.md` | Now — two live queues: the human's real-world actions with deadlines, the agent's build backlog with triggers. |
| Session memory | The always-loaded briefing: IDs, environment quirks, durable facts. |

Each conversation owns **one lane** (group sub-projects into 5–7), declared
at pickup; every session runs the same loop: **pick up (fixed read order) →
work (inside the lane) → hand off (checklist: repos clean, ledger and board
updated)**.

Every rule in the suite is a scar from real use, not a blog-post best
practice — the "git status clean" gate exists because an audit caught
uncommitted work; the concurrency rule exists because parallel sessions
collided on the shared files.

## The skills

| Skill | What it covers |
|---|---|
| [`workspace-standard`](skills/workspace-standard/SKILL.md) | The operating system: roles, lanes, the ledger, DECISION records, the action board, source-of-truth discipline, the hand-off checklist. |
| [`job-search-pipeline`](skills/job-search-pipeline/SKILL.md) | The daily funnel: pluggable sources (Apify LinkedIn actor, free official APIs, a JobSpy sidecar), the knockout gate, weighted scoring, the human curation bar, one master tracker, inbox feedback sync. |
| [`resume-engineering`](skills/resume-engineering/SKILL.md) | Résumés as build artifacts: one source-of-truth profile, per-track variants by honest reframing, ATS tuning with an honesty ceiling, the compile-scan loop. |
| [`cover-letters`](skills/cover-letters/SKILL.md) | Evidence-based letters: the evidence bank, four-paragraph structure, honest gap handling, the draft-generator pattern. |
| [`linkedin-visibility`](skills/linkedin-visibility/SKILL.md) | Algorithm-aware operation of a small expert account: niche consistency, the automated tone gate, de-AI rewriting, credibility-before-asks outreach sequencing. |

Reference implementation of the pipeline:
[auto-job-seek](https://github.com/chenxi-bot21/auto-job-seek).

## The projects (submodules)

The workspace's code projects — each born, built, and handed off entirely
under this standard — are pinned under [`projects/`](projects/) as git
submodules:

| Project | What it is |
|---|---|
| [`credit-risk-model`](https://github.com/chenxi-bot21/credit-risk-model) | End-to-end credit-risk PD model on Lending Club data — feature pipeline, scorecard + ML benchmarks, calibration and validation docs. |
| [`market-risk-engine`](https://github.com/chenxi-bot21/market-risk-engine) | Market-risk engine: VaR/ES four ways (historical, parametric, Monte Carlo, filtered), GARCH via MLE, Basel traffic-light backtesting. |
| [`auto-job-seek`](https://github.com/chenxi-bot21/auto-job-seek) | The agent-operated daily job-search pipeline this suite was distilled from. |
| [`risk-mcp`](https://github.com/chenxi-bot21/risk-mcp) | MCP server exposing the two risk engines to AI agents: 4-method VaR/ES, GARCH, EVT tail risk, Basel backtesting, stress scenarios, PD scorecard. |

Clone everything at once:

```
git clone --recurse-submodules https://github.com/chenxi-bot21/claude-workspace-standard.git
```

## Install

Copy any skill folder into a workspace you run with Claude Code:

```
your-workspace/
├── .claude/skills/<skill-name>/SKILL.md   ← from skills/ in this repo
├── README.md          ← add your goal + folder map + lane table
├── WORKLOG.md         ← start from templates/WORKLOG.md
└── NEXT_ACTIONS.md    ← start from templates/NEXT_ACTIONS.md
```

Then open every conversation with "pick up \<lane\>" and end it against the
hand-off checklist.

## Maturity

Distilled from one intensive production use by one person. Treat it as a
field-tested starting point, not a settled framework — adapt the lanes and
the queues to your own operation.

## License

MIT.
