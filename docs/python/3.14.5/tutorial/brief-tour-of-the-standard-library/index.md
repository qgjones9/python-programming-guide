# [Brief Tour of the Standard Library](https://docs.python.org/3/tutorial/stdlib.html)

Condensed notes for [chapter 10 — Brief Tour of the Standard Library](https://docs.python.org/3/tutorial/stdlib.html): **`os`**, **`glob`**, **`sys`**, **`re`**, **`math`**, **`random`**, **`urllib`**, **`datetime`**, **`zlib`**, **`timeit`**, **`doctest`**, and batteries-included philosophy. This page is a **high-level map**; each subsection below links to a stub that mirrors the official heading.

```python
import os
import math

# `os` exposes process + filesystem primitives; `math` is float-heavy numeric helpers.
assert isinstance(os.getcwd(), str)
assert math.isclose(math.sqrt(2) ** 2, 2.0)
```

### 10.1 — [Operating System Interface](https://docs.python.org/3/tutorial/stdlib.html#operating-system-interface)

- **`os`** exposes process ids, environment variables, and filesystem helpers; **`os.path`** is the portable string layer for paths.

### 10.6 — [Mathematics](https://docs.python.org/3/tutorial/stdlib.html#mathematics)

```python
import math

assert math.gcd(84, 30) == 6  # greatest common divisor — useful for rational reductions
```

## Sections in this repo

- [Operating System Interface](operating-system-interface/index.md)
- [File Wildcards](file-wildcards/index.md)
- [Command Line Arguments](command-line-arguments/index.md)
- [Error Output Redirection and Program Termination](error-output-redirection-and-program-termination/index.md)
- [String Pattern Matching](string-pattern-matching/index.md)
- [Mathematics](mathematics/index.md)
- [Random](../../standard-library/numeric-and-mathematical-modules/random-generate-pseudo-random-numbers/index.md)
- [Internet Access](internet-access/index.md)
- [Dates and Times](dates-and-times/index.md)
- [Data Compression](data-compression/index.md)
- [Performance Measurement](performance-measurement/index.md)
- [Quality Control](quality-control/index.md)
- [Batteries Included](batteries-included/index.md)

Next: [Brief Tour of the Standard Library — Part II](../brief-tour-of-the-standard-library-part-ii/index.md)
