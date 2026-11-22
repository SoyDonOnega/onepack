**What:** Google's Elephant-Goldfish Model (EGM, `google/elephant-goldfish-model`, Apache-2.0). A design-first spec layer. The "Elephant" (your session, with the project context) explores the problem and drafts a design document; "Goldfish" reviewers (fresh subagents with no conversation history) read only the document and the code it references, to expose unstated assumptions and gaps. You approve the design, then implement. It stops at the approved spec: no plan/tasks/implement phases.

**Choose when:**
- A feature with real design decisions (failure modes, data model, interfaces) where a second, context-free reading is worth the cost.
- You already have a design doc, README or PR plan and want it reviewed against the live code (`egm-review`).
- You want to check that existing design docs still match the code (`egm-drift-report`).

**Avoid when:** a small fix or spike; you need a task list and gated implementation (Spec Kit) or change-by-change living specs (OpenSpec); you need to keep Claude usage low.

**Workflow:**
1. `/egm:egm-brainstorm <idea>` → discussion with reviewer challenges, saved as `concepts_brief.md`.
2. `/egm:egm-draft` → `design_draft.md`, section by section, pausing for your feedback.
3. `/egm:egm-review design_draft.md` → five review phases (zoom out, comprehension, design critique, zoom out, implementation readiness).
4. `/egm:egm-resolve` → apply or decide on the reviewers' findings. Save the approved spec under `docs/designs/`, then implement.
- Small iterations, spec revisions, refactors, bug fixes: `/egm:egm-lite`.
- Other documents with your own reviewers and standards: `/egm:egm-review-loop`.
- Doc/code consistency: `/egm:egm-drift-report docs/designs/`. Per-folder README contracts: `/egm:egm-bootstrap <path>`.

**Cost:** ~0.8k tokens per session in the repo (`onepack add` reports ~801; mostly the 10 reviewer agent descriptions; the 8 skills load only when typed, ~1k to ~9k each). Each review spawns several subagents across five phases, so a full review costs **much more Claude usage** than a normal session.

**Combines with:** Pocock (`tdd` / `code-review` while implementing the approved design; skip its `to-spec`) or pstack (`poteto-mode` to implement and verify). Not with Spec Kit or OpenSpec: two spec systems.
