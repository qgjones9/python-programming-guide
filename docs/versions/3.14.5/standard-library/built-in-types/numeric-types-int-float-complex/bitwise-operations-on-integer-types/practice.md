# Practice: Bitwise Operations

Work through the tiers in order. Use Python's REPL, paper, or [practice.py](practice.py) for the coding drills. Each section maps directly to the operators on the [main page](index.md).

!!! tip "How to use this page"
    1. Try every **Predict** and **Fill in** item before opening an answer.
    2. Run `python practice.py` from this directory after filling in the TODO functions.
    3. When operators feel comfortable, continue to the [binary arithmetic practice ladder](../../../../../../dsa/binary-arithmetic/index.md#practice-ladder) for interview-style problems.

---

## Tier 1 — Predict the result

Evaluate each expression mentally or in a REPL. Assume non-negative integers unless noted.

| # | Expression | Your answer |
| --- | --- | --- |
| 1 | `0b1100 \| 0b1010` | |
| 2 | `0b1100 & 0b1010` | |
| 3 | `0b1100 ^ 0b1010` | |
| 4 | `0b1010 << 2` | |
| 5 | `0b1010 >> 1` | |
| 6 | `~0b1010` (as a Python `int`) | |
| 7 | `(0b1111_0000 >> 4) & 0xFF` | |

??? success "Tier 1 answers"
    | # | Result | Why |
    | --- | --- | --- |
    | 1 | `0b1110` (14) | OR keeps a bit if set in either operand |
    | 2 | `0b1000` (8) | AND keeps a bit only where both are 1 |
    | 3 | `0b0110` (6) | XOR is 1 where bits differ |
    | 4 | `0b101000` (40) | `<< 2` multiplies by $2^2$ |
    | 5 | `0b0101` (5) | `>> 1` floor-divides by 2 |
    | 6 | `-11` | Python: `~x` equals `-(x + 1)` |
    | 7 | `0b1111` (15) | Shift then mask the low byte |

---

## Tier 2 — Permission flags

Use the same constants as the main page: `READ = 4`, `WRITE = 2`, `EXECUTE = 1`.

| # | Starting value | Task | Your expression |
| --- | --- | --- | --- |
| 1 | `flags = READ` | Grant `WRITE` without clearing `READ` | |
| 2 | `flags = READ \| WRITE \| EXECUTE` | Remove `WRITE` only | |
| 3 | `flags = READ` | Test whether `EXECUTE` is set (truthy/falsy) | |
| 4 | `flags = READ \| EXECUTE` | Toggle `WRITE` on | |

??? success "Tier 2 answers"
    ```python
    READ, WRITE, EXECUTE = 4, 2, 1

    flags = READ
    flags |= WRITE
    assert flags == (READ | WRITE)

    flags = READ | WRITE | EXECUTE
    flags &= ~WRITE
    assert flags == (READ | EXECUTE)

    flags = READ
    assert not (flags & EXECUTE)
    assert flags & READ

    flags = READ | EXECUTE
    flags ^= WRITE
    assert flags == (READ | WRITE | EXECUTE)
    ```

---

## Tier 3 — Pack and unpack bytes

| # | Task | Your expression |
| --- | --- | --- |
| 1 | Build a one-hot mask for bit 7 | |
| 2 | Pack bytes `0xDE`, `0xAD`, `0xBE` into one int | |
| 3 | From `word = 0x12_34`, get high byte `0x12` | |
| 4 | From `word = 0x12_34`, get low byte `0x34` | |
| 5 | From `color = 0x3A7F2C`, extract green with `(color >> 8) & 0xFF` — what is green? | |

??? success "Tier 3 answers"
    ```python
    BIT_7 = 1 << 7
    assert BIT_7 == 128

    packed = (0xDE << 16) | (0xAD << 8) | 0xBE
    assert packed == 0xDEADBE

    word = 0x12_34
    high = word >> 8
    low = word & 0xFF
    assert (high, low) == (0x12, 0x34)

    color = 0x3A7F2C
    green = (color >> 8) & 0xFF
    assert green == 0x7F
    ```

---

## Tier 4 — Operator precedence

Bitwise operators bind **looser** than `+` and `*`, but **tighter** than comparisons. Parentheses usually make intent clearer.

| # | Expression | Your answer |
| --- | --- | --- |
| 1 | `3 + 4 << 1` | |
| 2 | `1 << 2 + 3` | |
| 3 | `5 & 3 + 1` | |

??? success "Tier 4 answers"
    | # | Result | Explanation |
    | --- | --- | --- |
    | 1 | `14` | `3 + 4` first → `7`, then `7 << 1` |
    | 2 | `32` | `2 + 3` first → `1 << 5` |
    | 3 | `4` | `3 + 1` first → `5 & 4` |

---

## Tier 5 — Implement the helpers

Open [practice.py](practice.py) and complete each function marked `TODO`. The file includes `assert` checks — when every test passes, you will see `All practice checks passed.`

| Function | Operator pattern |
| --- | --- |
| `grant` | `\|=` — turn on bits in a mask |
| `revoke` | `& ~` — turn off bits in a mask |
| `has` | `&` — test whether all mask bits are set |
| `toggle` | `^` — flip mask bits |
| `one_hot` | `1 << n` — single-bit mask |
| `pack_rgb` | `<<` and `\|` — three bytes into one int |
| `high_byte` / `low_byte` | `>> 8` and `& 0xFF` |

??? info "Starter template"
    ```python
    def grant(flags: int, mask: int) -> int:
        return flags | mask

    def revoke(flags: int, mask: int) -> int:
        return flags & ~mask
    ```
    Fill in the rest in `practice.py`, then run:
    ```bash
    python practice.py
    ```

---

## Tier 6 — Spot the bug

Each snippet has a mistake. Find it before reading the fix.

**A — clearing a flag**

```python
flags &= ~WRITE   # intended: drop WRITE bit
flags &= WRITE    # oops — wrong line left in the editor
```

**B — testing a flag**

```python
if flags == (flags & ADMIN):   # works only when no other bits are set
    ...
```

**C — negative shift**

```python
value >> -1   # what happens?
```

??? success "Tier 6 answers"
    **A** — The second line **sets** flags to only `WRITE` instead of clearing it. Use `flags &= ~WRITE` once.

    **B** — Prefer `if flags & ADMIN:` to test whether the admin bit is on regardless of other flags.

    **C** — Raises `ValueError: negative shift count` (see note 1 on the [main page](index.md)).

---

## Next steps

| When you are ready for… | Go to |
| --- | --- |
| XOR/carry addition and two's complement | [Binary arithmetic](../../../../../../dsa/binary-arithmetic/index.md) |
| Add without `+`, count bits, reverse bits | [Practice ladder](../../../../../../dsa/binary-arithmetic/index.md#practice-ladder) |
| Python operator semantics in the language reference | [Binary bitwise operations](../../../../../../language-reference/expressions/binary-bitwise-operations/index.md) |
