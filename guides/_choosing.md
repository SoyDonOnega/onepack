## How to choose

Decide two things separately, then combine:

1. **Spec layer (group `sdd`)** — does the work need a written agreement before code?
   - No: small fix, script, spike, one-file change → no SDD.
   - Yes, existing codebase, change by change → **openspec**.
   - Yes, greenfield or large feature, full plan with gates → **speckit**.
2. **Method (group `method`)** — how should the agent work?
   - Human in the loop, spec/tickets in a tracker, tdd, review → **pocock**.
   - Hard engineering (perf, forensics, subtle bugs, behaviour-preserving refactors), long or parallel runs, Claude usage not a concern → **pstack**.
   - Simple work → no method pack.
3. **Tool packs (no group)** — combine with anything when the task needs them:
   - Studying how an existing app works, to spec your own version → **rea**.

**Default to fewer packs.** "No pack" is a valid answer: plain Claude Code plus the always-available own skills covers most small work. Each method pack adds tokens to every session in the repo (pocock ~1.5k, pstack ~4.4k).

**Rules:** at most one pack per group per repo. Avoid two spec systems: with an SDD framework, do not also use Pocock's `to-spec` / `to-tickets`.

## Always available (own skills, no pack needed)

- `/mirror` — restate a long or fuzzy brief before starting (problem, goals, limits, gaps).
- `/inspo` — prior art: similar GitHub repos and X posts before building.
- `/knowledge-sources` — research scoped to trusted legal/tax sources, with verified citations.
- `/file-updater` — roll a DOCX/XLSX/PPTX report to the next period.
- `/brand-dna` — extract a brand from a URL and apply it to a deliverable.
