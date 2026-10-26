**What:** REA ("Reverse Engineer Anything", morluto/rea): one MCP server to study how an application works, from its runtime behaviour and JavaScript down to native binaries (optionally through Hopper, Ghidra or IDA).

**Choose when:** you need to understand how an existing app or feature behaves to write a spec for your own implementation (e.g. studying an app's flows and network API before rebuilding the idea).

**Avoid when:** the task does not involve understanding an existing application.

**Workflow:** `onepack add rea` registers the server for this folder only (Claude Code local scope, never committed) and installs Electron globally if missing, to run Electron apps (an original and your rebuild) side by side; REA itself does not need it. Then ask the agent to analyse the target with REA and turn the findings into a spec (e.g. `/speckit-specify`).

**Cost:** an MCP server's tool descriptions load in sessions in that folder; it runs through `npx rea-agents@latest`, so it is always the latest release (Node.js needed). Electron takes ~270 MB once, shared by every folder; `onepack update` keeps it current.

**Combines with:** anything (no group); typical pair: speckit or openspec for the spec.
