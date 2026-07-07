---
name: cover-letters
description: >-
  Methodology for evidence-based cover letters: an evidence bank mined from
  the candidate's real record, JD keyword mirroring, honest gap handling via
  transferable proof, a four-paragraph structure with a clear ask, and a
  draft-generator pattern the agent can run per posting. Use when drafting or
  reviewing a cover letter or building letter tooling.
---

# Cover Letters

A cover letter is an argument, not a formality: *this specific evidence makes
me worth interviewing for this specific role.* Everything below serves that
argument.

## 1. The evidence bank

Maintain one reusable bank of the candidate's strongest proof points, each a
single sentence with a number in it, tagged by the skills it evidences
(e.g. records processed, model metrics, money/time saved, tests passing).
Letters are assembled from the bank — never written from vibes. New
achievement → new bank entry first.

## 2. Structure (one page, four paragraphs)

1. **Hook** — the single strongest result relevant to *this* role, stated
   plainly. Never open on enthusiasm, biography, or a weakness.
2. **Evidence** — 2–3 bank items mapped to the JD's top requirements,
   mirroring the JD's own vocabulary honestly. Every skill claimed gets a
   concrete example; a skill without an example gets cut.
3. **Gap handling** — where the JD asks for experience the candidate lacks,
   name the nearest transferable evidence and one honest line of intent
   ("early in X, eager to learn it properly"). Honesty here reads as
   confidence; pretending reads as risk.
4. **Close** — why this company specifically (one researched line, not
   flattery) and a clear, single ask.

## 3. Generator pattern (agent tooling)

The drafting loop automates well: parse the JD → score evidence-bank entries
against it (word-boundary tag matching — substring matching false-positives
on short tags) → assemble a draft with the top evidence → insert the gap
line when a required tag has no owned evidence → emit text + document
formats. Test the matcher: the two real bugs found in production were a
substring tag matching inside an unrelated word, and a transferability tag
suppressing the gap line it should have triggered.

Generated drafts are scaffolding: the human rewrites for voice before
sending, same as any outbound copy.

## 4. Rules that survived contact

- Research the company for one specific, checkable fact; generic praise is
  filler.
- Match the résumé's factual claims exactly — a letter/résumé inconsistency
  is a screening red flag.
- Keep every sent letter; they become templates for their track.
- Track applications in the master tracker, not in the letters folder.
