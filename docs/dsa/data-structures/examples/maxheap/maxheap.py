class MaxHeap:
    def __init__(self, items=[]):
        super().__init__() # call the parent class constructor
        self.heap = [0] # 0 is not used, it is a placeholder
        self.size = 0

        # add the items to the heap
        if items:
            for i in items:
                self.heap.append(i) # add the item to the heap
                self.size += 1
                self._heapify_up(self.size)

    def push(self, item):
        self.heap.append(item)
        self.size += 1
        self._heapify_up(self.size)

    def peek(self):
        if self.size > 0:
            return self.heap[1]
        return False

    def pop(self):
        """
        First possibility is there are two or more values in the heap, in which case we want to swap the max value to the very end of the heap before we pop it off, and then we want to float down the value that we swapped into the top position. The second possibility is that there's only one value in the heap, in which case we can simply pop the top value off the heap and we'll have an empty heap after that And then the third possibility is we're trying to pop off an empty heap, in which case we just want to return false. There's
        """

        if self.size == 0:
            return False
        if self.size == 1:
            max_value = self.heap.pop()
            self.size = 0
            return max_value
        self._swap(1, self.size)
        max_value = self.heap.pop()
        self.size -= 1
        self._heapify_down(1)
        return max_value

    def _swap(self, i, j):
        """ 
        Swap the values at the given indices.
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self, index):
        """
        Bubble up the value at the given index.
        """
        # find the parent index
        parent_index = index // 2
        # check if the current value is greater than the parent value
        if index > 1 and self.heap[index] > self.heap[parent_index]:
            # swap the current value with the parent value
            self._swap(index, parent_index)
            # bubble up the parent value
            self._heapify_up(parent_index)
        # we're done
        return

    def _heapify_down(self, index):
        """
        Bubble down the value at the given index.
        """
        # find the index of the left child
        left_child_index = index * 2
        # find the index of the right child
        right_child_index = index * 2 + 1
        # find the index of the largest value
        largest = index
        # check if the left child value is greater than the largest value

        if (left_child_index <= self.size
                and self.heap[largest] < self.heap[left_child_index]):
            largest = left_child_index
        # check if the right child value is greater than the largest value
        if (right_child_index <= self.size
                and self.heap[largest] < self.heap[right_child_index]):
            largest = right_child_index
        # check if the largest value is not the current value
        if largest != index:
            # swap the current value with the largest value
            self._swap(index, largest)
            # bubble down the largest value
            self._heapify_down(largest)
        # we're done
        return # we're done