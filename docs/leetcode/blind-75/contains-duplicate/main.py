"""
Contains Duplicate - Multiple Solutions

Given an integer array nums, return True if any value appears at least twice
in the array, and return False if every element is distinct.

Example:
    nums = [1, 2, 3, 1]
    Output: True

Author: python-programming-guide
"""


def contains_duplicate_hash_set(nums):
    """
    Hash set solution: return True on first repeated value.

    Time Complexity: O(n)
    Space Complexity: O(n)

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


def contains_duplicate_sort(nums):
    """
    Sorting solution: duplicates become adjacent after sorting.

    Time Complexity: O(n log n)
    Space Complexity: O(n)

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


def contains_duplicate_brute_force(nums):
    """
    Brute force: compare every pair of elements.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

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


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify nums to test different cases.
    """
    nums = [1, 2, 3, 1]
    print("Hash Set:", contains_duplicate_hash_set(nums))
    print("Sorting:", contains_duplicate_sort(nums))
    print("Brute Force:", contains_duplicate_brute_force(nums))
