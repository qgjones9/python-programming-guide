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

## Addition (`+`)

The addition operator adds two numbers together and gives their sum.

```python
print(2 + 3)  # Output: 5
```

## Subtraction (`-`)

The subtraction operator finds the difference between two numbers.

```python
print(2 - 3)  # Output: -1
```

## Multiplication (`*`)

The multiplication operator multiplies two numbers.

```python
print(2 * 3)  # Output: 6
```

## Division (`/`)

The division operator divides one number by another. In Python 3, this always returns a float.

```python
print(2 / 3)  # Output: 0.6666666666666666
```

## Modulus (`%`)

The modulus operator gives you the remainder after dividing one number by another.

```python
print(2 % 3)  # Output: 2
```

## Exponentiation (`**`)

The exponentiation operator raises the number on the left to the power of the number on the right.

```python
print(2 ** 3)  # Output: 8
```

## Floor Division (`//`)

Floor division divides one number by another and gives you the largest possible integer (the floor) that is less than or equal to the result.

```python
print(2 // 3)  # Output: 0
```

---

## Putting arithmetic operators to work

You’ll use these operators all the time in real calculations — not just math exercises, but to solve everyday work problems. Here are a few examples:

### Example 1: Calculating Overtime Pay

Suppose you work 45 hours in a week, and you get paid \$20 per hour for the first 40 hours, and 1.5 times that for each hour over 40. Let’s use arithmetic:

```python
regular_hours = 40
hours_worked = 45
hourly_rate = 20

# Overtime hours
overtime_hours = hours_worked - regular_hours
# Regular pay
regular_pay = regular_hours * hourly_rate
# Overtime pay (1.5x regular rate)
overtime_pay = overtime_hours * hourly_rate * 1.5
# Total pay
total_pay = regular_pay + overtime_pay

print(total_pay)  # Output: 950.0
```

### Example 2: Distributing Items Equally

Suppose you have 23 apples and you want to pack them into bags of 5 apples each. How many full bags can you make and how many apples are left?

```python
total_apples = 23
apples_per_bag = 5

full_bags = total_apples // apples_per_bag  # Floor division
leftover_apples = total_apples % apples_per_bag  # Modulus

print("Bags:", full_bags)      # Output: Bags: 4
print("Leftover:", leftover_apples)  # Output: Leftover: 3
```

### Example 3: Compound Interest Calculation

You’ve \$1000 in your account and want to know how much you’ll have after 3 years with a 5% annual interest rate, compounded yearly.

```python
principal = 1000
rate = 0.05
years = 3

final_amount = principal * (1 + rate) ** years
print(final_amount)  # Output: 1157.625
```

---

Using these basic arithmetic operators, you can build up to more complex calculations—whether for finance, distributing resources, or just doing quick math in your daily work!

## Parentheses

Parentheses can be used to group expressions. See example below:
```python
print(2 + 3 * 4) # This will print 14
print((2 + 3) * 4) # This will print 20
```

The integer numbers (e.g. 2, 4, 20) have type [int](../../../../standard-library/built-in-functions/int/index.md), the ones with a fractional part (e.g. 5.0, 1.6) have type [float](../../../../standard-library/built-in-functions/float/index.md). We will see more about numeric types later in the tutorial.

Division `/` always returns a float. To do floor division and get an integer result you can use the `//` operator; to calculate the remainder you can use `%`:


