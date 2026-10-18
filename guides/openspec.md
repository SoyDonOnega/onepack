**What:** OpenSpec (Fission-AI). Lightweight spec layer: "fluid not rigid", "iterative not waterfall", "built for brownfield not just greenfield". Each change is a folder (`openspec/changes/<name>/`: proposal, spec deltas as ADDED/MODIFIED requirements with SHALL + WHEN/THEN scenarios, design, tasks) that is archived into the living specs when done.

**Choose when:**
- Changes to an existing codebase, one at a time, with a short written agreement before code.
- You want specs that stay current with the code (archive merges each change into `openspec/specs/`).
- You want less ceremony than Spec Kit.

**Avoid when:** you need a full upfront plan for a large greenfield product with formal gates (Spec Kit); a trivial fix.

**Workflow:**
1. `/opsx:explore` (optional): think the change through.
2. `/opsx:propose <change-name>` → proposal, spec deltas, design, tasks.
3. `/opsx:apply` → works through the task list.
4. `/opsx:archive` → merges the deltas into the specs and archives the change.
- More commands (`new`, `continue`, `ff`, `verify`, `onboard`): `openspec config profile`, then `openspec update`.

**Cost:** 0 outside the repo; commands load only when typed.

**Combines with:** Pocock (`grill-*` before `propose`, `tdd` / `code-review` during apply) or pstack (`poteto-mode` during apply).
