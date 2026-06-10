import pytest
from maxheap import MaxHeap


def test_empty_heap_peek_and_pop():
    heap = MaxHeap()
    assert heap.peek() is False
    assert heap.pop() is False


def test_push_and_peek():
    heap = MaxHeap()
    heap.push(3)
    heap.push(10)
    heap.push(5)
    assert heap.peek() == 10


def test_pop_single_element():
    heap = MaxHeap()
    heap.push(42)
    assert heap.peek() == 42
    assert heap.pop() == 42
    assert heap.peek() is False
    assert heap.pop() is False


def test_pop_two_elements():
    heap = MaxHeap()
    heap.push(1)
    heap.push(2)
    assert heap.pop() == 2
    assert heap.pop() == 1
    assert heap.pop() is False


def test_pop_returns_elements_in_descending_order():
    heap = MaxHeap()
    values = [4, 1, 7, 3, 9, 2, 8, 5, 6]
    for value in values:
        heap.push(value)
    popped = []
    while heap.peek() is not False:
        popped.append(heap.pop())
    assert popped == sorted(values, reverse=True)


def test_init_with_items():
    heap = MaxHeap([4, 1, 7, 3, 9, 2])
    assert heap.peek() == 9
    popped = []
    while heap.peek() is not False:
        popped.append(heap.pop())
    assert popped == [9, 7, 4, 3, 2, 1]


def test_push_after_pops_maintains_max_heap():
    heap = MaxHeap()
    for value in [10, 20, 15]:
        heap.push(value)
    assert heap.pop() == 20
    heap.push(25)
    heap.push(5)
    assert heap.peek() == 25
    assert heap.pop() == 25
    assert heap.pop() == 15
    assert heap.pop() == 10
    assert heap.pop() == 5
    assert heap.pop() is False


def test_duplicate_values():
    heap = MaxHeap()
    for value in [5, 5, 5, 3, 3]:
        heap.push(value)
    assert heap.pop() == 5
    assert heap.pop() == 5
    assert heap.pop() == 5
    assert heap.pop() == 3
    assert heap.pop() == 3
    assert heap.pop() is False


def test_negative_values():
    heap = MaxHeap()
    for value in [-3, -1, -10, 0, 2]:
        heap.push(value)
    assert heap.pop() == 2
    assert heap.pop() == 0
    assert heap.pop() == -1
    assert heap.pop() == -3
    assert heap.pop() == -10
