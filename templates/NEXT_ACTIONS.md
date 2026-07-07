# NEXT_ACTIONS — 行动看板

The live action board. Two queues; every session updates it on hand-off
(done → remove; new → add with owner + deadline; stale → challenge).
History lives in `WORKLOG.md`; this file is *now*.

_Last updated: YYYY-MM-DD (session: <lane> — <one-line what>)._

## Human's queue（真实世界动作，按优先级）

| # | Action | Deadline / note |
|---|--------|-----------------|
| 1 | … | … |

## Agent's queue（构建 / 自动化 backlog，按 lane 标注）

| # | Lane | Action | Trigger / note |
|---|------|--------|----------------|
| 1 | … | … | do when X — nothing gets built for its own sake |
