# [Escaped characters](https://docs.python.org/3/reference/lexical_analysis.html#escaped-characters)

To represent special characters that would otherwise have a syntactic meaning in Python string literals, you use escape sequences—combinations of a backslash (`\`) followed by another character. 

For instance, if you want to include an actual backslash character in a non-raw Python string, you must type two backslashes (`\\`). The first backslash is the escape character, telling Python to interpret the second as a literal backslash:

```python
print('C:\\Program Files')
```
This will output:
```
C:\Program Files
```

If you want to include a single quote (`'`) or double quote (`"`) character inside a string literal—especially if that quote matches the type of quotes used to define the string—you use escape sequences as well: `\'` for a literal single quote and `\"` for a literal double quote. 

For example:

```python
print('\' and \"')
```
This will output:
```
' and "
```