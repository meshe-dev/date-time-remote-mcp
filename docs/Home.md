# date-time-remote-mcp — docs

A remote MCP server with one tool, `get_current_datetime_pdt`, returning the current Pacific date and time as `DayOfWeek Month DD, YYYY HH:MMam/pm PDT` over Streamable HTTP with no authentication. One file (`server.py`, FastMCP), a Dockerfile and a compose file; deployed as a container on the Oracle Cloud VM awarm behind nginx-proxy-manager, host port 8222. This folder holds the project record: the decisions behind the four commits that built it, what has been found since, and the open loops. The repo is also the first target of swarm-builder's `/swarm-init` hand-run (exploration 03 T-6, pass 1).

## Map of content

### The record
- [Decision log](decision-log.md) — append-only; **D**-nnn decisions, **F**-nnn findings (OBS / HYP / LIT / CONF), **P**-nnn principles, **O**-nnn open loops with gates. The "why" document; law.
- [Decision index](Decision-Index.md) — generated, one line per entry. Navigation, never canon.
- [Exploration index](Exploration-Index.md) — generated, one line per working doc.

### Explorations (working docs — nothing decided until it's in the log)
- (none yet — copy `explorations/00-template.md`, set `type: exploration`)

### Reference
- [README](../README.md) — run, client config, curl smoke test.

### Meta
- [Working agreement](meta/working-agreement.md) — the rules that bind Claude here.

## Conventions

- **Decisions go in the log, never scattered.** A decision made in chat is a D-entry the same turn; a question with several open parts is an exploration; other docs cite entries by ID rather than restating the reasoning.
- **Explorations carry frontmatter** (`type: exploration`, `status`, `created`, `updated`, `tags`, `related`, `description`) and open with the *nothing decided* banner. Questions are **Q-n**, zero-cost checks are **T-n**, numbered within the doc. When a question is answered, the answer is a log entry and the exploration's `related` points at it; the page itself is not rewritten.
- **The indexes are generated:** `python3 tools/build_index.py` (`--check` in the tests fails when they're stale). Edit the log or the exploration, never the index.
- **IDs are glossed on first mention** in any message, commit body or doc paragraph — `D-009 (fuzzy phrase, exact anchors)`.
- **Grammar matches the vaults:** attribution meshe / claude / joint; ISO dates; append-only; reversals are new entries naming what died and what survived.
