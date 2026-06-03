# [calendar — General calendar-related functions](https://docs.python.org/3/library/calendar.html)

The [`calendar`](https://docs.python.org/3/library/calendar.html) module formats month and year calendars (like Unix `cal`), computes weekday/leap-year facts, and iterates weeks spanning month boundaries. It uses the **proleptic Gregorian** calendar (ISO 8601 year 0 = 1 BC). By default **Monday** is the first weekday; call `setfirstweekday(calendar.SUNDAY)` for US-style weeks. Full HTML/text formatters and locale hooks are on [docs.python.org](https://docs.python.org/3/library/calendar.html).

---

## Module constants

| Name | Value | Meaning |
|------|-------|---------|
| `MONDAY` … `SUNDAY` | 0–6 | Weekday indices |
| `JANUARY` … `DECEMBER` | 1–12 | Month numbers |
| `month_name` | sequence | Full English month names |
| `month_abbr` | sequence | Abbreviated month names |
| `day_name` | sequence | Full weekday names |
| `day_abbr` | sequence | Abbreviated weekday names |

---

## Key functions

| Function | Returns |
|----------|---------|
| `isleap(year)` | `True` if Gregorian leap year |
| `weekday(year, month, day)` | Weekday index for a date |
| `monthrange(year, month)` | `(weekday_of_first, num_days)` |
| `monthcalendar(year, month)` | Matrix of week rows (0 = outside month) |
| `timegm(tuple)` | UTC epoch seconds from struct_time-like tuple |
| `calendar(year, w=2, l=1, c=6, m=3)` | Multi-column year string |
| `month(year, month, w=2, l=1)` | Single month string |

```python
# Goal: leap check and days-in-month for scheduling
import calendar

assert calendar.isleap(2024)
assert calendar.isleap(1900) is False
first_weekday, ndays = calendar.monthrange(2024, 2)
assert ndays == 29
assert first_weekday == calendar.THURSDAY
```

```python
# Goal: iterate all dates in a month including padding weeks
import calendar
import datetime as dt

year, month = 2024, 6
dates = [d for d in calendar.Calendar().itermonthdates(year, month) if d.month == month]
assert dates[0].weekday() == calendar.SATURDAY  # 2024-06-01
assert len(dates) == 30
assert isinstance(dates[0], dt.date)
```

---

## Calendar classes — [Calendar Objects](https://docs.python.org/3/library/calendar.html#calendar-objects)

| Class | Output |
|-------|--------|
| `Calendar` | Raw date/week iterators and week matrices |
| `TextCalendar` | `formatmonth`, `formatyear` plain text |
| `HTMLCalendar` | `<table>` month/year markup |
| `LocaleTextCalendar` / `LocaleHTMLCalendar` | Locale-aware headers |

Subclass `Calendar` when you need custom formatting pipelines; the base class prepares data only.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use `monthrange` before allocating day slots | Avoid off-by-one in UI grids |
| Call `setfirstweekday` once at app startup | Global setting affects all formatters |
| Prefer `datetime.date` from `itermonthdates` | Easier arithmetic than raw day numbers |
| Use `timegm` only for **UTC** struct tuples | Local `mktime` lives in `time` module |
| Pair with **`datetime`** for timestamps | `calendar` does not attach time-of-day |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| ISO week-year vs calendar year | Week 1 can belong to adjacent year | Use `datetime.isocalendar()` for ISO weeks |
| Negative years in UI | Year 0 = 1 BC per ISO | Document proleptic convention |
| Assuming Sunday-first without setting | European Monday default | `setfirstweekday(calendar.SUNDAY)` |
| `monthcalendar` zeros | Days outside month show as `0` | Filter or use `itermonthdates` |

---

## See also

- [`datetime`](../datetime-basic-date-and-time-types/index.md) — `date` arithmetic
- [`zoneinfo`](../zoneinfo-iana-time-zone-support/index.md) — not needed for pure calendar grids
