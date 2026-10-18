**What:** GitHub Spec Kit. Full spec-driven pipeline with phase gates: constitution → specify → clarify → plan → tasks → analyze → implement → converge. Files live in the repo (`.specify/`, `specs/<feature>/`). OpenSpec describes it as "thorough but heavyweight".

**Choose when:**
- Greenfield product or a large new feature where you want the full trail: principles, spec, technical plan, task list, consistency check.
- Several people or agents must work from the same written plan.
- You want hard gates before code (clarify, analyze, checklists).

**Avoid when:** small or iterative changes to an existing codebase (OpenSpec is lighter); exploratory prototypes.

**Workflow:**
1. Once: `/speckit-constitution <project principles>`.
2. Per feature: `/speckit-specify <what and why, not how>` → `/speckit-clarify` (if gaps) → `/speckit-plan <tech choices>` → `/speckit-tasks` → `/speckit-analyze` (optional) → `/speckit-implement` → `/speckit-converge` until converged.
- Extras on demand: `/speckit-checklist`, `/speckit-taskstoissues`; extensions `bug` and `assess` (`specify extension add …`).

**Cost:** 0 outside the repo; skills load only when typed.

**Combines with:** Pocock (`grill-*` before `specify`, `tdd` / `code-review` during implement) or pstack (`poteto-mode` to execute and verify tasks).
