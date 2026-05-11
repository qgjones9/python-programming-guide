# [Classes](https://docs.python.org/3/tutorial/classes.html)

Condensed notes for [chapter 9 — Classes](https://docs.python.org/3/tutorial/classes.html): objects and names, scopes, class syntax, methods, instance data, inheritance, privacy conventions, iterators, and generators. For narrative examples (especially **scopes**), follow the subsection links.

### 9.1 — [A Word About Names and Objects](https://docs.python.org/3/tutorial/classes.html#a-word-about-names-and-objects)

- Objects have identity (**`is`**), type, and value; multiple names can reference the **same** object (aliases).

```python
xs = []
ys = xs  # second name binds to the same list object
ys.append(1)
assert xs is ys and xs == [1]  # mutation visible through either name
```

### 9.2 — [Python Scopes and Namespaces](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)

- **LEGB**: **L**ocal, **E**nclosing, **G**lobal, **B**uiltins — name resolution walks outward; **`global`** / **`nonlocal`** rebind outer namespaces explicitly.

```python
def outer():
    x = 1

    def inner():
        nonlocal x
        x += 1  # rebinds `x` in `outer`, not a new local
        return x

    return inner


f = outer()
assert f() == 2 and f() == 3
```

### 9.3 — [A First Look at Classes](https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes)

- **`class Name:`** creates a class object; methods are functions stored on the class; the instance is passed as **`self`** by the descriptor protocol when you call **`inst.method()`**.

```python
class Counter:
    def __init__(self) -> None:
        self.n = 0

    def inc(self) -> int:
        self.n += 1
        return self.n


c = Counter()
assert c.inc() == 1 and c.n == 1
```

### 9.4 — [Object Methods](https://docs.python.org/3/tutorial/classes.html#object-methods)

- Calling **`obj.meth(arg)`** passes **`obj`** as the first parameter **`self`**; **`Class.meth(obj, arg)`** is the explicit equivalent.

```python
class Greeter:
    def hi(self, name: str) -> str:
        return f"hi {name}"


g = Greeter()
# Bound method closes over the instance — first arg is supplied automatically.
assert g.hi("Ada") == Greeter.hi(g, "Ada")
```

### 9.5 — [Class and Instance Variables](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables)

- **Class variables** are shared unless you rebind them per instance carefully; **instance variables** live on **`self`**.

```python
class Dog:
    tricks: list[str] = []  # shared across all dogs — usually a bug if mutated

    def __init__(self) -> None:
        self.tricks = []  # per-dog list is the common fix


d1, d2 = Dog(), Dog()
d1.tricks.append("sit")
assert d1.tricks == ["sit"] and d2.tricks == []  # instance lists are independent
```

### 9.6 — [Random Remarks](https://docs.python.org/3/tutorial/classes.html#random-remarks)

- Data hiding is by convention (**`_name`**, **`__name`**) and **mangling** is mainly for subclass name collisions, not security.

```python
class C:
    def _semi_private(self) -> str:
        return "ok"


assert C()._semi_private() == "ok"
```

### 9.7 — [Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)

- **`class Derived(Base):`** puts **`Base`** on **`__mro__`**; **`super()`** follows the MRO for cooperative multiple inheritance.

```python
class Base:
    def f(self) -> str:
        return "base"


class Derived(Base):
    def f(self) -> str:
        return super().f() + "+derived"


assert Derived().f() == "base+derived"
```

### 9.8 — [Multiple Inheritance](https://docs.python.org/3/tutorial/classes.html#multiple-inheritance)

- Python’s **C3 linearization** defines **`Derived.__mro__`**; **`super()`** calls the next class in that order.

```python
class A:
    def tag(self) -> str:
        return "A"


class B(A):
    def tag(self) -> str:
        return super().tag() + "B"


class C(A):
    def tag(self) -> str:
        return super().tag() + "C"


class D(B, C):
    def tag(self) -> str:
        return super().tag() + "D"


assert "A" in D().tag()  # exact string order is version/layout-specific — only assert participation
```

### 9.9 — [Private Variables](https://docs.python.org/3/tutorial/classes.html#private-variables)

- **`__attr`** in a class body is name-mangled to **`_ClassName__attr`** to reduce accidental clashes in hierarchies.

```python
class Mapping:
    def __init__(self) -> None:
        self.__data: dict[str, int] = {}

    def set(self, k: str, v: int) -> None:
        self.__data[k] = v


m = Mapping()
m.set("a", 1)
assert m._Mapping__data == {"a": 1}  # mangled attribute name is discoverable — not a security boundary
```

### 9.10 — [Odds and Ends](https://docs.python.org/3/tutorial/classes.html#odds-and-ends)

- **`__slots__`** can reduce per-instance **`__dict__`** overhead when you have a fixed set of attributes (trade-offs apply).

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y


p = Point(1, 2)
assert p.x == 1 and not hasattr(p, "__dict__")
```

### 9.11 — [Iterators](https://docs.python.org/3/tutorial/classes.html#iterators)

- **`__iter__` / `__next__`** implement the iterator protocol; **`iter()` / `next()`** are the user-facing builtins.

```python
class CountToThree:
    def __init__(self) -> None:
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self) -> int:
        self.i += 1
        if self.i > 3:
            raise StopIteration
        return self.i


assert list(CountToThree()) == [1, 2, 3]
```

### 9.12 — [Generators](https://docs.python.org/3/tutorial/classes.html#generators)

- **`yield`** makes a generator function; each call to **`next()`** resumes after the last **`yield`**.

```python
def squares(n: int):
    for i in range(n):
        yield i * i


assert list(squares(4)) == [0, 1, 4, 9]
```

### 9.13 — [Generator Expressions](https://docs.python.org/3/tutorial/classes.html#generator-expressions)

- Like list comprehensions but **lazy**: **`(expr for x in it)`** returns an iterator without building a list.

```python
it = (x * x for x in range(3))
assert next(it) == 0 and next(it) == 1
```

## Sections in this repo

- [A Word About Names and Objects](a-word-about-names-and-objects/index.md)
- [Python Scopes and Namespaces](python-scopes-and-namespaces/index.md)
- [A First Look at Classes](a-first-look-at-classes/index.md)
- [Object Methods](object-methods/index.md)
- [Inheritance](inheritance/index.md)
- [Multiple Inheritance](inheritance/multiple-inheritance/index.md)
- [Private Variables](private-variables/index.md)
- [Random Remarks](random-remarks/index.md)
- [Odds and Ends](odds-and-ends/index.md)
- [Iterators](iterators/index.md)
- [Generators](generators/index.md)
- [Generator Expressions](generator-expressions/index.md)

Next: [Brief Tour of the Standard Library](../brief-tour-of-the-standard-library/index.md)
