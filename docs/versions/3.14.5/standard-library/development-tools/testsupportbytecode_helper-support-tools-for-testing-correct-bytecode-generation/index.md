# [test.support.bytecode_helper — Support tools for testing correct bytecode generation](https://docs.python.org/3/library/test.html#module-test.support.bytecode_helper)

`test.support.bytecode_helper` helps compiler tests assert that Python source compiles to **expected bytecode instruction sequences**. It subclasses patterns around `compile()` and `dis`. Canonical reference: [test.html#module-test.support.bytecode_helper](https://docs.python.org/3/library/test.html#module-test.support.bytecode_helper).

---

## Purpose

CPython's `test_compile`, `test_dis`, and related modules verify that language changes produce correct **opcode patterns**. Application developers rarely need this module unless authoring compiler-level tests.

---

## Key pieces

| Name | Role |
|------|------|
| `BytecodeTestCase` | Base class with assertion helpers for bytecode |
| `assertInBytecode` / `assertNotInBytecode` | Check for opname presence |
| `get_code` | Compile source to code object under test |

---

## Example — inspect bytecode for a snippet

```python
import unittest
import test.support.bytecode_helper as bh

class DemoTest(bh.BytecodeTestCase):
    def test_addition_bytecode(self):
        code = (lambda a, b: a + b).__code__
        self.assertInBytecode(code, "BINARY_OP", argval=0)  # NB_ADD

unittest.main(argv=["demo"], exit=False, verbosity=0)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Pin tests to **specific opnames** carefully | Opcodes evolve between Python versions |
| Prefer semantic tests for app code | Bytecode assertions break across releases |
| Use [`dis`](https://docs.python.org/3/library/dis.html) for exploratory debugging | Lower ceremony than subclassing |

---

## See also

- [`dis` — Disassembler](https://docs.python.org/3/library/dis.html)
- [`test.support`](../testsupport-utilities-for-the-python-test-suite/index.md)
