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
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    def __lt__(self, other):
        if self.rank == other.rank:
            return self.suit < other.suit
        if self.rank == 0: # I have an Ace!
            return False
        if other.rank == 0: # They have an Ace!
            return True
        return self.rank < other.rank

class Deck(deque):
    """A deck of cards. Uses python's deque"""
    def __init__(self, cards = None):
        if cards is None:
            for i,j in product(range(4), range(13)):
                self.append(Card(i,j))
        else:
            self.extend(cards)
        shuffle(self)
    def deal(self, n=1):
        return [self.popleft() for _ in range(n)]
    def shuffle(self):
        shuffle(self)
