# [time — Time access and conversions](https://docs.python.org/3/library/time.html)

The [`time`](https://docs.python.org/3/library/time.html) module exposes **C-style time functions**: seconds since the epoch, struct tuples, formatting/parsing, and sleep. Use **`time.monotonic()`** or **`perf_counter()`** for intervals; **`time.time()`** for wall-clock timestamps. For timezone-aware datetimes prefer [`datetime`](../../data-types/datetime-basic-date-and-time-types/index.md). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/time.html).

Related: [`threading`](../../concurrent-execution/threading-thread-based-parallelism/index.md) `Event.wait`; [`asyncio`](../../networking-and-interprocess-communication/asyncio-asynchronous-io/index.md) for non-blocking delays; [`calendar`](../../data-types/calendar-general-calendar-related-functions/index.md) for calendar arithmetic.

---

## Clock functions — overview

| Function | Behavior | Use for |
|----------|----------|---------|
| `time.time()` | Wall clock (epoch seconds, float) | Log timestamps, cache TTL keys |
| `time.monotonic()` | Always increasing, not adjustable | Timeouts, watchdogs |
| `time.perf_counter()` | Highest-resolution interval timer | Benchmarks |
| `time.process_time()` | CPU time of current process | Profiling hot paths |
| `time.sleep(secs)` | Block at least `secs` seconds | Simple pacing (not for precise scheduling) |

---

## Conversions — [Time Conversion](https://docs.python.org/3/library/time.html)

| API | Role |
|-----|------|
| `time.gmtime([secs])` / `localtime([secs])` | UTC vs local `struct_time` |
| `time.mktime(t)` | Local struct → epoch seconds |
| `time.strftime(format, t)` / `strptime(string, format)` | Format and parse |
| `time.struct_time` | 9-field tuple: tm_year … tm_isdst |

```python
# Goal: format UTC time from epoch seconds
import time

t = time.gmtime(0)
assert time.strftime("%Y-%m-%d", t) == "1970-01-01"
```

```python
# Goal: monotonic interval measurement
import time

start = time.perf_counter()
total = sum(range(1000))
elapsed = time.perf_counter() - start
assert elapsed >= 0 and total == 499500
```

```python
# Goal: parse a fixed local datetime string
import time

parsed = time.strptime("2024-06-01", "%Y-%m-%d")
assert parsed.tm_year == 2024 and parsed.tm_mon == 6
```

---

## struct_time fields

| Index | Attribute | Meaning |
|-------|-----------|---------|
| 0 | `tm_year` | Full year |
| 1 | `tm_mon` | Month 1–12 |
| 2 | `tm_mday` | Day 1–31 |
| 3 | `tm_hour` | Hour 0–23 |
| 4 | `tm_min` | Minute 0–59 |
| 5 | `tm_sec` | Second 0–61 (leap) |
| 6 | `tm_wday` | Weekday 0–6 (Monday=0) |
| 7 | `tm_yday` | Day of year 1–366 |
| 8 | `tm_isdst` | DST flag (-1, 0, 1) |

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`monotonic()`** / **`perf_counter()`** for durations | Wall clock can jump backward or forward |
| Store **UTC epoch floats** or **ISO-8601 with offset** | Avoid naive local-time ambiguity |
| Prefer **`datetime`** for calendar math | `time` lacks timedelta richness |
| Avoid **`sleep` in tight loops** for scheduling | Drift accumulates; use timers or schedulers |
| Document **timezone** when using `localtime` | Results depend on system locale |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| **`time.time()`** for benchmarks | NTP adjustment skews deltas | Use `perf_counter()` |
| **`mktime` on UTC struct** | Off by timezone offset | Use `calendar.timegm` or datetime UTC |
| **`strftime` `%y` two-digit year** | Y2K-style ambiguity | Prefer `%Y` |
| **`sleep(0)`** yields GIL | Other threads may run; not instant | Expected — not a busy spin |
| Platform **`clock()`** removed (3.8+) | Old tutorials break | Use `perf_counter()` |
