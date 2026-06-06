# Doubly linked list

A linear collection where **each node** points to both the **next** and **previous** item. You can walk forward from the **head** or backward from the **tail** without rescanning from the front.

| | |
| --- | --- |
| **What it is** | Nodes in a chain: each holds data, a `next` link, and a `prev` link. `head` and `tail` bound the sequence. |
| **Core operations** | O(1) insert/delete at head or tail when you hold the list object; O(1) rewire when you already hold a node reference (manual pointer update). |
| **When to use** | Frequent adds/removes at **both** ends, bidirectional traversal, or algorithms that need the predecessor without a separate scan. |
| **Trade-off** | Two pointers per node (more memory than singly linked); still no O(1) random access by index. |

This page is your **ready reference**: structure, a complete Python implementation, every way to create it, every method with daily weather data examples, and **time and space complexity** on each operation. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

## How a doubly linked list fits daily weather analysis

| Weather analysis idea | Doubly linked view | Why `prev` helps |
| --- | --- | --- |
| **Daily observation chain** | Head = oldest day in window; tail = latest | Walk backward from an unusual or sudden change in data (such as a temperature jump) to see the prior day’s reading |
| **Timeline scrubber** | Current node = day on chart; `next` / `prev` = step forward/back | No full rescan from head for “previous day” |
| **Recent readings buffer** | Fixed window of last *k* days; drop oldest from head while appending newest at tail | O(1) at both ends |
| **Merge two sorted station streams** | You have two lists of weather data, each sorted by station and reading. | As you join them into one list, you can insert pieces in the middle (not just the ends) more easily, because each node links to both its next and previous neighbors. This makes reorganizing parts of the list quicker than with a singly linked list.
| **Undo stack on forecast editor** | Remove “current” edit and restore neighbor links | O(1) removal with node reference |

**Use a Python `list` or DataFrame** when you filter 50,000 daily rows, compute multi-year climate aggregates, or need `readings[i]` in a tight loop. **Use a doubly linked list (or `collections.deque`)** when the problem is a **mutable ordered chain** with heavy **both-end** or **bidirectional** traffic on a **small** *n* (one month window, one station chunk, one dashboard session).

```mermaid
flowchart LR
  subgraph dll["Doubly linked daily readings"]
    NIL1["None"] <--> H["Day 1"]
    H <--> N2["Day 2"]
    N2 <--> N3["Day 3"]
    N3 <--> T["Day 4"]
    T <--> NIL2["None"]
  end
  head["head"] --> H
  tail["tail"] --> T
```

Throughout this page, **n** is the number of nodes (e.g. days in one analysis window). **i** is a zero-based index.

---

## Doubly linked vs singly linked vs Python `list`

| | **Doubly linked** | [Singly linked](../linked-list/index.md) | [Python `list`](../array-based-lists/index.md) |
| --- | --- | --- | --- |
| **Pointers per node** | `next` + `prev` | `next` only | None (array of refs) |
| **`pop()` (tail)** | O(1) with `tail` | O(n) — must find predecessor | O(1) amortized |
| **Delete node you hold** | O(1) rewire | O(n) unless copy-value hack | O(n) shift |
| **Access by index `i`** | O(n) forward walk from head | O(n) from head only | O(1) |
| **Memory** | Highest per element | Medium | Compact + cache-friendly |
| **Weather fit** | Bidirectional timeline UI, both-end window | Head-heavy live ingest, merge drills | Full daily observation table |

```mermaid
sequenceDiagram
  participant Analyst
  participant DLL as doubly linked series
  Analyst->>DLL: go to current day (node ref)
  DLL-->>Analyst: prev — previous reading O(1)
  DLL-->>Analyst: next — next reading O(1)
  Note over Analyst,DLL: Singly linked "prev" would cost O(n) from head
```

---

## Node definition

Every node stores **data** (e.g. a daily weather row), **next**, and **prev**.

```python
from dataclasses import dataclass


@dataclass
class DailyReading:
    """Minimal daily weather row for examples on this page."""
    reading_id: int
    month: int
    temp_anomaly: float
    summary: str


class Node:
    """Doubly linked node."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
```

| | |
| --- | --- |
| **Time** | O(1) to construct one node |
| **Space** | O(1) per node (data + two references + CPython object header) |

```mermaid
flowchart TB
  subgraph node["Node"]
    D["data: DailyReading"]
    P["prev"]
    N["next"]
  end
  P --- D
  D --- N
```

---

## Ways to create a doubly linked list

### 1. Empty list — `head` and `tail` are `None`

```python
head = None
tail = None
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 2. Empty `DoublyLinkedList` wrapper

```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

series = DoublyLinkedList()
assert series.is_empty()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 3. Single-node list

```python
node = Node(DailyReading(101, 2, 0.4, "partly cloudy"))
head = tail = node
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) one node |

### 4. Build from iterable — append at tail (chronological day order)

Preserves CSV / API order: day 101 → 102 → 103.

```python
def from_iterable_tail(items):
    head = tail = None
    for item in items:
        node = Node(item)
        if head is None:
            head = tail = node
        else:
            node.prev = tail
            assert tail is not None
            tail.next = node
            tail = node
    return head, tail

