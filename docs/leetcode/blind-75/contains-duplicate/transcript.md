# Contains Duplicate

```python
nums = [1, 2, 1, 2, 3]
```

## Welcome and Problem Overview

For this problem we're going to solve the classic coding interview question: "Contains Duplicate." We're given an array of integers and need to determine whether the array contains any duplicates. For example, in this array, the number 1 appears twice and the number 2 also appears twice, so the array contains duplicates.

```python
nums = [1, 2, 3, 1]
```

## Example with a Duplicate

Given this array, we see that 1 appears twice. Therefore, we should return `True`.

## Problem Statement and Examples

The goal is simple: return `True` if the array contains any duplicates. For instance, suppose our input is `[1, 1, 3, 3, 3]`. Here, 1 appears three times and 3 appears multiple times—clearly, there are duplicates, so the answer is `True`. If the array is `[1, 2, 3, 4]`, there are no duplicates, so we return `False`. That's the problem in a nutshell.

## Brute Force Approach

Let's talk about different approaches. First, the brute force solution: we use two nested loops to compare every pair of elements. For every element, we scan all elements to its right to check for duplicates. If we find a pair with the same value, we return `True`. This solution has a time complexity of O(n²), since for every element we might look at every other element. The space complexity is O(1) since we use no extra space. While the space usage is good, this is inefficient for large arrays.

## Sorting Approach

Can we improve the time complexity? Yes! We can sort the array first. Sorting takes O(n log n) time, and then we just check adjacent pairs: if any adjacent numbers are equal, there's a duplicate. For example, after sorting an array like `[2, 5, 1, 4, 5]`, we get `[1, 2, 4, 5, 5]`. Now we easily see two adjacent 5's, so we return `True`. This approach has O(n log n) time complexity and O(1) extra space if we sort in-place.

## Hash Set Approach — Intuition

Can we do even better? Yes—we can solve this in linear time, O(n), by using extra space. Here's the idea: as we iterate through the array, we keep track of elements we've seen so far using a set. For each number, we check if it's already in the set. If it is, we've found a duplicate and return `True`. Otherwise, we add it to the set and continue. Sets in Python allow us to check membership in constant time, which is why this approach is efficient.

## Hash Set Walkthrough from the Middle

Let's do a quick walkthrough: suppose we're halfway through the array and see the number 5. If 5 isn't already in our set of previously-seen numbers, we add it to the set and continue. Next, we see 4—it's not in the set, so we add it. Later, we see another 5; this time, since 5 is already in the set, we know there's a duplicate, so we return `True`.

## Hash Set Walkthrough from the Start

Let's walk through from the beginning. We initialize an empty set. The first element is 2—not in the set—so we add it. Next is 1—not in the set—so we add it. Next is 5—not in the set—so we add it. Then 4—not in the set—so we add it. Next, another 5—now 5 is in the set, so we've found a duplicate and return `True`.

## Efficient Solution Complexity and Closing

This hash set approach takes O(n) time and O(n) space. It's the most efficient approach for this problem. I hope this explanation made sense and helped you understand the different ways to solve the "Contains Duplicate" problem. Now, let's implement this algorithm!
