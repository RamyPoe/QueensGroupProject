class Queue:

    """ Constructor """
    def __init__(self):
        self._data = []

    """ Returns True if there are no items in the queue """
    def isEmpty(self):
        return len(self._data) == 0

    """ Add an item to the end of the queue """
    def enqueue(self, data):
        self._data.append(data)

    """ Return and remove next item from queue """
    def dequeue(self):
        if (self.isEmpty()): return
        
        data = self._data[0]
        del self._data[0]
        return data

    """ Return value of the next item in queue """
    def peek(self):
        return self._data[0] if not self.isEmpty() else None