readings = [
    DailyReading(101, 2, 0.4, "partly cloudy"),
    DailyReading(102, 2, -1.2, "cold front"),
    DailyReading(103, 2, 0.1, "light rain"),
]
head, tail = from_iterable_tail(readings)
```

| | |
| --- | --- |
| **Time** | O(k) for *k* readings |
| **Space** | O(k) nodes |

### 5. Build from iterable — push at head (reversed order)

Useful when data arrives **newest-first** (live feed) and you want oldest at head after a later `reverse`, or when you intentionally want reverse chronological storage.

```python
def from_iterable_head(items):
    head = None
    for item in items:
        node = Node(item)
        node.next = head
        if head is not None:
            head.prev = node
        head = node
    return head
```

| | |
| --- | --- |
| **Time** | O(k) |
| **Space** | O(k) |

### 6. Build with `append` (recommended)

```python
series = DoublyLinkedList()
for reading in [
    DailyReading(101, 2, 0.4, "partly cloudy"),
    DailyReading(102, 2, -1.2, "cold front"),
]:
    series.append(reading)
```

| | |
| --- | --- |
| **Time** | O(k) with tail-tracked `append` |
| **Space** | O(k) |

### 7. Manual wiring (tests, diagrams, interviews)

```python
n1 = Node(DailyReading(101, 2, 0.4, "partly cloudy"))
n2 = Node(DailyReading(102, 2, -1.2, "cold front"))
n3 = Node(DailyReading(103, 2, 0.1, "light rain"))
n1.next = n2
n2.prev = n1
n2.next = n3
n3.prev = n2
head, tail = n1, n3
```

| | |
| --- | --- |
| **Time** | O(k) |
| **Space** | O(k) |

### 8. From an existing Python `list` of daily readings

```python
readings_list = [
    DailyReading(201, 1, 0.2, "overcast"),
    DailyReading(202, 1, 1.1, "warm spell"),
]
series = DoublyLinkedList()
series.extend(readings_list)
```

| | |
| --- | --- |
| **Time** | O(k) |
| **Space** | O(k) nodes plus O(k) temporary if you keep both structures |

### Creation cheat sheet

```mermaid
flowchart TD
  Start([Building a daily reading chain?])
  Start --> Empty{Empty?}
  Empty -->|yes| E["DoublyLinkedList()"]
  Empty -->|no| Order{Order matters?}
  Order -->|chronological| Tail["append each reading — O(1) per day"]
  Order -->|newest-first ingest| Head["push each — then maybe reverse"]
  Order -->|3–5 nodes in test| Manual["wire prev/next by hand"]
  E --> Done([ready])
  Tail --> Done
  Head --> Done
  Manual --> Done
