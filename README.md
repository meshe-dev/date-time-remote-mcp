# DateTime PDT - Remote MCP Server

A remote [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that returns the current date and time in Pacific time (`America/Vancouver`) with the zone's live IANA abbreviation (`PDT`/`PST`, or `MST` under BC's permanent UTC-7). No authentication required.

## Tool

### `get_current_datetime_pdt`

Returns the current date and time in Pacific time (`America/Vancouver`), formatted as `DayOfWeek Month DD, YYYY HH:MMam/pm TZ`, where `TZ` is the zone's IANA abbreviation — `PDT`/`PST` historically, and `MST` (permanent UTC-7) from 2026-11-01 per BC's move to permanent daylight time.

**Example response:**

```
Saturday April 04, 2026 06:11pm PDT
```

## Quick Start

### Docker Compose (recommended)

```bash
docker compose up -d
```

### Docker

```bash
docker build -t datetime-mcp .
docker run -d -p 8222:8000 datetime-mcp
```

### Local

```bash
pip install -r requirements.txt
python server.py
```

The server starts on `http://localhost:8222` using the Streamable HTTP transport.

## MCP Client Configuration

### Claude Code

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "datetime-pdt": {
      "type": "streamable-http",
      "url": "http://localhost:8222/mcp"
    }
  }
}
```

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "datetime-pdt": {
      "type": "streamable-http",
      "url": "http://localhost:8222/mcp"
    }
  }
}
```

### Cursor / Windsurf / Other MCP Clients

Point your client to the Streamable HTTP endpoint:

```
http://localhost:8222/mcp
```

## Testing

Run the test suite with pytest in a virtualenv:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

`tests/unit/` covers the pure formatter against fixed datetimes (no clock);
`tests/integration/` drives the FastMCP server in-process (no container, no network).

Verify a running server with curl:

```bash
# Initialize a session
curl -X POST http://localhost:8222/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

## Project record

Start at [docs/Home.md](docs/Home.md) for the record: the decision log (D / F / P / O), explorations, and the working agreement.

## Project Structure

```
.
├── server.py            # MCP server + the pure formatter
├── requirements.txt     # Runtime dependencies
├── requirements-dev.txt # Test dependencies (pytest)
├── tests/               # unit/ (formatter) + integration/ (FastMCP in-process)
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Docker Compose configuration
└── README.md
```

## Tech Stack

- Python 3.13
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (FastMCP)
- Uvicorn (ASGI server)
- Docker
