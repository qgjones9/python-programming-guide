# [8.3. The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)

## The `for` Statement

The `for` statement in Python is a fundamental looping construct that allows you to iterate over the elements of a sequence (like a list, tuple, or string) or any object that is iterable.

### Syntax

```ebnf
for_stmt ::= "for" target_list "in" starred_expression_list ":" suite
             ["else" ":" suite]
```

Let's break down what this syntax means and how it works:

1. **Evaluation of the Iterable:**  
   The `starred_expression_list` (the part after in) is evaluated once at the start of the loop. It should yield an iterable object (for example, a [list](../../../standard-library/built-in-functions/list/index.md), [tuple](../../../standard-library/built-in-functions/tuple/index.md), [string](../../../standard-library/built-in-types/text-sequence-type-str/index.md), or any object that implements the iterator protocol).

2. **Iteration and Assignment:**  
   Python creates an iterator from this iterable. Each time through the loop, it fetches the next item from the iterator and assigns it to the variables listed in `target_list`, using standard assignment rules. (See the [Assignment statements](../../simple-statements/assignment-statements/index.md) section for details.)

3. **Loop Body Execution:**  
   The code block following the colon (called the "suite") is executed once for each item in the iterable.

4. **The Else Clause:**  
   If you include an optional `else` clause after the loop, its code will only be executed **if the loop runs to completion** (that is, it is not terminated early by a `break` statement).

5. **`break` and `continue`:**  
   - A `break` inside the loop's suite will terminate the loop **immediately** and skip the `else` clause.
   - A `continue` inside the suite skips the rest of the suite for the current item and proceeds to the next iteration.

### Important Details and Example

It's important to understand that the loop variable(s) in `target_list` are assigned a new value at the start of each iteration. Any changes you make to these variables inside the loop are overwritten in the next iteration. Let's see an example:

```python
for i in range(10):
    print(i)
    i = 5   # Changing 'i' here has no effect on the loop behavior,
            # because 'i' will be overwritten with the next value from range(10)
```

When the loop finishes, the variable names in `target_list` still exist, but if the iterable was empty, they may not have been assigned at all.

**Tip:** The built-in `range()` type is a common way to create an iterable of numbers. For example, `range(3)` produces `0, 1, 2` in sequence.

### Version Note

> **Changed in Python 3.11:**  
> You can now use starred (`*`) elements in the expression list part of the `for` statement.

---