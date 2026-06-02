# Circularly linked list

A linked list where the “tail” closes back to the “head,” so the structure has no end in a linear sense.

| | |
| --- | --- |
| **What it is** | The last node’s *next* points to the first node (circular), optionally doubly linked with *prev* too. |
| **Core operations** | Rotate, iterate “forever” in one direction, or share one pointer as both head and current. |
| **When to use** | Round-robin scheduling, buffer rings, or algorithms that treat the list as a cycle. |
| **Watch out** | Traversal needs a stop condition to avoid an infinite loop. |

[Parent: Data structures](../index.md)
