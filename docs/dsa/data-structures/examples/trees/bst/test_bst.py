import pytest
from bst import BST

def test_is_empty():
    bst = BST()
    assert bst.is_empty()
    bst.insert(1, "a")
    assert not bst.is_empty()

def test_insert_and_len():
    bst = BST()
    assert len(bst) == 0
    bst.insert(5, "one")
    assert bst.root.key == 5
    assert bst.root.value == "one"
    assert len(bst) == 1

    bst.insert(3, "two")
    assert bst.root.left.key == 3
    assert bst.root.left.value == "two"
    assert len(bst) == 2

    bst.insert(7, "three")
    assert bst.root.right.key == 7
    assert bst.root.right.value == "three"
    assert len(bst) == 3

    # Duplicate key updates value, does not increase count
    bst.insert(5, "one-modified")
    assert bst.root.value == "one-modified"
    assert len(bst) == 3

def test_search():
    bst = BST()
    bst.insert(5, "one")
    bst.insert(3, "two")
    bst.insert(7, "three")
    assert bst.search(5).value == "one"
    assert bst.search(3).value == "two"
    assert bst.search(7).value == "three"
    assert bst.search(4) is None

def test_contains():
    bst = BST()
    bst.insert(5, "one")
    bst.insert(3, "two")
    bst.insert(7, "three")
    assert bst.contains(5)
    assert bst.contains(3)
    assert bst.contains(7)
    assert not bst.contains(4)
    assert not bst.contains(100)

def test_delete_leaf_and_nonleaf():
    bst = BST()
    bst.insert(5, "one")
    bst.insert(3, "two")
    bst.insert(7, "three")

    # delete leaf
    assert bst.delete(3)
    assert not bst.contains(3)
    assert bst.root.left is None
    assert len(bst) == 2

    # delete node with only right child
    bst.insert(8, "four")
    assert bst.delete(7)
    assert not bst.contains(7)
    assert bst.root.right.key == 8
    assert len(bst) == 2

    # delete root node (with only one child)
    assert bst.delete(5)
    assert not bst.contains(5)
    assert bst.root.key == 8
    assert len(bst) == 1

    # delete non-existent node returns False
    assert not bst.delete(42)

def test_minimum():
    bst = BST()
    bst.insert(5, "one")
    bst.insert(3, "two")
    bst.insert(7, "three")
    assert bst.minimum().key == 3
    assert bst.minimum().value == "two"
    # more tricky: add smaller key
    bst.insert(2, "x")
    assert bst.minimum().key == 2

def test_maximum():
    bst = BST()
    bst.insert(5, "one")
    bst.insert(3, "two")
    bst.insert(7, "three")
    assert bst.maximum().key == 7
    assert bst.maximum().value == "three"
    # add larger key
    bst.insert(99, "big")
    assert bst.maximum().key == 99

def test_inorder():
    bst = BST()
    bst.insert(5, "one")
    bst.insert(3, "two")
    bst.insert(7, "three")
    assert bst.inorder() == [3, 5, 7]
    bst.insert(4, "mid")
    bst.insert(8, "biggest")
    assert bst.inorder() == [3, 4, 5, 7, 8]
    # empty tree
    bst2 = BST()
    assert bst2.inorder() == []

def test_preorder():
    bst = BST()
    bst.insert(6, "a")
    bst.insert(4, "l")
    bst.insert(8, "r")
    bst.insert(1, "ll")
    bst.insert(5, "lm")
    assert bst.preorder() == [6, 4, 1, 5, 8]

def test_postorder():
    bst = BST()
    bst.insert(6, "a")
    bst.insert(4, "l")
    bst.insert(8, "r")
    bst.insert(1, "ll")
    bst.insert(5, "lm")
    assert bst.postorder() == [1, 5, 4, 8, 6]

def test_inorder_iter():
    bst = BST()
    bst.insert(5, "one")
    bst.insert(3, "two")
    bst.insert(7, "three")
    assert list(bst.inorder_iter()) == [3, 5, 7]
    # check empty
    bst2 = BST()
    assert list(bst2.inorder_iter()) == []

def test_preorder_iter():
    bst = BST()
    bst.insert(5, "a")
    bst.insert(2, "b")
    bst.insert(6, "c")
    bst.insert(1, "d")
    bst.insert(3, "e")
    assert list(bst.preorder_iter()) == [5, 2, 1, 3, 6]

def test_postorder_iter():
    bst = BST()
    bst.insert(5, "a")
    bst.insert(2, "b")
    bst.insert(6, "c")
    bst.insert(1, "d")
    bst.insert(3, "e")
    assert list(bst.postorder_iter()) == [1, 3, 2, 6, 5]

def test_level_order():
    bst = BST()
    bst.insert(6, "a")
    bst.insert(3, "b")
    bst.insert(9, "c")
    bst.insert(1, "d")
    bst.insert(5, "e")
    assert list(bst.level_order()) == [6, 3, 9, 1, 5]
    # empty
    bst2 = BST()
    assert list(bst2.level_order()) == []

def test_level_order_iter():
    bst = BST()
    bst.insert(5, "a")
    bst.insert(2, "l")
    bst.insert(7, "r")
    bst.insert(1, "ll")
    bst.insert(3, "lm")
    assert list(bst.level_order_iter()) == [5, 2, 7, 1, 3]

def test_height():
    bst = BST()
    assert bst.height() == -1
    bst.insert(5, "root")
    assert bst.height() == 0
    bst.insert(3, "left")
    assert bst.height() == 1
    bst.insert(7, "right")
    assert bst.height() == 1
    bst.insert(2, "ll")
    assert bst.height() == 2
    bst.insert(8, "rr")
    assert bst.height() == 2

def test_range_query():
    bst = BST()
    for k in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        bst.insert(k, str(k))
    # Query covering all
    assert bst.range_query(1, 14) == [1, 3, 4, 6, 7, 8, 10, 13, 14]
    # Query a mid-range
    assert bst.range_query(4, 10) == [4, 6, 7, 8, 10]
    # Query with no hits
    assert bst.range_query(20, 22) == []
    # Single value in range
    assert bst.range_query(13, 13) == [13]

def test_to_list_and_from_list():
    # to_list
    bst = BST()
    for k in [5, 2, 8, 1, 3]:
        bst.insert(k, str(k))
    assert bst.to_list() == [1, 2, 3, 5, 8]
    # from_list
    bst2 = BST()
    bst2.from_list([4, 7, 2])
    assert bst2.to_list() == [2, 4, 7]

def test_dunder_str_repr_eq_ne_lt():
    bst1 = BST()
    bst2 = BST()
    bst1.from_list([1, 2, 3])
    bst2.from_list([1, 2, 3])
    # __str__ and __repr__
    assert str(bst1) == "[1, 2, 3]"
    assert repr(bst1).startswith("BST([1, 2, 3])")
    # __eq__ and __ne__
    assert bst1 == bst2
    bst2.insert(5, "new")
    assert bst1 != bst2
    # __lt__ comparison
    bst3 = BST()
    bst3.from_list([0, 1])
    assert bst3 < bst1
    assert not (bst1 < bst3)
    # __iter__
    keys = []
    for k in bst1:
        keys.append(k)
    assert keys == [1, 2, 3]