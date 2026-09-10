---
generated: true
source: decision-log.md
---
# Decision Index

> Generated from `decision-log.md` by `tools/build_index.py` — do not edit here, edits are overwritten. Navigation, never canon.

| ID | Date / opened | Who / gate | Headline |
|---|---|---|---|
| D-001 | 2026-04-04 | meshe | A remote MCP server that returns the current Pacific time, Streamable HTTP, no authentication, dockerized |
| D-002 | 2026-04-04 | meshe | Output is human-readable, not ISO |
| D-003 | 2026-04-04 | meshe | Host port 8222, container port 8000 |
| D-004 | 2026-04-04 | meshe | The container joins the external `nginx-proxy-manager` network for reverse-proxy access |
| D-005 | 2026-09-09 16:27 PDT | meshe | This repo adopts the project record |
| D-006 | 2026-09-09 16:33 PDT | joint | This repo gets a swarm, hand-generated from the swarm core doctrine draft; every deploy is HELD |
| D-007 | 2026-09-09 16:40 PDT | claude | Two orchestrator amendments to the O-001 contract during the first swarm run: `requirements.txt` pins `mcp[cli]>=1.9.0,<2`, and Rejections row 3 reads "ignored by the MCP layer", not "rejected" |
| D-008 | 2026-09-09 16:48 PDT | claude | The tool reports whatever abbreviation IANA gives `America/Vancouver`; from 2026-11-01 that is `MST`, and the contract's winter rows are amended accordingly |
| D-009 | 2026-09-09 17:03 PDT | meshe | The abbreviation is whatever `ZoneInfo("America/Vancouver")` returns for the supplied datetime |
| F-004 | 2026-09-09 16:48 PDT | claude | IANA tzdata 2026b moves `America/Vancouver` to permanent UTC−7 labelled `MST` from 2026-11-01 02:00; both the host and the `python:3.13-slim` image carry it |
| F-003 | 2026-09-09 16:40 PDT | claude | `mcp[cli]>=1.9.0` now resolves to mcp 2.2.0, which removes `mcp.server.fastmcp`; an unpinned rebuild of the image would crash at import |
| F-001 | 2026-09-09 16:27 PDT | claude | The server hardcodes UTC−7 and the literal "PDT", so from November to March it reports Pacific *Daylight* time while the wall clock is Pacific *Standard* |
| F-002 | 2026-09-09 16:27 PDT | claude | Deploy and test surface as found: no tests, no CI, no deploy script; the production host and URL are not in the repo |
| O-001 | 2026-09-09 16:27 PDT | gate: the first swarm run on this repo (swarm-builder T-6 step 4), deploy held for meshe | DST bug (F-001): the server reports PDT year-round |
| O-002 | 2026-09-09 16:27 PDT | gate: meshe (or the vault's `Oracle services` note) — record the path and hostname here or there, no credentials | Production location not recorded: compose path on awarm, public hostname behind nginx-proxy-manager, and how the workstation's MCP client reaches it |
| O-003 | 2026-09-09 16:27 PDT | gate: the swarm's test-writer under the contract for O-001 | No tests and no CI (F-002) |
| O-004 | 2026-09-09 16:27 PDT | gate: meshe | Is this repo a dashboard KB source (`kb_*` MCP, wiki page)? Not asked at adoption; if yes, the log is reachable through `decision_get` once registered |
| O-005 | 2026-09-09 16:33 PDT | gate: meshe | Ratify the swarm (D-006): roster, model assignment, the two test tiers, no headless lane, push/merge policy — or change any of it |
| O-006 | 2026-09-09 16:48 PDT | gate: meshe, before the O-001 deploy **Label half closed 2026-09-09 17:03 PDT — D-009 (IANA abbreviation as built); rename still open** | Tool name `get_current_datetime_pdt` and the client key `datetime-pdt` are now doubly misleading: the output is `PST` in past winters and `MST` from 2026-11-01 (D-008) |
| O-007 | 2026-09-09 16:48 PDT | gate: a future contract | mcp 2.x migration (F-003): `FastMCP` → `MCPServer` per the SDK migration guide, once the `<2` pin is no longer wanted |
