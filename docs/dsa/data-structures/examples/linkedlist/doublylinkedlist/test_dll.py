import pytest

from dll import DoublyLinkedList

# test helpers
def make_linked_list(values):
    """
    (1) Create an empty linked list.
    (2) Append the values to the linked list.
    (3) Return the linked list.
    """
    ll = DoublyLinkedList()
    for value in values:
        ll.append(value)
    return ll

# dunder methods
def test_str_representation():
    """
    (1) Create a linked list with 3 nodes.
    (2) Assert the string representation of the linked list is the expected value.
    """
    dll = make_linked_list([1, 2, 3])
    assert str(dll) == "DoublyLinkedList([1, 2, 3])"
    assert repr(dll) == "DoublyLinkedList([1, 2, 3])"

def test_repr_representation():
    """
    (1) Create a linked list with 3 nodes.
    (2) Assert the repr representation of the linked list is the expected value.
    """
    dll = make_linked_list([1, 2, 3])
    assert repr(dll) == "DoublyLinkedList([1, 2, 3])"

def test_len_representation():
    """
    (1) Create a linked list with 3 nodes.
    (2) Assert the len representation of the linked list is the expected value.
    """
    dll = make_linked_list([1, 2, 3])
    assert len(dll) == 3

def test_getitem():
    """
    (1) Create a linked list with 3 nodes.
    (2) Assert the value of the node at index 0 is the expected value.
    """
    dll = make_linked_list([1, 2, 3])
    assert dll[0] == 1

# utilities
def test_is_empty():
    """
    (1) Create an empty linked list.
    (2) Assert the linked list is empty.
    """
    dll = make_linked_list([])
    assert dll.is_empty()

# functional methods
def test_push():
    dll = make_linked_list([1, 2, 3])
    dll.push(0)
    assert dll.get(0) == 0

def test_append():
    dll = make_linked_list([1, 2, 3])
    dll.append(4)
    assert dll.get(3) == 4

def test_insert():
    dll = make_linked_list([1, 2, 3])
    dll.insert(1, 4)
    assert dll.get(1) == 4

def test_pop():
    dll = make_linked_list([1, 2, 3])
    assert dll.pop() == 3
    assert dll.get(1) == 2

def test_remove_head():
    dll = make_linked_list([1, 2, 3])
    assert dll.remove(0) == 1
    assert dll.get(0) == 2

def test_remove():
    dll = make_linked_list([1, 2, 3])
    assert dll.remove(1) == 2
    assert dll.get(1) == 3

def test_get():
    """
    (1) Create a linked list with 3 nodes.
    (2) Assert the value of the node at index 0 is the expected value.
    """
    dll = make_linked_list([1, 2, 3])
    assert dll.get(0) == 1

def test_set():
    """
    (1) Create a linked list with 3 nodes.
    (2) Set the value of the node at index 0 to the expected value.
    """
    dll = make_linked_list([1, 2, 3])
    dll.set(0, 4)
    assert dll.get(0) == 4

def test_index_of():
    dll = make_linked_list([1, 2, 3])
    assert dll.index_of(2) == 1

def test_contains():
    dll = make_linked_list([1, 2, 3])
    assert dll.contains(2)
    assert not dll.contains(4)

def test_reverse():
    dll = make_linked_list([1, 2, 3])
    dll.reverse()
    assert dll.get(0) == 3
    assert dll.get(1) == 2
    assert dll.get(2) == 1

def test_to_list():
    dll = make_linked_list([1, 2, 3])
    assert dll.to_list() == [1, 2, 3]

def test_clear():
    dll = make_linked_list([1, 2, 3])
    dll.clear()
    assert dll.is_empty()

def test_extend():
    dll = make_linked_list([1, 2, 3])
    dll.extend([4, 5, 6])
    assert dll.to_list() == [1, 2, 3, 4, 5, 6]

def test_sort():
    dll = make_linked_list([3, 2, 1])
    dll.sort()
    assert dll.to_list() == [1, 2, 3]

def test_copy():
    dll = make_linked_list([1, 2, 3])
    dll_copy = dll.copy()
    assert dll_copy.to_list() == [1, 2, 3]
    assert dll_copy.head is not dll.head
    assert dll_copy.tail is not dll.tail

def test_trim_front():
    dll = make_linked_list([1, 2, 3])
    dll.trim_front(2)
    assert dll.to_list() == [3]

def test_trim_back():
    dll = make_linked_list([1, 2, 3])
    dll.trim_back(2)
    assert dll.to_list() == [1, 2]

def test_latest():
    dll = make_linked_list([1, 2, 3])
    assert dll.latest() == 3

def test_oldest_in_window():
    dll = make_linked_list([1, 2, 3])
    assert dll.oldest_in_window() == 1

def test_current():
    dll = make_linked_list([1, 2, 3])
    assert dll.current() == 1

def test_find_reading():
    dll = make_linked_list([1, 2, 3])
    assert dll.find_reading(2) == 2
    assert dll.find_reading(4) is None

def test_walk_forward_from():
    dll = make_linked_list([1, 2, 3])
    assert dll.walk_forward_from(dll.head) == [1, 2, 3]

def test_walk_backward_from():
    dll = make_linked_list([1, 2, 3])
    assert dll.walk_backward_from(dll.tail) == [3, 2, 1]
