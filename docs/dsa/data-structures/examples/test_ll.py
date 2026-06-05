# write a test for the linked list

import pytest
from ll import LinkedList

# test helpers
def make_linked_list(values):
    """
    (1) Create an empty linked list.
    (2) Append the values to the linked list.
    (3) Return the linked list.
    """
    ll = LinkedList()
    for value in values:
        ll.append(value)
    return ll

# dunder methods
def test_str_representation():
    """
    (1) Create an empty linked list.
    (2) Prepend 3 nodes to the linked list.
    (3) Assert the string representation of the linked list is the expected value.
    """
    ll = LinkedList()
    ll.prepend(1) # 1 -> None
    assert str(ll) == "LinkedList([1])"
    ll.prepend(2) # 2 -> 1 -> None
    assert str(ll) == "LinkedList([2, 1])"
    ll.prepend(3) # 3 -> 2 -> 1 -> None
    assert str(ll) == "LinkedList([3, 2, 1])"

def test_repr_representation():
    """
    (1) Create an empty linked list.
    (2) Prepend 3 nodes to the linked list.
    (3) Assert the repr representation of the linked list is the expected value.
    """
    ll = LinkedList()
    ll.prepend(1) # 1 -> None
    assert repr(ll) == "LinkedList([1])"
    ll.prepend(2) # 2 -> 1 -> None
    assert repr(ll) == "LinkedList([2, 1])"
    ll.prepend(3) # 3 -> 2 -> 1 -> None
    assert repr(ll) == "LinkedList([3, 2, 1])"

def test_len_representation():
    """
    (1) Create an empty linked list.
    (2) Prepend 3 nodes to the linked list.
    (3) Assert the length of the linked list is the expected value.
    """
    ll = LinkedList()
    ll.prepend(1) # 1 -> None
    assert len(ll) == 1
    ll.prepend(2) # 2 -> 1 -> None
    assert len(ll) == 2
    ll.prepend(3) # 3 -> 2 -> 1 -> None
    assert len(ll) == 3
# utilities
def test_is_empty():
    """
    (1) Create an empty linked list.
    (2) Assert the linked list is empty.
    (3) Prepend a node to the linked list.
    (4) Assert the linked list is not empty.
    """
    ll = LinkedList()
    assert ll.is_empty()
    ll.prepend(1) # 1 -> None
    assert not ll.is_empty()

def test_get():
    """
    (1) Create a linked list.
    (2) Append 5 nodes to the linked list.
    (3) Get the node at the given index.
    (4) Assert the data from the node is the expected value.
    """

    ll = make_linked_list([0,1,2,3,4])
    assert ll.get(0) == 0
    assert ll.get(1) == 1
    assert ll.get(2) == 2
    assert ll.get(3) == 3
    assert ll.get(4) == 4

def test_set():
    """
    (1) Create a linked list.
    (2) Append 5 nodes to the linked list.
    (3) Set the node at the given index to the expected value.
    (4) Assert the data from the node is the expected value.
    """
    ll = make_linked_list([0,1,2,3,4])
    ll.set(2, 101)
    assert ll.get(2) == 101

# functional methods    
def test_prepend():
    """
    (1) Create an empty linked list.
    (2) Prepend a node to the linked list.
    (3) Assert the head of the linked list is the new node.
    (4) Assert the size of the linked list is 1.
    """
    ll = LinkedList()
    ll.prepend(1) # 1 -> None
    assert ll.head.data == 1
    assert ll.size == 1
    ll.prepend(2) # 2 -> 1 -> None
    assert ll.head.data == 2
    assert ll.size == 2

def test_append():
    """
    (1) Create an empty linked list.
    (2) Append a node to the linked list.
    (3) Assert the head and tail of the linked list are the new node.
    (4) Assert the size of the linked list is 1.
    """
    ll = LinkedList()
    ll.append(1) # 1 -> None
    assert ll.head.data == 1
    assert ll.tail.data == 1
    assert ll.size == 1

def test_insert_head():
    """
    (1) Create an empty linked list.
    (2) Append a node to the linked list.
    (3) Insert a node at the head of the linked list.
    (4) Assert the head of the linked list is the new node.
    """
    ll = LinkedList()
    ll.append(1)
    ll.insert(0, 2)
    assert ll.head.data == 2

def test_insert_tail():
    """
    (1) Create a linked list.
    (2) append 5 nodes to the linked list.
    (3) Insert a node at the tail of the linked list.
    (4) Assert that the tail of the linked list is the new node.
    """
    ll = make_linked_list([0,1,2,3,4])
    ll.insert(len(ll), 1)
    assert ll.tail.data == 1

def test_pop_head():
    """
    (1) Create a linked list.
    (2) Append 4 nodes to the linked list.
    (3) Assert the size of the linked list is 4.
    (4) Pop the head node from the linked list.
    (5) Assert the size of the linked list is 3.
    (6) Assert the data from the head node is 1.
    """

    ll = make_linked_list([1,2,3,4])
    assert ll.size == 4
    popped = ll.pop_head()
    assert ll.size == 3
    assert popped  == 1

