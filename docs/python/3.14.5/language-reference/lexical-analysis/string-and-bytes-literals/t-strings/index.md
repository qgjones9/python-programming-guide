# [t-strings](https://docs.python.org/3/reference/lexical_analysis.html#t-strings)

Introduced in Python 3.14.

A template string literal, or t-string, is a string literal prefixed with `t` or `T`. T-strings follow the same syntax rules as formatted string literals (f-strings), but produce a `Template` object instead of a plain string. For the differences in evaluation rules, see the Standard Library section on t-strings.

**Example:**

```python
from string import Template

user = "Alice"
product = "Python Programming Guide"
t = t"""
Dear $user,

Thank you for your interest in the $product.

Best regards,
The Team
"""
print(t.substitute(user=user, product=product))
# Output:
# Dear Alice,
#
# Thank you for your interest in the Python Programming Guide.
#
# Best regards,
# The Team
```