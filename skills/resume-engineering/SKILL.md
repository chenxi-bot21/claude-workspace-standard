---
name: resume-engineering
description: >-
  Methodology for engineering résumés as generated artifacts: a single
  source-of-truth profile, per-track variants produced by honest domain
  reframing (never fabrication), ATS keyword tuning with an explicit honesty
  ceiling, format rules that survive automated parsers, and a compile-scan
  verification loop. Use when building, tailoring, or auditing a résumé, or
  when a job description demands keyword alignment.
---

# Résumé Engineering

Treat the résumé as a **build artifact**: facts live in one source-of-truth
profile; each résumé is a generated, verified output. Never edit the PDF of
record directly, and never let a generated copy become the master.

## 1. Source of truth

- `PROFILE.md` — every verifiable fact: education, roles with exact dates,
  research with real methods and numbers, skills actually owned.
- `PROJECTS.md` — per-project write-ups plus ready-to-paste bullets.
- Résumés (`.tex → .pdf`) are outputs. When a fact changes, fix the profile
  first, then regenerate; a stale source of truth silently spreads into
  every future variant.
- Keep the original evidence (thesis, posters, manuscripts) archived beside
  the profile — cite from it, don't duplicate facts out of it.

## 2. Format that survives parsers

- **One page** for early-career; conservative layout: single column, a
  standard serif, black and white, no icons, tables, or text boxes.
- Disable hyphenation (`\hyphenpenalty=10000` in LaTeX) — a line-break
  hyphen splits a keyword and the parser misses it.
- **Un-blob joined tokens:** `PD×LGD×EAD` or `KYC/CDD` parse as one unknown
  word; space them (`KYC / CDD`) so each term matches.
- Spell out a high-value acronym once (e.g. "Probability of Default (PD)"),
  then use the acronym; skip expansions for universal terms. Mirror a target
  JD's phrasing when it differs.
- Check the compiler's exit code; a failed compile silently leaves a stale
  PDF that looks current.

## 3. ATS tuning with an honesty ceiling

- Scan with a keyword tool (exact + acronym-variant matching against a
  curated bank; coverage % with qualification bands; format checks;
  keyword-stuffing detection). Coverage target ≈ 90%, **not 100%**.
- **The ceiling:** never add a keyword for a skill the candidate does not
  own. Modern ATS flags stuffing, and every listed term is an interview
  question waiting to happen. Keep an explicit list of deliberate misses
  (terms the scan wants but the candidate can't defend) so the gap is a
  decision, not an oversight.
- Run the scanner in JD mode against each specific posting before applying;
  fix parse problems (blobs, hyphenation) before considering content
  changes.

## 4. Per-track variants — reframe, never fabricate

One profile, N variants, one per target track. A variant differs by:
- **Selection** — drop the section least relevant to this reader to hold one
  page.
- **Reframing** — restate the same real experience in the track's language
  (e.g. issuer review → due-diligence and escalation language for a
  compliance track; a scored model → "statistical ML pipeline" for a data
  track). The facts do not change; the vocabulary does.
- **A targeting summary** only where the variant needs it (career-changer
  tracks); it may name the target honestly ("seeking a first role in X") —
  it may **not** claim experience that doesn't exist. "Self-studied X" as a
  qualification line is an amateur signal; a real certification is the only
  legitimate hard-keyword shortcut, and its entry stays commented out until
  enrollment actually happens.

## 5. Verification loop

Every change runs: regenerate → confirm page count → ATS scan (general +
JD mode) → read it aloud for naturalness (keyword-soup bullets fail human
screens even when they pass parsers). Log the coverage number and what was
deliberately left out.
