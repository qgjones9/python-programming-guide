# [Logical lines](https://docs.python.org/3/reference/lexical_analysis.html#logical-lines)

The end of a logical line is represented by the token [`NEWLINE`](../../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#line-structure-tokens) (`token.NEWLINE`). Statements cannot cross logical line boundaries except where [`NEWLINE`](../../../../standard-library/python-language-services/token-constants-used-with-python-parse-trees/index.md#line-structure-tokens) is allowed by the syntax (e.g., between statements in compound statements). A logical line is constructed from one or more [physical lines](../physical-lines/index.md) by following the [explicit line joining](../explicit-line-joining/index.md) or [implicit line joining](../implicit-line-joining/index.md) rules.


