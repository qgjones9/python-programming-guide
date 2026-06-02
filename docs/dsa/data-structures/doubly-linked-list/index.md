# Doubly linked list

Like a singly linked list, but every node can walk both forward and backward in O(1) from a given node.

| | |
| --- | --- |
| **What it is** | Each node stores *next* and *prev* pointers, linking to successor and predecessor. |
| **Core operations** | Remove a node in O(1) if you already have its address; list iteration both directions. |
| **When to use** | You need to delete the current node, move backward, or splice sublists without scanning from head. |
| **Trade-off** | Two pointers per node (more memory) vs singly linked list. |

[Parent: Data structures](../index.md)
