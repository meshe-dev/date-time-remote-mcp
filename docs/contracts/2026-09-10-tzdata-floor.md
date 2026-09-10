# Pinned contract — tzdata floor assertion (issue #1, O-007 second half)

*Fix lane, core P-C. Pinned 2026-09-10 by the orchestrator from issue #1. Pasted verbatim
into every dispatch (U-1). No change to `server.py` and no change to the tool surface.*

## 1. Surface

The tool, its docstring and the output format are **unchanged**. What this build adds is a
guard on the environment the abbreviation comes from (D-009: the abbreviation is whatever
`ZoneInfo("America/Vancouver")` returns; F-004: that is `MST` from 2026-11-01 only under
IANA tzdata **2026b or newer**).

The assertion, stated once and implemented twice (test tier + image build):

| local datetime, `America/Vancouver` | `tzname()` | `utcoffset()` |
|---|---|---|
| `2026-12-01 12:00` | `MST` | `-1 day, 17:00:00` (UTC−07:00) |
| `2026-07-01 12:00` | `PDT` | `-1 day, 17:00:00` (UTC−07:00) |

A failure of either row means the running Python's tzdata predates 2026b. The failure
message must name the floor literally — the string `tzdata >= 2026b` — so a stale host or
a stale base image is diagnosable from the failure alone, with no lookup.

1. **`tests/integration/test_tzdata.py`** — asserts both rows against the tzdata the test
   run itself carries. Plus a self-check that the assertion actually detects a stale zone
   (perturbation, core §11): the same predicate applied to `America/Los_Angeles` — a zone
   that stays `PST`/UTC−08:00 in December 2026, exactly as pre-2026b Vancouver did — must
   fail. Without that, a guard that can never go red is indistinguishable from a guard that
   is always green.
2. **`Dockerfile`** — a build-time `RUN python -c …` carrying the same two rows, so an
   image built from a base whose Debian tzdata is older than 2026b **fails to build**
   instead of shipping `PST` for winter 2026.
3. **`README.md`** — one line under the run/deploy notes stating the floor.

## 2. Rejections table

Not applicable: no input shape changes. The tool takes no arguments and this build does not
touch `server.py` (issue #1, Scope: Out).

## 3. Definition of Done

- Whole suite: `.venv/bin/python -m pytest -q` → `N passed`, N stated.
- Red proven by perturbation, not by absence: the verifier shows the new assertion failing
  for a stale zone and passing for `America/Vancouver` under host tzdata 2026b.
- Local proof (project section): `docker build -t datetime-mcp .` succeeds — and, because
  the check is now in the build, its success *is* the image's tzdata floor evidence;
  `docker run --rm -p 18222:8000 datetime-mcp` answers the README `initialize` curl and a
  `tools/call` for `get_current_datetime_pdt`; container stopped before returning.
- Docs moved: README floor line. No docstring change (surface unchanged).
- Verifier `VERDICT: PASS`. QA **not** dispatched — no route and no tool surface changed.
  Security **not** dispatched — the diff touches no secrets, env or network line.

## 4. HELD

Every deploy (project section). This diff changes the `Dockerfile`, so it is HELD by two
rules at once. Also held: compose ports/networks, nginx-proxy-manager, secrets/env.
The run ends on branch `fix/1` with the awarm commands stated, never run.

## 5. Ownership

| Track | Files |
|---|---|
| `swarm-core:swarm-test-writer` | `tests/integration/test_tzdata.py` (new; the only file it may touch) |
| `datetime-engineer` | `Dockerfile`, `README.md` |
| orchestrator | `docs/decision-log.md`, `docs/contracts/*`, indexes, branch + commit |

Out of scope (issue #1): `server.py`, the O-006 rename, the O-007 mcp 2.x migration,
`requirements*.txt` (the `<2` pin stays — D-007).
