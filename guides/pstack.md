**What:** Lauren Tan's (poteto) pstack: "if you want to go fast, go deep first". One entry skill, `poteto-mode`, picks one of 23 playbooks (bug fix, perf, feature, refactoring, runtime/trace forensics, hillclimb, babysit a PR stack, eval, visual parity…) and pulls in ~30 engineering principles and verification skills as needed.

**Choose when:**
- Hard engineering: subtle bugs, performance, memory leaks, profiling traces, refactors that must preserve behaviour.
- You want runtime evidence and verification before "done", and fewer lines of code.
- You will run agents for long stretches or in parallel (`swarm`, `arena`, overnight "land the stack").

**Avoid when:** you want a spec/ticket trail (use Pocock or an SDD framework); the work is small; you need to keep Claude usage low.

**Workflow:**
1. `/pstack:poteto-mode <task, with the evidence you expect>`: it chooses the playbook and runs the other skills itself.
2. Unsure which skill fits: `/pstack:poteto-help`.
- `/pstack:setup-pstack` has nothing to configure in Claude Code (model routing is a Cursor rule); skip it.

**Claude Code caveats:** built for Cursor. Its multi-model routing (Grok for code delegates) falls back to the session model, and it spawns many subagents, so expect **higher Claude usage** than Pocock. Cursor-only steps (Bugbot, cloud agents, automations) are skipped.

**Cost:** ~4.4k tokens added to every session in the repo (many model-invoked principle skills), plus subagent runs.

**Combines with:** OpenSpec or Spec Kit for the spec layer; pstack then executes and verifies each task.