```

---

## Reference implementation

All method sections below use this class. It keeps **`head`**, **`tail`**, and **`size`** so `len`, both-end ops, and index walks stay cheap to reason about. Dunder methods (`__len__`, `__getitem__`, `__iter__`, `__str__`, `__repr__`) delegate to the helpers below. **`push`**, **`insert`**, **`set`**, **`reverse`**, **`clear`**, **`extend`**, **`sort`**, **`trim_front`**, and **`trim_back`** return **`self`** for chaining. Head removal uses private **`_pop_head()`**; **`remove(0)`** calls it. **`pop()`** always removes the **tail**. Index walks go through **`_node_at(index)`**.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        return f"DoublyLinkedList({self.to_list()})" # return the string representation of the linked list

    def __repr__(self):
        return f"DoublyLinkedList({self.to_list()})" # return the repr representation of the linked list

    def __len__(self):
        return self.size # return the size of the linked list

    def __getitem__(self, index):
        """
        Allows bracket access, e.g. dll[2], by delegating to self.get(index).
        (1) Raise an error if the index is out of bounds.
        (2) Otherwise, return the data from the node at the given index.
        """
        return self.get(index) # return the data from the node at the given index

    def __iter__(self):
        """
        Allows iteration over the linked list.
        (1) Start at the head.
        (2) While the current node is not None, yield the data of the current node and get the next node.
        """
        current = self.head # start at the head
        while current is not None: # while the current node is not None
            yield current.data # yield the data of the current node
            current = current.next # get the next node

    def is_empty(self):
        """
        (1) Return True if the linked list is empty, False otherwise.
        """
        return self.head is None # return True if the linked list is empty, False otherwise

    def push(self, data):
        """
        (1) Create a new node with the given data.
        (2) If the linked list is empty, set the head and tail to the new node.
        (3) Otherwise, set the new node's next pointer to the current head and the current head's previous pointer to the new node.
        (4) Set the head to the new node.
        (5) Increment the size of the linked list.
        (6) Return the linked list.
        """
        node = Node(data) # create a new node with the given data
        if self.is_empty(): # case: linked list is empty
            self.head = node # set the head to the new node
            self.tail = node # set the tail to the new node
        else: # case: linked list is not empty
            node.next = self.head # set the new node's next pointer to the current head
            self.head.prev = node # set the current head's previous pointer to the new node
            self.head = node # set the head to the new node
        self.size += 1 # increment the size of the linked list
        return self

    def append(self, data):
        """
        (1) Create a new node with the given data.
        (2) If the linked list is empty, set the head and tail to the new node.
        (3) Otherwise, set the new node's previous pointer to the current tail and the current tail's next pointer to the new node.
        (4) Set the tail to the new node.
        """
        node = Node(data) # create a new node with the given data
        if self.is_empty(): # case: linked list is empty
            self.head = node # set the head to the new node
            self.tail = node # set the tail to the new node
        else: # case: linked list is not empty
            node.prev = self.tail # set the new node's previous pointer to the current tail
            self.tail.next = node # set the current tail's next pointer to the new node
            self.tail = node # set the tail to the new node
        self.size += 1 # increment the size of the linked list

    def insert(self, index, data):
        """
        (1) Create a new node with the given data.
        (2) If the index is 0, set the new node's next pointer to the current head and the current head's previous pointer to the new node.
        (3) Otherwise, set the new node's previous pointer to the node at the given index and the node at the given index's next pointer to the new node.
        (4) Set the head to the new node.
        """
        if index < 0 or index > self.size: # case: index is out of bounds
            raise IndexError("index out of bounds") # raise an error if the index is out of bounds
        if index == 0: # case: index is 0
            self.push(data) # push the new node to the head of the linked list
            return self # return the linked list

        node = Node(data) # create a new node with the given data
        prev = self._node_at(index - 1) # get the node at the given index
        node.next = prev.next # set the new node's next pointer to the node at the given index
        prev.next.prev = node # set the node at the given index's next pointer to the new node
        node.prev = prev # set the new node's previous pointer to the node at the given index
        prev.next = node # set the node at the given index's next pointer to the new node
        self.size += 1 # increment the size of the linked list
        return self # return the linked list

    def pop(self):
        """
        (1) Raise an error if the linked list is empty.
        (2) Otherwise, remove the tail node and return its data.
        """
        if self.is_empty(): # case: linked list is empty
            raise IndexError("pop from empty list") # raise an error if the linked list is empty
        data = self.tail.data # get the data from the tail node
        if self.head.next is None: # case: linked list has only one node
            self.head = None # set the head to None
            self.tail = None # set the tail to None
        else: # case: linked list has more than one node
            self.tail = self.tail.prev # set the tail to the previous node
            self.tail.next = None # set the previous node's next pointer to None
        self.size -= 1 # decrement the size of the linked list
        return data # return the data from the tail node

    def _pop_head(self): # helper method to remove the head node and return its data
        if self.is_empty(): # case: linked list is empty
            raise IndexError("pop from empty list") # raise an error if the linked list is empty
        data = self.head.data # get the data from the head node
        if self.head.next is None: # case: linked list has only one node
            self.head = None # set the head to None
            self.tail = None # set the tail to None
        else: # case: linked list has more than one node
            self.head = self.head.next # set the head to the next node
            self.head.prev = None # set the previous node's previous pointer to None
        self.size -= 1 # decrement the size of the linked list
        return data # return the data from the head node

    def remove(self, index): # helper method to remove the node at the given index and return its data
        """
        Remove the node at the given index and return its data.
        """
        if index < 0 or index >= self.size: # case: index is out of bounds
            raise IndexError("index out of bounds") # raise an error if the index is out of bounds
        if index == 0:
            return self._pop_head() # remove the head node and return its data
        if index == self.size - 1:
            return self.pop() # remove the tail node and return its data
        prev = self._node_at(index - 1)
        cur = prev.next # get the next node
        prev.next = cur.next # set the previous node's next pointer to the next node
        cur.next.prev = prev # set the next node's previous pointer to the previous node
        self.size -= 1
        return cur.data # return the data from the node at the given index

    def get(self, index):
        """
        (1) If the index is out of bounds, raise an error.
        (2) Otherwise, return the data from the node at the given index.
        """
        return self._node_at(index).data # return the data from the node at the given index

    def set(self, index, data): # helper method to set the data of the node at the given index
        """
        (1) If the index is out of bounds, raise an error.
        (2) Otherwise, set the data of the node at the given index.
        """
        self._node_at(index).data = data # set the data of the node at the given index
        return self # return the linked list
    
    def _node_at(self, index):
        """
        (1) If the index is out of bounds, raise an error.
        (2) If the index is 0, return the head node.
        (3) Otherwise, return the node at the given index.
        """
        if index < 0 or index >= self.size: # case: index is out of bounds
            raise IndexError("index out of bounds") # raise an error if the index is out of bounds
        current = self.head # start at the head
        for _ in range(index): # iterate through the linked list
            current = current.next # get the next node
        return current # return the node at the given index

    def index_of(self, data):
        """
        (1) If the data is not found, return -1.
        (2) Otherwise, return the index of the data.
        """
        current = self.head # start at the head
        for i in range(self.size): # iterate through the linked list
            if current.data == data: # case: data is found
                return i # return the index of the data
            current = current.next # get the next node
        return -1 # return -1 if the data is not found

    def contains(self, data):
        """
        (1) If the data is found, return True.
        (2) Otherwise, return False.
        """
        return self.index_of(data) != -1 # return True if the data is found, False otherwise
    
    def reverse(self):
        """
        (1) If the linked list is empty, raise an error.
        (2) Otherwise, reverse the linked list.
        """
        if self.is_empty(): # case: linked list is empty
            raise IndexError("reverse empty list") # raise an error if the linked list is empty
        current = self.head # start at the head
        while current is not None: # iterate through the linked list
            current.next, current.prev = current.prev, current.next # swap the next and previous pointers
            current = current.prev # advance along the original forward chain
        self.head, self.tail = self.tail, self.head # swap the head and tail
        return self # return the linked list
    
    def to_list(self):
        """
        (1) If the linked list is empty, return an empty list.
        (2) Otherwise, return the linked list as a list.
        """
        if self.is_empty(): # case: linked list is empty
            return [] # return an empty list
        current = self.head # start at the head
        out = [] # create an empty list
        while current is not None: # iterate through the linked list
            out.append(current.data) # add the data to the list
            current = current.next # get the next node
        return out # return the linked list as a list
    
    def clear(self):
        """
        (1) Set the head and tail to None.
        (2) Set the size to 0.
        """
        self.head = None # set the head to None
        self.tail = None # set the tail to None
        self.size = 0 # set the size to 0
        return self # return the linked list
    
    def extend(self, items):
        """
        (1) If the items are a DoublyLinkedList, append each item from the items to the linked list.
        (2) Otherwise, append each item from the items to the linked list.
        """
        if isinstance(items, DoublyLinkedList): 
            # If items is a DoublyLinkedList instance
            if items.is_empty():  # nothing to extend if items has no nodes
                return self
            if self.is_empty():
                # If this list is empty, adopt items' chain directly (shallow copy)
                self.head = items.head # set the head to the head of the items
                self.tail = items.tail # set the tail to the tail of the items
                self.size = items.size # set the size to the size of the items
            else:
                # Otherwise, link their head to our tail and update attributes
                self.tail.next = items.head         # Our tail's next node points to items' head node
                items.head.prev = self.tail         # Items' head prev points back to our tail
                self.tail = items.tail              # Update our tail to be items' tail
                self.size += items.size             # Increase our size by items' size
            return self # return the linked list
        else:
            # Otherwise, items is any other iterable: append each item one by one
            for item in items:
                self.append(item) # append the item to the linked list
            return self # return the linked list
     

    def sort(self): # helper method to sort the linked list
        """
        Sort nodes in ascending order by data value.
        """
        if self.size < 2: # case: linked list has less than two nodes
            return self # return the linked list
            return self
        values = self.to_list() # get the list of values from the linked list
        values.sort() # sort the list of values
        self.clear() # clear the linked list
        for value in values: # iterate through the list of values
            self.append(value) # append the value to the linked list
        return self # return the linked list

    def copy(self):
        """
        Return a shallow copy with new nodes.
        """
        out = DoublyLinkedList() # create a new linked list
        for item in self:
            out.append(item) # append the item to the new linked list
        return out # return the new linked list

    def trim_front(self, count): # helper method to remove count nodes from the front of the linked list
        """
        Remove count nodes from the front of the list.
        """
        for _ in range(count): # iterate through the linked list
            if self.is_empty(): # case: linked list is empty
                break # break the loop
            self.remove(0) # remove the node at the given index
        return self # return the linked list

    def trim_back(self, keep): # helper method to remove nodes from the back of the linked list
        """
        Keep only the first keep nodes; drop the rest from the tail.
        """
        while self.size > keep: # while the size of the linked list is greater than keep
            self.pop() # remove the tail node
        return self # return the linked list

    def latest(self): # helper method to return the most recently appended value
        """
        Return the most recently appended value (tail), or None if empty.
        """
        if self.is_empty(): # case: linked list is empty
            return None # return None
        return self.tail.data # return the data from the tail node

    def oldest_in_window(self): # helper method to return the oldest value in the window
        """
        Return the oldest value in the window (head), or None if empty.
        """
        if self.is_empty(): # case: linked list is empty
            return None # return None
        return self.head.data # return the data from the head node

    def current(self): # helper method to return the value at the current read position
        """
        Return the value at the current read position (head), or None if empty.
        """
        if self.is_empty(): # case: linked list is empty
            return None # return None
        return self.head.data # return the data from the head node

    def find_reading(self, reading_id): # helper method to find the reading with the given reading id
        """
        (1) If the reading id is not found, return None.
        (2) Otherwise, return the reading with the given reading id.
        """
        current = self.head # start at the head
        while current is not None: # iterate through the linked list
            data = current.data # get the data from the current node
            if hasattr(data, "reading_id"): # case: data has a reading id
                if data.reading_id == reading_id: # case: reading id is found
                    return data # return the data
            elif data == reading_id: # case: reading id is found
                return data # return the data
            current = current.next # get the next node
        return None # return None if the reading id is not found

    def walk_forward_from(self, node): # helper method to walk forward from the given node  
        """
        Collect data walking forward via next pointers from node.
        """
        if node is None: # case: node is None
            return [] # return an empty list
        out = [] # create an empty list
        current = node # start at the given node
        while current is not None: # iterate through the linked list
            out.append(current.data) # add the data to the list
            current = current.next # get the next node
        return out # return the list of data

    def walk_backward_from(self, node): # helper method to walk backward from the given node
        """
        Collect data walking backward via prev pointers from node.
        """
        if node is None: # case: node is None
            return [] # return an empty list
        out = [] # create an empty list
        current = node # start at the given node
        while current is not None: # iterate through the linked list
            out.append(current.data) # add the data to the list
            current = current.prev # get the previous node
        return out # return the list of data
```

