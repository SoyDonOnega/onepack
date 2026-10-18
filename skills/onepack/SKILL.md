---
name: onepack
description: >-
  Recommends which onepack packs (pocock, pstack, speckit, openspec, or none) fit what
  the user wants to do in the current repo, and the exact workflow to follow; offers to
  turn them on. Use when the user runs /onepack <what they want to do>.
license: MIT
compatibility: Needs the onepack CLI (~/.onepack) and git. Plugin packs need a harness with plugin marketplaces (Claude Code).
argument-hint: "<what you want to do>"
disable-model-invocation: true
---

# onepack — which pack, and how

Input: what the user wants to do (the text after `/onepack`). If empty, ask for it in one line.

The catalog lives outside the skill, in the onepack checkout: `~/.onepack/CATALOG.md` (updated daily).

## Steps

1. Read `~/.onepack/CATALOG.md` in full: choosing rules, the four packs (when to use, when not, workflow, cost, combinations) and the real skill list of each plugin. It is the only source for pack facts; do not add skills or commands that are not in it.
2. Look at the repo, read-only:
   - `onepack list` → which packs are already on (respect the one-per-group rule).
   - `git rev-parse --show-toplevel`, `git log --oneline -5`, `ls` of the root → greenfield or existing code, stack, size.
   - No git repo → say packs are per repo and recommend for the repo the user names, or `git init` first.
3. If one fact would change the recommendation and you cannot infer it (e.g. greenfield vs existing code, need for a written spec), ask **at most two** short questions, then decide. Otherwise do not ask.
4. Decide per the catalog's "How to choose": spec layer (none / openspec / speckit) and method (none / pocock / pstack). Prefer fewer packs; "no pack" is a valid answer. An own skill (`/mirror`, `/inspo`, …) may be the better first step.
5. Answer in the user's language, this shape:

```
Recomendación: <packs, or "ningún pack">
Por qué: <2–4 bullets, each tied to the user's task; name the alternative you rejected and why>
Cómo: <numbered steps with the exact commands, e.g. /opsx:propose <name>, /pocock:tdd>
Coste: <always-on tokens added in this repo; usage caveats, e.g. pstack subagents>
Activar: onepack add <pack> [&& onepack add <pack>]
```

6. Ask whether to run the `onepack add` command(s). Run them only on an explicit yes, from the repo root, then remind: start a new session so the harness loads the packs, and commit the settings file onepack changed (see Harness notes).

## Rules

- Never recommend two packs of the same group. Packs without a group (tool packs, e.g. rea) can be added to any combination. With an SDD framework, use Pocock only for `grill-*`, `tdd`, `code-review`, `diagnosing-bugs` (not `to-spec` / `to-tickets`).
- A pack already on that fits: say so and go straight to the workflow.
- A pack already on that conflicts with the recommendation: say which one and give the `onepack remove` command; do not remove it yourself without a yes.
- No invented facts: if the catalog does not cover the task (e.g. a non-software task), say no pack fits.
- **Cómo** copies the pack's workflow from the catalog **in full and in order** (e.g. Spec Kit: specify → clarify if gaps → plan → tasks → analyze optional → implement → converge). Never skip or merge steps, and never say a step runs "automatically" unless the catalog says so.
- Every command you mention must belong to a pack that is on in this repo **or** be listed under **Activar**. Do not suggest `/pocock:*` or `/pstack:*` commands for a pack that is off without its `onepack add`.
- One recommendation, not a menu. Mention an alternative only in **Por qué**, as the rejected option.

## Harness notes

- Plugin packs (pocock, pstack) are Claude Code plugins: `onepack add` writes `.claude/settings.json`; load them with a new session or `/reload-plugins`. Commit that file so worktrees inherit the packs.
- Claude Code cloud sessions (`CLAUDE_CODE_REMOTE=true`): the environment's setup script (`cloud/setup.sh`) installs the packs as skills-directory plugins, off by default; `onepack add` turns one on with `<pack>@skills-dir` in `.claude/settings.json`, and it loads in the next cloud session (`/reload-plugins` is not available there). `rea` is not available in cloud.
- CLI packs (speckit, openspec) write their own files into the repo for the harness `onepack` targets (`--integration claude`, `--tools claude`).

