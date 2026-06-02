# Tries

A tree whose edges are labeled (often with characters) so **prefixes** of strings share the same path from the root.

| | |
| --- | --- |
| **What it is** | Also “prefix tree”: each level advances one character (or one token) of a key. |
| **Core operations** | Insert, search, and prefix search by walking the tree; space trades off with alphabet size. |
| **When to use** | Dictionaries, autocomplete, IP routing tables, and anything prefix-heavy. |
| **Variants** | Radix / Patricia trees compress long chains of single-child nodes. |

[Parent: Data structures](../index.md)
