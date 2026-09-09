# date-time-remote-mcp — project rules

## The record (standing)

This project keeps its decisions in `docs/decision-log.md` (D / F / P / O, append-only) and its open
questions in `docs/explorations/`. **A decision made in chat is a D-entry the same turn it's made;**
a question with several open parts is an exploration. `docs/meta/working-agreement.md` is how Claude
works here — read it first. Regenerate the indexes with `python3 tools/build_index.py` before
committing; `python3 -m unittest tools/test_build_index.py` fails when they're stale.
