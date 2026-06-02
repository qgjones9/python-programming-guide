# Binary search tree

A binary tree where, for every node, all keys in the **left** subtree are smaller and all keys in the **right** subtree are greater.

| | |
| --- | --- |
| **What it is** | Enables ordered `insert`, `search`, and `delete` by comparing at each step down the tree. |
| **Height** | Performance is O(h); unbalanced input can make h = O(n). |
| **When to use** | Ordered iteration and range queries when you may later balance (AVL, red–black) or the data is random. |
| **In-order traversal** | Visits keys in sorted order. |

[Parent: Data structures](../index.md)
