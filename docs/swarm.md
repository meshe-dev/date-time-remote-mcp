# Swarm doctrine — date-time-remote-mcp

How multi-agent work runs in this repo. **The gate roles, playbooks, hooks and ledger are the
`swarm-core` plugin's** (`claude plugin list` → `swarm-core@swarm-builder`, source
`~/Code/swarm-builder/plugin/swarm-core`); the core rules (C-1…C-9, U-1…U-4, the contract
shape, gate-role method, playbooks, output contracts, deploy-class shape, observability) are
embedded verbatim in [`swarm-core.md`](swarm-core.md) at the installed version — read it,
then this page. Only the project section below is edited here; the embedded block is
regenerated. The one project agent lives in `.claude/agents/` (the engineer). No project
agent may reuse a plugin agent's bare name — a same-named project agent silently overrides
the plugin's (swarm-builder F-008). First generated 2026-09-09 (D-006); moved onto the
plugin 2026-09-10 (D-010); roster ratification is still O-005.

## Project section

### Stack and test tiers (derived from the repo)

- Python 3.13, FastMCP (`mcp[cli]>=1.9.0,<2` — D-007, O-007), uvicorn; one file, `server.py`;
  Streamable HTTP on container port 8000, host port 8222; Dockerfile + compose.
- **No tests existed at adoption (F-002).** The first contract created the tier:
  `pytest`, `tests/` at the repo root, `.venv/bin/python -m pytest -q` is the whole suite
  (create with `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r
  requirements-dev.txt`; `.venv` is gitignored; the host Python is 3.14, the image 3.13).
  Two tiers:
  - `tests/unit/` — the formatter as a pure function of a `datetime` (no clock, no network);
  - `tests/integration/` — the FastMCP server in-process: list tools, call the tool, assert
    the docstring and the returned string shape. No container, no host port.
- Dev dependency file: `requirements-dev.txt` (`pytest`). Runtime deps stay in
  `requirements.txt`.
- No environment canary (the suite runs in seconds); the verifier's canary step is skipped.

### Roles (this repo)

| Role | Model | Tools enforce | Job |
|---|---|---|---|
| **Orchestrator** | Fable, main loop (never a subagent) | — | Pins the contract, partitions, dispatches, commits on green; never deploys (HELD). |
| `swarm-core:swarm-test-writer` | Opus | **no Bash** | RED tests from the contract + Rejections table. Method: core §5; tiers above. |
| `datetime-engineer` (`.claude/agents/`) | Opus | full, inside its ownership list | The one implementer: `server.py`, `tests/` fixtures it is assigned, `requirements*.txt`, `Dockerfile`, `README.md`; docs in-dispatch. |
| `swarm-core:swarm-verifier` | Fable | **no Edit/Write** | Sole broad test executor; local proof; adversarial diff review; names the deploy class. Method: core §5; checklist below. |
| `swarm-core:swarm-qa` | Opus | **no Edit/Write** | Consumer view, no contract in hand. Method: core §5; checklist below. |
| `swarm-core:swarm-security` | Fable | **no Edit/Write** | Only when a diff touches the HELD list's secrets/env or network lines (none expected). |

Model assignment follows core C-5 (judgment = Fable, implementation = Opus). Tool grants are
the plugin's (mechanical, not prompt-only).

### Contracts

Template: [`contract-template.md`](contract-template.md). The Rejections table here means
inputs the tool must reject *or ignore* — FastMCP 1.x ignores unexpected arguments
(pydantic `extra=ignore`, D-007 row 3), so a row's intent is "never a server error", and the
test asserts the formatted string comes back.

### Single-writer resources

