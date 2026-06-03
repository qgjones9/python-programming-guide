# [math — Mathematical functions](https://docs.python.org/3/library/math.html)

The [`math`](https://docs.python.org/3/library/math.html) module wraps common **real-valued** C math functions: trigonometry, logarithms, special integer tools, and high-quality summation helpers. Arguments may be integers or floats; results are floats unless noted. **Complex numbers are not supported** — use [`cmath`](../cmath-mathematical-functions-for-complex-numbers/index.md) instead (`math.sqrt(-1)` raises). Full catalog and edge-case notes are on [docs.python.org](https://docs.python.org/3/library/math.html).

---

## Real vs complex

| Call | `math` | `cmath` |
|------|--------|---------|
| `sqrt(-1)` | `ValueError` | `1j` |
| `log(-1)` | `ValueError` | `πi` (principal branch) |
| `isclose(1+0j, 1)` | N/A (complex not accepted) | Supported |

Use `math` when domain errors should surface immediately; use `cmath` when the pipeline is inherently complex.

---

## Function categories

| Category | Functions |
|----------|-----------|
| Number-theoretic | `comb`, `perm`, `factorial`, `gcd`, `lcm`, `isqrt` |
| Rounding / parts | `ceil`, `floor`, `trunc`, `modf`, `fabs`, `fmod`, `remainder` |
| Float inspection | `isfinite`, `isinf`, `isnan`, `isclose`, `copysign`, `frexp`, `ldexp`, `nextafter`, `ulp` |
| Powers / logs | `sqrt`, `cbrt`, `pow`, `exp`, `exp2`, `expm1`, `log`, `log10`, `log2`, `log1p` |
| Aggregation | `fsum`, `dist`, `hypot`, `prod`, `sumprod` |
| Angles | `degrees`, `radians` |
| Trig / hyperbolic | `sin`, `cos`, `tan`, `asin`, …, `sinh`, `cosh`, `tanh`, … |
| Constants | `pi`, `e`, `tau`, `inf`, `nan` |

---

## Combinatorics and integer tools

```python
# Goal: choose committees and permutations with exact integers
import math

assert math.comb(10, 3) == 120
assert math.perm(5, 2) == 20
assert math.factorial(5) == 120
assert math.gcd(48, 180) == 12
assert math.lcm(12, 18) == 36
assert math.isqrt(10) == 3
```

---

## Stable summation and distance

`fsum` tracks lost low-order bits; prefer it over built-in `sum` for floats when precision matters. `hypot` and `dist` avoid undue overflow/underflow in Pythagorean formulas.

```python
# Goal: fsum reduces rounding error on many small terms
import math

values = [0.1, 0.2, 0.3, 0.4]
assert math.isclose(math.fsum(values), 1.0, rel_tol=1e-12)
assert math.hypot(3, 4) == 5.0
assert math.dist((0, 0), (3, 4)) == 5.0
```

---

## `isclose` — approximate equality

Same formula as [`cmath.isclose`](../cmath-mathematical-functions-for-complex-numbers/index.md): `abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)`. When comparing to zero, set a positive `abs_tol`.

```python
# Goal: compare floats after trig without exact equality
import math

a = math.sin(math.pi / 6)
assert math.isclose(a, 0.5)
assert math.isclose(1e-12, 0.0, abs_tol=1e-9)
assert not math.isclose(1.0, 1.0001, rel_tol=1e-6, abs_tol=0.0)
```

---

## Domain errors vs `cmath`

```python
# Goal: math guards real domain; cmath extends it
import math
import cmath

try:
    math.sqrt(-1)
    raised = False
except ValueError:
    raised = True
assert raised
assert cmath.sqrt(-1) == 1j
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`math.isclose`** instead of `==` on floats | Binary representation noise |
| Prefer **`fsum`** for long float accumulations | Reduces rounding error |
| Use **`hypot` / `dist`** for geometry | More stable than `sqrt(x*x + y*y)` |
| Keep **`math` for real-only APIs** | Surprises from complex results are avoided |
| Import constants **`math.pi`, `math.tau`** | Clearer than hard-coded literals |

---

## See also

- [`cmath` — complex mathematical functions](../cmath-mathematical-functions-for-complex-numbers/index.md)
- [`statistics` — statistics functions](../statistics-mathematical-statistics-functions/index.md)
- [Numeric and mathematical modules hub](../index.md)
- [PEP 485 — `isclose`](https://peps.python.org/pep-0485/)
