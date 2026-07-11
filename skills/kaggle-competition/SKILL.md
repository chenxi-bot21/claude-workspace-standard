---
name: kaggle-competition
description: >-
  A lean, auditable harness for running Kaggle competitions from an agent: a
  pluggable competition registry, a shared download -> model -> submit -> score
  loop, and two submission paths — a CSV path for getting-started/Playground
  competitions and a kernel path (scaffold -> push -> poll -> pull) for
  code-competitions whose scoring code must run on Kaggle's own GPU infra. Use
  when entering, automating, or submitting to a Kaggle competition, or when
  building a repeatable pipeline that lands real leaderboard scores on a public
  profile.
---

# Kaggle Competition Harness

A thin CLI wrapper over the official `kaggle` API that turns a competition into
a repeatable, hand-off-able pipeline. It exists to keep two things separate:
the **plumbing** (download data, submit, read the score) which is identical for
every competition, and the **modelling** which is not. You add a competition by
adding one registry entry; you never edit the harness.

The design goal is an **honest, auditable** pipeline: every score that reaches a
résumé or public profile is a real number pulled from the Kaggle API after an
actual submission, never an estimate.

## When to use

- Entering a new Kaggle competition and wanting a clean local project layout.
- Automating the download → build submission → submit → record-score loop.
- Submitting to a **code-competition** (scoring code runs on Kaggle, not your
  machine — e.g. GPU notebooks with no internet at scoring time).
- Building portfolio signal: real leaderboard placements on a public profile.

## Prerequisites (one-time, human actions)

1. **API token.** Create a Kaggle API token (Settings → API → *Create New
   Token*). Either auth style works and is auto-detected:
   - classic `~/.kaggle/kaggle.json` (username + key), or
   - newer `~/.kaggle/access_token`.
2. **Accept the rules per competition.** The API rejects downloads and
   submissions until you click *Join / I Understand and Accept* on each
   competition's rules page. One click each, once. This is the one step the
   agent cannot do for you.

## Project layout

`harness.py` and `registry.py` sit at the root of your Kaggle working
directory, next to a `competitions/` tree:

```
<root>/
  registry.py              # key -> {slug, title, rules_url, ...}  (the pluggable seam)
  harness.py               # the shared plumbing (copy from scripts/)
  LEADERBOARD.md           # real scores only, pulled from the API
  competitions/
    <key>/
      data/                # downloaded + unzipped (git-ignore this — large)
      model.py             # builds submission.csv          (CSV path)
      submission.csv
      kernel/              # code-competitions only          (kernel path)
        kernel-metadata.json
        notebook.ipynb     # or main.py
        output/            # pulled-back run outputs
      README.md            # approach + score
```

## The two submission paths

Every Kaggle competition submits one of two ways. The harness supports both
with parallel command sets.

### CSV path — getting-started / Playground

A local model script trains on your machine and writes `submission.csv`; the
harness uploads it.

```
python harness.py download <key>        # pull + unzip the data
python competitions/<key>/model.py      # your code -> submission.csv
python harness.py submit   <key> -m "message"
python harness.py score    <key>        # read the leaderboard score back off the API
```

### Kernel path — code-competitions

Some competitions forbid uploading a CSV: the scoring code must **run on
Kaggle's own infrastructure** (a notebook/script, often GPU, usually with no
internet at scoring time). The harness scaffolds the kernel, pushes and runs it
on Kaggle, polls status, and pulls the output back.

```
python harness.py kernel-init   <key> [--gpu] [--script] [--code-file f]
#   ... edit competitions/<key>/kernel/<code-file> ...
python harness.py kernel-push   <key>   # push + run on Kaggle infra
python harness.py kernel-status <key>   # poll the run
python harness.py kernel-output <key>   # pull outputs (submission.csv) locally
```

`kernel-init` writes a `kernel-metadata.json` that wires the competition as an
input source (so the notebook can read `/kaggle/input/<comp>/`), sets
`enable_internet:false` (code-competition scoring is offline), toggles GPU, and
resolves your Kaggle username automatically. It refuses to overwrite an existing
kernel unless you pass `--force`.

**The final code-competition submit is a human website click** — open the
completed notebook on Kaggle and click *Submit*. This is deliberate: it is the
same accept-the-rules-style real-world action the API can't take, and it keeps a
human in the loop before a scored, quota-consuming submission.

## Operating discipline

- **Honesty rule.** `LEADERBOARD.md` records only real API-pulled scores. What
  goes on a résumé is what the public profile shows.
- **Watch the daily submission cap.** Most competitions cap submissions per day
  (commonly 5). Don't burn slots on noise — confirm a change beats the current
  best offline (cross-validation) before spending a slot.
- **Long kernel runs die on the hidden rerun.** Code-competitions re-run your
  notebook on hidden test data with a time budget. A notebook that takes hours
  locally can complete-but-not-score on the rerun. Build for minutes, not hours.
- **Pluggable, not hard-coded.** New competition = new `registry.py` entry.
  Keep the harness untouched so it stays auditable.

## Prior art

Two heavier public Kaggle agent skills exist and are worth knowing:
[`NVIDIA/nvidia-kaggle`](https://github.com/NVIDIA/nvidia-kaggle) and the
official [`Kaggle/kaggle-skills`](https://github.com/Kaggle/kaggle-skills). They
generalize the same kernel push → run → poll loop and add research helpers
(ingesting leaderboard writeups, discussions, and public kernels into a local
database). This skill deliberately stays a thin CLI wrapper you can read top to
bottom — no plugin install, no untrusted scripts, an enforced honesty rule. If
manual research of top solutions becomes your bottleneck, NVIDIA's
`fetch_leaderboard_writeups` / `fetch_writeup` scripts are the piece worth
borrowing.

## Files

- `scripts/harness.py` — the CLI: `download | submit | score | kernel-*`.
- `scripts/registry.py` — the competition registry (edit this; two worked
  examples included — one CSV, one code-competition).
