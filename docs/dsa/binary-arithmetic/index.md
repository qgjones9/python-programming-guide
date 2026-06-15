# Binary arithmetic

How integers are written in base 2, how column addition works on bits, and how XOR, AND, and left shift implement the same math in code.

| | |
| --- | --- |
| **What it is** | Representing numbers with only 0 and 1 digits, then adding (and later subtracting) column by column with carries. |
| **Why it matters** | Bit-manipulation interview problems, fixed-width integers, flags, packed bytes, and hardware-style adders all reuse the same patterns. |
| **In this guide** | Read before the [Blind 75 Binary](../../leetcode/blind-75/index.md#binary) problems—especially [Sum of Two Integers](../../leetcode/blind-75/sum-of-two-integers/index.md). For Python operator syntax, see [Bitwise operations on integer types](../../versions/3.14.5/standard-library/built-in-types/numeric-types-int-float-complex/bitwise-operations-on-integer-types/index.md). |

## Decimal and binary place value

In decimal, each column is a power of ten: $437 = 4 \times 10^2 + 3 \times 10^1 + 7 \times 10^0$.

Binary uses powers of two instead:

| Column (right → left) | Place value | Bit in `0b1011` |
| --- | --- | --- |
| 0 | $2^0 = 1$ | 1 |
| 1 | $2^1 = 2$ | 1 |
| 2 | $2^2 = 4$ | 0 |
| 3 | $2^3 = 8$ | 1 |

So `0b1011` = $8 + 0 + 2 + 1$ = **11**.

Python helpers:

```python
n = 11
assert bin(n) == "0b1011"
assert int("1011", 2) == 11
assert 0b1011 == 11
```

| Notation | Meaning |
| --- | --- |
| `0b1011` | Binary literal in Python |
| `bin(n)` | Decimal → binary string |
| `int(s, 2)` | Binary string → decimal |
| `n.bit_length()` | Minimum bits needed to represent `n` (excluding sign for positives) |

## Column addition in binary

Add the same way you do on paper: add each column, write the digit, carry any overflow to the next column.

Example: $5 + 14 = 19$

```text
    0101   (5)
  + 1110   (14)
  ------
   10011   (19)
```

Column by column (right to left):

| Column | Bits | Sum | Write | Carry out |
| --- | --- | --- | --- | --- |
| 0 | 1 + 0 | 1 | 1 | 0 |
| 1 | 0 + 1 | 1 | 1 | 0 |
| 2 | 1 + 1 | 2 | 0 | 1 |
| 3 | 0 + 1 + carry 1 | 2 | 0 | 1 |
| 4 | (implicit 0) + carry 1 | 1 | 1 | 0 |

The result is `10011` = **19**.

!!! tip "Practice until this feels automatic"
    Before touching XOR or AND, add two small binary numbers on paper three or four times. The bit tricks below are just this column math in bulk.

## The three operators you need first

These three operators encode one round of binary addition:

| Operator | Name | One-bit rule | Addition role |
| --- | --- | --- | --- |
| `^` | XOR | 1 if bits **differ** | Sum **without** carry |
| `&` | AND | 1 if **both** bits are 1 | Where a **carry** is born |
| `<< 1` | Left shift | Move every bit one column left | Move carries to the **next** column |

### XOR: sum without carry

When both bits are not 1 at the same time, XOR matches ordinary addition:

| `a` | `b` | `a + b` (no carry in) | `a ^ b` |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 (write 0, carry 1) | 0 |

XOR fails only when **both** bits are 1—that case needs a carry, which AND handles.

### AND + shift: carry

When both bits are 1, you get a carry into the next column:

```python
a, b = 0b0101, 0b1110   # 5 and 14
carry = (a & b) << 1    # positions where both had 1, shifted left
assert carry == 0b1000  # 8
```

For `5 + 14`, iteration 1:

```python
a, b = 5, 14
partial_sum = a ^ b      # 11  — sum without carry
carry = (a & b) << 1     # 8   — carry to next round
```

### One round on paper and in code

```text
  a = 0101  (5)
  b = 1110  (14)
      ↓
  XOR → 1011  (11)     ← new a (partial sum)
  AND → 0100 → <<1 → 1000  (8)   ← new b (carry)
```

Repeat until carry (`b`) is zero.

## Add without `+`: the carry loop

The full algorithm merges partial sum and carry each round:

```python
def add(a: int, b: int) -> int:
    while b:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    return a

assert add(5, 14) == 19
assert add(1, 2) == 3
```

Trace for `a = 5`, `b = 14`:

| Round | Start `a` | Start `b` | `a ^ b` (new `a`) | `(a & b) << 1` (new `b`) |
| --- | --- | --- | --- | --- |
| 1 | 5 | 14 | 11 | 8 |
| 2 | 11 | 8 | 3 | 16 |
| 3 | 3 | 16 | **19** | 0 |

When `b` is 0, nothing is left to carry and `a` is the answer.

This is the same idea as a hardware **full adder** chain: XOR produces the sum bit, AND finds the carry, and you propagate until quiet.

Further walkthrough: [Sum of Two Integers transcript](../../leetcode/blind-75/sum-of-two-integers/transcript.md).

## Two's complement and negative numbers

Fixed-width machines (and LeetCode's 32-bit assumption) store signed integers with **two's complement**:

- Positive numbers look like ordinary binary.
- To negate: flip every bit (`~x` in fixed width), then add 1.

Example in 8 bits: $-5$

```text
  +5 = 0000_0101
 ~5 = 1111_1010
 +1 = 1111_1011   →  -5 in two's complement
```

The same XOR/carry loop still adds signed values **if** you keep every value inside a fixed width each round.

### Python trap: unbounded integers

Python `int` has unlimited precision. On negative inputs, an unmasked carry loop may **never** finish because carries keep appearing at new positions.

For LeetCode-style 32-bit signed integers, mask each round:

```python
MASK = 0xFFFFFFFF
MAX_INT = 0x7FFFFFFF

def add32(a: int, b: int) -> int:
    a, b = a & MASK, b & MASK
    while b:
        carry = ((a & b) << 1) & MASK
        a, b = (a ^ b) & MASK, carry
    return a if a <= MAX_INT else ~(a ^ MASK)

assert add32(-20, -30) == -50
```

| Step | Purpose |
| --- | --- |
| `& MASK` | Keep only the low 32 bits each iteration |
| `a <= MAX_INT` check | High bit clear → non-negative result |
| `~(a ^ MASK)` | Convert unsigned 32-bit pattern back to signed Python int |

Details and diagram: [Sum of Two Integers solution notes](../../leetcode/blind-75/sum-of-two-integers/index.md).

## Other bitwise tools (quick reference)

| Operator | Meaning | Typical use |
| --- | --- | --- |
| `\|` | OR — 1 if either bit is 1 | Combine flags |
| `>>` | Right shift | Divide by $2^n$; read high bytes |
| `~` | NOT (in fixed width) | Clear flags with `x & ~MASK` |

Full examples: [Bitwise operations on integer types](../../versions/3.14.5/standard-library/built-in-types/numeric-types-int-float-complex/bitwise-operations-on-integer-types/index.md).

## Practice ladder

Work through in order after you can add two binary numbers by hand:

| Order | Topic | Page |
| --- | --- | --- |
| 1 | Add without `+` (XOR + carry loop) | [Sum of Two Integers](../../leetcode/blind-75/sum-of-two-integers/index.md) |
| 2 | Count set bits | [Number of 1 Bits](../../leetcode/blind-75/number-of-1-bits/index.md) |
| 3 | DP over bit counts | [Counting Bits](../../leetcode/blind-75/counting-bits/index.md) |
| 4 | XOR canceling trick | [Missing Number](../../leetcode/blind-75/missing-number/index.md) |
| 5 | Reverse bit order in a word | [Reverse Bits](../../leetcode/blind-75/reverse-bits/index.md) |

All five live under [Blind 75 → Binary](../../leetcode/blind-75/index.md#binary).

## Common mistakes

- **Jumping to XOR before binary addition makes sense** — the operators are column math, not magic symbols.
- **Forgetting carry rounds** — one XOR/AND pair is rarely enough; loop until `b == 0`.
- **Ignoring width in Python** — negatives need masking for a terminating loop on LeetCode.
- **Confusing `<< 1` with “multiply by 2” only** — here it means “move carry to the next column.”

## How to use this in the roadmap

1. Read this page after [complexity analysis](../complexity/index.md) when you plan to tackle bit-manipulation problems.
2. Do one full hand trace ($5 + 14$) before opening any solution code.
3. Implement `add(a, b)` without `+`, then upgrade to `add32` with masking.
4. Move to the [practice ladder](#practice-ladder) — start with [Sum of Two Integers](../../leetcode/blind-75/sum-of-two-integers/index.md).

Further reading: [Two's complement](https://en.wikipedia.org/wiki/Two%27s_complement) (Wikipedia); [Adder (electronics)](https://en.wikipedia.org/wiki/Adder_(electronics)) for the hardware view.

[Parent: Data structures and algorithms](../index.md)
