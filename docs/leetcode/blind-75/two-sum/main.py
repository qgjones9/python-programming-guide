"""
Two Sum Problem - Multiple Solutions

Given an array of integers `nums` and an integer `target`, find two indices such that the numbers at those indices add up to the target.
Assume that each input will have exactly one solution, and the same element cannot be used twice. Indices can be returned in any order.

Below are multiple approaches to solve the problem, each with its own time and space complexity.

Example:
    nums = [2, 1, 3, 5, 8]
    target = 9
    Output: [1, 4] because nums[1] + nums[4] == 9

Author: python-programming-guide
"""

def two_sum_brute_force(nums, target):
    """
    Brute Force Solution

    Time Complexity: O(n^2)
    Space Complexity: O(1)

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
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

def two_sum_two_pointers(nums, target):
    """
    Two Pointers Solution (requires sorted array for correct results)
    
    Time Complexity: O(n log n) (due to sorting)
    Space Complexity: O(n) (to store indices)

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
    indexed = sorted(enumerate(nums), key=lambda pair: pair[1])
    left, right = 0, len(indexed) - 1
    while left < right:
        current_sum = indexed[left][1] + indexed[right][1]
        if current_sum == target:
            return sorted([indexed[left][0], indexed[right][0]])
        if current_sum < target:
            left += 1
        else:
            right -= 1
    return []

def two_sum_hash_table(nums, target):
    """
    Hash Table (Dictionary) Solution

    Time Complexity: O(n)
    Space Complexity: O(n)

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
    hash_table = {}
    for i in range(len(nums)):
        if nums[i] in hash_table:
            return [hash_table[nums[i]], i]
        hash_table[target - nums[i]] = i
    return []

def two_sum_binary_search(nums, target):
    """
    Binary Search Solution (requires sorted array for binary search)

    Time Complexity: O(n log n)
    Space Complexity: O(n)

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

if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify nums and target to test different cases.
    """
    nums = [2, 1, 3, 5, 8]
    target = 9
    print("Brute Force:", two_sum_brute_force(nums, target))
    print("Two Pointers:", two_sum_two_pointers(nums, target))
    print("Hash Table:", two_sum_hash_table(nums, target))
    print("Binary Search:", two_sum_binary_search(nums, target))