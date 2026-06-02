# Array-based lists

A list implemented with a **contiguous** block of memory (array), sometimes resized to grow or shrink.

| | |
| --- | --- |
| **What it is** | Elements are stored in index order in an array; the logical “list” is that sequence (static size or dynamic reallocation). |
| **Core operations** | O(1) access by index; append or insert may cost if resize or shift is needed. |
| **When to use** | You need fast random access, cache-friendly storage, and a well-understood list API. |
| **Trade-off** | Middle insert/delete may shift many elements; growth strategy affects amortized cost. |

[Parent: Data structures](../index.md)
