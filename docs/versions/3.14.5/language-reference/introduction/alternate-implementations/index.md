# [Alternate Implementations](https://docs.python.org/3/reference/introduction.html#alternate-implementations)

Local notes on **Alternate Implementations** within [*Introduction*](../index.md). CPython is the reference implementation, but other runtimes exist for Java, .NET, and performance research. Each may differ from the language as documented here—check that runtime's own documentation for gaps.

Though there is one Python implementation which is by far the most popular, alternate implementations are of particular interest to different audiences. New language features generally land in CPython first; ports may lag or omit features.

## Known implementations

| Implementation | Host | Role |
|----------------|------|------|
| [CPython](https://docs.python.org/3/) | C | Original, most-maintained implementation; defines de-facto semantics for most users. |
| [Jython](https://www.jython.org/) | JVM | Python for Java platforms; integrates with Java class libraries and is often used to script or test Java code. |
| [Python for .NET](https://pythonnet.github.io/) | .NET | Embeds CPython and exposes .NET libraries to Python code. |
| [IronPython](https://ironpython.net/) | .NET | Full Python implementation compiling to IL and .NET assemblies (distinct from Python.NET). |
| [PyPy](https://pypy.org/) | RPython | Python written in Python, with JIT and experimental language/interpreter features. |

## Practical differences to watch

| Area | Typical variation |
|------|-------------------|
| Performance | PyPy JIT vs CPython interpreter; startup and memory profiles differ. |
| C extension modules | Many packages target the CPython C-API; other runtimes may not load them. |
| Language version | Ports may implement an older Python version or subset of syntax. |
| Standard library | Some modules are missing or replaced on non-CPython runtimes. |
| Object model details | Reference counts, GC timing, and introspection can differ. |

## Best practices

| Practice | Why |
|----------|-----|
| Detect the runtime with `sys.implementation` instead of guessing from `platform`. | Names and version tuples are the supported introspection API. |
| Read the port's compatibility matrix before deploying. | "Python 3.x" on a label does not guarantee full stdlib or extension support. |
| Test on your target runtime in CI when not using CPython. | Syntax accepted by CPython may parse differently or fail elsewhere. |
| Prefer pure-Python dependencies when portability matters. | C extensions tie you to CPython (or a runtime with compatible ABI). |
| Treat this Language Reference as CPython-oriented unless stated otherwise. | Disputes are usually settled against [docs.python.org](https://docs.python.org/3/reference/index.html). |

```python
import sys

info = sys.implementation
# name is typically 'cpython' on the reference implementation; other runtimes use their own id.
assert isinstance(info.name, str) and info.name
assert info.version is not None
assert info.version.major >= 3
```

Parent: [Introduction](../index.md)
