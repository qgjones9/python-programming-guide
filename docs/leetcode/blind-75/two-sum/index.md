# [Two Sum](https://leetcode.com/problems/two-sum)

If given an array of integers and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

## Example 1:

Input: nums = [2,1,3,5,8], target = 9
Output: [1,4]
Explanation: Because nums[1] + nums[4] == 9, we return [1, 4].

## Example 2:

Input: nums = [3,2,4], target = 6
Output: [1,2]

## Example 3:

Input: nums = [3,3], target = 6
Output: [0,1]


## Constraints:
`2` <= `nums.length` <= `10^4`
`-10^9` <= `nums[i]` <= `10^9`
`-10^9` <= `target` <= `10^9`

*Only one valid answer exists.*


## :material-school: What you'll learn

!!! abstract "Learning objectives"
    You will find two indices that sum to a target using a one-pass hash map of complements, compare brute force and sorted-array variants, and explain why a set alone is not enough when the answer must be indices.


## Worked example data

Primary input for the step-by-step trace below:

```text
# primary walkthrough input
nums = [2, 1, 3, 5, 8]
target = 9
# expected output: [1, 4]
```

| Example | Notes | Output |
|---------|-------|--------|
| `[2, 1, 3, 5, 8]`, target `9` | Full walkthrough below | `[1, 4]` |
| `[3, 2, 4]`, target `6` | LeetCode example 2 | `[1, 2]` |
| `[3, 3]`, target `6` | Duplicate values | `[0, 1]` |


## Approach

You need two indices whose values sum to `target`. Start with the obvious baseline—check every pair—then upgrade to a one-pass hash map. That second approach is what you should reach for in an interview.

### Brute force: check every pair

The simplest idea is to try every unique pair of indices with two nested loops and return the first pair whose values add up to `target`. You can code this in minutes, but ask yourself whether it scales.

| Aspect | Detail |
|--------|--------|
| Time | O(n²) — up to every pair may be checked |
| Space | O(1) — no extra structure beyond loop variables |
| Drawback | Too slow for large arrays |

It works for small inputs, but when `n` grows, the nested loops become a bottleneck.

### Hash map: one pass with complements

You can do better by scanning left to right **once**. At each element, ask: *have I already seen the number I need to reach the target?*

For a current value `x`, that needed value is the **complement**:

!!! info "Complement"
    The complement is `target - x`—the value that completes `x` to the target. At index `i`, if that complement is already in your map, you have the pair.

$$
\text{complement} = \text{target} - x
$$

If the complement was seen earlier, we have the pair. Otherwise, record the current value and its index and continue.

!!! warning "Interview trap: set vs hash map"
    A **set** only tells you whether a value exists—it does not store **indices**. This problem requires returning positions, so use a **dictionary** mapping value → index.

Because the problem asks for **indices**, use a **hash map (dictionary)** mapping each seen value to the index where it appeared. That gives O(1) average lookup and lets you return both indices immediately when a match is found.

| Step | Action |
|------|--------|
| 0 | Initialize an empty dictionary, `map = {}`, to store the seen values and their indices. |
| 1 | Scan `nums` from left to right with index `i`, starting at `i = 0`. |
| 2 | Compute `complement = target - nums[i]`. This is the number that, when added to `nums[i]`, equals `target`. |
| 3 | If `complement` is already in the map, return `[map[complement], i]`. This is the pair of indices that add up to `target`. |
| 4 | Otherwise, store `nums[i] : i` in the map and move on. This stores the current number and its index in the map for future lookups. |

That is the classic **time-for-space** trade-off: O(n) time instead of O(n²), at the cost of O(n) extra memory. Memorizing the steps is not enough—understand *why* storing complements as you go makes the second lookup O(1).

### Walkthrough: `nums = [2, 1, 3, 5, 8]`, `target = 9`

| Step | Current | Index | Complement | Map before | Result |
|------|---------|-------|------------|------------|--------|
| 1 | 2 | 0 | 7 | `{}` | Add `{2: 0}` |
| 2 | 1 | 1 | 8 | `{2: 0}` | Add `{1: 1}` |
| 3 | 3 | 2 | 6 | `{2: 0, 1: 1}` | Add `{3: 2}` |
| 4 | 5 | 3 | 4 | `{2: 0, 1: 1, 3: 2}` | Add `{5: 3}` |
| 5 | 8 | 4 | 1 | `{2: 0, 1: 1, 3: 2, 5: 3}` | `1` is in the map at index 1 → return `[1, 4]` |

At index 4, `8` needs complement `1`; we already saw `1` at index 1, so the answer is `[1, 4]` (order does not matter).

!!! success "Walkthrough confirmed"
    For `nums = [2, 1, 3, 5, 8]` and `target = 9`, the hash map returns **`[1, 4]`** when `8` finds complement `1` at index 1.

### Complexity of the hash map approach

| Time | Space | Why |
|------|-------|-----|
| O(n) | O(n) | One left-to-right pass; in the worst case every element is stored in the map |

The implementations below lead with the hash map solution, then show brute force and sorted-array variants so you can compare trade-offs side by side.

## Implementation

Runnable code: [main.py](main.py)

🎯 Reach for the one-pass hash map in an interview—it is the standard O(n) solution.

## Solution 1: Hash Table (Best for Interview)

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n)            | O(n)             |

