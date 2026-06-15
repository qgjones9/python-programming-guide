"""
3Sum - Multiple Solutions

Given an integer array nums, find all unique triplets that sum to zero.

Example:
    nums = [-1, 0, 1, 2, -1, -4]
    Output: [[-1, -1, 2], [-1, 0, 1]]

Author: python-programming-guide
"""


def three_sum_two_pointers(nums, debug=False):
    """
    Sort, fix one element, then two-pointer search for the remaining pair.

    Time Complexity: O(n^2)
    Space Complexity: O(1) excluding output and sort space

    Args:
        nums (List[int]): Input array of integers.
        debug (bool): When True, print each step of the search.

    Returns:
        List[List[int]]: Unique triplets that sum to zero.

    Example:
        three_sum_two_pointers([-1, 0, 1, 2, -1, -4]) -> [[-1, -1, 2], [-1, 0, 1]]
    """
    def log(message="", end="\n"):
        if debug:
            print(message, end=end)

    nums.sort()
    log(f"sorted nums: {nums}")
    result = []

    n = len(nums) - 2
    for index in range(n):
        anchor = nums[index]
        if index > 0 and anchor == nums[index - 1]:
            log(f"index={index} anchor={anchor} -> skip duplicate")
            continue
        if anchor > 0:
            log(
                f"index={index} anchor={anchor} > 0 -> break "
                "(remaining triplets cannot sum to 0)"
            )
            break

        left = index + 1
        right = len(nums) - 1
        log(
            f"index={index} anchor={anchor} -> "
            f"start two pointers left={left} right={right}"
        )

        while left < right:
            left_val = nums[left]
            right_val = nums[right]
            total = anchor + left_val + right_val
            log(
                f"  index={index} left={left}({left_val}) "
                f"right={right}({right_val}) total={total}",
                end="",
            )
            if total == 0:
                triplet = [anchor, left_val, right_val]
                result.append(triplet)
                log(f" -> found {triplet}")
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    log(f"  skip duplicate left at {left}({nums[left]})")
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    log(f"  skip duplicate right at {right}({nums[right]})")
                    right -= 1
            elif total < 0:
                log(" -> total < 0, move left")
                left += 1
            else:
                log(" -> total > 0, move right")
                right -= 1

    log(f"result: {result}")
    return result


def three_sum_brute_force(nums):
    """
    Check every distinct triplet; deduplicate with a set of sorted tuples.

    Time Complexity: O(n^3)
    Space Complexity: O(n) for the deduplication set

    Args:
        nums (List[int]): Input array of integers.

    Returns:
        List[List[int]]: Unique triplets that sum to zero.

    Example:
        three_sum_brute_force([-1, 0, 1, 2, -1, -4]) -> [[-1, -1, 2], [-1, 0, 1]]
    """
    nums.sort()
    triplets = set()

    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 0:
                    triplets.add((nums[i], nums[j], nums[k]))

    return [list(triplet) for triplet in triplets]


if __name__ == "__main__":
    """
    Run example tests for each solution.
    Modify walkthrough to test different cases.
    """
    walkthrough = [-1, 0, 1, 2, -1, -4]
    print("Two pointers:", three_sum_two_pointers(walkthrough.copy()))
    print()
    print("--- step-by-step trace ---")
    three_sum_two_pointers(walkthrough.copy(), debug=True)
    # print("Brute force:", three_sum_brute_force(walkthrough))
