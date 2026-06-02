# AVL tree

A **self-balancing** binary search tree: after insert/delete, the tree is rotated to keep the height **logarithmic** in the number of nodes.

| | |
| --- | --- |
| **What it is** | Each node stores balance info (e.g. height or balance factor: left minus right). Rotations fix violations. |
| **Guarantee** | Height stays O(log n), so search/insert/delete are O(log n) worst case. |
| **When to use** | You need a BST with predictable worst-case performance on ordered or adversarial input. |
| **Trade-off** | More bookkeeping and rotations than a plain BST. |

[Parent: Data structures](../index.md)
