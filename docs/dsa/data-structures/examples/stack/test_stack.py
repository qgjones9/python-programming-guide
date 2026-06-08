import pytest
from stack import Stack

def test_push():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.size() == 3
    assert stack.peek() == 3
    assert stack.pop() == 3
    assert stack.size() == 2

def test_pop():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.size() == 3
    assert stack.pop() == 3
    assert stack.size() == 2
    assert stack.pop() == 2
    assert stack.size() == 1
    assert stack.pop() == 1
    assert stack.size() == 0

def test_peek():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.peek() == 3
    assert stack.size() == 3
    assert stack.pop() == 3
    assert stack.size() == 2
    assert stack.peek() == 2
    assert stack.size() == 2

def test_is_empty():
    stack = Stack()
    assert stack.is_empty() == True
    stack.push(1)
    assert stack.is_empty() == False
    stack.pop()
    assert stack.is_empty() == True

def test_size():
    stack = Stack()
    assert stack.size() == 0
    stack.push(1)
    assert stack.size() == 1
    stack.push(2)
    assert stack.size() == 2
    stack.pop()
    assert stack.size() == 1
    stack.pop()
    assert stack.size() == 0

def test_str():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert str(stack) == "[1, 2, 3]"
    assert repr(stack) == "Stack([1, 2, 3])"
    assert len(stack) == 3
    assert 1 in stack
    assert 4 not in stack
    assert list(stack) == [1, 2, 3]

def tet_contains():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert 1 in stack
    assert 4 not in stack
    assert 2 in stack
    assert 3 in stack
    assert 4 not in stack
    assert 5 not in stack
    assert 6 not in stack
    assert 7 not in stack

def test_len():
    stack = Stack()
    assert len(stack) == 0
    stack.push(1)
    assert len(stack) == 1
    stack.push(2)
    assert len(stack) == 2
    stack.pop()
    assert len(stack) == 1
    stack.pop()
    assert len(stack) == 0

def test_to_list():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.to_list() == [1, 2, 3]
    assert list(stack) == [1, 2, 3]
    assert len(stack) == 3
    assert 1 in stack
    assert 4 not in stack
    assert 2 in stack
    assert 3 in stack
    assert 4 not in stack