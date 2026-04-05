from datetime import datetime, timezone, timedelta

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DateTime PDT", host="0.0.0.0", port=8000)

PDT = timezone(timedelta(hours=-7))


@mcp.tool()
def get_current_datetime_pdt() -> str:
    """Returns the current date and time in PDT (Pacific Daylight Time)."""
    now = datetime.now(PDT)
    return now.strftime("%Y-%m-%d %H:%M:%S PDT")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
