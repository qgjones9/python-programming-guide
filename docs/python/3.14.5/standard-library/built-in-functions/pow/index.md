# [pow()](https://docs.python.org/3/library/functions.html#pow)

## Description

`pow(base, exp, mod=None)` returns `base` raised to `exp`. With three integer arguments, it computes modular exponentiation efficiently. Two-argument form matches the `**` operator.

## What problem it solves

Exponentiation in math and cryptography—especially large powers modulo n, where the three-argument form avoids huge intermediate values.

## Implementation options

### Simple powers

```python
assert pow(2, 10) == 1024
assert pow(10, -2) == 0.01
```

### Modular exponentiation

```python
assert pow(2, 100, 1000) == 376
assert pow(38, -1, 97) == 23
assert 23 * 38 % 97 == 1
```

### Equivalent to ** for two arguments

```python
assert pow(3, 4) == 3 ** 4 == 81
```

## Best practices

- Use three-argument `pow(base, exp, mod)` for crypto and large modular math—not `(base ** exp) % mod`.
- Negative exponents with mod require base and mod to be relatively prime (see docs).
- Watch float/complex rules: negative non-integer exponents on negatives yield complex results.
