# [Boolean Operations — and, or, not](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not)

Python’s Boolean operations—`or`, `and`, and `not`—control how logical conditions are combined. Here they are, listed from lowest to highest precedence (priority):

| Operation   | Meaning (Explanatory)                                                                                  | Short-circuit? | Example                          |
|-------------|-------------------------------------------------------------------------------------------------------|:--------------:|-----------------------------------|
| `x or y`    | Returns `x` if `x` is truthy; otherwise returns `y`. Reads as: “If `x` is true, use `x`; else, use `y`.” | Yes (1)        | `a or b` returns `a` if true, else `b` |
| `x and y`   | Returns `x` if `x` is falsy; otherwise returns `y`. Reads as: “If `x` is false, use `x`; else, use `y`.”| Yes (2)        | `a and b` returns `a` if false, else `b` |
| `not x`     | Returns `True` if `x` is falsy, `False` if `x` is truthy. Unary logical negation.                     | No (3)         | `not a` is `True` only if `a` is falsy   |

**Explanatory Notes on Behavior:**

1. **Short-circuiting**:  
   - `or` only evaluates its second operand (`y`) if the first (`x`) is falsy, because if `x` is truthy, the outcome is already known.
   - `and` only evaluates its second operand (`y`) if the first (`x`) is truthy, because if `x` is falsy, the outcome is already known.

2. **Operator precedence**:  
   - `not` binds less tightly than comparison operators. For example, `not a == b` is parsed as `not (a == b)`, so it negates the comparison’s result.
   - Writing `a == not b` is invalid syntax, because `not` is not an operand for `==`.

**Tip:**  
These operators *return* one of their original operands (`x` or `y`)—not just a strict `True` or `False`. This is why expressions like `value = input or default` work, using the fallback only if `input` is falsy.
