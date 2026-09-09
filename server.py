from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DateTime PDT", host="0.0.0.0", port=8000)

PACIFIC = ZoneInfo("America/Vancouver")


def format_pacific(dt: datetime) -> str:
    """Render a datetime in America/Vancouver as `DayOfWeek Month DD, YYYY HH:MMam/pm TZ`.

    Accepts aware datetimes or naive datetimes (treated as UTC). TZ is the
    zone's IANA abbreviation — `PDT`/`PST` historically, `MST` (permanent
    UTC-7) from 2026-11-01; am/pm are lowercase.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    local = dt.astimezone(PACIFIC)
    return local.strftime("%A %B %d, %Y %I:%M%p %Z").replace("AM", "am").replace("PM", "pm")


@mcp.tool()
def get_current_datetime_pdt() -> str:
    """Returns the current date and time in Pacific time (America/Vancouver), formatted as `DayOfWeek Month DD, YYYY HH:MMam/pm TZ`, where TZ is the zone's IANA abbreviation: `PDT`/`PST` while daylight saving was observed, `MST` (permanent UTC-7) from 2026-11-01. Example: `Saturday April 04, 2026 06:11pm PDT`."""
    return format_pacific(datetime.now(timezone.utc))


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