`server.py` · `requirements.txt` / `requirements-dev.txt` · `Dockerfile` ·
`docker-compose.yml` · `README.md` · `docs/decision-log.md` and `docs/contracts/*`
(orchestrator only — the plugin's E-1 hook denies subagent writes there).
With one engineer these never collide; the list exists so a second track can be added
without re-deriving it.

### Deploy classes (this repo)

- **Auto**: none. There is no local production; the service runs on awarm.
- **Held — every deploy.** Production is a container on the Oracle Cloud VM awarm behind
  nginx-proxy-manager (D-004), compose path `/home/ubuntu/date-time-remote-mcp` (F-005),
  deployed by `git pull && docker compose up -d --build` on that host; there is no rollback
  script. A build that changes `server.py`, the image, or compose lands on a branch with
  the exact commands stated and waits for meshe. Also held: port changes (D-003: 8000 is
  Portainer on the host), compose network changes (D-004).
- **Local proof instead of a live probe**: `docker build -t datetime-mcp .` succeeds;
  `docker run --rm -p 18222:8000 datetime-mcp` answers the README `initialize` curl and a
  `tools/call` for `get_current_datetime_pdt`; the verifier records both outputs. Stop the
  container before returning (zero background processes). Docker unavailable on the host is
  a finding in the verdict, never a silent skip.

### HELD list

Any deploy to awarm · port or network changes in compose · anything touching the host's
nginx-proxy-manager config · secrets/env (none exist today; keep it that way — D-001 is
no-auth by design).

### Checklists

**Verifier** (core method + these): contract conformance · time zone comes from
`zoneinfo` (`America/Vancouver`), never a hardcoded offset or literal abbreviation (F-001;
the abbreviation is whatever `ZoneInfo` returns for the datetime — D-009, `MST` from
2026-11-01 under tzdata 2026b, F-004) · the tool's docstring and the README example show the
full output format and agree with the formatter (core "show the whole surface") ·
`Dockerfile` still builds and the image answers `initialize` (local proof above) · no new
runtime dependency without a reason · tests not weakened · `requirements.txt` unchanged
unless the contract says so (the `<2` pin stays until O-007).

**QA** (no contract in hand): start the server in-process, list tools, call the tool with
no arguments, with an empty-object argument, twice in a row; read the string as a client
would — is the weekday right for the date, is the abbreviation right for today, is the
hour 12-hour with lowercase am/pm; call it at midnight, at 23:59 and on both sides of a
DST boundary by freezing the clock if the harness allows. Findings as pasted failing tests.

**Judgment bucket** (fix-it triage → `needs-meshe`, not code): anything altering D-001
(no auth), D-002 (human-readable format), D-009 (abbreviation from `ZoneInfo`), or the
tool name / client key (O-006).

### Blockers

Core C-9 binds: an unsatisfiable requirement is parked, the rest of the run continues, the
report leads with the blocker. The run never decides it (D-008 was the first-run violation;
D-009 is meshe's actual ruling). The plugin's E-2 and Stop hooks deny a D-entry attributed
to claude.

### Lanes

- **Build** — `/swarm-core:swarm-build <plan-or-contract file>` (core P-A). Interactive
  only; no watcher, no timer (a one-tool clock does not need a headless lane; revisit if
  issues accumulate). The bare `/swarm-build` is not a command here (swarm-builder F-015).
- **Fix** — `/swarm-core:fix-it <n>` (core P-C) against a GitHub issue on
  `meshe-dev/date-time-remote-mcp`; a described bug gets an issue first. In-flight label
  `swarm-working`; waiting labels `needs-meshe`, `needs-meshe-deploy`, `blocked`. Every
  deploy is HELD, so a green fix ends on a `fix/<n>` branch with the awarm commands in the
  terminal comment. Terminal comment ends with the cost footer.

### Push and merge

Commits on a feature branch; pushing the branch is allowed; merging to `main` and deploying
are meshe's (HELD). `main` is what awarm was built from.

### Cost footer

The plugin's ledger over this repo's session (one row per model, deduplicated per message):

```bash
python3 ~/.claude/plugins/cache/swarm-builder/swarm-core/0.1.1/bin/ledger.py \
  ~/.claude/projects/-home-meshe-Code-date-time-remote-mcp/<session>
```

Event ledger (zero-token, written by the plugin hooks):
`~/.claude/plugins/data/swarm-core-swarm-builder/ledger/<session>.jsonl`.
