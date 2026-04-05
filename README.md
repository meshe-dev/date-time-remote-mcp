# DateTime PDT - Remote MCP Server

A remote [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that returns the current date and time in Pacific Daylight Time (PDT). No authentication required.

## Tool

### `get_current_datetime_pdt`

Returns the current date and time formatted as `DayOfWeek Month DD, YYYY HH:MMam/pm PDT`.

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

Verify the server is running with curl:

```bash
# Initialize a session
curl -X POST http://localhost:8222/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

## Project Structure

```
.
├── server.py            # MCP server with the datetime tool
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Docker Compose configuration
└── README.md
```

## Tech Stack

- Python 3.13
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (FastMCP)
- Uvicorn (ASGI server)
- Docker
