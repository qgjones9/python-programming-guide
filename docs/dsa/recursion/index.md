# Recursion

A function that solves a problem by calling itself on **smaller or simpler** instances until a **base case** stops the chain.

| | |
| --- | --- |
| **What it is** | Decompose a problem into the same problem on reduced input, then combine results on the way back up. |
| **Why it matters** | Trees, divide-and-conquer sorts, graph DFS, and backtracking are natural to express recursively; many structure definitions are recursive. |
| **In this guide** | Read after [complexity analysis](../complexity/index.md): recursive depth adds **call-stack** space. See [merge sort](../algorithms/merge-sort/index.md), [binary search tree](../data-structures/binary-search-tree/index.md), and [graphs](../data-structures/graphs/index.md). |

## The two required parts

Every correct recursive function needs both:

1. **Base case** — Input small enough to answer directly (no further recursive call).
2. **Recursive case** — Call the same function on input that moves **toward** the base case.

If either is missing or the recursive step does not shrink the problem, you get infinite recursion and a `RecursionError` once Python hits its recursion limit (often around 1000 frames by default).

```python
def factorial(n):
 if n <= 1: # base case
 return 1
 return n * factorial(n - 1) # recursive case: smaller n
```

## Call stack intuition

Each call waits for the next to finish. Python keeps **stack frames**: local variables and “where to return” for each active call.

For `factorial(3)`:

```text
factorial(3) → waits on 3 * factorial(2)
 factorial(2) → waits on 2 * factorial(1)
 factorial(1) → returns 1 (base case)
 factorial(2) → returns 2 * 1 = 2
factorial(3) → returns 3 * 2 = 6
```

**Space:** If the chain has depth *d*, the call stack uses O(*d*) auxiliary space. Deep recursion on large *n* can overflow the stack before time becomes an issue—see [complexity analysis](../complexity/index.md).

## How to read and write recursive code

1. **State the base case** in words (“empty list sums to 0”).
2. **Assume** the recursive call on the smaller input is correct (inductive step).
3. **Combine** that result with the current step (one element, one child, one half).
4. **Verify progress** — each call must move strictly closer to the base case (smaller list, shorter path, half-sized array).

Tracing on paper or with a few `print` depths helps at first; later you rely on the structure of the problem.

## Patterns you will reuse

| Pattern | Idea | Example in this guide |
| --- | --- | --- |
| **Linear recursion** | One recursive call per step | Walk a [linked list](../data-structures/linked-list/index.md); factorial |
| **Tree recursion** | Multiple recursive calls (children) | [BST](../data-structures/binary-search-tree/index.md) search; tree height |
| **Divide and conquer** | Split input, recurse on parts, merge | [Merge sort](../algorithms/merge-sort/index.md), [quicksort](../algorithms/quicksort/index.md) |
| **Graph / state search** | Recurse on neighbors or choices; track visited | DFS on [graphs](../data-structures/graphs/index.md); backtracking (Phase 5+) |

## Examples

**Sum a list** — base case empty list; recursive case first element plus sum of rest:

```python
def sum_list(values):
 if not values:
 return 0
 return values[0] + sum_list(values[1:])
```

Time O(*n*), stack depth O(*n*). An iterative loop uses O(1) extra space and is often preferable for long lists in Python.

**Tree height** — base case no children; recursive case one plus max of subtrees:

```python
class Node:
 def __init__(self, value, left= None, right= None):
 self.value = value
 self.left = left
 self.right = right

def height(root):
 if root is None:
 return 0
 return 1 + max(height(root.left), height(root.right))
```

Matches how [binary trees](../data-structures/binary-search-tree/index.md) are defined: a node plus left and right subtrees.

**Binary search (recursive)** — same logic as the iterative version on [complexity analysis](../complexity/index.md):

```python
def binary_search_rec(
 sorted_values, target, lo, hi
):
 if lo > hi:
 return None
 mid = (lo + hi) // 2
 if sorted_values[mid] == target:
 return mid
 if sorted_values[mid] < target:
 return binary_search_rec(sorted_values, target, mid + 1, hi)
 return binary_search_rec(sorted_values, target, lo, mid - 1)
```

Depth O(log *n*) for *n* elements.

## Recursion vs iteration

| Prefer recursion when | Prefer iteration (or explicit stack) when |
| --- | --- |
| The data is recursive (trees, nested structures) | Depth can reach thousands (risk `RecursionError`) |
| Divide-and-conquer is clearest recursively | You need O(1) auxiliary space |
| Backtracking explores branches | Hot loops in performance-critical code |

Python does **not** guarantee tail-call elimination: a recursive call that is the **last** action still consumes a stack frame. Deep linear recursion should use a loop or an explicit stack (`list` as your own call stack).

## Common mistakes

- **No base case** — function never stops.
- **Base case never reached** — e.g. `factorial(n - 2)` when *n* can be odd and even paths diverge incorrectly.
- **Wrong combine step** — recursive calls are correct but you drop or double-count work when returning.
- **Ignoring stack space** — O(*n*) depth means O(*n*) memory even if each frame does O(1) work.

## Tie-in to complexity

For recursive algorithms, estimate:

- **Time** — (number of recursive calls) × (work per call, excluding deeper calls), or “levels × work per level” for divide-and-conquer.
- **Space** — maximum **depth** of the call tree, plus any allocations at each level.

Example: [merge sort](../algorithms/merge-sort/index.md) has Θ(log *n*) levels and Θ(*n*) merge work per level → Θ(*n* log *n*) time; typical array merge also uses Θ(*n*) extra space for the buffer.

## How to use this in the roadmap

1. Read this page after [complexity analysis](../complexity/index.md).
2. Before Phase 3 (trees), you should be able to write base case + recursive case for a simple tree walk.
3. Before [merge sort](../algorithms/merge-sort/index.md) and [quicksort](../algorithms/quicksort/index.md), trace one small array through the recursive splits.

Further reading: [Recursion (computer science)](https://en.wikipedia.org/wiki/Recursion_(computer_science)) (Wikipedia); Python tutorial on [defining functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions).

[Parent: Data structures and algorithms](../index.md)
