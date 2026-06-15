class SinglyLinkedList:
    # Initialize the list
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # Return the size of the list
    def __len__(self):
        return self.size

    # Iterate through the list
    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next
    

ll = SinglyLinkedList()
results = [ll.head is None, len(ll) == 0]
print("Test results:", results)