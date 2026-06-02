# Linked list

A linear collection stored as nodes that point to the next item—unlike a contiguous array, there is no index-based address arithmetic.

| | |
| --- | --- |
| **What it is** | Nodes in a chain: each holds a value (or “element”) and a link to the *next* node. The *head* is the entry to the list. |
| **Core operations** | Insert or delete a node when you have a pointer to it; traverse from the head. |
| **When to use** | Frequent insert/delete at the front, unknown or changing length, or avoiding large array copies. |
| **Trade-off** | Random access by index is O(n); extra space per item for the pointer. |

[Parent: Data structures](../index.md)
