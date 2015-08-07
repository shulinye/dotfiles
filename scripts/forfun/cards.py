#!/usr/bin/python3

from random import shuffle
from collections import deque
from itertools import product

__all__ = ['Card', 'Deck']

class Card(object):
    suit_map = ['Clubs','Diamonds', 'Hearts', 'Spades']
    rank_map = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __repr__(self):
        return '<%s: %s of %s>' % (self.__class__.__name__, self.rank_map[self.rank], self.suit_map[self.suit])

class Deck(deque):
    """A deck of cards. Uses python's deque"""
    def __init__(self):
        for i,j in product(range(4), range(13)):
            self.append(Card(i,j))
        shuffle(self)
    def deal(self):
        return self.popleft()
    def shuffle(self):
        shuffle(self)
