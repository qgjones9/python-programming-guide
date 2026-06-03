# [decimal — Decimal fixed-point and floating-point arithmetic](https://docs.python.org/3/library/decimal.html)

The [`decimal`](https://docs.python.org/3/library/decimal.html) module implements **correctly rounded decimal floating-point** per the General Decimal Arithmetic specification. Unlike binary `float`, values such as `0.1` are represented exactly; trailing zeros preserve significant digits (important for currency). Arithmetic runs inside a **context** that controls precision, rounding mode, exponent limits, and **signals** (flags/traps for inexact, overflow, etc.). Full tutorial, `Decimal` API, and context objects are on [docs.python.org](https://docs.python.org/3/library/decimal.html).

---

## Core concepts

| Concept | Role |
|---------|------|
| `Decimal` | Immutable sign + coefficient + exponent; special values `NaN`, `±Infinity`, `±0` |
| `Context` | Active precision, rounding, traps, and sticky flags |
| `getcontext()` / `setcontext()` | Thread-local default context |
| `localcontext()` | Temporary context manager for scoped changes |
| Signals | `Inexact`, `Rounded`, `Overflow`, `DivisionByZero`, `InvalidOperation`, … |

---

## Constructing `Decimal` values

| Source | Behavior |
|--------|----------|
| String `'3.14'` | Exact — preferred for literals |
| `int` | Exact conversion |
| `float` | Exact binary→decimal expansion (often long coefficient) |
| Tuple `(sign, digits, exponent)` | Low-level constructor |
| `Decimal('NaN')`, `'Infinity'` | Special values |

```python
# Goal: string construction preserves schoolbook decimals
from decimal import Decimal

assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
assert Decimal("1.30") + Decimal("1.20") == Decimal("2.50")
assert Decimal(10) == Decimal("10")
```

---

## Context and rounding

| Setting | Effect |
|---------|--------|
| `getcontext().prec = n` | Maximum significant digits for **results** of operations |
| `rounding = ROUND_HALF_EVEN` (default) | Banker's rounding |
| `traps[FloatOperation] = True` | Reject accidental `Decimal`/`float` mixing |
| `flags` | Sticky indicators — clear before monitoring a calculation |

```python
# Goal: lower precision for display rounding vs full internal precision
from decimal import Decimal, getcontext, ROUND_HALF_UP, localcontext

with localcontext() as ctx:
    ctx.prec = 4
    ctx.rounding = ROUND_HALF_UP
    quote = Decimal("1") / Decimal("7")
    assert str(quote) == "0.1429"

getcontext().prec = 28
full = Decimal("1") / Decimal("7")
assert len(str(full).replace(".", "")) > 6
```

---

## Arithmetic and quantize

| Operation | Note |
|-----------|------|
| `+`, `-`, `*`, `/`, `//`, `%`, `**` | Context precision applies to results |
| `quantize(exp)` | Fix exponent (e.g. cents with `Decimal('0.01')`) |
| `compare`, `compare_total` | Total ordering including NaN payload rules |
| `sqrt`, `ln`, `log10`, `exp` | Context precision applied |

```python
# Goal: price line items with half-up cent rounding
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().rounding = ROUND_HALF_UP
unit = Decimal("19.99")
qty = Decimal("3")
tax_rate = Decimal("0.0825")
subtotal = (unit * qty).quantize(Decimal("0.01"))
tax = (subtotal * tax_rate).quantize(Decimal("0.01"))
total = subtotal + tax
assert subtotal == Decimal("59.97")
assert tax == Decimal("4.95")
assert total == Decimal("64.92")
```

---

## Mitigating float contamination — [Special values](https://docs.python.org/3/library/decimal.html#special-values)

| Approach | When |
|----------|------|
| `Decimal(str(float_value))` | Import legacy float measurements explicitly |
| Enable **`FloatOperation` trap** | Strict apps that forbid silent float mixing |
| Use **`fractions.Fraction`** bridge | Exact rationals before decimal formatting |

```python
# Goal: sum decimal strings like a ledger (exact zero residual)
from decimal import Decimal

parts = "1.34 1.87 3.45 2.35 1.00 0.03 9.25".split()
data = list(map(Decimal, parts))
assert sum(data) == Decimal("19.29")
assert sum([Decimal("0.1")] * 3) - Decimal("0.3") == Decimal("0.0")
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Parse money from **strings**, not floats | Avoids inherited binary noise |
| Set **`prec`** and **`rounding`** explicitly for reporting | Defaults may not match regulatory rules |
| Use **`localcontext()`** in tests | Avoid mutating global context for other threads |
| **`quantize`** after tax/discount chains | Keeps fixed decimal places for invoices |
| Clear or inspect **`flags`** when debugging inexact results | Sticky flags accumulate across operations |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `Decimal(3.14)` expecting short coefficient | Long exact float expansion | Use `Decimal('3.14')` |
| Comparing `Decimal('3.5') < 3.7` with float trap | `FloatOperation` | Compare to `Decimal('3.7')` |
| Assuming trailing zeros are cosmetic | They encode significant digits | Format with `quantize` / f-strings |
| Ignoring **`InvalidOperation`** on huge literals | Construction fails | Validate input strings |
| Mixing contexts across threads without care | Surprising precision in web workers | Set context per task or use `localcontext` |
