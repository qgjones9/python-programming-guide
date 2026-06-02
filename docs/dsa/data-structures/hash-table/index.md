# Hash table

A map from **keys** to **values** by hashing the key to a bucket index, with a policy for when two keys collide.

| | |
| --- | --- |
| **What it is** | `hash(key)` picks a slot; collisions are resolved (chaining, open addressing, etc.). |
| **Core operations** | Average O(1) find, insert, and delete; worst case if many collisions. |
| **When to use** | Counting, membership sets, caches, and almost any “dictionary” behavior. |
| **Trade-off** | Order of iteration is not meaningful unless you use a linked structure. |

[Parent: Data structures](../index.md)
