"""
Find Minimum in Rotated Sorted Array - Multiple Solutions

Given a sorted array that has been rotated, find the minimum element.

Example:
    nums = [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    Output: 0

Author: python-programming-guide
"""


def find_min_decreasing_pivot(nums):
    """
    Modified binary search: locate the decreasing pivot (minimum).

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        nums (List[int]): Rotated sorted array of unique integers.

    Returns:
        int: Minimum element in the array.

    Example:
        find_min_decreasing_pivot([6, 7, 8, 9, 0, 1, 2, 3, 4, 5]) -> 0
    """
    if len(nums) == 1:
        return nums[0]
    if nums[0] < nums[-1]:
        return nums[0]

    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2

        if mid + 1 <= right and nums[mid + 1] < nums[mid]:
            return nums[mid + 1]
        if mid > left and nums[mid] < nums[mid - 1]:
            return nums[mid]

        if nums[left] <= nums[mid]:
            left = mid + 1
        else:
            right = mid

    return nums[left]


def find_min_mid_vs_right(nums):
    """
    Compact binary search: compare nums[mid] with nums[right].

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        nums (List[int]): Rotated sorted array of unique integers.

    Returns:
        int: Minimum element in the array.

    Example:
        find_min_mid_vs_right([3, 4, 5, 1, 2]) -> 1
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]


def find_min_linear(nums):
    """
    Linear scan: track the smallest value seen.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        nums (List[int]): Rotated sorted array of unique integers.

    Returns:
        int: Minimum element in the array.

    Example:
        find_min_linear([4, 5, 6, 7, 0, 1, 2]) -> 0
    """
    return min(nums)


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify walkthrough to test different cases.
    """
    walkthrough = [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    print("Decreasing pivot:", find_min_decreasing_pivot(walkthrough))
    print("Mid vs right:", find_min_mid_vs_right(walkthrough))
    print("Linear:", find_min_linear(walkthrough))
