# [Hashing of numeric types](https://docs.python.org/3/library/stdtypes.html#hashing-of-numeric-types)

Python requires that for any two numbers `x` and `y` (even of different numeric types), if `x == y` then `hash(x) == hash(y)`. This ensures consistent behavior with sets, dictionaries, and other hash-based collections.

To achieve this consistently and efficiently across numeric types like `int`, `float`, `decimal.Decimal`, and `fractions.Fraction`, Python defines hashing of numeric types using a common mathematical approach that can be applied to any rational number. The core idea uses reduction modulo a large prime number `P`, which is accessible in Python as `sys.hash_info.modulus`.

**Implementation Detail (CPython):**

- For machines with 32-bit C longs:  `P = 2**31 - 1`
- For machines with 64-bit C longs:  `P = 2**61 - 1`

---

## Hashing Rules

**Let `x = m / n` (as a rational number in lowest terms, where `n > 0`):**

1. **If `n` is not divisible by `P`:**

   ```
   hash(x) = (m * invmod(n, P)) % P
   ```
   where `invmod(n, P)` is the inverse of `n` modulo `P`.

2. **If `n` *is* divisible by `P` (but `m` is not):**  
   `n` has no inverse modulo `P`. In this case,
   ```
   hash(x) = sys.hash_info.inf
   ```

3. **If `x` is negative:**  
   ```
   hash(x) = -hash(-x)
   ```
   If the result is `-1`, replace it with `-2`.

4. **Special values:**
   - `hash(x) = sys.hash_info.inf`  for positive infinity
   - `hash(x) = -sys.hash_info.inf` for negative infinity

5. **For a complex number `z = a + bj`:**
   ```
   hash(z) = (hash(z.real) + sys.hash_info.imag * hash(z.imag)) % M
   ```
   where `M = 2**sys.hash_info.width` (with range centered at 0, i.e. symmetric for negatives).
   If this yields `-1`, replace it with `-2`.

---

## Example: Equivalent Python Implementation

```python
import sys
import math

def hash_fraction(m, n):
    """Compute the hash for a rational number m / n (n > 0)."""
    P = sys.hash_info.modulus
    # Remove common factors with P
    while m % P == 0 and n % P == 0:
        m //= P
        n //= P

    if n % P == 0:
        hash_value = sys.hash_info.inf
    else:
        # Calculate modular inverse: pow(n, P-2, P) (Fermat's Little Theorem)
        hash_value = (abs(m) % P) * pow(n, P - 2, P) % P
    if m < 0:
        hash_value = -hash_value
    if hash_value == -1:
        hash_value = -2
    return hash_value

def hash_float(x):
    """Compute the hash for a float x."""
    if math.isnan(x):
        return object.__hash__(x)
    elif math.isinf(x):
        return sys.hash_info.inf if x > 0 else -sys.hash_info.inf
    else:
        return hash_fraction(*x.as_integer_ratio())

def hash_complex(z):
    """Compute the hash for a complex number z."""
    hash_value = hash_float(z.real) + sys.hash_info.imag * hash_float(z.imag)
    # Signed reduction modulo 2**sys.hash_info.width
    M = 2**(sys.hash_info.width - 1)
    hash_value = (hash_value & (M - 1)) - (hash_value & M)
    if hash_value == -1:
        hash_value = -2
    return hash_value
```

---

**Summary Table**

| Type                       | Hashing Rule                                                                       |
|----------------------------|------------------------------------------------------------------------------------|
| Rational (`m / n`, `n > 0`)| If `n % P != 0`: `(m * invmod(n, P)) % P`<br>If `n % P == 0`: `sys.hash_info.inf` |
| Negative Number            | `-hash(-x)` (replace -1 with -2 if needed)                                         |
| Positive/Negative Infinity | `sys.hash_info.inf` / `-sys.hash_info.inf`                                         |
| Complex (`z = a + bj`)     | `hash(a) + sys.hash_info.imag * hash(b)` (modulo)                                 |

These rules ensure consistent hash values for different numeric types that compare equal, supporting reliable usage in Python's hash-based containers like sets and dictionaries.