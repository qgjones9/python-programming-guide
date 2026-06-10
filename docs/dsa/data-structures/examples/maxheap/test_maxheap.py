import pytest
from maxheap import MaxHeap


def test_empty_heap_raises():
    heap = MaxHeap()
    assert heap.is_empty()
    assert len(heap) == 0
    with pytest.raises(IndexError):
        heap.peek_max()
    with pytest.raises(IndexError):
        heap.extract_max()


def test_insert_and_peek_max():
    heap = MaxHeap()
    heap.insert(3)
    heap.insert(10)
    heap.insert(5)
    assert heap.peek_max() == 10
    assert heap.validate()


def test_extract_max_single_element():
    heap = MaxHeap()
    heap.insert(42)
    assert heap.peek_max() == 42
    assert heap.extract_max() == 42
    assert heap.is_empty()
    with pytest.raises(IndexError):
        heap.peek_max()


def test_extract_max_two_elements():
    heap = MaxHeap()
    heap.insert(1)
    heap.insert(2)
    assert heap.extract_max() == 2
    assert heap.extract_max() == 1
    assert heap.is_empty()


def test_extract_max_returns_descending_order():
    heap = MaxHeap()
    values = [4, 1, 7, 3, 9, 2, 8, 5, 6]
    for value in values:
        heap.insert(value)
        assert heap.validate()
    popped = []
    while not heap.is_empty():
        popped.append(heap.extract_max())
    assert popped == sorted(values, reverse=True)


def test_init_with_items_heapifies():
    heap = MaxHeap([4, 1, 7, 3, 9, 2])
    assert heap.validate()
    assert heap.peek_max() == 9
    popped = []
    while not heap.is_empty():
        popped.append(heap.extract_max())
    assert popped == [9, 7, 4, 3, 2, 1]


def test_insert_after_extracts_maintains_max_heap():
    heap = MaxHeap()
    for value in [10, 20, 15]:
        heap.insert(value)
    assert heap.extract_max() == 20
    heap.insert(25)
    heap.insert(5)
    assert heap.peek_max() == 25
    assert heap.extract_max() == 25
    assert heap.extract_max() == 15
    assert heap.extract_max() == 10
    assert heap.extract_max() == 5
    assert heap.is_empty()


def test_duplicate_values():
    heap = MaxHeap()
    for value in [5, 5, 5, 3, 3]:
        heap.insert(value)
    assert heap.extract_max() == 5
    assert heap.extract_max() == 5
    assert heap.extract_max() == 5
    assert heap.extract_max() == 3
    assert heap.extract_max() == 3
    assert heap.is_empty()


def test_negative_values():
    heap = MaxHeap()
    for value in [-3, -1, -10, 0, 2]:
        heap.insert(value)
    assert heap.extract_max() == 2
    assert heap.extract_max() == 0
    assert heap.extract_max() == -1
    assert heap.extract_max() == -3
    assert heap.extract_max() == -10
    assert heap.is_empty()


def test_from_pairs_and_extract_entry():
    heap = MaxHeap.from_pairs([(5, "a"), (2, "b"), (8, "c"), (1, "d")])
    assert heap.validate()
    assert heap.peek_entry() == (8, "c")
    results = []
    while not heap.is_empty():
        results.append(heap.extract_entry())
    assert results == [(8, "c"), (5, "a"), (2, "b"), (1, "d")]


def test_copy_of_is_independent():
    orig = MaxHeap([3, 1, 4])
    copy = MaxHeap.copy_of(orig)
    assert copy.validate()
    assert copy.to_list() == orig.to_list()
    orig.extract_max()
    assert copy.peek_max() == 4


def test_replace_max_smaller_and_larger():
    heap = MaxHeap([5, 3, 7, 9])
    old = heap.replace_max(1)
    assert old == 9
    assert heap.peek_max() == 7
    assert heap.validate()

    heap2 = MaxHeap([5, 3, 7])
    old = heap2.replace_max(10)
    assert old == 7
    assert heap2.peek_max() == 10
    assert heap2.validate()


def test_replace_max_on_empty_heap():
    heap = MaxHeap()
    returned = heap.replace_max(7)
    assert returned == 7
    assert heap.peek_max() == 7


def test_increase_key_at():
    heap = MaxHeap([10, 5, 15, 3, 7])
    idx = next(i for i, e in enumerate(heap._data) if e.key == 5)
    heap.increase_key_at(idx, 20)
    assert heap.peek_max() == 20
    assert heap.validate()

    with pytest.raises(ValueError):
        heap.increase_key_at(idx, 1)


def test_increase_key_at_invalid_index():
    heap = MaxHeap([1, 2, 3])
    with pytest.raises(IndexError):
        heap.increase_key_at(10, 100)


def test_clear_and_to_list():
    heap = MaxHeap([4, 2, 6])
    assert sorted(heap.to_list()) == [2, 4, 6]
    heap.clear()
    assert heap.is_empty()
    assert heap.to_list() == []


def test_iter_yields_array_order_not_sorted():
    heap = MaxHeap([4, 1, 3])
    assert list(heap) == heap.to_list()
