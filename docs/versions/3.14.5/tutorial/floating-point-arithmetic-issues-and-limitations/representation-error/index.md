# [Representation Error](https://docs.python.org/3/tutorial/floatingpoint.html#representation-error)

**Representation error** means many decimal fractions cannot be stored exactly as binary (base 2) fractions. That is why Python—and most languages using IEEE 754 hardware floats—often will not show the decimal you typed.

This section explains the `0.1` example in detail. Basic familiarity with binary floating-point helps.

Parent chapter: [Floating-Point Arithmetic: Issues and Limitations](../index.md).

## Why 1/10 is not exact in binary

Since about 2000, nearly all machines use **IEEE 754 binary64** (“double precision”) for Python [`float`](../../../standard-library/built-in-types/index.md) values. Each value has **53 bits** of precision. When you write `0.1`, the hardware finds the closest fraction $J / 2^N$ with $J$ using exactly 53 bits.

Rewrite the target:

```text
1 / 10 ≈ J / (2**N)
```

as

```text
J ≈ 2**N / 10
```

With $J$ requiring exactly 53 bits ($2^{52} \le J < 2^{53}$), the best exponent is $N = 56$:

```shell
>>> 2**52 <= 2**56 // 10 < 2**53
True
```

The best numerator comes from dividing $2^{56}$ by 10:

```shell
>>> q, r = divmod(2**56, 10)
>>> r
6
```

The remainder exceeds half of 10, so round up:

```shell
>>> q + 1
7205759403792794
```

The best IEEE 754 double approximation to $1/10$ is therefore:

```text
7205759403792794 / 2**56
```

Halving numerator and denominator gives the equivalent form:

```text
3602879701896397 / 2**55
```

That value is slightly **larger** than $1/10$ because we rounded up; without rounding up it would be slightly smaller—but never exact.

## What the computer actually stores

The machine never holds $1/10$; it holds the fraction above:

```shell
>>> 0.1 * 2**55
3602879701896397.0
```

Scaled to a 55-digit decimal:

```shell
>>> 3602879701896397 * 10**55 // 2**55
1000000000000000055511151231257827021181583404541015625
```

So the stored value equals decimal `0.1000000000000000055511151231257827021181583404541015625`. Older Python versions often displayed 17 significant digits:

```shell
>>> format(0.1, '.17f')
'0.10000000000000001'
```

## Using `fractions` and `decimal`

The [`fractions`](../../../standard-library/numeric-and-mathematical-modules/fractions-rational-numbers/index.md) and [`decimal`](../../../standard-library/numeric-and-mathematical-modules/decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md) modules make the analysis explicit:

```shell
>>> from decimal import Decimal
>>> from fractions import Fraction
>>> Fraction.from_float(0.1)
Fraction(3602879701896397, 36028797018963968)
>>> (0.1).as_integer_ratio()
(3602879701896397, 36028797018963968)
>>> Decimal.from_float(0.1)
Decimal('0.1000000000000000055511151231257827021181583404541015625')
>>> format(Decimal.from_float(0.1), '.17')
'0.10000000000000001'
```
