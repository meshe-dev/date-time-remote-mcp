# Swarm doctrine — date-time-remote-mcp

How multi-agent work runs in this repo. Agents live in `.claude/agents/`, playbooks in
`.claude/commands/`. **This page is the canon every agent reads first; agent files are thin
wiring.** The core rules (C-1…C-8, U-1…U-4, the contract shape, gate-role method, playbooks,
output contracts, deploy-class shape, observability) are the swarm core doctrine, embedded
verbatim in [`swarm-core.md`](swarm-core.md) — read it, then this page. Only the project
section below is edited here. Hand-generated 2026-09-09 as swarm-builder exploration 03
T-6 pass 1 (that repo's D-005); not yet ratified by meshe (this repo's D-006 records the
adoption, O-005 the ratification).

## Project section

### Stack and test tiers (derived from the repo)

- Python 3.13, FastMCP (`mcp[cli]>=1.9.0`), uvicorn; one file, `server.py`; Streamable HTTP
  on container port 8000, host port 8222; Dockerfile + compose.
- **No tests existed at adoption (F-002).** The first contract creates the tier:
  `pytest`, `tests/` at the repo root, `.venv/bin/python -m pytest -q` is the whole suite (create with `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt`; `.venv` is gitignored; the host Python is 3.14, the image 3.13). Two tiers:
  - `tests/unit/` — the formatter as a pure function of a `datetime` (no clock, no network);
  - `tests/integration/` — the FastMCP server in-process: list tools, call the tool, assert
    the docstring and the returned string shape. No container, no host port.
- Dev dependency file: `requirements-dev.txt` (`pytest`). Runtime deps stay in
  `requirements.txt`.

### Roles (this repo)

| Role | Model | Tools enforce | Job |
|---|---|---|---|
| **Orchestrator** | Fable, main loop (never a subagent) | — | Pins the contract, partitions, dispatches, commits on green; never deploys (HELD). |
| `swarm-test-writer` | Opus | **no Bash** | RED tests from the contract + Rejections table; cannot run them. |
| `datetime-engineer` | Opus | full, inside its ownership list | The one implementer: `server.py`, `tests/` fixtures it is assigned, `requirements*.txt`, `Dockerfile`, `README.md`; docs in-dispatch. |
| `swarm-verifier` | Fable | **no Edit/Write** | Sole broad test executor; adversarial diff review; names the deploy class. |
| `swarm-qa` | Opus | **no Edit/Write** | Consumer view: calls the tool the way a Claude session would, with no contract in hand. |

Model assignment follows core C-5 (judgment = Fable, implementation = Opus). Gate roles are
the core method; their checklists are below.

### Single-writer resources

`server.py` · `requirements.txt` / `requirements-dev.txt` · `Dockerfile` ·
`docker-compose.yml` · `README.md` · `docs/decision-log.md` (orchestrator only).
With one engineer these never collide; the list exists so a second track can be added
without re-deriving it.

### Deploy classes (this repo)

- **Auto**: none. There is no local production; the service runs on awarm.
- **Held — every deploy.** Production is a container on the Oracle Cloud VM awarm behind
  nginx-proxy-manager (D-004), deployed by `docker compose up -d --build` on that host; the
  compose path and public hostname are not recorded (O-002) and there is no rollback
  script. A build that changes `server.py`, the image, or compose lands on a branch with
  the exact commands stated and waits for meshe. Also held: port changes (D-003: 8000 is
  Portainer on the host), compose network changes (D-004).
- **Local proof instead of a live probe**: `docker build -t datetime-mcp .` succeeds;
  `docker run --rm -p 18222:8000 datetime-mcp` answers the README `initialize` curl and a
  `tools/call` for `get_current_datetime_pdt`; the verifier records both outputs. Stop the
  container before returning (zero background processes).

### HELD list

Any deploy to awarm · port or network changes in compose · anything touching the host's
nginx-proxy-manager config · secrets/env (none exist today; keep it that way — D-001 is
no-auth by design).

### Checklists

**Verifier** (core method + these): contract conformance · time zone comes from
`zoneinfo` (`America/Vancouver`), never a hardcoded offset or literal abbreviation (F-001)
· the tool's docstring and the README example show the full output format and agree with
the formatter (core "show the whole surface") · `Dockerfile` still builds and the image
answers `initialize` · no new runtime dependency without a reason · tests not weakened ·
`requirements.txt` unchanged unless the contract says so.

**QA** (no contract in hand): start the server in-process, list tools, call the tool with
no arguments, with an empty-object argument, twice in a row; read the string as a client
would — is the weekday right for the date, is the abbreviation right for today, is the
hour 12-hour with am/pm; call it around midnight and around a DST boundary by freezing the
clock if the harness allows. Findings as pasted failing tests.

### Lanes

- **Build** — `/swarm-build <plan-or-contract file>`. Interactive only; no watcher, no
  timer (a one-tool clock does not need a headless lane; revisit if issues accumulate).
- **Fix** — `/fix-it <n>` against a GitHub issue on `meshe-dev/date-time-remote-mcp`; a
  described bug gets an issue first. Terminal comment ends with the cost footer.

### Push and merge

Commits on a feature branch; pushing the branch is allowed; merging to `main` and deploying
are meshe's (HELD). `main` is what awarm was built from.

### Cost footer

Until the shared ledger exists, the footer is the dashboard's pricer run over this repo's
transcripts: `python3 ~/Code/dashboard/dashboard/jobs/issue_cost.py --file
~/.claude/projects/-home-meshe-Code-date-time-remote-mcp/<session>.jsonl` (read-only use
of another repo's tool; replace when swarm-builder ships its own).
