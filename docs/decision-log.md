---
title: "Decision Log — date-time-remote-mcp"
type: registry
tags: [decisions]
---
# Decision Log — date-time-remote-mcp

*The running record of decisions, findings, principles and open loops for this project. **D**-nnn decisions, **F**-nnn findings (OBS / HYP / LIT / CONF), **P**-nnn principles, **O**-nnn open loops with gates. Attribution is meshe / claude / joint. Append-only — new entries land at the end of their section; reversals are new entries that say what died, why, and what survived. `Decision-Index.md` is generated from this file by `tools/build_index.py` and is navigation, never canon. Opened 2026-09-09 16:27 PDT (America/Vancouver, `YYYY-MM-DD HH:MM TZ`).*

## Decisions

**D-001** (2026-04-04, meshe) — **A remote MCP server that returns the current Pacific time, Streamable HTTP, no authentication, dockerized.** Initial commit `10227ea`: "Dockerized MCP server that returns current date/time in PDT via Streamable HTTP transport with no authentication." One tool, `get_current_datetime_pdt`; FastMCP on port 8000 inside the container. No auth is a deliberate scope choice for a read-only clock, not an omission.

**D-002** (2026-04-04, meshe) — **Output is human-readable, not ISO.** `7d476e1`: "Changed output from 'YYYY-MM-DD HH:MM:SS PDT' to 'DayOfWeek Month DD, YYYY HH:MMam/pm PDT'." Reverses the initial ISO-style format from D-001's commit; the consumer is a model reading prose, not a parser.

**D-003** (2026-04-04, meshe) — **Host port 8222, container port 8000.** `adb7e8b`: "Port 8000 is used by Portainer on the production server." The container keeps 8000; only the host mapping moved.

**D-004** (2026-04-04, meshe) — **The container joins the external `nginx-proxy-manager` network for reverse-proxy access.** `90b5404`: compose declares `nginx-proxy-manager` as an external network (`nginx-proxy-manager_nginx-proxy-manager`) alongside `default`, so the proxy on the same host can reach the service by container name.

**D-005** (2026-09-09 16:27 PDT, meshe) — **This repo adopts the project record.** `docs/decision-log.md` (D / F / P / O, append-only), `docs/explorations/`, `docs/meta/working-agreement.md` with the embedded parent block, and `tools/build_index.py`, copied from `meshe-dev/project-record` at `.record-version` 3. "Joint" here means meshe + Claude. Adopted as step 1 of swarm-builder's exploration 03 T-6 pass 1 (meshe, 2026-09-09: this repo is "not too small" as the first `/swarm-init` target because it has a real deploy on awarm and a real consumer). Backfilled from the four commits of 2026-04-04 and the adopting conversation.

## Findings

**F-001** (2026-09-09 16:27 PDT, claude) — **The server hardcodes UTC−7 and the literal "PDT", so from November to March it reports Pacific *Daylight* time while the wall clock is Pacific *Standard*.** CONF: `server.py:7` `PDT = timezone(timedelta(hours=-7))`; `server.py:14` formats with a fixed `"PDT"` suffix. Consequence: every consumer (Claude Code and Claude Desktop sessions that call `get_current_datetime_pdt`, including the swarm-builder session that found this) gets a time one hour ahead of Vancouver wall-clock during PST and a wrong abbreviation. Fix shape: `zoneinfo.ZoneInfo("America/Vancouver")` and `%Z`; regression test asserting the abbreviation and offset on both sides of a DST boundary. Open as O-001.

**F-002** (2026-09-09 16:27 PDT, claude) — **Deploy and test surface as found: no tests, no CI, no deploy script; the production host and URL are not in the repo.** OBS: tree = `server.py` (18 lines), `Dockerfile`, `docker-compose.yml`, `requirements.txt` (`mcp[cli]>=1.9.0`, `uvicorn`), `README.md`, `.gitignore`; README's smoke test is a hand-typed `curl` initialize call against `localhost:8222`. meshe (2026-09-09): "It's actually deployed on my oracle server (awarm)". LIT: the workstation vault (`Servers/Oracle awarm`, `Oracle services`) documents awarm as an Oracle Cloud VM running ~20 dockerized sites behind nginx-proxy-manager; the specific compose path and public hostname for this service are not recorded there or here (O-002). Consequence for a swarm here: deploy is a remote `docker compose up -d --build` on another host with no rollback script — a HELD deploy class by construction.

## Principles

## Open loops

| ID | Item | Gate | Opened |
|---|---|---|---|
| O-001 | DST bug (F-001): the server reports PDT year-round. Fix = `ZoneInfo("America/Vancouver")` + `%Z`, red-first test across a DST boundary, then a held deploy to awarm. | the first swarm run on this repo (swarm-builder T-6 step 4), deploy held for meshe | 2026-09-09 16:27 PDT |
| O-002 | Production location not recorded: compose path on awarm, public hostname behind nginx-proxy-manager, and how the workstation's MCP client reaches it. README shows `localhost:8222` only. | meshe (or the vault's `Oracle services` note) — record the path and hostname here or there, no credentials | 2026-09-09 16:27 PDT |
| O-003 | No tests and no CI (F-002). What the test tier is for an 18-line server: unit on the formatter, an in-process Streamable HTTP round-trip, or both. | the swarm's test-writer under the contract for O-001 | 2026-09-09 16:27 PDT |
| O-004 | Is this repo a dashboard KB source (`kb_*` MCP, wiki page)? Not asked at adoption; if yes, the log is reachable through `decision_get` once registered. | meshe | 2026-09-09 16:27 PDT |
