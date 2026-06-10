import pytest
from minheap import MinHeap


def test_empty_heap_raises():
    heap = MinHeap()
    assert heap.is_empty()
    assert len(heap) == 0
    with pytest.raises(IndexError):
        heap.peek_min()
    with pytest.raises(IndexError):
        heap.extract_min()


def test_insert_and_peek_min():
    heap = MinHeap()
    heap.insert(3)
    heap.insert(10)
    heap.insert(5)
    assert heap.peek_min() == 3
    assert heap.validate()


def test_extract_min_single_element():
    heap = MinHeap()
    heap.insert(42)
    assert heap.peek_min() == 42
    assert heap.extract_min() == 42
    assert heap.is_empty()
    with pytest.raises(IndexError):
        heap.peek_min()


def test_extract_min_two_elements():
    heap = MinHeap()
    heap.insert(2)
    heap.insert(1)
    assert heap.extract_min() == 1
    assert heap.extract_min() == 2
    assert heap.is_empty()


def test_extract_min_returns_ascending_order():
    heap = MinHeap()
    values = [4, 1, 7, 3, 9, 2, 8, 5, 6]
    for value in values:
        heap.insert(value)
        assert heap.validate()
    popped = []
    while not heap.is_empty():
        popped.append(heap.extract_min())
    assert popped == sorted(values)


def test_init_with_items_heapifies():
    heap = MinHeap([4, 1, 7, 3, 9, 2])
    assert heap.validate()
    assert heap.peek_min() == 1
    popped = []
    while not heap.is_empty():
        popped.append(heap.extract_min())
    assert popped == [1, 2, 3, 4, 7, 9]


def test_insert_after_extracts_maintains_min_heap():
    heap = MinHeap()
    for value in [10, 20, 15]:
        heap.insert(value)
    assert heap.extract_min() == 10
    heap.insert(5)
    heap.insert(25)
    assert heap.peek_min() == 5
    assert heap.extract_min() == 5
    assert heap.extract_min() == 15
    assert heap.extract_min() == 20
    assert heap.extract_min() == 25
    assert heap.is_empty()


def test_duplicate_values():
    heap = MinHeap()
    for value in [5, 5, 5, 3, 3]:
        heap.insert(value)
    assert heap.extract_min() == 3
    assert heap.extract_min() == 3
    assert heap.extract_min() == 5
    assert heap.extract_min() == 5
    assert heap.extract_min() == 5
    assert heap.is_empty()


def test_negative_values():
    heap = MinHeap()
    for value in [-3, -1, -10, 0, 2]:
        heap.insert(value)
    assert heap.extract_min() == -10
    assert heap.extract_min() == -3
    assert heap.extract_min() == -1
    assert heap.extract_min() == 0
    assert heap.extract_min() == 2
    assert heap.is_empty()


def test_from_pairs_and_extract_entry():
    heap = MinHeap.from_pairs([(5, "a"), (2, "b"), (8, "c"), (1, "d")])
    assert heap.validate()
    assert heap.peek_entry() == (1, "d")
    results = []
    while not heap.is_empty():
        results.append(heap.extract_entry())
    assert results == [(1, "d"), (2, "b"), (5, "a"), (8, "c")]


def test_copy_of_is_independent():
    orig = MinHeap([3, 1, 4])
    copy = MinHeap.copy_of(orig)
    assert copy.validate()
    assert copy.to_list() == orig.to_list()
    orig.extract_min()
    assert copy.peek_min() == 1


def test_replace_min_larger_and_smaller():
    heap = MinHeap([5, 3, 7, 1])
    old = heap.replace_min(10)
    assert old == 1
    assert heap.peek_min() == 3
    assert heap.validate()

    heap2 = MinHeap([5, 3, 7])
    old = heap2.replace_min(0)
    assert old == 3
    assert heap2.peek_min() == 0
    assert heap2.validate()


def test_replace_min_on_empty_heap():
    heap = MinHeap()
    returned = heap.replace_min(7)
    assert returned == 7
    assert heap.peek_min() == 7


def test_decrease_key_at():
    heap = MinHeap([10, 5, 15, 3, 7])
    idx = next(i for i, e in enumerate(heap._data) if e.key == 10)
    heap.decrease_key_at(idx, 1)
    assert heap.peek_min() == 1
    assert heap.validate()

    with pytest.raises(ValueError):
        heap.decrease_key_at(idx, 100)


def test_decrease_key_at_invalid_index():
    heap = MinHeap([1, 2, 3])
    with pytest.raises(IndexError):
        heap.decrease_key_at(10, 0)


def test_clear_and_to_list():
    heap = MinHeap([4, 2, 6])
    assert sorted(heap.to_list()) == [2, 4, 6]
    heap.clear()
    assert heap.is_empty()
    assert heap.to_list() == []


def test_iter_yields_array_order_not_sorted():
    heap = MinHeap([4, 1, 3])
    assert list(heap) == heap.to_list()
