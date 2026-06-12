# [Contains Duplicate](https://leetcode.com/problems/contains-duplicate)

Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.

## Example 1:

Input: nums = [1,2,3,1]
Output: true
Explanation: The element `1` appears at indices 0 and 3.

## Example 2:

Input: nums = [1,2,3,4]
Output: false
Explanation: All elements are distinct.

## Example 3:

Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true

## Constraints:

`1` <= `nums.length` <= `10^5`
`-10^9` <= `nums[i]` <= `10^9`


## Approach

You need to know whether any number appears more than once. Start with the obvious baseline—compare every pair—then upgrade through sorting and finally a one-pass hash set. The hash set is what you should reach for in an interview.

### Brute force: compare every pair

The simplest idea is two nested loops: for each element, scan every element to its right and return `true` as soon as values match.

| Aspect | Detail |
|--------|--------|
| Time | O(n²) — every pair may be checked |
| Space | O(1) — no extra structure beyond loop variables |
| Drawback | Too slow for large arrays |

For `nums = [1, 2, 1, 2, 3]`, comparing `1` at index 0 with `1` at index 2 immediately finds a duplicate.

### Sorting: check adjacent elements

You can improve time by sorting first. After sorting, any duplicate becomes an equal **adjacent** pair.

| Aspect | Detail |
|--------|--------|
| Time | O(n log n) — dominated by the sort |
| Space | O(1) extra if sorting in place (Python's `sorted()` uses O(n)) |
| Trade-off | Better than O(n²), but still not linear |

For `nums = [2, 5, 1, 4, 5]`, sorting gives `[1, 2, 4, 5, 5]`; the adjacent `5`s mean the answer is `true`.

### Hash set: one pass with membership checks

You can do better with a **single left-to-right scan**. Keep a set of numbers seen so far. At each element, ask: *have I already seen this value?*

| Step | Action |
|------|--------|
| 0 | Initialize an empty set, `seen = set()`. |
| 1 | Scan `nums` from left to right. |
| 2 | If `num` is already in `seen`, return `true`. |
| 3 | Otherwise, add `num` to `seen` and continue. |
| 4 | If the loop finishes, return `false`. |

Set membership is O(1) average, so the whole scan is O(n) time at the cost of O(n) extra space—the classic **time-for-space** trade-off.

### Walkthrough: `nums = [2, 1, 5, 4, 5]`

| Step | Current | `seen` before | Result |
|------|---------|---------------|--------|
| 1 | 2 | `{}` | Add `{2}` |
| 2 | 1 | `{2}` | Add `{1}` |
| 3 | 5 | `{1, 2}` | Add `{5}` |
| 4 | 4 | `{1, 2, 5}` | Add `{4}` |
| 5 | 5 | `{1, 2, 4, 5}` | `5` already seen → return `true` |

For `nums = [1, 2, 3, 4]`, every value is new until the loop ends, so the answer is `false`.

### Complexity of the hash set approach

| Time | Space | Why |
|------|-------|-----|
| O(n) | O(n) | One pass; in the worst case every element is stored in the set |

The implementations below lead with the hash set solution, then show sorting and brute force so you can compare trade-offs side by side.

## Solution 1: Hash Set (Best for Interview)

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n)            | O(n)             |

```python
def contains_duplicate_hash_set(nums):
    """
    Hash set solution: return True on first repeated value.

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        bool: True if any value appears at least twice.

    Example:
        contains_duplicate_hash_set([1, 2, 3, 1]) -> True
    """
    seen = set()

    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False
```

```java
public class ContainsDuplicate {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (seen.contains(num)) {
                return true;
            }
            seen.add(num);
        }
        return false;
    }
}
```

## Solution 2: Sorting

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n log n)      | O(n)             |

Uses `sorted(nums)` (O(n) extra space). For in-place sort on a mutable copy, space can be O(1) beyond the input.

```python
def contains_duplicate_sort(nums):
    """
    Sorting solution: duplicates become adjacent after sorting.

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        bool: True if any value appears at least twice.

    Example:
        contains_duplicate_sort([2, 5, 1, 4, 5]) -> True
    """
    sorted_nums = sorted(nums)

    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] == sorted_nums[i - 1]:
            return True

    return False
```

## Solution 3: Brute Force

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n^2)          | O(1)             |

```python
def contains_duplicate_brute_force(nums):
    """
    Brute force: compare every pair of elements.

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        bool: True if any value appears at least twice.

    Example:
        contains_duplicate_brute_force([1, 2, 1, 2, 3]) -> True
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True

    return False
```

## Summary

Run all three approaches with the same input:

```python
if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify nums to test different cases.
    """
    nums = [1, 2, 3, 1]
    print("Hash Set:", contains_duplicate_hash_set(nums))
    print("Sorting:", contains_duplicate_sort(nums))
    print("Brute Force:", contains_duplicate_brute_force(nums))
```