```python
def two_sum_hash_table(nums, target):
    """
    Hash Table (Dictionary) Solution

    Iterate through the array, for each number check if it's in the hash table (hashtable stores target - value as key, index as value).
    If found, return indices; otherwise, store complement.

    Args:
        nums (List[int]): Input array of integers.
        target (int): The target sum.

    Returns:
        List[int]: Indices of two numbers whose sum equals target.

    Example:
        two_sum_hash_table([2, 1, 3, 5, 8], 9) -> [1, 4]
    """
    seen = {}  # complement -> index where that complement was seen

    for i in range(len(nums)):
        current_num = nums[i] # current_num is the current number in the array
        complement  = target - current_num # complement is the number that, when added to current_num, equals target
        
        if complement in seen: # if the complement is in the seen dictionary, return the indices of the two numbers
            return [seen[complement], i]
        seen[current_num] = i # store the current number and its index in the seen dictionary
    return [] # if no pair is found, return an empty list
```

```java
public class TwoSum {
    public int[] twoSum(int[] nums, int target) {
        // write your code here
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int current_num = nums[i];
            int complement = target - current_num;
            if (seen.containsKey(complement)) {
                return new int[] {seen.get(complement), i};
            }
            seen.put(current_num, i);
        }
        return new int[] {};
    }
}

```

## Solution 2: Brute Force

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n^2)          | O(1)             |

```python
def two_sum_brute_force(nums, target):
    """
    Brute Force Solution

    Iterate through each unique pair in the array and check if the sum matches the target.
    Return the indices of the first matching pair found.

    Args:
        nums (List[int]): Input array of integers.
        target (int): The target sum to achieve with two numbers.

    Returns:
        List[int]: List containing the indices of the two numbers adding up to target, or empty if no solution is found.

    Example:
        two_sum_brute_force([2, 1, 3, 5, 8], 9) -> [1, 4]
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):  # j starts after i to avoid duplicate pairs
            if nums[i] + nums[j] == target:
                return [i, j]
    return []  # no pair found
```

## Solution 3: Two Pointers (on Sorted Array)

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n log n)      | O(n)             |

Two pointers requires a sorted array. Sort `(index, value)` pairs so you can scan values while returning original indices.

```python
def two_sum_two_pointers(nums, target):
    """
    Two Pointers Solution (requires sorted array for correct results)

    Sort nums while keeping track of original indices. Use two pointers at either end of the array to find two numbers whose sum is the target.
    This method is only correct if you're allowed to rearrange the elements, or if the problem allows for sorted input.

    Args:
        nums (List[int]): Input array of integers.
        target (int): The target sum.

    Returns:
        List[int]: List of original indices of the two elements adding up to target, or empty if no solution is found.

    Example:
        two_sum_two_pointers([2, 1, 3, 5, 8], 9) -> [1, 4]
    """
    # Sort by value while preserving original index in each (index, value) pair
    indexed = sorted(enumerate(nums), key=lambda pair: pair[1])
    left, right = 0, len(indexed) - 1
    while left < right:
        current_sum = indexed[left][1] + indexed[right][1]
        if current_sum == target:
            # Return original indices in ascending order
            return sorted([indexed[left][0], indexed[right][0]])
        if current_sum < target:
            left += 1  # need a larger sum
        else:
            right -= 1  # need a smaller sum
    return []
```

## Solution 4: Binary Search (on Sorted Array)

| Time Complexity | Space Complexity |
|-----------------|------------------|
| O(n log n)      | O(n)             |

Binary search also needs sorted values. Keep original indices in `indexed` and search `sorted_vals`.

```python
def two_sum_binary_search(nums, target):
    """
    Binary Search Solution (requires sorted array for binary search)

    First, sort nums along with their original indices. For each number, use binary search to look for its complement in the remaining array.

    Args:
        nums (List[int]): Input array of integers.
        target (int): The target sum.

    Returns:
        List[int]: Indices of two numbers whose sum equals target.

    Example:
        two_sum_binary_search([2, 1, 3, 5, 8], 9) -> [1, 4]
    """
    indexed = sorted(enumerate(nums), key=lambda pair: pair[1])
    sorted_vals = [val for _, val in indexed]
    for i in range(len(sorted_vals)):
        complement = target - sorted_vals[i]
        # Search only to the right of i so the same element is not reused
        left, right = i + 1, len(sorted_vals) - 1
        while left <= right:
            mid = (left + right) // 2
            if sorted_vals[mid] == complement:
                return sorted([indexed[i][0], indexed[mid][0]])
            if sorted_vals[mid] < complement:
                left = mid + 1
            else:
                right = mid - 1
    return []
```

## Summary

Run all four approaches with the same input:

```python
if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify nums and target to test different cases.
    """
    nums = [2, 1, 3, 5, 8]
    target = 9
    print("Hash Table:", two_sum_hash_table(nums, target))
    print("Brute Force:", two_sum_brute_force(nums, target))
    print("Two Pointers:", two_sum_two_pointers(nums, target))
    print("Binary Search:", two_sum_binary_search(nums, target))
```

## Industry scenarios

- 📈 **Portfolio pairs:** Find two holdings whose combined weight hits a target allocation—same complement lookup once values are in a hash map.
- 🔒 **Credential checks:** Pair a user id with a session token that sums (or hashes) to an expected key—two-pointer variants apply when the key space is sorted.
- 🎮 **Loot matching:** Two items whose stat bonuses combine to a build threshold—brute force works for tiny inventories; hash map scales.


## :material-lightbulb: Key takeaways

- 🔑 Store **value → index** as you scan; ask whether `target - nums[i]` was seen already.
- ⚡ One pass with a hash map: O(n) time, O(n) space.
- 🧩 A set answers “exists?” but not “where?”—indices require a map.


## Internal References

- 🔗 [Contains Duplicate](../contains-duplicate/index.md) — hash-set membership pattern without needing indices.


## External References

- :fontawesome-solid-link: [Two Sum — LeetCode #1](https://leetcode.com/problems/two-sum/)
