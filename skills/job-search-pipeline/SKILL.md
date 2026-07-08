---
name: job-search-pipeline
description: >-
  Methodology for an agent-operated daily job-search pipeline: pluggable
  posting sources (a managed LinkedIn scraper via an Apify actor, free
  official job-board APIs, a JobSpy sidecar for Indeed), an ATS-style
  knockout gate for hard disqualifiers, transparent weighted scoring, a human
  curation bar, a single master application tracker, and an inbox-driven
  status feedback loop. Use when building or operating a recurring
  job-matching cycle, screening postings against a candidate profile, or
  reconciling application statuses from email.
---

# Job-Search Pipeline

The funnel, end to end:

```
sources → normalize + dedup → knockout gate → weighted score
        → human curation → master tracker → inbox feedback sync → daily digest
```

The mechanical steps run as tested code; the judgment steps (reading full job
descriptions, deciding true fit, writing tracker rows) stay with the agent in
an interactive session. Reference implementation:
[auto-job-seek](https://github.com/chenxi-bot21/ai-job-search-pipeline).

## 1. Sources — pluggable, never scraped in-house

Define one `JobSource` interface and add implementations behind it; extend by
adding a source, not by editing callers.

- **Managed scraper (recommended for LinkedIn):** an Apify actor. The input
  contract is a JSON file — `keyword[]`, `locations[]`, `publishedAt`
  (`r86400` = last 24h), `maxItems` — and the output is a dataset of raw
  postings. Cost scales with `maxItems` (cents per run). Do not scrape
  LinkedIn directly (ToS).
- **Free official APIs:** many government job boards expose public JSON
  search endpoints with no key (e.g. Singapore's MyCareersFuture:
  `POST api/v2/search`). Zero cost, high signal, small daily volume — a
  supplement, not a pillar.
- **JobSpy sidecar for Indeed:** run `python-jobspy` under a pinned
  interpreter via `uv run --python 3.12 --with python-jobspy` when the main
  environment's Python is too new for its dependency pins; write CSV, ingest
  through the normal pipeline. Never force-install it into the main env.
- **Persist every raw scrape** (`output/raw.json`) and every gate survivor
  with its full description (`candidates_full.json`). Curation needs full JD
  text, and raw files make any run re-screenable without re-paying.

### Keyword hygiene (hard-won)
- `maxItems` is usually a **global** cap: one broad keyword can eat the whole
  budget and starve the rest to zero results. Audit the per-keyword result
  distribution after config changes; prune noise magnets (e.g. a term that
  returns mostly engineering titles), keep the cap generous.
- **Never search for and penalize the same track.** If a keyword is worth
  scraping, the scorer must not down-rank its results — resolve the
  contradiction in one direction.
- Prefer **ranking boosts over tighter hard gates** when steering the mix
  (e.g. boost explicit graduate/trainee titles rather than lowering the
  max-experience cutoff and losing good borderline roles).

## 2. Knockout gate — hard disqualifiers first

Separate non-negotiables (instant disqualify) from soft signals (rank). The
gate checks, in text of the posting:
- **Work authorization** — citizens-only / no-sponsorship / clearance
  phrases, when the candidate needs sponsorship.
- **Experience floor** — the JD's *minimum* required years exceeds the
  candidate's ceiling ("minimum 3 years" means ≥3; a new grad fails it).
- **Degree** — PhD/postdoc required and the candidate is below.

Everything else is a score, not a gate: skill overlap, title relevance,
domain fit, seniority alignment, location, plus bounded focus adjustments
(±N points for priority/deprioritized title keywords, clamped, with a
human-readable reason attached to every adjustment).

## 3. Deduplication — two keys plus a backstop

- Cross-run dedup by **job id AND normalized company+title**: boards repost
  the same role under a new id, so id-only "exclude seen" leaks reposts.
- **Backstop:** before inserting a curated match into the tracker, query the
  tracker for the company/title. The strongest roles are reposted most —
  without this check you will re-surface roles the candidate already applied
  to.

## 4. The curation bar — score is a first pass, not a verdict

The agent reads every gate survivor's **full description** and applies
judgment the gate cannot:
- **KEEP:** roles squarely in the candidate's target tracks; genuine
  entry-level roles in adjacent tracks with transferable evidence.
- **CUT:** roles that keyword-match but mismatch in kind — e.g. trading-desk
  roles surfacing for "quant", pure software/data-engineering roles for
  "data", ops/middle-office dressed as "analyst", commission sales dressed
  as "investment", citizens-only defense/government labs, wrong locations,
  far-future start dates.
- **Quality over quantity.** A short honest list beats a padded one; if asked
  for a fixed count and true fits fall short, say so rather than pad.
- Assign an honest fit tier (Strong / Good / Moderate) and put every caveat
  in the notes column — the human decides with eyes open.

## 5. One master tracker

A single append-only table (Notion or equivalent) for matching AND tracking —
never a new table per day. Columns: title, company, location, fit tier,
notes (why + caveats), seniority, status, apply URL, date. Status lifecycle:
`To Apply → Applied → Assessment → Interview → Offer`, with `Rejected` and
`Dropped` as exits. **Prefer a reversible `Dropped` status over deleting
rows** — strategy changes; deletes don't undo.

## 6. Inbox feedback sync

The other half of the loop: application status flows back from email.
- Search the inbox (`newer_than:2d`) for confirmations, rejections,
  assessment invites, interview requests; reconcile each hit against the
  tracker; update statuses or add untracked rows.
- **Idempotent by design** — re-running the sync on the same mail must
  produce zero writes; verify this on the first scheduled runs.
- **Consolidate inboxes first:** auto-forward secondary addresses into one
  primary inbox so a single connector sees everything. Verify forwarding
  actually works (it is not retroactive), and backfill history once.

## 7. Daily rhythm and digest

One scheduled run per day: scrape → gate → curate → tracker → feedback sync →
a dated report file → a digest email to the human (subject: N new matches,
M status changes, action items). If programmatic send is not configured,
leave a ready-to-send draft rather than failing silently. Log every run in
the workspace ledger with counts (fetched → deduped → passed gate → curated).

## Operating gotchas

- Verify a top pick's minimum-years and sponsorship language in the actual JD
  before recommending it — gate regexes are not a substitute for reading.
- Watch scheduled runs for keyword drift (a new term flooding the digest with
  off-target roles) and prune within a day or two.
- MCP-connector steps (tracker, inbox) may require an interactive session;
  design every automated half to degrade gracefully into "report and stop".
