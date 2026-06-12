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
