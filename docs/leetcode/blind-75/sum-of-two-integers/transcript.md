# Sum of Two Integers

You are given two integers `a` and `b`. Return their sum without using `+`, `-`, `*`, `/`, or `%`.

```text
a = 5
b = 14
```

The goal is **19**. We will verify that with ordinary addition first, then build the same result using only bitwise operations.

## Step 1: Add the worked example directly

```text
a = 5
b = 14
sum = 19
```

You cannot use `+` in code, but checking the answer by hand anchors the trace below.

## Step 2: Compare other inputs

The same pattern should work for any pair in the constraint range:

| `a` | `b` | Expected sum |
|-----|-----|--------------|
| 37 | 62 | 99 |
| -20 | -30 | -50 |
| 1 | 2 | 3 |

We focus on **`a = 5`, `b = 14`** for the full bitwise walkthrough, then note how negatives fit in at the end.

## Step 3: Brute force baseline

Move one unit at a time from `b` into `a` until `b` reaches zero. Without `+` or `-`, each single-step move still reduces to bit-level carry—so this approach is slow and does not scale.

```python
# Conceptual only — still needs a way to increment without +/-
while b != 0:
    # add 1 to a, subtract 1 from b  (not allowed as written)
    pass
```

This is **O(|b|)** at best and impractical for large integers.

## Step 4: Bitwise setup — sum and carry

Binary addition splits into two pieces at each bit position:

```python
sum_without_carry = a ^ b
carry = (a & b) << 1
```

| Role | Operation | Meaning |
|------|-----------|---------|
| Sum without carry | `a ^ b` | Add bits where carries do not overlap |
| Carry | `(a & b) << 1` | Positions where both bits are 1 send a carry left |

Repeat until `carry` is zero:

```python
while b:
    carry = (a & b) << 1
    a = a ^ b
    b = carry
return a
```

## Step 5: Binary view of `a = 5`, `b = 14`

```text
  5 = 0101
 14 = 1110
```

Adding column by column: `1+0=1`, `0+1=1`, `1+1=0 carry 1`, `0+1+carry=0 carry 1` → result **10011** = **19**.

The bitwise loop computes the same result in carry rounds instead of one `+` operator.

## Step 6: First iteration — `a = 5`, `b = 14`

```text
  a = 0101  (5)
  b = 1110  (14)
```

```python
sum_without_carry = a ^ b   # 0101 ^ 1110 = 1011  →  11
carry = (a & b) << 1        # (0101 & 1110) << 1 = 1000  →  8

a = 11
b = 8
```

## Step 7: Second iteration — `a = 11`, `b = 8`

```text
  a = 1011  (11)
  b = 1000  (8)
```

```python
sum_without_carry = 11 ^ 8   # 1011 ^ 1000 = 0011  →  3
carry = (11 & 8) << 1        # 1000 << 1 = 10000  →  16

a = 3
b = 16
```

## Step 8: Third iteration — `a = 3`, `b = 16`

```text
  a = 0011   (3)
  b = 10000  (16)
```

```python
sum_without_carry = 3 ^ 16   # 10011  →  19
carry = (3 & 16) << 1        # 0

a = 19
b = 0
```

`b` is zero, so the loop stops.

## Step 9: Full iteration table

| Iteration | `a` (start) | `b` (start) | `a ^ b` (new `a`) | `(a & b) << 1` (new `b`) |
|-----------|-------------|-------------|-------------------|--------------------------|
| 1 | 5 | 14 | 11 | 8 |
| 2 | 11 | 8 | 3 | 16 |
| 3 | 3 | 16 | **19** | 0 |

After iteration 3, carry is zero and the answer is **19**.

## Step 10: Negative inputs — `a = -20`, `b = -30`

Two's complement still applies: the same XOR/carry loop adds signed integers bit by bit. In **Python**, integers are unbounded, so an unmasked loop can run forever on negatives because carry never settles.

Mask to 32 bits each round, then convert back to signed:

```python
MASK = 0xFFFFFFFF
MAX_INT = 0x7FFFFFFF

a, b = a & MASK, b & MASK
while b:
    carry = ((a & b) << 1) & MASK
    a, b = (a ^ b) & MASK, carry
return a if a <= MAX_INT else ~(a ^ MASK)
```

For `a = -20` and `b = -30`, this returns **-50**.

## Result

```text
19
```

For the primary worked example `a = 5` and `b = 14`, the bitwise loop matches ordinary addition.

## Why bitwise addition works

Each iteration merges two numbers into (sum without carry, carry). The carry shifts left until no 1-bits overlap at the same position—exactly how hardware adders propagate carries.

- XOR handles addition where both bits are not simultaneously 1.
- AND finds positions that generate a carry; `<< 1` moves carries to the next column.
- At most **32** rounds for 32-bit integers → **O(1)** time, **O(1)** space.

The core loop:

```python
while b:
    carry = (a & b) << 1
    a = a ^ b
    b = carry
return a
```

In Python for LeetCode, always mask to `0xFFFFFFFF` and convert the final value back to signed form when the sign bit is set.
