# [zoneinfo — IANA time zone support](https://docs.python.org/3/library/zoneinfo.html)

The [`zoneinfo`](https://docs.python.org/3/library/zoneinfo.html) module (3.9+) supplies [`ZoneInfo`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfo), a concrete [`datetime.tzinfo`](https://docs.python.org/3/library/datetime.html#datetime.tzinfo) backed by the **IANA time zone database**. Pair it with [`datetime`](datetime-basic-date-and-time-types/index.md) for DST-aware local times.

---

## Data sources

| Source | When used |
|--------|-----------|
| System TZ database | Default on POSIX/macOS when installed |
| [`tzdata`](https://pypi.org/project/tzdata/) PyPI package | Fallback; required on Windows for portable apps |
| `PYTHONTZPATH` / [`TZPATH`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.TZPATH) | Override search path |

If no database is found, [`ZoneInfo(key)`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfo) raises [`ZoneInfoNotFoundError`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfoNotFoundError).

---

## Key API

| Name | Role |
|------|------|
| `ZoneInfo("Area/City")` | Canonical constructor; instances are cached and identical per key |
| [`ZoneInfo.from_file(f)`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfo.from_file) | Load TZif bytes from a file object |
| [`ZoneInfo.no_cache(key)`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfo.no_cache) | Bypass instance cache (testing) |
| [`available_timezones()`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.available_timezones) | Set of valid keys on the current path |
| [`reset_tzpath()`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.reset_tzpath) | Runtime path configuration |

---

## DST and ambiguous times

During a **fall-back** transition, the same local clock time can map to two UTC offsets. Use the [`fold`](https://docs.python.org/3/library/datetime.html#datetime.datetime.fold) attribute: `fold=0` picks the first occurrence, `fold=1` the second. [`astimezone()`](https://docs.python.org/3/library/datetime.html#datetime.datetime.astimezone) sets `fold` correctly when converting from UTC.

---

## Best practices

- Declare a **`tzdata`** dependency for cross-platform apps; do not assume OS zone data exists.
- Store and exchange **UTC** (`datetime.timezone.utc`) in APIs; convert to `ZoneInfo` at display boundaries.
- Use **IANA keys** (`Europe/Berlin`), not fixed offsets, for recurring local times.
- [`ZoneInfo.key`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfo.key) is an identifier, not a user-facing label — use CLDR/locale data for UI strings.
- Pickle serializes by **key**; unpickling requires the same zone data on both ends.

---

## Example — attach zone and DST shift

```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

la = ZoneInfo("America/Los_Angeles")
when = datetime(2020, 10, 31, 12, tzinfo=la)
later = when + timedelta(days=1)
assert when.tzname() == "PDT"
assert later.tzname() == "PST"
assert later.utcoffset() != when.utcoffset()
```

---

## Example — `fold` on ambiguous local time

```python
from datetime import datetime
from zoneinfo import ZoneInfo

la = ZoneInfo("America/Los_Angeles")
first = datetime(2020, 11, 1, 1, 30, tzinfo=la, fold=0)
second = datetime(2020, 11, 1, 1, 30, tzinfo=la, fold=1)
assert first.utcoffset() != second.utcoffset()
assert str(first).endswith("-07:00")
assert str(second).endswith("-08:00")
```

---

## Example — UTC conversion sets fold

```python
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

la = ZoneInfo("America/Los_Angeles")
utc = datetime(2020, 11, 1, 8, tzinfo=timezone.utc)
before = utc.astimezone(la)
after = (utc + timedelta(hours=1)).astimezone(la)
assert before.fold == 0
assert after.fold == 1
assert before.hour == after.hour == 1
```

---

## See also

- [`datetime`](datetime-basic-date-and-time-types/index.md) — naive vs aware datetimes
- [`calendar`](calendar-general-calendar-related-functions/index.md) — calendar arithmetic without zones
