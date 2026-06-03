# [nested scope](https://docs.python.org/3.14/glossary.html#term-nested-scope)

The ability to refer to a variable in an enclosing definition.  For instance, a function defined inside another function can refer to variables in the outer function.  Note that nested scopes by default work only for reference and not for assignment.  Local variables both read and write in the innermost scope.  Likewise, global variables read and write to the global namespace.  The [nonlocal](https://docs.python.org/3.14/reference/simple_stmts.html#nonlocal) allows writing to outer scopes.
