# [timeit — Measure execution time of small code snippets](https://docs.python.org/3/library/timeit.html)

`timeit` times **small code snippets** with high precision by disabling GC (optionally), picking sensible repeat counts, and reporting the minimum elapsed time. Ideal for micro-benchmarks comparing algorithms. Canonical reference: [timeit.html](https://docs.python.org/3/library/timeit.html).

---

## Purpose

Wall-clock timing with `time.perf_counter()` alone is noisy. `timeit.timeit()` runs the snippet many times and returns total seconds; divide by `number` for per-iteration estimates.

---

## Key API

| Function / class | Role |
|------------------|------|
| `timeit.timeit(stmt, setup, number, ...)` | Total seconds for `number` executions |
| `timeit.repeat(..., repeat, number)` | List of `repeat` timings |
| `timeit.Timer` | Object-oriented interface |
| `timeit.default_timer` | Usually `time.perf_counter` |

---

## Example — compare two approaches

```python
import timeit

list_time = timeit.timeit("sum([i for i in range(100)])", number=10000)
gen_time = timeit.timeit("sum(i for i in range(100))", number=10000)
assert list_time > 0 and gen_time > 0
```

---

## Example — setup code and globals

```python
import timeit

setup = "data = list(range(500))"
stmt = "sum(data)"
elapsed = timeit.timeit(stmt, setup=setup, number=5000)
assert elapsed > 0
```

---

## Example — Timer with repeat

```python
import timeit

timer = timeit.Timer("x = 1 + 2")
samples = timer.repeat(repeat=3, number=100000)
assert len(samples) == 3
assert min(samples) <= max(samples)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`min` of `repeat`** | Reduces OS noise impact |
| Keep **`setup` one-time work** | Only `stmt` should be measured |
| Disable GC only when needed | `timeit` can pass `gc.disable()` internally |
| Benchmark **realistic data sizes** | Micro-results do not always scale |

---

## See also

- [`cProfile`](../the-python-profilers/index.md) — function-level profiling
- [`statistics`](https://docs.python.org/3/library/statistics.html) — analyze repeat samples
