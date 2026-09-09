# Pinned contract — <build name>

*Copy per build. Pasted verbatim into every dispatch (core U-1). Shape per core §4.*

## 1. Surface

- Tool: `get_current_datetime_pdt` — docstring (verbatim, the whole surface):
  > …
- Output format (exact): `DayOfWeek Month DD, YYYY HH:MMam/pm TZ` — e.g. `…`
- Time source: `zoneinfo.ZoneInfo("America/Vancouver")`; abbreviation from `%Z`.
- Files: `server.py`; tests in `tests/unit/`, `tests/integration/`.

## 2. Rejections table

| input shape | status / behaviour | message or result |
|---|---|---|
| no arguments | OK | the formatted string |
| `{}` | OK | the formatted string |
| any unexpected argument | rejected by the MCP layer, never a 500 | validation error from FastMCP |

## 3. Definition of Done

- `python -m pytest -q` → `N passed`, N stated.
- `docker build` succeeds; the container answers `initialize` and `tools/call`.
- Docstring, README example and formatter agree.
- Verifier `VERDICT: PASS`; QA `VERDICT: CLEAN` if the surface changed.

## 4. HELD

Deploy to awarm; compose ports/networks; nginx-proxy-manager; secrets/env.

## 5. Ownership

| Track | Files |
|---|---|
| test-writer | `tests/unit/test_<x>.py`, `tests/integration/test_<y>.py` |
| datetime-engineer | `server.py`, `requirements-dev.txt`, `README.md`, `Dockerfile` (if needed) |
| orchestrator | `docs/decision-log.md`, commit |
