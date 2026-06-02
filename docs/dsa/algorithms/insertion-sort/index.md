# Insertion sort

Keeps a **sorted region** at the left; each new element is **inserted** by shifting larger elements right.

| | |
| --- | --- |
| **What it is** | Card-by-card style: take the next card and slide it into place in the sorted hand. |
| **Time & space** | O(n²) worst case; best O(n) on nearly sorted data; O(1) extra space; **stable**. |
| **When to use** | Small arrays, nearly sorted input, or as the base case in Timsort–style hybrids. |
| **Online** | Can sort a stream as items arrive (left side always sorted). |

[Parent: Algorithms](../index.md)
