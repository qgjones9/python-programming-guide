# [Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html)

Condensed notes for [chapter 15](https://docs.python.org/3/tutorial/floatingpoint.html): why **binary floating-point** cannot represent every decimal fraction exactly, how [`repr()`](../../standard-library/built-in-functions/repr/index.md) and display rounding differ from the stored value, and when to use [`decimal`](../../standard-library/numeric-and-mathematical-modules/decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md), [`fractions`](../../standard-library/numeric-and-mathematical-modules/fractions-rational-numbers/index.md), or [`math.isclose()`](https://docs.python.org/3/library/math.html#math.isclose).

## Binary fractions vs decimal fractions

**Floating-point** numbers are stored in hardware as **base 2 (binary) fractions**. The decimal fraction `0.625` equals $6/10 + 2/100 + 5/1000$; the binary fraction `0.101` equals $1/2 + 0/4 + 1/8$. Same value, different notation.

Unfortunately, most **decimal fractions cannot be represented exactly as binary fractions**. The decimal literals you type are usually **approximations** of the binary value the machine stores.

## Base 10 intuition: why 1/3 never terminates

The idea is easier in base 10 first. The fraction **1/3** can only be approximated:

```text
0.3
0.33
0.333
…
```

No finite number of digits equals exactly $1/3$—only a better approximation each time.

## Base 2: why 0.1 is a repeating fraction

Likewise, **0.1** cannot be represented exactly in binary. In base 2, $1/10$ is an infinitely repeating fraction:

```text
0.0001100110011001100110011001100110011001100110011...
```

Stop at any finite number of bits and you get an **approximation**. On typical hardware today, floats use a binary fraction whose numerator uses the first **53 bits** and whose denominator is a power of two. For $1/10$, that stored value is `3602879701896397 / 2**55`—close to, but not equal to, the true $1/10$.

## How Python displays floats

Many users never notice the approximation because Python prints a **rounded decimal** view of the binary value stored. For `0.1`, the true stored decimal would be:

```shell
>>> 0.1
0.1000000000000000055511151231257827021181583404541015625
```

That is more digits than most people want, so the REPL shows a shorter rounded value:

```shell
>>> 1 / 10
0.1
```

Even when the display looks exact, the **stored** value is the nearest representable binary fraction.

Several different decimal literals can share the same nearest binary approximation—for example `0.1`, `0.10000000000000001`, and the long decimal above all map to `3602879701896397 / 2**55`. Any of them could be shown while keeping `eval(repr(x)) == x`.

Historically, [`repr()`](../../standard-library/built-in-functions/repr/index.md) often picked the 17-digit form `0.10000000000000001`. Since Python 3.1, the interpreter usually picks the **shortest** decimal that still round-trips—often `0.1`.

This behavior is inherent to **binary floating point**, not a Python bug. Other languages that use the same hardware arithmetic behave similarly (some hide the difference in default output).

## Formatting for pleasant output

You can limit how many digits appear using the built-in [`format()`](../../standard-library/built-in-functions/format/index.md) function (often with constants from the [`math`](../../standard-library/numeric-and-mathematical-modules/math-mathematical-functions/index.md) module):

```shell
>>> import math
>>> format(math.pi, '.12g')  # 12 significant digits
'3.14159265359'
>>> format(math.pi, '.2f')   # 2 digits after the decimal point
'3.14'
>>> repr(math.pi)
'3.141592653589793'
```

That only changes **display**—you are rounding the presentation of the true machine value, not changing what is stored.

## Equality surprises

Because `0.1` is not exactly $1/10$, adding three copies may not equal `0.3`:

```shell
>>> 0.1 + 0.1 + 0.1 == 0.3
False
```

Pre-rounding with [`round()`](../../standard-library/built-in-functions/round/index.md) does not fix the underlying representation:

```shell
>>> round(0.1, 1) + round(0.1, 1) + round(0.1, 1) == round(0.3, 1)
False
```

For **fuzzy comparisons**, use [`math.isclose()`](https://docs.python.org/3/library/math.html#math.isclose):

```shell
>>> import math
>>> math.isclose(0.1 + 0.1 + 0.1, 0.3)
True
```

Alternatively, compare values rounded to a fixed number of digits:

```shell
>>> round(math.pi, ndigits=2) == round(22 / 7, ndigits=2)
True
```

Binary floating-point has many surprises like these. The “0.1” case is worked through step by step in [Representation Error](representation-error/index.md). For broader background, see [Examples of Floating-Point Problems](https://docs.python.org/3/tutorial/floatingpoint.html) in the official tutorial and [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cdl/E199-02/821-1462/gtd1b.html) (classic survey).

## Practical guidance

“There are no easy answers,” but you need not fear floats for everyday work. Rounding error per operation is typically on the order of **1 part in $2^{53}$** on modern hardware—ample for most tasks. Remember it is **not decimal arithmetic**: every operation can introduce a new rounding step.

For casual use, rounding the **final** result to the decimal places you care about often matches expectations. [`str()`](../../standard-library/built-in-functions/str/index.md) is usually enough; for finer control, see [`str.format()`](../../tutorial/input-and-output/fancier-output-formatting/the-string-format-method/index.md) and [Format string syntax](https://docs.python.org/3/library/string.html#formatstrings).

When you need **exact decimal** semantics (accounting, legal amounts), use the [`decimal`](../../standard-library/numeric-and-mathematical-modules/decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md) module.

When you need **exact rationals** (such as $1/3$), use the [`fractions`](../../standard-library/numeric-and-mathematical-modules/fractions-rational-numbers/index.md) module.

Heavy numeric work may also use [NumPy](https://numpy.org/) and the [SciPy](https://scipy.org/) ecosystem.

## Inspecting the exact stored value

### [`float.as_integer_ratio()`](https://docs.python.org/3/library/functions.html#float.as_integer_ratio)

Expresses a float as an **exact integer fraction**:

```shell
>>> x = 3.14159
>>> x.as_integer_ratio()
(3537115888337719, 1125899906842624)
>>> x == 3537115888337719 / 1125899906842624
True
```

### [`float.hex()`](https://docs.python.org/3/library/functions.html#float.hex) and [`float.fromhex()`](https://docs.python.org/3/library/functions.html#float.fromhex)

Shows the **exact hexadecimal** representation stored by the machine—useful for portability and interchange with languages such as Java and C99:

```shell
>>> x.hex()
'0x1.921f9f01b866ep+1'
>>> x == float.fromhex('0x1.921f9f01b866ep+1')
True
```

## Summation accuracy

Repeated addition can accumulate error:

```shell
>>> 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 == 1.0
False
>>> sum([0.1] * 10) == 1.0
True
```

Built-in [`sum()`](../../standard-library/built-in-functions/sum/index.md) uses extended precision for intermediate steps in some cases. [`math.fsum()`](https://docs.python.org/3/library/math.html#math.fsum) tracks lost low-order bits so the final result has a **single** rounding—slower, but more accurate when large values mostly cancel:

```shell
>>> import math
>>> from fractions import Fraction
>>> arr = [-0.10430216751806065, -266310978.67179024, 143401161448607.16,
...        -143401161400469.7, 266262841.31058735, -0.003244936839808227]
>>> float(sum(map(Fraction, arr)))   # exact rationals, one float conversion
8.042173697819788e-13
>>> math.fsum(arr)                   # single rounding
8.042173697819788e-13
>>> sum(arr)                         # extended-precision intermediate steps
8.042178034628478e-13
>>> total = 0.0
>>> for x in arr:
...     total += x
...
>>> total                            # naive loop: no reliable digits here
-0.0051575902860057365
```

## Sections in this repo

- [Representation Error](representation-error/index.md) — why `0.1` is not exactly $1/10$ in IEEE 754 binary64 (§15.1).