def test_pop_tail():
    """
    """
    ll = LinkedList()

    # Testcase: linkedlist is empty    
    try:
        ll.pop_tail()
        assert False, "Expected IndexError when popping tail from empty list"
    except IndexError:
        ...

    # Testcase: single node linkedlist
    ll.append(1)
    assert ll.pop_head() == 1

    # Testcase: multinode linkedlist
    ll = make_linked_list([1,2,3,4])
    assert ll.pop_tail() == 4

def test_remove_at():
    """
    (1) case: empty linkedlist
    (2) case: single node linkedlist
    (3) case: multi node linkedlist
    (4) update the size of the linked list
    (5) return the data from the node that was removed back to the caller
    """
    # Testcase: empty linkedlist
    ll = LinkedList()
    try:
        ll.remove(0)
        assert False, "Expected IndexError when removing from empty list"
    except IndexError:
        pass

    # Testcase: single node linkedlist remove head node
    ll = make_linked_list([1])
    assert ll.remove(0) == 1
    assert ll.size == 0

    # Testcase: multi node linkedlist remove middle node
    ll = make_linked_list([1,2,3,4,5])
    assert ll.remove(2) == 3
    assert ll.size == 4

    # Testcase: multi node linkedlist remove tail node
    ll = make_linked_list([1,2,3,4])
    assert ll.remove(3) == 4
    assert ll.size == 3

def test_index_of():
    """
    """
    # Testcase: found data in node
    ll = make_linked_list(["New York","Los Angelos","Houston","New Orleans"])
    assert ll.index_of("Houston") == 2

    # Testcase: no data found in linkedlist
    try: 
        ll.index_of("Seattle")
    except ValueError:
        ...

def test_contains():
    """
    (1) case: found data in linkedlist
    (2) case: no data found in linkedlist then raise ValueError
    """
    # Testcase: found data in linkedlist
    ll = make_linked_list([1,2,3,4,5])  # 1 -> 2 -> 3 -> 4 -> 5 -> None
    assert ll.contains(1) == True # case: found data in linkedlist then return True
    assert ll.contains(10) == False # case: no data found in linkedlist then raise ValueError

def test_reverse():
    """
    (1) case: empty linkedlist
    (2) case: single node linkedlist
    (3) case: multi node linkedlist
    """
    # Testcase: empty linkedlist
    ll = LinkedList() # empty linkedlist
    ll.reverse() # reverse the empty linkedlist
    assert ll.to_list() == [] # case: empty linkedlist then return empty list

    # Testcase: single node linkedlist
    ll = make_linked_list([1]) # 1 -> None
    ll.reverse() # reverse the linkedlist 1 -> None
    assert ll.to_list() == [1] # case: single node linkedlist then return the reversed list

    # Testcase: multi node linkedlist
    ll = make_linked_list([1,2,3,4,5]) # 1 -> 2 -> 3 -> 4 -> 5 -> None
    ll.reverse() # reverse the linkedlist 5 -> 4 -> 3 -> 2 -> 1 -> None
    assert ll.to_list() == [5, 4, 3, 2, 1] # case: multi node linkedlist then return the reversed list

def test_to_list():
    """
    (1) case: convert linkedlist to list
    """
    # Testcase: convert linkedlist to list
    ll = make_linked_list([1,2,3,4,5]) # 1 -> 2 -> 3 -> 4 -> 5 -> None
    assert ll.to_list() == [1,2,3,4,5] # case: convert linkedlist to list then return the list

def test_clear():
    """
    (1) case: clear linkedlist
    """
    # Testcase: clear linkedlist
    ll = make_linked_list([1,2,3,4,5]) # 1 -> 2 -> 3 -> 4 -> 5 -> None
    ll.clear() # clear the linkedlist
    assert ll.to_list() == [] # case: clear linkedlist then return empty list


def test_extend():
    """
    (1) case: extend linkedlist
    """
    # Testcase: extend linkedlist
    ll = make_linked_list([1,2,3,4,5]) # 1 -> 2 -> 3 -> 4 -> 5 -> None
    ll.extend(make_linked_list([6,7,8,9,10])) # extend the linkedlist with [6,7,8,9,10]
    assert ll.to_list() == [1,2,3,4,5,6,7,8,9,10] # case: extend linkedlist then return the extended list
    assert ll.size == 10 # case: extend linkedlist then return the size of the extended list

def test_sort():
    """
    (1) case: sort linkedlist
    """
    # Testcase: sort linkedlist
    ll = make_linked_list([5,4,3,2,1]) # 5 -> 4 -> 3 -> 2 -> 1 -> None
    ll.sort() # sort the linkedlist
    assert ll.to_list() == [1,2,3,4,5] # case: sort linkedlist then return the sorted list
    assert ll.size == 5 # case: sort linkedlist then return the size of the sorted list


