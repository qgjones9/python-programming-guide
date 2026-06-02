# Bucket sort

Assumes (or uses) a distribution of values into **buckets**; sort each bucket, then **concatenate**.

| | |
| --- | --- |
| **What it is** | Map each key to a bucket index, sort buckets (often with insertion sort), then output in order. |
| **Time** | O(n) when buckets are O(n) and each bucket is O(1) size; degrades if all land in one bucket. |
| **When to use** | Uniform floats in [0,1) or when range maps cleanly to m buckets. |
| **Not** | A default for arbitrary orderings without distribution assumptions. |

[Parent: Algorithms](../index.md)