---

## All operations (weather examples + complexity)

```mermaid
flowchart TB
  subgraph ends["O(1) at ends"]
    push
    append
    remove0["remove(0)"]
    pop
  end
  subgraph scan["O(n) scan"]
    find_reading
    index_of
    get_at["_node_at(i)"]
  end
```

Helper used in several examples:

```python
def make_series(readings):
    series = DoublyLinkedList()
    for reading in readings:
        series.append(reading)
    return series
```

### `is_empty()` / `len(series)` / `series[i]`

**`is_empty()`** checks `head is None`. **`__len__`** returns cached **`size`**. Bracket access **`series[i]`** delegates to **`get(i)`** and returns **data** (not a node).

```python
series = DoublyLinkedList()
assert series.is_empty()
assert len(series) == 0

series.append(DailyReading(101, 2, 0.4, "partly cloudy"))
assert len(series) == 1
assert series[0].reading_id == 101
```

| | |
| --- | --- |
| **Time** | O(1) with cached `size` |
| **Space** | O(1) |

---

### `push(data)` — new reading before the oldest day

Create a node, wire `next`/`prev` to the current head (or set both `head` and `tail` when empty), increment `size`, and return **`self`**.

Example: push a **backfilled observation** reclassified as the first row in a corrected daily chain.

