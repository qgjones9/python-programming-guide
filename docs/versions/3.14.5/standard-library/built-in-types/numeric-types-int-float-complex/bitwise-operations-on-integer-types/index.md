# [Bitwise Operations on Integer Types](https://docs.python.org/3/library/stdtypes.html#bitwise-operations-on-integer-types)

Bitwise operations apply only to integers in Python. These operations act as if performed using two’s complement arithmetic with an infinite number of sign bits.

**Operator Precedence:**  
- All binary bitwise operators (`|`, `^`, `&`, `<<`, `>>`) have *lower* precedence than arithmetic operators, but *higher* than comparisons.
- The unary `~` (bitwise NOT) has the same precedence as other unary numeric operators (`+`, `-`).

---

## Bitwise Operation Table (in increasing order of precedence)

| Operation   | Meaning (Explanatory)               | Notes    |
|-------------|-------------------------------------|----------|
| `x \| y`    | **Bitwise OR** — each bit of result is 1 if set in `x` *or* `y` | (4) |
| `x ^ y`     | **Bitwise XOR** — each bit of result is 1 if set in *either* `x` *or* `y`, but not both | (4) |
| `x & y`     | **Bitwise AND** — each bit of result is 1 if set in *both* `x` and `y` | (4) |
| `x << n`    | **Left shift** — `x` shifted left by `n` bits | (1), (2) |
| `x >> n`    | **Right shift** — `x` shifted right by `n` bits | (1), (3) |
| `~x`        | **Bitwise NOT** — inverts all bits of `x` |          |

---

## Real-world examples

These patterns show up whenever you store several on/off settings in one integer (permissions, feature flags, protocol fields) or need cheap power-of-two math.

| Operator | Problem you might face | Typical pattern |
|----------|------------------------|-----------------|
| `\|` | Turn on one or more flags without touching the rest | `flags \|= MASK` |
| `^` | Flip a single option on/off, or spot which bits differ | `flags ^= MASK` |
| `&` | Ask “is this permission enabled?” or pull one field out of a packed value | `flags & MASK` |
| `<<` | Multiply by $2^n$, build a one-hot mask, or pack bytes into an `int` | `1 << n`, `value << 8` |
| `>>` | Divide by $2^n$ (floor), or read the high byte of a packed integer | `value >> 8` |
| `~` | Build a mask for “every bit except these” when clearing flags | `flags & ~MASK` |

### Bitwise OR (`|`): combine flags

You often store several booleans in one `int` (file mode bits, UI feature toggles, socket options). OR lets you **enable** more flags in one assignment.

```python
READ, WRITE, EXECUTE = 4, 2, 1  # one bit per permission (like Unix rwx)

# Example: Granting additional permissions with bitwise OR
user_mode = READ                 # User initially has READ permission only
user_mode |= WRITE              # Add WRITE permission without affecting existing ones
# After this, user_mode has both READ and WRITE bits set
assert user_mode == (READ | WRITE)
# (READ | WRITE) evaluates to a value with both permission bits turned on

# Starting from zero, OR builds the full mask
options = 0
options |= 1 << 0   # feature A
options |= 1 << 2   # feature C
assert options == 0b101
```

### Bitwise XOR (`^`): toggle a flag or compare bit patterns

XOR is “on in exactly one operand.” Use it to **flip** a bit, or to see which bits differ between two values (handy for diffs and simple parity checks).

```python
NOTIFICATIONS_ON = 1 << 3
settings = 0b1000   # notifications currently on

settings ^= NOTIFICATIONS_ON   # toggle off
assert settings == 0

settings ^= NOTIFICATIONS_ON   # toggle back on
assert settings == NOTIFICATIONS_ON

# XOR highlights differing bits (here, which flags changed)
before, after = 0b1011, 0b1001
changed = before ^ after
assert changed == 0b0010
```

### Bitwise AND (`&`): test or extract bits

AND keeps only bits that are set in **both** operands. That is how you **test** a flag and how you **mask** down to one byte or one field in a packed integer.

```python
ADMIN = 1 << 4
role = 0b110000   # admin bit set

if role & ADMIN:
    print("admin actions allowed")

# Low byte of a 32-bit color: 0xRRGGBB
color = 0x3A7F2C
green = (color >> 8) & 0xFF
assert green == 0x7F

# Keep only the lower 12 bits of a sensor reading
raw = 0xFFFF_ABCD
value = raw & 0xFFF
assert value == 0xBCD
```

### Left shift (`<<`): powers of two and packing

Shifting left is multiplying by $2^n$ without calling `pow`. You also use `1 << n` to mean “only bit $n$ is set,” which is the building block for every mask above.

```python
# Fast scaling when n is small and you know x stays in range
page_size = 4096
offset = 3 * page_size
assert offset == 3 << 12   # 3 * 2**12

# Pack three bytes into one int (network order style)
b0, b1, b2 = 0xDE, 0xAD, 0xBE
packed = (b0 << 16) | (b1 << 8) | b2
assert packed == 0xDEADBE

# One-hot mask for bit 5
BIT_5 = 1 << 5
assert BIT_5 == 32
```

### Right shift (`>>`): divide by $2^n$ and unpack high bytes

Right shift is floor division by $2^n$ for non-negative values. Use it to **strip** bytes you already extracted with `&`, or to walk fixed-width binary layouts.

