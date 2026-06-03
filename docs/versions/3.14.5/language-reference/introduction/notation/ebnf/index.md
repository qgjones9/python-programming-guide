# [EBNF](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form)

## Basics

**EBNF** (Extended Backus–Naur Form) is a compact way to write down the rules of a language—what pieces are allowed, and in what order. Think of it as a recipe book for valid syntax: instead of listing every possible program by hand, you define a few named rules and how they combine.

Every EBNF grammar uses two kinds of symbols:

- **Terminal symbols** are the actual characters you can type—letters, digits, punctuation, and spaces. In a rule, they appear in quotes, like `"0"` or `"9"`. Those quoted characters are terminals: they are the raw material and are not defined by another rule.
- **Non-terminal symbols** are names for patterns built from terminals (and other non-terminals). In the example below, `digit` and `digit excluding zero` are non-terminals—they are labels for rules, not characters you type literally. A production rule says “this name stands for one of these sequences.”

For example, `"7"` is a **terminal** (one specific character). **`digit`** is a **non-terminal** (a name that means “any one decimal digit”). The rule `digit = "0" | digit excluding zero` connects them: to match `digit`, you eventually expand the name down to a single terminal such as `"7"`. Non-terminals are the building blocks in the grammar; terminals are where expansion stops.

Here is a small example that defines what counts as a digit:

```ebnf
digit excluding zero = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
digit                = "0" | digit excluding zero ;
```

The first rule defines a non-zero digit as any single character from `"1"` to `"9"`, using vertical bar `|` to indicate “or”—you choose one option. The second rule says a **digit** is either `"0"` or a non-zero digit as described above. By specifying the rules this way, you precisely describe all decimal digits without having to write out all ten cases in ordinary language.

## Sequences

A production rule can list several pieces in order. In classic EBNF, commas separate the parts:

```ebnf
twelve                          = "1", "2" ;
two hundred one                 = "2", "0", "1" ;
three hundred twelve            = "3", twelve ;
twelve thousand two hundred one = twelve, two hundred one ;
```

Read `"1", "2"` as: first a `"1"`, then a `"2"`, in that order. Later rules reuse earlier names (`twelve`, `two hundred one`) to build longer patterns from shorter ones.

## Optional and repeated elements

Classic EBNF uses **curly braces** for “zero or more” and **square brackets** for “zero or one”:

```ebnf
positive integer = digit excluding zero, { digit } ;
integer          = "0" | [ "-" ], positive integer ;
```

- `{ digit }` — the part inside may repeat any number of times, including not at all. So `positive integer` matches `1`, `42`, `10000`, and so on.
- `[ "-" ]` — the part inside may appear once or be omitted. So `integer` matches `0`, `42`, or `-42`.

For how Python applies grammar notation in the Language Reference, see [Python's grammar notation](../index.md).
