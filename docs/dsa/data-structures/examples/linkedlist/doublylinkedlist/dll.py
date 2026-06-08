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

    def oldest_in_buffer(self): # helper method to return the oldest value in the buffer
        """
        Return the oldest value in the buffer (head), or None if empty.
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

    def find_entry(self, entry_id): # helper method to find the entry with the given entry id
        """
        (1) If the entry id is not found, return None.
        (2) Otherwise, return the entry with the given entry id.
        """
        current = self.head # start at the head
        while current is not None: # iterate through the linked list
            data = current.data # get the data from the current node
            if hasattr(data, "entry_id"): # case: data has an entry id
                if data.entry_id == entry_id: # case: entry id is found
                    return data # return the data
            elif data == entry_id: # case: entry id is found
                return data # return the data
            current = current.next # get the next node
        return None # return None if the entry id is not found

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

