# [cmath — Mathematical functions for complex numbers](https://docs.python.org/3/library/cmath.html)

The [`cmath`](https://docs.python.org/3/library/cmath.html) module mirrors [`math`](../math-mathematical-functions/index.md) for **complex numbers**: exponentials, logarithms, trig, hyperbolic functions, polar conversions, and classification helpers. Every function accepts int, float, or complex (or objects with `__complex__` / `__float__`) and **returns a complex number**, even when the mathematical result is purely real. Branch-cut conventions follow C99 / Kahan — signed zero distinguishes sides of cuts. Full API and cut diagrams are on [docs.python.org](https://docs.python.org/3/library/cmath.html).

---

## Polar and rectangular form

| Function | Role |
|----------|------|
| `cmath.phase(z)` | Argument (angle) in radians, range (−π, π] |
| `cmath.polar(z)` | Pair `(abs(z), phase(z))` |
| `cmath.rect(r, phi)` | Complex from modulus r and phase phi |
| Built-in `abs(z)` | Modulus (no separate `cmath` function) |

```python
# Goal: round-trip polar coordinates
import cmath
import math

z = complex(3, 4)
r, phi = cmath.polar(z)
back = cmath.rect(r, phi)
assert math.isclose(back.real, z.real) and math.isclose(back.imag, z.imag)
assert r == 5.0
```

---

## Powers and logarithms

| Function | Branch-cut note |
|----------|-----------------|
| `cmath.exp(z)` | Entire function — no cut |
| `cmath.log(z[, base])` | Cut along negative real axis from 0 |
| `cmath.log10(z)` | Same cut as `log` |
| `cmath.sqrt(z)` | Cut along negative real axis; sign of `imag` matters |

```python
# Goal: sqrt and log extend to negative reals on the principal branch
import cmath

assert cmath.sqrt(-1) == 1j
assert cmath.sqrt(-4) == 2j
assert cmath.log(-1 + 0j).imag > 0  # principal log: πi
# Signed zero can flip the side of cuts (see upstream docs); test platform behavior explicitly if needed.
```

---

## Trigonometric and hyperbolic families

| Family | Functions |
|--------|-----------|
| Trig | `sin`, `cos`, `tan`, `asin`, `acos`, `atan` |
| Hyperbolic | `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, `atanh` |

These extend real functions analytically; cuts differ per function (see upstream docs for each).

```python
# Goal: Euler identity and hyperbolic relation
import cmath
import math

identity = cmath.exp(1j * cmath.pi) + 1
assert cmath.isclose(identity, 0j, abs_tol=1e-15)
z = 0.5 + 0.2j
assert cmath.isclose(cmath.cosh(z), (cmath.exp(z) + cmath.exp(-z)) / 2)
```

---

## Classification and constants

| Function / constant | Purpose |
|---------------------|---------|
| `cmath.isfinite(z)` | Both components finite |
| `cmath.isinf(z)` | Either component infinite |
| `cmath.isnan(z)` | Either component NaN |
| `cmath.isclose(a, b, *, rel_tol, abs_tol)` | Complex-aware tolerant equality |
| `cmath.pi`, `cmath.e`, `cmath.tau` | Same as `math` constants |
| `cmath.inf`, `cmath.nan`, `cmath.infj`, `cmath.nanj` | Special values including pure-imaginary inf/NaN |

```python
# Goal: detect non-finite values before downstream math
import cmath

bad = complex(float("nan"), 1.0)
assert cmath.isnan(bad) and not cmath.isfinite(bad)
assert cmath.isclose(complex(1, 1e-12), 1 + 0j, rel_tol=1e-9)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`cmath`** when domain includes negatives under **`sqrt`/`log`** | Real `math` raises or loses solutions |
| Construct literals with explicit **`±0j`** near branch cuts | Cut side follows imaginary sign |
| Compare complex results with **`cmath.isclose`** | Component-wise tolerance handles NaN rules |
| Convert final answers with **`.real`** only when you proved imag ≈ 0 | Silent discard hides bugs |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Expecting `cmath.sqrt(x).imag == 0` for negative real x | Non-zero imaginary part by design | Document branch choice |
| Using `math` on complex `z.real` only | Ignores imaginary component | Call `cmath` on full `z` |
| `phase(-1 + 0j)` vs `phase(-1 - 0j)` | π vs −π | Treat signed zero seriously |
| Assuming `cmath` functions are always cheaper than `math` | Complex paths add overhead | Use `math` when domain is purely real |
| Comparing NaN with `==` | Always false | Use `cmath.isnan` / `isclose` |
