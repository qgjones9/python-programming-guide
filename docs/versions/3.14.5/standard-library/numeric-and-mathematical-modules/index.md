# [Numeric and Mathematical Modules](https://docs.python.org/3/library/numeric.html)

Python’s standard library groups **numeric abstractions, floating-point math, exact decimal and rational arithmetic, pseudo-random sampling, and descriptive statistics** under **Numeric and Mathematical Modules**. The [`numbers`](numbers-numeric-abstract-base-classes/index.md) module defines the numeric tower ABCs; [`math`](math-mathematical-functions/index.md) and [`cmath`](cmath-mathematical-functions-for-complex-numbers/index.md) wrap C-level real and complex elementary functions; [`decimal`](decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md) and [`fractions`](fractions-rational-numbers/index.md) provide exact or rational alternatives to binary floats; [`random`](random-generate-pseudo-random-numbers/index.md) implements deterministic PRNGs for simulations; [`statistics`](statistics-mathematical-statistics-functions/index.md) covers calculator-grade descriptive stats. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/numeric.html); this hub orients you to each module and when to reach for it.

Related material outside this section: built-in [`int`](../built-in-types/index.md), [`float`](../built-in-types/index.md), and [`complex`](../built-in-types/index.md); array numerics in [`array`](../data-types/array-efficient-arrays-of-numeric-values/index.md); cryptographic randomness in [`secrets`](../cryptographic-services/secrets-generate-secure-random-numbers-for-managing-secrets/index.md) (if present) or the `secrets` module in the library index.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`numbers`](numbers-numeric-abstract-base-classes/index.md) | ABC hierarchy: `Number`, `Complex`, `Real`, `Rational`, `Integral` |
| [`math`](math-mathematical-functions/index.md) | Real-valued math: trig, logs, `isclose`, combinatorics, `fsum` |
| [`cmath`](cmath-mathematical-functions-for-complex-numbers/index.md) | Complex elementary functions and polar conversions |
| [`decimal`](decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md) | Correctly rounded decimal floating point with configurable context |
| [`fractions`](fractions-rational-numbers/index.md) | Exact rational numbers (`Fraction`) with reduced numerators/denominators |
| [`random`](random-generate-pseudo-random-numbers/index.md) | Pseudo-random integers, sampling, and statistical distributions |
| [`statistics`](statistics-mathematical-statistics-functions/index.md) | Mean, median, variance, correlation, regression on small datasets |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Type-check “is this numeric?” in APIs | [`numbers.Number`](numbers-numeric-abstract-base-classes/index.md) or narrower ABC |
| Fast trig/log on floats | [`math`](math-mathematical-functions/index.md) |
| Complex branch cuts, polar form | [`cmath`](cmath-mathematical-functions-for-complex-numbers/index.md) |
| Money, tax, or decimal equality invariants | [`decimal.Decimal`](decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md) |
| Exact rationals or recover float ratios | [`fractions.Fraction`](fractions-rational-numbers/index.md) |
| Shuffle, sample, or simulate distributions | [`random`](random-generate-pseudo-random-numbers/index.md) |
| Summary stats without NumPy | [`statistics`](statistics-mathematical-statistics-functions/index.md) |
| Cryptographic tokens or keys | **`secrets`**, not `random` |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Pick the **numeric type to match invariants** | Float speed vs decimal exactness vs rational exactness |
| Use **`math.isclose`** / **`cmath.isclose`** for float comparisons | Direct `==` fails on accumulated binary error |
| Construct **`Decimal` from strings**, not bare floats | `Decimal(3.14)` inherits binary float imprecision |
| **`random.seed`** or separate **`Random` instances** for reproducible tests | Global generator state is shared |
| Strip **`NaN`** before `statistics.median` and related order-sensitive APIs | NaN poisons sort order and results |
| Register custom numeric types on the **`numbers`** ABCs when implementing operators | Enables mixed-type dispatch via `NotImplemented` |

```python
# Goal: compare float vs decimal vs fraction exactness
import math
from decimal import Decimal
from fractions import Fraction

assert 0.1 + 0.2 != 0.3
assert not math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-17, abs_tol=0.0)
assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
assert Fraction(1, 3) + Fraction(1, 6) == Fraction(1, 2)
```

```python
# Goal: reproducible sampling and a descriptive statistic
import random
import statistics

random.seed(42)
rolls = [random.randint(1, 6) for _ in range(120)]
assert all(1 <= r <= 6 for r in rolls)
assert 1 <= statistics.mean(rolls) <= 6
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Using `random` for security | Predictable tokens | Use `secrets` or `SystemRandom` only where appropriate |
| `Fraction(1.1)` expecting `11/10` | Binary float ≠ decimal literal | Use `Fraction('1.1')`, `Decimal`, or `limit_denominator()` |
| Mixing `Decimal` and `float` with traps enabled | `FloatOperation` exception | Convert explicitly or disable trap |
| Calling `math.sqrt(-1)` | `ValueError` | Use `cmath.sqrt` for complex domain |
| Ignoring **signed zero** in `cmath` branch cuts | `-2-0j` vs `-2+0j` differ | Construct complex literals with explicit `0j` sign when needed |
| `statistics` on mixed-type data | Undefined behavior | Normalize with `map(float, data)` first |

---

## Sections in this repo

| Module | Notes |
|--------|-------|
| [numbers — Numeric abstract base classes](numbers-numeric-abstract-base-classes/index.md) | Numeric tower ABCs, operator dispatch patterns |
| [math — Mathematical functions](math-mathematical-functions/index.md) | Real functions, constants, combinatorics, summation |
| [cmath — Mathematical functions for complex numbers](cmath-mathematical-functions-for-complex-numbers/index.md) | Polar form, branch cuts, complex classification |
| [decimal — Decimal fixed-point and floating-point arithmetic](decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md) | Context, rounding, signals, `Decimal` construction |
| [fractions — Rational numbers](fractions-rational-numbers/index.md) | `Fraction`, `limit_denominator`, formatting |
| [random — Generate pseudo-random numbers](random-generate-pseudo-random-numbers/index.md) | PRNG, sampling, distributions, `Random` subclasses |
| [statistics — Mathematical statistics functions](statistics-mathematical-statistics-functions/index.md) | Central tendency, spread, correlation, regression |
