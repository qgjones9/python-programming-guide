# Red–black tree

A self-balancing BST with **one bit of color** per node and a small set of local rules that keep the tree approximately balanced.

| | |
| --- | --- |
| **What it is** | Nodes are *red* or *black*; invariants (e.g. no two reds in a row, black height same on all root-to-leaf paths) bound height. |
| **Guarantee** | O(log n) search, insert, and delete. |
| **When to use** | The basis of many `map` / `set` containers (e.g. C++ `std::map`, Java `TreeMap`). |
| **Trade-off** | Slightly more complex rules than AVL, often fewer rotations on insert in practice. |

[Parent: Data structures](../index.md)
