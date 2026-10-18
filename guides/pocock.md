**What:** Matt Pocock's skills for disciplined engineering with a human in the loop: align first, then spec, tickets, build test-first, review. "Skills for real engineers", not vibe coding.

**Choose when:**
- A feature or change in a real codebase where you want to stay in control of each step.
- You want a spec and tickets in an issue tracker (GitHub, GitLab or local files).
- Bug hunting with a gated loop (`diagnosing-bugs`), test-first work (`tdd`), architecture review.
- A big, foggy effort that spans sessions (`wayfinder`).

**Avoid when:** you only need a quick script or a one-file change (plain Claude is enough); you want agents to run long and parallel on their own (pstack fits better).

**Workflow:**
1. Once per repo: `/pocock:setup-matt-pocock-skills` (issue tracker, labels, docs folder).
2. Align: `/pocock:grill-with-docs` (code; updates glossary and ADRs) or `/pocock:grill-me` (non-code).
3. `/pocock:to-spec` → spec in the tracker. 4. `/pocock:to-tickets` → tracer-bullet tickets.
5. `/pocock:implement` (one ticket set: drives `tdd`, ends with `code-review`) or `/pocock:implement-spec` (whole spec, parallel subagents).
- Bugs: `/pocock:diagnosing-bugs`. Big effort: `/pocock:wayfinder`. After a session: `/pocock:retro`.

**Cost:** ~1.5k tokens added to every session in the repo. Mostly user-invoked skills, so little else until used.

**Combines with:** either SDD framework; with Spec Kit or OpenSpec, use their spec flow and keep Pocock for `grill-*`, `tdd`, `code-review`, `diagnosing-bugs` (skip `to-spec` / `to-tickets` to avoid two spec systems).
