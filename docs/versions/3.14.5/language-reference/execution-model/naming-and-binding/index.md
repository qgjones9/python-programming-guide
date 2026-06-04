# [4.2. Naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)

**Names** refer to **objects**. Binding operations introduce or rebind names in a scope; **resolution** rules decide which binding a use refers to. Python has no separate declaration syntax—any binding anywhere in a block can make a name **local** to that block. Subsections **4.2.1–4.2.6** are consolidated here (no nested folders in this mirror). Canonical text: [Naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding).

Parent: [4. Execution model](../index.md)

---

## 4.2.1. Binding of names — [Binding of names](https://docs.python.org/3/reference/executionmodel.html#binding-of-names)

| Construct | Binds names? |
|-----------|----------------|
| Function parameters | Yes |
| `def` / `class` statements | Yes (function/class name) |
| Assignment (`=`, augmented `+=`, walrus `:=` in allowed places) | Yes |
| `import` / `from … import` | Yes |
| `from module import *` | Yes (module level only; skips `_` names) |
| `as` target in `with`, `except`, `except*`, pattern matching | Yes |
| `del` target | Treated as bound for resolution rules (semantics: unbind) |
| Type parameter lists (PEP 695) | Yes |

```python
# Goal: assignment binds a name in the current block
box = []
box.append(1)
assert box == [1]
```

```python
# Goal: import binds a module object to a name
import math as m
assert m.isfinite(3.14)
```

---

## 4.2.2. Resolution of names — [Resolution of names](https://docs.python.org/3/reference/executionmodel.html#resolution-of-names)

| Term | Meaning |
|------|---------|
| **Local** | Bound in the current block (unless `global` / `nonlocal` say otherwise) |
| **Global** | Bound at module level |
| **Free** | Used in a block but defined in an enclosing block |
| **Environment** | All scopes visible to a block |

Resolution uses the **nearest enclosing scope**. Missing names raise `NameError`. Using a local before it is bound raises `UnboundLocalError` (subclass of `NameError`).

**Critical rule:** If a name is **bound anywhere** in a function block, **all** uses in that block are treated as local unless declared `global` or `nonlocal`.

```python
# Goal: free variable resolved at call time from enclosing scope
i = 10

def f():
    return i

i = 42
assert f() == 42
```

```python
# Goal: assignment anywhere in the function makes x local → UnboundLocalError
def broken():
    print(x)  # x is local to broken() but not yet bound
    x = 1

raised = False
try:
    broken()
except UnboundLocalError:
    raised = True
assert raised
```

```python
# Goal: global statement redirects to module namespace
count = 0

def inc():
    global count
    count += 1

inc()
assert count == 1
```

```python
# Goal: nonlocal writes the enclosing function's binding
def make_counter():
    n = 0

    def step():
        nonlocal n
        n += 1
        return n

    return step

counter = make_counter()
assert counter() == 1 and counter() == 2
```

**Class bodies:** Names in a class block do not leak into methods or most comprehensions in that block; unbound locals in a class block fall back to the **global** namespace.

```python
# Goal: class body name not visible inside a comprehension in the class block
def class_body_fails():
    class A:
        a = 42
        b = list(a + i for i in range(2))  # NameError: a not visible here

    return A

raised = False
try:
    class_body_fails()
except NameError:
    raised = True
assert raised
```

---

## 4.2.3. Annotation scopes — [Annotation scopes](https://docs.python.org/3/reference/executionmodel.html#annotation-scopes)

Introduced in Python 3.12 (PEP 695), extended in 3.13–3.14 for lazy defaults and annotations. Annotation scopes behave like function scopes but:

| Difference | Detail |
|------------|--------|
| Class access | Can use names from the enclosing **class** body (unlike ordinary nested functions) |
| Forbidden syntax | No `yield`, `yield from`, `await`, or walrus `:=` in annotation-scope expressions |
| `nonlocal` | Cannot rebind names defined in annotation scopes from inner scopes |
| `__qualname__` | Objects appear as if defined in the enclosing scope |

```python
# Goal: type alias in class body can refer to nested class (annotation scope)
class A:
    type Alias = Nested

    class Nested:
        pass

assert A.Alias.__value__ is A.Nested
```

---

## 4.2.4. Lazy evaluation — [Lazy evaluation](https://docs.python.org/3/reference/executionmodel.html#lazy-evaluation)

Type aliases, type parameter bounds/defaults/constraints, and many annotations are **not** evaluated at definition time. Evaluation happens when attributes such as `__value__` or `__bound__` are accessed—useful for forward references and mutual recursion.

```python
# Goal: division error deferred until __value__ is read
type Bad = 1 / 0

deferred = False
try:
    _ = Bad.__value__
except ZeroDivisionError:
    deferred = True
assert deferred
```

```python
# Goal: mutually recursive type aliases (lazy) — requires Python 3.12+
from typing import Literal

type SimpleExpr = int | Parenthesized
type Parenthesized = tuple[Literal["("], Expr, Literal[")"]]
type Expr = SimpleExpr | tuple[SimpleExpr, Literal["+", "-"], Expr]

assert SimpleExpr.__value__ is not None
```

---

## 4.2.5. Builtins and restricted execution — [Builtins and restricted execution](https://docs.python.org/3/reference/executionmodel.html#builtins-and-restricted-execution)

The builtins namespace is found via `__builtins__` in the global namespace (dict or module). In `__main__`, it usually references the `builtins` module; in other modules, an alias to that module’s dict.

| Practice | Reason |
|----------|--------|
| Do not mutate `__builtins__` directly | Implementation detail |
| Override via `import builtins; builtins.len = …` | Supported pattern for sandboxes (with care) |

```python
# Goal: unqualified len resolves through builtins namespace
assert len([1, 2, 3]) == 3
```

---

## 4.2.6. Interaction with dynamic features — [Interaction with dynamic features](https://docs.python.org/3/reference/executionmodel.html#interaction-with-dynamic-features)

`eval()` and `exec()` resolve names in caller-supplied **global** and **local** dicts. **Free variables** from enclosing functions are **not** visible unless copied into those dicts. If only one namespace dict is passed, it is used for both global and local lookup.

```python
# Goal: exec with explicit globals sees assignments there
g = {}
exec("z = 40 + 2", g)
assert g["z"] == 42
```

```python
# Goal: pass explicit namespace dict when exec needs enclosing bindings
def run_with_secret():
    secret = 7
    loc = {"secret": secret}
    exec("result = secret + 1", loc)
    return loc["result"]

assert run_with_secret() == 8
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `print(x)` then `x = 1` in same function | `UnboundLocalError` on `print` | Rename, reorder, or use `global` / `nonlocal` |
| `from mod import *` inside a function | SyntaxError (only module level) | Import explicitly |
| Comprehension in **class body** using class locals | `NameError` | Move comprehension to method or module level |
| Lazy type alias looks fine at definition | Fails at first `__value__` access | Test attribute access; design forward refs |
| `exec(code)` expecting closure capture | Name not found | Pass a namespace dict with needed keys |