```python
series = make_series([DailyReading(102, 2, -1.2, "cold front")])
series.push(DailyReading(101, 2, 0.4, "partly cloudy"))
assert series.get(0).reading_id == 101
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) one new node |

```mermaid
sequenceDiagram
  participant D as series
  participant New as new reading node
  participant Old as old head
  D->>New: create node; New.next = head
  New->>Old: Old.prev = New
  D->>D: head = New
```

---

### `append(data)` — next day in the series

Create a node, link it after `tail` (or set both `head` and `tail` when empty), and increment `size`. Does not return `self`.

```python
series = DoublyLinkedList()
series.append(DailyReading(101, 2, 0.4, "partly cloudy"))
series.append(DailyReading(102, 2, -1.2, "cold front"))
assert list(series)[-1].summary == "cold front"
```

| | |
| --- | --- |
| **Time** | O(1) with `tail` |
| **Space** | O(1) |

---

### `insert(index, data)` — insert a reading mid-series

Valid indices are `0 … size` (inclusive upper bound). Index **`0`** delegates to **`push(data)`**. Otherwise **`_node_at(index - 1)`** finds the predecessor, splices the new node between it and its successor, increments `size`, and returns **`self`**.

Insert a **corrected sensor spike** before the row currently at index 2.

```python
series = make_series([
    DailyReading(101, 2, 0.4, "partly cloudy"),
    DailyReading(102, 2, -1.2, "cold front"),
    DailyReading(104, 2, 0.1, "overcast"),
])
series.insert(2, DailyReading(103, 2, 2.1, "sensor correction"))
ids = [s.reading_id for s in series]
assert ids == [101, 102, 103, 104]
```

| | |
| --- | --- |
| **Time** | O(n) — `_node_at(index)` plus O(1) rewire |
| **Space** | O(1) |

```mermaid
flowchart LR
  A["day A"] <--> B["day B"]
  B <--> C["day C"]
  B <--> NEW["new reading"]
  NEW <--> C
```

---

### `get(index)` / `set(index, data)` — access by position

Both use **`_node_at(index)`**, which walks forward from the head and raises **`IndexError("index out of bounds")`** when **`index < 0`** or **`index >= size`**. **`set`** mutates **`node.data`** in place and returns **`self`**.

```python
series = make_series([DailyReading(i, 1, 0.0, f"day {i}") for i in range(10)])
assert series.get(0).reading_id == 0
assert series.get(9).reading_id == 9
series.set(5, DailyReading(99, 1, 0.0, "replaced"))
assert series.get(5).reading_id == 99
```

| | |
| --- | --- |
| **Time** | O(i) ≤ O(n) |
| **Space** | O(1) |

For thousands of daily rows, store an index in a **`dict[reading_id, DailyReading]`** beside the chain—not `get(i)` in a hot loop.

---

### `remove(0)` — drop the oldest day from the window

Head removal is handled by `remove(0)` (internally `_pop_head`).

```python
series = make_series([
    DailyReading(101, 2, 0.4, "partly cloudy"),
    DailyReading(102, 2, -1.2, "cold front"),
])
old_first = series.remove(0)
assert old_first.reading_id == 101
assert series.get(0).reading_id == 102
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

---

### `pop()` — remove the latest reading (e.g. undo last annotation)

Removes the **tail** node, returns its **data**, and decrements **`size`**. On a one-node list, sets both **`head`** and **`tail`** to **`None`**. Singly linked lists need an O(n) scan for the predecessor; **doubly linked does not**.

```python
series = make_series([
    DailyReading(101, 2, 0.4, "partly cloudy"),
    DailyReading(102, 2, -1.2, "cold front"),
])
last = series.pop()
assert last.reading_id == 102
assert len(series) == 1
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

```mermaid
sequenceDiagram
  participant D as series
  D->>D: read tail.data
  D->>D: tail = tail.prev; tail.next = None
  Note over D: Singly linked would walk n-1 steps
