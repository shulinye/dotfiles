#!/usr/bin/python/

"""Wrapper around heapq, to make it an object"""

import heapq

__all__ = ['Heap']

class Heap(object):
    """Wrapper around python's heapq module"""
    def __init__(self, h = None, key = None):
        if h is None:
            self.h = []
        elif key is None:
            self.h = list(h)
        else:
            self.h = [(key(i), i) for i in h]
        heapq.heapify(self.h)
        self.key = key
    def __len__(self):
        return len(self.h)
    def __contains__(self, item):
        if self.key is None:
            return item in self.h
        else:
            for i,j in self.h:
                if item == j:
                    return True
            return False
    def __repr__(self):
        s =  '<' + self.__class__.__name__
        if self.key:
            s += " with key " + self.key.__name__
            s += ": " + ", ".join(repr(j) for i,j in self.h[:10])
        else:
            s += ": " + ", ".join(repr(i) for i in self.h[:10])
        if len(self.h) > 10:
            s += "..."
        s += '>'
        return s
    def pop(self, index = None):
        """Removes the item at index and returns it,
        keeping the heap invariant
        
        if index is None, pops smallest element"""
        if index is None:
            val =  heapq.heappop(self.h)
        else:
            val = self.h[index]
            self.h[index] = self.h[-1]
            self.h.pop()
            heapq._siftup(self.h, index)
        if self.key:
            return val[1]
        else:
            return val
    def push(self, item):
        if self.key is None:
            heapq.heappush(self.h, item)
        else:
            heapq.heappush(self.h, (self.key(item), item))
    def pushpop(self, item):
        """Push, then pop
        
        Calls heapq.heappushpop"""
        if self.key is None:
            return heapq.heappushpop(self.h, item)
        else:
            return heapq.heappushpop(self.h, (self.key(item), item))[1]
    def heapify(self, key = None):
        """Heapifies the heap. If optional parameter
        key is supplied, uses that as the key"""
        if key is None:
            pass
        elif self.key is None:
            self.h = [(key(i), i) for i in self.h]
        else:
            self.h = [(key(j), j) for i,j in self.h]
        self.key = key
        heapq.heapify(self.h)
    def replace(self, item):
        """Pop, then push
        
        Calls heapq.heapreplace"""
        if self.key is None:
            return heapq.heapreplace(self.h, item)
        else:
            return heapq.heapreplace(self.h, (self.key(item), item))[1]
    def consume(self):
        """Outputs the heap as a sorted iterator.
        Consumes heap while doing so"""
        while self.h:
            yield self.pop()
    def verify(self):
        """Verifies my heapiness."""
        length = len(self.h)
        for index, val in enumerate(self.h):
            left_child = index*2 + 1
            if left_child >= length: break
            if self.h[left_child] < val: return False
            right_child = left_child + 1
            if right_child >= length: break
            if self.h[right_child] < val: return False
        return True
