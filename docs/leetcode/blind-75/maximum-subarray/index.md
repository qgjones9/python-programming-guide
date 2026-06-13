# [Maximum Subarray](https://leetcode.com/problems/maximum-subarray)

Given an integer array `nums`, find the **contiguous subarray** (containing at least one number) which has the **largest sum** and return its sum.

A **subarray** is a contiguous non-empty sequence of elements within an array.

## Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray `[4, -1, 2, 1]` has the largest sum `6`.

## Example 2:

Input: nums = [1]
Output: 1

## Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray `[5, 4, -1, 7, 8]` has the largest sum `23`.

## Constraints:

`1` <= `nums.length` <= `10^5`
`-10^4` <= `nums[i]` <= `10^4`


## Approach

You need the largest sum among all **continuous** subarrays. Start with the obvious baseline—generate every contiguous subarray and track the best sum—then upgrade to Kadane's algorithm with two running variables. That second approach is what you should reach for in an interview.

### Brute force: all contiguous subarrays

The simplest idea is two nested loops: fix a start index, extend the end index, compute each subarray sum, and keep the maximum.

| Aspect | Detail |
|--------|--------|
| Time | O(n²) — every contiguous subarray may be summed |
| Space | O(1) — only loop variables and running max |
| Drawback | Too slow when `n` is large |

For `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`, the best subarray is `[4, -1, 2, 1]` with sum `6`.

### Kadane's algorithm: `current` and `max`

You can do better with a **single left-to-right scan** and two variables:

| Variable | Role |
|----------|------|
| `current` | Maximum subarray sum **ending at the current index** |
| `max` | Best subarray sum seen anywhere in the array so far |

At each element `nums[i]`, either extend the subarray ending at the previous index, or start fresh at `nums[i]`:

$$
\text{current} = \max(\text{nums}[i],\ \text{current} + \text{nums}[i])
$$

Then update the global best:

$$
\text{max} = \max(\text{max},\ \text{current})
$$

| Step | Action |
|------|--------|
| 0 | Set `current = nums[0]` and `max = nums[0]`. |
| 1 | Walk `nums` from index `1` to the end. |
| 2 | Update `current` — extend the running subarray or restart at `nums[i]`. |
| 3 | Update `max` with the best sum seen so far. |
| 4 | Return `max`. |

**Intuition:** if the running sum before `nums[i]` is negative, dropping it and starting at `nums[i]` cannot hurt the maximum ending here. That is why `max(nums[i], current + nums[i])` works.

### Walkthrough: `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| Index | `nums[i]` | `current` after update | `max` after update |
|-------|-----------|------------------------|--------------------|
| 0 | -2 | -2 | -2 |
| 1 | 1 | max(1, -2+1) = 1 | 1 |
| 2 | -3 | max(-3, 1-3) = -2 | 1 |
| 3 | 4 | max(4, -2+4) = 4 | 4 |
| 4 | -1 | max(-1, 4-1) = 3 | 4 |
| 5 | 2 | max(2, 3+2) = 5 | 5 |
| 6 | 1 | max(1, 5+1) = 6 | 6 |
| 7 | -5 | max(-5, 6-5) = 1 | 6 |
| 8 | 4 | max(4, 1+4) = 5 | 6 |

The answer is `6`, from subarray `[4, -1, 2, 1]`. One pass, two variables—O(n) time and O(1) space.

### Kadane's algorithm: reset when negative (alternative)

The same O(n) scan appears often on LeetCode with a running sum that **resets to zero** once it goes negative:

| Step | Action |
|------|--------|
| 1 | Add `nums[i]` to a running `current_sum`. |
| 2 | If `current_sum > best`, update `best`. |
| 3 | If `current_sum < 0`, set `current_sum = 0` (drop the prefix; it cannot help any future subarray). |

When `current_sum` is reset and the next element is added, that is equivalent to `max(nums[i], current + nums[i])` — both are Kadane's algorithm.

| Aspect | `current` / `best` (extend or restart) | Reset when negative |
|--------|----------------------------------------|---------------------|
| Time / space | O(n) / O(1) | O(n) / O(1) |
| Matches the recurrence above | Yes — direct DP framing | Indirect — reset is a consequence of the same rule |
| Initialization | `current = best = nums[0]`; loop from index `1` | `current_sum = 0`, `best = -∞`; loop all elements |
| Easy to memorize | Slightly more formal | Very common LeetCode template |

**Bottom line:** neither variant is faster or more correct for this problem. Prefer **`current` / `best`** in an interview because it matches the recurrence and walkthrough above. It also extends more cleanly if you later need **indices of the best subarray** — when `current` restarts at `nums[i]`, record that index as the new subarray start; the reset version only tells you when to drop a prefix, not where a winning subarray began.

### Complexity of Kadane's algorithm

| Time | Space | Why |
|------|-------|-----|
| O(n) | O(1) | One left-to-right pass; only two scalars are stored |

The implementations below lead with the extend-or-restart form, then the reset variant, then brute force so you can compare trade-offs side by side.

## Implementation

Runnable code: [main.py](main.py)

## Solution 1: Kadane's Algorithm — extend or restart (Best for Interview)

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n)            | O(1)             |

```python
def max_subarray_kadane(nums):
    """
    Kadane's algorithm: track best sum ending here and best overall.

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        int: Largest sum of any contiguous subarray.

    Example:
        max_subarray_kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6
    """
    current = nums[0]
    best = nums[0]

    for i in range(1, len(nums)):
        current = max(nums[i], current + nums[i])
        best = max(best, current)

    return best
```

```java
public class MaxSubArray {
    public int maxSubArray(int[] nums) {
        int current = nums[0];
        int best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            current = Math.max(nums[i], current + nums[i]);
            best = Math.max(best, current);
        }
        return best;
    }
}
```

## Solution 2: Kadane's Algorithm — reset when negative

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n)            | O(1)             |

Equivalent to Solution 1; useful if you already know this template. For sum-only answers, either form is fine. Prefer Solution 1 when you may need start/end indices of the best subarray.

```python
def max_subarray_kadane_reset(nums):
    """
    Kadane's algorithm: accumulate a running sum; reset when it goes negative.

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        int: Largest sum of any contiguous subarray.

    Example:
        max_subarray_kadane_reset([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6
    """
    best = float("-inf")
    current_sum = 0

    for num in nums:
        current_sum += num
        best = max(best, current_sum)
        if current_sum < 0:
            current_sum = 0

    return best
```

## Solution 3: Brute Force

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n^2)          | O(1)             |

```python
def max_subarray_brute_force(nums):
    """
    Brute force: sum every contiguous subarray and keep the maximum.

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        int: Largest sum of any contiguous subarray.

    Example:
        max_subarray_brute_force([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6
    """
    best = nums[0]

    for start in range(len(nums)):
        running_sum = 0
        for end in range(start, len(nums)):
            running_sum += nums[end]
            best = max(best, running_sum)

    return best
```

## Summary

Run both approaches with the same input:

```python
if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify nums to test different cases.
    """
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print("Kadane (extend/restart):", max_subarray_kadane(nums))
    print("Kadane (reset):", max_subarray_kadane_reset(nums))
    print("Brute Force:", max_subarray_brute_force(nums))
```

## Internal References

- [Maximum Product Subarray](../maximum-product-subarray/index.md) — same contiguous-subarray pattern with **product**; track min and max running products when negatives flip signs.
