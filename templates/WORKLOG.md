# WORKLOG — <workspace name>

The single chronological ledger for this workspace. **Newest entry on top.**
Append one entry per meaningful unit of work; tag decisions with `DECISION`.
Format and rules: `.claude/skills/workspace-standard/SKILL.md`.

Entry template:
```
## YYYY-MM-DD — <short title>  [project: <lane>]
- **Did:** what changed, in files. Link paths.
- **Why:** the reason / what was asked.
- **Result:** outcome, numbers, tests passing, links.
- **Next / open:** what's unfinished. "none" if clean.
```

DECISION template:
```
## YYYY-MM-DD — DECISION: <the choice>  [project: <lane>]
- **Context:** what forced the choice.
- **Chose:** X, because …
- **Rejected:** Y (why not).
- **Revisit if:** the condition that would change this.
```

---

## Baseline as of YYYY-MM-DD (state carried over from before the ledger existed)
- <project / asset> — <current state, links>.
- **Open items:** <anything already known to be pending>.
