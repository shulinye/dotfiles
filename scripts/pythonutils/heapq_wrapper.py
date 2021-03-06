#!/usr/bin/python/

"""Wrapper around heapq, to make it an object"""

import heapq
import itertools
from .utils import NullArgument

__all__ = ['Heap']


class Heap(object):
    """Wrapper around python's heapq module"""
    def __init__(self, heap=None, key=None):
        if heap is None:
            self._heap = []
        elif key is None:
            self._heap = list(heap)
        else:
            self._heap = [(key(i), i) for i in heap]
        heapq.heapify(self._heap)
        self.key = key

    def __len__(self):
        return len(self._heap)

    def __contains__(self, item):
        if self.key is None:
            return item in self._heap
        else:
            for _, value in self._heap:
                if item == value:
                    return True
            return False

    def __repr__(self):
        s = ['<' + self.__class__.__name__]
        if self.key:
            s.append(" with key {}: {}".format(self.key.__name__, ", ".join(repr(value) for _, value in self._heap[:10])))
        else:
            s.append(": " + ", ".join([repr(value) for value in self._heap[:10]]))
        if len(self._heap) > 10:
            s.append("...")
        s.append('>')
        return ''.join(s)

    def __str__(self):
        if self.key:
            return '[%s]' % ', '.join([repr(val) for _, val in self._heap])
        else:
            return str(self._heap)

    def count(self, x):
        if self.key:
            return sum(x == val for _, val in self._heap)
        else:
            return self._heap.count(x)

    def extend(self, *iterables, key=NullArgument):
        if key is NullArgument:
            if self.key:
                self._heap
        elif key is None:
            pass
        raise NotImplemented

    def pop(self, index=None):
        """Removes the item at index and returns it,
        keeping the heap invariant
        
        if index is None, pops smallest element"""
        if index is None:
            val = heapq.heappop(self._heap)
        elif index == len(self._heap) - 1: #asking for the last element
            val = self._heap.pop()
        else:
            val = self._heap[index]
            self._heap[index] = self._heap.pop()
            heapq._siftup(self._heap, index)
        if self.key:
            return val[1]
        else:
            return val

    def push(self, item):
        if self.key is None:
            heapq.heappush(self._heap, item)
        else:
            heapq.heappush(self._heap, (self.key(item), item))

    def push_from_iterator(self, *iterables):
        if self.key is None:
            for iterable in iterables:
                for i in iterable:
                    heapq.heappush(self._heap, i)
        else:
            for iterable in iterables:
                for i in iterable:
                    heapq.heappush(self._heap, (self.key(i), i))

    def pushpop(self, item):
        """Push, then pop
        
        Calls heapq.heappushpop"""
        if self.key is None:
            return heapq.heappushpop(self._heap, item)
        else:
            return heapq.heappushpop(self._heap, (self.key(item), item))[1]

    def heapify(self, key=NullArgument):
        """Heapifies the heap. If optional parameter
        key is supplied, uses that as the key.
        If key=None, removes key"""
        if key is NullArgument:
            pass
        elif key is None:
            self._heap = [value for _, value in self._heap]
        elif self.key is None:
            self._heap = [(key(value), value) for value in self._heap]
        else:
            self._heap = [(key(value), value) for _, value in self._heap]
        self.key = key
        heapq.heapify(self._heap)

    def replace(self, item):
        """Pop, then push
        
        Calls heapq.heapreplace"""
        if self.key is None:
            return heapq.heapreplace(self._heap, item)
        else:
            return heapq.heapreplace(self._heap, (self.key(item), item))[1]

    def consume(self):
        """Outputs the heap as a sorted iterator.
        Consumes heap while doing so"""
        while self._heap:
            yield self.pop()

    def verify(self):
        """Verifies my heapiness."""
        length = len(self._heap)
        for index, val in enumerate(self._heap):
            left_child = index*2 + 1
            if left_child >= length:
                break
            if self._heap[left_child] < val:
                return False
            right_child = left_child + 1
            if right_child >= length:
                break
            if self._heap[right_child] < val:
                return False
        return True

    @classmethod
    def sort(cls, iterable, key=None):
        return cls(itertable, key).consume() 