```

---

### `remove(index)` — delete by position

Returns the removed **data**. Index **`0`** calls **`_pop_head()`**; index **`size - 1`** delegates to **`pop()`**; otherwise rewire through the predecessor at **`index - 1`**. All three paths update `size` and fix `prev`/`next`.

```python
series = make_series([
    DailyReading(101, 2, 0.4, "partly cloudy"),
    DailyReading(102, 2, -1.2, "cold front"),
    DailyReading(103, 2, 0.1, "light rain"),
])
assert series.remove(1).reading_id == 102
assert [s.reading_id for s in series] == [101, 103]
```

| | |
| --- | --- |
| **Time** | O(1) at index `0` or `size - 1`; O(n) mid-list — walk to index, then O(1) rewire |
| **Space** | O(1) |

---

### `find_reading(reading_id)` / `index_of` / `contains`

`find_reading` returns the **data** (not the node). It matches objects with a `reading_id` attribute or raw values.

```python
series = make_series([
    DailyReading(101, 2, 0.4, "partly cloudy"),
    DailyReading(102, 2, -1.2, "cold front"),
])
reading = series.find_reading(102)
assert reading is not None and reading.summary == "cold front"
assert series.contains(DailyReading(101, 2, 0.4, "partly cloudy"))
assert series.index_of(DailyReading(102, 2, -1.2, "cold front")) == 1
assert series.index_of(DailyReading(999, 1, 0.0, "missing")) == -1
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

---

### Bidirectional iteration — `__iter__`, `walk_forward_from`, `walk_backward_from`

Forward iteration uses **`__iter__`** (yields each node's **data** from head to tail). **`walk_forward_from(node)`** and **`walk_backward_from(node)`** take a **`Node`** reference (e.g. `series.head` or `series.tail`), follow `next` or `prev`, and return a **Python list of data**—not an iterator.

```python
series = make_series([
    DailyReading(101, 2, 0.4, "partly cloudy"),
    DailyReading(102, 2, -1.2, "cold front"),
    DailyReading(103, 2, 0.1, "light rain"),
])

forward_anomaly = [s.temp_anomaly for s in series]
backward_anomaly = [s.temp_anomaly for s in series.walk_backward_from(series.tail)]
assert forward_anomaly == [0.4, -1.2, 0.1]
assert backward_anomaly == [0.1, -1.2, 0.4]
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) auxiliary (not counting result lists) |

| | |
| --- | --- |
| **`walk_forward_from(node)`** | O(k) forward from a known node |
| **`walk_backward_from(node)`** | O(k) backward from a known node |

---

### `clear()` — reset forecast editor

Sets **`head`**, **`tail`**, and **`size`** back to empty state. Returns **`self`**.

```python
series = make_series([DailyReading(101, 2, 0.4, "partly cloudy")])
series.clear()
assert series.is_empty()
```

| | |
| --- | --- |
| **Time** | O(1) to drop head/tail |
| **Space** | O(1) |

---

### `copy()` — duplicate chain for forecast scenario

Shallow copy: new nodes, **same** `DailyReading` objects.

```python
original = make_series([DailyReading(101, 2, 0.4, "partly cloudy")])
branch = original.copy()
branch.append(DailyReading(999, 2, 0.0, "forecast scenario"))
assert len(original) == 1 and len(branch) == 2
assert branch.head is not original.head
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) |

---

### `reverse()` — flip chronological order in place

Swaps each node's `next` and `prev`, then swaps `head` and `tail`. Raises **`IndexError("reverse empty list")`** on an empty list. Returns **`self`**.

Useful after **push-heavy** ingest to get chronological order.

```python
series = DoublyLinkedList()
for pid in [103, 102, 101]:  # newest first
    series.push(DailyReading(pid, 2, 0.0, "x"))
series.reverse()
assert [s.reading_id for s in series] == [101, 102, 103]
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

---

### `sort()` — order readings by comparable data

Exports values with **`to_list()`**, sorts in place with Python's **`list.sort()`** (data must be mutually comparable), clears the chain, and rebuilds with **`append`**. No-op when **`size < 2`**. Returns **`self`**.

```python
series = make_series([
    DailyReading(103, 2, 0.0, "c"),
    DailyReading(101, 2, 0.0, "a"),
    DailyReading(102, 2, 0.0, "b"),
])
series.sort()
assert [s.reading_id for s in series] == [101, 102, 103]
```

| | |
| --- | --- |
| **Time** | O(n log n) — Python `list.sort` on exported values |
| **Space** | O(n) temporary list |

---

### `extend(iterable)` / `to_list()`

When **`items`** is another **`DoublyLinkedList`**: empty source is a no-op; if **`self`** is empty, adopt the other chain's **`head`**, **`tail`**, and **`size`**; otherwise splice at the tail in O(1). Any other iterable appends one item at a time. Returns **`self`**. **`to_list()`** walks head→tail and returns a Python list of data.

```python
series = make_series([DailyReading(101, 2, 0.4, "partly cloudy")])
series.extend([DailyReading(102, 2, -1.2, "cold front"), DailyReading(103, 2, 0.1, "light rain")])
rows = series.to_list()  # export to pandas: pd.DataFrame([s.__dict__ for s in rows])
assert len(rows) == 3
```

| Operation | Time | Space |
| --- | --- | --- |
| `extend` (another `DoublyLinkedList`) | O(1) splice | O(1) |
| `extend` (generic iterable) | O(k) | O(1) aux per append |
| `to_list` | O(n) | O(n) |

---

### `trim_front(count)` / `trim_back(keep)` — window helpers

**`trim_front(count)`** loops up to **count** times, calling **`remove(0)`** until empty. **`trim_back(keep)`** loops **`pop()`** while **`size > keep`**. Both return **`self`**.

```python
series = make_series([DailyReading(i, 1, 0.0, f"day {i}") for i in range(10)])
series.trim_front(5)  # drop days 0–4
assert len(series) == 5
assert series.get(0).reading_id == 5

