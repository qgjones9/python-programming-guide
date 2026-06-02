# 2-3-4 tree

A **B-tree of order 4**: each non-leaf node has 2, 3, or 4 **children** and 1, 2, or 3 **keys** that separate ranges.

| | |
| --- | --- |
| **What it is** | Self-balancing search tree; all leaves end up at the same depth. |
| **Relation to red–black** | A 2-3-4 tree can be encoded as a red–black tree (one common teaching path). |
| **When to use** | Pedagogy, disk-oriented B-trees, and understanding isometry with red–black trees. |
| **Search** | Compare key against 1–3 separators per node, choose child, repeat. |

[Parent: Data structures](../index.md)
