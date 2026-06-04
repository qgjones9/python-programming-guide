# [The Python Profilers](https://docs.python.org/3/library/profile.html)

Python ships two **deterministic profilers**: **`cProfile`** (C extension, recommended) and **`profile`** (pure Python reference). Both measure **per-function call counts and cumulative time**. Analyze output with **`pstats`**. Canonical reference: [profile.html](https://docs.python.org/3/library/profile.html).

---

## Purpose

Find **hot spots**—functions whose cumulative time dominates a workload. Profilers add overhead; use representative inputs and focus on `tottime` vs `cumtime` in reports.

---

## Module roles

| Module | Role |
|--------|------|
| `cProfile` | Fast profiler; same interface as `profile` |
| `profile` | Readable reference implementation |
| `pstats.Stats` | Sort, filter, and print statistics |
| `runpy.run` / `-m cProfile` | CLI profiling |

---

## Example — profile a function with cProfile

```python
import cProfile
import pstats
import io

def work(n):
    total = 0
    for i in range(n):
        total += i
    return total

profiler = cProfile.Profile()
profiler.enable()
result = work(5000)
profiler.disable()
assert result == sum(range(5000))

stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream)
stats.sort_stats("cumulative")
stats.print_stats(5)
report = stream.getvalue()
assert "work" in report
```

---

## Example — Stats sorting keys

```python
import cProfile
import pstats

def a():
    b()

def b():
    sum(range(1000))

prof = cProfile.Profile()
prof.runcall(a)
stats = pstats.Stats(prof)
stats.strip_dirs()
stats.sort_stats("tottime")
top = stats.get_stats_profile().func_profiles
assert len(top) >= 2
```

---

## Reading output

| Column | Meaning |
|--------|---------|
| `ncalls` | Number of calls |
| `tottime` | Time in function excluding subcalls |
| `cumtime` | Time including subcalls |
| `percall` | `tottime / ncalls` |

---

## CLI (interactive session)

```text
python -m cProfile -s cumulative myscript.py
```

---

## See also

- [`timeit`](../timeit-measure-execution-time-of-small-code-snippets/index.md) — micro-benchmarks
- [`trace`](../trace-trace-or-track-python-statement-execution/index.md) — line-level counts
