# [Numbers](https://docs.python.org/3/tutorial/introduction.html#numbers)


Python can be used like a simple calculator to perform arithmetic using operators such as +, -, *, /, and parentheses for grouping.

See example below:
```python
print(2 + 3) # This will print 5
print(2 - 3) # This will print -1
print(2 * 3) # This will print 6
print(2 / 3) # This will print 0.6666666666666666
print(2 % 3) # This will print 2
print(2 ** 3) # This will print 8
print(2 // 3) # This will print 0
```

The following operators are supported:

| Operator | Description |
|----------|-------------|
| + | Addition (sum of two numbers) (2 + 3 = 5) |
| - | Subtraction (difference of two numbers) (2 - 3 = -1) |
| * | Multiplication (product of two numbers) (2 * 3 = 6) |
| / | Division (quotient of two numbers) (2 / 3 = 0.6666666666666666) |
| % | Modulus (remainder of two numbers) (2 % 3 = 2) |
| ** | Exponentiation (power of two numbers) (2 ** 3 = 8) |
| // | Floor division (quotient of two numbers) (2 // 3 = 0) |

## Parentheses

Parentheses can be used to group expressions. See example below:
```python
print(2 + 3 * 4) # This will print 14
print((2 + 3) * 4) # This will print 20
```

The integer numbers (e.g. 2, 4, 20) have type [int](../../../../standard-library/built-in-functions/int/index.md), the ones with a fractional part (e.g. 5.0, 1.6) have type [float](../../../../standard-library/built-in-functions/float/index.md). We will see more about numeric types later in the tutorial.

Division `/` always returns a float. To do floor division and get an integer result you can use the `//` operator; to calculate the remainder you can use `%`:


