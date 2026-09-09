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
| F-001 | 2026-09-09 16:27 PDT | claude | The server hardcodes UTC−7 and the literal "PDT", so from November to March it reports Pacific *Daylight* time while the wall clock is Pacific *Standard* |
| F-002 | 2026-09-09 16:27 PDT | claude | Deploy and test surface as found: no tests, no CI, no deploy script; the production host and URL are not in the repo |
| O-001 | 2026-09-09 16:27 PDT | gate: the first swarm run on this repo (swarm-builder T-6 step 4), deploy held for meshe | DST bug (F-001): the server reports PDT year-round |
| O-002 | 2026-09-09 16:27 PDT | gate: meshe (or the vault's `Oracle services` note) — record the path and hostname here or there, no credentials | Production location not recorded: compose path on awarm, public hostname behind nginx-proxy-manager, and how the workstation's MCP client reaches it |
| O-003 | 2026-09-09 16:27 PDT | gate: the swarm's test-writer under the contract for O-001 | No tests and no CI (F-002) |
| O-004 | 2026-09-09 16:27 PDT | gate: meshe | Is this repo a dashboard KB source (`kb_*` MCP, wiki page)? Not asked at adoption; if yes, the log is reachable through `decision_get` once registered |
| O-005 | 2026-09-09 16:33 PDT | gate: meshe | Ratify the swarm (D-006): roster, model assignment, the two test tiers, no headless lane, push/merge policy — or change any of it |
