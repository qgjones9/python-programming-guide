# 3Sum

In this problem, we are given an array of integers and must find every unique triplet that sums to zero.

```text
nums = [-1, 0, 1, 2, -1, -4]
```

In this array, two triplets add to zero:

```text
[-1, -1, 2]   # -1 + -1 + 2 = 0
[-1, 0, 1]    # -1 + 0 + 1 = 0
```

Arrays with repeated values are common. For example, `[-2, -2, -1, -1, -1, 0, 0, 0, 2, 2, 2]` also contains several valid triplets. For clarity, we will work through the smaller example above.

## Step 1: Sort the array

The first step is to sort the array. After sorting:

```text
nums = [-4, -1, -1, 0, 1, 2]
```

Sorting lets us scan in order and use pointers that move predictably toward a target sum.

## Step 2: Think in terms of three pointers

We can conceptually label the three positions in a triplet as **A**, **B**, and **C**:

```python
A + B + C == 0
```

Fix **A** at index `i`. Then the remaining two values must satisfy:

```python
B + C == 0 - nums[i]
```

Define the target for the inner search:

```python
target = 0 - nums[i]
```

So for each choice of **A**, the problem reduces to finding **B** and **C** that sum to `target`.

## Step 3: Fix A, then move B and C

Scan the sorted array from left to right. At each index `i`, treat `nums[i]` as **A** and search the rest of the array with two pointers **B** and **C**.

```python
i = 0          # A points here
left = i + 1   # B starts just right of A
right = len(nums) - 1   # C starts at the end
```

## Step 4: First iteration — A = -4

At the first iteration, `i = 0`, so **A** is `-4`:

```text
nums = [-4, -1, -1, 0, 1, 2]
        A    B              C
        i  left           right
```

Compute the target:

```python
target = 0 - nums[i]   # 0 - (-4) = 4
# B + C must equal 4
```

Now **B** and **C** move toward each other:

```python
while left < right:
    pair_sum = nums[left] + nums[right]

    if pair_sum == target:
        # found a triplet: A, B, C
        left += 1
        right -= 1
    elif pair_sum < target:
        left += 1    # need a larger sum
    else:
        right -= 1   # need a smaller sum
```

For `A = -4`, no pair in the remaining subarray sums to `4`, so this iteration finds nothing. Advance **A** by moving `i` forward and repeat.

## Step 5: Next iteration — A = -1

When `i = 1`, **A** is `-1`:

```text
nums = [-4, -1, -1, 0, 1, 2]
             A    B        C
             i  left     right
```

```python
target = 0 - nums[i]   # 0 - (-1) = 1
# B + C must equal 1
```

Moving **B** and **C** inward:

```text
# left=2, right=5  →  -1 + 2 = 1  ✓
nums = [-4, -1, -1, 0, 1, 2]
             A    B              C
```

Record `[-1, -1, 2]`, then advance both pointers.

```text
# left=3, right=4  →  0 + 1 = 1  ✓
nums = [-4, -1, -1, 0, 1, 2]
             A         B  C
```

Record `[-1, 0, 1]`. **B** and **C** cross, so this iteration is done.

## Step 6: Skip duplicate A — i = 2

When `i = 2`, **A** is again `-1` — the same value as at `i = 1`:

```text
nums = [-4, -1, -1, 0, 1, 2]
                A    B        C
                i  left     right
```

Any triplets starting here would duplicate ones we already found. Skip when **A** repeats:

```python
if i > 0 and nums[i] == nums[i - 1]:
    continue
```

## Step 7: Next iteration — A = 0

When `i = 3`, **A** is `0`:

```text
nums = [-4, -1, -1, 0, 1, 2]
                      A  B  C
                      i left right
```

```python
target = 0 - nums[i]   # 0 - 0 = 0
# B + C must equal 0
```

Check the only pair: `1 + 2 = 3`, which is greater than `0`, so move **C** left. **B** and **C** meet with no match — `0` cannot be part of a valid triplet in this array.

## Step 8: Stop early — A = 1

When `i = 4`, **A** is `1`:

```text
nums = [-4, -1, -1, 0, 1, 2]
                         A  B
                         i left/right
```

```python
target = 0 - nums[i]   # 0 - 1 = -1
```

**B** and **C** would start at the same index (`left = 5`, `right = 5`), so there is no pair to check. More generally, once **A** is positive the remaining values are too — no triplet can sum to zero. Stop the outer loop:

```python
if nums[i] > 0:
    break
```

## Result

After all iterations, the answer is:

```text
[[-1, -1, 2], [-1, 0, 1]]
```

## Why three pointers work

Each outer step fixes one element (**A**). The inner two-pointer pass finds every pair (**B**, **C**) that completes the triplet in **O(n)** time for that fixed **A**. Repeating for each index gives **O(n²)** overall—much better than three nested loops at **O(n³)**.

The core idea stays the same throughout:

```python
# for each A at index i
target = 0 - nums[i]

# find B and C such that
nums[left] + nums[right] == target
```

When duplicates appear in the sorted array, skip repeated values at **A**, **B**, and **C** so each unique triplet is recorded only once.
