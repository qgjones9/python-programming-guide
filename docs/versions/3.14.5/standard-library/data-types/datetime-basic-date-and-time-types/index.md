# [datetime — Basic date and time types](https://docs.python.org/3/library/datetime.html)

The [`datetime`](https://docs.python.org/3/library/datetime.html) module supplies immutable types for **dates**, **times**, **datetimes**, **durations**, and simple **UTC offsets**. Full reference: [docs.python.org](https://docs.python.org/3/library/datetime.html). For IANA zones, pair with [`zoneinfo`](zoneinfo-iana-time-zone-support/index.md).

---

## Core types

| Class | Represents | Key attributes |
|-------|------------|----------------|
| `date` | Calendar date (naive) | `year`, `month`, `day` |
| `time` | Time of day | `hour`, `minute`, `second`, `microsecond`, `tzinfo` |
| `datetime` | Date + time | All of the above combined |
| `timedelta` | Duration between two dates/times | `days`, `seconds`, `microseconds` |
| `tzinfo` | Abstract time zone info | Subclass for custom zones |
| `timezone` | Fixed UTC offset | `timezone.utc`, `datetime.UTC` (3.11+) |

All instances are **immutable** and **hashable** (when `tzinfo` is fixed or None consistently).

---

## Aware vs naive

| Kind | `tzinfo` | Can compare unambiguously across zones? |
|------|----------|----------------------------------------|
| **Naive** | `None` | No — interpretation is application-defined |
| **Aware** | Non-None `tzinfo` | Yes — represents an absolute instant |

An object is **aware** when `dt.tzinfo is not None` and `dt.tzinfo.utcoffset(dt) is not None`. Store and exchange timestamps as **aware UTC** internally; convert to local zones only for display.

---

## Common operations

| Task | Approach |
|------|----------|
| Parse ISO strings | `datetime.fromisoformat("2024-06-15T14:30:00")` |
| Format output | `dt.isoformat()`, `strftime(format)` |
| Add duration | `dt + timedelta(days=1)` |
| Difference | `dt2 - dt1` → `timedelta` |
| UTC now | `datetime.now(datetime.UTC)` (3.11+) |
| Replace fields | `dt.replace(hour=0, minute=0, second=0, microsecond=0)` |

Constants: `MINYEAR` = 1, `MAXYEAR` = 9999.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`datetime.now(datetime.UTC)`** for timestamps | Avoid naive local-time ambiguity |
| Never compare **aware and naive** datetimes | Raises `TypeError` in 3.x |
| Use **`zoneinfo.ZoneInfo`** for real-world zones | `timezone` only handles fixed offsets |
| Prefer **`fromisoformat`** over ad-hoc parsing | Handles many ISO 8601 forms natively |
| Normalize to UTC before **storing in databases** | Simplifies sorting and arithmetic |
| Use **`timedelta`**, not integer seconds, for calendar math gaps | Months/years need `date`/`relativedelta`, not plain deltas |

---

## Example — date construction and weekday

```python
from datetime import date

d = date(2024, 6, 15)
assert d.year == 2024
assert d.isoweekday() == 6  # Saturday
assert d.isoformat() == "2024-06-15"
```

---

## Example — timedelta arithmetic

```python
from datetime import date, timedelta

start = date(2024, 1, 1)
end = start + timedelta(days=31)
assert end == date(2024, 2, 1)
assert (end - start).days == 31
```

---

## Example — aware UTC datetime

```python
from datetime import datetime, timezone

utc = datetime(2024, 6, 15, 12, 0, tzinfo=timezone.utc)
assert utc.tzinfo is timezone.utc
assert utc.isoformat().endswith("+00:00")
now = datetime.now(timezone.utc)
assert now.tzinfo is not None
```

---

## Example — fromisoformat round-trip

```python
from datetime import datetime

text = "2024-06-15T14:30:00.123456"
dt = datetime.fromisoformat(text)
assert dt.isoformat() == text
```

---

## See also

- [`zoneinfo`](zoneinfo-iana-time-zone-support/index.md) — IANA time zone database
- [`calendar`](calendar-general-calendar-related-functions/index.md) — month grids and weekday helpers
- [`time`](https://docs.python.org/3/library/time.html) — epoch seconds and `struct_time`
