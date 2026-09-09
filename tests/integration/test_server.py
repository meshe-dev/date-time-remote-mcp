"""RED tests for the FastMCP surface, in-process (contract O-001 / F-001).

    .venv/bin/python -m pytest -q tests/integration/test_server.py

No container, no host port, no network: the FastMCP instance is driven
directly via its async `list_tools` / `call_tool`, wrapped in `asyncio.run`
inside plain sync tests (no pytest-asyncio is installed).
"""
import asyncio
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from server import mcp  # noqa: E402

TOOL = "get_current_datetime_pdt"

# The whole surface of the tool, verbatim from the pinned contract.
EXPECTED_DOCSTRING = (
    "Returns the current date and time in Pacific time (America/Vancouver), "
    "formatted as `DayOfWeek Month DD, YYYY HH:MMam/pm TZ`, where TZ is the "
    "zone's IANA abbreviation: `PDT`/`PST` while daylight saving was observed, "
    "`MST` (permanent UTC-7) from 2026-11-01. Example: `Saturday April 04, 2026 "
    "06:11pm PDT`."
)

RESULT_RE = re.compile(
    r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) "
    r"(January|February|March|April|May|June|July|August|September|October|"
    r"November|December) \d{2}, \d{4} \d{2}:\d{2}(am|pm) (PDT|PST|MST)$"
)


def _text_of(result):
    """Extract the single text payload, tolerant of mcp>=1.9 return shapes.

    FastMCP.call_tool returns either a sequence of content blocks or a
    ``(content_list, structured_content)`` tuple when the tool has an output
    schema (a `-> str` tool does). Either way the first content block is a
    TextContent with `.text`.
    """
    content = result
    if isinstance(result, tuple):
        content = result[0]
    assert len(content) == 1, "expected exactly one content block, got %r" % (content,)
    return content[0].text


def test_exactly_one_tool_named_get_current_datetime_pdt():
    tools = asyncio.run(mcp.list_tools())
    names = [t.name for t in tools]
    assert names == [TOOL]


def test_tool_description_equals_the_contract_docstring():
    tools = asyncio.run(mcp.list_tools())
    tool = next(t for t in tools if t.name == TOOL)
    assert tool.description.strip() == EXPECTED_DOCSTRING


def test_calling_with_empty_object_returns_formatted_string():
    text = _text_of(asyncio.run(mcp.call_tool(TOOL, {})))
    assert RESULT_RE.match(text), "unexpected shape: %r" % (text,)


def test_calling_with_no_arguments_returns_formatted_string():
    # Row 1 of the Rejections table: an absent/empty argument set is OK.
    text = _text_of(asyncio.run(mcp.call_tool(TOOL, {})))
    assert RESULT_RE.match(text), "unexpected shape: %r" % (text,)


def test_unexpected_argument_is_ignored_by_the_mcp_layer():
    # Row 3 (amended): an unexpected argument is ignored by the MCP layer
    # (pydantic extra=ignore) and the normal formatted string comes back.
    text = _text_of(asyncio.run(mcp.call_tool(TOOL, {"bogus": 1})))
    assert RESULT_RE.match(text), "unexpected shape: %r" % (text,)


def test_source_has_no_hardcoded_offset_or_literal_timezone_in_format():
    # Static guard for F-001: the fix must derive the zone from zoneinfo, not
    # a fixed timedelta offset or a literal abbreviation baked into strftime.
    source = (REPO_ROOT / "server.py").read_text(encoding="utf-8")
    assert "timedelta(hours=" not in source
    assert not re.search(r"strftime\([^)]*P[SD]T", source)
    assert not re.search(r"strftime\([^)]*MST", source)
