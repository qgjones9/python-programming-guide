# [Reserved classes of identifiers](https://docs.python.org/3/reference/lexical_analysis.html#reserved-classes-of-identifiers)

Certain patterns of identifiers—based on leading and/or trailing underscores—convey special meaning in Python, even though they are not language keywords. Understanding these patterns helps in reading, writing, and reasoning about Python code.

---

## 1. Single Leading Underscore: `_variable`

A single leading underscore indicates a "protected" variable by convention. This is a hint to programmers that the name is intended for internal use (private to a module or class) and should not be imported with `from module import *`:

```python
# mymodule.py
_var = 42  # Intended as 'internal use only'

# another.py
from mymodule import *  # _var will NOT be imported
print(_var)  # NameError: name '_var' is not defined
```

---

## 2. Underscore Alone: `_`

The single underscore `_` has several context-dependent uses:

- **Wildcard in Match Case Statements (Soft Keyword)**
  
  Used as a wildcard (catch-all) pattern in `match` statements (Python 3.10+):

  ```python
  value = 10
  match value:
      case 1:
          print("one")
      case _:
          print("something else")  # Matches anything not matched above
  ```

- **Last Evaluated Result in Interpreter**

  In the interactive Python interpreter, `_` stores the result of the last expression:

  ```python
  >>> 2 + 3
  5
  >>> _
  5
  ```

- **A Conventional "Unused" Variable**

  Programmers often use `_` to discard a value they do not intend to use:

  ```python
  for _ in range(5):
      print("Hello!")  # Value of '_' is ignored
  ```

- **Internationalization Marker**

  By convention, `_` is often assigned as an alias for translation functions, e.g., using [gettext](https://docs.python.org/3/library/gettext.html):

  ```python
  from gettext import gettext as _
  print(_("Translate this string"))
  ```

  > **Note:** While `_` has these common roles, it is a regular identifier and can be overwritten or repurposed in user code outside these situations.

---

## 3. Double Leading and Trailing Underscores: `__special__`

These are called **"dunder"** names (double-underscore). They are **system-defined** and reserved for special use by Python itself—such as magic methods and attributes.

- **Example:**

  ```python
  class MyClass:
      def __init__(self):    # Special method for initialization
          pass

  obj = MyClass()
  print(obj.__class__)        # Prints the class of the object
  ```

> **Caution:** Only use names with double leading and trailing underscores (`__*__`) if you are implementing a feature intended to interact with Python's internals or protocol. Inventing new "dunder" names in user code may cause compatibility issues in future Python versions.

---

## 4. Double Leading Underscore (No Trailing): `__variable`

A name beginning with two underscores and **not** ending with two is treated as a **class-private identifier**. Python performs name mangling for such variables to help prevent accidental attribute name clashes in subclasses.

- **Example:**

  ```python
  class Base:
      def __init__(self):
          self.__private = 123

      def get_private(self):
          return self.__private

  class Derived(Base):
      def __init__(self):
          super().__init__()
          self.__private = 456  # This does NOT overwrite Base's __private

  obj = Derived()
  print(obj.get_private())    # 123
  print(obj.__dict__)         # Shows _Base__private and _Derived__private
  ```

  > Name mangling rewrites `__private` in `Base` to `_Base__private`, and `__private` in `Derived` to `_Derived__private`.

---

**Summary Table of Reserved Identifier Classes**

| Pattern         | Explanation & Use                                                |
|-----------------|------------------------------------------------------------------|
| `_variable`     | Internal-use indicator; not imported via `from module import *`. |
| `_`             | Wildcard in match statements, last value in REPL, unused, i18n.  |
| `__special__`   | System "dunder" names, e.g. `__init__`, `__str__`.              |
| `__variable`    | Class-private; triggers name mangling to avoid conflicts.        |

For more on special names and methods, see [Special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names).