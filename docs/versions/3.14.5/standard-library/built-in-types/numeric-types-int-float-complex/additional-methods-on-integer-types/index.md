# [Additional Methods on Integer Types](https://docs.python.org/3/library/stdtypes.html#additional-methods-on-integer-types)

## Additional Methods on Integer Types

The standard integer type (`int`) in Python implements the [`numbers.Integral`](https://docs.python.org/3/library/numbers.html#numbers.Integral) abstract base class and provides several additional methods that offer introspection and data conversion abilities beyond basic arithmetic.

---

### `int.bit_length()`

Returns the number of bits required to represent the absolute value of the integer in binary, **excluding the sign and any leading zeros**.

#### Example

```python
n = -37
print(bin(n))         # '-0b100101'
print(n.bit_length()) # 6
```

Formally, for any nonzero integer `x`, `x.bit_length()` is the unique integer `k` such that `2**(k-1) <= abs(x) < 2**k`.  
If `x` is zero, `x.bit_length()` returns `0`.

**Roughly equivalent to:**

```python
def bit_length(self):
    s = bin(self)         # e.g. '-0b100101' for -37
    s = s.lstrip('-0b')   # remove leading '-', '0b'
    return len(s)         # count bits in the binary representation
```

*Added in version 3.1.*

---

### `int.bit_count()`

Returns the count of ones ("set bits") in the binary representation of the absolute value of the integer (also called the [population count](https://en.wikipedia.org/wiki/Hamming_weight)).

#### Example

```python
n = 19
print(bin(n))           # '0b10011'
print(n.bit_count())    # 3 — three '1's in 0b10011
print((-n).bit_count()) # 3 — negation does not affect count
```

**Equivalent to:**

```python
def bit_count(self):
    return bin(self).count("1")
```

*Added in version 3.10.*

---

### `int.to_bytes(length=1, byteorder='big', *, signed=False)`

Returns a [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) object representing the integer as a sequence of bytes. This method is often used for encoding integers for binary file formats or network protocols.

#### Example

```python
(1024).to_bytes(2, byteorder='big')      # b'\x04\x00'
(1024).to_bytes(10, byteorder='big')     # b'\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00'
(-1024).to_bytes(10, byteorder='big', signed=True)  # b'\xff\xff\xff\xff\xff\xff\xff\xff\xfc\x00'

x = 1000
x.to_bytes((x.bit_length() + 7) // 8, byteorder='little')  # b'\xe8\x03'
```

- The `length` argument specifies how many bytes to use.
- `OverflowError` is raised if the integer will not fit in the supplied number of bytes.
- `byteorder` ("big" or "little") determines the byte endianness (order).
- If `signed` is `False` and the integer is negative, `OverflowError` is raised.

The defaults allow encoding a small integer directly as a one-byte object:

```python
(65).to_bytes()     # b'A'
```

> **Warning**: Using default arguments, attempting to encode a value greater than 255 will raise `OverflowError` (because the default `length=1`).

**Roughly equivalent to:**

```python
def to_bytes(n, length=1, byteorder='big', signed=False):
    if byteorder == 'little':
        order = range(length)
    elif byteorder == 'big':
        order = reversed(range(length))
    else:
        raise ValueError("byteorder must be either 'little' or 'big'")

    return bytes((n >> i*8) & 0xff for i in order)
```

*Added in version 3.2. Default arguments for `length` and `byteorder` added in 3.11.*

---

### `int.from_bytes(bytes, byteorder='big', *, signed=False)` (classmethod)

The inverse of `to_bytes()`: returns the integer represented by a given `bytes` object (or any iterable of bytes).

#### Example

```python
int.from_bytes(b'\x00\x10', byteorder='big')       # 16
int.from_bytes(b'\x00\x10', byteorder='little')    # 4096
int.from_bytes(b'\xfc\x00', byteorder='big', signed=True)   # -1024
int.from_bytes(b'\xfc\x00', byteorder='big', signed=False)  # 64512
int.from_bytes([255, 0, 0], byteorder='big')       # 16711680
```

- `bytes` can be a bytes object or other sequence/iterator yielding integers in the range 0 <= x < 256.
- `byteorder` specifies endianness; use [`sys.byteorder`](https://docs.python.org/3/library/sys.html#sys.byteorder) for native order if needed.
- If `signed` is `True`, results use two’s complement conversion.

**Roughly equivalent to:**

```python
def from_bytes(bytes, byteorder='big', signed=False):
    if byteorder == 'little':
        little_ordered = list(bytes)
    elif byteorder == 'big':
        little_ordered = list(reversed(bytes))
    else:
        raise ValueError("byteorder must be either 'little' or 'big'")

    n = sum(b << i*8 for i, b in enumerate(little_ordered))
    if signed and little_ordered and (little_ordered[-1] & 0x80):
        n -= 1 << 8*len(little_ordered)
    return n
```

*Added in version 3.2. Default argument for `byteorder` added in 3.11.*

---

### `int.as_integer_ratio()`

Returns a tuple `(numerator, denominator)` representing the integer exactly as a fraction with a positive denominator. For integers, this always returns `(n, 1)`.

```python
(15).as_integer_ratio()   # (15, 1)
(-42).as_integer_ratio()  # (-42, 1)
```

*Added in version 3.8.*

---

### `int.is_integer()`

Always returns `True`. Provided for API compatibility with `float.is_integer()`, where the method returns `True` only if the value is a whole number.

```python
(17).is_integer()      # True
(-123).is_integer()    # True
```

*Added in version 3.12.*