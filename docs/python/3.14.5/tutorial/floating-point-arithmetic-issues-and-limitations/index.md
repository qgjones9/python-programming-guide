# [Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html)

Condensed notes for [chapter 15](https://docs.python.org/3/tutorial/floatingpoint.html): why binary floats cannot represent every decimal fraction, **`repr` vs str**, **`Decimal`**, **`Fraction`**, and **representation error**.

```python
# Classic surprise: 0.1 + 0.2 uses IEEE-754 binary64, which cannot store 0.1 exactly.
assert 0.1 + 0.2 != 0.3
assert round(0.1 + 0.2, 1) == 0.3  # rounding to a fixed precision often restores expectations
```

### 15.1 — [Representation Error](https://docs.python.org/3/tutorial/floatingpoint.html#representation-error)

```python
from fractions import Fraction

# Exact rationals make the algebra visible — compare to float approximations.
assert Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10)
```

## Sections in this repo

- [Representation Error](representation-error/index.md)

Next: [Appendix](../appendix/index.md)