series2 = make_series([DailyReading(i, 1, 0.0, f"day {i}") for i in range(10)])
series2.trim_back(5)  # keep days 0–4
assert len(series2) == 5
assert series2.get(4).reading_id == 4
```

| Operation | Time | Space |
| --- | --- | --- |
| `trim_front(count)` | O(count) | O(1) |
| `trim_back(keep)` | O(n − keep) | O(1) |

---

### `latest()` / `oldest_in_window()` / `current()`

**`latest()`** returns **`tail.data`**; **`oldest_in_window()`** and **`current()`** both return **`head.data`**. Each returns **`None`** when the list is empty. These are fixed head/tail accessors—not a movable cursor (see **`ReadingNavigator`** below for prev/next scrubbing).

```python
series = make_series([DailyReading(101, 2, 0.4, "a"), DailyReading(102, 2, -1.2, "b")])
assert series.latest().reading_id == 102
assert series.oldest_in_window().reading_id == 101
assert series.current().reading_id == 101
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

---

## Weather application: recent readings buffer

```python
class RecentReadings:
    """Last k daily rows using a doubly linked list."""

    def __init__(self, max_readings=5):
        self._chain = DoublyLinkedList()
        self._max = max_readings

    def push(self, reading):
        self._chain.append(reading)
        while self._chain.size > self._max:
            self._chain.remove(0)

    def latest(self):
        return self._chain.latest()

    def oldest_in_window(self):
        return self._chain.oldest_in_window()


feed = RecentReadings(max_readings=3)
for rid in range(10):
    feed.push(DailyReading(rid, 1, 0.0, f"day {rid}"))
assert feed.latest().reading_id == 9
assert feed.oldest_in_window().reading_id == 7
```

| Operation | Time | Space |
| --- | --- | --- |
| `push` | O(1) append + O(1) per excess head removal | O(k) stored |

---

## Weather application: reading navigator (prev / next)

```python
class ReadingNavigator:
    """Bidirectional scrubber over one daily reading chain."""

    def __init__(self, series):
        self._series = series
        self._current = series.head

    def current(self):
        return None if self._current is None else self._current.data

    def next_reading(self):
        if self._current is None or self._current.next is None:
            return None
        self._current = self._current.next
        return self._current.data

    def prev_reading(self):
        if self._current is None or self._current.prev is None:
            return None
        self._current = self._current.prev
        return self._current.data


series = make_series([
    DailyReading(101, 2, 0.4, "partly cloudy"),
    DailyReading(102, 2, -1.2, "cold front"),
    DailyReading(103, 2, 0.1, "light rain"),
])
nav = ReadingNavigator(series)
assert nav.current().reading_id == 101
assert nav.next_reading().reading_id == 102
assert nav.prev_reading().reading_id == 101
```

| Step | Time | Space |
| --- | --- | --- |
| `next_reading` / `prev_reading` | O(1) | O(1) |
| Jump to arbitrary `reading_id` | O(n) search first | O(1) after found |

---

## Low-level patterns

### Dummy head and tail sentinels

Simplify deletion near ends when you do not keep a full `DoublyLinkedList` class.

```python
def remove_readings_with_negative_anomaly(head):
    dummy = Node(DailyReading(0, 0, 0.0, "sentinel"))
    dummy.next = head
    if head is not None:
        head.prev = dummy
    cur = dummy
    while cur.next is not None:
        if cur.next.data.temp_anomaly < 0:
            nxt = cur.next.next
            if nxt is not None:
                nxt.prev = cur
            cur.next = nxt
        else:
            cur = cur.next
    out = dummy.next
    if out is not None:
        out.prev = None
    return out
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) extra for dummy |

### Merge two sorted station chains by `reading_id`

Same pointer technique as singly linked merge; doubly linked lets you splice without rebuilding `prev` if you assign both links.

```python
def merge_by_reading_id(a, b):
    dummy = Node(DailyReading(0, 0, 0.0, ""))
    tail = dummy
    while a is not None and b is not None:
        if a.data.reading_id <= b.data.reading_id:
            tail.next = a
            a.prev = tail
            a = a.next
        else:
            tail.next = b
            b.prev = tail
            b = b.next
        tail = tail.next
    rest = a if a is not None else b
    if rest is not None:
        tail.next = rest
        rest.prev = tail
    out = dummy.next
    if out is not None:
        out.prev = None
    return out
```

| | |
| --- | --- |
| **Time** | O(n + m) |
| **Space** | O(1) auxiliary |

```mermaid
sequenceDiagram
  participant A as Station A chain
  participant B as Station B chain
  participant M as merged chain
  loop while both non-empty
    M->>A: compare reading_id at heads
    M->>M: attach smaller node, fix prev/next
  end
  M->>M: attach remainder
```

---

## Python stdlib: `collections.deque`

CPython's `deque` is implemented as a **block doubly linked list** at C level—not the same as your `Node` class, but the same **complexity story** for ends.

```python
from collections import deque

