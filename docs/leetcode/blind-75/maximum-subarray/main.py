"""
Maximum Subarray - Multiple Solutions

Given an integer array nums, find the contiguous subarray with the largest
sum and return that sum.

Example:
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    Output: 6  (subarray [4, -1, 2, 1])

Author: python-programming-guide
"""


def max_subarray_kadane(nums):
    """
    Kadane's algorithm: track best sum ending here and best overall.

    Time Complexity: O(n)
    Space Complexity: O(1)

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


def max_subarray_brute_force(nums):
    """
    Brute force: sum every contiguous subarray and keep the maximum.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

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


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify nums to test different cases.
    """
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print("Kadane:", max_subarray_kadane(nums))
    print("Brute Force:", max_subarray_brute_force(nums))
