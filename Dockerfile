FROM python:3.13-slim

WORKDIR /app

# Fail the build on a base image whose tzdata predates IANA 2026b (F-004): without it
# America/Vancouver renders PST/UTC-08:00 for winter 2026 instead of the permanent
# MST/UTC-07:00 that BC moved to on 2026-11-01. Guards the base image, so it runs first.
RUN python -c "from datetime import datetime, timedelta; from zoneinfo import ZoneInfo; z = ZoneInfo('America/Vancouver'); d = datetime(2026, 12, 1, 12, 0, tzinfo=z); j = datetime(2026, 7, 1, 12, 0, tzinfo=z); assert d.tzname() == 'MST' and d.utcoffset() == timedelta(hours=-7), 'tzdata >= 2026b required: America/Vancouver 2026-12-01 12:00 rendered %s / %s, expected MST / -1 day, 17:00:00' % (d.tzname(), d.utcoffset()); assert j.tzname() == 'PDT' and j.utcoffset() == timedelta(hours=-7), 'tzdata >= 2026b required: America/Vancouver 2026-07-01 12:00 rendered %s / %s, expected PDT / -1 day, 17:00:00' % (j.tzname(), j.utcoffset())"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]
