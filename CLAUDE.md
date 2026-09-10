# date-time-remote-mcp — project rules

## The record (standing)

This project keeps its decisions in `docs/decision-log.md` (D / F / P / O, append-only) and its open
questions in `docs/explorations/`. **A decision made in chat is a D-entry the same turn it's made;**
a question with several open parts is an exploration. `docs/meta/working-agreement.md` is how Claude
works here — read it first. Regenerate the indexes with `python3 tools/build_index.py` before
committing; `python3 -m unittest tools/test_build_index.py` fails when they're stale.

## The swarm (standing, D-006, D-010)

Multi-agent work here runs through the `swarm-core` plugin (`swarm-core@swarm-builder`,
source `~/Code/swarm-builder/plugin/swarm-core`): gate agents `swarm-core:swarm-test-writer`,
`swarm-core:swarm-verifier`, `swarm-core:swarm-qa`, playbooks `/swarm-core:swarm-build` and
`/swarm-core:fix-it`, plus this repo's engineer `.claude/agents/datetime-engineer.md`, per
`docs/swarm.md` (project section) and `docs/swarm-core.md` (the core, embedded at the
installed version). **Every deploy is HELD** — production is on awarm; state the commands,
never run them. Roles are enforced by the plugin's tool grants and hooks: the test-writer
cannot run tests, the verifier and qa cannot edit, subagents cannot write the log or a
contract, no run writes a D-entry.
