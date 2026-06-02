# Dequeue (deque)

A **double-ended queue**: efficient insertion and removal at both front and back.

| | |
| --- | --- |
| **What it is** | Combines features of a queue and a stack: both ends are “active” in O(1) for a good implementation. |
| **Core operations** | `push_front`, `push_back`, `pop_front`, `pop_back`, and optional `peek` at either end. |
| **When to use** | Sliding windows, “steal from both ends,” palindrome checks, or BFS on grids with early exits. |
| **Note** | Pronounced “deck.” Not the same as *dequeue* the verb in queue APIs. |

[Parent: Data structures](../index.md)
