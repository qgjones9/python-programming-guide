# [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html)

The [`random`](https://docs.python.org/3/library/random.html) module implements **deterministic pseudo-random** generators (Mersenne Twister by default) for integers, sequence sampling, shuffling, and common statistical distributions. It is **not** suitable for cryptography — use the **`secrets`** module for security-sensitive tokens. Almost all module-level functions delegate to a hidden `random.Random` instance; you can create isolated **`Random`** or **`SystemRandom`** objects. Full distribution list and subclassing notes are on [docs.python.org](https://docs.python.org/3/library/random.html).

**Thread safety:** global generator and `Random` instances are thread-safe; free-threaded builds may see contention — prefer per-thread instances.

---

## Bookkeeping

| Function | Purpose |
|----------|---------|
| `random.seed(a=None, version=2)` | Reproducible sequences from int/str/bytes/`None` |
| `random.getstate()` / `setstate(state)` | Snapshot and restore generator state |
| `random.getrandbits(k)` | Integer with k random bits |

```python
# Goal: reproducible sequence via seed
import random

random.seed(31415, version=2)
first = [random.random() for _ in range(3)]
random.seed(31415, version=2)
second = [random.random() for _ in range(3)]
assert first == second
```

---

## Integers and sequences

| Function | Behavior |
|----------|----------|
| `randrange(start, stop[, step])` | Uniform from `range` — optimized for large spans |
| `randint(a, b)` | Inclusive both ends |
| `choice(seq)` | One uniform element |
| `choices(population, weights=…, k=n)` | Sampling **with** replacement |
| `sample(population, k)` | Unique sample **without** replacement |
| `shuffle(x)` | In-place permutation |

```python
# Goal: weighted draw and fixed-size sample without replacement
import random

random.seed(0)
bag = ["red", "green", "blue"]
draws = random.choices(bag, weights=[5, 2, 1], k=20)
assert all(color in bag for color in draws)
deck = list(range(52))
hand = random.sample(deck, k=5)
assert len(hand) == len(set(hand)) == 5
```

---

## Real-valued distributions

| Function | Distribution |
|----------|--------------|
| `random()` | Uniform [0.0, 1.0) |
| `uniform(a, b)` | Continuous uniform on [a, b] (endpoint rounding nuances) |
| `triangular(low, high, mode)` | Triangular |
| `gauss(mu, sigma)` / `normalvariate` | Normal (Gaussian) |
| `expovariate(lambd)` | Exponential |
| `betavariate(alpha, beta)` | Beta on [0, 1] |
| `gammavariate`, `lognormvariate`, `vonmisesvariate`, … | Other standard distributions |
| `binomialvariate(n, p)` | Binomial count (3.12+) |

```python
# Goal: simulate exponential waits with known mean
import random
import statistics

random.seed(99)
mean_target = 2.0
waits = [random.expovariate(1.0 / mean_target) for _ in range(5000)]
observed = statistics.fmean(waits)
assert 1.7 < observed < 2.3
```

---

## `Random` and `SystemRandom` classes

| Class | Use |
|-------|-----|
| `random.Random()` | Independent state; subclass to swap core algorithm |
| `random.SystemRandom()` | OS entropy via `os.urandom` — not MT; still not a secrets replacement |

```python
# Goal: isolated generator with deterministic local sequence
import random

local = random.Random(123)
seq_a = [local.random() for _ in range(3)]
local = random.Random(123)
seq_b = [local.random() for _ in range(3)]
assert seq_a == seq_b
assert all(0.0 <= x < 1.0 for x in seq_a)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| **`seed`** in unit tests and notebooks | Makes failures reproducible |
| Use **`sample`** for draws without replacement | `choices` allows duplicates |
| Pass **`counts=`** to `sample` for weighted decks | Cleaner than repeating elements |
| Instantiate **`Random()` per thread** in free-threaded apps | Reduces lock contention |
| Never use **`random`** for passwords or session IDs | Predictable PRNG |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `randrange(10.0)` | `TypeError` (3.12+) | Pass integers |
| `sample` larger than population | `ValueError` | Check sizes |
| `shuffle` on immutable sequence | `TypeError` | Use `sample(x, k=len(x))` |
| Permutation space vs MT period | Long sequences can't realize all permutations | Use crypto-grade shufflers if needed |
| `choices` vs repeated `choice` | Different algorithms / sequences | Pick one API per simulation design |
| Using `random` for crypto | Attackable tokens | Use `secrets` |