```python
# Halve or quarter when you know the value is non-negative
count = 100
half = count >> 1
assert half == 50

# High byte of a packed 16-bit value
word = 0x12_34
high = word >> 8
low = word & 0xFF
assert (high, low) == (0x12, 0x34)

# Extract version from a packed field: major in high 8 bits, minor in low 8
version = 0x03_0E   # 3.14 stored as (major << 8) | minor
major = version >> 8
minor = version & 0xFF
assert (major, minor) == (3, 14)
```

### Bitwise NOT (`~`): clear flags with a complemented mask

On Python `int`, `~x` is $-(x+1)$ because integers have unlimited precision, but the **idiom** that matters in practice is `value & ~MASK`: keep every bit except the ones in `MASK`.

```python
READ, WRITE, EXECUTE = 4, 2, 1
flags = READ | WRITE | EXECUTE

# Drop write permission, leave read and execute
flags &= ~WRITE
assert flags == (READ | EXECUTE)
assert flags & WRITE == 0

# ~MASK is the usual way to express "every bit except these"
# (for fixed-width ints in C you would write ~MASK & 0xFF; Python ints are unbounded)
```

```python
MASK = 0b1111
cleared = 0b1010_1010 & ~MASK
assert cleared == 0b1010_0000
```

---

### Notes

1. **Negative shift counts** are not allowed and will raise a `ValueError`.
2. A left shift (`x << n`) is mathematically equivalent to multiplying `x` by `pow(2, n)`.
3. A right shift (`x >> n`) is mathematically equivalent to floor-dividing `x` by `pow(2, n)`.
4. Bitwise logical operations treat numbers as if they have an infinite supply of sign bits, but for most practical purposes, using a *bit-width* of `1 + max(x.bit_length(), y.bit_length())` or more (that is, one extra sign bit) matches the infinite model.

**Summary:**  
Bitwise operations provide fine-grained control over the binary representation of integers and are governed by clear operator precedence and two’s complement logic.

---

## Where bitwise operations show up

Bitwise work is most common when you are close to how data is laid out in memory or on the wire, which is why it is often associated with **low-level** programming. The patterns in the examples above (flags, packed bytes, masks) are the same ideas you see in systems code, even when you write them in Python.

### Classic low-level territory

| Area | Typical use of bitwise ops |
|------|----------------------------|
| Hardware and drivers | GPIO registers, interrupt masks, device control blocks |
| C, C++, Rust, embedded | Struct layout, alignment, firmware bit fields |
| Networking and file formats | IP addresses, protocol flags, binary chunks (PNG, etc.) |
| Operating systems | Unix `rwx` permissions, `open()` flags, memory protection bits |

### Not only low-level Python

In everyday Python you may still rely on bit-oriented data without writing `&` and `|` yourself. Libraries often hide the operators but still use integer flags underneath.

| Task | Higher-level tool | What it replaces |
|------|-------------------|------------------|
| Permissions and feature flags | [`enum.IntFlag`](https://docs.python.org/3/library/enum.html#enum.IntFlag), [`enum.Flag`](https://docs.python.org/3/library/enum.html#enum.Flag) | Manual `|`, `&`, `^` on constants |
| Binary structs and records | [`struct`](https://docs.python.org/3/library/struct.html) `pack` / `unpack` | Hand-packed `<<`, `>>`, and masks |
| IP addresses and subnets | [`ipaddress`](https://docs.python.org/3/library/ipaddress.html) | Manual masking of address bytes |
| Stdlib options | `socket`, `os`, `subprocess`, and similar modules | Integer flag arguments passed to C APIs |

### Why Python feels less “low level”

Python `int` values have **unlimited precision**; there is no fixed 32-bit word in the language itself. You rarely manage word size the way you would in C. You reach for bitwise operators when the **problem** is inherently bit-oriented (flags, encodings, fast multiply/divide by powers of two), not because Python itself is close to the machine.

In fixed-width languages, `~MASK` often must be combined with a width mask (for example `~MASK & 0xFF`). In Python, the important idiom is usually `value & ~MASK` for clearing bits; width limits matter only when you interoperate with external binary formats via [`int.to_bytes()`](https://docs.python.org/3/library/stdtypes.html#int.to_bytes) or [`int.from_bytes()`](https://docs.python.org/3/library/stdtypes.html#int.from_bytes).

### Practical takeaway

| Kind of work | How often you write bitwise ops |
|--------------|----------------------------------|
| Systems programming, embedded, performance-sensitive code, custom protocols | Regularly |
| Typical application logic (CRUD, REST APIs, scripting, data analysis) | Occasionally, often only at integration boundaries |
| Pure business logic with no binary protocols or flag APIs | Rarely |

Bitwise operations are **foundational low-level machinery**. In Python they are a focused tool for bit-packed data and power-of-two math, not something most high-level code needs on every line. When you do need them, the operators in the table above are the direct way to express that logic; when you do not, prefer `enum`, `struct`, or domain-specific modules so intent stays clear.

---

## See also

- [Binary arithmetic](../../../../../../dsa/binary-arithmetic/index.md) — column addition, XOR/carry loops, two's complement, and a practice ladder for bit-manipulation problems.
- [Sum of Two Integers](../../../../../../leetcode/blind-75/sum-of-two-integers/index.md) — add two integers without `+` using the carry loop.
