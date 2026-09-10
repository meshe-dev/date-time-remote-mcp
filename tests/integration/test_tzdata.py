"""RED tests for the tzdata 2026b floor (issue #1, O-007 second half; contract
2026-09-10-tzdata-floor).

    .venv/bin/python -m pytest -q tests/integration/test_tzdata.py

Behavioural, not a version string: the abbreviation and offset come from
`ZoneInfo("America/Vancouver")` itself (D-009), so this holds whether the data
is the OS `/usr/share/zoneinfo` or the PyPI `tzdata` package. `server.py` is not
imported — this tier tests the environment the tool's abbreviation comes from,
not the module. The same one predicate is used for the real assertion and for
the perturbation self-check (core §11), which is what makes the guard provably
able to go red.

Contract rows (local wall-clock in America/Vancouver):

    | 2026-12-01 12:00 | MST | UTC-07:00 (timedelta(hours=-7)) |
    | 2026-07-01 12:00 | PDT | UTC-07:00 (timedelta(hours=-7)) |

A failure of either row means the running Python's tzdata predates 2026b; the
message names the floor literally (`tzdata >= 2026b`) so a stale host or a stale
base image is diagnosable from the failure alone.
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

# Both contract rows: (local wall-clock datetime, expected tzname, expected utcoffset).
# Both offsets are UTC-7 — December is permanent standard MST, July is daylight PDT.
FLOOR = "tzdata >= 2026b"
ROWS = (
    (datetime(2026, 12, 1, 12, 0), "MST", timedelta(hours=-7)),
    (datetime(2026, 7, 1, 12, 0), "PDT", timedelta(hours=-7)),
)


def assert_pacific_tzdata_floor(zone_key):
    """Assert both contract rows against `zone_key`, raising AssertionError with a
    message naming `tzdata >= 2026b` (and the observed value) on the first miss.

    The expected values are the America/Vancouver ones regardless of the zone
    passed, so the same predicate is the real guard and the perturbation probe.
    """
    zone = ZoneInfo(zone_key)
    for local, expected_abbr, expected_offset in ROWS:
        dt = local.replace(tzinfo=zone)
        actual_abbr = dt.tzname()
        actual_offset = dt.utcoffset()
        assert actual_abbr == expected_abbr, (
            "%s: %s at %s rendered tzname %r, expected %r"
            % (FLOOR, zone_key, local, actual_abbr, expected_abbr)
        )
        assert actual_offset == expected_offset, (
            "%s: %s at %s rendered utcoffset %s, expected %s"
            % (FLOOR, zone_key, local, actual_offset, expected_offset)
        )


def test_host_tzdata_meets_the_2026b_floor_for_vancouver():
    # Green under host tzdata 2026b+; red (AssertionError naming the floor) on a
    # stale host, which renders Vancouver December 2026 as PST / UTC-08:00.
    assert_pacific_tzdata_floor("America/Vancouver")


def test_perturbation_a_stale_shaped_zone_is_caught():
    # America/Los_Angeles stays PST / UTC-08:00 in December 2026 — exactly as
    # pre-2026b Vancouver did — so it is the stand-in for stale data: applying the
    # Vancouver predicate to it must raise, proving the guard can go red.
    with pytest.raises(AssertionError) as excinfo:
        assert_pacific_tzdata_floor("America/Los_Angeles")
    message = str(excinfo.value)
    assert FLOOR in message
    # The message reports what the stale-shaped zone actually rendered.
    assert "PST" in message
