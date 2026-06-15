# Container With Most Water

You are given an array of integers where each value is the height of a vertical line. Pick two lines to form the sides of a container; the x-axis is the base. Return the maximum amount of water the container can hold.

```text
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
```

Each index is a line on a plane:

```text
index:  0  1  2  3  4  5  6  7  8
height: 1  8  6  2  5  4  8  3  7
```

Visually, the best container uses the lines at **index 1** (height 8) and **index 8** (height 7). We will confirm that with the formula first, then solve the problem efficiently with two pointers.

## Step 1: Compute area for one container

Water cannot rise above the shorter of the two boundary lines. For lines at indices `left` and `right`:

```python
width = right - left
bounded_height = min(height[left], height[right])
area = width * bounded_height
```

For indices **1** and **8**:

```text
left = 1, right = 8
width = 8 - 1 = 7
bounded_height = min(8, 7) = 7
area = 7 * 7 = 49
```

The taller line at index 1 does not increase capacity — water would spill over the shorter line at index 8.

## Step 2: Compare another pair

Check indices **1** and **6** (both height 8):

```text
left = 1, right = 6
width = 6 - 1 = 5
bounded_height = min(8, 8) = 8
area = 5 * 8 = 40
```

`49 > 40`, so the container between indices 1 and 8 holds more water. The answer for this input is **49**.

## Step 3: Brute force baseline

Try every pair of indices `(i, j)` with `i < j`, compute area, and track the maximum.

```python
def max_area_brute_force(height):
    best = 0
    n = len(height)
    for left in range(n):
        for right in range(left + 1, n):
            w = right - left
            h = min(height[left], height[right])
            best = max(best, w * h)
    return best
```

This is correct but slow: **O(n²)** time for **n** lines.

## Step 4: Two pointers — setup

Place one pointer at the **leftmost** line and one at the **rightmost** line:

```python
left = 0
right = len(height) - 1
best = 0
```

```text
height = [1, 8,  6,  2,  5,  4,  8,  3,  7]
          L                              R
          0                              8
```

At each step:

1. Compute area for the current pair.
2. Update `best` if the area is larger.
3. Move **one** pointer inward.

## Step 5: Which pointer moves?

Always move the pointer at the **shorter** line.

If `height[left] < height[right]`, increment `left`. Otherwise decrement `right`.

```python
while left < right:
    w = right - left
    h = min(height[left], height[right])
    best = max(best, w * h)

    if height[left] < height[right]:
        left += 1
    else:
        right -= 1

return best
```

Why this is safe: shrinking width always happens when a pointer moves. Keeping the shorter line fixed cannot help — the height is capped by that short line, and width only gets smaller. The only way to find a taller effective boundary is to advance the shorter side and hope the new partner is taller.

## Step 6: First iteration — left = 0, right = 8

```text
height = [1, 8,  6,  2,  5,  4,  8,  3,  7]
          L                              R
```

```python
w = 8 - 0 = 8
h = min(1, 7) = 1
area = 8
best = 8
# height[left] < height[right]  →  move left
```

## Step 7: Second iteration — left = 1, right = 8

```text
height = [1, 8,  6,  2,  5,  4,  8,  3,  7]
             L                           R
```

```python
w = 8 - 1 = 7
h = min(8, 7) = 7
area = 49
best = 49
# height[left] > height[right]  →  move right
```

This is the best area we will see for this array.

## Step 8: Third iteration — left = 1, right = 7

```text
height = [1, 8,  6,  2,  5,  4,  8,  3,  7]
             L                        R
```

```python
w = 7 - 1 = 6
h = min(8, 3) = 3
area = 18
best = 49   # unchanged
# move right (3 < 8)
```

## Step 9: Fourth iteration — left = 1, right = 6

```text
height = [1, 8,  6,  2,  5,  4,  8,  3,  7]
             L                     R
```

```python
w = 6 - 1 = 5
h = min(8, 8) = 8
area = 40
best = 49   # unchanged
# equal heights  →  move right (either side is valid)
```

This matches the manual comparison from Step 2: 40 is less than 49.

## Step 10: Continue until pointers meet

| Step | left | right | width | min height | area | best | move |
|------|------|-------|-------|------------|------|------|------|
| 1 | 0 | 8 | 8 | 1 | 8 | 8 | left |
| 2 | 1 | 8 | 7 | 7 | **49** | **49** | right |
| 3 | 1 | 7 | 6 | 3 | 18 | 49 | right |
| 4 | 1 | 6 | 5 | 8 | 40 | 49 | right |
| 5 | 1 | 5 | 4 | 4 | 16 | 49 | right |
| 6 | 1 | 4 | 3 | 5 | 15 | 49 | right |
| 7 | 1 | 3 | 2 | 2 | 4 | 49 | right |
| 8 | 1 | 2 | 1 | 6 | 6 | 49 | right |

After step 8, `left = 1` and `right = 2`. The loop stops when `left >= right`.

## Result

```text
49
```

The optimal container spans indices **1** and **8**.

## Why two pointers work

Every brute-force pair `(i, j)` is still considered implicitly. When the wider window `(left, right)` is evaluated, moving the shorter boundary inward discards only pairs that cannot beat the current best:

- Width decreases on every move.
- Area is limited by `min(height[left], height[right])`.
- Advancing the taller line cannot increase the minimum height while width shrinks.

Each pointer moves at most **n − 1** times, so the scan is **O(n)** time and **O(1)** extra space — a strict improvement over **O(n²)** brute force.

The core loop:

```python
while left < right:
    best = max(best, (right - left) * min(height[left], height[right]))
    if height[left] < height[right]:
        left += 1
    else:
        right -= 1
```

When `height[left] == height[right]`, moving either pointer is correct; the implementation above moves `right`.
