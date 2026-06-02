# [The if statement](https://docs.python.org/3/reference/compound_stmts.html#the-if-statement)

The `if` statement allows you to execute code conditionally based on one or more expressions:

```ebnf
if_stmt ::= "if" assignment_expression ":" suite
            ("elif" assignment_expression ":" suite)*
            ["else" ":" suite]
```

Here's how it works:

- Each condition (the `if` or any `elif`) is evaluated in order.
- The first condition that evaluates to true (see [Boolean operations](../../expressions/boolean-operations/index.md)) causes its corresponding suite (block) to be executed.
- No other part of the if-statement is executed after a true condition.
- If none of the conditions are true, and there is an `else` clause, the `else` suite is executed.

For example:

```python
x = 10
if x < 0:
    print("Negative")
elif x == 0:
    print("Zero")
else:
    print("Positive")
```
