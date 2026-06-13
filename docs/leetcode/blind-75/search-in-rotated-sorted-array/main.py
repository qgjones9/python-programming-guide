"""
Search in Rotated Sorted Array - Multiple Solutions

Given a rotated sorted array and a target value, return the index of target
if found, otherwise return -1.

Example:
    nums = [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    target = 4
    Output: 8

Author: python-programming-guide
"""


def search_rotated_binary(nums, target):
    """
    Modified binary search: identify the sorted half, then keep or discard it.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Args:
        nums (List[int]): Rotated sorted array of unique integers.
        target (int): Value to locate.

    Returns:
        int: Index of target, or -1 if absent.

    Example:
        search_rotated_binary([6, 7, 8, 9, 0, 1, 2, 3, 4, 5], 4) -> 8
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2 # floor division
        if nums[mid] == target: # if the middle element is equal to the target, return the index of the middle element
            return mid

        if nums[left] <= nums[mid]: # if the left element is less than or equal to the middle element, then the left portion of the array is sorted
            if nums[left] <= target <= nums[mid]: # if the target is in the left portion of the array, then we can discard the right portion of the array and search in the left portion of the array
                right = mid - 1 # move the right pointer to the middle of the left portion of the array
            else: # if the target is not in the left portion of the array, then we can discard the left portion of the array and search in the right portion of the array
                left = mid + 1 # move the left pointer to the middle of the right portion of the array
        else:
            if nums[mid] <= target <= nums[right]: # if the target is in the right portion of the array, then we can discard the left portion of the array and search in the right portion of the array
                left = mid + 1 # move the left pointer to the middle of the right portion of the array
            else: # if the target is not in the right portion of the array, then we can discard the right portion of the array and search in the left portion of the array
                right = mid - 1 # move the right pointer to the middle of the left portion of the array

    return -1 # if the target is not in the array, return -1


def search_rotated_linear(nums, target):
    """
    Linear scan: compare target with each element.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Args:
        nums (List[int]): Rotated sorted array of unique integers.
        target (int): Value to locate.

    Returns:
        int: Index of target, or -1 if absent.

    Example:
        search_rotated_linear([4, 5, 6, 7, 0, 1, 2], 0) -> 4
    """
    for i, value in enumerate(nums):
        if value == target:
            return i
    return -1


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify walkthrough to test different cases.
    """
    walkthrough = [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    target = 4
    print("Binary search:", search_rotated_binary(walkthrough, target))
    print("Linear:", search_rotated_linear(walkthrough, target))
