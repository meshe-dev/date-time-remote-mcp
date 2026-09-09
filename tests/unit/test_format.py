"""RED tests for the pure formatter `format_pacific` (contract O-001 / F-001).

    .venv/bin/python -m pytest -q tests/unit/test_format.py

The formatter converts any datetime to America/Vancouver and renders
`DayOfWeek Month DD, YYYY HH:MMam/pm TZ`, where TZ is the zone's IANA
abbreviation (`PDT`/`PST` historically, `MST` permanent UTC-7 from
2026-11-01 per D-008). No clock is read: every case pins a fixed UTC datetime.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from server import format_pacific  # noqa: E402 — missing symbol today is the RED reason


def _utc(year, month, day, hour, minute):
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


def test_summer_utc_renders_pdt():
    assert format_pacific(_utc(2026, 7, 1, 19, 11)) == "Wednesday July 01, 2026 12:11pm PDT"


def test_winter_utc_renders_mst():
    # tzdata 2026b: America/Vancouver is permanent UTC-7 labelled MST from 2026-11-01 (D-008).
    assert format_pacific(_utc(2026, 12, 1, 20, 11)) == "Tuesday December 01, 2026 01:11pm MST"


def test_just_before_spring_forward_is_pst():
    # 2026 spring-forward is 02:00 PST (10:00 UTC) on Mar 08; 09:59 UTC is still PST.
    assert format_pacific(_utc(2026, 3, 8, 9, 59)).endswith(" PST")


def test_just_after_spring_forward_is_pdt():
    assert format_pacific(_utc(2026, 3, 8, 10, 1)).endswith(" PDT")


def test_just_before_fall_back_is_pdt():
    # 2026 fall-back is 02:00 PDT (09:00 UTC) on Nov 01; 08:30 UTC is still PDT.
    assert format_pacific(_utc(2026, 11, 1, 8, 30)).endswith(" PDT")


def test_just_after_fall_back_is_mst():
    # After 2026-11-01 the zone stays UTC-7 permanently, labelled MST (D-008).
    assert format_pacific(_utc(2026, 11, 1, 9, 30)).endswith(" MST")


def test_local_midnight_renders_twelve_am():
    # 07:00 UTC = 00:00 PDT on 2026-07-01.
    assert format_pacific(_utc(2026, 7, 1, 7, 0)) == "Wednesday July 01, 2026 12:00am PDT"


def test_local_noon_renders_twelve_pm():
    # 19:00 UTC = 12:00 PDT on 2026-07-01.
    assert format_pacific(_utc(2026, 7, 1, 19, 0)) == "Wednesday July 01, 2026 12:00pm PDT"


def test_local_midnight_in_winter_renders_twelve_am_mst():
    # 07:00 UTC = 00:00 MST on 2026-12-01 (permanent UTC-7, D-008).
    assert format_pacific(_utc(2026, 12, 1, 7, 0)) == "Tuesday December 01, 2026 12:00am MST"


def test_summer_after_permanent_switch_stays_mst():
    # 2027-07-01: no return to PDT — permanent UTC-7 / MST. 19:00 UTC = 12:00 MST.
    assert format_pacific(_utc(2027, 7, 1, 19, 0)) == "Thursday July 01, 2027 12:00pm MST"


def test_meridiem_is_lowercase_never_uppercase():
    out = format_pacific(_utc(2026, 7, 1, 19, 11))
    assert "am" in out or "pm" in out
    assert "AM" not in out and "PM" not in out


def test_naive_datetime_is_treated_as_utc():
    naive = datetime(2026, 7, 1, 19, 11)
    assert format_pacific(naive) == "Wednesday July 01, 2026 12:11pm PDT"