recent = deque(maxlen=5)
recent.append(DailyReading(101, 2, 0.4, "partly cloudy"))
recent.appendleft(DailyReading(100, 2, 0.0, "backfill"))
assert len(recent) <= 5
```

| Operation | `deque` (amortized) | Your `DoublyLinkedList` |
| --- | --- | --- |
| `append` / `appendleft` | O(1) | `append` / `push` O(1) |
| `pop` / `popleft` | O(1) | `pop` / `remove(0)` O(1) |
| Indexing `dq[i]` | O(n) | O(n) via `get` / `__getitem__` |
| Custom `DailyReading` + `find_reading` | Use your class | Use your class |

**Rule of thumb:** ship **`deque`** in production weather dashboards; implement **`DoublyLinkedList`** to learn and to pass interviews.

---

## Master complexity table

Let **n** = `len(series)`, **i** = index.

| Operation | Time | Space (auxiliary) | Notes |
| --- | --- | --- | --- |
| Create empty | O(1) | O(1) | |
| Build from *k* items | O(k) | O(k) nodes | tail `append` |
| `push` / `append` | O(1) | O(1) | |
| `insert(i)` | O(n) | O(1) | find + splice |
| `get` / `set` at *i* | O(i) | O(1) | forward walk from head |
| `remove(0)` / `pop()` | O(1) | O(1) | |
| `remove(i)` mid-list | O(n) | O(1) | ends delegate to `_pop_head` / `pop` |
| `find_reading` / `contains` | O(n) | O(1) | |
| `latest` / `oldest_in_window` / `current` | O(1) | O(1) | `None` if empty |
| `walk_forward_from` / `walk_backward_from` | O(k) | O(k) | returns list of data |
| `len` (cached) | O(1) | O(1) | |
| Forward `__iter__` | O(n) | O(1) | yields data, head → tail |
| `clear` | O(1) | O(1) | |
| `copy` | O(n) | O(n) | |
| `reverse` in place | O(n) | O(1) | raises on empty list |
| `sort` | O(n log n) | O(n) | export, sort, rebuild |
| `extend` | O(k) | O(1) per item | O(1) splice for another DLL |
| `to_list` | O(n) | O(n) | |
| `trim_front(count)` | O(count) | O(1) | repeated `remove(0)` |
| `trim_back(keep)` | O(n − keep) | O(1) | repeated `pop()` |

**Total storage:** Θ(n) nodes, each with `data`, `prev`, `next`.

---

## When to pick which structure (weather context)

```mermaid
flowchart TD
  Q([What is the job?])
  Q --> S{Multi-year / table analytics?}
  S -->|yes| DF["pandas DataFrame or list of dicts"]
  S -->|no| B{Need prev/next from current day?}
  B -->|yes| DLL["Doubly linked or ReadingNavigator"]
  B -->|no| E{Only head inserts?}
  E -->|yes| SLL["Singly linked or deque"]
  E -->|no| L["Python list — index readings[i]"]
```

| Scenario | Best tool |
| --- | --- |
| Multi-year climate aggregates | pandas, not linked list |
| One month window, timeline prev/next | Doubly linked or `deque` + index |
| Live "last 5 days" ticker | `deque(maxlen=5)` or `remove(0)` loop |
| Merge sorted reading-id streams (exercise) | Doubly or singly linked merge |
| Random access `readings[412]` in loop | `list` |

---

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Confusing `pop()` with `remove(0)` | `pop()` drops the **tail**; `remove(0)` drops the **head** | Use `remove(0)` for oldest-in-window; `pop()` for latest |
| Calling `reverse()` on empty list | Raises `IndexError` | Guard with `is_empty()` first |
| Forgetting to update `prev` on splice | Broken backward walk | Always set both `prev` and `next` |
| Losing `head` / `tail` after delete | Orphan chain | Branch on whether node is head or tail |
| Storing full archive in DLL | O(n) lookups, huge memory | DataFrame + optional small DLL per window |
| Expecting `find_reading` to return a node | API returns data | Use `series.head` / `_node_at` when you need the node |
| Shallow copy shares `DailyReading` | Mutate one branch, affects other | `copy.deepcopy` if needed |
| Using DLL for `readings[i]` hot loop | O(n) per access | `list` or columnar store |

---

## Related pages

| Page | Relationship |
| --- | --- |
| [Singly linked list](../linked-list/index.md) | One pointer; O(n) `pop_tail` |
| [Circularly linked list](../circularly-linked-list/index.md) | Ring of nodes; round-robin |
| [Array-based lists](../array-based-lists/index.md) | Python `list` for observation tables |
| [Deque](../dequeue-deque/index.md) | Production O(1) both ends |
| [Complexity analysis](../../complexity/index.md) | Big-O reference |

---

## Quick reference card

```python
# create
series = DoublyLinkedList()
for r in [reading1, reading2]:
    series.append(r)

# O(1) ends — pop() = tail; remove(0) = head (_pop_head)
series.push(reading)
series.append(reading)
series.remove(0)           # oldest / head
series.pop()               # latest / tail; doubly linked O(1), singly O(n)

# O(n) index / search
series.get(i)
series[i]
series.insert(i, reading)
series.remove(i)
series.find_reading(reading_id)

# both directions
for r in series: ...                    # __iter__: head → tail
series.walk_forward_from(series.head)
series.walk_backward_from(series.tail)

# window helpers
series.trim_front(3)
series.trim_back(5)
series.latest()
series.oldest_in_window()
```

Use a **doubly linked list** when the problem is an **ordered chain** and you need **both ends** or **backward steps** without rescanning from the head—then reach for **`deque`** when you ship real weather analysis tooling.
