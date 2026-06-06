class Node:
    def __init__(self, data, next=None):
        self.data = data # set node data to provided value
        self.next = next # set next node
   
class LinkedList:
    # initialize the linked list
    def __init__(self, values=None):
        self.head = None # set head pointer to None
        self.tail = None # set tail pointer to None
        self.next = None # set next pointer to None (unused for linked list instance)
        self.size = 0 # set initial size to 0

        if values is not None:
            for value in values:
                self.append(value)
    


    # print the linked list
    def __str__(self):
        """
        (1) Traverse the linked list and append the data of each node to a list.
        (2) Return a string representation of the linked list.
        """
        current = self.head # set starting point to head node
        out = [] # initialize output list
        while current: # iterate while current node is not None
            out.append(repr(current.data)) # append string representation of node data
            current = current.next # set current node to next node
        return f"LinkedList([{', '.join(out)}])" # return formatted string

    def __getitem__(self, index):
        """
        Allows bracket access, e.g. ll[2], by delegating to self.get(index).
        Raises IndexError if the index is out of bounds.
        """
        return self.get(index)

    # represent the linked list
    def __repr__(self):
        return self.__str__() # call __str__ to return string representation

    # get the size of the linked list
    def __len__(self):
        return self.size # return size attribute

    def __iter__(self):
        """
        (1) Iterate over the linked list and yield each node's data.
        """
        cur = self.head # set starting point to head node
        while cur is not None: # iterate while cur node is not None
            yield cur.data # yield the current node's data
            cur = cur.next # set current node to next node

    # check if the linked list is empty
    def is_empty(self):
        """
        (1) Return True if the linked list is empty, False otherwise.
        """
        # if the head is None, then the linked list is empty
        return self.head is None # return True if head is None

    # prepend a node to the linked list
    def prepend(self, data):
        """
        (1) Create a new node with the given data and set its next pointer to the current head.
        (2) Update the linked list's head pointer to the new node.
        (3) Update the linked list's tail pointer to the new node only if the list was empty.
        (4) Update the size of the linked list.
        """
        # create a new node
        new_node = Node(data, next=self.head) # the new node's next pointer is the current head

        # update the head to the new node
        self.head = new_node # set head to new node
        
        # update tail only if the list was empty
        if self.tail is None:
            self.tail = new_node # set tail to new node if list was empty
        
        # update the size of the linked list
        self.size += 1 # increment size

    # append a node to the linked list
    def append(self, data):
        """
        (1) Create a new node with the given data and set its next pointer to None.
        (2) If the list is empty, set the head and tail to the new node.
        (3) If the list is not empty
            (a) set the next pointer of the current tail node to the new node
            (b) update the linked list's tail pointer to the new node.
        (4) Update the size of the linked list.
        """
        # create a new node
        node = Node(data) # create new node with given data

        # if the list is empty, set the head and tail to the new node
        if self.tail is None:
            self.head = self.tail = node # set head and tail to the new node
        else:
            # set the next pointer of the current tail to the new node
            self.tail.next = node # set current tail's next to new node
            # update the tail to the new node
            self.tail = node # set tail to new node
        
        # update the size of the linked list
        self.size += 1 # increment size

    def insert(self, index, data):
        """
        (1) Create a new node from data in argument
        (2) If the list is empty, set the head and tail to the new node.
        (3) If the list is not empty
            (a) set the next pointer of the current tail node to the new node
            (b) update the linked list's tail pointer to the new node.
        (4) Update the size of the linked list.
        """
        # if index is larger than the size of the linked list then append to end of linked list
        if index >= self.size:
            self.append(data) # append if index is out of range
            return
        
        # handle inserting a new head node
        if index == 0:
            self.prepend(data) # prepend if index is zero
            return
        
        # get the node right before the node that we want to insert
        prev = self._node_at(index - 1) # get node at index-1

        # create the node and set node next pointer to the next node after prev
        node = Node(data, next=prev.next) # create new node with next set to prev.next

        # set prev next node to the new node to append the new node to the linked list
        prev.next = node # set prev's next to new node

        # update linkedlist size
        self.size += 1 # increment size

    def pop_head(self):
        """
        (1) case: linkedlist is empty then raise IndexError
        (2) Handle: store current head data somewhere in memory 
        (3) case: single node linkedlist
        (4) case: multi node linkedlist
        (5) update the size of the linked list
        (6) return the data from the head node back to the caller
        """
        # case: linkedlist is empty
        if self.head is None: # case: linkedlist is empty then raise IndexError
            raise IndexError("pop from empty list") # raise error if list empty

        data = self.head.data # store current head data somewhere in memory

        # case: single node linkedlist
        if self.head.next is None:
            self.head = None # set head to None
            self.tail = None # set tail to None
        # case: multi node linkedlist
        else:
            self.head = self.head.next # set new head node
        
        # case: update size
        self.size -= 1 # update the size of the linked list

        # return the data from the head node back to the caller
        return data # return the data from the head node back to the caller

    def pop_tail(self):
        """
        (1) case: empty linkedlist
        (2) case: single node linkedlist
        (3) case: multinode linkedlist
        (4) update the size of the linked list
        (5) return the data from the tail node back to the caller
        """
        # case: empty linkedlist
        if self.head is None: # case: linkedlist is empty then raise IndexError
            raise IndexError("pop from empty list") # raise error if linkedlist is empty
        
        # case: single node linkedlist
        if self.head.next == None: # case: single node linkedlist then pop head node
            return self.pop_head() # pop head node and return the data from the head node back to the caller

        # case: multinode linkedlist
        else:
            prev = self._node_at(self.size - 2) # get second to last node
            data = prev.next.data # get data from last node
            prev.next = None # set second to last node's next pointer to None
            self.tail = prev # set new tail node
            self.size -= 1 # decrement size of linkedlist
            return data # return data to caller

    def remove(self, index):
        """
        (1) case: empty linkedlist
        (2) case: single node linkedlist
        (3) case: multi node linkedlist
        (4) update the size of the linked list
        (5) return the data from the node that was removed back to the caller
        """
        # case: empty linkedlist
        if index < 0 or index >= self.size:
            raise IndexError("index out of range") # case: index is out of range then raise IndexError
        
        # case: single node linkedlist
        if index == 0:
            return self.pop_head() # pop head node

        # case: multi node linkedlist
        else:         
            prev      = self._node_at(index - 1) # get the node right before the node that we want to remove
            cur       = prev.next # get current node
            prev.next = cur.next # remove node from list by setting prev node next node to current node next node

            # case: removed tail node
            if prev.next is None:
                self.tail = prev # set new tail node
        
        self.size -= 1 # decrement size of linkedlist
        return cur.data # return data to caller

    # helpers
    def get(self, index):
        """
        (1) Return the data found at a given index or raise
        """
        return self._node_at(index).data # get node at index and return data

    def set(self, index, data):
        """
        (1) Set data for a given node or raise
        """
        self._node_at(index).data = data # set node's data at given index

    # get the node at the given index
    def _node_at(self, index):
        """
        (1) case: index is out of range then raise IndexError
        (2) case: index is in range then traverse the linked list and return the node at the given index.
        """
        if index < 0 or index >= self.size:
            raise IndexError("index out of range") # case: index is out of range then raise IndexError
        cur = self.head # set starting point to head node
        for _ in range(index): # traverse the linked list
            cur = cur.next # set current node to next node in the linkedlist
        return cur # return the node at the given index

    def index_of(self, data):
        """
        (1) case: found data in linkedlist
        (2) case: no data found in linkedlist then raise ValueError
        """
        
        index = 0 # track iteration index starting at 0
        cur = self.head # set starting point to head node
        while cur is not None: # iterate while cur node next pointer is set
            if cur.data == data: # check if node data is equal to parameters data
                return index # case: is equal then is the data we need so return            
            cur = cur.next # case is not equal then set current node to next node in the linkedlist
            index += 1 # update index to move to next node in linkedlist
        raise ValueError() # raise here sense the data was not found in the linkedlist
    

    def contains(self, data):
        """
        (1) case: found data in linkedlist
        (2) case: no data found in linkedlist then return False
        """
        cur = self.head # set starting point to head node
        while cur is not None: # iterate while cur node next pointer is set
            if cur.data == data: # check if node data is equal to parameters data
                return True # case: is equal then is the data we need so return            
            cur = cur.next # case is not equal then set current node to next node in the linkedlist
        return False # case: no data found in linkedlist then return False

    def reverse(self):
        """
        (1) case: reverse the linkedlist
        """
        prev = None # set previous node to None
        cur = self.head # set current node to head node
        self.tail = self.head # set tail to head
        while cur is not None: # iterate while cur node next pointer is set
            nxt = cur.next # set next node to current node next node
            cur.next = prev # set current node next node to previous node
            prev = cur # set previous node to current node
            cur = nxt # set current node to next node
        self.head = prev # set head to previous node

    def to_list(self):
        """
        Converts the linked list to a Python list.

        (1) Iterates over the linked list using the __iter__ method, 
            which yields each node's data in order.
        (2) Uses the built-in list() function to collect these values into a list.
        (3) Returns the resulting list.
        """
        return list(self) # convert linked list to python list and return result
    
    def clear(self):
        """
        (1) Clear the linked list by setting the head and tail to None and the size to 0.
        """
        self.head = None # set head to None
        self.tail = None # set tail to None
        self.size = 0 # set size to 0


    def extend(self, other):
        """
        (1) Extend the linked list by appending all nodes from another linked list.
        """
        self.tail.next = other.head # set current tail's next to other head
        self.tail = other.tail # set new tail to other tail
        self.size += other.size # update size by adding other size

    def sort(self):
        """
        (1) Sort the linked list using the built-in sorted function.
        """
        nodes = self.to_list() # convert linked list to python list
        nodes.sort() # sort the linked list using the built-in sorted function
        self.clear() # clear the linked list
        for node in nodes: # iterate through the sorted nodes
            self.append(node) # append the sorted nodes to the linked list