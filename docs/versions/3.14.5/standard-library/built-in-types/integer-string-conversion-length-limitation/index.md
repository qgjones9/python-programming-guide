# [Integer string conversion length limitation](https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation)

CPython limits how many **decimal digits** may participate in certain **`int` ↔ `str`** conversions to mitigate **denial-of-service** attacks ([CVE-2020-10735](https://nvd.nist.gov/vuln/detail/CVE-2020-10735)). The cap applies to **non-power-of-two bases** (especially base 10); **hex**, **oct**, and **binary** paths use linear-time algorithms and are **unlimited**. Full specification remains on [docs.python.org](https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation).

> **Added in version 3.11.**

---

## Why the limit exists

**`int`** values are stored as arbitrary-precision binary integers (“bignums”). Converting between strings and integers in **base 10** (and other non-power-of-two bases) has **sub-quadratic** cost—`int('1' * 500_000)` can take more than a second on a fast CPU. Bounding digit count prevents hostile input from pinning a core in conversion code.

The limit counts **digit characters** in the input or output string when a slow algorithm would run. **Underscores** and the **sign** do not count toward the limit.

---

## Defaults and errors

| Setting | Value | Meaning |
|---------|-------|---------|
| **`sys.int_info.default_max_str_digits`** | `4300` | Compiled-in default limit |
| **`sys.int_info.str_digits_check_threshold`** | `640` | Lowest configurable limit (except `0` = disabled) |

When a conversion would exceed the active limit, CPython raises **`ValueError`**.

```python
import sys

assert sys.int_info.default_max_str_digits == 4300
assert sys.int_info.str_digits_check_threshold == 640
```

```python
import sys

original = sys.get_int_max_str_digits()
try:
    sys.set_int_max_str_digits(4300)
    try:
        int('2' * 5432)
    except ValueError as err:
        assert '4300' in str(err)
    else:
        raise AssertionError('expected ValueError')

    i = int('2' * 4300)
    assert len(str(i)) == 4300

    squared = i * i
    try:
        str(squared)
    except ValueError:
        pass
    else:
        raise AssertionError('expected ValueError on str of large square')

    assert len(hex(squared)) > 4300
    assert int(hex(squared), base=16) == squared
finally:
    sys.set_int_max_str_digits(original)
```

Large **decimal** literals within the limit still convert to **`bytes`** without stringifying the full integer:

```python
payload = int(
    '578966293710682886880994035146873798396722250538762761564'
    '9252925514383915483333812743580549779436104706260696366600'
    '571186405732'
)
assert len(payload.to_bytes(53, 'big')) == 53
```

---

## Affected APIs

### Limited (potentially slow base-10 / non-power-of-two paths)

| API | Notes |
|-----|-------|
| **`int(string)`** | Default base 10 |
| **`int(string, base)`** | Bases that are **not** powers of 2 |
| **`str(integer)`** | Decimal string form |
| **`repr(integer)`** | Decimal in repr for ints |
| **`f"{n}"`**, **`"{}".format(n)`**, **`b"%d" % n`** | Any base-10 integer formatting |

### Not limited (linear-time or non-int paths)

| API | Notes |
|-----|-------|
| **`int(string, base)`** | Bases **2, 4, 8, 16, 32** |
| **`int.from_bytes()`** / **`int.to_bytes()`** | Binary blob conversion |
| **`hex()`**, **`oct()`**, **`bin()`** | Power-of-two string forms |
| Format mini-language | **`x`**, **`o`**, **`b`** conversions |
| **`float(string)`** | Not int conversion |
| **`decimal.Decimal(string)`** | Separate implementation |

---

## Configuring the limit

Set the limit **before** heavy conversion work—or at process startup for apps that need a non-default cap.

### Startup (environment and CLI)

| Mechanism | Example |
|-----------|---------|
| **`PYTHONINTMAXSTRDIGITS`** | `PYTHONINTMAXSTRDIGITS=640 python3` · `PYTHONINTMAXSTRDIGITS=0 python3` disables the cap |
| **`-X int_max_str_digits`** | `python3 -X int_max_str_digits=640` |

**`-X`** overrides the environment variable. **`sys.flags.int_max_str_digits`** records the configured value; **`-1`** means neither was set and the default **`4300`** was used at init.

### Runtime (`sys`)

| API | Role |
|-----|------|
| **`sys.get_int_max_str_digits()`** | Current interpreter-wide limit |
| **`sys.set_int_max_str_digits(n)`** | Set limit (`0` disables); subinterpreters have their own limit |
| **`sys.int_info.default_max_str_digits`** | Compiled-in default |
| **`sys.int_info.str_digits_check_threshold`** | Minimum allowed limit (except `0`) |

!!! warning
    A **low** limit can break **import** or **install** if source files contain **decimal integer literals** longer than the threshold—Python may fail while parsing before a `.pyc` exists. Prefer **`0x…`** hex literals for huge constants in source. Test with the limit enabled from startup (env or `-X`) when tuning production values.

---

## Recommended configuration

The default **4300** digits suits most programs. If you need a different bound, clamp from **`main`** with a version guard (APIs exist on patched 3.9–3.11 and in 3.12+):

```python
import sys

if hasattr(sys, 'set_int_max_str_digits'):
    original = sys.get_int_max_str_digits()
    try:
        upper_bound = 68000
        lower_bound = 4004
        current_limit = sys.get_int_max_str_digits()
        if current_limit == 0 or current_limit > upper_bound:
            sys.set_int_max_str_digits(upper_bound)
        elif current_limit < lower_bound:
            sys.set_int_max_str_digits(lower_bound)
    finally:
        sys.set_int_max_str_digits(original)
```

Set the limit to **`0`** to disable it entirely (not recommended unless you accept the DoS risk).

---

## Related topics in this guide

| Subject | Description |
|---------|-------------|
| [Numeric Types — int, float, complex](../numeric-types-int-float-complex/index.md) | Arbitrary-precision **`int`** and literals. |
| [Binary Sequence Types](../binary-sequence-types-bytes-bytearray-memoryview/index.md) | **`int.to_bytes()`** / **`int.from_bytes()`** bypass decimal string limits. |
| [Built-in Types](../index.md) | Overview of standard interpreter types. |

**See also:** [`sys.int_info`](https://docs.python.org/3/library/sys.html#sys.int_info) · [`sys.set_int_max_str_digits()`](https://docs.python.org/3/library/sys.html#sys.set_int_max_str_digits)
